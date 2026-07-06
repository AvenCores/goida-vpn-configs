package main

import (
	"bufio"
	"encoding/base64"
	"encoding/json"
	"fmt"
	"net/url"
	"os"
	"path/filepath"
	"regexp"
	"strings"
	"sync"
)

type VmessPayload struct {
	Add  interface{} `json:"add"`
	Host interface{} `json:"host"`
	Ip   interface{} `json:"ip"`
	Port interface{} `json:"port"`
}

var hostPortRegex = regexp.MustCompile(`(?:@|//)([\w\.-]+):(\d{1,5})`)

func interfaceToString(val interface{}) string {
	if val == nil {
		return ""
	}
	switch v := val.(type) {
	case string:
		return v
	case float64:
		return fmt.Sprintf("%.0f", v)
	case int:
		return fmt.Sprintf("%d", v)
	default:
		return fmt.Sprintf("%v", v)
	}
}

func extractHostPort(line string) (string, string, bool) {
	if line == "" {
		return "", "", false
	}

	if strings.HasPrefix(line, "vmess://") {
		payload := line[8:]
		cleanPayload := removeAllWhitespace(payload)
		if rem := len(cleanPayload) % 4; rem > 0 {
			cleanPayload += strings.Repeat("=", 4-rem)
		}

		decodedBytes, err := base64.StdEncoding.DecodeString(cleanPayload)
		if err != nil {
			decodedBytes, err = base64.URLEncoding.DecodeString(cleanPayload)
		}

		if err == nil {
			decoded := string(decodedBytes)
			if strings.HasPrefix(decoded, "{") {
				var jp VmessPayload
				if err := json.Unmarshal(decodedBytes, &jp); err == nil {
					host := interfaceToString(jp.Add)
					if host == "" {
						host = interfaceToString(jp.Host)
					}
					if host == "" {
						host = interfaceToString(jp.Ip)
					}
					port := interfaceToString(jp.Port)
					if host != "" && port != "" {
						return host, port, true
					}
				}
			}
		}
		return "", "", false
	}

	matches := hostPortRegex.FindStringSubmatch(line)
	if len(matches) > 2 {
		return matches[1], matches[2], true
	}

	return "", "", false
}

func extractSourceName(urlStr string) string {
	parsed, err := url.Parse(urlStr)
	if err != nil {
		return "Источник"
	}
	pathParts := strings.Split(strings.Trim(parsed.Path, "/"), "/")
	if len(pathParts) > 1 {
		return pathParts[0] + "/" + pathParts[1]
	}
	return parsed.Host
}

func countNonEmptyLines(s string) int {
	count := 0
	for _, line := range strings.Split(s, "\n") {
		if strings.TrimSpace(line) != "" {
			count++
		}
	}
	return count
}

func saveToLocalFile(path string, content string) {
	if err := os.MkdirAll(filepath.Dir(path), 0755); err != nil {
		logMessage(fmt.Sprintf("⚠️ Ошибка создания директории %s: %v", filepath.Dir(path), err))
	}
	if err := os.WriteFile(path, []byte(content), 0644); err != nil {
		logMessage(fmt.Sprintf("⚠️ Ошибка записи файла %s: %v", path, err))
		return
	}
	configCount := countNonEmptyLines(content)
	logMessage(fmt.Sprintf("📁 Данные сохранены локально в %s с %d конфигами", filepath.Base(path), configCount))
}

func downloadAndSave(idx int) *struct {
	LocalPath string
	FileIndex int
} {
	url := Urls[idx]
	localPath := LocalPaths[idx]
	fileIndex := idx + 1

	data, err := fetchData(url, 10, 3, true)
	if err != nil {
		shortMsg := formatFetchError(err)
		logMessage(fmt.Sprintf("⚠️ Ошибка при скачивании %d.txt (%s): %s", fileIndex, url, shortMsg))
		return nil
	}

	data, _ = filterInsecureConfigs(localPath, data, true)

	existingData, err := os.ReadFile(localPath)
	if err == nil && string(existingData) == data {
		nonEmptyLines := countNonEmptyLines(data)
		logMessage(fmt.Sprintf("🔄 Изменений для %d.txt нет (%d конфигов).", fileIndex, nonEmptyLines))
		return nil
	}

	saveToLocalFile(localPath, data)
	return &struct {
		LocalPath string
		FileIndex int
	}{LocalPath: localPath, FileIndex: fileIndex}
}

func loadSniDomains() ([]string, error) {
	data, err := os.ReadFile(SniDomainsPath)
	if err != nil {
		return nil, err
	}
	var domains []string
	if err := json.Unmarshal(data, &domains); err != nil {
		return nil, err
	}
	return domains, nil
}

func optimizeDomains(domains []string) []string {
	s := make([]string, len(domains))
	copy(s, domains)
	for i := 0; i < len(s); i++ {
		for j := i + 1; j < len(s); j++ {
			if len(s[i]) > len(s[j]) {
				s[i], s[j] = s[j], s[i]
			}
		}
	}

	var optimized []string
	for _, d := range s {
		anySubstr := false
		for _, existing := range optimized {
			if strings.Contains(d, existing) {
				anySubstr = true
				break
			}
		}
		if !anySubstr {
			optimized = append(optimized, d)
		}
	}
	return optimized
}

func matchesAnyDomain(line string, domains []string) bool {
	lineLower := strings.ToLower(line)
	for _, d := range domains {
		if strings.Contains(lineLower, d) {
			return true
		}
	}
	return false
}

func createFilteredConfigs() string {
	sniDomains, err := loadSniDomains()
	if err != nil {
		logMessage(fmt.Sprintf("❌ Ошибка загрузки %s: %v", SniDomainsPath, err))
		return filepath.Join(GithubMirrorDir, "26.txt")
	}

	optimized := optimizeDomains(sniDomains)
	for i := range optimized {
		optimized[i] = strings.ToLower(optimized[i])
	}

	var allConfigs []string
	var configsMutex sync.Mutex

	var wg sync.WaitGroup
	for i := 1; i <= 25; i++ {
		wg.Add(1)
		go func(fileIdx int) {
			defer wg.Done()
			localPath := filepath.Join(GithubMirrorDir, fmt.Sprintf("%d.txt", fileIdx))
			
			file, err := os.Open(localPath)
			if err != nil {
				return
			}
			defer file.Close()

			var matchedLines []string
			scanner := bufio.NewScanner(file)
			buf := make([]byte, 0, 64*1024)
			scanner.Buffer(buf, 1024*1024)

			for scanner.Scan() {
				lineStripped := strings.TrimSpace(scanner.Text())
				if lineStripped != "" && matchesAnyDomain(lineStripped, optimized) {
					matchedLines = append(matchedLines, lineStripped)
				}
			}

			if err := scanner.Err(); err != nil {
				logMessage(fmt.Sprintf("⚠️ Ошибка сканирования файла %s: %v", localPath, err))
			}

			configsMutex.Lock()
			allConfigs = append(allConfigs, matchedLines...)
			configsMutex.Unlock()
		}(i)
	}
	wg.Wait()

	var totalInsecureFiltered26 int32
	var extraWg sync.WaitGroup
	type extraResult struct {
		configs []string
		removed int
	}
	extraCh := make(chan extraResult, len(ExtraUrlsFor26))

	for _, u := range ExtraUrlsFor26 {
		extraWg.Add(1)
		go func(urlStr string) {
			defer extraWg.Done()
			data, err := fetchData(urlStr, ExtraUrlTimeout, ExtraUrlMaxAttempts, false)
			if err != nil {
				logMessage(fmt.Sprintf("⚠️ Ошибка при загрузке 26.txt (%s): %s", urlStr, formatFetchError(err)))
				return
			}
			path26 := filepath.Join(GithubMirrorDir, "26.txt")
			filteredData, countRemoved := filterInsecureConfigs(path26, data, false)

			var lines []string
			scanner := bufio.NewScanner(strings.NewReader(filteredData))
			buf := make([]byte, 0, 64*1024)
			scanner.Buffer(buf, 1024*1024)

			for scanner.Scan() {
				lStripped := strings.TrimSpace(scanner.Text())
				if lStripped != "" {
					lines = append(lines, lStripped)
				}
			}
			if err := scanner.Err(); err != nil {
				logMessage(fmt.Sprintf("⚠️ Ошибка сканирования extra URL %s: %v", urlStr, err))
			}
			extraCh <- extraResult{configs: lines, removed: countRemoved}
		}(u)
	}

	extraWg.Wait()
	close(extraCh)

	for res := range extraCh {
		allConfigs = append(allConfigs, res.configs...)
		totalInsecureFiltered26 += int32(res.removed)
	}

	if totalInsecureFiltered26 > 0 {
		logMessage(fmt.Sprintf("ℹ️ Отфильтровано %d небезопасных конфигов для 26.txt", totalInsecureFiltered26))
	}

	seenFull := make(map[string]bool)
	seenHostPort := make(map[string]bool)
	var uniqueConfigs []string

	for _, cfg := range allConfigs {
		c := strings.TrimSpace(cfg)
		if c == "" || seenFull[c] {
			continue
		}
		seenFull[c] = true

		host, port, ok := extractHostPort(c)
		if ok {
			key := strings.ToLower(host) + ":" + port
			if seenHostPort[key] {
				continue
			}
			seenHostPort[key] = true
		}
		uniqueConfigs = append(uniqueConfigs, c)
	}

	localPath26 := filepath.Join(GithubMirrorDir, "26.txt")
	err = os.WriteFile(localPath26, []byte(strings.Join(uniqueConfigs, "\n")), 0644)
	if err != nil {
		logMessage(fmt.Sprintf("⚠️ Ошибка при сохранении 26.txt: %v", err))
	} else {
		logMessage(fmt.Sprintf("📁 Создан файл 26.txt с %d конфигами", len(uniqueConfigs)))
	}

	return localPath26
}

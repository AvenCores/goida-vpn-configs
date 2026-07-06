package main

import (
	"bufio"
	"encoding/base64"
	"fmt"
	"html"
	"net/url"
	"path/filepath"
	"regexp"
	"strings"
)

var protocolPrefixes = []string{
	"vmess://", "vless://", "trojan://", "ss://", "ssr://",
	"tuic://", "hysteria://", "hysteria2://", "hy2://",
	"socks5://", "socks4://", "wireguard://", "ssh://",
	"snell://", "brook://", "juicity://",
}

var protoRegex = regexp.MustCompile(`(?i)(vmess|vless|trojan|ss|ssr|tuic|hysteria|hysteria2|hy2|socks5|socks4|wireguard|ssh|snell|brook|juicity)://`)
var insecureRegex = regexp.MustCompile(`(?i)(?:[?&;]|3%b|%3b)(allowinsecure|allow_insecure|insecure)=(?:1|true|yes)(?:[&;#]|\s|$)`)

func hasProtocolPrefix(s string) bool {
	lower := strings.ToLower(s)
	for _, prefix := range protocolPrefixes {
		if strings.HasPrefix(lower, prefix) {
			return true
		}
	}
	return false
}

func hasAnyProtocolPrefix(s string) bool {
	lower := strings.ToLower(s)
	for _, prefix := range protocolPrefixes {
		if strings.Contains(lower, prefix) {
			return true
		}
	}
	return false
}

func removeAllWhitespace(s string) string {
	var builder strings.Builder
	builder.Grow(len(s))
	for _, r := range s {
		if r != ' ' && r != '\n' && r != '\r' && r != '\t' {
			builder.WriteRune(r)
		}
	}
	return builder.String()
}

func tryDecodeBase64(data string) string {
	if strings.Contains(data, "://") {
		return data
	}

	cleanData := removeAllWhitespace(data)
	if rem := len(cleanData) % 4; rem > 0 {
		cleanData += strings.Repeat("=", 4-rem)
	}

	decodedBytes, err := base64.StdEncoding.DecodeString(cleanData)
	if err == nil {
		decoded := string(decodedBytes)
		if hasAnyProtocolPrefix(decoded) {
			return decoded
		}
	}

	decodedBytes, err = base64.URLEncoding.DecodeString(cleanData)
	if err == nil {
		decoded := string(decodedBytes)
		if hasAnyProtocolPrefix(decoded) {
			return decoded
		}
	}

	return data
}

func unescapeConfig(s string) string {
	if !strings.Contains(s, "&") && !strings.Contains(s, "%") {
		return s
	}
	decodedHtml := s
	if strings.Contains(s, "&") {
		decodedHtml = html.UnescapeString(s)
	}
	if strings.Contains(decodedHtml, "%") {
		decodedUrl, err := url.QueryUnescape(decodedHtml)
		if err == nil {
			return decodedUrl
		}
	}
	return decodedHtml
}

func filterInsecureConfigs(localPath string, data string, logEnabled bool) (string, int) {
	data = tryDecodeBase64(data)

	data = protoRegex.ReplaceAllString(data, "\n${1}://")

	var result []string
	insecureCount := 0

	scanner := bufio.NewScanner(strings.NewReader(data))
	buf := make([]byte, 0, 64*1024)
	scanner.Buffer(buf, 1024*1024)

	for scanner.Scan() {
		lineStripped := strings.TrimSpace(scanner.Text())
		if lineStripped == "" {
			continue
		}

		if !hasProtocolPrefix(lineStripped) {
			continue
		}

		processed := unescapeConfig(lineStripped)
		if !insecureRegex.MatchString(processed) {
			result = append(result, lineStripped)
		} else {
			insecureCount++
		}
	}

	if err := scanner.Err(); err != nil {
		logMessage(fmt.Sprintf("⚠️ Ошибка сканирования при фильтрации небезопасных конфигов для %s: %v", filepath.Base(localPath), err))
	}

	if insecureCount > 0 && logEnabled {
		logMessage(fmt.Sprintf("ℹ️ Отфильтровано %d небезопасных конфигов для %s", insecureCount, filepath.Base(localPath)))
	}

	return strings.Join(result, "\n"), insecureCount
}

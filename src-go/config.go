package main

import (
	"encoding/json"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"strconv"
	"strings"
)

var (
	GitRoot         string
	SourceRoot      string
	GithubMirrorDir string
	ReadmePath      string
	SniDomainsPath  string
	UrlsPath        string
	Urls26Path      string

	Urls           []string
	ExtraUrlsFor26 []string

	GithubToken string
	RepoName    = "AvenCores/goida-vpn-configs"

	ExtraUrlTimeout     int
	ExtraUrlMaxAttempts int

	LocalPaths []string

	DefaultMaxWorkers int
)

func initConfig() {
	// -------------------- КОРЕНЬ РЕПОЗИТОРИЯ --------------------
	cmd := exec.Command("git", "rev-parse", "--show-toplevel")
	out, err := cmd.Output()
	if err == nil {
		GitRoot = strings.TrimSpace(string(out))
	} else {
		cwd, err := os.Getwd()
		if err == nil {
			GitRoot = cwd
		} else {
			GitRoot = "."
		}
	}
	GitRoot, _ = filepath.Abs(GitRoot)

	SourceRoot = filepath.Join(GitRoot, "src-go")

	GithubMirrorDir = filepath.Join(GitRoot, "githubmirror")
	ReadmePath = filepath.Join(GitRoot, "README.md")
	SniDomainsPath = filepath.Join(SourceRoot, "config", "sni_domains.json")
	UrlsPath = filepath.Join(SourceRoot, "config", "urls.json")
	Urls26Path = filepath.Join(SourceRoot, "config", "26_urls.json")

	// -------------------- ЗАГРУЗКА КОНФИГУРАЦИИ --------------------
	Urls = loadJsonList(UrlsPath)
	ExtraUrlsFor26 = loadJsonList(Urls26Path)

	if err := os.MkdirAll(GithubMirrorDir, 0755); err != nil {
		fmt.Printf("⚠️ Ошибка создания папки зеркала: %v\n", err)
	}

	GithubToken = os.Getenv("MY_TOKEN")

	ExtraUrlTimeout = getEnvInt("EXTRA_URL_TIMEOUT", 6)
	ExtraUrlMaxAttempts = getEnvInt("EXTRA_URL_MAX_ATTEMPTS", 2)
	DefaultMaxWorkers = getEnvInt("MAX_WORKERS", 16)

	LocalPaths = make([]string, len(Urls))
	for i := range Urls {
		LocalPaths[i] = filepath.Join(GithubMirrorDir, fmt.Sprintf("%d.txt", i+1))
	}
	LocalPaths = append(LocalPaths, filepath.Join(GithubMirrorDir, "26.txt"))
}

func getEnvInt(key string, defaultVal int) int {
	valStr := os.Getenv(key)
	if valStr == "" {
		return defaultVal
	}
	val, err := strconv.Atoi(valStr)
	if err != nil {
		return defaultVal
	}
	return val
}

func loadJsonList(path string) []string {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil
	}

	var arr []string
	if err := json.Unmarshal(data, &arr); err == nil {
		return arr
	}

	var obj map[string]string
	if err := json.Unmarshal(data, &obj); err == nil {
		type keyVal struct {
			key int
			val string
		}
		var list []keyVal
		for k, v := range obj {
			if num, err := strconv.Atoi(k); err == nil {
				list = append(list, keyVal{key: num, val: v})
			}
		}
		for i := 0; i < len(list); i++ {
			for j := i + 1; j < len(list); j++ {
				if list[i].key > list[j].key {
					list[i], list[j] = list[j], list[i]
				}
			}
		}
		var result []string
		for _, kv := range list {
			result = append(result, kv.val)
		}
		return result
	}

	return nil
}

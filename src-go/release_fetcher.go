package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"path/filepath"
	"regexp"
	"strings"
	"time"
)

type GHAsset struct {
	Name               string `json:"name"`
	BrowserDownloadUrl string `json:"browser_download_url"`
}

type GHRelease struct {
	Assets []GHAsset `json:"assets"`
}

func fetchVcRuntimeLink() string {
	url := "https://www.comss.ru/download/page.php?id=6271"
	logMessage("🔍 Получение ссылки на Visual C++ Runtimes...")

	htmlContent, err := fetchData(url, 15, 1, false)
	if err != nil {
		logMessage(fmt.Sprintf("❌ Ошибка при получении Visual C++ Runtimes: %v", err))
		return ""
	}

	re := regexp.MustCompile(`https://dl\.comss\.org/download/Visual-C-Runtimes[^\s'\"<>]+`)
	matches := re.FindStringSubmatch(htmlContent)
	if len(matches) > 0 {
		downloadLink := matches[0]
		logMessage(fmt.Sprintf("✅ Visual C++ Runtimes: %s", filepath.Base(downloadLink)))
		return downloadLink
	}

	logMessage("⚠️ Не удалось найти ссылку на Visual C++ Runtimes")
	return ""
}

func selectV2rayngApk(assets []GHAsset) *GHAsset {
	for i := range assets {
		nameLower := strings.ToLower(assets[i].Name)
		if strings.Contains(nameLower, "universal.apk") &&
			!strings.Contains(nameLower, "f-droid") &&
			!strings.Contains(nameLower, "fdroid") {
			return &assets[i]
		}
	}
	for i := range assets {
		nameLower := strings.ToLower(assets[i].Name)
		if strings.Contains(nameLower, "universal.apk") {
			return &assets[i]
		}
	}
	return nil
}

func fetchGHRelease(repo string) (*GHRelease, error) {
	url := fmt.Sprintf("https://api.github.com/repos/%s/releases/latest", repo)
	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		return nil, err
	}

	req.Header.Set("User-Agent", ChromeUA)
	if GithubToken != "" {
		req.Header.Set("Authorization", "Bearer "+GithubToken)
	}

	client := &http.Client{Timeout: 10 * time.Second}
	resp, err := client.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("HTTP status %d", resp.StatusCode)
	}

	var release GHRelease
	if err := json.NewDecoder(resp.Body).Decode(&release); err != nil {
		return nil, err
	}

	return &release, nil
}

func fetchLatestReleaseLinks() map[string]string {
	links := make(map[string]string)

	logMessage("🔍 Получение v2rayNG...")
	v2rayRelease, err := fetchGHRelease("2dust/v2rayNG")
	if err == nil {
		apk := selectV2rayngApk(v2rayRelease.Assets)
		if apk != nil {
			links["v2rayng-apk"] = apk.BrowserDownloadUrl
			logMessage(fmt.Sprintf("✅ v2rayNG: %s", filepath.Base(apk.BrowserDownloadUrl)))
		} else {
			logMessage("⚠️ Не удалось найти universal.apk для v2rayNG")
		}
	} else {
		logMessage(fmt.Sprintf("❌ Ошибка при получении v2rayNG: %v", err))
	}

	logMessage("🔍 Получение Throne...")
	throneRelease, err := fetchGHRelease("throneproj/Throne")
	if err == nil {
		var win10, win7, linux *GHAsset
		for i := range throneRelease.Assets {
			nameLower := strings.ToLower(throneRelease.Assets[i].Name)
			if strings.Contains(nameLower, "windows64") && !strings.Contains(nameLower, "legacy") {
				win10 = &throneRelease.Assets[i]
			}
			if strings.Contains(nameLower, "windowslegacy64") {
				win7 = &throneRelease.Assets[i]
			}
			if strings.Contains(nameLower, "linux-amd64") {
				linux = &throneRelease.Assets[i]
			}
		}

		if win10 != nil {
			links["throne-win10"] = win10.BrowserDownloadUrl
			logMessage(fmt.Sprintf("✅ Throne Win10/11: %s", filepath.Base(win10.BrowserDownloadUrl)))
		}
		if win7 != nil {
			links["throne-win7"] = win7.BrowserDownloadUrl
			logMessage(fmt.Sprintf("✅ Throne Win7/8/8.1: %s", filepath.Base(win7.BrowserDownloadUrl)))
		}
		if linux != nil {
			links["throne-linux"] = linux.BrowserDownloadUrl
			logMessage(fmt.Sprintf("✅ Throne Linux: %s", filepath.Base(linux.BrowserDownloadUrl)))
		}
	} else {
		logMessage(fmt.Sprintf("❌ Ошибка при получении Throne: %v", err))
	}

	return links
}

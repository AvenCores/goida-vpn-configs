package main

import (
	"fmt"
	"os"
	"regexp"
	"strings"
)

func updateReadmeDownloadLinks(links map[string]string, vcRuntimeLink string) {
	if len(links) == 0 && vcRuntimeLink == "" {
		logMessage("⚠️ Нет новых ссылок для обновления в README.md")
		return
	}

	readmeData, err := os.ReadFile(ReadmePath)
	if err != nil {
		logMessage(fmt.Sprintf("❌ README.md не найден: %v", err))
		return
	}

	content := string(readmeData)
	originalContent := content

	if apkLink, ok := links["v2rayng-apk"]; ok {
		reV2 := regexp.MustCompile(`(\*\*1\.\*\* Скачиваем \*\*«v2rayNG»\*[^\n]*?\[Ссылка\]\()https://github\.com/2dust/v2rayNG/releases/download/[^)]+(\))`)
		if reV2.MatchString(content) {
			content = reV2.ReplaceAllString(content, `${1}`+apkLink+`${2}`)
			logMessage("✅ Ссылка на v2rayNG обновлена в README.md")
		} else {
			logMessage("⚠️ Не найдена ссылка на v2rayNG в README.md")
		}
	}

	if tWin10, ok := links["throne-win10"]; ok {
		reT10 := regexp.MustCompile(`(\[Windows 10/11\]\()https://github\.com/throneproj/Throne/releases/download/[^)]+(\))`)
		if reT10.MatchString(content) {
			content = reT10.ReplaceAllString(content, `${1}`+tWin10+`${2}`)
			logMessage("✅ Ссылка на Throne Win10/11 обновлена в README.md")
		}
	}
	if tWin7, ok := links["throne-win7"]; ok {
		reT7 := regexp.MustCompile(`(\[Windows 7/8/8\.1\]\()https://github\.com/throneproj/Throne/releases/download/[^)]+(\))`)
		if reT7.MatchString(content) {
			content = reT7.ReplaceAllString(content, `${1}`+tWin7+`${2}`)
			logMessage("✅ Ссылка на Throne Win7/8/8.1 обновлена в README.md")
		}
	}
	if tLinux, ok := links["throne-linux"]; ok {
		reTLinux := regexp.MustCompile(`(\[Linux\]\()https://github\.com/throneproj/Throne/releases/download/[^)]+(\))`)
		if reTLinux.MatchString(content) {
			content = reTLinux.ReplaceAllString(content, `${1}`+tLinux+`${2}`)
			logMessage("✅ Ссылка на Throne Linux обновлена в README.md")
		}
	}

	if vcRuntimeLink != "" {
		reVC := regexp.MustCompile(`(\*\*4\.\*\* Скачиваем архив и распаковываем[^\n]*?\[Ссылка\]\()https://[^\)]+(\))`)
		if reVC.MatchString(content) {
			content = reVC.ReplaceAllString(content, `${1}`+vcRuntimeLink+`${2}`)
			logMessage("✅ Ссылка на Visual C++ Runtimes обновлена в README.md")
		} else {
			logMessage("⚠️ Не найдена ссылка на Visual C++ Runtimes в README.md")
		}
	}

	if content != originalContent {
		if err := os.WriteFile(ReadmePath, []byte(content), 0644); err != nil {
			logMessage(fmt.Sprintf("⚠️ Ошибка при записи README.md: %v", err))
		} else {
			logMessage("📝 Ссылки на скачивание в README.md обновлены")
		}
	} else {
		logMessage("ℹ️ Ссылки на скачивание не требуют изменений")
	}
}

func updateReadmeTable() {
	readmeData, err := os.ReadFile(ReadmePath)
	if err != nil {
		logMessage(fmt.Sprintf("❌ README.md не найден: %v", err))
		return
	}

	oldContent := string(readmeData)

	timePart, datePart := "", ""
	parts := strings.Split(OffsetStr, " | ")
	if len(parts) == 2 {
		timePart = parts[0]
		datePart = parts[1]
	}

	tableHeader := "| № | Файл | Источник | Время | Дата |\n|--|--|--|--|--|"
	var tableRows []string

	allUrlsWith26 := append([]string{}, Urls...)
	allUrlsWith26 = append(allUrlsWith26, "")

	for i, urlStr := range allUrlsWith26 {
		fileIdx := i + 1
		filename := fmt.Sprintf("%d.txt", fileIdx)
		rawFileUrl := fmt.Sprintf("https://github.com/%s/raw/refs/heads/main/githubmirror/%s", RepoName, filename)

		var sourceColumn string
		if fileIdx <= 25 {
			sourceName := extractSourceName(urlStr)
			sourceColumn = fmt.Sprintf("[%s](%s)", sourceName, urlStr)
		} else {
			sourceName := "Обход SNI/CIDR белых списков"
			sourceColumn = fmt.Sprintf("[%s](%s)", sourceName, rawFileUrl)
		}

		var updateTime, updateDate string
		if isFileUpdated(fileIdx) {
			updateTime = timePart
			updateDate = datePart
		} else {
			escapedFilename := regexp.QuoteMeta(filename)
			patternStr := fmt.Sprintf(`\|\s*%d\s*\|\s*\[`+"`"+`%s`+"`"+`\][^|]*\|[^|]*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|`, fileIdx, escapedFilename)
			reRow := regexp.MustCompile(patternStr)
			matches := reRow.FindStringSubmatch(oldContent)
			if len(matches) > 2 {
				updateTime = strings.TrimSpace(matches[1])
				updateDate = strings.TrimSpace(matches[2])
			} else {
				updateTime = "Никогда"
				updateDate = "Никогда"
			}
		}

		tableRows = append(tableRows, fmt.Sprintf("| %d | [`%s`](%s) | %s | %s | %s |", fileIdx, filename, rawFileUrl, sourceColumn, updateTime, updateDate))
	}

	newTable := tableHeader + "\n" + strings.Join(tableRows, "\n")

	reTable := regexp.MustCompile(`(?s)\| № \| Файл \| Источник \| Время \| Дата \|\s*\n\|--\|--\|--\|--\|--\|(\s*\n\|[^\r\n]*)*`)
	
	hasStats := strings.Contains(oldContent, "## 📊 Статистика репозитория")
	
	var newContent string
	repoStats := getRepoStats()
	
	if repoStats != nil {
		statsSection := "## 📊 Статистика репозитория\n" + buildRepoStatsTable(repoStats) + "\n"
		if hasStats {
			newContent = reTable.ReplaceAllString(oldContent, newTable)
			reStats := regexp.MustCompile(`(?s)## 📊 Статистика репозитория\s*\n\| Показатель \| Значение \|\s*\n\|--\|--\|(\s*\n\|[^\r\n]*)*`)
			newContent = reStats.ReplaceAllString(newContent, statsSection)
		} else {
			newContent = reTable.ReplaceAllString(oldContent, newTable + "\n\n" + statsSection)
		}
	} else {
		logMessage("⚠️ Статистика репозитория недоступна, раздел не обновлён.")
		newContent = reTable.ReplaceAllString(oldContent, newTable)
	}

	if newContent == oldContent {
		logMessage("📝 README.md не требует изменений")
		return
	}

	if err := os.WriteFile(ReadmePath, []byte(newContent), 0644); err != nil {
		logMessage(fmt.Sprintf("⚠️ Ошибка при записи README.md: %v", err))
	} else {
		logMessage("📝 README.md обновлён")
	}
}

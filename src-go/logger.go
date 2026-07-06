package main

import (
	"regexp"
	"strconv"
	"sync"
	"time"
)

var (
	logsByFile   = make(map[int][]string)
	logMutex     sync.Mutex
	updatedFiles = make(map[int]bool)
	updatedMutex sync.Mutex

	githubmirrorIndexRe = regexp.MustCompile(`(?:githubmirror/)?(\d+)\.txt`)
	OffsetStr           string
)

func initLogger() {
	msk := time.FixedZone("MSK", 3*60*60)
	now := time.Now().In(msk)
	OffsetStr = now.Format("15:04 (МСК) | 02.01.2006")
}

func extractIndex(msg string) int {
	matches := githubmirrorIndexRe.FindStringSubmatch(msg)
	if len(matches) > 1 {
		idx, err := strconv.Atoi(matches[1])
		if err == nil {
			return idx
		}
	}
	return 0
}

func logMessage(message string) {
	idx := extractIndex(message)
	logMutex.Lock()
	logsByFile[idx] = append(logsByFile[idx], message)
	logMutex.Unlock()
}

func markFileUpdated(idx int) {
	updatedMutex.Lock()
	updatedFiles[idx] = true
	updatedMutex.Unlock()
}

func isFileUpdated(idx int) bool {
	updatedMutex.Lock()
	defer updatedMutex.Unlock()
	return updatedFiles[idx]
}

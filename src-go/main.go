package main

import (
	"flag"
	"fmt"
	"os"
	"sort"
	"sync"
)

func main() {
	dryRun := flag.Bool("dry-run", false, "Сохранять файлы локально и делать коммит, но не пушить")
	flag.Parse()

	initConfig()
	initLogger()

	maxWorkersDownload := DefaultMaxWorkers
	if maxWorkersDownload > len(Urls) {
		maxWorkersDownload = len(Urls)
	}
	if maxWorkersDownload < 1 {
		maxWorkersDownload = 1
	}

	type taskResult struct {
		fileIndex int
	}

	sem := make(chan struct{}, maxWorkersDownload)
	var wg sync.WaitGroup
	resultCh := make(chan taskResult, len(Urls))

	for i := 0; i < len(Urls); i++ {
		wg.Add(1)
		go func(idx int) {
			defer wg.Done()
			sem <- struct{}{}
			defer func() { <-sem }()

			res := downloadAndSave(idx)
			if res != nil {
				resultCh <- taskResult{fileIndex: res.FileIndex}
			}
		}(i)
	}

	wg.Wait()
	close(resultCh)

	for res := range resultCh {
		markFileUpdated(res.fileIndex)
	}

	localPath26 := createFilteredConfigs()
	if _, err := os.Stat(localPath26); err == nil {
		markFileUpdated(26)
	}

	releaseLinks := fetchLatestReleaseLinks()
	vcRuntimeLink := fetchVcRuntimeLink()
	updateReadmeDownloadLinks(releaseLinks, vcRuntimeLink)

	updateReadmeTable()
	gitCommitAndPush(*dryRun)

	logMutex.Lock()
	var orderedKeys []int
	for k := range logsByFile {
		if k != 0 {
			orderedKeys = append(orderedKeys, k)
		}
	}
	sort.Ints(orderedKeys)

	var outputLines []string
	for _, k := range orderedKeys {
		outputLines = append(outputLines, fmt.Sprintf("----- %d.txt -----", k))
		outputLines = append(outputLines, logsByFile[k]...)
	}
	if len(logsByFile[0]) > 0 {
		outputLines = append(outputLines, "----- Общие сообщения -----")
		outputLines = append(outputLines, logsByFile[0]...)
	}
	logMutex.Unlock()

	for _, line := range outputLines {
		fmt.Println(line)
	}
}

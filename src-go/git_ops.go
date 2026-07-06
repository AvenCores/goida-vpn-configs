package main

import (
	"fmt"
	"os/exec"
	"path/filepath"
)

func gitCommitAndPush(dryRun bool) {
	relGithubMirror, err := filepath.Rel(GitRoot, GithubMirrorDir)
	if err != nil {
		relGithubMirror = GithubMirrorDir
	}
	relReadme, err := filepath.Rel(GitRoot, ReadmePath)
	if err != nil {
		relReadme = ReadmePath
	}

	cmdAdd := exec.Command("git", "add", relGithubMirror, relReadme)
	cmdAdd.Dir = GitRoot
	if err := cmdAdd.Run(); err != nil {
		logMessage(fmt.Sprintf("❌ Ошибка git add: %v", err))
		return
	}

	cmdDiff := exec.Command("git", "diff", "--cached", "--quiet")
	cmdDiff.Dir = GitRoot
	err = cmdDiff.Run()
	if err == nil {
		logMessage("ℹ️ Нет изменений для коммита")
		return
	}

	commitMsg := fmt.Sprintf("🚀 Автообновление репозитория: %s", OffsetStr)
	cmdCommit := exec.Command("git", "commit", "-m", commitMsg)
	cmdCommit.Dir = GitRoot
	if err := cmdCommit.Run(); err != nil {
		logMessage(fmt.Sprintf("❌ Ошибка git commit: %v", err))
		return
	}
	logMessage("✅ Коммит создан")

	if dryRun {
		logMessage("ℹ️ Dry-run: push пропущен")
		return
	}

	cmdPush := exec.Command("git", "push")
	cmdPush.Dir = GitRoot
	if err := cmdPush.Run(); err != nil {
		logMessage(fmt.Sprintf("❌ Ошибка git push: %v", err))
		return
	}
	logMessage("✅ Изменения запушены в репозиторий")
}

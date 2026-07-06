package main

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
)

type TrafficResponse struct {
	Count   int `json:"count"`
	Uniques int `json:"uniques"`
}

type RepoStats struct {
	ViewsCount    int
	ViewsUniques  int
	ClonesCount   int
	ClonesUniques int
}

func getRepoStats() *RepoStats {
	if GithubToken == "" {
		logMessage("⚠️ MY_TOKEN не задан — статистика репозитория недоступна")
		return nil
	}

	views, err := fetchTrafficStats("views")
	if err != nil {
		logMessage(fmt.Sprintf("⚠️ Не удалось получить просмотры: %v", err))
		return nil
	}

	clones, err := fetchTrafficStats("clones")
	if err != nil {
		logMessage(fmt.Sprintf("⚠️ Не удалось получить клоны: %v", err))
		return nil
	}

	return &RepoStats{
		ViewsCount:    views.Count,
		ViewsUniques:  views.Uniques,
		ClonesCount:   clones.Count,
		ClonesUniques: clones.Uniques,
	}
}

func fetchTrafficStats(statType string) (*TrafficResponse, error) {
	url := fmt.Sprintf("https://api.github.com/repos/%s/traffic/%s", RepoName, statType)
	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		return nil, err
	}

	req.Header.Set("Accept", "application/vnd.github+json")
	req.Header.Set("Authorization", "Bearer "+GithubToken)
	req.Header.Set("X-GitHub-Api-Version", "2022-11-28")
	req.Header.Set("User-Agent", "Go-http-client")

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		body, _ := io.ReadAll(resp.Body)
		return nil, fmt.Errorf("HTTP status %d: %s", resp.StatusCode, string(body))
	}

	var tr TrafficResponse
	if err := json.NewDecoder(resp.Body).Decode(&tr); err != nil {
		return nil, err
	}

	return &tr, nil
}

func formatIntWithCommas(v int) string {
	s := fmt.Sprintf("%d", v)
	if len(s) <= 3 {
		return s
	}
	var res []byte
	n := len(s)
	for i := 0; i < n; i++ {
		res = append(res, s[i])
		if (n-i-1)%3 == 0 && i != n-1 {
			res = append(res, ',')
		}
	}
	return string(res)
}

func buildRepoStatsTable(stats *RepoStats) string {
	header := "| Показатель | Значение |\n|--|--|"
	rows := []string{
		fmt.Sprintf("| Просмотры (14Д) | %s |", formatIntWithCommas(stats.ViewsCount)),
		fmt.Sprintf("| Клоны (14Д) | %s |", formatIntWithCommas(stats.ClonesCount)),
		fmt.Sprintf("| Уникальные клоны (14Д) | %s |", formatIntWithCommas(stats.ClonesUniques)),
		fmt.Sprintf("| Уникальные посетители (14Д) | %s |", formatIntWithCommas(stats.ViewsUniques)),
	}
	res := header
	for _, row := range rows {
		res += "\n" + row
	}
	return res
}

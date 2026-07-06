package main

import (
	"context"
	"crypto/tls"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"strings"
	"time"
)

const ChromeUA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36"

var (
	secureTransport = &http.Transport{
		MaxIdleConns:        100,
		MaxIdleConnsPerHost: 20,
	}
	insecureTransport = &http.Transport{
		MaxIdleConns:        100,
		MaxIdleConnsPerHost: 20,
		TLSClientConfig:     &tls.Config{InsecureSkipVerify: true},
	}

	secureClient = &http.Client{
		Transport: secureTransport,
	}
	insecureClient = &http.Client{
		Transport: insecureTransport,
	}
)

func fetchData(
	urlStr string,
	timeoutSec int,
	maxAttempts int,
	allowHttpDowngrade bool,
) (string, error) {
	var lastErr error
	for attempt := 1; attempt <= maxAttempts; attempt++ {
		modifiedUrl := urlStr
		verify := true

		switch attempt {
		case 2:
			verify = false
		case 3:
			parsed, err := url.Parse(urlStr)
			if err == nil && parsed.Scheme == "https" && allowHttpDowngrade {
				parsed.Scheme = "http"
				modifiedUrl = parsed.String()
			}
			verify = false
		}

		ctx, cancel := context.WithTimeout(context.Background(), time.Duration(timeoutSec)*time.Second)
		req, err := http.NewRequestWithContext(ctx, "GET", modifiedUrl, nil)
		if err != nil {
			cancel()
			lastErr = err
			continue
		}

		req.Header.Set("User-Agent", ChromeUA)

		var client *http.Client
		if verify {
			client = secureClient
		} else {
			client = insecureClient
		}

		resp, err := client.Do(req)
		if err != nil {
			cancel()
			lastErr = err
			continue
		}

		bodyBytes, err := io.ReadAll(resp.Body)
		resp.Body.Close()
		cancel()

		if err != nil {
			lastErr = err
			continue
		}

		if resp.StatusCode < 200 || resp.StatusCode >= 300 {
			lastErr = fmt.Errorf("HTTP %d: %s", resp.StatusCode, string(bodyBytes))
			continue
		}

		return string(bodyBytes), nil
	}

	return "", lastErr
}

func formatFetchError(err error) string {
	if err == nil {
		return ""
	}
	msg := err.Error()
	if strings.Contains(msg, "context deadline exceeded") || strings.Contains(msg, "timeout") {
		if strings.Contains(msg, "dial") {
			return "Connect timeout"
		}
		return "Timeout"
	}
	if strings.Contains(msg, "certificate") || strings.Contains(msg, "tls") || strings.Contains(msg, "handshake") {
		return "TLS error"
	}
	if strings.Contains(msg, "connection refused") || strings.Contains(msg, "no such host") {
		return "Connection error"
	}
	if len(msg) > 160 {
		return msg[:160] + "…"
	}
	return msg
}

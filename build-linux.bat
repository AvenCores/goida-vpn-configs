@echo off
echo Building Go project for Linux (amd64)...
set GOOS=linux
set GOARCH=amd64
if not exist loader mkdir loader
cd src-go
go build -o ../loader/goida-vpn-configs
cd ..
echo Done! Binary generated at loader/goida-vpn-configs
pause

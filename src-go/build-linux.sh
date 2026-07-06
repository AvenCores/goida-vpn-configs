#!/bin/bash
echo "Building Go project for Linux (amd64)..."
export GOOS=linux
export GOARCH=amd64
mkdir -p ../loader
go build -o ../loader/goida-vpn-configs
echo "Done! Binary generated at loader/goida-vpn-configs"

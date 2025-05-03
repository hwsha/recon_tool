#!/bin/bash

# Exit on error
set -e

# Declare Go tools and their install paths
declare -A go_tools=(
  [subfinder]="github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest"
  [shuffledns]="github.com/projectdiscovery/shuffledns/cmd/shuffledns@latest"
  [httpx]="github.com/projectdiscovery/httpx/cmd/httpx@latest"
  [urlfinder]="github.com/projectdiscovery/urlfinder/cmd/urlfinder@latest"
  [katana]="github.com/projectdiscovery/katana/cmd/katana@latest"
  [nuclei]="github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest"
)

GO_BIN="$HOME/go/bin"
MASSDNS_BIN="/usr/bin/massdns"

echo "[*] Checking for Go..."
if ! go version >/dev/null 2>&1; then
    echo "[-] Go is not installed. Please install Go from https://golang.org/dl/"
    exit 1
else
    echo "[+] Go is installed: $(go version)"
fi

echo "[*] Checking for ProjectDiscovery tools..."
for tool in "${!go_tools[@]}"; do
    if [ -f "$GO_BIN/$tool" ]; then
        echo "[+] $tool is already installed at $GO_BIN/$tool"
    else
        echo "[*] $tool not found. Installing..."
        go install "${go_tools[$tool]}"
    fi
done

echo "[*] Checking for massdns..."
if [ -f "$MASSDNS_BIN" ]; then
    echo "[+] massdns is already installed at $MASSDNS_BIN"
else
    echo "[*] massdns not found. Cloning and building..."
    git clone https://github.com/blechschmidt/massdns.git /tmp/massdns
    cd /tmp/massdns || exit 1
    make
    sudo cp bin/massdns "$MASSDNS_BIN"
    echo "[+] massdns installed to $MASSDNS_BIN"
    cd - >/dev/null || exit
fi

echo "[+] All dependencies checked and installed."

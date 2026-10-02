#!/usr/bin/env bash
# Download every docker project (submodule) at the commit recorded in Dockers.
set -euo pipefail
cd "$(dirname "$0")"

git submodule sync --recursive
git submodule update --init --recursive

echo "Downloaded:"
git config -f .gitmodules --get-regexp '\.path$' | awk '{print "  - " $2}'

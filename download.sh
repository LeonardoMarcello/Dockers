#!/usr/bin/env bash
# Download only the given docker project(s).
# Usage: ./download.sh <project> [<project> ...]   (no args: list available projects)
set -euo pipefail
cd "$(dirname "$0")"

mapfile -t available < <(git config -f .gitmodules --get-regexp '\.path$' | awk '{print $2}')

if [ $# -eq 0 ]; then
    echo "Usage: $0 <project> [<project> ...]"
    echo "Available projects:"
    printf '  - %s\n' "${available[@]}"
    exit 1
fi

paths=()
for arg in "$@"; do
    p="${arg%/}"
    if [[ ! " ${available[*]} " =~ " $p " ]]; then
        echo "Unknown project: $p (run $0 without arguments to list them)" >&2
        exit 1
    fi
    paths+=("$p")
done

git submodule sync --recursive -- "${paths[@]}"
git submodule update --init --recursive -- "${paths[@]}"
echo "Downloaded: ${paths[*]}"

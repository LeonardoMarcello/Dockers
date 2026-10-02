#!/usr/bin/env bash
# Update Dockers and bring the downloaded docker projects to the latest commit of their branch (main).
# Usage: ./update.sh                 update every downloaded project
#        ./update.sh <project> ...   update only the given project(s)
set -euo pipefail
cd "$(dirname "$0")"

git pull --ff-only
git submodule sync --recursive

if [ $# -gt 0 ]; then
    paths=("${@%/}")
else
    # Only projects already downloaded (use download.sh / download_all.sh for the others)
    mapfile -t paths < <(git submodule status | grep -v '^-' | awk '{print $2}')
fi

failed=()
for p in "${paths[@]}"; do
    name=$(git config -f .gitmodules --get-regexp '\.path$' | awk -v p="$p" '$2 == p {sub(/^submodule\./, "", $1); sub(/\.path$/, "", $1); print $1}')
    if [ -z "$name" ]; then
        echo "Unknown project: $p" >&2
        failed+=("$p")
        continue
    fi
    branch=$(git config -f .gitmodules "submodule.$name.branch" || echo main)

    echo "== $p ($branch)"
    git submodule update --init --recursive -- "$p"
    if git -C "$p" switch -q "$branch" && git -C "$p" pull --ff-only; then
        git -C "$p" submodule update --init --recursive
    else
        echo "!! Could not update $p (uncommitted changes or diverged branch?)" >&2
        failed+=("$p")
    fi
done

if [ ${#failed[@]} -gt 0 ]; then
    echo "Failed: ${failed[*]}" >&2
    exit 1
fi
echo "All up to date."

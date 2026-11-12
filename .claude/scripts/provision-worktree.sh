#!/usr/bin/env bash
# Provision a git worktree of api-docs. Run from inside the worktree:
#   bash .claude/scripts/provision-worktree.sh
# Docs-only repo: no package.json, no env files. The preview runs via
# `pnpm dlx mint dev`, which needs nothing installed. Add copies or installs
# here if the repo ever gains gitignored files a worktree needs.
set -euo pipefail
case "$PWD" in */.claude/worktrees/*) ;; *) echo "ERROR: run from inside a worktree" >&2; exit 1 ;; esac
main_root="${PWD%%/.claude/worktrees/*}"
rest="${PWD#*/.claude/worktrees/}"
cd "$main_root/.claude/worktrees/${rest%%/*}"
echo "api-docs worktree ready: nothing to copy or install"

#!/bin/bash
# sync-upstream.sh - Check upstream changes and guide sync decisions
# Usage: ./scripts/sync-upstream.sh [--dry-run]
#   --dry-run : Show diff but don't apply anything

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

DRY_RUN=false
if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN=true
fi

UPSTREAM="upstream"
MAIN_BRANCH="main"

# Files we track (P0/P1 translated scope)
TRANSLATED_FILES=(
  "README.md"
  "guide/cheatsheet.md"
  "guide/learning-path/README.md"
  "guide/learning-path/01-installation.md"
  "guide/learning-path/02-core-loop.md"
  "guide/learning-path/03-memory.md"
  "guide/learning-path/04-agents.md"
  "guide/learning-path/05-skills.md"
  "guide/learning-path/06-hooks.md"
)

echo "=== Upstream Sync Check ==="
echo "Checking: $UPSTREAM/$MAIN_BRANCH → origin/$MAIN_BRANCH"
echo "Date: $(date -u '+%Y-%m-%d %H:%M UTC')"
echo ""

# Step 1: Fetch upstream
echo "① Fetching upstream..."
if ! git fetch "$UPSTREAM" 2>&1; then
  echo "❌ Failed to fetch upstream. Check remote: git remote -v"
  exit 1
fi
echo ""

# Step 2: Find new upstream commits affecting our scope
echo "② New upstream commits (tracked scope):"
NEW_COMMITS=$(git log --oneline "$UPSTREAM/$MAIN_BRANCH" --not "$MAIN_BRANCH" -- 'guide/*.md' 'docs/*.md' 'README.md' 2>&1)

if [[ -z "$NEW_COMMITS" ]]; then
  echo "   No new upstream changes in tracked scope."
  exit 0
fi

echo "$NEW_COMMITS" | head -20
TOTAL=$(echo "$NEW_COMMITS" | wc -l | tr -d ' ')
echo "   Total: $TOTAL new commit(s)"
echo ""

# Step 3: Check which changed files are translated vs untranslated
echo "③ Changed files analysis:"
CHANGED_FILES=$(git diff --name-only "$MAIN_BRANCH".."$UPSTREAM/$MAIN_BRANCH" -- 'guide/*.md' 'docs/*.md' 'README.md')

for file in $CHANGED_FILES; do
  # Check if file exists in our branch (might be new upstream file)
  if ! git cat-file -e "$MAIN_BRANCH:$file" 2>/dev/null; then
    echo "   🆕 $file → NEW file (will checkout)"
    continue
  fi

  # Check if this is a translated file
  IS_TRANSLATED=false
  for tf in "${TRANSLATED_FILES[@]}"; do
    if [[ "$file" == "$tf" ]]; then
      IS_TRANSLATED=true
      break
    fi
  done

  if $IS_TRANSLATED; then
    echo "   🔴 $file → TRANSLATED (needs manual diff)"
  else
    echo "   🟢 $file → UNTRANSLATED (safe to checkout)"
  fi
done
echo ""

# Step 4: Show actionable commands
echo "④ Recommended actions:"

for file in $CHANGED_FILES; do
  if ! git cat-file -e "$MAIN_BRANCH:$file" 2>/dev/null; then
    echo "   git checkout $UPSTREAM/$MAIN_BRANCH -- '$file'  # 🆕 new file"
    continue
  fi

  IS_TRANSLATED=false
  for tf in "${TRANSLATED_FILES[@]}"; do
    if [[ "$file" == "$tf" ]]; then
      IS_TRANSLATED=true
      break
    fi
  done

  if $IS_TRANSLATED; then
    echo "   # $file → review manually:"
    echo "   git diff $MAIN_BRANCH..$UPSTREAM/$MAIN_BRANCH -- '$file'"
  else
    echo "   git checkout $UPSTREAM/$MAIN_BRANCH -- '$file'  # 🟢 untranslated"
  fi
done
echo ""

# Step 5: Summary
echo "=== Summary ==="
echo "Translated files with upstream changes: $(git diff --name-only "$MAIN_BRANCH".."$UPSTREAM/$MAIN_BRANCH" -- "${TRANSLATED_FILES[@]}" 2>/dev/null | wc -l | tr -d ' ')"
echo "Untranslated files to auto-sync: $(git diff --name-only "$MAIN_BRANCH".."$UPSTREAM/$MAIN_BRANCH" -- 'guide/*.md' 'docs/*.md' 'README.md' 2>/dev/null | wc -l | tr -d ' ')"
echo ""

if $DRY_RUN; then
  echo "✅ Dry-run complete. No changes applied."
else
  echo "⚠️  Review the list above before applying."
  echo "   Unchanged files that are untranslated can be checked out directly."
  echo "   Translated files need manual review."
fi

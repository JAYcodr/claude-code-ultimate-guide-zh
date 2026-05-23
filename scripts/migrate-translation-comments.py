"""
Migrate HTML comments about translation to YAML comments (when frontmatter exists),
or remove them entirely (when no frontmatter).

Before (has frontmatter):
  <!-- 中文翻译版 · 基于上游 commit: xxx -->
  ---
  title: "..."

After:
  ---
  # 中文翻译版 · 基于上游 commit: xxx
  title: "..."

Before (no frontmatter):
  <!-- 中文翻译版 · 基于上游 commit: xxx -->
  # Heading

After:
  # Heading
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCLUDE_DIRS = {"node_modules", ".git", "claudedocs", "whitepapers"}

COMMENT_RE = re.compile(
    rb"^<!--\s+(\S[\s\S]*?\S)\s+-->\s*$"
)

def should_skip(dirpath):
    parts = dirpath.replace(ROOT, "").lstrip(os.sep).split(os.sep)
    return any(p in EXCLUDE_DIRS for p in parts)


def migrate_file(filepath):
    with open(filepath, "rb") as f:
        content = f.read()

    lines = content.split(b"\n")
    if not lines:
        return False

    first_line = lines[0].rstrip(b"\r")
    match = COMMENT_RE.match(first_line)
    if not match:
        return False

    comment_text = match.group(1).decode("utf-8")

    # Verify this is a translation comment
    if "\u4e2d\u6587" not in comment_text and "\u7ffb\u8bd1" not in comment_text:
        return False

    # Find YAML frontmatter opener (skip blank lines)
    frontmatter_idx = None
    for i in range(1, len(lines)):
        stripped = lines[i].rstrip(b"\r")
        if stripped == b"":
            continue
        if stripped == b"---":
            frontmatter_idx = i
            break
        break  # Non-blank, non-frontmatter -> not our case

    if frontmatter_idx is not None and frontmatter_idx < len(lines) - 1:
        # Build new content: keep ---, insert YAML comment, skip old comment + blank lines
        new_lines = [b"---", f"# {comment_text}".encode("utf-8")]
        new_lines.extend(lines[frontmatter_idx + 1:])
    else:
        # No frontmatter: just remove the HTML comment
        new_lines = lines[1:]

    new_content = b"\n".join(new_lines)

    # Preserve trailing newline if original had one
    if content.endswith(b"\n"):
        new_content += b"\n"

    with open(filepath, "wb") as f:
        f.write(new_content)

    return True


def main():
    migrated = 0
    errors = 0

    for dirpath, dirnames, filenames in os.walk(ROOT):
        if should_skip(dirpath):
            continue
        for fn in filenames:
            if not fn.endswith(".md"):
                continue
            fpath = os.path.join(dirpath, fn)
            try:
                if migrate_file(fpath):
                    print(f"  migrated: {os.path.relpath(fpath, ROOT)}")
                    migrated += 1
            except Exception as e:
                print(f"  ERROR: {os.path.relpath(fpath, ROOT)}: {e}", file=sys.stderr)
                errors += 1

    print(f"\nDone: {migrated} files migrated, {errors} errors")


if __name__ == "__main__":
    main()

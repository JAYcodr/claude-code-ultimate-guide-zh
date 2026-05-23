"""
Remove all # 中文翻译版 YAML comments from frontmatter.
Files with no frontmatter already had their HTML comments removed in the previous pass.
"""

import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCLUDE_DIRS = {"node_modules", ".git", "claudedocs", "whitepapers"}

COMMENT_PREFIX = b"# \xe4\xb8\xad\xe6\x96\x87\xe7\xbf\xbb\xe8\xaf\x91\xe7\x89\x88"

def should_skip(dirpath):
    parts = dirpath.replace(ROOT, "").lstrip(os.sep).split(os.sep)
    return any(p in EXCLUDE_DIRS for p in parts)


def remove_comment(filepath):
    with open(filepath, "rb") as f:
        content = f.read()

    lines = content.split(b"\n")
    new_lines = []
    in_frontmatter = False
    changed = False

    for line in lines:
        stripped = line.rstrip(b"\r")

        # Detect frontmatter boundaries
        if not in_frontmatter and stripped == b"---":
            in_frontmatter = True
            new_lines.append(line)
            continue

        if in_frontmatter and stripped == b"---":
            in_frontmatter = False
            new_lines.append(line)
            continue

        # Remove comment lines inside frontmatter
        if in_frontmatter and stripped.startswith(COMMENT_PREFIX):
            changed = True
            continue

        new_lines.append(line)

    if not changed:
        return False

    new_content = b"\n".join(new_lines)
    if content.endswith(b"\n"):
        new_content += b"\n"

    with open(filepath, "wb") as f:
        f.write(new_content)

    return True


def main():
    removed = 0
    errors = 0

    for dirpath, dirnames, filenames in os.walk(ROOT):
        if should_skip(dirpath):
            continue
        for fn in filenames:
            if not fn.endswith(".md"):
                continue
            fpath = os.path.join(dirpath, fn)
            try:
                if remove_comment(fpath):
                    print(f"  removed: {os.path.relpath(fpath, ROOT)}")
                    removed += 1
            except Exception as e:
                print(f"  ERROR: {os.path.relpath(fpath, ROOT)}: {e}", file=sys.stderr)
                errors += 1

    print(f"\nDone: {removed} comments removed, {errors} errors")


if __name__ == "__main__":
    main()

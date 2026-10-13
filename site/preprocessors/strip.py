#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///
"""mdBook preprocessor: drop YAML front matter and HTML comments before rendering.

Pages record their feature nodes in front matter and `<!-- node: ... -->` comments.
Neither may reach the published HTML. Comments inside fenced code blocks stay.
"""

import json
import re
import sys

FRONT_MATTER = re.compile(r"\A---\n.*?\n---\n+", re.S)
COMMENT = re.compile(r"<!--.*?-->[ \t]*\n?", re.S)
FENCE = re.compile(r"^(```|~~~)", re.M)


def strip(text: str) -> str:
    text = FRONT_MATTER.sub("", text, count=1)
    out, inside = [], False
    # Split on fence lines so comments inside code blocks survive.
    for part in re.split(r"(^(?:```|~~~).*\n?)", text, flags=re.M):
        if FENCE.match(part):
            inside = not inside
            out.append(part)
        else:
            out.append(part if inside else COMMENT.sub("", part))
    return re.sub(r"\n{3,}", "\n\n", "".join(out))


def walk(items: list) -> None:
    for item in items:
        chapter = item.get("Chapter") if isinstance(item, dict) else None
        if chapter:
            chapter["content"] = strip(chapter["content"])
            walk(chapter.get("sub_items", []))


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "supports":
        return 0
    _context, book = json.load(sys.stdin)
    walk(book.get("sections") or book.get("items") or [])
    json.dump(book, sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())

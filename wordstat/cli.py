import argparse
import re
import sys
from collections import Counter
from pathlib import Path


def count_words(text: str) -> Counter[str]:
    words = re.findall(r"\b\w+\b", text.casefold())
    return Counter(words)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Count words in a text file and show the most common ones."
    )

    parser.add_argument("file", help="Path to the text file")
    parser.add_argument(
        "-n",
        "--top",
        type=int,
        default=10,
        help="Number of top words to display (default: 10)",
    )

    args = parser.parse_args()

    if args.top < 1:
        parser.error("The number of top words must be at least 1")

    try:
        text = Path(args.file).read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    counts = count_words(text)

    for word, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))[: args.top]:
        print(f"{word}: {count}")


if __name__ == "__main__":
    main()

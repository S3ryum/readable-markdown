import argparse
import math
import re
from pathlib import Path

FENCED_CODE = re.compile(r"\x60{3}.*?\x60{3}|~~~.*?~~~", re.DOTALL)
INLINE_CODE = re.compile(r"\x60[^\x60]*\x60")
LINK = re.compile(r"!?\[([^\]]*)\]\([^)]+\)")
WORD = re.compile(r"\b[\w]+(?:['’-][\w]+)*\b", re.UNICODE)
SENTENCE = re.compile(r"[^.!?]+[.!?]+|[^.!?]+$")


def readable_text(markdown: str) -> str:
    text = FENCED_CODE.sub(" ", markdown)
    text = INLINE_CODE.sub(" ", text)
    text = LINK.sub(r"\1", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"^\s{0,3}#{1,6}\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*[-*+]\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*\d+[.)]\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"[*_~>#|]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize writing signals in a Markdown file.")
    parser.add_argument("file", type=Path)
    args = parser.parse_args()
    path = args.file.expanduser()
    try:
        markdown = path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as error:
        parser.error(str(error))
    text = readable_text(markdown)
    words = WORD.findall(text)
    sentences = [part.strip() for part in SENTENCE.findall(text) if WORD.search(part)]
    count = len(words)
    sentence_count = len(sentences)
    average_sentence = count / sentence_count if sentence_count else 0
    average_word = sum(len(word) for word in words) / count if count else 0
    minutes = max(1, math.ceil(count / 220)) if count else 0
    print(f"File: {path.name}")
    print(f"Words: {count}")
    print(f"Sentences: {sentence_count}")
    print(f"Average words per sentence: {average_sentence:.1f}")
    print(f"Average word length: {average_word:.1f} characters")
    print(f"Estimated reading time: {minutes} minute(s)")
    print("Use these figures as editing signals, not as a quality score.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

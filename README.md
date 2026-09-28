# Readable Markdown

A small Python tool that reports writing signals for a Markdown file: words, sentences, average sentence length, and estimated reading time.

## Requirements

Python 3.10 or newer. No third-party packages.

## Run

~~~sh
python readable_markdown.py article.md
~~~

Code blocks and link destinations are excluded from the word count. Reading time uses an approximate pace of 220 words per minute; it is a guide, not a grade.

---
name: ai-writing-detector
description: Detect AI-generated text and check plagiarism using the Pangram API. Use when asked to check if text is AI-written, verify human authorship, or run a plagiarism check on a file.
allowed-tools: Bash, Read
---

# AI Writing Detector

Pangram API wrapper for AI-text detection and plagiarism checking.

## Requirements

- `PANGRAM_API_KEY` — [Pangram](https://pangram.cello.so/xGzUNafMfjD)

## Commands

```bash
./scripts/detect detect <file> [options]
./scripts/detect plagiarism <file> [options]
```

## Options

| Option | Description |
|--------|-------------|
| `-k, --api-key` | Overrides env |
| `-s, --short` | Short prediction, 512-token limit (`detect` only) |
| `-o, --output` | `json` (default) or `table` |
| `-i, --input-format` | `text`, `markdown`, `html` — auto-detected from extension |

## Output

JSON. `detect`: `fraction_ai`, `fraction_ai_assisted`, `fraction_human`, `num_ai_segments`, `windows[]`. With `-s`: just `ai_likelihood`. `plagiarism`: `plagiarism_detected`, `percent_plagiarized`, `plagiarized_sentences`, `plagiarized_content[]`.

## Gotchas

- `-o/--output` selects the output **format** (`json` | `table`), not a file path — `-o report.json` is rejected as an invalid value. Redirect stdout to write a file.
- Input is a file path only; there is no stdin or inline-text mode.
- Markdown input is stripped to prose before sending: frontmatter `title`/`excerpt`/`description`/`summary` are prepended, code blocks, images, links and formatting are removed. HTML input is reduced to visible text. So scores describe the prose, not the raw file.

## Examples

```bash
./scripts/detect detect post.md
./scripts/detect detect article.txt -i markdown   # force md parsing on .txt
./scripts/detect detect essay.txt -o table > report.txt
```

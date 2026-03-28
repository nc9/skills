---
name: ai-writing-detector
description: Detect AI-generated text using Pangram API. Use when user asks to check if text/content is AI-written, detect AI content, verify human authorship, or check for plagiarism.
allowed-tools: Bash, Read
---

# AI Writing Detector

Detect AI-generated content and plagiarism using the Pangram API.

## When to Use

- User asks to check if text is AI-generated
- User wants to verify human authorship
- User asks to detect AI content in a document
- User wants to check for plagiarism
- Keywords: "AI detector", "AI written", "detect AI", "human written", "plagiarism check"

## Requirements

- `PANGRAM_API_KEY` - API key from [Pangram](https://pangram.cello.so/xGzUNafMfjD)

## Commands

### Detect AI Content

```bash
./scripts/detect detect <file_path> [options]
```

| Option | Description |
|--------|-------------|
| `--api-key`, `-k` | Pangram API key (overrides env) |
| `--short`, `-s` | Use short prediction (faster, 512 token limit) |
| `--output`, `-o` | Output format: `json` (default) or `table` |
| `--input-format`, `-i` | Input format: `text`, `markdown`, `html` (auto-detected from extension) |

### Check Plagiarism

```bash
./scripts/detect plagiarism <file_path> [options]
```

| Option | Description |
|--------|-------------|
| `--api-key`, `-k` | Pangram API key (overrides env) |
| `--output`, `-o` | Output format: `json` (default) or `table` |
| `--input-format`, `-i` | Input format: `text`, `markdown`, `html` (auto-detected from extension) |

## Input Format Detection

Auto-detected from file extension:
- **markdown**: `.md`, `.mdx`, `.markdown`, `.mdown`, `.mkd`
- **html**: `.html`, `.htm`, `.xhtml`
- **text**: everything else

For markdown files:
- Strips YAML frontmatter
- Extracts `title`, `excerpt`, `description`, `summary` into plain text
- Removes code blocks, images, links, formatting

For HTML files:
- Removes script/style/meta tags
- Extracts visible text content

## Output Format

**Agents should prefer JSON output (default).** Use `--output table` only for human review.

### AI Detection (JSON)

Key fields:
- `fraction_ai` - Percentage of text detected as AI-written (0.0-1.0)
- `fraction_human` - Percentage of text detected as human-written (0.0-1.0)
- `fraction_ai_assisted` - Percentage detected as AI-assisted (0.0-1.0)

```json
{
  "fraction_ai": 0.45,
  "fraction_ai_assisted": 0.30,
  "fraction_human": 0.25,
  "num_ai_segments": 3,
  "windows": [
    {"label": "AI-Generated", "ai_assistance_score": 0.92, "confidence": "Medium"}
  ]
}
```

### Short Prediction (JSON)

```json
{
  "ai_likelihood": 0.87
}
```

### Plagiarism Check (JSON)

```json
{
  "plagiarism_detected": true,
  "percent_plagiarized": 0.15,
  "total_sentences_checked": 20,
  "plagiarized_sentences": 3,
  "plagiarized_content": [
    {"source_url": "https://example.com", "matched_text": "..."}
  ]
}
```

## Examples

```bash
# Full AI detection analysis
./scripts/detect detect essay.txt

# Analyze markdown blog post (auto-detected)
./scripts/detect detect post.md

# Force markdown parsing on .txt file
./scripts/detect detect article.txt --input-format markdown

# Analyze HTML page
./scripts/detect detect page.html

# Quick check (512 token limit)
./scripts/detect detect essay.txt --short

# Human-readable output
./scripts/detect detect essay.txt --output table

# With explicit API key
./scripts/detect detect essay.txt --api-key sk-xxx

# Check for plagiarism
./scripts/detect plagiarism article.md --output table
```

## API Key Resolution

The script searches for `PANGRAM_API_KEY` in order:
1. `--api-key` CLI flag
2. `PANGRAM_API_KEY` environment variable
3. `.env` in current directory
4. `.env.local` in current directory
5. `.env` in home directory

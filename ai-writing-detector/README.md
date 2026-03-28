# AI Writing Detector

Detect AI-generated text and plagiarism using the [Pangram](https://pangram.cello.so/xGzUNafMfjD) API.

## Setup

1. Get API key from [Pangram](https://pangram.cello.so/xGzUNafMfjD)
2. Set `PANGRAM_API_KEY` in environment or `.env`

```bash
export PANGRAM_API_KEY=your_key_here
```

## Usage

### Detect AI Content

```bash
./scripts/detect detect essay.txt
./scripts/detect detect post.md              # auto-detects markdown
./scripts/detect detect page.html            # auto-detects html
./scripts/detect detect file.txt -i markdown # force format
```

Options:
- `--short`, `-s` - Quick prediction (512 token limit)
- `--output`, `-o` - Output format: `json` or `table`
- `--input-format`, `-i` - Input format: `text`, `markdown`, `html`
- `--api-key`, `-k` - Override API key

### Check Plagiarism

```bash
./scripts/detect plagiarism article.md
```

## Input Formats

| Format | Extensions | Processing |
|--------|------------|------------|
| markdown | `.md`, `.mdx`, `.markdown` | Strips frontmatter, extracts title/excerpt/description, removes syntax |
| html | `.html`, `.htm`, `.xhtml` | Removes scripts/styles, extracts visible text |
| text | everything else | Sent as-is |

## Output

JSON by default:

```json
{
  "fraction_ai": 0.45,
  "fraction_human": 0.25,
  "fraction_ai_assisted": 0.30,
  "num_ai_segments": 3
}
```

Use `--output table` for readable output:

```
==================================================
AI WRITING DETECTION RESULTS
==================================================

Metric                              Value
--------------------------------------------------
AI Fraction                          45.0%
AI-Assisted Fraction                 30.0%
Human Fraction                       25.0%
AI Segments                              3
```

## API Key Resolution

Searches in order:
1. `--api-key` CLI flag
2. `PANGRAM_API_KEY` env var
3. `.env` in current directory
4. `.env.local` in current directory
5. `.env` in home directory

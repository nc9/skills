---
name: write-content
description: Create blog posts, articles, and content pieces with research, humanization, and thumbnail generation. Use when user asks to write content, blog posts, articles, or needs help with content creation.
allowed-tools: Bash, Read, Write, Glob, Grep, WebSearch, Skill, Task, AskUserQuestion, Edit
---

# Write Content

Create well-researched, human-sounding content with AI detection verification and thumbnail generation.

## When to Use

- User asks to write a blog post or article
- User wants content on a specific topic
- User mentions `/write-content` or similar
- User needs help creating content for their blog or website

## Workflow Overview

1. **Gather preferences** - Voice, keywords, length
2. **Analyze existing content** - Find gaps, avoid duplicates, identify internal links
3. **Generate suggestions** - Topic, title, excerpt ideas based on research + existing content
4. **Research** - Deep research to ground the content
5. **Write** - Create the content in the chosen voice
6. **Humanize** - Run through humanizer skill
7. **Generate thumbnail** - Create matching illustration
8. **Verify** - Run AI detection to ensure quality

---

## Step 1: Gather User Preferences

Ask the user three questions before starting:

### a) Voice

Ask: "What voice/tone should this content use?"

Options to offer:
| Voice | Description |
|-------|-------------|
| **Conversational** | Casual, like talking to a friend. Short sentences. Direct. |
| **Professional** | Clear and authoritative but not stuffy. Business-appropriate. |
| **Technical** | Precise, detailed, assumes reader knowledge. Good for dev content. |
| **Storytelling** | Narrative-driven, personal anecdotes, journey-focused. |
| **Edgy/Opinionated** | Hot takes, strong opinions, contrarian where warranted. |

### b) Keywords

Ask: "Should we base this on keyword research?"

If yes, ask: "Provide seed keywords (comma-separated) or a topic area for research."

Then run keyword research:
```bash
cd /Users/n/.claude/skills/keyword-research
./scripts/keyword_research suggestions "seed keyword" "another seed" -n 20 -f table
```

Look for keywords with:
- Decent search volume (100+ monthly)
- Low competition
- Relevance to the user's audience

### c) Length

Ask: "How long should this content be?"

| Length | Word Count | Best For |
|--------|------------|----------|
| **Short** | 800-1200 words | Quick reads, news, updates |
| **Medium** | 1500-2000 words | Standard blog posts, tutorials |
| **Long** | 2500-3500 words | In-depth guides, pillar content |
| **Detailed** | 4000+ words | Comprehensive guides, ultimate resources |

---

## Step 2: Analyze Existing Content

Before generating suggestions, scan existing posts to understand what's already covered:

```bash
# Find existing posts
find . -name "*.mdx" -path "*/content/*" 2>/dev/null | head -30

# Or common alternatives
ls content/blog/*.mdx 2>/dev/null || ls posts/*.md 2>/dev/null || ls src/content/*.mdx 2>/dev/null
```

For each relevant post, note:
- **Title and topic** - Avoid duplicating existing content
- **Gaps** - Topics mentioned but not fully covered
- **Linking opportunities** - Posts that could link to/from the new content

This informs both topic suggestions and internal linking later.

---

## Step 3: Generate Suggestions

Based on keyword research **and existing content analysis**, generate **up to 10 topic suggestions** for the user to choose from.

Each suggestion should include:
- **Title** - SEO-friendly, compelling
- **Topic angle** - What makes this take unique
- **Excerpt** - 2-3 sentence hook (under 160 chars for meta description)
- **Target keyword** - Primary keyword to target

Example format:
```
1. "Why Most [X] Advice Is Wrong (And What Actually Works)"
   Angle: Contrarian take on common misconceptions
   Excerpt: Everyone tells you to do X. Here's why that's broken and what works instead.
   Target: [primary keyword]

2. "The Complete Guide to [X] in 2025"
   Angle: Comprehensive, up-to-date resource
   Excerpt: Everything you need to know about X, updated for 2025.
   Target: [primary keyword]
```

Present these to the user and let them pick one (or provide their own).

---

## Step 4: Research

Use the `parallel-deep-research` skill to gather comprehensive information:

```bash
cd /Users/n/.claude/skills/parallel-deep-research
./scripts/parallel_research research "Your research query based on chosen topic" -p pro-fast -f markdown -t 2000
```

**Processor options:**
- `pro-fast` - Good quality, faster (default)
- `pro` - Better quality, slower
- `ultra-fast` - Better quality, faster
- `ultra` - Best quality, slowest

If unavailable, use `WebSearch` tool with multiple queries.

---

## Step 5: Write the Content

Create the content following the chosen voice and length.

### Content Structure

Adapt structure based on voice, but generally:

1. **Opening hook** - 2-3 paragraphs setting up the problem or story
2. **Context** - Why this matters now
3. **Main sections** - Core content with clear headers
4. **Practical takeaways** - What the reader should do
5. **Closing** - Forward momentum, not generic summary

### Formatting Guidelines

- **Headers:** Use sentence case, not Title Case
- **Paragraphs:** Keep short (2-4 sentences max)
- **Lists:** Mix prose and bullets for variety
- **Links:** Include 4-6 links minimum (mix of internal and external)

### Internal Links

Use the existing content analysis from Step 2 to find internal linking opportunities:

```bash
# Search existing posts for related topics
grep -r "keyword" content/ --include="*.mdx" -l 2>/dev/null

# Read a post to find its slug/path
head -20 content/blog/some-post.mdx
```

Include 2-3 internal links to related posts. Good linking patterns:
- Link to posts that go deeper on a subtopic mentioned
- Link to posts that provide prerequisite context
- Link to posts in the same topic cluster

### File Output

Ask the user where to save the file. Common patterns:
- `content/blog/[slug].mdx`
- `posts/[slug].md`
- `src/content/[slug].mdx`

Include frontmatter appropriate to their setup:
```yaml
---
title: "Title Here"
excerpt: "2-3 sentence summary"
publishedAt: "2025-01-15T10:00:00+0000"
image: "/images/blog/[slug].webp"
imageAlt: "Descriptive alt text"
tags:
  - "tag1"
  - "tag2"
---
```

---

## Step 6: Humanize the Content

**CRITICAL:** After writing, use the `humanizer` skill to remove AI patterns.

Key areas humanizer addresses:
- AI vocabulary ("delve", "landscape", "testament", etc.)
- Structural tells (rule of three, parallel lists)
- Missing personality and voice
- Over-polished, consistent sentence lengths

The humanizer skill contains 46+ patterns to detect and fix. Run the content through it before proceeding.

---

## Step 7: Generate Thumbnail

Use the `generate-image` skill to create a matching illustration.

### Finding Design Context

Before generating, look for design hints:
1. Check for existing blog images in the project
2. Look for brand guidelines or design memory files
3. Check CLAUDE.md or similar for style preferences
4. Look at the blog's existing visual style

```bash
# Find existing blog images
ls -la public/images/blog/ 2>/dev/null || ls -la images/ 2>/dev/null

# Look for design guidelines
find . -name "*brand*" -o -name "*design*" -o -name "*style*" 2>/dev/null | head -20
```

### Generate the Image

```bash
cd /Users/n/.claude/skills/generate-image
./scripts/generate_image "STYLE: [based on found design context or user preference]. SUBJECT: [relevant to content topic]." --output [path]/[slug].png
```

If no design context found, ask the user:
- "What style should the thumbnail use? (minimalist, photorealistic, illustrated, etc.)"
- "Any brand colors to incorporate?"

### Optimize for Web

Convert to WebP for smaller file size:
```bash
cwebp -q 80 [slug].png -o [slug].webp
rm [slug].png
```

Update frontmatter to use `.webp` extension.

---

## Step 8: AI Detection Verification

Run the final content through AI detection:

```bash
cd /Users/n/.claude/skills/ai-writing-detector/scripts
./scripts/detect detect [content-file-path] --output table
```

### Interpreting Results

| AI Fraction | Quality |
|-------------|---------|
| Below 30% | Excellent - reads as human |
| 30-50% | Good - some AI patterns but acceptable |
| 50-70% | Fair - consider more humanization |
| Above 70% | Poor - needs significant rewriting |

If score is too high:
1. Re-run humanizer with focus on flagged segments
2. Add more personal anecdotes and specific numbers
3. Vary sentence lengths more aggressively
4. Convert any remaining lists to narrative prose

---

## Checklist

Before finishing:

- [ ] User confirmed voice, keywords, and length
- [ ] Existing content analyzed for gaps and linking opportunities
- [ ] Topic/title selected from suggestions (avoids duplicating existing posts)
- [ ] Content researched with parallel-deep-research
- [ ] Content written in chosen voice and length
- [ ] Humanizer skill applied
- [ ] AI detection score acceptable (< 50%)
- [ ] Thumbnail generated matching design style
- [ ] Image optimized to WebP
- [ ] Frontmatter complete with all fields
- [ ] Internal and external links included

---

## Example Session

```
User: Write a blog post about remote work productivity

Agent: Great! Let me gather some preferences first.

1. What voice should this use?
   - Conversational (casual, direct)
   - Professional (clear, authoritative)
   - Technical (precise, detailed)
   - Storytelling (narrative-driven)
   - Edgy/Opinionated (hot takes)

User: Conversational

Agent: Should we base this on keyword research? If yes, provide seed keywords.

User: Yes - "remote work", "work from home productivity"

Agent: How long should this be?
   - Short (800-1200 words)
   - Medium (1500-2000 words)
   - Long (2500-3500 words)
   - Detailed (4000+ words)

User: Medium

Agent: [runs keyword research, generates 10 topic suggestions]

Here are some topic ideas based on the research:

1. "The Remote Work Myth Nobody Talks About"
   Angle: Contrarian take on productivity theater
   Excerpt: You're not lazy. Your setup is broken. Here's what actually moves the needle.
   Target: remote work productivity

2. "I Tracked My Remote Work for 90 Days. Here's What Broke."
   Angle: Personal experiment with data
   ...

Which would you like, or describe your own?

User: Option 1

Agent: [researches, writes, humanizes, generates thumbnail, runs AI detection]
```

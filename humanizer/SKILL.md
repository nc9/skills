---
name: humanizer
version: 5.0.0
description: Remove AI-writing tells from text - 65 catalogued patterns plus measured AI-detector results. Use when humanizing a draft, editing text to sound human or natural, or lowering an AI detector score before publishing.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
  - AskUserQuestion
---

# Humanizer: remove AI writing patterns

Strip the signs of AI-generated text, then add the human tells detectors look
for. Based on Wikipedia's "Signs of AI writing" (WikiProject AI Cleanup) plus
hands-on testing against the Pangram detector.

Current models already avoid the obvious tells unprompted. What earns its keep
here is the measured, counterintuitive part: structure beats vocabulary,
polishing makes things worse, and some topics cannot be rescued at all.

## Process

1. **Assess the content type** - set a realistic target from the difficulty
   table below before editing anything.
2. **Remove AI patterns** - scan for all 65 patterns in the index below. The
   index is enough to spot them; open the reference file for any pattern whose
   fix you need worked through.
3. **Add human patterns** - specific numbers and timeframes, self-deprecating
   asides, admitted uncertainty, varied sentence rhythm, casual transitions
   ("Look," "Anyway," "Point is,"), broken parallelism in lists. Removing tells
   without adding voice leaves sterile text that still flags.
4. **Verify** - read it aloud. Sounds like Wikipedia? Add voice. Sounds
   over-polished? Put roughness back. Report the rewrite plus a short changelog:
   patterns removed, human patterns added, structural changes.

## Narrative-first structure

The highest-leverage move, and the one most often skipped. For how-to, guide or
advice content, lead with narrative and weave structure in.

Measured: pure narrative scores 30-35% AI, pure how-to 60-100%, narrative with
structure woven in 40-50% *and* it reads better *and* it still ranks.

Open with a specific personal experience. Establish the problem through
narrative, not bullets. Introduce solutions as things you tried, not "Step 1,
Step 2". Keep headers, bold and lists sparse, for scanning only. Close with
reflection, not a CTA. So "## How to Build Backlinks / - **Digital PR:** ..."
becomes "I wasn't planning to write another backlinks post. Google keeps saying
they matter less. Yet every time I look at actual data - my own sites, client
sites - links are still the biggest factor. ... ## Digital PR (the best ROI
right now) / Took me a while to come around on this one."

## Measured detector results

Real Pangram runs, not estimates:

- Narrative blog post: 100% -> 35% AI. Aggressive humanization works.
- How-to guide: 100% -> 53-90% per segment; individual sections improved, the
  overall label stayed "AI".
- AI/SEO industry post: 100% -> 100% AI, segments 99.98% -> 99.91%. Barely moved
  despite anecdotes, self-deprecation, tangents, casual headers, fragments and
  varied structure.

Voice work has a ceiling, and structure and topic set it.

## Content-type difficulty

| Content type | Difficulty | Realistic target |
|---|---|---|
| Personal narrative | Easy | Below 30% AI |
| Opinion / hot take | Easy | Below 35% AI |
| Mixed narrative + advice | Medium | Below 45% AI |
| How-to guide | Hard | 50-70% AI (win at segment level) |
| Pure listicle | Very hard | May not drop below 60% |
| AI / SEO / marketing topics | Near-impossible | May stay 100% regardless of effort |

A personal essay drops from 80% to 30% on voice changes alone. The same effort
on a how-to moves 100% to 60%, because the structure itself is the signal.

## The polished-rewrite trap

Over-editing *increases* detection scores. Clean rewrites routinely score higher
than the rough originals they replaced - one measured pair went 50% (tidy
rewrite) versus 35% (rougher version, same content). Detectors flag consistent
sentence lengths, perfect parallel structure, smooth transitions and the absence
of false starts. Leave the rough edges in.

Related traps: structure (how-to formats flag regardless of voice), consistency
(uniform sentence length), authority (confident expertise reads as AI - admit
uncertainty), parallel headers ("What works: A", "What works: B" repeating is an
instant flag).

## Topic-based detection bias

Some topics are so heavily represented in detector training data that they flag
on subject matter rather than style: AI/ML, SEO and digital marketing, SaaS
growth, productivity optimization, crypto, "future of X" analysis.

Decide early whether such content needs to pass detection at all. If it does,
the only remaining lever is full restructuring into personal narrative.
Otherwise accept the score and publish - a useful piece that reads as human to
human readers is fine when detection scores do not gate your distribution.

## Target metrics

Narrative: below 40% is good, below 30% excellent. Structured: 50-70% overall is
expected, so measure by segment - get 2-3 segments below 60%. If three passes
cannot get below 60%, stop humanizing and restructure.

## Publishing workflow

**Publish gate:** never publish - to a CMS, repo, MCP endpoint, file or anywhere
else - until both loops below have run and the final score is acceptable. Every
article, single or batched, no exceptions for momentum or deadlines or "I'll
humanize them after"; drafting and shipping in one pass produces detectable AI
prose every time. About to call a publish, create-post or commit tool with text
that hasn't been through both loops? Stop and run them first.

**Loop 1 - humanize, then detect.** Apply this skill to the full draft, then run
the `ai-writing-detector` skill's detector:
`./scripts/detect detect <file> --input-format markdown --output json`. Capture
`fraction_ai` and `fraction_ai_assisted`. If `fraction_ai` is below 25% and
`fraction_ai_assisted` below 40%, skip Loop 2.

**Loop 2 - re-humanize the flagged segments, then detect again.** Use the
segment-level output to find the highest-scoring passages and rewrite only
those: break parallel and symmetrical structure, replace listicle scaffolding
with narrative, add a specific anecdote, named product, concrete number or
first-person aside every ~300 words, cut closing-paragraph macro framing.

| Final `fraction_ai` | Action |
|---|---|
| Below 25% | Publish. |
| 25-50% | Acceptable if the voice is genuinely distinct and the format is structurally constrained (listicle, monthly guide, medical, finance - known topic and format bias). Note the score in the report. |
| Above 50% | Do not publish. Restructure the piece (listicle to narrative, survey to Q&A) and rerun the loops, or escalate to the user with the segment scores and ask whether to publish anyway. |

**Why this order, and only two loops:** humanize first so the detector reports
the *remaining* scaffolding instead of the obvious tells you were always going
to fix - detecting raw output wastes a cycle and biases the rewrite toward
whatever that first run flagged, missing structural tells. Two loops, not three
or more: if the score is still high after two, the piece needs structural
redesign, not more humanization passes.

## Pattern index

All 65 patterns, one line each. `(+)` marks patterns that are things to **add**,
not tells to remove. Full before/after treatment lives in the reference files.

**Content (1-6)** - `references/patterns.md`

1. Inflated significance - "stands as a testament", "pivotal moment", "evolving landscape", "reflects broader".
2. Notability padding - lists of media coverage, "active social media presence".
3. Superficial -ing tails - "highlighting...", "ensuring...", "reflecting..." bolted onto sentences.
4. Promotional language - "nestled", "vibrant", "breathtaking", "rich cultural heritage", "boasts a".
5. Vague attribution - "Experts argue", "Industry reports", "Observers have cited".
6. "Challenges and future prospects" sections - "Despite these challenges, ... continues to thrive".

**Language and grammar (7-12)** - `references/patterns.md`

7. AI vocabulary - delve, crucial, intricate, tapestry, underscore, landscape, showcase; magic adverbs (quietly, deeply, fundamentally).
8. Copula avoidance - "serves as", "boasts", "features" where "is"/"has" belongs.
9. Negative parallelism - "It's not just X, it's Y", "Not only... but...".
10. Rule of three - forced triplets to sound comprehensive.
11. Elegant variation - synonym cycling for one referent (protagonist/main character/central figure/hero).
12. False ranges - "from X to Y" where X and Y aren't on a scale.

**Style (13-18)** - `references/patterns.md`

13. Em dash overuse.
14. Boldface overuse - mechanical emphasis on phrases.
15. Inline-header vertical lists - "- **User Experience:** The user experience...".
16. Title Case headings.
17. Emojis decorating headings or bullets.
18. Curly quotes and Unicode decoration - smart quotes, arrows in running prose.

**Communication (19-21)** - `references/patterns.md`

19. Chatbot artifacts - "I hope this helps", "Certainly!", "let me know".
20. Knowledge-cutoff disclaimers - "as of my last update", "while specific details are limited".
21. Sycophantic tone - "Great question!", "You're absolutely right".

**Filler and hedging (22-24)** - `references/patterns.md`

22. Filler phrases - "in order to", "due to the fact that", "it is important to note".
23. Excessive hedging - "could potentially possibly be argued".
24. Generic positive conclusions - "exciting times lie ahead", "a step in the right direction".

**Blog posts (25-32)** - `references/blog-patterns.md`

25. "You did X" openings - three short beats ending in "You're proud."
26. "The dirty secret" / "nobody talks about" trope.
27. Marketing jargon - "top-of-funnel", "low-friction", "community engagement".
28. Formulaic advice lists - valid points forced into parallel bullets.
29. Generic section headers - descriptive and Wikipedia-flavoured instead of opinionated.
30. Missing vulnerability - advice delivered from detached authority.
31. Cliché transitions - "move the needle", "here's the kicker", "let that sink in".
32. (+) "Welcome to the club" - naming a shared frustration to build solidarity.

**Detector-driven (33-46)** - `references/detector-testing.md`

33. The polished-rewrite trap - clean edits score higher than rough ones.
34. (+) Personal anecdotes with specific numbers - "200+ points once", "maybe 30 launches".
35. (+) Self-deprecating parenthetical asides - "(yes I'm that person)".
36. (+) Admitted confusion - "I don't fully understand it but it works".
37. (+) Sentence fragments - "Wild." "Works though." "Yeah yeah,".
38. (+) Casual quantifiers - "like 40-60 words max", "roughly 28%".
39. (+) Specific sequences of events - narrate the steps instead of summarizing them.
40. Detector-flagging structures - numbered steps, parallel bullets, FAQ format, uniform header+paragraph rhythm.
41. Content-type difficulty - narrative easy, how-to hard, AI/SEO near-impossible (table above).
42. (+) Converting lists to narrative - same information as flowing prose with asides.
43. Repeated header pattern - "What works: A", "What works: B", "What works: C".
44. (+) Conversational transitions - "So", "Look,", "Here's the thing:" instead of "Moreover".
45. (+) Named emotions about specific things - "that one stung", not "the results were disappointing".
46. Topic-based detection bias - AI/SEO/marketing topics flag on subject matter.

**Sentence and paragraph structure (47-52)** - `references/patterns.md`

47. Dramatic countdown - "Not a framework. Not a library. Something far more fundamental."
48. Self-posed rhetorical questions - "The result? A mass exodus."
49. Anaphora abuse - consecutive sentences opening on the same word.
50. Gerund fragment litany - "Building trust. Breaking barriers. Creating opportunity."
51. Short punchy fragment overuse - one-sentence paragraphs manufacturing drama.
52. Listicle in a trench coat - "The first... The second... The third...".

**Tone and voice (53-58)** - `references/patterns.md`

53. Patronizing analogies - "Think of a database index as a book's table of contents".
54. Futurism invitation - "Imagine a world where...".
55. False vulnerability - "I'll be honest:" that resolves straight back into confidence.
56. Asserting obviousness - "The truth is simple", "it all comes down to one thing".
57. Pedagogical voice - "Let's break this down", "let's unpack this".
58. Invented concept labels - "the visibility paradox", pseudo-academic coinages.

**Composition (59-65)** - `references/patterns.md`

59. Fractal summaries - the same point in the intro, the section, and the conclusion.
60. Dead metaphor - one metaphor's vocabulary appearing 4+ times.
61. Historical analogy stacking - "Just as the printing press...", "Like the Industrial Revolution...".
62. One-point dilution - a single argument restated ten ways to fill space.
63. Content duplication - near-verbatim repeats between intro, body and conclusion.
64. Signposted conclusion - "In conclusion", "At the end of the day".
65. Formulaic introduction - "In today's rapidly evolving digital landscape".

## When to read the references

- `references/patterns.md` - before/after examples for 1-24 and 47-65, the
  personality-and-soul guidance, two worked full-document rewrites. Read when
  you need a specific pattern's fix worked through, or when a rewrite comes back
  technically clean but voiceless.
- `references/blog-patterns.md` - patterns 25-32. Read when the text is a blog
  post, marketing page, or startup/SaaS content.
- `references/detector-testing.md` - patterns 33-46, the iterative test loop and
  restructuring criteria. Read when the text will be scored by a detector, when
  a score stops moving between passes, or before deciding a piece needs
  structural redesign.

## Attribution

Patterns 1-24: [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
(WikiProject AI Cleanup), drawn from thousands of observed instances on
Wikipedia. Patterns 25-32: detector testing on marketing content, January 2026.
Patterns 33-45 and the iterative process: hands-on Pangram API testing, January
2026, which took a narrative blog post from 51% to 35% across five iterations.
Pattern 41 (content-type difficulty) came from how-to and listicle testing where
aggressive humanization only moved segments from 91-100% to 53-90% while the
overall label stayed "AI" - the finding that established structure matters as
much as voice. Pattern 46 (topic bias) came from an AI/SEO post that stayed at
100% through every available technique. Patterns 47-65: adapted from
[tropes.fyi](https://tropes.fyi) (March 2026), ~30 recurring rhetorical moves in
LLM output.

**From Wikipedia:** "LLMs use statistical algorithms to guess what should come
next. The result tends toward the most statistically likely result that applies
to the widest variety of cases."

**From detector testing:** detectors look for the *absence* of human patterns as
much as the presence of AI ones. Removing tells is half the job. And for some
formats the structure itself is the signal, so no amount of voice work moves the
label.

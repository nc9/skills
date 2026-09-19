# Detector testing: patterns 33-46 and the iterative process

Discovered through iterative testing with the Pangram detector. Key finding:
removing AI tells is only half the job — you must also add the human tells
detectors look for. Patterns marked as additions are things to put IN, not
things to cut.

---

### 33. The Polished Rewrite Trap

**CRITICAL:** Over-editing text can INCREASE AI detection scores. Clean, well-structured rewrites often score higher than rough originals.

**Why this happens:** AI detectors flag:
- Consistent sentence lengths
- Perfect parallel structure
- Smooth transitions between ideas
- Lack of false starts or rough edges

**Before (flagged at 50% AI):**
> Show HN remains the gold standard for reaching developers who actually try stuff. But you can't just dump a link and hope.
>
> Post on Tuesday or Wednesday between 8-11 AM UTC. I've tested this. Posts in that window get around 28% more points than other times.

**After (flagged at 35% AI):**
> Show HN. Still the best place if you want developers who'll actually try your stuff. Had a post hit 200+ points once - drove signups for like three weeks after.
>
> Here's what I've learned after watching this way too closely: post Tuesday or Wednesday, 8-11 AM UTC. I kept a spreadsheet tracking this across 20 posts (yes I'm that person). Posts in that window got roughly 28% more engagement. Not scientific but not nothing either.

**Key changes:**
- Fragment opener ("Show HN.")
- Specific personal result ("200+ points once")
- Self-deprecating aside ("yes I'm that person")
- Hedging with specificity ("Not scientific but not nothing either")
- Casual approximation ("like three weeks")

---

### 34. Personal Anecdotes with Specific Numbers

**Problem:** Generic advice reads as AI. Grounding in personal experience with specific counts reads as human.

**Before:**
> Many developers have found success posting on Show HN.

**After:**
> My best Show HN post hit 200+ points. Drove signups for weeks. The one before that? 3 points and died.

**Before:**
> I analyzed several successful launches to identify patterns.

**After:**
> I went down a rabbit hole last month trying to figure out why some apps get traction. Looked at maybe 30 launches that actually worked.

**Key technique:** Include specific numbers even when approximating ("maybe 30", "like three weeks", "roughly 28%").

---

### 35. Self-Deprecating Parenthetical Asides

**Problem:** AI writes from a position of authority. Humans admit their quirks.

**Examples that work:**
- "I kept a spreadsheet tracking this (yes I'm that person)"
- "I've tested this way more than is healthy"
- "spent an embarrassing amount of time on this"
- "because I'm obsessive like that"

**Before:**
> I systematically tracked posting times across multiple submissions.

**After:**
> I kept a spreadsheet of my own posts because I'm obsessive like that.

---

### 36. Admitting Confusion and Uncertainty

**Problem:** AI confidently explains everything. Humans admit when things don't make sense to them.

**Phrases that humanize:**
- "I don't fully understand the algorithm but it works"
- "The combined momentum does... something. Algorithms are weird."
- "Wild but true."
- "I genuinely don't know how to feel about this one."
- "The truth is probably somewhere boring in the middle"

**Before:**
> The synergy between Hacker News and Product Hunt launches creates compounding visibility effects.

**After:**
> Day 1 HN, day 2 PH. The combined momentum does... something. I don't fully understand it but it works.

---

### 37. Sentence Fragments and Incomplete Thoughts

**Problem:** AI writes in complete, grammatically correct sentences. Humans use fragments.

**Fragment types that work:**
- One-word sentences: "Wild." "Brutal." "Works though."
- Trailing thoughts: "Not scientific but not nothing either."
- Casual starters: "Alright, so." "Look," "Yeah yeah,"

**Before:**
> This approach is surprisingly effective despite seeming unconventional.

**After:**
> Wild but true. Works though.

**Before:**
> "Write for humans, not algorithms." That advice was relevant in the past.

**After:**
> Yeah yeah, "write for humans not algorithms." That was good advice in 2015.

---

### 38. Casual Quantifiers and Approximations

**Problem:** AI gives precise numbers or ranges. Humans approximate casually.

**Before → After:**
- "40-60 words" → "like 40-60 words max"
- "approximately 30%" → "roughly 30%"
- "several weeks" → "like three weeks"
- "numerous instances" → "maybe 30"
- "significant improvement" → "almost 30% more"

**Why it works:** The words "like", "maybe", "roughly", "something like" signal informal estimation rather than computed precision.

---

### 39. Specific Sequences of Events

**Problem:** AI summarizes. Humans narrate sequences.

**Before:**
> I had difficulty getting traction for my command-line tool until I changed my distribution strategy.

**After:**
> Built a CLI tool, put up a landing page, wondered why nobody cared. Then I packaged the same thing as a VS Code extension. Installs jumped overnight.

**Key pattern:** Short clauses in sequence. Past tense. No connecting words like "subsequently" or "therefore."

---

### 40. Structural Patterns That Flag Detectors

**IMPORTANT:** Some structures inherently score high on AI detection regardless of voice quality. You can add perfect human voice patterns and still flag as AI if the structure is wrong.

**High-risk structures:**
- Numbered step-by-step lists
- Parallel bullet points ("First... Second... Third...")
- "How to X" headers followed by structured advice
- FAQ-style Q&A formats
- Consistent header+paragraph+header+paragraph rhythm
- **Repeated parallel headers** like "What works: X", "What works: Y", "What works: Z"

**Mitigation strategies:**
1. **Vary list formats:** Mix numbered lists with prose. Use **bold labels** instead of numbers sometimes.
2. **Break parallel structure:** Don't start every point the same way.
3. **Interrupt with asides:** Add parenthetical comments, tangents, or personal reactions between structured elements.
4. **Use varying paragraph lengths:** A one-sentence paragraph, then a longer one, then a medium one.
5. **Vary your headers:** Instead of "What works: A", "What works: B", "What works: C" use different formats: "Digital PR (the best ROI right now)", "The unlinked mentions goldmine", "Broken link building (tedious but legit)"

**Before (flagged):**
> 1. Check your backlinks
> 2. Set up alerts
> 3. Join a community
> 4. Optimize your content
> 5. Calculate your time value

**After (less flagged):**
> **One:** Ahrefs or Moz. Check your backlinks. Zero from quality sources? That's why.
>
> **Two:** Google Alerts. 30 seconds to set up. Now you'll find out when someone mentions your app name somewhere.
>
> **Three:** This one's annoying but necessary. Pick ONE community. Reddit, Indie Hackers, HN - whatever fits your thing. Hang out there for a few weeks being useful before you post anything about your product. Feels slow. Works though.

---

### 41. Content Type Difficulty Levels

**CRITICAL INSIGHT:** Different content types have vastly different humanization difficulty. Set expectations accordingly.

**Easy to humanize (narrative content):**
- Personal stories and experiences
- Opinion pieces and hot takes
- First-person accounts of failures/successes
- Reflections and lessons learned
- Rants and complaints

**Hard to humanize (structured content):**
- How-to guides and tutorials
- Listicles ("10 ways to X")
- Comparison posts
- Resource roundups
- Step-by-step processes

**Essentially impossible (resistant topics + structure):**
- AI/technology industry analysis
- SEO advice posts
- "Problem → Solution" arcs about tech trends
- Content explaining algorithmic changes
- Marketing/growth hacking advice

**Why this matters:** A personal essay can often drop from 80% AI to 30% AI with voice changes alone. A how-to post might go from 100% AI to 60% AI with the same effort - the structure itself signals AI regardless of voice.

**Real-world test results:**
- Narrative blog post: 100% → 35% AI (65-point improvement)
- How-to guide: 100% → 53-90% per segment (individual sections improved but overall still flagged)
- **AI/SEO industry post: 100% → 100% AI (segment scores 99.98% → 99.91%)** - barely moved despite aggressive humanization with personal anecdotes, self-deprecation, tangents, and varied structure

**Implications:**
1. For how-to content, accept that perfect scores may be impossible
2. Focus on segment-level improvements rather than overall label
3. Consider restructuring into narrative format if AI score matters
4. Mix narrative sections into how-to content to lower overall score
5. **For AI/tech industry content: accept that detectors may be biased against the topic itself**

---

### 42. Converting Lists to Narrative

**Problem:** Bullet lists are AI catnip. Even with good voice, they flag.

**Solution:** Convert lists into flowing prose with the same information.

**Before (flagged at 95%):**
> Examples that work:
> - Comprehensive guides that cover a topic better than anyone else
> - Interactive calculators (think "Should I buy or rent?")
> - Original research or benchmarks
> - Free templates and checklists
> - Curated resource lists

**After (flagged at 65%):**
> What tends to work? Guides that actually go deep - not the generic "10 tips" garbage everyone else publishes. Calculators are weirdly powerful (those "should I rent or buy?" tools get linked constantly). Original research with real data. Templates people can download and use. Comprehensive resource lists.

**Key changes:**
- Removed bullet structure entirely
- Kept the same information
- Added commentary between items ("weirdly powerful", "generic garbage")
- Used casual parentheticals
- Made it read like someone talking

---

### 43. The Repeated Header Pattern

**Problem:** Using the same header format repeatedly is a major AI signal.

**Before (screams AI):**
> ## What works: Digital PR
> ## What works: Linkable assets
> ## What works: Unlinked mentions
> ## What works: Broken link building
> ## What works: Local citations

**After (more human):**
> ## Digital PR (the best ROI right now)
> ## Linkable assets (the passive play)
> ## The unlinked mentions goldmine
> ## Broken link building (tedious but legit)
> ## Local citations (if that's your game)

**Why it works:**
- Each header has different structure
- Parenthetical commentary varies
- Some have parentheticals, some don't
- Personality comes through in header choice
- Reads like someone with opinions wrote it

---

### 44. Conversational Transitions

**Problem:** AI uses formal transition words. Humans use conversational ones.

**AI transitions to avoid:**
- Moreover, Furthermore, Additionally
- Subsequently, Consequently
- It is worth noting that
- This is particularly evident in
- The significance of this cannot be overstated

**Human alternatives:**
- "So" (starting sentences)
- "Anyway," "Point is,"
- "Here's the thing:"
- "Look,"
- "Alright, so"
- Just... make the point. No transition needed.

---

### 45. Named Emotions About Specific Things

**Problem:** AI uses generic emotional language. Humans get specific.

**Before:**
> This situation is concerning.

**After:**
> There's something unsettling about agents churning away at 3am while nobody's watching.

**Before:**
> The results were disappointing.

**After:**
> 3 points. Died on /new. That one stung.

**Key technique:** Name the specific thing and the specific feeling. "Concerning" → "unsettling about agents churning away at 3am"

---

### 46. Topic-Based Detection Bias

**CRITICAL FINDING:** Some topics are so heavily represented in AI training data that detectors flag them regardless of voice quality.

**Topics that resist humanization:**
- AI and machine learning discussions
- SEO and digital marketing advice
- SaaS/startup growth strategies
- Productivity and workflow optimization
- Cryptocurrency and blockchain content
- "Future of X" industry analysis

**Why this happens:** AI detectors are trained on AI-generated content. Certain topics (AI, SEO, marketing) were heavily generated by LLMs during the detector's training period. The detectors learned to associate these topics themselves - not just the writing style - with AI.

**Test case:**
An SEO post about AI search visibility was humanized with:
- Personal anecdotes with specific numbers ("I emailed Google support thinking my site got penalized")
- Self-deprecating asides ("I literally emailed Google support thinking my site got penalized. They didn't reply. Nobody at Google replies to anything.")
- Tangents that go nowhere
- Admissions of uncertainty ("I don't fully understand it")
- Casual headers ("wait, is Google even a search engine anymore?")
- Fragment sentences
- First-person vulnerability

**Result:** 100% AI → 100% AI. Segment scores moved from 100% to 99.91%. The topic itself appears to be flagged.

**Implications:**
1. For AI/SEO/marketing topics, don't expect humanization to work
2. Consider whether the content even needs to pass AI detection
3. If it must pass, completely restructure into pure personal narrative
4. Alternatively: accept the score and publish anyway

**When to just publish:**
- The content is genuinely useful
- The voice sounds human to human readers
- AI detection scores don't affect your distribution channels
- You're not submitting to platforms that filter for AI content

---

## ITERATIVE TESTING PROCESS

When humanizing content that will be run through AI detectors:

### Step 0: Assess Content Type
Before starting, identify what type of content you're working with and set the
realistic target from the content-type difficulty table in `SKILL.md` (full
detail in pattern 41 above). A how-to post may never score as "human" overall -
focus on individual segment improvements.

### Initial Pass
1. Fix obvious AI patterns (vocabulary, structure, transitions)
2. Add personal voice and vulnerability
3. Vary sentence lengths and structures
4. **For how-to content:** Convert at least some lists to narrative prose

### Test and Iterate
5. Run through detector
6. Identify flagged segments
7. For each flagged segment, add:
   - A personal anecdote or specific number
   - A self-deprecating aside or admission of confusion
   - Sentence fragments or casual approximations
   - Break any remaining parallel structure
8. **Check segment scores individually** - even if overall label doesn't change, segment scores may improve dramatically

### Common Traps
- **The polished trap:** Clean rewrites often score HIGHER. Leave rough edges.
- **The structure trap:** How-to content inherently scores high. Voice alone won't fix it.
- **The consistency trap:** All sentences similar length = AI flag. Mix it up.
- **The authority trap:** Confident expertise = AI. Admit uncertainty.
- **The parallel header trap:** "What works: A", "What works: B" repeating = instant AI flag.

### Target Metrics

See "Target metrics" in `SKILL.md`. Short version: narrative below 40% is good
and below 30% is excellent; structured content may sit at 50-70% overall, so
score it on segment-level improvement instead.

### When to Consider Restructuring

If after 3+ iterations you can't get below 60% AI:
1. Consider converting the entire piece to narrative format
2. Merge multiple short sections into longer flowing sections
3. Add substantial personal story sections to dilute the how-to parts
4. Accept the score if the content must stay structured


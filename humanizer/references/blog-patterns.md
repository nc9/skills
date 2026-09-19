# Blog post patterns (25-32)

Discovered through AI detector testing on real marketing/startup blog posts.
Indexed in `SKILL.md`; core patterns are in `patterns.md`, detector findings in
`detector-testing.md`.

---

### 25. Formulaic "You did X" Openings

**Problem:** AI loves the pattern: "You [did something]. [Short sentence]. [Another short sentence]. You're proud/excited/ready."

**Before:**
> You built an app over the weekend. Claude Code, Cursor, Lovable, Bolt, Replit Agent - pick your weapon. The code works. It's deployed. You're proud.

**After:**
> So you vibe coded an app. Mass prompted your way through a weekend with Claude Code or Cursor or Lovable or whatever. It works. It's live. You tweeted about it.
>
> And then... nothing.

**Why it works:** The rewrite uses casual phrasing ("or whatever"), acknowledges the anticlimax ("And then... nothing"), and doesn't follow the predictable three-beat structure.

---

### 26. "The dirty secret" / "Nobody talks about" Trope

**Problem:** AI uses mystery-building phrases to introduce points that aren't actually secrets.

**Words to watch:** "The dirty secret of...", "What nobody tells you...", "Nobody talks about it because...", "Here's what they won't tell you..."

**Before:**
> This is the dirty secret of the vibe coding boom. Building is easy now. Distribution is fundamentally broken. And nobody talks about it because the AI coding tool companies are too busy celebrating how fast you can ship.

**After:**
> Here's what Cursor and Lovable won't tell you in their marketing: they solved building. They didn't solve distribution. That part is still brutal, and it might actually be getting worse.

**Why it works:** Instead of vague "nobody talks about it," directly call out specific companies. Makes it concrete and confrontational rather than mysteriously vague.

---

### 27. Marketing Jargon as AI Tell

**Problem:** Certain B2B/SaaS marketing phrases are heavily overrepresented in AI training data and flag immediately.

**Phrases to kill:**
- "low-friction install-to-try experience" → "install it in two clicks"
- "top-of-funnel" → just describe what happens
- "serves as top-of-funnel" → "gets you initial users"
- "funnels them to" → "leads them to" or just restructure
- "canonical source for citable facts" → "a page people actually link to"
- "sustained effort" → "months of work" or be specific
- "community engagement" → describe what you actually do

**Before:**
> Open-source repositories on GitHub serve as top-of-funnel. Developers discover the tool, and the README funnels them to a hosted or premium version.

**After:**
> Throw a useful repo on GitHub. Make the README good. Link to your paid thing at the bottom. People who love the free version will check out what else you've got.

---

### 28. Formulaic Advice Lists

**Problem:** AI structures advice as parallel bullet points with similar construction. Even if each point is valid, the structure itself screams AI.

**Before:**
> Create content that AI can easily extract and cite. This means:
>
> - Short paragraphs (40-60 words) that stand alone as complete answers
> - H2/H3 headings that mirror user queries ("How does vibe coding work?")
> - Fresh, verifiable statistics with clear sources
> - Direct quotations from experts
> - "Key Takeaways" sections at the top

**After:**
> AI models pull quotes from your content to answer questions. If your content is a wall of text, they skip you. If it's neatly packaged into bite-sized chunks with actual numbers? You get cited.
>
> Keep paragraphs short - like 40-60 words max. Use headers that sound like questions people actually ask. Throw in real stats. Quote people by name. Put a TL;DR at the top.

**Why it works:** Same information, but as flowing prose with casual asides ("like 40-60 words max") instead of rigid parallel structure.

---

### 29. Generic Section Headers

**Problem:** AI defaults to descriptive, Wikipedia-style headers. Human writers use headers with attitude or intrigue.

**Before → After:**
- "Content structured for AI citation" → "Write for the robots (seriously)"
- "Marketplace distribution" → "Go where developers already are"
- "Why DIY link building fails for solo builders" → "Why you probably won't do any of this"

**Why it works:** The rewrites have voice. They make a point or provoke rather than just describing.

---

### 30. Missing Vulnerability/Admission

**Problem:** AI gives advice from a detached, authoritative position. Humans admit they struggle too.

**Before:**
> Be honest with yourself. You have limited time. You're running product, support, and development. Maybe you have a day job too. Link building requires consistent outreach over months. It's grunt work. Most solo founders give up after two weeks.

**After:**
> Real talk.
>
> You're already stretched thin. You're fixing bugs, answering support emails, maybe working a day job on top of all this. Link building means sending cold emails for months. Writing guest posts nobody reads. Showing up in Reddit threads every day pretending you're not there to promote yourself.
>
> It works. But it's boring. And slow. Most founders bail after two weeks because they'd rather build features.
>
> I get it. I've been there. The new feature feels productive. The outreach feels like begging.

**Key additions:**
- "Real talk." - signals honesty
- "I get it. I've been there." - first-person admission
- "The outreach feels like begging." - specific emotional truth
- "pretending you're not there to promote yourself" - acknowledges the awkwardness everyone feels

---

### 31. Cliché Transitions and Filler

**Phrases to cut:**
- "move the needle" → just say what changes
- "The tactical playbook:" → unnecessary framing
- "The conversion difference is striking:" → just state the stat
- "Let that sink in." → delete entirely
- "Here's the kicker:" → delete or just make the point
- "Some specific tactics that move the needle:" → "What actually works:"
- "Here's where it gets interesting" → delete or just make the point
- "Here's what most people miss" → delete or just make the point

These phrases buy time without adding information. Humans usually just make their point.

---

### 32. The "Welcome to the club" Move

**Technique:** When describing a common frustration, acknowledge that the reader isn't alone. Creates solidarity.

**Example:**
> Nobody's signing up. Nobody's sharing it. Your analytics dashboard is a flatline. Welcome to the club. There are thousands of us here, all staring at apps that work perfectly fine and have zero users.

This works because it:
- Validates the reader's experience
- Creates community ("thousands of us")
- Has dark humor ("work perfectly fine and have zero users")
- Doesn't offer false hope or pivot to selling immediately

---

# The skills kit

A skill is one task written down once, so the AI stops improvising it. Everyone is told to
write them. Almost nobody knows **which** ones to write, or whether the ones they downloaded
are any good.

Three steps, and each is a prompt you paste:

| | Step | What it does |
|---|---|---|
| 1 | **Find it** — the Repeat Finder | Looks for what you keep redoing, and says which of it is worth writing down |
| 2 | **Write it** — [the generator](01-generator-prompt.md) | Interviews you about one task and writes the skill from your own answers |
| 3 | **Fix it** — the Skill Doctor | Checks any skill, flags the risky lines, and rewrites it so it learns from corrections |

Step 2 already exists. This page is steps 1 and 3.

---

## Step 1 · The Repeat Finder

Works in a chat window and in a terminal agent. It does not guess: every suggestion has a
count and says where it came from, and if nothing repeats enough it says so and stops.

**What it can see decides what it does.** A terminal agent can read your saved history and
count. A chat window usually cannot see past chats, so it asks you five short questions
instead and says plainly that the evidence is what you told it.

```
===== COPY FROM HERE =====
```

I want you to find the things I keep doing by hand, then tell me which are worth turning into
skills. A skill is one task written down once, so you stop improvising it. Write no skill until
I have picked one.

**How to run this**

**Start by telling me what you can see, in one line, and ask me to correct you.** Do not ask
me what access you have: you know that better than I do. Say whichever is true:
- "I can read your saved history and files on this machine."
- "I can see your memory or past chats in this tool."
- "I can only see what you tell me in this chat."

**If you can see history, ask me once whether you may read it.** Name the sources in that one
question and let me answer yes, no, or which. Open nothing until I say yes. If I say no, or you
can see nothing, run the interview below, and say plainly that your evidence is only what I
told you.

**Reading it, once I say yes**
- Read locally. Send nothing anywhere.
- **Before you open any message text, scan every source for secrets:** sk-, key, token, secret,
  password, bearer, AKIA, ghp_, BEGIN, and any run of 24 or more letters and digits. Do not open
  a source that matches. Name it, count it, and leave it out. Tell me you did this.
- Count with commands (grep, sort, uniq -c, wc). Do not estimate by eye. Show me each command.
- Report patterns and counts only: no quotes, no email addresses, no names, no file contents.
- Look back 30 days unless I say otherwise.
- Look for four kinds of repeat:
    a. the same kind of request, three or more times
    b. the same steps in the same order
    c. the same correction from me, twice or more. This is the strongest signal: it is a
       missing line in a skill.
    d. the same files or tools used together

**The interview, when you cannot see any history**

Ask **one question at a time** and wait. Never send a list: I will answer the easiest one and
ignore the rest. **Five questions, and five is the limit.** If I say "skip" or "I don't know",
move on and say what you assumed.

1. What did you redo last week that you would hand to a colleague if you could?
2. What did you ask me for three or more times this month, worded a little differently?
3. What did you correct me on twice? ("No, not like that" is the signal.)
4. Which steps do you do in the same order every time?
5. What do you copy from the last version of something before you start?

If I get impatient and tell you to just suggest something: use what I have told you, mark every
assumption, and still finish with the one thing for tonight.

**Then suggest at most three skills**, about 60 words each:

```
name     — short and hyphenated
seen     — how many times, over what period, and where. Or "from what you told me".
trigger  — the words I would use when I want it
worth    — one line: time saved, or mistakes avoided
stable   — yes or no: is it done the same way each time? If no, say it is not ready.
gaps     — what you could not see and would need to ask me
```

Rank by how often it happens, times how stable it is. **If nothing appears three or more
times, say "nothing repeats enough yet" and stop.** An honest empty answer is a good answer.

**Then ask which one I want first, and write it.** Ask me, one at a time: how I do it now, in
order, including the fiddly parts; then what keeps going wrong and what a right one looks like.
Write it as one block:

```
name    — short, hyphenated
when    — the situations where I'd reach for this
ask     — what you need to know first
steps   — from my answer, in my order
good    — how I know it's right
avoid   — what I keep having to fix
```

**`steps` must come from what I told you.** Do not invent a tidier process. Mark gaps with
`(check this)`. Last line, matching how I will use it:
- Terminal agent — *"If I correct you twice on the same thing while using this skill, add the
  rule to this file before you finish."*
- Chat window — *"If I correct you while using this, show me the whole block again with the fix
  in it, from its first line, so I can paste it back."*

**Do not save anything to disk, even if you can.** Paste the block and tell me where it goes:
- Terminal agent: for Claude Code, `.claude/skills/<name>/SKILL.md`, and it **needs frontmatter
  or it will not load** (`---`, `name:`, `description:`, `---`). For any other agent, a heading
  in `AGENTS.md`, or its own skills folder if it has one.
- ChatGPT, Gemini, Claude.ai, Copilot: paste it at the top of a chat when I need it, or put it in
  a Project, a Gem or custom instructions.
- On a phone: keep it in one note and paste it.

**Then give me one thing to do tonight. Never skip this, however rushed we were.** Name a
specific real task I could run the skill on in the next ten minutes, in my words.

```
===== COPY TO HERE =====
```

**Where history lives.** Claude Code keeps it as files under `~/.claude/projects/`. Other
tools keep theirs somewhere else, or not as plain files at all, so the prompt says *find your
own history, or tell me you can't* instead of naming paths. In a chat tool, if it has memory or
can search past chats, it will use that. If you paste history, **paste titles only**: pasting
sends it to that provider.

**What it cannot do.** It cannot see across tools unless their history is readable. It cannot
tell you which repeats are worth the effort; the ranking is a judgement call. And a model
reading a very large history can miss things, which is why it counts with commands.

**Run it once a month.** What you repeat changes.

---

## Step 2 · Write it

Pick the top suggestion and give it to [the generator](01-generator-prompt.md), or just say yes
when the Finder offers. It writes the skill from how *you* describe doing the task, and marks
what you left out with `(check this)`.

---

## Step 3 · The Skill Doctor

Paste any skill under it: one you wrote, one a colleague sent, one from GitHub. It checks the
skill, scans it for risky lines, and rewrites it into the shape that makes a skill get better
with use.

```
===== COPY FROM HERE =====
```

I want you to check a skill I will paste, tell me whether it is safe and any good, then fix
it. Check first. Write the fix last.

**How to run this**

**If I have not pasted a skill yet, ask for it once** and wait. If I give you a folder or a path
instead, read every file in it, scripts included.

**Tell me what you can see, in one line, and ask me to correct you.** Do not ask me what access
you have: you know that better than I do. Say "I can see the files in this folder" or "I can
only see what you paste here". It matters, because a skill can call scripts, and you can only
judge what you can see.

**Step 1 — Check it.** Answer each, and quote the line you are judging:
  1. Does it say what a good result looks like? Quote it, or say "no definition of good".
  2. Does it say what to avoid? Quote it, or say "no traps listed".
  3. Does it ask me anything when the answer would change the work? Quote it, or say "never asks".
  4. Does it say what to do when I correct it? Quote it, or say "no rule for corrections".

**Step 2 — The risk scan.** List every line that deletes or overwrites something, pushes, posts,
emails, installs, downloads, reaches the network, or tells you to run a command. Say "none seen"
if there are none. If the skill mentions a script or a file you were not given, say "I could not
see <name>", and do not assume it is safe.

Give a verdict in one line: **SAFE TO TRY**, **READ THE FLAGGED LINES FIRST**, or **DO NOT
INSTALL**.

**Step 3 — Fix it.** If it already passes all four checks, say "No rewrite needed", list only
the small changes you would make, and stop. Otherwise rewrite it, keeping my intent and my
wording where it is good, in this shape:

```
---
name: short-and-hyphenated
description: when to use it and when not to, using the words in the original. If the original
  gives no trigger words, write (check this). Do not make up example phrases.
---
## Get the context that changes the answer
What you need to know before starting. Ask me. Do not assume.
## Procedure
Numbered, in the order the original gives.
## Deliverable
What I get back, and what good looks like.
## Traps
What goes wrong, from the original.
## When you are corrected
A correction is a change to the method, not just to this answer. Name what it changes. Say it
back as one rule in my words. Offer the line for keeping, and say plainly that it is lost when
the conversation ends unless I save it. If the same correction arrives twice, say so, and
treat it as a missing line in this file.
```

Rules for the rewrite:
- **Do not add steps, traps, checks or questions that are not in the original**, and do not
  invent numbers, thresholds, tools or example phrases. Where the original is silent, write
  `(check this)`. If you think something is missing, list it AFTER the skill under "Suggested
  additions" and leave it out of the skill.
- The one exception is a DO NOT INSTALL verdict. Then remove or neutralise each dangerous line,
  and list every change you made and why.
- **Keep names, paths and accounts as written.** List any that look specific to the author's own
  setup under "Check these fit you", so I can change them.
- Put any question for me AFTER the skill, never inside it. The skill itself must be something
  I can save as it stands.
- Keep only `name` and `description` in the header, so it works in any tool.

**Do not save anything to disk, even if you can.** Show the whole rewritten skill as one block,
from its first line, so I can paste it back, and tell me where it goes:
- Terminal agent: for Claude Code, `.claude/skills/<name>/SKILL.md`; it **needs the `---` header
  or it will not load**. For any other agent, a heading in `AGENTS.md`, or its own skills folder
  if it has one.
- ChatGPT, Gemini, Claude.ai, Copilot: paste it at the top of a chat when I need it, or put it in
  a Project, a Gem or custom instructions.
- On a phone: keep it in one note and paste it.

**Then give me one thing to do tonight. Never skip this.** Name a specific real task I could run
the fixed skill on in the next ten minutes, taken from the skill's own "when".

SKILL
(paste it here)

```
===== COPY TO HERE =====
```

**What it cannot do.** It reads what you paste. A skill folder can hide scripts that a pasted
`SKILL.md` does not show, and the Doctor will say "I could not see" rather than guess. For a
whole folder, run it in a terminal agent and point it at the path. It also can't catch what is
cleverly hidden: **read the flagged lines yourself before you install anything.**

**Why the rewrite has that shape.** The `When you are corrected` section is what makes a skill
improve. It is the same rule behind [making it remember](08-make-it-remember.md): once is a
correction, twice is a missing line. The [36 business analytics skills](https://github.com/moheetsubudhi-isb/business-analytics-skills)
all use this shape.

---

## Where to find skills to run the Doctor on

A skill is a folder of text, so any tool that reads folders can use one. A few places to look:

- [anthropics/skills](https://github.com/anthropics/skills) — first-party, and the reference for what a well-written one looks like
- [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) — a big index by category; browse, then pick one
- [obra/superpowers](https://github.com/obra/superpowers) — a framework as much as a collection; it installs hooks and scripts, so run the Doctor on it first

Most public skills were written for someone else's process. Install five, keep one, and run the
Doctor on the one you keep.

---

## What's been tested, honestly

Both prompts were run against Claude over four rounds, and rewritten three times after real
problems turned up. The Finder ran against a made-up history with a planted secret and a planted
email, and printed neither. The Doctor ran against a good skill, a thin one and a deliberately
dangerous one. The last version, written in the same shape as the generator, passed every check
once one of the checks was corrected for being too narrow.

What the early runs caught: the Doctor invented trigger phrases, added a confirmation step the
skill never had, and stripped a name that was the owner's own; and the Finder read a secret
before it had scanned for one. All fixed. **Each prompt has been run once per case, so treat
this as reviewed, not proven.** It has not been run in ChatGPT, Gemini or Copilot. If it
misbehaves in yours, that is a bug in the file; tell me.

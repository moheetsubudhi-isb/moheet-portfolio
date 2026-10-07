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

Find the things I keep doing by hand, and tell me which are worth turning into skills.

A skill is one task written down once, so you stop improvising it. I want this found from
evidence, not guessed.

STEP 1 — What can you actually see?
Tell me in two lines which of these you can reach. Ask me before you read any of them.
  - your saved history with me: past sessions, memory, past chats you can search
  - the files in this folder
  - shell history, if you can run commands
If you can reach none of them, say so, and go to STEP 1B. Do not pretend.

STEP 1B — If you cannot see any history, ask me these, ONE AT A TIME. Wait for each answer.
  1. What did you redo last week that you would hand to a colleague if you could?
  2. What did you ask me for three or more times this month, worded a little differently?
  3. What did you correct me on twice? ("No, not like that" is the signal.)
  4. Which steps do you do in the same order every time?
  5. What do you copy from the last version of something before you start?
Then go to STEP 3. Say clearly that your evidence is what I told you, not what you saw.

STEP 2 — Read it safely, only after I say yes.
  - Read locally. Send nothing anywhere.
  - Count with commands (grep, sort, uniq -c, wc). Do not estimate by eye. Show me each
    command you ran.
  - Report patterns and counts. Do not quote my messages, and never print a password, key,
    token, email address, customer name or the contents of a file. If you meet a secret, say
    "found a secret in <where>" and stop reading that source.
  - Look back 30 days unless I say otherwise.
  - Look for four kinds of repeat:
      a. the same kind of request, three or more times
      b. the same steps in the same order
      c. the same correction from me, twice or more. This is the strongest signal: it is a
         missing line in a skill.
      d. the same files or tools used together

STEP 3 — Suggest at most three skills. For each one:
  name     — short and hyphenated
  seen     — how many times, over what period, and where. Or "from what you told me".
  trigger  — the words I would use when I want it
  worth    — one line: time saved, or mistakes avoided
  stable   — yes or no: is it done the same way each time? If no, say it is not ready.
  gaps     — what you could not see and would need to ask me
Rank by how often it happens, times how stable it is.
If nothing appears three or more times, say "nothing repeats enough yet" and stop. An honest
empty answer is a good answer.

STEP 4 — Ask which one I want first. Then ask how I do it, step by step, and write it down as:
name, when to use it, what to ask me first, the steps, what good looks like, what to avoid,
and "if I correct you twice on this, add the rule here".
Mark anything I did not tell you with (check this). Do not invent steps.

Do not save anything to disk, even if you can. Show me the skill as one block.

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

Check the skill I paste below the line that says SKILL, then fix it.
If I give you a folder or a path instead, read every file in it, scripts included, and check
those too.

FIRST, CHECK IT. Answer each of these, and quote the line you are judging:
  1. Does it say what a good result looks like? Quote it, or say "no definition of good".
  2. Does it say what to avoid? Quote it, or say "no traps listed".
  3. Does it ask me anything when the answer would change the work? Quote it, or say "never asks".
  4. Does it say what to do when I correct it? Quote it, or say "no rule for corrections".

THEN THE RISK SCAN. List every line that deletes or overwrites something, pushes, posts,
emails, installs, downloads, reaches the network, or tells you to run a command. Say "none
seen" if there are none.
You can only see what I pasted. If the skill mentions a script or a file you were not given,
say "I could not see <name>" and do not assume it is safe.

Give a verdict in one line: SAFE TO TRY, READ THE FLAGGED LINES FIRST, or DO NOT INSTALL.

THEN REWRITE IT, keeping my intent and my wording where it is good, in this shape:

---
name: <short, hyphenated>
description: <when to use it and when not to, in the words I would actually type>
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

Rules for the rewrite:
  - Do not invent steps, numbers, thresholds or tools. Where the original is silent, write
    (check this).
  - Remove anything that only makes sense for its author's own setup, and list what you removed.
  - Keep only name and description in the header, so it works in any tool.

Show the whole rewritten skill as one block, from its first line, so I can paste it back.

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

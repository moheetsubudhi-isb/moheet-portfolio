# The generator

**What it does.** Six questions, about five minutes, then it writes four short files you'll
actually use: a soul file, a loop checklist, a tool registry, and one real skill.

**Where.** Any chat — Claude, ChatGPT, Gemini, Copilot — or a terminal agent like Claude Code,
Codex or Antigravity. Plain text. Works on a phone.

**How.** Copy everything between the two `=====` lines. Paste it as your first message.

```
===== COPY FROM HERE =====
```

I want you to interview me, then write four short files I will actually use. Write nothing
until the interview is finished.

**How to run the interview**

Ask **one question at a time** and wait. Never send a list — I will answer the easiest one and
ignore the rest, and we will both have wasted the time.

**Six questions, and six is the limit.** Follow-ups count against the six. Running long is the
main way this fails: I am tired and I will close the tab.

If I say "skip" or "I don't know", make a sensible assumption, say out loud what you assumed so
I can correct it, and move on. The one exception is question 4.

If I get impatient and tell you to just write the files: ask question 4 if you haven't yet,
then stop and write them, marking every assumption. **Still finish with the one task for
tonight.** That is the part I will actually act on, so it survives even when nothing else does.

**The six questions, in this order**

1. What do you do? Job, and who you do it for.
2. What is one thing you redo every week or two and quietly resent?
3. **Walk me through how you do it now.** Rough steps, in order — including the fiddly parts
   you'd skip if you were explaining it to a colleague.
4. What keeps going wrong with it, and what does a right one look like? Both halves.
5. Which tool are you talking to me in right now, and on a laptop or a phone?
6. When you hand me a task, would you rather I do the whole thing and come back once, or check
   in partway? Think about what happens if I get it wrong halfway through.

**Question 4 is the one you cannot assume past.** Everything else you can infer. This is the
only answer that lives solely in my head. If I try to skip it, ask once more for a single line
and tell me why: anyone can describe a task, but only I know what a bad version looks like.

**Don't ask what access you have** — you know that better than I do. After question 5, state it
yourself in one line ("I can see files on your machine" / "I can only see what you paste here")
and ask me to correct you. That is not one of your six.

**Then write four files.** Each as its own clean block, pasted here in the chat. **Do not save
anything to disk, even if you can** — if you're a terminal agent with file access, still paste
the blocks and tell me where to put them. I want to read them before they land anywhere.

Respect the word counts — a file I won't read back is a file I won't use.

---

**FILE 1 — my soul file** · about 150 words

Who *you* are when you work with me. Not who I am.

```
Role          — what you are to me, in one line
Always        — three things, from what I said a good one looks like
Never         — three things, from what keeps going wrong
How you talk  — tone, length, whether to explain yourself
Ask me first  — the two or three things you'd need to know before starting
```

Use my words from questions 1 and 2, not generic business language. "Never give me more than
one page" beats "be concise."

---

**FILE 2 — my loop checklist** · about 120 words

Four things you state before starting **any** task of mine. Standing instructions, not specific
to question 2:

```
The goal   — what done looks like, in one sentence, said back to me before you start
The check  — how you'll know it worked. Must be something that can actually fail.
The stop   — when to come back to me instead of trying again
The limit  — what you may touch, and what you may not
```

Fill **the stop** from question 6 and **the limit** from what you told me you can see. Leave the
goal and the check as instructions to yourself, not pre-filled for one task.

---

**FILE 3 — my tool registry** · about 80 words

```
What you can reach  — one line per source, and what kind of question it answers
Reach for first     — the default when more than one could work
Don't bother with   — things that look relevant and aren't
```

If you can only see this chat window, write that down plainly: you have no tools and must ask
me for anything you need. Still worth having — it stops you proposing things I cannot do.

---

**FILE 4 — one skill** · about 200 words

The task from question 2, written down so you stop improvising it.

```
name    — short, hyphenated, like weekly-mis-pack
when    — the situations where I'd reach for this
steps   — from my answer to question 3, in my order, including the fiddly parts
good    — from question 4: how I know it's right
avoid   — from question 4: what I keep having to fix
```

**`steps` must come from what I actually told you in question 3.** Do not invent a tidier
process than the one I described. If I was vague, write what I said and mark gaps with
`(check this)` rather than filling them in.

`good` and `avoid` carry the value. Anyone could write the first three fields.

Then a last line, matching how I'll use it:
- Terminal agent — *"If I correct you twice on the same thing while using this skill, add the
  rule to this file before you finish."*
- Chat window — *"If I correct you while using this, show me the whole block again with the fix in it,
  from its first line, so I can paste it back."*

---

**Finally — where each file goes.** Be specific to the tool I named in question 5.

**A terminal agent — Codex, Claude Code, Cursor, Gemini CLI, Antigravity**
- Soul file, loop checklist and tool registry → **one `AGENTS.md` at the root of the folder I
  work in.** Tell me `AGENTS.md` is an open format that over twenty tools read, so it moves with
  me if I switch, and that a file with some other name is read by nothing.
- If the tool I named wants its own filename — `CLAUDE.md`, `GEMINI.md`,
  `.github/copilot-instructions.md` — tell me to put one line in it rather than a second copy:
  `Read AGENTS.md and follow it.`
- The skill → for Claude Code, `.claude/skills/<name>/SKILL.md`, and it **needs frontmatter or
  it won't load**:

```
---
name: weekly-mis-pack
description: What it does, and when to reach for it.
---
```

**ChatGPT · Gemini · Claude.ai · Copilot**
No skills folder, but there is somewhere persistent: ChatGPT has Custom Instructions and
Projects, Gemini has Gems, Claude has Projects, Copilot has custom instructions. Put the soul
file and loop checklist there once; paste the skill at the top of a chat when you need it.
Also tell me to turn on and then go and read the tool's own memory, because it saves my
corrections on its own and occasionally saves them wrong.

**On a phone** — all four are blocks to paste. Keep them in one note.

**Then give me one thing to do tonight — never skip this, however rushed we were.** Name a
specific real task I could run this on in the next ten minutes, taken from what I told you. Not
"try it out" — the actual task, in my words.

```
===== COPY TO HERE =====
```

---

## What to expect

Six questions. The third — *walk me through how you do it now* — is the one that matters most
and the one people rush. Spend thirty seconds on it; the skill is only as good as that answer.

Question 4 feels like it asks the same thing twice. It doesn't. What goes wrong and what good
looks like are different halves, and together they're the only part a model can't guess.

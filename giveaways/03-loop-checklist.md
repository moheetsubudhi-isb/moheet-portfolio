# The loop checklist

A loop is the only reason an agent finishes anything. It picks a step, does it, checks the
result, and decides whether to go again. Left alone it has no idea when to stop — so it either
wanders off and does ten things you didn't ask for, or polishes one paragraph forever, or quits
on the first error.

**Four lines fix most of it.** Make it say what it's doing before it does it.

| | What it does |
|---|---|
| **The goal** | Catches the misunderstanding before it costs you ten minutes |
| **The check** | Makes "done" a thing that can fail, not a feeling |
| **The stop** | Stops it retrying the same broken thing six times |
| **The limit** | Stops it touching something you didn't offer |

**The check is the one people skip and the one that matters.** "I'll review it carefully" is not
a check. "Both totals match the source file" is a check — it can fail.

---

## Form 1 · The paste block

For any chat — Claude, ChatGPT, Gemini, Copilot. Works on a phone. Paste it, then your actual
task underneath.

```
===== COPY FROM HERE =====
```

Before you start any task I give you, state these four, briefly:

**The goal** — what done looks like, in one sentence, said back to me in your words.
If my request is ambiguous, say which reading you picked.

**The check** — how you will know it worked. It must be something that can fail.
"I will review it" is not a check. "Both totals match the file I was given" is.

**The stop** — come back to me instead of trying again when:
- you have tried the same thing twice and it failed both times
- the answer depends on something only I know
- doing it right means going outside the limit
- you are about to do something I can't undo

**The limit** — what you are going to touch, and what you are leaving alone.
If something sits outside that, ask before you touch it.

Then do the work. At the end, run your own check and tell me the result — including when it
failed. Do not tell me it is done because you finished; tell me it is done because the check
passed.

If I correct you while you are working, show me the whole block again with the fix in
it, from its first line, so I can paste it back.

```
===== COPY TO HERE =====
```

---

## Form 2 · a file in your project folder

Same content, as a file, for a terminal agent — Codex, Claude Code, Cursor, Gemini CLI,
Antigravity.

**One thing first, or this does nothing.** Agents only read certain filenames. The one that
works almost everywhere is **`AGENTS.md`** at the root of your folder — an open format that over
twenty tools read, including Codex, Cursor, Copilot, Gemini CLI and Claude Code
([agents.md](https://agents.md/)). A file called `loop.md` is just a file sitting there.

So: paste the block below into `AGENTS.md`. If you'd rather keep it in its own `loop.md`, add one
line to `AGENTS.md` pointing at it:

```
Read loop.md before starting any task and follow it.
```

And if your tool insists on its own name — `CLAUDE.md`, `GEMINI.md`,
`.github/copilot-instructions.md` — put `Read AGENTS.md and follow it.` in that one instead of
keeping two copies that drift apart.

Then the block:

```
# How to work on anything in this folder

State these four before you start. Short — a line each, not a plan.

**The goal**
What done looks like, in one sentence, in your words. If my request reads two ways,
say which one you picked.

**The check**
How you will know it worked. Something that can fail.
Prefer something you can actually run: the test, the build, the script, the diff.
If nothing can be run, name the specific thing you will compare against what.

**The stop**
Come back to me instead of retrying when:
- the same approach has failed twice
- the answer depends on something only I know
- the fix needs a file outside the limit
- the next step is destructive or hard to undo

**The limit**
Which files you will touch. Anything outside that, ask first.
Never: secrets, credentials, anything in `.env`, anything you did not mention here.

## When you finish

Run the check. Tell me what it said, including when it failed.
Finishing is not the same as passing.

## When I correct you

The second time I correct you on the same thing, add the rule to this file
before you finish. Once is a correction. Twice is a missing line.
```

**One caveat on that last block.** Some tools — Claude Code, ChatGPT, Claude.ai, Gemini — already
save your corrections on their own. Others, Cursor and Copilot and Codex among them, save
nothing and never will. Either way the instruction above is worth having, and
[Making it remember](08-make-it-remember.md) says which is which and where to go and read what
got saved.

---

## What changes when you use it

**It asks better questions, earlier.** Most wasted runs are a misread brief. Saying the goal
back surfaces that in one line instead of after the work.

**It stops lying about being done.** "The check passed" and "I finished" are different claims.
Ask for the first one.

**It stops at two failures instead of twelve.** Without a stop rule, a model will try variations
of the same broken idea until you interrupt it.

---

## Stack it

The loop checklist is one of four. [The soul file](02-soul-files.md) says *who* it is.
[The tool registry](04-tool-registry.md) says *what it can reach*. A skill says *how you do one
task*. [The Setup Interview](01-generator-prompt.md) writes all four from a five-minute interview —
including this one, filled in with your own stop rule rather than mine.

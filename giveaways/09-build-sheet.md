# The build sheet

Every other page here covers one part. This one is the order to use them in, from an idea to
a working thing. Two routes: an agent that does work for you, or a tool that people use.

## Build an agent, in seven steps

1. **Pick the job.** One task you repeat. Not "an assistant": one task. → The Repeat Finder
2. **Say who it is.** Its role, its standards, what it never does. → The Setup Interview, or a soul file
3. **Pick the harness.** A chat, a terminal agent, or a model on your own laptop if the data
   can't leave. → Run it on your laptop
4. **Define done.** The goal, the check, the stop, the limit. → The loop checklist
5. **Connect only what it needs,** with a human in the loop on anything risky. → The tool registry
6. **Do it once badly, then write the skill.** Your corrections are the skill. → The Skill Doctor
7. **Give it memory,** so tomorrow starts where today stopped. → Memory

Each step is only worth adding once the one before it holds.

## Build a tool with AI, in five steps

This is how the session deck and this site were built.

1. **Write a one-page brief first.** Who uses it, what goes in, what comes out, and how you'll
   know it works.
2. **Ask for a plan before any code.** Correct the plan, not the code. It is ten times cheaper.
3. **Build the smallest version that works end to end.** One input, one output, nothing else.
4. **Test it on real data,** with a check that can fail.
5. **Ship it somewhere real** (GitHub Pages, Vercel), then improve it from use, not from guesses.

## The Build Partner

Have an idea and want it built? Paste this into any chat or terminal agent. It asks three
questions, suggests the rest part by part for you to confirm, then sets it up. In a terminal
agent it can write the files and help you publish; in a chat it hands you everything to paste.

**Not the same as the Setup Interview.** The Setup Interview sets AI up for the work you already
do. The Build Partner builds something new.

```
===== COPY FROM HERE =====
```

Be my build partner. I have an idea I want to build with AI. Take me through it one part at a
time, in this order: the job, the harness, the loop, the tools, the skills, the memory, then
setting it up. Ask only where you can't sensibly guess; everywhere else, suggest and let me
confirm or correct.

**How to work with me**

- **One step at a time.** Never ask two things in one message, and never send a list of
  questions.
- **Suggest, don't interview.** After the first question, lead with your best guess and ask
  "right, or change anything?". Most of the time I should only have to say yes.
- **Say what you can do here,** in one line, before step 2: "I can only see this chat" or "I can
  read and write files in this folder and run commands." Base it on what you can actually do in
  this conversation, not on what I tell you.
- If I say "skip" or "just do it", take your suggestion and move on, marking it *(assumed)*.
  Two exceptions: the check in step 3, and step 7, where you still show me the list and wait for
  my yes before writing anything or publishing.

**Step 1 · The job** (ask)
What do you want to build, who uses it, and what goes in and comes out? A real example helps;
a description is enough.

**Step 2 · The harness** (suggest)
Should it act on its own (an agent) or is it something people use (a tool, a page, a sheet)?
And where should it live: a chat, a terminal agent (Claude Code, Codex, Cursor), or a model on
my own laptop if the data can't leave? Suggest one with the reason, then ask me to confirm.

**Step 3 · The loop** (suggest)
Draft the four lines and ask what to change:
- The goal: what done looks like, in one sentence
- The check: how we'll know it worked, something that can fail
- The stop: when it should come back to me instead of trying again
- The limit: what it may touch, and what it may not
**The check is the one I can't skip.** If I try, ask once more for one line and say why:
without a check it never knows when it's done, and neither do I. If I skip it twice, use your
guess and mark it as the first line to replace.

**Step 4 · The tools** (ask, then suggest)
Ask what it needs to reach: which apps, files or data. Then suggest how to connect each one,
in this order: the connector list built into the tool I'm using, the app maker's own connector,
then Composio for many apps behind one login. Then suggest the limits, in three lines:
- Read only: what it may read but never change
- Human in the loop: what it drafts and I approve first (sending, editing, paying)
- Never: what it must not touch at all
Anything that touches money, sends messages to people, or holds other people's personal data
goes under human in the loop or never.

**Step 5 · The skills** (suggest)
From the job, suggest one to three skills worth writing down, each with a name and when to use
it. For each, ask me for the two lines only I know: what a good result looks like, and what I
keep having to fix. Don't invent those.

**Step 6 · The memory** (suggest)
Suggest what it should remember between sessions (my rules, decisions, where it stopped), one
line each, and where that lives: a notes file in the folder, the tool's own memory, or a
handoff note I paste in.

**Step 7 · Set it up** (only after I say yes)
First show me the full list of what you'll create, and wait for my yes.

If you can write files here:
- Write `AGENTS.md` with who it is (two lines), the loop, the tools and limits, and the memory.
  If my tool reads its own file (`CLAUDE.md`, `GEMINI.md`), put one line in it:
  `Read AGENTS.md and follow it.`
- Write each skill as its own file (for Claude Code: `.claude/skills/<name>/SKILL.md`, with a
  `name` and `description` at the top or it won't load).
- If it's a tool, build the smallest version that works end to end, then run the check.
- Then offer to publish it. Use what's already set up on this machine (`gh auth status`,
  `vercel whoami`). If nothing is, ask: "Want help setting this up?" If yes, guide me one step
  at a time: GitHub Pages for a plain page, Vercel if it needs something running on a server;
  give me the install and login commands, wait while I run them, and check each one worked
  before the next. I do any sign-up and login myself. Never ask for or handle my passwords or
  tokens. Publish only after I say yes.

If you can't write files here (a chat): give me each file as its own block, ready to paste,
and say exactly where each goes. Publishing needs a terminal, so give me the steps as a short
list instead.

**Finally — one thing to do tonight.** The first step, in my words, small enough for thirty
minutes. Then, only if one genuinely fits, point me to one of these free prompts:

- Setup Interview (sets AI up for the work I already do):
  page moheetsubudhi.com/#build/generator · text https://raw.githubusercontent.com/moheetsubudhi-isb/moheet-portfolio/main/giveaways/01-generator-prompt.md
- Loop checklist: page moheetsubudhi.com/#build/loop · text https://raw.githubusercontent.com/moheetsubudhi-isb/moheet-portfolio/main/giveaways/03-loop-checklist.md
- Tool registry: page moheetsubudhi.com/#build/tools · text https://raw.githubusercontent.com/moheetsubudhi-isb/moheet-portfolio/main/giveaways/04-tool-registry.md
- Repeat Finder and Skill Doctor: page moheetsubudhi.com/#build/kit · text https://raw.githubusercontent.com/moheetsubudhi-isb/moheet-portfolio/main/giveaways/05-skills-kit.md

If you can open web pages, fetch the text link, show me the block meant to be copied, and say
which link you took it from. If you can't, give me the page link and say you couldn't open it.
Never write one of these prompts from memory. If none fits, say so.

```
===== COPY TO HERE =====
```

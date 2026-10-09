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
7. **Give it memory,** so tomorrow starts where today stopped. → Second Brain

Each step is only worth adding once the one before it holds.

## Build a tool with AI, in five steps

This is how the session deck and this site were built.

1. **Write a one-page brief first.** Who uses it, what goes in, what comes out, and how you'll
   know it works.
2. **Ask for a plan before any code.** Correct the plan, not the code. It is ten times cheaper.
3. **Build the smallest version that works end to end.** One input, one output, nothing else.
4. **Test it on real data,** with a check that can fail.
5. **Ship it somewhere real** (GitHub Pages, Vercel), then improve it from use, not from guesses.

## The Build Planner

Not sure which route, or which parts you need? Paste this into any chat or agent. Five
questions, then a one-page plan for your idea.

```
===== COPY FROM HERE =====
```

I want you to help me plan something I'll build with AI. Interview me first, then write a
one-page build plan. Write nothing until the interview is finished.

**How to run the interview**

Ask **one question at a time** and wait. Never send a list.

**Five questions, and five is the limit.** Follow-ups count against the five.

If I say "skip" or "I don't know", make a sensible assumption, say what you assumed so I can
correct it, and move on. The one exception is question 4.

If I tell you to just write the plan: ask question 4 if you haven't yet, then write it,
marking every assumption.

**The five questions, in this order**

1. What do you want to build, in one sentence, and who uses it?
2. What goes in, and what should come out? A real example of each if you have one. If you
   don't, describe them and I'll work from that.
3. Should it act on its own (an agent that does the work for you), or is it something people
   use (a tool, an app, a sheet, a page)?
4. How will you know it works? Name one check that can fail.
5. What can it touch? Which data and accounts, and is any of it sensitive or not allowed to
   leave your company?

**Question 4 is the one you cannot assume past.** If I try to skip it, ask once more for one
line, and tell me why: without a check, it never knows when it's done, and neither do I. If I
skip it twice, write the plan anyway with your best guess, and mark it as the line to replace first.

**Don't ask which tool I'm in.** State what you can see in one line ("I can only see this
chat" / "I can see files in this folder") and let me correct you. That is not one of the five.

**Then write the plan.** One clean block, pasted here, 300 to 400 words. Do not save anything to
disk, even if you can. I want to read it first.

```
What we're building — one sentence, in my words
Who it's for        — one line
Done when           — the check from question 4, in my words
Parts it needs      — only the ones it needs, from: model, harness, loop, tools (MCP),
                      skills, context, memory. One line each on why. Then name the ones
                      it doesn't need yet.
Where to build it   — a chat, a terminal agent (Claude Code, Codex, Cursor), or a local
                      model if the data can't leave. Pick one and say why.
Limits              — read only / human in the loop / never, from question 5
Build order         — 3 to 5 steps. Step 1 is the smallest version that works end to
                      end. Every step ends with a check.
Skip for now        — what looks important and isn't, yet
```

**Rules for the plan**

- Use my words, not business language.
- Don't add features I didn't ask for. If you think one matters, put it under "Skip for now".
- Anything that touches sensitive data or money, or sends messages to people, goes under
  "human in the loop".
- If it's something people use, step 1 is a one-page brief and a plan before any code.

**Finally — one thing to do tonight.** The first step, in my words, small enough to do in thirty
minutes. Then, only if one genuinely fits, name the free prompt that helps with it:
- the Setup Interview: writes its soul file, loop checklist, tool registry and one skill
- the loop checklist: makes it state the goal, the check, the stop and the limit first
- the tool registry: which tool for what, and what it may do without asking
- the Repeat Finder: finds the tasks worth turning into skills
- the Skill Doctor: checks a skill and fixes it
If none fits the first step, say so rather than forcing one.

```
===== COPY TO HERE =====
```

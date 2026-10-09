#!/usr/bin/env python3
"""Build index.html from the giveaway markdown, so the page cannot drift from the files.

  node extract-art.js     refresh the deck's diagrams (art.json)
  python3 build.py        rebuild index.html

Paper theme. A poster of numbered objects; clicking one opens it as its own
scrollable view. Everything the visitor copies is pulled from giveaways/*.md at
build time, never retyped here.
"""
import html as H
import json
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
GIVE = HERE / "giveaways" if (HERE / "giveaways").is_dir() else HERE.parent / "giveaways"
REPO = "https://github.com/moheetsubudhi-isb/business-analytics-skills"


def read(name):
    return (GIVE / name).read_text(encoding="utf-8")


def between(txt, a, b):
    return txt.split(a)[1].split(b)[0].replace("```", "").strip()


def content():
    c = {}
    c["generator"] = between(read("01-generator-prompt.md"),
                             "===== COPY FROM HERE =====", "===== COPY TO HERE =====")
    souls = read("02-soul-files.md")
    c["souls"] = [{"name": m.group(1).strip(), "body": m.group(2).strip()}
                  for m in re.finditer(r"^## \d+ · (.+?)\n+```\n(.*?)\n```", souls, re.S | re.M)]
    loop = read("03-loop-checklist.md")
    c["loopChat"] = between(loop, "===== COPY FROM HERE =====", "===== COPY TO HERE =====")
    c["loopFile"] = re.search(r"Then the block:\n+```\n(.*?)\n```", loop, re.S).group(1).strip()
    # Two prompts in one file. Each has code fences inside it, so take everything between the
    # markers and drop the fences, the way the generator is read above.
    kit = re.findall(r"===== COPY FROM HERE =====(.*?)===== COPY TO HERE =====", read("05-skills-kit.md"), re.S)
    c["finder"], c["doctor"] = (re.sub(r"\n{3,}", "\n\n", x.replace("```", "")).strip() for x in kit[:2])
    reg = re.findall(r"```\n(.*?)\n```", read("04-tool-registry.md"), re.S)
    c["regTemplate"], c["regExample"], c["regChat"] = (b.strip() for b in reg[:3])
    c["installClaude"] = ("/plugin marketplace add moheetsubudhi-isb/business-analytics-skills\n"
                          "/plugin install statistics-toolkit@business-analytics-skills")
    c["installCodex"] = "codex plugin marketplace add moheetsubudhi-isb/business-analytics-skills"
    c["installCli"] = "npx skills add moheetsubudhi-isb/business-analytics-skills --list"
    c["ollama"] = "ollama run qwen3.5:2b"
    c["planner"] = between(read("09-build-sheet.md"),
                           "===== COPY FROM HERE =====", "===== COPY TO HERE =====")
    return c


def art():
    a = json.loads((HERE / "art-light.json").read_text(encoding="utf-8"))
    # The deck drew the loop with its top circle at y=-6 (centre 150, offset -110,
    # radius 45 plus stroke), which the 0-origin viewBox cut off. Give it the room
    # rather than move the drawing.
    a["loop"] = a["loop"].replace('viewBox="0 0 1000 300"', 'viewBox="0 -16 1000 318"', 1)
    return a


def icons():
    """Phosphor Icons, MIT, fetched once by fetch-icons and inlined at build time so
    the page needs no icon CDN at runtime."""
    return json.loads((HERE / "icons.json").read_text(encoding="utf-8"))


LINKEDIN = "https://www.linkedin.com/in/moheetsubudhi/"
WHATSAPP = "https://wa.me/919861379000"
MAIL_USER = "moheetsubudhi"
MAIL_HOST = "gmail.com"


CSS = """
*{margin:0;padding:0;box-sizing:border-box}
/* Every tile for every folder is in the markup and all but one set is hidden.
   A display rule on the element beats the attribute, so say it once, here. */
[hidden]{display:none!important}
:root{
  --paper:#F2EEE3; --paper-2:#EAE4D6; --paper-3:#E2DBC9;
  --ink:#17150F; --muted:#5C574C; --faint:#8C8573;
  --line:rgba(23,21,15,.13); --line-2:rgba(23,21,15,.26);
  --accent:#2F4FD4; --accent-rgb:47,79,212;
  --accent-2:#8094E4; --accent-2-rgb:128,148,228;
  --accent-soft:rgba(var(--accent-rgb),.10);
  --display:'Bricolage Grotesque',ui-sans-serif,system-ui,sans-serif;
  --body:'Hanken Grotesk',ui-sans-serif,system-ui,-apple-system,sans-serif;
  --mono:'JetBrains Mono',ui-monospace,SFMono-Regular,Menlo,monospace;
  --e:cubic-bezier(.2,.8,.2,1);
  --r:10px;
  --panel:#FAF8F3;     /* the results panel, and so also the wipe that reveals the arrow */
  --rule:29px;          /* the ruling pitch, and the body line-height, so text sits on it */
}
html{-webkit-text-size-adjust:100%;background:var(--paper)}

/* Paper. A fixed, non-interactive overlay so the grain never repaints while
   anything scrolls: fibre speckle, a faint rule, and a soft vignette. */
body::before{content:"";position:fixed;inset:0;z-index:0;pointer-events:none;
  opacity:.55;mix-blend-mode:multiply;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='180' height='180'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='180' height='180' filter='url(%23n)' opacity='.42'/%3E%3C/svg%3E")}
/* The ruling and the vignette are light on the page, not ink on it: both stay put
   while the content moves over them. Fixed rather than attached, because iOS Safari
   ignores background-attachment:fixed. */
body::after{content:"";position:fixed;inset:0;z-index:0;pointer-events:none;
  background:
    repeating-linear-gradient(to bottom, transparent 0 31px, rgba(23,21,15,.045) 31px 32px),
    radial-gradient(120% 90% at 50% 40%, transparent 55%, rgba(23,21,15,.07) 100%)}
body > *{position:relative;z-index:1}
@media (prefers-reduced-transparency: reduce){body::before{display:none}}
body{background-color:var(--paper);color:var(--ink);font-family:var(--body);
  line-height:1.55;-webkit-font-smoothing:antialiased;overflow-x:hidden}
.wrap{max-width:820px;margin:0 auto;padding:0 20px}
a{color:var(--accent);text-decoration:none;border-bottom:1px solid rgba(47,79,212,.3)}
a:hover{border-bottom-color:var(--accent)}
h1,h2,h3{font-family:var(--display);letter-spacing:-.025em}
h1{font-weight:800;line-height:.94;font-size:clamp(38px,min(9vw,10vh),84px)}
h2{font-weight:800;line-height:1.04;font-size:clamp(27px,5.4vw,42px)}
h3{font-weight:600;font-size:clamp(17px,3.4vw,21px);letter-spacing:-.01em}
p{color:var(--muted);font-size:clamp(15px,3.6vw,17px)}
p + p{margin-top:13px}
p strong,li strong{color:var(--ink);font-weight:600}
.lead{font-size:clamp(16px,4vw,19px);max-width:56ch}

/* ---------- the poster ----------
   Objects sit around the title at wide widths, the way a printed poster would lay
   them out. Below 1040px, and whenever a search is running, they fall back to a
   plain grid: a scatter cannot survive a narrow screen or a changing item count. */
/* The poster is exactly one screen: the objects and the contact row share it, so a
   laptop never scrolls to reach either. */
/* One shell: the poster or an opened item, and under either of them the same
   contact bar. Nothing is duplicated, so the bar cannot drift between the two. */
#shell{min-height:100dvh;display:flex;flex-direction:column}
#poster{flex:1;display:flex;flex-direction:column;justify-content:center}
body.open #poster{display:none}
/* The poster fills what the bar and the contact row leave, and centres its own
   contents inside that, so the bar stays at the top of the page. */
#hub{display:flex;flex-direction:column;justify-content:center;
  padding:clamp(12px,2.4vh,28px) 0 clamp(8px,1.2vh,14px);position:relative;flex:1}
#hub.scatter{flex:1}
/* Climbing out of a folder, back to whatever holds it. */
/* A poster inside a folder uses the same bar as an opened item, at the top of
   the page rather than floating over the heading. */
#poster > .topbar{position:sticky;flex:0 0 auto}
#poster > .topbar .inner{max-width:none;padding-left:clamp(14px,3vw,34px);
  padding-right:clamp(14px,3vw,34px)}
@media(max-width:639px){#poster > .topbar .where{display:none}}
/* The heading is a full-width block, so it sits over the objects beside it and
   eats their clicks. It is only text, so it takes no pointer events. */
.poster-title{text-align:center;padding:0 20px;position:relative;z-index:2;
  pointer-events:none}
/* Ink settling: each word arrives slightly late and slightly out of focus,
   then sets. The old heading leaves as one block rather than word by word, so
   the change reads as a relabel and not as two animations fighting. */
@keyframes inkIn{
  from{opacity:0;transform:translateY(9px);filter:blur(7px)}
  to{opacity:1;transform:none;filter:blur(0)}
}
.poster-title h1 .w{display:inline-block;animation:inkIn .38s var(--e) both;
  animation-delay:var(--d,0s)}
.poster-title h1,.poster-title .sub{transition:opacity .16s var(--e),filter .16s var(--e)}
.poster-title h1.out,.poster-title .sub.out{opacity:0;filter:blur(5px)}
.poster-title .sub .w{display:inline-block;animation:inkIn .38s var(--e) both .12s}
@media (prefers-reduced-motion: reduce){
  .poster-title h1 .w,.poster-title .sub .w{animation:none}
}
.poster-title .sub{font-family:var(--mono);font-size:10.5px;letter-spacing:.16em;
  text-transform:uppercase;color:var(--faint);margin-top:clamp(8px,1.4vh,14px)}
@media(min-width:520px){.poster-title .sub{font-size:11px;letter-spacing:.24em}}
.objects{display:grid;grid-template-columns:repeat(2,1fr);gap:8px;
  max-width:980px;margin:clamp(14px,2.4vh,30px) auto 0;padding:0 14px}
@media(min-width:720px){.objects{grid-template-columns:repeat(4,1fr);gap:10px}}
/* On a phone every folder is the same two-column grid with the same tile, however
   many it holds, and a full folder scrolls. Squeezing eight or eleven tiles onto one
   screen shrank the thumbs until the icons spilled out of them (Moheet, 6 Oct 2026). */
/* Two or three objects are a row in the middle, not a stripe across the page. */
/* auto side margins on a column flex item shrink it to its content, so the width
   has to be stated or the row collapses */
/* One or two objects centre as a row at the same size as every other tile.
   Scaling them up to fill the space changed the proportion of the icon to the
   card, which is the thing that made the poster read. */
.objects.few{display:flex;width:100%;justify-content:center;
  gap:clamp(12px,2.5vw,26px);max-width:560px}
.objects.few .obj{flex:0 1 200px}
@media(min-width:850px){
  #hub.scatter .objects{display:block;position:absolute;inset:0;max-width:none;
    margin:0;padding:0;pointer-events:none}
  #hub.scatter .obj{position:absolute;width:124px;pointer-events:auto;padding:7px;z-index:3;
    transform:rotate(var(--r))}
  #hub.scatter .obj .label{font-size:13px;line-height:1.15}
  #hub.scatter .obj .thumb{padding:10px}
  #hub.scatter .obj:hover,#hub.scatter .obj:focus-visible{
    transform:rotate(0deg) translateY(-4px) scale(1.04);z-index:4}
  #hub.scatter .obj{cursor:grab;touch-action:none}
  #hub.scatter .obj.dragging{cursor:grabbing;z-index:5;transform:rotate(0deg) scale(1.06);
    filter:drop-shadow(0 10px 18px rgba(23,21,15,.18))}
  #hub.scatter .obj .thumb{aspect-ratio:1/1}
}
.obj{position:relative;display:flex;flex-direction:column;gap:4px;text-align:left;
  background:transparent;border:0;padding:7px 7px 9px;cursor:pointer;
  border-radius:var(--r);transition:transform .22s var(--e),background .22s var(--e);
  font-family:inherit;color:inherit}
.obj:hover,.obj:focus-visible{background:rgba(23,21,15,.045);transform:translateY(-3px)}
.obj:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.obj:active{transform:translateY(-1px)}
.obj .thumb{aspect-ratio:16/11;display:grid;place-items:center;overflow:hidden;
  border-radius:8px;background:var(--paper-2);padding:6px;
  border:1px solid rgba(23,21,15,.07);max-height:clamp(52px,8.6vh,104px)}
.obj .thumb svg{width:100%;height:auto;max-height:100%}
.obj .thumb .ico{width:clamp(30px,38%,52px);height:auto;max-height:72%;aspect-ratio:1/1;
  color:var(--accent)}
.obj .thumb .ico svg{width:100%;height:100%}
.obj .thumb .glyph{font-family:var(--display);font-weight:800;
  font-size:clamp(26px,6vw,40px);color:var(--accent);letter-spacing:-.03em}
.obj .n{font-family:var(--mono);font-size:9.5px;letter-spacing:.12em;color:var(--faint)}
.obj .label{font-family:var(--display);font-weight:600;font-size:clamp(13px,3.2vw,15.5px);
  line-height:1.18;letter-spacing:-.01em}
.obj .label .arrow{color:var(--accent);opacity:0;transition:opacity .2s}
/* While a search is open the objects step back rather than crowd the panel.
   Faded, not removed: in the scatter they are positioned absolutely, so this
   hides them without anything reflowing. */
#hub.searching .obj{opacity:0;pointer-events:none;transition:opacity .18s var(--e)}
.obj:hover .label .arrow{opacity:1}

/* ---------- search ---------- */
.search{position:relative;z-index:2;max-width:360px;margin:clamp(12px,2vh,20px) auto 0;
  padding:0 20px}
.search .box{position:relative;display:flex;align-items:center;gap:9px;
  border:1px solid var(--line-2);border-radius:999px;padding:9px 15px;
  background:rgba(255,255,255,.4)}
.search .box:focus-within{border-color:var(--accent)}
.search svg{width:16px;height:16px;color:var(--faint);flex:none}
.search input{flex:1;border:0;background:transparent;font-family:var(--body);
  font-size:15px;color:var(--ink);outline:none;min-width:0}
.search input::placeholder{color:var(--faint)}
.search .count{font-family:var(--mono);font-size:10.5px;color:var(--faint);
  text-align:center;margin-top:9px;min-height:14px}

/* Search is a list of every node, not a filter over the tiles: once most of the
   page lives inside folders, hiding root tiles would find almost nothing. */
/* Anchored under the box rather than placed in the flow: the heading, the
   search and the objects must not move while someone is typing. */
/* One width, set by the viewport and not by what happens to match, so the
   panel does not resize itself under the cursor as someone types. */
.results{position:absolute;z-index:8;top:calc(100% + 9px);left:50%;
  transform:translateX(-50%);width:min(min(560px,78vw),calc(100vw - 32px));
  text-align:left}
.results[hidden]{display:none}
/* Solid, not translucent: the nothing-found arrow is revealed by sliding a
   panel-coloured cover off it, and the cover has to match exactly. */
.results ol{list-style:none;margin:0;border:1px solid var(--line-2);border-radius:var(--r);
  background:var(--panel);overflow:hidden;max-height:min(46vh,340px);overflow-y:auto}
.results li + li{border-top:1px solid var(--line)}
.results button{width:100%;display:flex;align-items:center;gap:11px;text-align:left;
  background:transparent;border:0;padding:10px 13px;cursor:pointer;font-family:inherit;
  color:inherit}
.results button:hover,.results button.on{background:var(--accent-soft)}
.results .ico{width:18px;height:18px;flex:none;color:var(--accent)}
.results .ico svg{width:100%;height:100%}
.results .t{flex:1;min-width:0;font-family:var(--display);font-weight:600;font-size:14.5px;
  letter-spacing:-.01em;line-height:1.25;overflow:hidden;text-overflow:ellipsis;
  white-space:nowrap}
/* The trail is pushed to the far end rather than following the name, which is
   what made the two read as one run-on word. */
.results .c{flex:none;margin-left:14px;font-family:var(--mono);font-size:10px;
  letter-spacing:.08em;color:var(--faint);text-transform:uppercase;white-space:nowrap}
@media(max-width:519px){.results .c{display:none}}

/* Nothing found is not an error, it is an invitation. */
.results .none{padding:20px 16px;display:flex;flex-direction:column;
  align-items:center;gap:2px;text-align:center}

.results .none .say{font-family:var(--display);font-weight:600;font-size:15.5px;
  letter-spacing:-.01em}
.results .none .sub2{font-family:var(--mono);font-size:10.5px;letter-spacing:.08em;
  color:var(--faint);text-transform:uppercase;margin-top:4px}


/* ---------- accent picker ---------- */
.swatches{position:relative;z-index:2;display:flex;justify-content:center;gap:7px;
  margin-top:clamp(10px,1.8vh,16px)}
.sw{width:17px;height:17px;border-radius:999px;border:1px solid rgba(23,21,15,.2);
  cursor:pointer;padding:0;transition:transform .15s var(--e),box-shadow .15s var(--e)}
.sw:hover{transform:scale(1.18)}
.sw[aria-pressed=true]{box-shadow:0 0 0 2px var(--paper),0 0 0 3.5px var(--ink)}
.sw:focus-visible{outline:2px solid var(--ink);outline-offset:3px}

/* ---------- contact ---------- */
.contact{position:relative;z-index:2;display:flex;justify-content:center;gap:8px;
  flex-wrap:wrap;margin-top:clamp(14px,2.4vh,26px);padding:0 20px}
.contact a{display:inline-flex;align-items:center;gap:8px;font-family:var(--mono);
  font-size:12px;letter-spacing:.03em;color:var(--muted);border:1px solid var(--line);
  border-radius:999px;padding:8px 15px;background:rgba(255,255,255,.35)}
.contact a:hover{border-color:var(--accent);color:var(--accent);background:var(--accent-soft)}
.contact svg{width:16px;height:16px;flex:none}
.hub-foot{text-align:center;margin-top:10px;font-family:var(--mono);font-size:10.5px;
  letter-spacing:.1em;color:var(--faint)}
/* The same bar under the poster and under an opened item: how to reach me, the
   accent, and the reset once anything has been moved. */
#chrome{flex:0 0 auto;border-top:1px solid var(--line);margin-top:auto;
  padding:clamp(12px,2vh,20px) 20px clamp(14px,2.4vh,26px)}
#chrome .row{max-width:980px;margin:0 auto;display:flex;align-items:center;
  justify-content:center;gap:10px;flex-wrap:wrap}
#chrome .contact{margin-top:0;padding:0;gap:8px}
#chrome .swatches{margin-top:0}
#chrome .tail{position:relative;display:flex;align-items:center;gap:10px}
.corner{position:fixed;left:clamp(14px,2.4vw,30px);bottom:clamp(14px,2.4vh,26px);z-index:7;
  display:flex;flex-direction:column;align-items:flex-start;gap:8px;pointer-events:none}
.corner > *{pointer-events:auto}
body.open .corner{display:none}

/* ---------- a detail view ---------- */
#view{display:none}
body.open #hub{display:none}
body.open #view{display:block}
.topbar{position:sticky;top:0;z-index:40;background:rgba(242,238,227,.9);
  backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);
  border-bottom:1px solid var(--line)}
.topbar .inner{max-width:820px;margin:0 auto;padding:11px 20px;
  display:flex;align-items:center;gap:14px}
.back{font-family:var(--mono);font-size:12px;letter-spacing:.04em;color:var(--ink);
  border:1px solid var(--line-2);border-radius:999px;padding:7px 14px;background:transparent;
  cursor:pointer;white-space:nowrap}
.back:hover{border-color:var(--accent);color:var(--accent)}
.where{font-family:var(--mono);font-size:11px;letter-spacing:.14em;
  text-transform:uppercase;color:var(--faint);overflow:hidden;text-overflow:ellipsis;
  white-space:nowrap;min-width:0}
.topbar .search{margin:0 0 0 auto;padding:0;flex:0 1 268px;min-width:132px;z-index:41}
.topbar .search .box{padding:7px 13px}
.topbar .search input{font-size:13.5px}
.topbar .search .count{display:none}
/* Anchored to the right edge of the box here, not centred on it, or it would
   hang off the side of the window. */
.topbar .search .results{left:auto;right:0;transform:none;
  width:min(420px,calc(100vw - 28px))}
/* On a narrow screen the trail gives way to the input: the heading underneath
   already says where you are. */
@media(max-width:639px){
  .topbar .where{display:none}
  .topbar .search{flex:1 1 auto}
}
/* Written on the lines: prose uses the ruling pitch for its line-height, and the
   page starts on a whole number of rules so the two stay in step as you scroll. */
#view{padding-top:0}
.view-body p,.view-body li,.notes li{line-height:var(--rule)}
.view-body p{font-size:clamp(15px,3.6vw,16.5px)}
.view-head{padding-top:calc(var(--rule) * 2)}
.view-head .n{font-family:var(--mono);font-size:11px;letter-spacing:.2em;color:var(--accent)}
.view-head h2{margin-top:12px}
.view-head .lead{margin-top:16px}
/* Top and bottom only: these share an element with .wrap, whose side padding
   keeps text off the screen edge on a phone. */
.view-body{padding-top:var(--rule);padding-bottom:clamp(50px,11vw,86px)}
.view-body > * + *{margin-top:var(--rule)}

/* ---------- shared blocks ---------- */
.panel{border:1px solid var(--line);border-radius:var(--r);background:var(--paper-2);
  margin-top:24px;overflow:hidden}
.panel-head{display:flex;align-items:center;gap:12px;padding:12px 15px;
  border-bottom:1px solid var(--line)}
.panel-head .t{font-family:var(--mono);font-size:12px;color:var(--muted);letter-spacing:.05em}
.panel-head .note{font-family:var(--mono);font-size:10.5px;letter-spacing:.05em;
  color:var(--faint);margin-left:auto;text-align:right}
.panel-head .t + .copy{margin-left:auto}
pre{font-family:var(--mono);font-size:12.5px;line-height:1.62;color:var(--ink);
  padding:15px;overflow-x:auto;white-space:pre-wrap;word-break:break-word;max-height:340px}
.copy{font-family:var(--mono);font-size:11.5px;letter-spacing:.05em;padding:7px 14px;
  border-radius:999px;border:1px solid var(--line-2);background:transparent;color:var(--ink);
  cursor:pointer;white-space:nowrap;transition:border-color .15s,color .15s,background .15s}
.copy:hover{border-color:var(--accent);color:var(--accent)}
.copy.done{border-color:var(--accent);color:#fff;background:var(--accent)}
.btn{font-family:var(--mono);font-size:12.5px;letter-spacing:.04em;padding:11px 18px;
  border-radius:999px;border:1px solid var(--line-2);color:var(--ink);background:transparent;
  cursor:pointer;display:inline-block}
.btn:hover{border-color:var(--accent);background:var(--accent-soft);color:var(--accent)}
.btn.primary{background:var(--accent);border-color:var(--accent);color:#fff;font-weight:700}
.btn.primary:hover{background:#2440b8;border-color:#2440b8;color:#fff}

.tabs{display:flex;gap:6px;flex-wrap:wrap;margin-top:22px}
.tab{font-family:var(--mono);font-size:11.5px;padding:8px 13px;border-radius:999px;
  border:1px solid var(--line);background:transparent;color:var(--muted);cursor:pointer}
.tab:hover{color:var(--ink);border-color:var(--line-2)}
.tab[aria-selected=true]{background:var(--accent);border-color:var(--accent);color:#fff}

/* the PIN pop-up: the paper card, the mono kicker, the accent. No native dialog, so
   it looks the same on every OS. */
.scrim{position:fixed;inset:0;z-index:100;display:grid;place-items:center;padding:20px;
  background:rgba(23,21,15,.38);opacity:0;transition:opacity .2s var(--e)}
.scrim.on{opacity:1}
.dialog{position:relative;width:min(380px,100%);background:var(--paper);
  border:1px solid var(--line-2);border-radius:14px;padding:30px 28px 24px;text-align:center;
  box-shadow:0 24px 60px rgba(23,21,15,.22);transform:translateY(10px) scale(.97);
  transition:transform .24s var(--e)}
.scrim.on .dialog{transform:none}
.dlg-kicker{font-family:var(--mono);font-size:10.5px;letter-spacing:.24em;color:var(--faint)}
.dialog h3{margin-top:10px;font-size:clamp(24px,6vw,30px);font-weight:800;letter-spacing:-.025em}
.dlg-hint{margin-top:6px;font-size:14.5px}
.dlg-x{position:absolute;top:10px;right:12px;width:34px;height:34px;border:0;background:transparent;
  font-size:24px;line-height:1;color:var(--faint);cursor:pointer;border-radius:8px}
.dlg-x:hover{color:var(--ink);background:rgba(23,21,15,.06)}
.cells{position:relative;display:flex;justify-content:center;gap:10px;margin-top:22px;cursor:text}
.cells input{position:absolute;inset:0;width:100%;height:100%;opacity:0;border:0;
  font-size:16px;caret-color:transparent}   /* 16px so iOS does not zoom the page */
.cell{width:50px;height:60px;display:grid;place-items:center;border:1px solid var(--line-2);
  border-radius:var(--r);background:rgba(255,255,255,.55);font-family:var(--mono);
  font-size:26px;color:var(--ink);transition:border-color .15s,box-shadow .15s}
.cell.on{border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-soft)}
.cells.bad .cell{border-color:#B3431E}
.cells.bad{animation:nope .34s}
@keyframes nope{20%,60%{transform:translateX(-6px)}40%,80%{transform:translateX(6px)}}
.dlg-msg{min-height:var(--rule);margin-top:14px;font-family:var(--mono);font-size:12px;
  letter-spacing:.04em;color:var(--muted)}
@media (prefers-reduced-motion: reduce){
  .scrim,.dialog{transition:none}.cells.bad{animation:none}
}
/* a small lock on the tile, so it reads as locked before it is touched */
.lockmark{position:absolute;right:7px;bottom:7px;width:17px;height:17px;color:var(--faint)}
.lockmark svg{width:100%;height:100%}
.thumb{position:relative}

.split{display:grid;gap:16px;margin-top:24px}
@media(min-width:760px){.split{grid-template-columns:1fr 1fr}.split .panel{margin-top:0}}

details{border:1px solid var(--line);border-radius:var(--r);background:var(--paper-2);
  margin-top:12px;overflow:hidden}
summary{padding:13px 15px;cursor:pointer;font-family:var(--mono);font-size:12.5px;
  color:var(--ink);list-style:none;display:flex;align-items:center;gap:10px}
summary::-webkit-details-marker{display:none}
summary .arrow{color:var(--faint);transition:transform .15s}
details[open] summary .arrow{transform:rotate(90deg)}
summary .note{color:var(--faint);font-size:11px;margin-left:auto}
summary .copy{margin-left:auto}
summary .note + .copy{margin-left:14px}

.fig{margin-top:24px;border:1px solid var(--line);border-radius:var(--r);
  background:var(--paper-2);padding:16px;overflow:hidden}
.fig svg{display:block;width:100%;height:auto}
.fig .cap{font-family:var(--mono);font-size:10.5px;letter-spacing:.1em;
  text-transform:uppercase;color:var(--faint);margin-top:11px}

table{width:100%;border-collapse:collapse;margin-top:20px;font-size:14.5px}
th,td{text-align:left;padding:11px 12px 11px 0;vertical-align:top}
th{font-family:var(--mono);font-size:10.5px;letter-spacing:.13em;text-transform:uppercase;
  color:var(--faint);font-weight:400;border-bottom:1px solid var(--line-2)}
td{color:var(--muted);border-bottom:1px solid var(--line)}
td:first-child{color:var(--ink);font-weight:600;white-space:nowrap;padding-right:18px}
code{font-family:var(--mono);font-size:.88em;color:var(--ink);
  background:var(--paper-3);padding:2px 6px;border-radius:5px}

ul{list-style:none;margin-top:16px}
ul li{color:var(--muted);font-size:clamp(15px,3.6vw,16.5px);padding:8px 0 8px 20px;
  position:relative}
ul li::before{content:"";position:absolute;left:0;top:17px;width:8px;height:1px;
  background:var(--faint)}

.rule{font-family:var(--display);font-weight:800;font-size:clamp(21px,4.8vw,32px);
  line-height:1.22;letter-spacing:-.02em;color:var(--ink);max-width:21ch;margin-top:22px}
.formula{font-family:var(--mono);font-size:clamp(11.5px,2.9vw,14px);line-height:2;
  display:flex;flex-wrap:wrap;gap:6px;align-items:center;justify-content:center}
.f-op{color:var(--faint)}.f-key{color:var(--accent)}
.f-out{color:var(--ink);font-weight:500}
.f-end{color:var(--ink);font-weight:700;border-bottom:2px solid var(--accent)}

/* The nudge sits above the reset in the bar, so the arrow points past it at the
   folders rather than at the button under it. */
.hint{display:flex;flex-direction:column;align-items:flex-start;gap:3px;white-space:nowrap;
  font-family:var(--mono);font-size:10.5px;line-height:1.35;letter-spacing:.06em;
  color:var(--faint);text-align:left;animation:hintIn .6s var(--e) both .9s}
.hint svg{width:68px;height:38px;fill:none;stroke:var(--faint);stroke-width:1.7;
  stroke-linecap:round;stroke-linejoin:round;margin-left:6px}
/* Two passes over the same line, the way a pencil actually leaves one. */
.hint svg path{stroke-dasharray:170;stroke-dashoffset:170;
  animation:draw 1.1s var(--e) forwards 1.25s}
.hint svg .pass2{opacity:.45;animation-delay:1.45s;animation-duration:.95s}
.hint.gone{animation:hintOut .4s var(--e) both}
@keyframes draw{to{stroke-dashoffset:0}}
@keyframes hintIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
@keyframes hintOut{to{opacity:0;transform:translateY(4px)}}
body.open .hint,body.open .reset{display:none}
.reset{font-family:var(--mono);font-size:10px;letter-spacing:.1em;color:var(--faint);
  background:rgba(255,255,255,.4);border:1px solid var(--line-2);border-radius:999px;
  cursor:pointer;padding:6px 12px}
.reset:hover{color:var(--accent);border-color:var(--accent)}
@media (prefers-reduced-motion: reduce){
  .hint{animation:none}
  .hint svg path{animation:none;stroke-dashoffset:0}
}

html.reveal .view-body > *{opacity:0;transform:translateY(16px);
  transition:opacity .5s var(--e),transform .5s var(--e)}
html.reveal .view-body > *.in{opacity:1;transform:none}
@media (prefers-reduced-motion: reduce){
  *{transition:none!important;animation:none!important}
  html.reveal .view-body > *{opacity:1;transform:none}
}
@keyframes rise{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
@keyframes settle{
  from{opacity:0;transform:rotate(var(--r)) translateY(-14px) scale(.94)}
  to{opacity:1;transform:rotate(var(--r))}
}
html.anim .obj{animation:settle .5s var(--e) both;animation-delay:var(--d,0s)}
html.anim #hub.scatter .obj{animation-name:settle}
@media (prefers-reduced-motion: reduce){html.anim .obj{animation:none}}
::view-transition-old(root),::view-transition-new(root){animation-duration:.26s}

/* ---------- the stamp ----------
   Same tile, same size, same drag. Only what sits inside the thumb changes: a
   perforated postage stamp with a photo instead of an icon. Frame and lettering
   take the accent, so the picker recolours it like every other icon. */
/* Pinned to the thumb's box: the thumb's height comes from max-height, which a
   percentage height inside it cannot see. */
.stamp-wrap{position:absolute;inset:clamp(2px,5%,5px);display:flex;justify-content:center;
  filter:drop-shadow(0 1px 1.5px rgba(23,21,15,.22))}
.stamp{--p:2.6px;height:100%;aspect-ratio:4/5;flex:none;background:#FFFDF7;
  padding:calc(var(--p)*2.2);display:grid;grid-template-rows:1fr auto;gap:2px;
  -webkit-mask:radial-gradient(var(--p),#0000 97%,#000) round
      calc(var(--p)*-1.5) calc(var(--p)*-1.5)/calc(var(--p)*3) calc(var(--p)*3),
    linear-gradient(#000 0 0) no-repeat 50%/calc(100% - var(--p)*3) calc(100% - var(--p)*3);
  mask:radial-gradient(var(--p),#0000 97%,#000) round
      calc(var(--p)*-1.5) calc(var(--p)*-1.5)/calc(var(--p)*3) calc(var(--p)*3),
    linear-gradient(#000 0 0) no-repeat 50%/calc(100% - var(--p)*3) calc(100% - var(--p)*3)}
.stamp img{display:block;width:100%;height:100%;min-height:0;object-fit:cover;
  object-position:50% 18%;outline:1px solid var(--accent);outline-offset:1px}
/* The stamp keeps its 4:5 shape whatever its label says: a long name is clipped,
   never allowed to widen the stamp. Below about 56px tall the label is unreadable,
   so it gives its room to the face instead. */
.stamp-wrap{container-type:size}
.stamp{min-width:0;grid-template-columns:minmax(0,1fr);overflow:hidden}
.stamp .st{min-width:0;overflow:hidden}
@container (max-height:56px){
  .stamp{--p:1.7px;aspect-ratio:1/1;grid-template-rows:1fr;padding:calc(var(--p)*2)}
  .stamp .st{display:none}
  .stamp img.logo{padding:4%}
}
/* A logo sits whole on white; an icon takes the accent, like every other icon. */
.stamp img.logo{object-fit:contain;object-position:50% 50%;background:#fff;padding:12%}
.stamp .face.icon{display:grid;place-items:center;min-height:0;background:#fff;color:var(--accent);
  outline:1px solid var(--accent);outline-offset:1px}
.stamp .face.icon svg{width:58%;height:auto}
.stamp .st{font-family:var(--mono);font-weight:500;font-size:7px;line-height:1;
  letter-spacing:.14em;color:var(--accent);text-align:center;white-space:nowrap}

/* ---------- the CV, as an old application form ----------
   Restraint is the whole look: ruled boxes, mono small caps, one rubber stamp. */
.cv-dl{display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.cv-dl .note{font-family:var(--mono);font-size:10.5px;letter-spacing:.1em;
  text-transform:uppercase;color:var(--faint)}
.form{border:1.5px solid var(--ink);background:#FBF9F2;
  box-shadow:3px 3px 0 rgba(23,21,15,.08)}
.form-head{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;
  border-bottom:1.5px solid var(--ink);padding:9px 14px;font-family:var(--mono);
  font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:var(--ink)}
.fsec{padding:16px 14px 18px;border-bottom:1px solid var(--line-2)}
.fsec:last-child{border-bottom:0}
.fh{font-family:var(--mono);font-size:11px;font-weight:500;letter-spacing:.2em;
  text-transform:uppercase;color:var(--ink);display:flex;gap:10px;margin:0 0 12px}
.fh b{color:var(--accent);font-weight:500}
.form p,.form li{font-size:14.5px;line-height:1.55;color:var(--muted)}
.form ul{margin-top:6px}
.form li strong{color:var(--ink);font-weight:600}
.form ul li{padding:2px 0 2px 16px}
.form ul li::before{top:12px;width:7px}
.fgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,190px),1fr));
  border-top:1px solid var(--line-2);border-left:1px solid var(--line-2)}
.f{border-right:1px solid var(--line-2);border-bottom:1px solid var(--line-2);
  padding:7px 10px 8px;min-width:0}
.f .k{display:block;font-family:var(--mono);font-size:9px;letter-spacing:.18em;
  text-transform:uppercase;color:var(--faint)}
.f .v{display:block;color:var(--ink);font-size:14.5px;line-height:1.4;overflow-wrap:anywhere}
.f .v a{border-bottom:0}
.particulars{display:grid;grid-template-columns:1fr auto;gap:14px;align-items:start}
.photo{position:relative;width:clamp(84px,22vw,116px)}
.photo img{display:block;width:100%;height:auto;aspect-ratio:4/5;object-fit:cover;object-position:50% 18%;
  border:1px solid var(--line-2);background:#fff;padding:3px}
.photo .k{display:block;text-align:center;margin-top:5px;font-family:var(--mono);font-size:8.5px;
  letter-spacing:.16em;text-transform:uppercase;color:var(--faint)}
.rubber{position:absolute;left:-16px;top:12px;transform:rotate(-14deg);
  border:2px solid var(--accent);border-radius:4px;padding:3px 7px;
  font-family:var(--mono);font-weight:500;font-size:10px;letter-spacing:.18em;
  color:var(--accent);background:rgba(251,249,242,.7);opacity:.9;white-space:nowrap;
  pointer-events:none}
.rec{display:grid;grid-template-columns:158px 1fr;gap:4px 16px;padding:12px 0;
  border-top:1px dashed var(--line-2)}
.rec:first-of-type{border-top:0;padding-top:2px}
.rec .when{font-family:var(--mono);font-size:11px;letter-spacing:.04em;color:var(--faint);
  padding-top:3px}
.rec .who{font-family:var(--display);font-weight:600;font-size:16px;color:var(--ink);
  letter-spacing:-.01em;line-height:1.3}
.rec .who span{font-family:var(--body);font-weight:400;font-size:14px;color:var(--muted)}
@media(max-width:559px){
  .rec{grid-template-columns:1fr}
  .particulars{grid-template-columns:1fr}
  .photo{justify-self:start}
  /* Beside the photo rather than over the face, which a narrow photo cannot spare. */
  .rubber{left:calc(100% + 10px);top:38%}
}
.sign{display:flex;justify-content:space-between;align-items:flex-end;gap:16px;flex-wrap:wrap}
.sign .line{min-width:180px;border-bottom:1px solid var(--ink);padding:0 4px 2px;
  font-family:var(--display);font-weight:800;font-size:20px;color:var(--ink);
  transform:rotate(-2deg);transform-origin:left bottom}
.sign .k{font-family:var(--mono);font-size:9px;letter-spacing:.18em;text-transform:uppercase;
  color:var(--faint)}
/* ---------- project diagrams ---------- */
.arch{display:grid;gap:8px}
.arch-row{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,190px),1fr));gap:8px}
.node{border:1px solid var(--line-2);border-radius:var(--r);padding:11px 13px;background:var(--paper)}
.node b{display:block;font-family:var(--display);font-weight:600;font-size:15px;color:var(--ink);
  letter-spacing:-.01em}
.node span{display:block;margin-top:3px;font-size:13.5px;line-height:1.45;color:var(--muted)}
.node.strong{border-color:var(--accent);background:var(--accent-soft)}
.node.guard{border-style:dashed}
.arch .down{text-align:center;font-family:var(--mono);font-size:10.5px;letter-spacing:.12em;
  text-transform:uppercase;color:var(--faint)}
.steps{list-style:none;counter-reset:step;margin-top:16px}
.steps li{counter-increment:step;position:relative;padding:8px 0 8px 36px;color:var(--muted);
  font-size:clamp(15px,3.6vw,16.5px);line-height:var(--rule)}
.steps li::before{content:counter(step);position:absolute;left:0;top:10px;width:24px;height:24px;
  border-radius:999px;border:1px solid var(--accent);color:var(--accent);font-family:var(--mono);
  font-size:12px;line-height:22px;text-align:center}

/* ---------- phones ----------
   Below 16px, iOS Safari zooms the whole page when an input takes focus. */
@media (max-width:719px), (pointer:coarse){
  .search input,.topbar .search input{font-size:16px}
}
/* Fingers, not cursors: every control gets at least a 40px target. The swatches
   keep their size and grow an invisible hit area instead. */
@media (pointer:coarse){
  .back,.copy,.tab,.reset{min-height:40px}
  /* The taller back pill must not make the bar taller, or a full folder scrolls. */
  .topbar .inner{padding-top:7px;padding-bottom:7px}
  #chrome .swatches{gap:12px}
  .sw{position:relative}
  .sw::after{content:"";position:absolute;inset:-12px -6px}
}
/* The page is laid out under the notch and home bar (viewport-fit=cover), so keep
   the edges and the contact row clear of them. */
body{padding-left:env(safe-area-inset-left,0px);padding-right:env(safe-area-inset-right,0px)}
#chrome{padding-bottom:calc(clamp(14px,2.4vh,26px) + env(safe-area-inset-bottom,0px))}
/* A phone with its browser bars showing is short. Tighten the poster so a full
   folder and the contact row still fit one screen: the same rules at every level,
   just less air. */
@media (max-width:719px){
  .contact a{padding:8px 11px;gap:6px}
  #chrome{padding-top:10px}
  #chrome .row{gap:8px}
}
@media (max-width:719px) and (max-height:900px){
  .obj .n{display:none}
  .poster-title .sub{margin-top:6px}
  .search{margin-top:10px}
  .search .count{margin-top:4px;min-height:0}
  .objects,.objects.many{margin-top:8px}
  #hub{padding-top:8px;padding-bottom:6px}
}
/* Below the scatter width the tiles are a grid, and each thumb fills its column:
   sized by aspect ratio and a max-height it came out half the column wide, so the
   label ran past it. */
@media(max-width:849px){
  .obj .thumb{aspect-ratio:auto;width:100%;height:var(--th,clamp(76px,15vh,132px));max-height:none}
}
/* Below the scatter width the tiles are a grid and cannot be dragged, so the reset
   and the drag hint have nothing to act on, and the corner would sit on the swatches. */
@media(max-width:849px){.corner{display:none}}
@media(max-width:559px){
  .f .k,.photo .k,.sign .k{font-size:10px}
  .form-head{font-size:10.5px}
}
"""


def panel(key, label, note=""):
    n = f'<span class="note">{H.escape(note)}</span>' if note else ""
    return (f'<div class="panel"><div class="panel-head"><span class="t">{H.escape(label)}</span>{n}'
            f'<button class="copy" data-copy="{key}">Copy</button></div>'
            f'<pre data-block="{key}"></pre></div>')


def disclosure(key, summary, note=""):
    n = f'<span class="note">{H.escape(note)}</span>' if note else ""
    return (f'<details><summary><span class="arrow">&#9656;</span>{H.escape(summary)}{n}'
            f'<button class="copy" data-copy="{key}">Copy</button></summary>'
            f'<pre data-block="{key}"></pre></details>')


def fig(A, key, caption):
    return f'<div class="fig">{A[key]}<div class="cap">{H.escape(caption)}</div></div>'


# The CV, written as an old application form. Facts come from the CV itself; edit
# them here and rebuild. The PDF beside it is the version to hand over.
CV_PDF = "cv/moheet-subudhi-cv.pdf"

def cv_rec(when, who, where, lines=()):
    li = "".join(f"<li>{x}</li>" for x in lines)
    return (f'<div class="rec"><div class="when">{when}</div><div>'
            f'<div class="who">{who} <span>&middot; {where}</span></div>'
            + (f"<ul>{li}</ul>" if li else "") + "</div></div>")

def cv_field(k, v):
    return f'<div class="f"><span class="k">{k}</span><span class="v">{v}</span></div>'

DL = (f'<div class="cv-dl"><a class="btn primary" href="{CV_PDF}" download>Download the CV</a>'
      f'<span class="note">PDF &middot; January 2026 edition</span></div>')

CV = DL + f"""
<div class="form">
<div class="form-head"><span>Application for employment</span><span>Form CV &middot; 2026</span></div>

<div class="fsec"><h3 class="fh"><b>1.</b> Particulars</h3>
<div class="particulars">
<div class="fgrid">
{cv_field("Name", "Moheet Subudhi")}
{cv_field("Present post", "Product Manager, Business Automation &middot; Mailmodo")}
{cv_field("Email", '<a class="js-mail" href="#">email</a>')}
{cv_field("Phone", '<a href="tel:+919861379000">+91 98613 79000</a>')}
{cv_field("LinkedIn", '<a href="https://www.linkedin.com/in/moheetsubudhi/" target="_blank" rel="noopener">linkedin.com/in/moheetsubudhi</a>')}
{cv_field("Languages", "English (fluent), Hindi, Odia")}
</div>
<div class="photo"><img src="cv/portrait.jpg" alt="Moheet Subudhi" width="350" height="350" loading="lazy">
<span class="k">Photograph</span><span class="rubber">VERIFIED</span></div>
</div></div>

<div class="fsec"><h3 class="fh"><b>2.</b> In brief</h3>
<p>I work on how a business runs: its processes, its compliance and its customers. Since 2020
I have done this across SaaS, government and consulting.</p>
<p>I redesign processes, automate the manual parts, and change systems without adding risk, so
costs come down and customers have a better time. I am at home with data analysis, dashboards
and projects that cut across teams.</p></div>

<div class="fsec"><h3 class="fh"><b>3.</b> Employment record</h3>
{cv_rec("Jul 2026 &ndash; now", "Product Manager, Business Automation", "Mailmodo (YC21), Bangalore")}
{cv_rec("Jan 2024 &ndash; Jun 2026", "Customer Success &amp; Product Operations", "Mailmodo (YC21), Bangalore", [
    "Ran customer success operations for 200+ SaaS accounts worth $27k MRR, and planned how each account would grow.",
    "Doubled MRR on several accounts, month after month, while keeping a 75% customer retention rate.",
    "Set up AI-powered workflows in Vitally to bring quiet customers back: a 4% reply rate and a better NPS.",
    "Drove product adoption and stickiness with targeted rollouts, reaching 98.5% net revenue retention (NRR).",
    "Ran self-serve accounts end to end, with automated touchpoints and success metrics, so support could scale and customers stayed happy.",
    "Built dashboards joining HubSpot, Chargebee and Vitally, so compliance and KPI numbers came from one trusted place.",
    "Designed a shared reporting framework between Customer Success and Onboarding, to track accounts as they moved between the two teams.",
    "Automated the team&rsquo;s daily work with AI-enabled workflows in Pipedream, Slackbots and Google Apps Script."])}
{cv_rec("Oct 2022 &ndash; Jan 2024", "Sales Development Representative", "Mailmodo (YC21), Bangalore", [
    "Ran outbound sales for the US market end to end: LinkedIn, email campaigns, cold calls and website chatbots.",
    "Brought in 10+ qualified leads every month, with 60%+ converting to demos, across SaaS, EdTech and D2C companies.",
    "Used Apollo, Outplay, HubSpot and Walaaxy together to find and qualify prospects.",
    "Reworked the website chatbot funnel so more visitors engaged and replied; chatbot leads grew to over 30% of the outbound pipeline."])}
{cv_rec("Oct 2022 &ndash; Jan 2025", "Independent Consultant, Strategy &amp; Process Optimization", "Bizarc Ventures, Bhubaneswar", [
    "<strong>NeoTeric.</strong> Designed and ran a government PR campaign with a 45-member team, standard SOPs and compliance checks on every outreach step. It reached 2,50,000+ impressions.",
    "<strong>Mahabeer Inventory.</strong> Audited 120+ warehouse transactions a day and built a custom inventory system. Order accuracy went from 82% to 97%, billing compliance risk fell by 90%, and monthly orders tripled.",
    "<strong>OSDA, Government of Odisha.</strong> Directed a &#8377;60-lakh digital transformation, keeping the product in line with the government&rsquo;s compliance goals. Launched a modular CMS, push notifications and analytics dashboards, making the work transparent for 12,000+ users.",
    "<strong>IWD Secretary App.</strong> Built a reporting app for 2,400+ leaders across 60+ clubs. It automated their monthly and yearly compliance reports, made them audit-ready, and every club onboarded (100%).",
    "<strong>Volunteer monitoring.</strong> Built custom modules to track volunteer hours, funds and beneficiaries. Manual effort fell by more than 80%, and the reports became ready for international review.",
    "<strong>Royal Living Tangi.</strong> Ran a data governance project on a base of 34,000+ LPG customers. Led a 7-member team that cleaned 14,500+ records and verified 5,027+ addresses, then replaced the IVRS line with GSM-based outbound calling, projecting a 12&ndash;15% rise in digital LPG bookings.",
    "<strong>Rural outreach under PMUY.</strong> Worked with self-help groups and Mission Shakti groups to get past language barriers, reaching 10,000+ beneficiaries.",
    "Across government, nonprofit and small-business clients: careful diagnosis first, then tighter budgets, automation, and changes made without adding risk."])}
{cv_rec("Feb 2021 &ndash; Oct 2022", "Head of Operations", "Bizarc Ventures, Bhubaneswar", [
    "Managed a &#8377;5-lakh yearly marketing budget across 20+ client campaigns. Cost-benefit analysis on ad spend raised average ROAS by 30% for F&amp;B, retail and hospitality clients.",
    "Built and led a 5-member in-house marketing team serving F&amp;B, e-commerce, personal care, retail, real estate and hospitality brands, from strategy to execution.",
    "Ran data-backed campaigns for acquisition, engagement and retention, improving ROI across digital channels.",
    "Built websites for hospitality clients, giving them direct bookings as a new source of revenue.",
    "Handled 20+ B2B and B2C clients: strategy, campaigns, client communication and performance reviews.",
    "Set up marketing automation and CRM tools so campaigns ran faster and internal work was simpler."])}
{cv_rec("May 2020 &ndash; Feb 2021", "Founder", "V DO Hosting", [
    "Started the company during the COVID-19 pandemic.",
    "Built a working business around video conferencing and virtual meeting platforms.",
    "Handled 500+ events with 60,000+ participants.",
    "Led a team of 10 people who kept it running smoothly."])}
{cv_rec("Feb 2020 &ndash; Apr 2020", "Telesales Representative", "Molson Coors Beverage Company, UK", [
    "Worked in telesales, handling customers alongside 2 area managers.",
    "Pitched the product to about 60 businesses a day and generated leads for the company.",
    "Collected customer data and carried out sales audits."])}
</div>

<div class="fsec"><h3 class="fh"><b>4.</b> Education</h3>
{cv_rec("Jan 2026 &ndash; Apr 2027", "Advanced Management Programme in Business Analytics", "Indian School of Business, Hyderabad")}
{cv_rec("Sep 2018 &ndash; May 2021", "BSc Accounting and Finance, Class II Upper Division", "City St George&rsquo;s, University of London")}
{cv_rec("Sep 2017 &ndash; Jun 2018", "International Foundation Programme, 86.86%", "INTO City University London")}
</div>

<div class="fsec"><h3 class="fh"><b>5.</b> Skills &amp; tools</h3>
<div class="fgrid">
{cv_field("Product &amp; growth", "GTM strategy, funnel optimization, customer lifecycle management")}
{cv_field("Process", "BPM, workflow re-engineering, SOP design")}
{cv_field("Ops &amp; analytics", "HubSpot, Chargebee, Vitally, Google Sheets (advanced), reporting automation, Apps Script")}
{cv_field("Tools", "Excel (advanced), Google Sheets automation, Pipedream, Zapier, Postman, Amplitude, AI and automation workflows")}
{cv_field("Compliance &amp; risk", "Audit tracking, KPI reporting, data governance")}
{cv_field("Team", "Hiring, goal setting, cross-functional collaboration")}
{cv_field("Soft skills", "Communication, teamwork, analytical thinking, fast learner")}
{cv_field("Code", "Python, SQL")}
</div></div>

<div class="fsec"><h3 class="fh"><b>6.</b> Volunteering &amp; leadership</h3>
{cv_rec("2017", "Led a team of 7 photographers documenting the event", "SICC Convention")}
{cv_rec("2016", "One of a 10-member cultural team running the annual college fest", "SAI UNWIND")}
{cv_rec("2014 &ndash; 15", "Core member, organising charitable initiatives", "Interact Club")}
</div>

<div class="fsec"><h3 class="fh"><b>7.</b> Declaration</h3>
<div class="sign"><p>The particulars above are true.</p>
<div><div class="line">Moheet Subudhi</div><span class="k">Signature of applicant</span></div></div>
</div>
</div>
""" + DL


def views(A, c):
    """Each entry: slug, poster label, thumbnail art key or glyph, title, lede, body."""
    tabs = "".join(
        f'<button class="tab" role="tab" data-soul="{i}" aria-selected="{"true" if i == 0 else "false"}">'
        f'{H.escape(s["name"])}</button>' for i, s in enumerate(c["souls"]))

    v = []
    v.append(dict(
        slug="generator", label="The Setup Interview", art=None, glyph="?",
        title="The Setup Interview",
        lede="One prompt. It asks you questions for five minutes, then writes four files "
             "for your actual job.",
        body=f"""
<p>It asks what you do, what you redo every week and resent, how you do it now, and what keeps
going wrong. Then it writes: how it should behave, how it should work, what it can reach, and
how you do that one task.</p>
<p>Paste it as the first message in any chat. Claude, ChatGPT, Gemini, Copilot. It works in a
terminal agent too, and on a phone.</p>
{panel("generator", "The Setup Interview", "about 5 minutes")}
<p><strong>The third question is the one people rush.</strong> Walk it through how you actually
do the thing, fiddly parts included. The skill it writes is only as good as that answer.</p>"""))

    v.append(dict(
        slug="soul", label="Five soul files", art="harness", glyph=None,
        title="Five soul files",
        lede="Who the AI is when it works with you: its standards, its voice, what it never "
             "does.",
        body=f"""
<p>Same model, different colleague. Pick the closest to your job, then change two lines so it
sounds like you. That is the whole setup.</p>
<div class="tabs" role="tablist">{tabs}</div>
<div class="panel"><div class="panel-head"><span class="t" id="soul-name"></span>
<button class="copy" data-copy="soul">Copy</button></div>
<pre data-block="soul"></pre></div>
<p>Where it goes: ChatGPT Custom Instructions or a Project, Gemini Gems, a Claude Project,
Copilot custom instructions, or <code>AGENTS.md</code> in a project folder.</p>
{fig(A, "harness", "The harness is everything around the model")}"""))

    v.append(dict(
        slug="loop", label="The loop checklist", art="loop", glyph=None,
        title="Make it finish instead of wander",
        lede="Four lines above any task: the goal, the check, the stop, the limit.",
        body=f"""
<p><strong>The check is the one people skip and the one that matters.</strong> "I will review it
carefully" is not a check. "Both totals match the source file" is, because it can fail.</p>
{fig(A, "loop", "Do a step, check it, decide whether to go again")}
<div class="split">
{panel("loopChat", "For a chat", "paste above your task")}
{panel("loopFile", "For a project folder", "goes in AGENTS.md")}
</div>
<p>Without a stop rule, a model will try variations of the same broken idea until you interrupt
it. With one, it comes back after two.</p>"""))

    v.append(dict(
        slug="tools", label="The tool registry", art="mcp", glyph=None,
        title="Stop it guessing and overstepping",
        lede="Which tool for which question, and what it may do without asking you.",
        body=f"""
<p>Once an agent has more than about three tools, it starts guessing. It searches the web for
something sitting in your own files, or proposes a plan built on access it does not have.</p>
<p>Pasted into a plain chat with no tools at all, this tells the model what access <em>you</em>
have, so it stops suggesting things you cannot do and starts asking for what it needs.</p>
<p><strong>The second half is the limits.</strong> A connector runs as you, so it can send, edit
and delete. Write down what it may only read, what it must bring to you first (that is
<em>human in the loop</em>), and what it must never touch. A written rule guides it; for risky
actions, also set the tool itself to ask before it acts. It drafts, you press send.</p>
<p><strong>It keeps itself current.</strong> The template's last section has the agent update the
file after every task that used a tool: new tools get a line, wrong picks get fixed, broken ones
get parked with a date. It may never change its own limits unless you tell it to. In a chat
window it cannot save files, so it shows you the lines to change.</p>
{disclosure("regChat", "If you have no tools connected", "start here")}
{disclosure("regTemplate", "The blank template")}
{disclosure("regExample", "A filled example, someone in data")}
{fig(A, "mcp", "One standard, so each tool needs no integration of its own")}
<p><strong>Where the tools come from:</strong> the connector list built into Claude and ChatGPT
first, then the app maker's own, <a href="https://composio.dev" target="_blank" rel="noopener">Composio</a> for many apps behind
one login, <a href="https://mcp.so" target="_blank" rel="noopener">mcp.so</a> for everything else, or ask your agent to build one
around your own system.</p>
<p><strong>Before you connect anything:</strong> who wrote it, what access is it asking for, when
was it last updated, and would you be fine if it could see everything you point it at.</p>"""))

    v.append(dict(
        slug="memory", label="Second Brain", art="memory", glyph=None,
        title="Second Brain",
        lede="A memory that outlives the conversation, so you stop re-explaining yourself "
             "every Monday.",
        body=f"""
<p>Context is what it can see right now. It fills up, and things fall out. Memory is what
survives the conversation ending, and it is the whole difference between a tool you operate
and a colleague who already knows the background.</p>
<p class="rule">Once is a correction. Twice is a missing line in a file.</p>
<p>Correcting it in the moment costs nothing and teaches it nothing. The second time the same
thing happens, write the line down. Some tools now save your corrections for you. Go and read
what they saved, because they get it wrong sometimes.</p>
<table><thead><tr><th>Tool</th><th>Where to look</th></tr></thead><tbody>
<tr><td>Claude Code</td><td>Type <code>/memory</code>. On by default.</td></tr>
<tr><td>ChatGPT</td><td>Settings, Personalization, Memory. Separate from Custom Instructions.</td></tr>
<tr><td>Claude</td><td>Settings, Memory. A separate memory per Project.</td></tr>
<tr><td>Gemini</td><td>Settings, Personal context, Memory.</td></tr>
<tr><td>Cursor, Copilot, Codex</td><td>Nothing is saved for you. Write it in <code>AGENTS.md</code> yourself.</td></tr>
</tbody></table>
{fig(A, "memory", "Context is this conversation. Memory is every conversation.")}
<p>Worth saying plainly: <strong>it does not get smarter.</strong> The model is fixed. What
changes is how much it knows about you and your work, and that is worth a lot on its own.</p>
<div class="panel"><div class="panel-head"><span class="t">Built on exactly this</span></div>
<div style="padding:16px 15px">
<p style="margin:0">Every tool above keeps its own memory, in its own format, locked to itself.
Correct something in one and the others never hear about it. <strong>Ownr</strong> is the
version of this I am building: one memory, shared across every assistant you use.</p>
<p style="margin-top:12px"><a href="https://ownr.digital" target="_blank" rel="noopener">
ownr.digital &rarr;</a></p>
</div></div>"""))

    v.append(dict(
        slug="skills", label="Business Analytics Skills", art="skill", glyph=None,
        title="Business Analytics Skills",
        # Same PIN as the slides. A right answer opens the page here instead of leaving.
        lock=dict(unlock="open", hint="Four digits. Ask me for it."),
        lede="Thirty-six skills across machine learning, statistics, optimisation, pricing, "
             "decision analysis, data engineering and recommenders.",
        body=f"""
<p>Each one asks what the work is for, follows a real method, checks its own logic, and hands
back a decision rather than a number. MIT licensed, yours to change.</p>
<p>They install as seven toolkits from a marketplace, or as plain folders in any tool that
reads the open Agent Skills format. The repository is
<code>moheetsubudhi-isb/business-analytics-skills</code>.</p>
<div class="split">
{panel("installClaude", "Claude Code")}
{panel("installCodex", "Codex")}
</div>
<p>Any other tool, or several at once:</p>
{panel("installCli", "Cursor, Copilot, Gemini CLI and more")}
{fig(A, "skill", "A skill is one task, written down once")}
<p>Browse them first at <a href="{REPO}">the repository</a>.</p>"""))

    v.append(dict(
        slug="local", label="Run it on your laptop", art="context", glyph=None,
        title="Open models, and running one yourself",
        lede="The weights are published, so you can download the model and run it on your "
             "own machine. No account, no API, no data leaving the building.",
        body="""
<h3>What &ldquo;open&rdquo; actually means here</h3>
<p>A model is a very large file of numbers, the weights. With GPT-5 or Claude those numbers
stay on the company&rsquo;s servers and you rent access through an API. With an open model the
company publishes the file. You download it and run it, and nobody can switch it off, meter
it, or see what you asked.</p>
<p><strong>Open weights is not the same as open source.</strong> Almost all of these publish the
weights under their own licence while keeping the training data and code private. Most allow
commercial use; a few restrict it above a size of business. If you are shipping something
commercial, read the licence rather than assuming.</p>

<h3>Why it is worth knowing</h3>
<ul>
<li><strong>Nothing leaves.</strong> The obvious one, and the only answer that satisfies a
compliance team without a procurement cycle.</li>
<li><strong>No per-token cost.</strong> The work is free once the file is on disk, so you can
run it over ten thousand rows without watching a meter.</li>
<li><strong>It cannot be deprecated.</strong> A model you have downloaded behaves the same next
year. Hosted models change underneath you.</li>
<li><strong>It works offline.</strong> Genuinely: turn the wifi off and it still answers.</li>
</ul>

<h3>The families worth knowing</h3>
<table><thead><tr><th>Family</th><th>From</th><th>Worth it for</th></tr></thead><tbody>
<tr><td><a href="https://www.llama.com" target="_blank" rel="noopener">Llama</a></td><td>Meta</td><td>The default all-rounder. The small ones are fast and good enough for most everyday work.</td></tr>
<tr><td><a href="https://qwen.ai" target="_blank" rel="noopener">Qwen</a></td><td>Alibaba</td><td>Strongest small models right now, and the best multilingual coverage.</td></tr>
<tr><td><a href="https://ai.google.dev/gemma" target="_blank" rel="noopener">Gemma</a></td><td>Google</td><td>Small, efficient, well-behaved. Good on a modest laptop.</td></tr>
<tr><td><a href="https://mistral.ai" target="_blank" rel="noopener">Mistral</a></td><td>Mistral AI</td><td>European, permissive licensing, strong at its size.</td></tr>
<tr><td>Phi</td><td>Microsoft</td><td>Punches far above its weight at reasoning and code for how small it is.</td></tr>
<tr><td><a href="https://www.deepseek.com" target="_blank" rel="noopener">DeepSeek</a></td><td>DeepSeek</td><td>Reasoning models at a fraction of the usual size.</td></tr>
<tr><td><a href="https://huggingface.co/openai" target="_blank" rel="noopener">gpt-oss</a></td><td>OpenAI</td><td>OpenAI&rsquo;s open-weight release. The 20B is the largest thing that fits in plain 16&nbsp;GB.</td></tr>
</tbody></table>
<p>Everything published lives on <a href="https://huggingface.co/models" target="_blank" rel="noopener">Hugging Face</a>, which is where these actually get released. It is worth half an hour of browsing.</p>

<h3>Three ways to run one</h3>
<table><thead><tr><th>Tool</th><th>Suits</th></tr></thead><tbody>
<tr><td><a href="https://ollama.com" target="_blank" rel="noopener">Ollama</a></td><td>One command, a desktop window if you want one, and it plugs into coding agents. Start here.</td></tr>
<tr><td><a href="https://lmstudio.ai" target="_blank" rel="noopener">LM Studio</a></td><td>A proper app with a model browser. Best if you would rather never see a terminal.</td></tr>
<tr><td><a href="https://jan.ai" target="_blank" rel="noopener">Jan</a></td><td>Open source, offline by default, looks like a normal chat app.</td></tr>
</tbody></table>

<h3>Which size fits your machine</h3>
<p>Match the model to your memory first, then worry about which one. The download size is
roughly what it needs in RAM while running, and you need headroom for everything else open.</p>
<table><thead><tr><th>You have</th><th>Run</th></tr></thead><tbody>
<tr><td>4 GB</td><td>A 1&ndash;2B model. Summarising, extraction, tidying text.</td></tr>
<tr><td>8 GB</td><td>A 3&ndash;4B model, around 2&ndash;2.5 GB on disk. The everyday sweet spot.</td></tr>
<tr><td>16 GB</td><td>A 7&ndash;8B model. Good enough for most daily work.</td></tr>
<tr><td>16 GB and patient</td><td>gpt-oss 20B, about 14 GB. Slow, but it runs with no graphics card.</td></tr>
</tbody></table>
<p>Start with the smallest one that could work:</p>
{panel("ollama", "Your first model", "1.4 GB download")}
<p>If it will not load you will see <code>model requires more system memory than is
available</code>. It checks free memory, not installed, so closing a browser with forty tabs
genuinely fixes it. In any model picker, avoid anything with <code>:cloud</code> in the name,
which runs on someone else&rsquo;s servers and defeats the point.</p>

<h3>Be honest about what it cannot do</h3>
<p>A small local model is meaningfully worse than a frontier model at hard, multi-step
reasoning. It is entirely good enough for pulling fields out of messy text, summarising,
classifying, redacting, and first drafts you were going to rewrite anyway.</p>
<p class="rule">The local model filters. The cloud model finishes.</p>
<p>Run the local one over anything sensitive, strip what matters, send only the remainder to
the better model. Most of your data never leaves, and you still get a frontier answer where it
counts. That is the pattern worth stealing, and the one that gets signed off.</p>"""))

    # Every project page has the same four parts, so they read as a set. A part with
    # nothing true to say is left out rather than filled.
    def project(problem, did, result, tools="", links="", extra=""):
        out = f"<h3>The problem</h3>\n<p>{problem}</p>\n<h3>What I did</h3>\n{did}\n{extra}"
        if result is not None:
            body = result if result.lstrip().startswith("<") else f"<p>{result}</p>"
            out += f"<h3>What came of it</h3>\n{body}\n"
        if tools:
            out += f"<h3>Tools</h3>\n<p>{tools}</p>\n"
        return out + (f"<p>{links}</p>" if links else "")

    v.append(dict(
        slug="projects", label="My projects", art=None, icon="projects",
        title="Things I have built",
        lede="Mine, and for clients.",
        children=[
            dict(slug="ishaan", label="Ishaan", icon="robot",
                 stamp=dict(icon="robot", text="MAILMODO"),
                 title="Ishaan, an ops agent",
                 lede="An always-on teammate in Slack that runs customer success ops at Mailmodo, and checks its own work.",
                 body=project(
                     "Customer success work at Mailmodo spans many systems: account health, "
                     "billing, the product knowledge base, Slack. Much of it is routine and daily, "
                     "and it has to be right every time, because some of it reaches customers.",
                     "<p>I built Ishaan: two agents sharing one brain. Claude Code is the one I "
                     "work with directly. Hermes runs always on as Ishaan in Slack, where the team "
                     "asks it questions and where it posts its scheduled work.</p>",
                     """<p><strong>Routine customer-success work now runs on its own, and the system repairs itself when something breaks.</strong></p>
<ul>
<li><strong>19 jobs run on a schedule</strong> with nobody at a keyboard: a morning health check, a daily summary of the customer inbox, a daily summary of unpaid invoices, a twice-daily refresh of what the team knows about each customer, and a weekly refresh of product knowledge.</li>
<li><strong>The team asks Ishaan in Slack</strong> and gets answers drawn from that same customer and product knowledge.</li>
<li><strong>The daily digest went from 3,487 words to about 195</strong>, so it can be read at a glance.</li>
<li><strong>Breakages are caught and fixed.</strong> A watchdog restarts it within seconds, and every 30 minutes each tool connection is tested again. Tool connection errors fell from 18.9 an hour to zero.</li>
<li><strong>It keeps improving.</strong> It has run since July 2026, and every Monday it reviews its own week and proposes new checks for me to approve.</li>
</ul>""",
                     "Hermes Agent, Claude Code, MCP, Python, Slack Block Kit, Supabase vector "
                     "search, Composio, SQLite, launchd, git",
                     extra="""
<h3>How it is built</h3>
<div class="fig"><div class="arch">
<div class="arch-row"><div class="node"><b>The team</b><span>asks Ishaan in Slack</span></div><div class="node"><b>Me</b><span>works in Claude Code</span></div></div>
<div class="down">&darr;</div>
<div class="arch-row"><div class="node strong"><b>Ishaan</b><span>Hermes, always on. 19 scheduled jobs, 13 plugins.</span></div><div class="node strong"><b>Claude Code</b><span>Interactive, for the work I do by hand.</span></div></div>
<div class="down">&darr; both read and write &darr;</div>
<div class="arch-row"><div class="node"><b>One brain</b><span>Customer and product pages, a knowledge graph, and a vector knowledge base of the help centre.</span></div><div class="node"><b>Shared memory</b><span>Decisions and context that carry across sessions and machines, through Ownr.</span></div><div class="node"><b>Tools over MCP</b><span>Customer success, billing, CRM, analytics, Slack and email.</span></div></div>
<div class="down">&darr; watched by &darr;</div>
<div class="arch-row"><div class="node guard"><b>The guard</b><span>A watchdog restarts it within 5 seconds. Self-heal re-tests every tool every 30 minutes. Invariant checks run each morning. Every real tool call is recorded, and a drift detector flags when the system doc stops matching the machine.</span></div></div>
</div><div class="cap">Two agents, one brain, and a guard that watches both</div></div>

<h3>The loop that keeps it honest</h3>
<p>Restarting what breaks is self-healing. Learning what to watch is the harder part. Every
Monday Ishaan reviews its own week and asks one question: what happened that none of the
existing checks would have caught?</p>
<ol class="steps">
<li>A script gathers the evidence with no AI at all: tool-call outcomes, job status, new error types, what changed in git. The cost is fixed however bad the week was.</li>
<li>The model reads it and proposes at most three new checks.</li>
<li>I approve or reject each one. Nothing applies itself.</li>
<li>An approved check goes in with a git snapshot, a syntax check and a full run of the guard, and is reverted automatically if anything breaks.</li>
</ol>
<p>Its first run caught a bug in its own proposals: all three described a time window but
checked the whole log, so they would have stayed red forever. They were rejected, and that
rule is now enforced at the moment a check is proposed.</p>

<h3>What it taught me</h3>
<ul>
<li><strong>A check that passes is not a check that works.</strong> Every incident had a check that ran green while watching the wrong layer: a server that connected while every tool call on it failed, a restart that quietly did nothing in 1,900+ runs. Now the outcome of every real call is recorded, and idle never counts as healthy.</li>
<li><strong>Write decisions down where the next reader looks.</strong> A cost decision lived in one agent&rsquo;s memory only, so the next session re-derived it and called it a bug. Decisions now go into the shared memory and the system doc.</li>
<li><strong>Your own instructions are untrusted input.</strong> The agent&rsquo;s safety scanner blocked its own rulebook twice: once for a warning that quoted the command it warned against, once for a rule that read like hiding something. Rules now say what to do, not what to hide, and are scanned when they are edited.</li>
<li><strong>Measure before you optimise.</strong> A token-saving proxy made Ishaan about four times more expensive per conversation, because it broke prompt caching for that kind of traffic. It stays off, on purpose.</li>
</ul>
""")),
            dict(slug="self-serve", label="Self-serve strategy", icon="analytics",
                 stamp=dict(img="logos/mailmodo.png", logo=True, text="MAILMODO"),
                 title="Self-serve strategy",
                 lede="Mailmodo has a lot of small customers who run on their own. I worked out which ones to help, and how.",
                 body=project(
                     "Mailmodo is email software: businesses use it to send emails to their own "
                     "customers. Most of Mailmodo&rsquo;s customers are small and use it without "
                     "anyone from our team looking after them. That is called <strong>self-serve</strong>. "
                     "A support team cannot talk to everyone, so it has to choose who to spend time on.</p>\n<p>"
                     "We were choosing badly. The groups we used described what <em>we</em> had "
                     "decided, not what the customer was doing: &ldquo;we decided they don&rsquo;t need "
                     "help&rdquo;, &ldquo;they chose to be self-serve&rdquo;, &ldquo;they ghosted "
                     "us&rdquo;. Nothing in them told us who was about to leave and who was ready to "
                     "spend more, so the same message went to everyone, it worked for no one, and more "
                     "customers were leaving.",
                     "<p>I redesigned it. Every self-serve customer is now placed in one of four groups "
                     "by how they actually use the product, and each group has its own plan: what to "
                     "do, how often, and who does it. Placement is automatic, from usage data that "
                     "refreshes every day, so nobody sorts customers by hand.</p>\n"
                     "<p>The goal was simple: keep more of these customers, help the ones who can "
                     "grow, and stop spending the team&rsquo;s time on accounts that don&rsquo;t need it.</p>",
                     None,
                     "Vitally (customer data), Amplitude (usage data), Chargebee (billing), HubSpot, "
                     "Google Sheets and Apps Script",
                     extra="""
<h3>Two email terms, in plain words</h3>
<ul>
<li><strong>Bulk email.</strong> One message sent to a whole list at once, like a newsletter or a sale announcement.</li>
<li><strong>Automatic email.</strong> Emails that go out by themselves when something happens, like a welcome message after someone signs up, or a reminder after an abandoned basket. Mailmodo calls these journeys and trigger campaigns.</li>
</ul>
<p>Almost everything in the strategy comes back to one question: does this customer only blast
emails by hand, or have they set up emails that work for them?</p>

<h3>The four groups</h3>
<div class="fig"><div class="arch">
<div class="arch-row"><div class="node strong"><b>Auto Pilot</b><span>Already good at it. Sends steadily, gets good results, and asks for help only when something breaks. <em>Light-touch care: regular check-ins and product updates.</em></span></div><div class="node"><b>Needs a nudge</b><span>Uses it, but results are weak or patchy. Wants ideas and a little help. <em>We coach them toward Auto Pilot.</em></span></div></div>
<div class="arch-row"><div class="node"><b>Stable, not growing</b><span>Joined for one job, and it is done. Little time and no appetite for more. <em>Light, automatic contact, and make sure payment is on autopay.</em></span></div><div class="node guard"><b>Gone quiet</b><span>Nothing sent for 30 days or more, though they still pay. <em>We find a use that makes the product stick.</em></span></div></div>
</div><div class="cap">Four groups, sorted by behaviour</div></div>
<p>The group names are Mailmodo&rsquo;s own: Auto Pilot, Non-Auto Pilot, No Growth Opportunity and
Dormant.</p>

<h3>How we decide who is on Auto Pilot</h3>
<p>Auto Pilot is the group everything else is measured against, so the test has to be strict and
steady. My first version looked at one month, and customers kept flipping in and out. The
version that works asks for <strong>three months in a row</strong>. Each month the customer must have:</p>
<ul>
<li>had at least 1 in 10 emails opened, and 2 in 100 clicked;</li>
<li>sent at least 5 bulk emails;</li>
<li>used automatic emails, in a journey that month or a trigger campaign at some point in the three;</li>
<li>used at least 100 email credits (the unit of sending in their plan).</li>
</ul>
<p>Miss any one month and the customer drops out. Customers who use it but do not pass go to the
&ldquo;needs a nudge&rdquo; group, and every group has a written rule for moving in and out, marked
automatic or needs a person.</p>

<h3>How it runs day to day</h3>
<ol class="steps">
<li>Usage data arrives every day: emails sent, opens, clicks, credits used, automatic emails running.</li>
<li>It is combined with account data: who the customer is, their invoices, their onboarding stage and who looks after them.</li>
<li>The rules place each customer in a group and move them when their behaviour changes.</li>
<li>The group sets the plan. For example, an Auto Pilot customer gets a check-in every three months. A support message from them is marked high priority. A customer whose results slip gets a goal, a playbook, and a return to Auto Pilot once they reach it.</li>
</ol>

<h3>What came of it</h3>
<p><strong>Mailmodo&rsquo;s small customers now get the help that suits them, and the team&rsquo;s time goes where it counts.</strong></p>
<ul>
<li><strong>The team knows who to call and why.</strong> Time goes to customers who are slipping or ready to grow, and the steady ones get light, automatic care.</li>
<li><strong>Churn gets an early warning.</strong> If a customer&rsquo;s last 30 days make up less than a quarter of their last 90 days of activity, their activity has fallen off, and they move to a group that gets help before they leave.</li>
<li><strong>A clear way to grow revenue.</strong> The data showed that customers who use automatic emails have higher open and click rates and send much more. The plan is to move the others across, and see whether it helps them as much.</li>
<li><strong>Every customer gets a message that fits</strong>, instead of the same one as everybody else.</li>
</ul>
<p>It is live and running. How much it has reduced the number of customers leaving is still being measured, and I will add the figure here.</p>

<h3>What the data showed</h3>
<p>The first look at 88 customers on Auto Pilot found the biggest opportunity in the whole group:</p>
<ul>
<li><strong>Most only send by hand.</strong> 36 of the 88 (41%) send bulk email and nothing else, and 57% had no automatic emails running in the past month.</li>
<li><strong>Automatic emails go with better results.</strong> Customers using them average about 35% opened and 10% clicked. Five who used only trigger emails reached 46% opened and 27% clicked. Whether automation causes this, or just marks the more skilled customers, is still to be tested.</li>
<li><strong>They also use the product more.</strong> Customers using bulk, trigger and journey emails together used about 75% more of their sending allowance (17.6k credits in 30 days) than bulk-only customers. That is where growth in revenue comes from.</li>
</ul>

<h3>What I learned</h3>
<ul>
<li><strong>Group people by what they do, not by what you decided.</strong> &ldquo;We decided they don&rsquo;t need help&rdquo; says nothing about the customer.</li>
<li><strong>One month misleads.</strong> A rule on a single month moves customers around for no reason. Three in a row holds.</li>
<li><strong>Write the way out as carefully as the way in.</strong> Every group says how a customer leaves it and whether a system or a person makes the call.</li>
<li><strong>The data pipe is half the job.</strong> The groups only work when the right numbers arrive every day, next to the customer details.</li>
</ul>
"""
                 )),
            dict(slug="outreach", label="Outreach Console", icon="send",
                 stamp=dict(img="logos/mailmodo.png", logo=True, text="MAILMODO"),
                 title="Outreach Console",
                 lede="Cold outbound for Mailmodo, from strategy to reply, with the expensive mistakes made impossible.",
                 body=project(
                     "Cold email is easy to start and easy to wreck. One careless run can burn a "
                     "sending domain, mail someone twice, mail someone who opted out, or send "
                     "made-up details about a prospect. And cold contacts must never leak into "
                     "Mailmodo itself, which is opt-in only.",
                     "<p>I built an internal web app at Mailmodo where one person runs a whole "
                     "campaign: who to target, a verified list from Apollo or a CSV, the copy, a "
                     "personal opener for each lead, a paced multi-touch sequence, reply triage, "
                     "and handing anyone who opts in over to Mailmodo nurture. AI drafts the "
                     "strategy, the copy and the openers. The rules decide what is sent.</p>\n"
                     "<p>The same motion also runs from the terminal as an SDR agent on Hermes and "
                     "Claude Code, following 27 playbooks across 8 stages.</p>",
                     """<p><strong>One person can run a whole cold-email campaign from a single screen, and the mistakes that cost the most cannot happen.</strong></p>
<ul>
<li><strong>The costly mistakes are blocked in code:</strong> nobody is emailed twice, nobody who opted out or replied is chased, no mailbox sends before it has warmed up for 14 days, no more than 100 a day per mailbox, and nothing goes live until the exact words CONFIRM SEND are typed.</li>
<li><strong>Follow-ups go out on the right day by themselves</strong>, once the operator switches that on.</li>
<li><strong>Only people who say yes reach Mailmodo.</strong> Cold contacts never do.</li>
<li><strong>Tested hard:</strong> 478 tests pass on file storage and 472 on Postgres, with the live-send path tested against a fake mail server. It has been handed to the tech team for hosting.</li>
<li><strong>Not used for a live send yet.</strong> That waits on a mailbox that has finished its 14-day warm-up.</li>
</ul>""",
                     "Node 22 with four dependencies, Postgres, SMTP and IMAP, Apollo, Claude, "
                     "OpenAI or OpenRouter (pluggable), Docker, Hermes, Claude Code",
                     extra="""
<h3>How it is built</h3>
<div class="fig"><div class="arch">
<div class="arch-row"><div class="node"><b>The console</b><span>One operator, one screen, the whole campaign.</span></div><div class="node"><b>The SDR agent</b><span>The same motion from the terminal, on Hermes and Claude Code.</span></div></div>
<div class="down">&darr; same rules &darr;</div>
<div class="arch-row"><div class="node strong"><b>Strategy &rarr; list &rarr; copy</b><span>Who to target, verified contacts, AI-drafted copy and openers.</span></div><div class="node strong"><b>Pre-flight &rarr; send</b><span>Every email checked, then sent 2 to 8 minutes apart, inside the recipient&rsquo;s working hours.</span></div><div class="node strong"><b>Replies &rarr; nurture</b><span>Each mailbox read over IMAP, every reply routed, opt-ins handed to Mailmodo.</span></div></div>
<div class="down">&darr; stored in &darr;</div>
<div class="arch-row"><div class="node"><b>Postgres, 20 tables</b><span>A send ledger, an atomic daily cap and a run lock, so two runs can never overlap.</span></div><div class="node guard"><b>Autopilot</b><span>Sends follow-ups on their day once armed. Change the copy, the list or the mailbox and it switches itself off.</span></div></div>
</div><div class="cap">Two ways in, one set of rules</div></div>

<h3>Rules written into the code</h3>
<p>Not guidelines. Each one is enforced in code, and a change that weakens one is treated as
a bug.</p>
<ul>
<li><strong>No invented contact data.</strong> A field that cannot be verified stays blank.</li>
<li><strong>Cold and opt-in never mix.</strong> Only someone who replied positively reaches Mailmodo.</li>
<li><strong>A mailbox warms for 14 days</strong> before it sends anything cold.</li>
<li><strong>At most 100 emails per mailbox per day</strong>, claimed before every send, across all campaigns.</li>
<li><strong>Dry run by default.</strong> Live sending needs the words <code>CONFIRM SEND</code>, typed.</li>
<li><strong>Nobody gets the same step twice</strong>, even after a crash, and nobody who replied gets a follow-up.</li>
</ul>

<h3>What it taught me</h3>
<ul>
<li><strong>Make the expensive mistakes impossible, not discouraged.</strong> A warning gets clicked past. A rule in code does not.</li>
<li><strong>Test the crash, not just the happy path.</strong> The worst bug found was a crash after every first email that would have mailed people again on restart. A ledger written right after each send now closes it.</li>
<li><strong>Agents arrive with no context, so the repo has to explain itself.</strong> Every kind of file has one home, every folder has a README, and the rules live in one document that binds people and agents alike.</li>
</ul>
""")),
            dict(slug="leaderboard", label="AI model leaderboard", icon="ranking",
                 stamp=dict(img="logos/besthunt.svg", logo=True, text="BESTHUNT"),
                 title="BestHunt AI model leaderboard",
                 lede="Every AI model, ranked by what it costs to do real work.",
                 body=project(
                     "AI model leaderboards are written for developers: dollars per million tokens, "
                     "context windows, quantization. besthunt.ai serves marketing, sales and ops "
                     "teams, who want to know which model does their job well for the least "
                     "money, and its promise is no pay-to-rank.",
                     "<p>I built the leaderboard at Mailmodo for besthunt.ai: a data pipeline and a "
                     "static site. The pipeline pulls every model&rsquo;s price, hosts and benchmark "
                     "scores from one public source, works out which models are the best value at "
                     "their quality, and turns token maths into jobs a team recognises.</p>",
                     """<p><strong>Someone choosing an AI model for marketing or operations can see which one is the best value for their job, in plain money terms.</strong></p>
<ul>
<li><strong>It tracks 400+ priced models</strong> and ranks about 150 on quality, with a price worked out for six everyday jobs, like writing 1,000 marketing emails.</li>
<li><strong>The headline finding:</strong> 150 of 157 models cost more than an equally capable alternative. Most people are paying more than they need to.</li>
<li><strong>It can be trusted.</strong> It refreshes every Monday and checks its own data first, so a bad update cannot go live. Every change is published in a changelog with an RSS feed, and the whole dataset is a free download.</li>
</ul>""",
                     "Python, Next.js (static export), the OpenRouter API, launchd, Vercel, GitHub",
                     '<a class="btn primary" href="https://besthunt-leaderboard.vercel.app" '
                     'target="_blank" rel="noopener">See it live</a>',
                     extra="""
<h3>How it is built</h3>
<div class="fig"><div class="arch">
<div class="arch-row"><div class="node"><b>One public source</b><span>OpenRouter: every model&rsquo;s catalogue entry, per-host prices and uptime, and two benchmark families. No API keys.</span></div></div>
<div class="down">&darr; every Monday &darr;</div>
<div class="arch-row"><div class="node strong"><b>Build</b><span>Pull, enrich per host, and find the best-value models at each quality level.</span></div><div class="node strong"><b>Gate</b><span>Twelve checks against the live data. A failure restores yesterday&rsquo;s files.</span></div><div class="node strong"><b>Publish</b><span>Snapshot, changelog, RSS, and CSV and JSON downloads.</span></div></div>
<div class="down">&darr; becomes &darr;</div>
<div class="arch-row"><div class="node"><b>A static site</b><span>The ranking, a page per model, the best model for each use case, findings, a changelog, the dataset and an embed.</span></div></div>
</div><div class="cap">One source in, one checked dataset out</div></div>

<h3>The translation layer</h3>
<p>The data is the same as any developer leaderboard. The product is what it says to
someone who does not think in tokens.</p>
<ul>
<li><code>$0.15 / 1M input tokens</code> becomes <strong>$0.23 to write 1,000 marketing emails</strong>.</li>
<li><code>context 1,048,576 tokens</code> becomes <strong>reads about 1,500 pages at once</strong>.</li>
<li><code>on_frontier</code> becomes <strong>best value at this quality</strong>.</li>
<li><code>overpay 117&times;</code> becomes <strong>you are paying 117&times; more than you need to</strong>.</li>
<li><code>tools: true</code> becomes <strong>can connect to your CRM and other tools</strong>.</li>
</ul>

<h3>Nothing goes live unchecked</h3>
<p>New data is compared against what is live before anything is archived. It never drops
below 150 models, never has a duplicate, never has an unpriced row, cannot shrink by more than
a quarter, and the median price cannot jump more than five times. Any failure stops the run
and puts the previous files back. Twelve tests prove each check rejects what it claims to.</p>

<h3>What it taught me</h3>
<ul>
<li><strong>Never let an optional field decide who is in.</strong> The ranking once required a quality score. When benchmark coverage in the feed fell from 153 models to 56 in two days, the changelog announced 102 withdrawals, and 101 of them were still on sale. Now price alone decides, a missing score shows as a dash, and a change is reported only when the field exists on both dates.</li>
<li><strong>One source beats three.</strong> Matching the same model named three different ways is the most expensive part of a build like this. One source that already carries prices, hosts and benchmarks under one id removes it.</li>
<li><strong>A laptop can keep a schedule.</strong> Not with cron, which skips a job the machine slept through, but with launchd, which runs it the moment the lid opens.</li>
</ul>
""")),
            dict(slug="lpg-guru", label="LPG Guru", icon="gas",
                 stamp=dict(img="logos/lpgguru.png", logo=True, text="LPG GURU"),
                 title="LPG Guru",
                 lede="One platform to run an LPG gas agency, with an AI assistant on top.",
                 body=project(
                     "An HPCL distributor runs a regulated, high-volume business on tools that do "
                     "not talk to each other. Booking data sits in HPCL&rsquo;s portals; cash, stock, "
                     "credit and staff sit in registers, Excel, Tally and WhatsApp. Reconciliation "
                     "is done by hand every day, compliance is chased from lists, calls outside "
                     "counter hours go unlogged, and answers live with the owner. The owner ends "
                     "up being the integration layer.",
                     "<p>At Solarc Ventures we built LPG Guru, a vertical SaaS ERP made only for "
                     "HPCL LPG distributors. Twelve modules run the agency from one record of its "
                     "HPCL data: CRM, IVRS, tickets, daily operations, inventory, credit "
                     "management, accounts, HRMS and payroll, and compliance and licences.</p>\n"
                     "<p>On top sits LPG Guru AI, a chat portal that brings HPCL&rsquo;s scattered "
                     "platforms, circulars and scheme rules into one place, so staff ask a question "
                     "in plain language instead of hunting across portals.</p>\n"
                     "<p>LPG Guru is independent technology built for distributors. It is not an "
                     "HPCL product and carries no HPCL endorsement.</p>",
                     """<p><strong>A gas agency runs on one system instead of paper registers, spreadsheets and a separate tool for everything.</strong></p>
<ul>
<li><strong>The numbers tie out by themselves.</strong> Daily entries, accounts and stock are linked, so nobody matches them by hand at the end of the day.</li>
<li><strong>No complaint is lost.</strong> Every consumer call is answered and logged, and each complaint becomes a ticket tracked until it is closed.</li>
<li><strong>Deadlines are visible.</strong> Dashboards show who still owes eKYC or an inspection, and which licences are coming up for renewal.</li>
<li><strong>Hidden revenue is found.</strong> Lapsed and due customers are listed and reached by WhatsApp, SMS or a call.</li>
<li><strong>Staff stop asking the owner.</strong> LPG Guru AI answers questions about HPCL processes and schemes.</li>
<li><strong>It replaces</strong> paper registers, Excel trackers, a separate accounting package, an IVR vendor and a bulk-messaging tool, with one login, one support line and one bill. It is live at lpgguru.in.</li>
</ul>""",
                     links='<a class="btn primary" href="https://lpgguru.in" target="_blank" '
                           'rel="noopener">See it live</a>\n<a class="btn" href="https://chat.lpgguru.in" '
                           'target="_blank" rel="noopener">LPG Guru AI</a>',
                     extra="""
<h3>How it is built</h3>
<div class="fig"><div class="arch">
<div class="arch-row"><div class="node"><b>The agency&rsquo;s HPCL data</b><span>Consumers and bookings from HPCL and CDCMS. Entered once, reused everywhere.</span></div></div>
<div class="down">&darr; one record &darr;</div>
<div class="arch-row"><div class="node strong"><b>Front office</b><span>CRM, IVRS, tickets and consumer campaigns.</span></div><div class="node strong"><b>Operations</b><span>Daily operations, inventory and credit management.</span></div><div class="node strong"><b>Back office</b><span>Accounts, HRMS and payroll, compliance and licences.</span></div><div class="node strong"><b>Knowledge</b><span>LPG Guru AI for HPCL processes, schemes and circulars.</span></div></div>
<div class="down">&darr; one login &darr;</div>
<div class="arch-row"><div class="node"><b>The owner and the staff</b><span>Counter, godown, deliveries and the books, all in the same place.</span></div></div>
</div><div class="cap">Twelve modules, one record of the agency</div></div>

<h3>Problem by problem</h3>
<ul>
<li><strong>Fragmented systems.</strong> One consumer, stock and cash record, shared across the agency.</li>
<li><strong>Manual reconciliation.</strong> Daily entries, accounts and inventory are linked, so the numbers tie out without matching by hand.</li>
<li><strong>Compliance without tracking.</strong> Dashboards show who is pending for eKYC and inspection, and which licences are due.</li>
<li><strong>Missed consumer calls.</strong> Every call is answered and logged, and each complaint becomes a ticket tracked to closure.</li>
<li><strong>Invisible revenue.</strong> Lapsed and due consumers are listed, then reached by WhatsApp, SMS and voice campaigns.</li>
<li><strong>Scattered knowledge.</strong> One chat answers HPCL process and policy questions.</li>
</ul>

<h3>Three design choices</h3>
<ol class="steps">
<li><strong>HPCL data first.</strong> Built around the data the distributor already has, so adoption does not start with retyping.</li>
<li><strong>Assisted onboarding.</strong> The team sets the agency up with the distributor instead of leaving it to self-serve.</li>
<li><strong>Built for the counter.</strong> Screens and terms match what agency staff already use, which keeps training short.</li>
</ol>

<h3>Why now</h3>
<p>25,616 PSU LPG distributors serve about 33 crore active domestic customers, and most still
run the agency itself on paper and generic tools. Compliance went digital before the agency
did, and oil company portals capture what must be reported upward, not the distributor&rsquo;s
cash, people or profit. With a fixed commission per cylinder, profit comes from less leakage,
fewer penalties and faster reconciliation. Packed domestic LPG sales fell 14.1% from April to
July 2026, so keeping consumers and cutting cost matter more than before.</p>
<p>The trade-off is deliberate: depth in one oil company&rsquo;s workflows first, at the cost of
a smaller starting market.</p>

<h3>The test we hold it to</h3>
<p class="rule">One-stop only counts if the old tool goes.</p>
<p>If an agency still keeps Tally or a register alongside, LPG Guru is one more system, not the
only one. Every extra module in use makes the others more accurate, because they all read the
same data.</p>
"""
                 )),
            dict(slug="ownr", label="Ownr", icon="memory",
                 stamp=dict(img="logos/ownr.svg", logo=True, text="OWNR"),
                 title="Ownr",
                 lede="Your memory, not the model’s. One private memory and persona that every AI you use plugs into.",
                 body=project(
                     "Every AI keeps its own memory, locked inside itself. Tell ChatGPT something on "
                     "your phone and Claude on your laptop has never heard it. Switch tools and you "
                     "start again. You end up repeating yourself and carrying context between your "
                     "own assistants. And the context that would help most, how you actually work, "
                     "is something nobody writes down. Every memory tool today makes you curate it "
                     "by hand.",
                     "<p>We are building ownr: a portable &ldquo;agent self&rdquo; that you own. It "
                     "holds who you are, what you know and how you work, and carries it to every AI "
                     "you use over MCP: ChatGPT, Claude, Cursor, Claude Code, Codex and the agents "
                     "you run. Tell one AI something and every other one already knows it.</p>",
                     """<p><strong>I never repeat myself to an AI. What I tell one of them, all of them know.</strong></p>
<ul>
<li><strong>It is the shared memory behind my daily work</strong> across Claude, Codex, ChatGPT and always-on agents, including Ishaan.</li>
<li><strong>It holds 1,699 memories across 45 projects</strong>, and 31 tools let any connected AI read and write them.</li>
<li><strong>Corrections stick.</strong> Fix a fact once and every tool sees the fix.</li>
<li><strong>Early access is open</strong> by invitation.</li>
</ul>""",
                     links='<a class="btn primary" href="https://ownr.digital/#waitlist" target="_blank" '
                           'rel="noopener">Join the waitlist</a>\n<a class="btn" href="https://ownr.digital" '
                           'target="_blank" rel="noopener">ownr.digital</a>',
                     extra="""
<h3>What it holds</h3>
<div class="fig"><div class="arch">
<div class="arch-row"><div class="node strong"><b>Persona</b><span>Your role, tone and preferences, learned from your own activity rather than typed into a settings page.</span></div><div class="node strong"><b>Memory</b><span>Projects, decisions with their reasons, standing rules and notes. Versioned, editable, and nothing silently deleted.</span></div></div>
<div class="arch-row"><div class="node strong"><b>Skills</b><span>Your skill files from Claude Code, Codex, Cursor and Antigravity in one versioned registry, plus new skills drawn from the rules and decisions you keep repeating.</span></div><div class="node"><b>Handoffs</b><span>Leave a task in one tool, pick it up in another where you stopped. The next layer we are building.</span></div></div>
</div><div class="cap">One self, carried to every AI</div></div>

<h3>It fills itself</h3>
<p>The point is good context with no curation. ownr learns from what you already do:</p>
<ul>
<li><strong>Your own activity.</strong> What you work on, when and where, reduced to derived signals on your device before anything leaves it.</li>
<li><strong>Your AI conversations.</strong> Sessions from the AI tools on your machine, with secrets scrubbed on the device, become facts and decisions.</li>
<li><strong>What you already have.</strong> Import the memory you have built up in other tools on day one.</li>
<li><strong>What you tell any AI.</strong> Say &ldquo;remember this&rdquo; to any connected tool and it is saved once, for all of them.</li>
</ul>
<p>From that it builds a personal map of your things, so &ldquo;my bank&rdquo; or &ldquo;the
Nexa deal&rdquo; resolves to <em>yours</em>, with the evidence shown, or it asks you.</p>

<h3>What a day looks like</h3>
<ol class="steps">
<li>On your phone you tell ChatGPT: &ldquo;Priya at Nexa wants the invoice split in two. Say yes.&rdquo;</li>
<li>On your laptop, Claude drafts the reply to Priya. Two invoices, as agreed.</li>
<li>Cursor fixes the export bug three customers reported, and your inbox agent drafts the three &ldquo;it&rsquo;s fixed&rdquo; emails for you to send.</li>
<li>Next morning, any of them opens with: Priya is sorted, the fix is out, and Thursday&rsquo;s brief is ready.</li>
</ol>
<p class="rule">You said it once. They all kept it.</p>

<h3>How it is different</h3>
<ul>
<li><strong>Not one model&rsquo;s memory.</strong> Built-in AI memory stays with that AI. ownr moves with you to every model, and switching tools costs nothing.</li>
<li><strong>Not a notebook you maintain.</strong> Other context tools make you curate, map by map. ownr fills itself from behaviour you already have.</li>
<li><strong>Not a cloud that holds you.</strong> Only derived, domain-level or hashed data leaves your device: never raw URLs, page titles, keystrokes or content. Running it locally is free.</li>
<li><strong>Memory and a twin, together.</strong> A record of what you decided, and a persona of how you work, from the same source. Either alone is a commodity.</li>
</ul>

<h3>You stay in control</h3>
<p>Every app you connect gets read only, or read and write, and nothing more. Your persona is a
separate permission that is never implied. Every call is logged, and a revoked app is refused
on its next call. A wrong fact is corrected in place, and history is kept rather than erased.</p>

<h3>Honest about the bet</h3>
<p>The memory is shipped and used daily. Predicting what you will do next is the long bet: its
top guess has been right 8% to 54% of the time, against a frequency baseline of 2% to 26%. It
beats the baseline. It is not yet a moat.</p>
"""
                 )),
            dict(slug="vdo-hosting", label="VDO Hosting", icon="video",
                 stamp=dict(img="logos/vdo-hosting.svg", logo=True, text="VDO HOSTING"),
                 title="VDO Hosting",
                 lede="When India locked down, we put its gatherings online, for the people the internet had left behind.",
                 body=project(
                     "In March 2020 every meeting, ceremony, class and celebration in India had to "
                     "move online, overnight. The tools existed. The people running these events, "
                     "most of them over 30, had never used them. A bank still had to hold its AGM, "
                     "a coach still had to run an exam, a family still wanted the birthday. The "
                     "lockdown had opened a digital divide right in the middle of everyday life.",
                     "<p>I founded VDO Hosting in May 2020 to close it. We did not sell software. We "
                     "ran the event, so the host never had to learn a setting: planning it with "
                     "them, choosing the right platform, hosting it live, streaming it, and handing "
                     "back the recording.</p>",
                     """<p><strong>People who had never used online tools could still hold their meetings, and a small team grew into a business.</strong></p>
<ul>
<li><strong>700+ events with 2,50,000+ participants</strong>, for clients across India.</li>
<li><strong>From a couple of meetings a week to several a day</strong>, run by a team of 10.</li>
<li><strong>Real gatherings, held online</strong> when meeting in person was not possible: banks held their AGMs, coaches ran exams, and families held birthdays and religious gatherings.</li>
</ul>""",
                     "Video conferencing and live-streaming platforms, 3D event hosting, graphic "
                     "design, video composition and editing",
                     '<a class="btn primary" href="https://vdohosting.in" target="_blank" '
                     'rel="noopener">vdohosting.in</a>',
                     extra="""
<h3>Everything, held online</h3>
<p>If people gathered for it, we hosted it: events, talk shows, keynotes, award ceremonies,
corporate meetings, annual general meetings for banks, celebrity and YouTube events, religious
gatherings, social gatherings, birthday parties, Zumba classes, coaching and exams.</p>

<h3>The whole event, end to end</h3>
<div class="fig"><div class="arch">
<div class="arch-row"><div class="node strong"><b>Before</b><span>Personal planning with the host, the right platform for the format, and the graphics.</span></div><div class="node strong"><b>During</b><span>Live hosting, interactive formats, streaming to social media, broadcasting, and immersive 3D hosting.</span></div><div class="node strong"><b>After</b><span>Video composition and editing, the recording, and analytics.</span></div></div>
</div><div class="cap">The host shows up. We run everything else.</div></div>

<h3>Why it worked</h3>
<ul>
<li><strong>Speed over polish.</strong> It started within weeks of the lockdown, while the need was brand new.</li>
<li><strong>Sell the outcome, not the tool.</strong> Nobody wanted to learn video software. They wanted their event to happen. So we made sure it did.</li>
<li><strong>Say yes to every format.</strong> A Zumba class and a bank AGM need different things, but the same playbook: plan it with the host, run it, hand it back.</li>
</ul>
"""
                 )),
            dict(slug="mahabeer", label="Mahabeer Inventory", icon="warehouse",
                 stamp=dict(icon="warehouse", text="MAHABEER"),
                 title="Mahabeer Inventory",
                 lede="An inventory app that tripled a rental business\u2019s orders.",
                 body=project(
                     "Mahabeer rents steel shuttering rods to construction sites and events from "
                     "three warehouses, two in Delhi and one in Punjab. Stock lived in Excel, "
                     "interstate E-way bills were done by hand, and rods going out and coming back "
                     "were hard to track.",
                     "<p>At Bizarc Ventures I audited their 120+ warehouse transactions a day, then "
                     "we built a custom app around what they actually do: live stock across all "
                     "three warehouses, orders allocated from one stock table, order history and "
                     "tracking, and E-way bills generated for interstate moves.</p>",
                     """<p><strong>A rental business tripled its monthly orders and stopped losing track of its steel.</strong></p>
<ul>
<li><strong>Orders went from 30 to 90 a month</strong> within four months of using the app.</li>
<li><strong>Order accuracy rose from 82% to 97%</strong>, and the risk of billing mistakes fell by 90%.</li>
<li><strong>Stock in all three warehouses is visible live</strong>, so a missing rod shows up instead of going unnoticed.</li>
<li><strong>The Excel sheets are gone</strong>, and the interstate bills are produced inside the app.</li>
</ul>""")),
            dict(slug="royal-living-tangi", label="Royal Living Tangi", icon="phone",
                 stamp=dict(icon="phone", text="ROYAL LIVING"),
                 title="Royal Living Tangi",
                 lede="Cleaning a 34,000-customer gas agency database, by phone and on foot.",
                 body=project(
                     "Royal Living Tangi, an HPCL LPG agency, serves 34,000 customers. About 1% "
                     "skipped booking and phoned the delivery staff directly, so orders and routes "
                     "could not be tracked, and the customer records had drifted.",
                     "<p>At Bizarc Ventures I cleaned the database first: duplicates merged, "
                     "conflicts resolved. Then I led a remote team of 7, hired from the customers' "
                     "own areas so language was never a barrier, to call customers, verify their "
                     "details and show them online booking and the PMUY scheme. GSM-based outbound "
                     "calling replaced the old IVRS line.</p>\n"
                     "<p>For customers a call could not reach, we worked with self-help groups and "
                     "Mission Shakti groups to verify them in person.</p>",
                     """<p><strong>A gas agency now has a clean customer database, and a team that keeps it clean.</strong></p>
<ul>
<li><strong>14,500 records cleaned and 5,027 addresses verified in two months</strong>, out of 34,000 customers.</li>
<li><strong>Customers who used to phone the delivery staff directly are being brought back</strong> into the proper booking process, with online booking explained on every call.</li>
<li><strong>Calls now run on GSM-based outbound calling</strong> in place of the old IVRS line.</li>
<li><strong>Digital bookings are projected to rise 12&ndash;15%.</strong></li>
</ul>""")),
            dict(slug="osda", label="OSDA", icon="govt",
                 stamp=dict(img="logos/osda.jpg", logo=True, text="OSDA"),
                 title="OSDA, Government of Odisha",
                 lede="A \u20b960-lakh digital transformation, built for 12,000+ users.",
                 body=project(
                     "OSDA, part of the Government of Odisha, needed its digital platform rebuilt "
                     "for the 12,000+ people who use it: more transparent, and within government "
                     "compliance rules.",
                     "<p>At Bizarc Ventures I directed the &#8377;60-lakh project, keeping product "
                     "decisions in line with the government's compliance goals. We launched "
                     "process automation features: a modular CMS, push notifications and "
                     "analytics dashboards.</p>",
                     """<p><strong>A government platform that is easier to see into, for the 12,000+ people who use it.</strong></p>
<ul>
<li><strong>A &#8377;60-lakh digital transformation</strong>, delivered inside the government&rsquo;s compliance rules.</li>
<li><strong>A modular CMS, push notifications and analytics dashboards</strong>, so the people using the platform can see what is happening on it.</li>
</ul>""")),
            dict(slug="neoteric", label="Neoteric", icon="megaphone",
                 stamp=dict(icon="megaphone", text="NEOTERIC"),
                 title="Neoteric",
                 lede="From an idea to a working consultancy, and a 2,50,000-impression campaign.",
                 body=project(
                     "Neoteric was a new consultancy with good ideas and little else: no aligned "
                     "team, no way of running day to day, no brand, and a government PR campaign "
                     "to deliver.",
                     "<p>At Bizarc Ventures we built the business around the idea. We helped hire "
                     "and align the team, wrote the standard operating procedures, and automated "
                     "the routine work so they could focus on clients. We wrote the brand story and "
                     "designed the identity: logo, colours and imagery.</p>\n"
                     "<p>I designed and ran the government PR campaign with a 45-member team, "
                     "standard SOPs and compliance checks on every outreach step.</p>",
                     """<p><strong>A new consultancy went from an idea to a working business, and ran a government campaign that generated 2,50,000+ impressions.</strong></p>
<ul>
<li><strong>A team, written ways of working and a brand of its own:</strong> logo, colours, imagery and story.</li>
<li><strong>A government PR campaign run by 45 people</strong> with standard steps and compliance checks on every outreach step, generating 2,50,000+ impressions.</li>
</ul>""")),
            dict(slug="iwd-app", label="IWD Secretary App", icon="app",
                 stamp=dict(img="logos/innerwheel.jpg", logo=True, text="INNER WHEEL"),
                 title="IWD Secretary App",
                 lede="Taking 2,400+ women changemakers from paper to an app.",
                 body=project(
                     "Inner Wheel District 301 in Delhi has 2,400+ members across 60+ clubs, "
                     "running events and projects all year, with no system to count them: who "
                     "benefited, how many hours members gave, what each project cost.",
                     "<p>At Bizarc Ventures we built the IWD Secretary App with them. Every club's "
                     "projects sit in one place, each tracking beneficiaries, members' hours and "
                     "spend. The monthly and yearly reports for the international body are "
                     "generated automatically, and finance reports export as PDF.</p>",
                     """<p><strong>2,400+ volunteers across 60+ clubs now report their work in one app, instead of by hand.</strong></p>
<ul>
<li><strong>Every club onboarded.</strong></li>
<li><strong>Reports write themselves.</strong> The monthly and yearly reports for the international body are produced automatically and are ready for audit.</li>
<li><strong>Every project is tracked:</strong> beneficiaries, hours given and money spent, with finance reports exported as PDF.</li>
<li><strong>The work is visible.</strong> Anyone outside the club can see what the district does.</li>
</ul>""")),
        ]))

    v.append(dict(
        slug="cv", label="Moheet CV", icon="cv",
        stamp=dict(img="cv/portrait.jpg", text="VERIFIED"),
        title="My work, so far",
        lede="Seven roles since 2020, in plain lines.",
        body=CV))

    v.append(dict(
        slug="parts", label="The seven parts", art="loopring", glyph=None,
        title="The seven parts",
        lede="Six of these seven are not the model. Six of these seven are where things "
             "actually break.",
        body="""
<p>Nearly everyone starts at the model and stops there, which is why most attempts stall at
something that talks back well and does nothing. The model is one part. The other six are the
work, and they are all things you control.</p>
<div class="panel"><div class="panel-head"><span class="t">The whole thing, in one line</span></div>
<div style="padding:18px 15px">
<div class="formula"><span class="f-key">Model</span><span class="f-op">+</span><span class="f-key">Harness</span><span class="f-op">+</span><span class="f-key">Loop</span><span class="f-op">+</span><span class="f-key">MCP</span><span class="f-op">+</span><span class="f-key">Skills</span><span class="f-op">+</span><span class="f-key">Memory</span><span class="f-op">=</span><span class="f-end">your idea, working</span></div>
</div></div>
<table><thead><tr><th>Part</th><th>What it is</th></tr></thead><tbody>
<tr><td>Model</td><td>Predicts text. On its own it can only talk back.</td></tr>
<tr><td>Harness</td><td>What it reads, what it may touch, who it is. <a href="#build/soul" data-jump="build/soul">Start here</a>.</td></tr>
<tr><td>Loop</td><td>Do, check, decide whether to go again. Why work finishes. <a href="#build/loop" data-jump="build/loop">Here</a>.</td></tr>
<tr><td>MCP</td><td>One standard for reaching tools. <a href="#build/tools" data-jump="build/tools">Here</a>.</td></tr>
<tr><td>Skills</td><td>One task, written down once. <a href="#skills" data-jump="skills">Here</a>.</td></tr>
<tr><td>Context</td><td>What it sees right now. It fills up, and things fall out.</td></tr>
<tr><td>Memory</td><td>What survives the conversation ending. <a href="#build/memory" data-jump="build/memory">Here</a>.</td></tr>
</tbody></table>
<p>The order matters. Each one is only worth adding once the one before it holds.</p>"""))

    v.append(dict(
        slug="kit", label="The skills kit", art=None, icon="kit",
        title="Find it. Write it. Fix it.",
        lede="Three prompts for skills.",
        body=f"""
<p>A skill is one task written down once. Everyone says to write them. Nobody says which ones,
or whether the ones you downloaded are any good.</p>
<p>The first prompt finds what you keep redoing. The second is
<a href="#build/generator">the Setup Interview</a>, which writes the skill from how you do it.
The third checks any skill and fixes it.</p>
{panel("finder", "1 \u00b7 The Repeat Finder", "chat or terminal")}
<p>It counts, it does not guess. Every suggestion says how many times and where, and if nothing
repeats enough it says so and stops. A terminal agent reads your saved history. A chat usually
cannot, so it asks you five short questions instead and says that is what it used. It never
prints a secret, and it asks before it reads anything.</p>
{panel("doctor", "3 \u00b7 The Skill Doctor", "paste a skill under it")}
<p>Paste any skill: yours, a colleague's, one from GitHub. It checks it, lists every risky line,
and rewrites it so it improves each time you correct it. It only sees what you paste, so for a
whole folder use a terminal agent. <strong>Read the flagged lines yourself before you install
anything.</strong></p>"""))

    v.append(dict(
        slug="sheet", label="The build sheet", art=None, icon="build",
        title="From idea to working thing",
        lede="The order to use everything here in. Two routes: an agent that works for you, "
             "or a tool people use.",
        body=f"""
<h3>Build an agent, in seven steps</h3>
<ol class="steps">
<li><strong>Pick the job.</strong> One task you repeat. Not &ldquo;an assistant&rdquo;: one task. <a href="#build/kit" data-jump="build/kit">The Repeat Finder</a></li>
<li><strong>Say who it is.</strong> Its role, its standards, what it never does. <a href="#build/generator" data-jump="build/generator">The Setup Interview</a> or <a href="#build/soul" data-jump="build/soul">a soul file</a></li>
<li><strong>Pick the harness.</strong> A chat, a terminal agent, or a model on your own laptop if the data can&rsquo;t leave. <a href="#build/local" data-jump="build/local">Run it on your laptop</a></li>
<li><strong>Define done.</strong> The goal, the check, the stop, the limit. <a href="#build/loop" data-jump="build/loop">The loop checklist</a></li>
<li><strong>Connect only what it needs,</strong> with a human in the loop on anything risky. <a href="#build/tools" data-jump="build/tools">The tool registry</a></li>
<li><strong>Do it once badly, then write the skill.</strong> Your corrections are the skill. <a href="#build/kit" data-jump="build/kit">The Skill Doctor</a></li>
<li><strong>Give it memory,</strong> so tomorrow starts where today stopped. <a href="#build/memory" data-jump="build/memory">Second Brain</a></li>
</ol>
<p>Each step is only worth adding once the one before it holds.</p>
<h3>Build a tool with AI, in five steps</h3>
<p>How the session deck and this site were built.</p>
<ol class="steps">
<li><strong>Write a one-page brief first.</strong> Who uses it, what goes in, what comes out, and how you&rsquo;ll know it works.</li>
<li><strong>Ask for a plan before any code.</strong> Correct the plan, not the code. It is ten times cheaper.</li>
<li><strong>Build the smallest version that works end to end.</strong> One input, one output, nothing else.</li>
<li><strong>Test it on real data,</strong> with a check that can fail.</li>
<li><strong>Ship it somewhere real</strong> (GitHub Pages, Vercel), then improve it from use, not from guesses.</li>
</ol>
<h3>Not sure which route?</h3>
<p>Five questions about your idea, then a one-page plan: which parts it needs, where to build it,
its limits, the build order, and what to skip for now.</p>
{panel("planner", "The Build Planner", "any chat or agent")}"""))

    v.append(dict(
        slug="slides", label="The slides", art=None, icon="slides",
        title="The slides",
        lede="From the session. Four digits.",
        # A lock turns the tile into a pop-up that asks for a PIN. Any node can carry
        # one, a folder as well as a page; "unlock" names what happens on success.
        lock=dict(unlock="deck", hint="Four digits. Ask me for it."),
        body="<p>Locked. Open it from the poster.</p>"))

    # Words people are likely to type that the prose does not happen to contain.
    KEYWORDS = {
        "generator": "prompt interview setup start here chatgpt claude gemini copilot custom instructions",
        "soul": "persona role tone voice style system prompt consultant data ops product marketing harness",
        "loop": "agent wander stuck retry goal check stop limit finish done",
        "tools": "mcp connector server integration access permissions registry composio human in the loop approval limits mcp.so",
        "memory": "remember forget context corrections agents.md claude.md learning "
                  "second brain secondary ownr shared memory",
        "skills": "business analytics skills bas repo github machine learning statistics "
                  "optimisation optimization pricing price elasticity regression clustering "
                  "forecasting ab test experiment recommender data engineering toolkit "
                  "install plugin marketplace",
        "local": "ollama offline privacy compliance laptop cpu ram gpu open source weights licence llama qwen gemma mistral phi deepseek gpt-oss hugging face lm studio jan",
        "parts": "model harness loop mcp skills context memory overview recap formula summary",
        "slides": "slides deck presentation pin code locked session talk powerpoint",
        "sheet": "build sheet planner framework plan idea agent tool app product capstone steps route brief ship",
        "kit": "skills skill doctor repeat finder find recurring repeat automate history review audit "
               "safe risky rewrite SKILL.md prompt agent chat",
        "projects": "projects ownr portfolio work building side product repo client case study "
                    "things i have built side project",
        "vdo-hosting": "vdo hosting video virtual events webinar zoom lockdown covid founder startup agm live streaming 3d hosting digital divide",
        "mahabeer": "mahabeer inventory warehouse stock e-way bill app rental steel bizarc",
        "royal-living-tangi": "royal living tangi lpg gas hpcl database data cleaning pmuy ivrs gsm bizarc",
        "iwd-app": "iwd inner wheel secretary app ngo club reports women bizarc",
        "ishaan": "ishaan hermes agent ai agent mailmodo slack automation ops customer success self-healing self-review claude code mcp",
        "self-serve": "self serve strategy segmentation churn customer success auto pilot dormant playbook vitally amplitude health score mailmodo cohort retention adoption",
        "outreach": "outreach console cold email outbound sdr sales prospecting apollo sequence campaign mailmodo deliverability",
        "leaderboard": "benchmark benchmarking leaderboard ai models pricing besthunt openrouter llm compare cost ranking",
        "lpg-guru": "lpg guru lpgguru gas agency distributor hpcl erp saas crm ivrs compliance solarc ai chat",
        "osda": "osda odisha government digital transformation cms dashboards compliance bizarc",
        "neoteric": "neoteric consultancy pr campaign government branding brand identity sop bizarc",
        "build": "session talk presentation how to build with ai giveaway pack take home "
                 "seven parts model harness loop mcp skills context memory plain text tonight",
    }
    KEYWORDS["cv"] = ("cv resume résumé experience work history employment career hire "
                      "download pdf mailmodo bizarc v do hosting molson coors education skills "
                      "osda odisha government lpg neoteric mahabeer iwd vitally hubspot")
    def index(item):
        """A node is searchable on its own words plus, if it is a folder, its children's."""
        kids = item.get("children", [])
        for k in kids:
            index(k)
        # Keywords go before the body: the index is cut at 1400 characters, and a long
        # page would otherwise push them off the end.
        words = " ".join([item["title"], item["lede"], KEYWORDS.get(item["slug"], ""),
                          re.sub(r"&[#\w]+;", " ", re.sub(r"<[^>]+>", " ", item.get("body", ""))),
                          " ".join(k["find"] for k in kids)])
        item["find"] = re.sub(r"\s+", " ", item["label"] + " " + words).strip().lower()[:1400]

    # The root is a portfolio. One folder holds everything from the session, in the
    # order it is taught; the other holds the work. Both grow by adding a child.
    by = {n["slug"]: n for n in v}
    ORDER = ["parts", "sheet", "generator", "soul", "loop", "tools", "kit", "memory", "local", "slides"]
    root = [
        dict(slug="build", label="How to Build with AI", art=None, icon="loop",
             title="How to Build with AI",
             lede="Everything from the session.",
             children=[by[k] for k in ORDER]),
        by["skills"],
        by["projects"],
        by["cv"],
    ]
    for item in root:
        index(item)
    return root


def build():
    c = content()
    A = art()
    I = icons()
    V = views(A, c)

    SPOTS_UNUSED = None

    def icon_for(node):
        """A node names an icon, or borrows the one matching its slug."""
        return I.get(node.get("icon") or node["slug"]) or I["spark"]

    def walk(nodes, parent=""):
        """Every node, with the path that addresses it. One place that knows the tree."""
        for i, n in enumerate(nodes):
            path = f"{parent}/{n['slug']}" if parent else n["slug"]
            yield path, n, i, parent
            for item in walk(n.get("children", []), path):
                yield item

    ALL = list(walk(V))

    def art_for(node):
        """An icon, or for a node that names a stamp, a postage stamp with a photo."""
        st = node.get("stamp")
        if st:
            if st.get("icon"):
                inner = f'<span class="face icon">{I[st["icon"]]}</span>'
            else:
                fit = " logo" if st.get("logo") else ""
                inner = (f'<img class="face{fit}" src="{st["img"]}" alt="" draggable="false" '
                         f'width="350" height="350">')
            return (f'<span class="stamp-wrap"><span class="stamp">{inner}'
                    f'<span class="st">{H.escape(st["text"])}</span></span></span>')
        return f'<span class="ico">{icon_for(node)}</span>'

    def tile(path, node, i, parent):
        """Every tile for every folder is rendered once; the poster shows one set."""
        badge = f'<span class="lockmark" aria-label="locked">{I["lock"]}</span>' if node.get("lock") else ""
        return (f'<button class="obj{" locked" if node.get("lock") else ""}" data-go="{path}" data-parent="{parent}" '
                f'data-find="{H.escape(node.get("find", ""))}">'
                f'<span class="thumb{" has-stamp" if node.get("stamp") else ""}">{art_for(node)}{badge}</span>'
                f'<span class="n">({i + 1:02d})</span>'
                f'<span class="label">{H.escape(node["label"])} '
                f'<span class="arrow">&rarr;</span></span></button>')

    objects = "".join(tile(p2, n, i, parent) for p2, n, i, parent in ALL)

    # Only a leaf gets a pane. A folder opens the poster again, retitled.
    panes = "".join(
        f'<article class="pane" data-pane="{path}" hidden>'
        f'<div class="wrap view-head"><span class="n">({i + 1:02d})</span>'
        f'<h2>{H.escape(n["title"])}</h2>'
        f'<p class="lead">{H.escape(n["lede"])}</p></div>'
        f'<div class="wrap view-body">{n["body"]}</div></article>'
        for path, n, i, parent in ALL if not n.get("children"))

    # The poster can stand at the root or inside any folder, so each needs a heading.
    HOME = ("Hey, I\u2019m Moheet.", "Steal anything.")
    FOLDERS = {"": {"t": HOME[0], "s": HOME[1]}}
    for path, n, i, parent in ALL:
        if n.get("children"):
            FOLDERS[path] = {"t": n["title"], "s": n["lede"]}
    ICONS_BY_PATH = {p2: icon_for(n) for p2, n, i, parent in ALL}

    # Every one checked for contrast on the paper background and with white text on it.
    ACCENTS = [("Cobalt", "#2F4FD4"), ("Forest", "#1F6B4A"), ("Rust", "#B3431E"),
               ("Oxblood", "#8C2130"), ("Violet", "#5B33B5"), ("Teal", "#11636E")]
    swatches = "".join(
        f'<button class="sw" data-accent="{hx}" title="{n2}" aria-label="{n2}" '
        f'aria-pressed="{"true" if j == 0 else "false"}" '
        f'style="background:{hx}"></button>' for j, (n2, hx) in enumerate(ACCENTS))

    FOLDERS_JSON = json.dumps(FOLDERS)
    ICONS_JSON = json.dumps(ICONS_BY_PATH)
    LOCKS_JSON = json.dumps({p2: dict(title=n["title"], **n["lock"])
                             for p2, n, i, parent in ALL if n.get("lock")})
    PATHS = json.dumps([p2 for p2, n, i, parent in ALL])
    LABELS = json.dumps({p2: n["label"] for p2, n, i, parent in ALL})
    PARENTS = json.dumps({p2: parent for p2, n, i, parent in ALL})

    page = f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-EZKQBDEGY9"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  /* The tag loads everywhere but reports only from the real site, so staging, previews
     and localhost never count as visits. Page views are sent by the page itself
     (see apply), because this is one page that swaps its content: Google would
     otherwise see the home page and nothing else. */
  if (location.hostname === "moheetsubudhi.com") {{
    gtag('config', 'G-EZKQBDEGY9', {{ send_page_view: false }});
  }}
</script>
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Moheet Subudhi</title>
<meta name="description" content="Things I am building, and the whole How to Build with AI pack: a prompt that writes your own setup, five ready-made ones, and 36 analytics skills.">
<meta name="theme-color" content="#F2EEE3">
<meta property="og:title" content="Moheet Subudhi">
<meta property="og:description" content="Everything I am building, and everything I would hand over. Plain text, nothing to install, and it works on your phone.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,800&family=Hanken+Grotesk:wght@400;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head><body>

<div id="shell">
<div id="poster">
<div class="topbar" id="hubBar" hidden><div class="inner">
  <button class="back" id="hubUp">&larr; Back</button>
  <span class="where" id="hubWhere"></span>
</div></div>
<main id="hub" class="scatter">
  <div class="poster-title">
    <h1 id="hubTitle">{HOME[0]}</h1>
    <div class="sub" id="hubSub">{HOME[1]}</div>
  </div>
  <div class="search"><label class="box">
    {I["search"]}
    <input type="search" id="q" placeholder="Search everything" autocomplete="off"
           aria-label="Search everything">
    <div class="results" id="results" hidden></div>
  </label><div class="count" id="count"></div></div>
  <div class="objects">{objects}</div>
</main>
</div>

<div id="view">
  <div class="topbar"><div class="inner">
    <button class="back" id="back">&larr; Back</button>
    <span class="where" id="where"></span>
  </div></div>
  {panes}
</div>

<div id="chrome"><div class="row">
  <div class="contact">
    <a href="{LINKEDIN}" target="_blank" rel="noopener">{I["linkedin"]}LinkedIn</a>
    <a id="mail" href="#">{I["mail"]}Email</a>
    <a href="{WHATSAPP}" target="_blank" rel="noopener">{I["whatsapp"]}WhatsApp</a>
  </div>
  <div class="tail">
    <div class="swatches" role="group" aria-label="Accent colour">{swatches}</div>
  </div>
</div></div>

<div class="scrim" id="pinScrim" hidden>
  <div class="dialog" id="pinDialog" role="dialog" aria-modal="true" aria-labelledby="pinTitle">
    <button class="dlg-x" id="pinX" type="button" aria-label="Close">&times;</button>
    <div class="dlg-kicker">LOCKED</div>
    <h3 id="pinTitle"></h3>
    <p class="dlg-hint" id="pinHint"></p>
    <label class="cells" for="pinIn">
      <input id="pinIn" type="text" inputmode="numeric" pattern="[0-9]*" maxlength="4"
             autocomplete="one-time-code" autocapitalize="off" spellcheck="false"
             aria-label="Four digit PIN">
      <span class="cell"></span><span class="cell"></span><span class="cell"></span><span class="cell"></span>
    </label>
    <p class="dlg-msg" id="pinMsg" role="status" aria-live="polite"></p>
  </div>
</div>

<div class="corner">
  <div class="hint" id="dragHint" hidden>
    <svg viewBox="0 0 96 54" aria-hidden="true"><path d="M8 50C22 48 50 44 70 30 80 23 85 16 87 9"/><path class="pass2" d="M9 52C23 50 51 45 71 31 81 24 85 17 86.5 10"/><path d="M90 8l-13 2M90 8l-3 13"/></svg>
    <span>drag the folders<br>anywhere you like</span>
  </div>
  <button id="resetSpots" class="reset" hidden>reset layout</button>
</div>
</div>

<script type="application/json" id="content">{json.dumps(c)}</script>
<script>
const C = JSON.parse(document.getElementById("content").textContent);
const SLUGS = {PATHS};        /* every addressable node, "projects/ownr" and so on */
const TITLES = {LABELS};
const PARENTS = {PARENTS};    /* so back climbs one level instead of jumping home */
const FOLDERS = {FOLDERS_JSON};   /* a path the poster can stand at, and its heading */
const PICS = {ICONS_JSON};
const LOCKS = {LOCKS_JSON};      /* nodes that ask for a PIN before they open */        /* each node's icon, reused in the search results */

document.querySelectorAll("pre[data-block]").forEach(function (el) {{
  if (C[el.dataset.block]) el.textContent = C[el.dataset.block];
}});

/* ---------- soul picker ---------- */
let currentSoul = 0;
const soulName = document.getElementById("soul-name");
const soulBody = document.querySelector('pre[data-block="soul"]');
function showSoul(i) {{
  currentSoul = i;
  soulName.textContent = C.souls[i].name;
  soulBody.textContent = C.souls[i].body;
  document.querySelectorAll("[data-soul]").forEach(function (t) {{
    t.setAttribute("aria-selected", String(Number(t.dataset.soul) === i));
  }});
}}
document.querySelectorAll("[data-soul]").forEach(function (t) {{
  t.addEventListener("click", function () {{ showSoul(Number(t.dataset.soul)); }});
}});
showSoul(0);

/* ---------- the PIN pop-up ----------
   The page never knows a PIN. It sends what was typed to a server, which checks it and
   hands back a token that expires. Wrong answers come back slowly on purpose. A node
   opts in with a lock flag in the tree; "unlock" says what a right answer does. */
const DECK_API = "https://how-to-build-with-ai-deck.vercel.app";
const UNLOCKERS = {{
  deck: async function (pin) {{
    const r = await fetch(DECK_API + "/api/unlock", {{
      method: "POST", headers: {{ "Content-Type": "application/json" }},
      body: JSON.stringify({{ pin: pin }})
    }});
    if (!r.ok) return false;
    const d = await r.json();
    location.href = DECK_API + "/api/deck?t=" + encodeURIComponent(d.token);
    return true;
  }},
  /* Same check, but a right answer opens the locked page here and keeps it open for
     the rest of the visit. A deterrent, like the slides: the server holds the PIN. */
  open: async function (pin, path) {{
    const r = await fetch(DECK_API + "/api/unlock", {{
      method: "POST", headers: {{ "Content-Type": "application/json" }},
      body: JSON.stringify({{ pin: pin }})
    }});
    if (!r.ok) return false;
    unlocked[path] = true;
    try {{ sessionStorage.setItem("unlocked", JSON.stringify(unlocked)); }} catch (e) {{}}
    closeLock();
    go(path);
    return true;
  }}
}};
let unlocked = {{}};
try {{ unlocked = JSON.parse(sessionStorage.getItem("unlocked") || "{{}}") || {{}}; }} catch (e) {{}}
function isLocked(path) {{ return !!LOCKS[path] && !unlocked[path]; }}
const scrim = document.getElementById("pinScrim"), pinIn = document.getElementById("pinIn"),
      pinMsg = document.getElementById("pinMsg"), cellsEl = document.querySelector(".cells"),
      cellEls = [...document.querySelectorAll(".cell")];
let pinFor = null, pinBusy = false, pinReturn = null;

function paintCells() {{
  cellEls.forEach(function (c, i2) {{
    c.textContent = pinIn.value[i2] ? "\u2022" : "";
    c.classList.toggle("on", i2 === Math.min(pinIn.value.length, 3) && document.activeElement === pinIn);
  }});
}}
function openLock(path) {{
  const lock = LOCKS[path]; if (!lock) return;
  pinFor = path; pinReturn = document.activeElement;
  document.getElementById("pinTitle").textContent = lock.title;
  document.getElementById("pinHint").textContent = lock.hint;
  pinIn.value = ""; pinMsg.textContent = ""; cellsEl.classList.remove("bad");
  scrim.hidden = false;
  requestAnimationFrame(function () {{ scrim.classList.add("on"); }});
  setTimeout(function () {{ scrim.classList.add("on"); }}, 40);   /* if frames are throttled */
  pinIn.focus(); paintCells();
}}
function closeLock() {{
  if (scrim.hidden) return;
  scrim.classList.remove("on");
  setTimeout(function () {{ scrim.hidden = true; }}, 220);
  pinFor = null;
  if (pinReturn && pinReturn.focus) try {{ pinReturn.focus(); }} catch (e) {{}}
}}
async function trySubmit() {{
  if (pinBusy || pinIn.value.length !== 4 || !pinFor) return;
  pinBusy = true; pinMsg.textContent = "Checking\u2026";
  let ok = false;
  try {{ ok = await UNLOCKERS[LOCKS[pinFor].unlock](pinIn.value, pinFor); }}
  catch (err) {{ pinMsg.textContent = "Could not reach the server. Try again."; pinBusy = false; return; }}
  pinBusy = false;
  if (ok) {{ pinMsg.textContent = scrim.hidden ? "" : "Opening\u2026"; return; }}
  pinMsg.textContent = "Not that one.";
  cellsEl.classList.remove("bad"); void cellsEl.offsetWidth; cellsEl.classList.add("bad");
  pinIn.value = ""; paintCells();
}}
pinIn.addEventListener("input", function () {{
  pinIn.value = pinIn.value.replace(/\D/g, "").slice(0, 4);
  pinMsg.textContent = ""; cellsEl.classList.remove("bad");
  paintCells(); trySubmit();
}});
pinIn.addEventListener("focus", paintCells);
pinIn.addEventListener("blur", paintCells);
document.getElementById("pinX").addEventListener("click", closeLock);
scrim.addEventListener("mousedown", function (e) {{ if (e.target === scrim) closeLock(); }});
scrim.addEventListener("keydown", function (e) {{
  if (e.key === "Escape") {{ e.stopPropagation(); closeLock(); }}
  if (e.key === "Tab") {{ e.preventDefault(); pinIn.focus(); }}   /* the pop-up holds focus */
}});

/* ---------- copy ---------- */
document.querySelectorAll("[data-copy]").forEach(function (btn) {{
  btn.addEventListener("click", async function (ev) {{
    /* The button sits inside a <summary>, so a click on it would also open or
       close the disclosure. Copying is not opening. */
    if (btn.closest("summary")) {{ ev.preventDefault(); ev.stopPropagation(); }}
    const key = btn.dataset.copy;
    const text = key === "soul" ? C.souls[currentSoul].body : C[key];
    let ok = false;
    try {{
      await navigator.clipboard.writeText(text);
      ok = true;
    }} catch (e) {{
      const ta = document.createElement("textarea");
      ta.value = text;
      ta.setAttribute("readonly", "");
      ta.style.cssText = "position:absolute;left:-9999px;top:0";
      document.body.appendChild(ta);
      ta.select();
      ta.setSelectionRange(0, text.length);
      try {{ ok = document.execCommand("copy"); }} catch (e2) {{ ok = false; }}
      document.body.removeChild(ta);
    }}
    btn.textContent = ok ? "Copied" : "Select and copy";
    btn.classList.toggle("done", ok);
    setTimeout(function () {{ btn.textContent = "Copy"; btn.classList.remove("done"); }}, 2000);
  }});
}});

/* ---------- routing: the poster, then one view at a time ----------
   Hash based, so it is a plain static file with no server rules, and any single
   item can be linked to directly. */
const panes = document.querySelectorAll("[data-pane]");
const whereEl = document.getElementById("where");
const backBtn = document.getElementById("back");

function crumb(path) {{
  /* "projects/ownr" reads as "My projects / Ownr" */
  const out2 = [];
  let p3 = path;
  while (p3) {{ out2.unshift(TITLES[p3] || p3); p3 = PARENTS[p3] || ""; }}
  return out2.join("  /  ");
}}

const hubTitle = document.getElementById("hubTitle");
const hubSub = document.getElementById("hubSub");
const hubUp = document.getElementById("hubUp");
const hubBar = document.getElementById("hubBar");
const hubWhere = document.getElementById("hubWhere");
const SITE = "Moheet Subudhi";

/* An old link, or one written before the tree grew a level, still resolves: an
   unknown hash falls back to the one node whose own slug matches it. */
function resolvePath(raw) {{
  if (!raw) return "";
  if (raw in FOLDERS || SLUGS.indexOf(raw) > -1) return raw;
  /* Compare last segments, so a node that has since moved up a level resolves
     too: #build/skills still finds skills now that it sits at the root. */
  const tail = raw.split("/").pop();
  const hit = SLUGS.filter(function (s2) {{ return s2.split("/").pop() === tail; }});
  return hit.length === 1 ? hit[0] : "";
}}

/* The heading changes the way ink arrives on paper, not the way a terminal
   types: the old words blur away together, the new ones settle in one after
   another. Typing a word at a time out of nothing read as a glitch at any speed
   fast enough not to be annoying. CSS animations, so a throttled tab still
   lands on the finished state. */
let headTimers = [];
function words(text) {{
  return text.split(" ").map(function (w2, i) {{
    return '<span class="w" style="--d:' + (0.055 * i).toFixed(3) + 's">' +
      w2.replace(/&/g, "&amp;").replace(/</g, "&lt;") + "</span>";
  }}).join(" ");
}}
function setHeading(text, sub, animate) {{
  headTimers.forEach(clearTimeout);
  headTimers = [];
  hubTitle.setAttribute("aria-label", text);
  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const same = hubTitle.textContent.trim() === text;
  const write = function () {{
    hubTitle.innerHTML = words(text);
    hubSub.innerHTML = '<span class="w">' +
      sub.replace(/&/g, "&amp;").replace(/</g, "&lt;") + "</span>";
    hubTitle.classList.remove("out");
    hubSub.classList.remove("out");
  }};
  if (!animate || reduced || same) {{ write(); return; }}
  hubTitle.classList.add("out");
  hubSub.classList.add("out");
  headTimers.push(setTimeout(write, 170));
  /* A backstop for a dropped timer, not a second run: rewriting unconditionally
     replaced the words and started the whole settle again. */
  headTimers.push(setTimeout(function () {{
    if (hubTitle.textContent.trim() !== text) write();
  }}, 700));
}}

let hubPath = "";
function showFolder(path, animate) {{
  hubPath = path;
  const f = FOLDERS[path] || FOLDERS[""];
  setHeading(f.t, f.s, animate);
  hubBar.hidden = !path;
  if (path) {{
    hubUp.textContent = "\u2190 " + (PARENTS[path] ? TITLES[PARENTS[path]] : SITE);
    hubWhere.textContent = TITLES[path];
  }}
  document.title = path ? TITLES[path] + " \u2014 " + SITE : SITE;
  if (q.value.trim()) {{ q.value = ""; }}
  runSearch();
  maybeHint();
}}

function apply(raw, animate) {{
  let path = resolvePath(raw);
  /* A pasted link to a locked node shows the folder it sits in and asks for the PIN. */
  if (path && isLocked(path)) {{
    const lockPath = path;
    path = PARENTS[path] || "";
    try {{ history.replaceState(null, "", path ? "#" + path : location.pathname); }} catch (e) {{}}
    setTimeout(function () {{ openLock(lockPath); }}, 60);
  }}
  const leaf = SLUGS.indexOf(path) > -1 && !(path in FOLDERS);
  document.body.classList.toggle("open", leaf);
  if (q.value.trim()) {{ q.value = ""; runSearch(); }}
  placeSearch(leaf);
  panes.forEach(function (p) {{ p.hidden = p.dataset.pane !== path; }});
  if (leaf) {{
    /* The button beside it already says what it came out of. */
    whereEl.textContent = TITLES[path];
    document.title = TITLES[path] + " \u2014 " + SITE;
    const parent = PARENTS[path] || "";
    backBtn.textContent = "\u2190 " + (parent ? TITLES[parent] : SITE);
    backBtn.dataset.up = parent;
  }} else {{
    whereEl.textContent = "";
    showFolder(path in FOLDERS ? path : "", animate);
  }}
  window.scrollTo(0, 0);
  if (leaf) reveal(document.querySelector('[data-pane="' + path + '"]'));
  /* Tell Google which screen this is: the folder or project, by its title and its #path. */
  if (location.hostname === "moheetsubudhi.com") {{
    gtag("event", "page_view", {{
      page_title: document.title,
      page_location: location.origin + "/" + (path ? "#" + path : "")
    }});
  }}
}}

/* history.pushState throws on file:// and inside some sandboxed previews, which
   would otherwise break every link on the page. Fall back to setting the hash. */
function setUrl(slug) {{
  try {{
    history.pushState(null, "", slug ? "#" + slug : location.pathname + location.search);
  }} catch (e) {{
    if (slug) location.hash = slug;
    else if (location.hash) location.hash = "";
  }}
}}

function go(slug) {{
  if (slug && isLocked(slug)) {{ openLock(slug); return; }}
  const run = function () {{ setUrl(slug); apply(slug, true); }};
  if (document.startViewTransition &&
      !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {{
    try {{ document.startViewTransition(run); }} catch (e) {{ run(); }}
  }} else {{
    run();
  }}
}}
window.addEventListener("hashchange", function () {{
  apply(location.hash.replace("#", ""));
}});

document.querySelectorAll("[data-go]").forEach(function (b) {{
  b.addEventListener("click", function () {{ go(b.dataset.go); }});
}});
backBtn.addEventListener("click", function () {{ go(backBtn.dataset.up || null); }});
hubUp.addEventListener("click", function () {{ go(PARENTS[hubPath] || null); }});
window.addEventListener("popstate", function () {{
  apply(location.hash.replace("#", ""));
}});
document.addEventListener("keydown", function (e) {{
  if (e.key === "Escape" && !scrim.hidden) return;
  if (e.key === "Escape" && document.body.classList.contains("open")) go(null);
}});

/* ---------- reveal on scroll ----------
   A CSS class, not a JavaScript tween: a transition still lands on its final state
   when frames are dropped, so a throttled tab never leaves content invisible. The
   class is only added by script, so with no JavaScript the page is simply visible. */
let io = null;
function reveal(pane) {{
  if (!pane) return;
  const items = pane.querySelectorAll(".view-body > *");
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches ||
      !("IntersectionObserver" in window)) {{
    items.forEach(function (el) {{ el.classList.add("in"); }});
    return;
  }}
  document.documentElement.classList.add("reveal");
  if (io) io.disconnect();
  io = new IntersectionObserver(function (entries) {{
    entries.forEach(function (e) {{
      if (e.isIntersecting || e.boundingClientRect.top < 0) {{
        e.target.classList.add("in");
        io.unobserve(e.target);
      }}
    }});
  }}, {{ rootMargin: "0px 0px -6% 0px" }});
  items.forEach(function (el) {{ el.classList.remove("in"); io.observe(el); }});

  /* Anything already on screen is shown at once rather than waiting for the observer,
     which is delivered on a rendering step and can be throttled. Without this the
     first screenful of an opened view can sit blank. */
  function showOnScreen() {{
    items.forEach(function (el) {{
      if (el.getBoundingClientRect().top < window.innerHeight) el.classList.add("in");
    }});
  }}
  /* Deferred by a frame. Adding the start and end states in one go means the
     browser never sees a change to transition between, which is why nothing moved. */
  if (window.requestAnimationFrame) {{
    requestAnimationFrame(function () {{ requestAnimationFrame(showOnScreen); }});
  }}
  setTimeout(showOnScreen, 220);
  setTimeout(function () {{ items.forEach(function (el) {{ el.classList.add("in"); }}); }}, 2500);
}}

/* ---------- poster scatter ----------
   Positions are measured, not guessed. Eight slots are laid around the title: three
   along the top, one at each side, three along the bottom. If the viewport cannot
   hold them clear of the title, the poster stays a grid instead of overlapping
   itself. Re-run on resize and once the fonts have settled, since both change the
   height of the centre block. */
function layoutScatter() {{
  const wide = window.matchMedia("(min-width: 850px)").matches;
  /* No minimum. A folder holding one thing lays out and drags like a folder
     holding seven; otherwise the page changes its own rules as it fills up. */
  const objsAll = [...hub.querySelectorAll(".obj")].filter(function (o) {{ return !o.hidden; }});
  if (!objsAll.length) {{ hub.classList.remove("scatter"); return; }}
  if (!wide) {{
    hub.classList.remove("scatter"); clearSpots(objsAll); return;
  }}

  hub.classList.add("scatter");
  /* Clamp the field to a band around the title. Anchored to the container edges,
     the objects end up half a screen from the headline on a wide monitor. */
  const H = hub.clientHeight;
  /* Held in around the heading rather than pushed to the edges of the monitor:
     at 1440 the full width put the corner objects a screen away from the title. */
  const band = Math.min(hub.clientWidth * 0.84, 1020);
  const x0 = (hub.clientWidth - band) / 2;
  const W = band;
  const pad = 14;
  const probe = objsAll[0].getBoundingClientRect();
  const ow = probe.width || 132, oh = probe.height || 170;

  /* Measure the headline's text, not its block: .poster-title spans the full width,
     so using its box would always claim there is no room beside it. */
  function textWidth(el) {{
    const rng = document.createRange();
    rng.selectNodeContents(el);
    const r2 = rng.getBoundingClientRect();
    return r2.width || el.getBoundingClientRect().width;
  }}
  const title = document.querySelector(".poster-title").getBoundingClientRect();
  const titleText = textWidth(document.querySelector(".poster-title h1"));
  const search = document.querySelector(".search").getBoundingClientRect();
  const hubTop = hub.getBoundingClientRect().top;
  const centreTop = title.top - hubTop, centreBottom = search.bottom - hubTop;

  const fieldH = Math.min(H, 700);
  const y0 = (H - fieldH) / 2;
  const topY = y0 + pad;
  const botY = y0 + fieldH - oh - pad;
  const roomTop = centreTop - (topY + oh);
  const roomBot = botY - centreBottom;
  if (roomTop < 8 || roomBot < 8) {{ hub.classList.remove("scatter"); clearSpots(objsAll); return; }}

  /* Slots are generated for however many objects exist, so adding one to the tree
     never leaves it stacked on another. Two sit beside the title when it leaves
     room; the rest spread along the top and the bottom. */
  const N = objsAll.length;
  const widest = Math.max(titleText, search.width);
  const useSides = ((W - widest) / 2 - pad * 2) >= ow && N >= 6;
  const spots = [];

  function row(count, y) {{
    if (count <= 0) return;
    const span = W - ow - pad * 2;
    for (let i = 0; i < count; i++) {{
      spots.push([pad + (count > 1 ? (span / (count - 1)) * i : span / 2), y]);
    }}
  }}

  const rest = N - (useSides ? 2 : 0);
  /* One or two sit under the heading rather than above it: a lone object over
     the title reads as a mistake. */
  const topCount = rest <= 2 ? 0 : Math.ceil(rest / 2);
  row(topCount, topY);
  if (useSides) {{
    const midY = Math.max(topY + oh + 8,
      Math.min(centreTop + (centreBottom - centreTop) / 2 - oh / 2, botY - oh - 8));
    spots.push([pad, midY]);
    spots.push([W - ow - pad, midY]);
  }}
  row(rest - topCount, botY);
  objsAll.forEach(function (o, i) {{
    const sp = spots[i] || spots[spots.length - 1];
    o.style.left = Math.round(x0 + sp[0]) + "px";
    o.style.top = Math.round(sp[1]) + "px";
  }});
  if (typeof applyPlaced === "function") applyPlaced();
}}
function clearSpots(list) {{
  list.forEach(function (o) {{ o.style.left = ""; o.style.top = ""; }});
  const live = [...hub.querySelectorAll(".obj")].filter(function (o) {{ return !o.hidden; }});
  const box = hub.querySelector(".objects");
  box.classList.toggle("few", live.length > 0 && live.length < 3);
  box.classList.toggle("many", live.length > 6);
}}

/* ---------- search ----------
   Matches every word typed against each item's title, lede and body text. While a
   search is running the poster drops out of scatter into a grid, because a scatter
   with items removed from it reads as broken rather than filtered. */
const hub = document.getElementById("hub");
const q = document.getElementById("q");
const countEl = document.getElementById("count");
const objs = [...hub.querySelectorAll(".obj")];
const resultsEl = document.getElementById("results");
const searchEl = document.querySelector(".search");
const searchHome = searchEl.parentNode, searchAfter = searchEl.nextSibling;
/* The opened page's own bar. The folder poster has a top bar too, earlier in the page
   and hidden while a page is open, so a bare ".topbar" would pick that one. */
const topbarInner = document.querySelector("#view .topbar .inner");
function placeSearch(open) {{
  const want = open ? topbarInner : searchHome;
  if (searchEl.parentNode === want) return;
  if (open) want.appendChild(searchEl);
  else want.insertBefore(searchEl, searchAfter);
}}

/* Search reaches every node from anywhere, including one nested two levels down,
   and each hit says where it lives, so a name need not be unique on its own.
   Filtering the tiles instead would find almost nothing once most of the page
   sits inside folders. */
const INDEX = objs.map(function (o) {{
  return {{ path: o.dataset.go, find: o.dataset.find,
           label: TITLES[o.dataset.go], where: crumb(PARENTS[o.dataset.go] || "") }};
}});
let shown = [], cursor = 0;

function paint() {{
  resultsEl.querySelectorAll("[data-go]").forEach(function (b, i) {{
    b.classList.toggle("on", i === cursor);
  }});
}}
function open_(path) {{ q.value = ""; runSearch(); go(path); }}

function runSearch() {{
  const terms = q.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
  if (!terms.length) {{
    shown = []; cursor = 0;
    resultsEl.hidden = true;
    resultsEl.innerHTML = "";
    countEl.textContent = "";
    hub.classList.remove("searching");
    objs.forEach(function (o) {{ o.hidden = o.dataset.parent !== hubPath; }});
    layoutScatter();
    return;
  }}
  hub.classList.add("searching");
  /* A hit nearer the front of the indexed text is a more central one: the
     string starts with the label, so a name match sorts above a body match. */
  shown = INDEX.filter(function (it) {{
    return terms.every(function (t) {{ return it.find.indexOf(t) > -1; }});
  }}).sort(function (a, b) {{
    const sc = function (it) {{
      let n2 = 0;
      terms.forEach(function (t) {{ n2 += it.find.indexOf(t); }});
      return n2;
    }};
    return sc(a) - sc(b);
  }}).slice(0, 8);
  cursor = 0;
  countEl.textContent = "";
  resultsEl.hidden = false;
  if (!shown.length) {{
    resultsEl.innerHTML = '<ol><li class="none">' +
      '<span class="say">Not here. Ask me.</span>' +
      '<span class="sub2">Three ways below. I answer.</span>' +
      "</li></ol>";
    return;
  }}
  resultsEl.innerHTML = "<ol>" + shown.map(function (it) {{
    /* Flat children: the name and the trail are both flex items of the row, so
       the trail can be pushed to the far end. Nested in a wrapper they were not. */
    return '<li><button data-go="' + it.path + '"><span class="ico">' +
      (PICS[it.path] || "") + '</span><span class="t">' + it.label + '</span>' +
      (it.where ? '<span class="c">' + it.where + '</span>' : '') +
      '</button></li>';
  }}).join("") + "</ol>";
  resultsEl.querySelectorAll("[data-go]").forEach(function (b) {{
    b.addEventListener("click", function () {{ open_(b.dataset.go); }});
  }});
  paint();
}}
q.addEventListener("input", runSearch);
q.addEventListener("keydown", function (e) {{
  if (e.key === "Escape") {{ q.value = ""; runSearch(); q.blur(); return; }}
  if (!shown.length) return;
  if (e.key === "ArrowDown") {{ e.preventDefault(); cursor = (cursor + 1) % shown.length; paint(); }}
  else if (e.key === "ArrowUp") {{ e.preventDefault(); cursor = (cursor - 1 + shown.length) % shown.length; paint(); }}
  else if (e.key === "Enter") {{ e.preventDefault(); open_(shown[cursor].path); }}
}});
/* "/" anywhere puts the cursor in the box, the way every search field people
   already use behaves. */
document.addEventListener("keydown", function (e) {{
  if (e.key === "/" && document.activeElement !== q) {{ e.preventDefault(); q.focus(); }}
}});

/* Assembled at runtime so the address is not sitting in the markup for scrapers. */
const mail = document.getElementById("mail");
mail.href = "mailto:" + "moheetsubudhi" + "@" + "gmail.com";
document.querySelectorAll(".js-mail").forEach(function (a) {{
  a.href = mail.href; a.textContent = mail.href.slice(7);
}});

/* ---------- accent ----------
   Only the accent moves; paper and ink stay put, so contrast holds whichever is
   picked. Stored per visitor, and a blocked localStorage must not break the page. */
function store(k, v) {{ try {{ localStorage.setItem(k, v); }} catch (e) {{}} }}
function recall(k) {{ try {{ return localStorage.getItem(k); }} catch (e) {{ return null; }} }}

function hexRgb(hex) {{
  const n = parseInt(hex.slice(1), 16);
  return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
}}
function setAccent(hex) {{
  const [r, g, b] = hexRgb(hex);
  const root = document.documentElement.style;
  root.setProperty("--accent", hex);
  root.setProperty("--accent-rgb", r + "," + g + "," + b);
  /* the second tint is the accent lifted toward the paper, so diagrams stay legible */
  const mix = function (c, p) {{ return Math.round(c + (p - c) * 0.52); }};
  const l = [mix(r, 242), mix(g, 238), mix(b, 227)];
  root.setProperty("--accent-2", "rgb(" + l.join(",") + ")");
  root.setProperty("--accent-2-rgb", l.join(","));
  document.querySelectorAll("[data-accent]").forEach(function (b2) {{
    b2.setAttribute("aria-pressed", String(b2.dataset.accent === hex));
  }});
  store("accent", hex);
}}
document.querySelectorAll("[data-accent]").forEach(function (b2) {{
  b2.addEventListener("click", function () {{ setAccent(b2.dataset.accent); }});
}});
const savedAccent = recall("accent");
if (savedAccent && /^#[0-9a-f]{{6}}$/i.test(savedAccent)) setAccent(savedAccent);

/* ---------- dragging the objects ----------
   Pointer events so it works with a mouse, a trackpad and a finger. A press that
   travels under a few pixels is still a click, so opening an item never breaks.
   Positions are remembered, and layoutScatter restores them on the next visit. */
const DRAG_KEY = "spots";
let placed = {{}};
try {{ placed = JSON.parse(recall(DRAG_KEY) || "{{}}") || {{}}; }} catch (e) {{ placed = {{}}; }}

function applyPlaced() {{
  if (!hub.classList.contains("scatter")) return;
  Object.keys(placed).forEach(function (slug) {{
    const el = hub.querySelector('[data-go="' + slug + '"]');
    if (!el || el.hidden) return;
    el.style.left = placed[slug][0] + "px";
    el.style.top = placed[slug][1] + "px";
  }});
}}

document.querySelectorAll(".obj").forEach(function (el) {{
  let sx = 0, sy = 0, ox = 0, oy = 0, moved = false, id = null;

  el.addEventListener("pointerdown", function (e) {{
    if (!hub.classList.contains("scatter") || e.button) return;
    id = e.pointerId; moved = false;
    sx = e.clientX; sy = e.clientY;
    ox = parseFloat(el.style.left) || el.offsetLeft;
    oy = parseFloat(el.style.top) || el.offsetTop;
    el.setPointerCapture(id);
  }});

  el.addEventListener("pointermove", function (e) {{
    if (id === null || e.pointerId !== id) return;
    const dx = e.clientX - sx, dy = e.clientY - sy;
    if (!moved && Math.abs(dx) + Math.abs(dy) < 5) return;   /* still a click */
    moved = true;
    el.classList.add("dragging");
    const w = hub.clientWidth - el.offsetWidth, h = hub.clientHeight - el.offsetHeight;
    const nx = Math.max(0, Math.min(w, ox + dx));
    const ny = Math.max(0, Math.min(h, oy + dy));
    el.style.left = nx + "px";
    el.style.top = ny + "px";
    placed[el.dataset.go] = [Math.round(nx), Math.round(ny)];
  }});

  function end(e) {{
    if (id === null || (e && e.pointerId !== id)) return;
    try {{ el.releasePointerCapture(id); }} catch (e2) {{}}
    id = null;
    if (moved) {{
      el.classList.remove("dragging");
      store(DRAG_KEY, JSON.stringify(placed));
      resetBtn.hidden = false;
      dismissHint();
    }}
  }}
  el.addEventListener("pointerup", end);
  el.addEventListener("pointercancel", end);

  /* a drag must not also open the item */
  el.addEventListener("click", function (e) {{
    if (moved) {{ e.stopImmediatePropagation(); e.preventDefault(); moved = false; }}
  }}, true);
}});

/* The nudge shows once, only where dragging is possible, and only to someone who
   has not already moved something. It leaves as soon as they do. */
const dragHint = document.getElementById("dragHint");
let hintTimer = null;
function maybeHint() {{
  const canDrag = hub.classList.contains("scatter");
  if (!canDrag) {{ dragHint.hidden = true; return; }}
  if (dragHint.dataset.gone) return;
  dragHint.hidden = false;
  clearTimeout(hintTimer);
  hintTimer = setTimeout(dismissHint, 7000);
}}
function dismissHint() {{
  if (dragHint.hidden) return;
  dragHint.dataset.gone = "1";
  dragHint.classList.add("gone");
  setTimeout(function () {{ dragHint.hidden = true; dragHint.classList.remove("gone"); }}, 400);
}}

const resetBtn = document.getElementById("resetSpots");
resetBtn.hidden = !Object.keys(placed).length;
resetBtn.addEventListener("click", function () {{
  placed = {{}};
  store(DRAG_KEY, "{{}}");
  hub.querySelectorAll(".obj").forEach(function (o) {{ o.style.left = ""; o.style.top = ""; }});
  layoutScatter();
  resetBtn.hidden = true;
}});

/* ---------- the opening ----------
   The objects settle into place once, when the poster first loads. Added by script
   after the positions are set, so nothing animates from the wrong spot, and never
   on the way back from an opened item. The class is only ever added here, so with
   no JavaScript the objects are simply there. */
function playOpening() {{
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  const objs2 = [...hub.querySelectorAll(".obj")].filter(function (o) {{ return !o.hidden; }});
  objs2.forEach(function (o, i) {{ o.style.setProperty("--d", (0.04 + i * 0.055) + "s"); }});
  document.documentElement.classList.add("anim");
  /* Drop the class once it has played, so a later relayout does not replay it. */
  setTimeout(function () {{ document.documentElement.classList.remove("anim"); }}, 1400);
}}

apply(location.hash.replace("#", ""));
maybeHint();
playOpening();
window.addEventListener("resize", function () {{ layoutScatter(); maybeHint(); }});
if (document.fonts && document.fonts.ready) {{
  document.fonts.ready.then(layoutScatter);
}}

</script>
</body></html>
"""
    (HERE / "index.html").write_text(page, encoding="utf-8")
    print(f"wrote index.html  {len(page):,} bytes  ·  {len(V)} views  ·  {len(c['souls'])} soul files")


if __name__ == "__main__":
    build()

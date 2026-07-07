---
name: funloom-minigame-maker
description: Create or adapt lightweight HTML/CSS/JavaScript minigames for the Funloom/002 interactive video minigame node. Use when the user wants a ZIP that can be uploaded to the 002 minigame resource, needs an existing web game adapted to return success/failure or explicitly declared custom result states, or asks to validate/package a Funloom-compatible minigame.
---

# Funloom Minigame Maker

## Overview

Use this skill to create, adapt, validate, and package lightweight web minigames for the Funloom/002 interactive video minigame node.

The minigame must run inside the 002/player iframe. Default to the basic return states `success` and `failure`. If the creator genuinely needs advanced multi-outcome behavior, first help them define the exact custom result ids, labels, trigger conditions, and story semantics. The minigame must not read or write story variables; variables are configured by the creator in the 002 minigame node.

## Required Workflow

Before generating or adapting code, establish these decisions with the user. Ask directly when missing; if the user wants you to proceed quickly, choose the default and state it.

1. Determine task type:
   - `create`: build a new minigame from a gameplay idea.
   - `adapt`: modify existing web game source or ZIP to support the Funloom protocol.
   - `validate`: inspect and fix an existing minigame package.
2. Determine asset mode:
   - `multi-file ZIP` by default.
   - `single-file HTML` only for simple games without many assets.
   - `user assets` when the user supplies images, audio, video, or existing source files.
3. Lock return states:
   - Default to basic mode with `success` and `failure`.
   - Success must be a concrete event such as score target, cleared rounds, survived time, or correct answer count.
   - Failure must be a concrete event such as lives reaching 0, time expiring, wrong answers reaching a limit, or game-over.
   - Do not invent extra result states by default.
   - If the user asks for advanced outcomes, help them confirm each custom state before implementation:
     - result id, using only ASCII letters, numbers, `_`, or `-` (for example `perfect`);
     - creator-facing label (for example `完美通关`);
     - exact trigger condition in game code;
     - story meaning and expected 002 node exit.
4. Lock controls and screen posture:
   - PC must support mouse and/or keyboard.
   - mobile mini-program WebView must support touch controls.
   - Default to responsive portrait/landscape support.
   - Suggest forced landscape only when the gameplay would be much worse otherwise, and document that choice.
5. Build or adapt the minigame.
6. Validate with `scripts/validate_minigame.py`.
7. Package with `scripts/package_minigame.py`.
8. Tell the user to upload the ZIP to the 002 interactive video tool and test through a real minigame node.

Do not create a local host simulator or `test-host.html`. Opening `index.html` directly can check whether the game itself runs, but it is not proof that the 002 node integration works.

## Protocol Rules

Every minigame must include a one-shot completion helper:

```js
const FUNLOOM_ALLOWED_RESULTS = ["success", "failure"];
let funloomCompleted = false;

function completeFunloomMinigame(result) {
  if (funloomCompleted) return;
  if (!FUNLOOM_ALLOWED_RESULTS.includes(result)) return;
  funloomCompleted = true;
  parent.postMessage({
    type: "funloom:minigame:complete",
    result
  }, "*");
}
```

For basic mode, call `completeFunloomMinigame("success")` on success and `completeFunloomMinigame("failure")` on failure.

For advanced mode, only after the creator confirms custom states, add those ids to `FUNLOOM_ALLOWED_RESULTS` and call them from their exact trigger paths. Example:

```js
const FUNLOOM_ALLOWED_RESULTS = ["success", "failure", "perfect"];

if (score >= targetScore && mistakes === 0) {
  completeFunloomMinigame("perfect");
}
```

Do not use fuzzy matching, Chinese result ids, or undeclared result names.

Read `references/protocol.md` when adapting protocol code or debugging completion behavior.

## Packaging Rules

The upload ZIP must contain `index.html` at the ZIP root. Do not wrap the game in an extra parent folder inside the ZIP.

The game must be self-contained:

- Use relative paths for local files.
- Do not depend on external CDN scripts, remote images, remote fonts, or remote APIs.
- Avoid `localStorage` as required state; iframe sandbox behavior may vary.
- Keep total ZIP size under 50 MB.
- Prefer ASCII file names for generated assets. Existing Chinese file names are allowed if all references are relative and validated.

Read `references/zip-rules.md` when preparing ZIPs or fixing resource paths.

## Templates

Use templates as starting points, not as final products unless the user asks for a simple sample.

- `assets/templates/vanilla-minigame`: multi-file starter with adapter, PC click/touch support, lives, timer, and score.
- `assets/templates/quiz-minigame`: single-file quiz starter.
- `assets/templates/action-minigame`: single-file movement/avoidance starter with keyboard and touch buttons.

For new games, copy the closest template into the user's requested output/source directory, then customize gameplay, visuals, success/failure thresholds, and copy.

For existing games, preserve original gameplay and assets where possible. Add only the minimum protocol adapter and mobile/iframe fixes needed for 002 compatibility.

Read `references/game-design.md` for gameplay defaults and dual-end guidance. Read `references/adapting-existing-games.md` for existing-source adaptation.

## Scripts

Validate a source directory or ZIP:

```bash
python scripts/validate_minigame.py path/to/game-or-zip
```

Validate an advanced package with creator-confirmed result ids:

```bash
python scripts/validate_minigame.py path/to/game-or-zip --results success,failure,perfect
```

Package a source directory:

```bash
python scripts/package_minigame.py path/to/source --name my-game --output output
```

Package an advanced source directory:

```bash
python scripts/package_minigame.py path/to/source --name my-game --output output --results success,failure,perfect
```

The package script writes:

- `output/<game-name>.zip`
- `output/source/`
- `output/INTEGRATION.md`

Run validation again on the produced ZIP before delivering it.

## Final Response Requirements

When delivering a minigame ZIP or adapted source, report:

- ZIP path.
- Source path.
- Declared result states and their meanings.
- Success condition.
- Failure condition.
- Custom result conditions, if advanced mode was requested.
- PC controls.
- mobile controls.
- whether forced landscape is used.
- validation command and result.
- 002 testing steps: upload resource, select it in a minigame node, configure variable mutations for declared results, connect every declared exit, and play from an option node. If custom results are used, tell the creator to switch the minigame node to advanced mode and add the exact custom result ids and labels first.

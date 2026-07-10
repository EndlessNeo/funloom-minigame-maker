---
name: funloom-minigame-maker
description: Create or adapt lightweight HTML/CSS/JavaScript minigames for the Funloom interactive story creator tool's minigame node. Use when the user wants a ZIP that can be uploaded as a Funloom minigame resource, needs an existing web game adapted to return basic success/failure or creator-confirmed advanced custom result states, or asks to validate/package a Funloom-compatible minigame.
---

# Funloom Minigame Maker

## Overview

Use this skill to create, adapt, validate, and package lightweight web minigames for the Funloom interactive story creator tool's minigame node.

The minigame must run inside the Funloom player iframe and report one final result through `parent.postMessage({ type: "funloom:minigame:complete", result }, "*")`. It must not read or write story variables; the creator configures variable mutations and branch exits in the Funloom minigame node.

## Conversation Rules

- Keep design approval in the chat. Do not write a separate proposal `.md` file and ask the user to open a path to confirm it.
- Do not offer or use a browser visual companion, local URL mockup, `test-host.html`, or visual preview page as the planning/approval step.
- Before writing game code, show a concise chat proposal and ask the user to confirm or edit it. Include:
  - task type: create, adapt, or validate;
  - gameplay summary;
  - asset mode: multi-file ZIP, single-file HTML, or supplied assets;
  - result mode and exact result ids/labels/trigger conditions;
  - PC and mobile controls;
  - 互动影游形态：横屏影游或竖屏影游；
  - output directory.
- When the interaction video shape is not clear, ask exactly: “您所需要设计的互动影游是横屏影游还是竖屏影游？这会涉及到后边小游戏的呈现方式。”
- Do not ask users with internal terms such as `landscape`, `portrait`, `playback orientation`, or “项目播放方向”. Map 横屏影游 to the internal `landscape` package option and 竖屏影游 to the internal `portrait` package option.
- Ask only for the interactive video's 横屏影游/竖屏影游 shape. Do not propose a per-minigame forced-orientation override; Funloom minigame nodes inherit the interactive video's shape.
- Ask for an output directory in chat. If the user has no preference, recommend:
  - Windows: `%USERPROFILE%\FunloomMinigames\<game-slug>`
  - macOS/Linux: `~/FunloomMinigames/<game-slug>`
  Use the user's custom path if provided.

## Return-State Rules

Basic mode:

- Use exactly `success` and `failure`.
- Success must map to a concrete event such as score target, cleared rounds, survived time, or enough correct answers.
- Failure must map to a concrete event such as lives reaching 0, time expiring before target, wrong answers reaching a limit, or game over.

Advanced mode:

- Use only the custom result ids confirmed by the creator.
- Do not automatically include `success` or `failure` in advanced mode.
- Confirm each advanced result before implementation:
  - result id, ASCII letters, numbers, `_`, or `-` only, for example `perfect`;
  - creator-facing label, for example `完美通关`;
  - exact trigger condition in game code;
  - story meaning and expected Funloom minigame node exit.
- Do not invent undeclared result states by default. Do not use Chinese result ids. Do not fuzzy-match result names.

## Protocol Rules

Every minigame must include a one-shot completion helper.

Basic example:

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

Advanced example after creator confirmation:

```js
const FUNLOOM_ALLOWED_RESULTS = ["perfect", "timeout"];
```

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

For new games, copy the closest template into the confirmed output/source directory, then customize gameplay, visuals, result triggers, and copy.

For existing games, preserve original gameplay and assets where possible. Add only the minimum protocol adapter and mobile/iframe fixes needed for Funloom compatibility.

Read `references/game-design.md` for gameplay defaults. Read `references/adapting-existing-games.md` for existing-source adaptation.

## Scripts

Validate a basic source directory or ZIP:

```bash
python scripts/validate_minigame.py path/to/game-or-zip
```

Validate an advanced package with creator-confirmed custom result ids:

```bash
python scripts/validate_minigame.py path/to/game-or-zip --results perfect,timeout
```

Package a basic source directory:

```bash
python scripts/package_minigame.py path/to/source --name my-game --output output --orientation landscape
```

Package an advanced source directory:

```bash
python scripts/package_minigame.py path/to/source --name my-game --output output --orientation portrait --results perfect,timeout
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
- Result mode: basic or advanced.
- Declared result ids, labels, trigger conditions, and story meanings.
- PC controls.
- Mobile controls.
- 互动影游形态：横屏影游或竖屏影游.
- Validation command and result.
- Funloom testing steps:
  - upload the ZIP to minigame resources;
  - select it in a minigame node;
  - keep basic mode for `success` / `failure`, or switch the node to advanced mode and define the complete custom result id and label set first;
  - configure variable mutations for declared results;
  - connect every declared exit;
  - playtest every result path from an option node.

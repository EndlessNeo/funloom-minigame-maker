---
name: funloom-minigame-maker
description: Create, adapt, validate, and package lightweight HTML/CSS/JavaScript minigames for the Funloom interactive story creator tool's minigame node. Use when the user wants a Funloom-compatible ZIP minigame, needs an existing web game adapted to return success/failure or creator-confirmed custom result states, or asks to validate/package a Funloom minigame.
---

# Funloom Minigame Maker

Use this skill to build or adapt self-contained web minigames that can be uploaded to the Funloom interactive story creator tool.

## Workflow

Before writing or changing code, establish these decisions:

1. Task type:
   - `create`: build a new minigame from a gameplay idea.
   - `adapt`: modify existing web game source or ZIP to support the Funloom protocol.
   - `validate`: inspect and fix an existing minigame package.
2. Asset mode:
   - Prefer multi-file ZIP for real games.
   - Use single-file HTML only for small samples.
   - Preserve supplied assets when adapting existing games.
3. Return states:
   - Default to basic mode: `success` and `failure`.
   - Do not invent custom states.
   - If the creator asks for advanced outcomes, confirm each custom result id, label, trigger condition, and story meaning first.
4. Controls:
   - Support mouse or keyboard on PC.
   - Support touch controls in mobile WebView.
   - Default to responsive portrait/landscape layout.

## Protocol

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

For basic mode, call `completeFunloomMinigame("success")` and `completeFunloomMinigame("failure")` from concrete game-end paths.

For advanced mode, only after creator confirmation, add exact custom ids:

```js
const FUNLOOM_ALLOWED_RESULTS = ["success", "failure", "perfect"];

if (score >= targetScore && mistakes === 0) {
  completeFunloomMinigame("perfect");
}
```

Never use fuzzy matching, Chinese result ids, or undeclared result names. The minigame returns only the result string; story variables and plot exits are configured in the Funloom minigame node.

## Bundled Resources

- Read `references/protocol.md` when adapting completion behavior.
- Read `references/zip-rules.md` before packaging or fixing resource paths.
- Read `references/game-design.md` for default success/failure design.
- Read `references/adapting-existing-games.md` when modifying existing game code.
- Use `assets/templates/vanilla-minigame`, `quiz-minigame`, or `action-minigame` as starting points.

## Scripts

Validate source or ZIP:

```bash
python scripts/validate_minigame.py path/to/game-or-zip
```

Validate advanced results:

```bash
python scripts/validate_minigame.py path/to/game-or-zip --results success,failure,perfect
```

Package source:

```bash
python scripts/package_minigame.py path/to/source --name my-game --output output
```

Package advanced source:

```bash
python scripts/package_minigame.py path/to/source --name my-game --output output --results success,failure,perfect
```

The package script writes `output/<game-name>.zip`, `output/source/`, and `output/INTEGRATION.md`.

## Delivery

When delivering a minigame, report:

- ZIP path.
- Source path.
- Declared result ids and meanings.
- Success and failure conditions.
- Custom result conditions, if any.
- PC and mobile controls.
- Whether forced landscape is used.
- Validation command and result.
- Funloom testing steps: upload ZIP, select it in a minigame node, configure variables for declared results, connect every declared exit, and playtest every result.

# Funloom Minigame Protocol

This shared reference defines the minigame behavior that all adapters in this repository must preserve.

## Result Contract

A Funloom minigame reports one final result to the host player:

```js
parent.postMessage({
  type: "funloom:minigame:complete",
  result: "success"
}, "*");
```

Default basic results:

- `success`: the player cleared the minigame.
- `failure`: the player failed the minigame.

Advanced results are allowed only when the creator explicitly asks for them and confirms:

- result id, using ASCII letters, numbers, `_`, or `-`, such as `perfect`;
- creator-facing label, such as `完美通关`;
- exact trigger condition in game code;
- story meaning and expected Funloom minigame node exit.

Never invent custom result ids automatically. Never fuzzy-match result ids. Never use Chinese result ids.

## Variable Boundary

The minigame returns only a result string. It must not read, write, or assume story variables.

Creators configure variable mutations and plot exits on the Funloom minigame node:

1. Upload the ZIP as a minigame resource.
2. Select the resource in a minigame node.
3. Keep basic mode for `success` and `failure`, or switch to advanced mode and add creator-confirmed custom ids.
4. Configure variable mutations for each declared result that needs them.
5. Connect every declared result exit before publishing.

## ZIP Rules

- ZIP root must contain `index.html`.
- Do not wrap the game in an extra parent folder.
- Use relative local paths.
- Do not depend on remote scripts, fonts, images, or APIs.
- Keep total package size under 50 MB.
- Prefer ASCII file names for generated assets.

## Validation

Use the bundled validator whenever possible:

```bash
python scripts/validate_minigame.py path/to/game-or-zip
```

For advanced results:

```bash
python scripts/validate_minigame.py path/to/game-or-zip --results success,failure,perfect
```

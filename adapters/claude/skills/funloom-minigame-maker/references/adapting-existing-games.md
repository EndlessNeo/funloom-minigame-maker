# Adapting Existing Games

## Preserve First

Keep the original game structure, visuals, and gameplay whenever possible. Add only what is needed for Funloom compatibility:

- one-shot completion helper,
- result calls for the confirmed basic or advanced mode,
- relative resource paths,
- mobile controls if missing,
- iframe responsive sizing.

## Find Existing Outcomes

Trace the existing game logic:

- win screen,
- level complete,
- score target,
- game over,
- lives,
- timer,
- wrong-answer counter,
- rank or special clear state.

For basic mode, wire the original success path to `completeFunloomMinigame("success")` and the original failure path to `completeFunloomMinigame("failure")`.

For advanced mode, do not keep `success` or `failure` automatically. Ask the creator to confirm every custom result id, display label, trigger condition, and story meaning, then wire only those confirmed ids.

## Common Fixes

- Replace absolute local paths with relative paths.
- Remove remote CDN dependencies or inline/download the needed code.
- Avoid `window.top` access.
- Avoid popups and navigation away from `index.html`.
- Make keyboard-only interactions available through touch buttons.
- Keep audio optional and user-gesture friendly.

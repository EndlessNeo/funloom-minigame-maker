# Adapting Existing Games

## Preserve first

Keep the original game structure, visuals, and gameplay whenever possible. Add only what is needed for Funloom compatibility:

- one-shot completion helper,
- calls to return `success` and `failure` by default,
- relative resource paths,
- mobile controls if missing,
- iframe responsive sizing.

## Find existing outcomes

Trace the existing game logic:

- win screen,
- level complete,
- score target,
- game over,
- lives,
- timer,
- wrong-answer counter.

Wire the original success path to `completeFunloomMinigame("success")` and the original failure path to `completeFunloomMinigame("failure")`.

If the existing game has meaningful extra outcomes, such as perfect clear, timeout, draw, rank, or special loss, do not choose result ids automatically. Ask the creator whether they want the 002 node in advanced mode. If yes, confirm each custom result id, display label, trigger condition, and story meaning before changing the code.

## Common fixes

- Replace absolute local paths with relative paths.
- Remove remote CDN dependencies or inline/download the needed code.
- Avoid `window.top` access.
- Avoid popups and navigation away from `index.html`.
- Make keyboard-only interactions available through touch buttons.
- Keep audio optional and user-gesture friendly.

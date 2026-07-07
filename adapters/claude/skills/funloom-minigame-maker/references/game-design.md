# Minigame Design Defaults

## Return-state design

Default to clear binary outcomes:

- Score target: success at `score >= target`.
- Round target: success after `clearedRounds >= target`.
- Survival: success after `timeLeft <= 0` while still alive.
- Quiz: success after enough correct answers.
- Failure: lives reach 0, mistakes reach limit, time expires without target, or explicit game over.

If the user does not provide thresholds, choose a short testable target and state it.

Only propose advanced custom results when the game design genuinely has more than two meaningful outcomes, or when the creator asks for them. Before implementing custom results, confirm:

- result id: ASCII letters, numbers, `_`, or `-` only, such as `perfect`;
- display label: creator-facing text in Funloom, such as `完美通关`;
- trigger condition: exact code condition that returns this id;
- story meaning: what branch or variable changes this state is meant to drive.

Do not create custom result ids just because a game has score tiers; simple scores can remain internal UI unless the creator wants separate story exits.

## Dual-end controls

PC:

- Keyboard is fine, but do not make it the only control when mobile is required.
- Mouse click/tap targets should be large enough.

Mobile mini-program WebView:

- Support touch controls.
- Avoid hover-only UI.
- Avoid tiny buttons.
- Avoid right-click and file download flows.
- Keep all important UI inside the iframe viewport.

## Orientation

Default to responsive layout that works in portrait and landscape.

Use forced landscape only when it materially improves the game, such as horizontal runners, wide battle lanes, or precision movement games. If forced landscape is used, add a visible in-game prompt and mention it in delivery notes.

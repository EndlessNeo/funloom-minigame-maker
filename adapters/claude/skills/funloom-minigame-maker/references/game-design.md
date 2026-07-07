# Minigame Design Defaults

## Return-State Design

Use basic mode when the game only needs two story outcomes:

- Score target: `success` at `score >= target`.
- Round target: `success` after `clearedRounds >= target`.
- Survival: `success` after the required duration while still alive.
- Quiz: `success` after enough correct answers.
- Failure: lives reach 0, mistakes reach a limit, time expires without target, or explicit game over.

If the user does not provide thresholds, choose a short testable target and state it in the chat proposal.

Use advanced mode only when the creator explicitly wants custom story exits. Before implementing custom results, confirm:

- result id: ASCII letters, numbers, `_`, or `-` only, such as `perfect`;
- display label: creator-facing text in Funloom, such as `完美通关`;
- trigger condition: exact code condition that returns this id;
- story meaning: what branch or variable changes this state is meant to drive.

Advanced mode uses only the confirmed custom ids. Do not add `success` or `failure` unless the creator explicitly chooses those ids as custom advanced exits.

Do not create custom result ids just because a game has score tiers; simple scores can remain internal UI unless the creator wants separate story exits.

## Dual-End Controls

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

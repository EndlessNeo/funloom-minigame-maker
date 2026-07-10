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

## Interactive Video Shape

Confirm the interactive video's shape before implementation. If it is not clear from the current project or user request, ask exactly:

> 您所需要设计的互动影游是横屏影游还是竖屏影游？这会涉及到后边小游戏的呈现方式。

- 横屏影游：design the primary experience for a 16:9 horizontal stage. It must work on PC and on mobile when the user holds the phone horizontally.
- 竖屏影游：design the primary experience for a 9:16 vertical stage. It must work in the mobile mini-program vertical stage and remain centered when previewed on wider screens.

The minigame must inherit the Funloom interactive video's shape. Do not add a per-minigame forced orientation or an in-game rotate prompt by default.

Templates should still be fluid inside the iframe because the platform supplies the actual stage size. If the requested gameplay conflicts with the confirmed interactive video shape, pause and suggest a gameplay adjustment before writing code; for example, turn a wide runner into lane taps, quick decisions, or a compact vertical dodge game for a 竖屏影游.

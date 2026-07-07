# Funloom Minigame Protocol

## Contract

The minigame only reports the final result to the host player:

```js
parent.postMessage({
  type: "funloom:minigame:complete",
  result: "success"
}, "*");
```

By default, `result` is `success` or `failure`.

In advanced mode, the creator may declare additional result ids on the 002 minigame node, such as `perfect`. Only use custom ids after the creator confirms their exact spelling, display label, trigger condition, and story meaning.

The minigame must not read, mutate, or assume story variables. The 002 creator configures variable mutations on the minigame node.

## One-shot helper

Always use a helper that prevents repeated completion:

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

Use it from game logic:

```js
if (score >= targetScore) completeFunloomMinigame("success");
if (lives <= 0) completeFunloomMinigame("failure");
```

For creator-confirmed advanced results, add the declared ids:

```js
const FUNLOOM_ALLOWED_RESULTS = ["success", "failure", "perfect"];

if (score >= targetScore && mistakes === 0) {
  completeFunloomMinigame("perfect");
}
```

## What not to do

- Do not send undeclared custom result names.
- Do not use Chinese result ids; use Chinese only for the creator-facing label in the 002 node.
- Do not infer or fuzzy-match result ids.
- Do not send multiple results.
- Do not call platform APIs.
- Do not require the parent frame to send game state.
- Do not treat directly opening `index.html` as integration proof.

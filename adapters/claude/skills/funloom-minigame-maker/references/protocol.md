# Funloom Minigame Protocol

## Contract

The minigame only reports one final result to the host player:

```js
parent.postMessage({
  type: "funloom:minigame:complete",
  result: "success"
}, "*");
```

The minigame must not read, mutate, or assume story variables. The creator configures variable mutations and plot exits on the Funloom minigame node.

## Result Modes

Basic mode uses exactly:

- `success`
- `failure`

Advanced mode uses only the complete custom result id set the creator confirms and declares on the Funloom minigame node. Do not automatically include `success` or `failure` in advanced mode.

Advanced result ids must use ASCII letters, numbers, `_`, or `-`. Chinese text belongs in the creator-facing label, not in the result id.

## One-Shot Helper

Always use a helper that prevents repeated completion.

Basic:

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

Advanced after creator confirmation:

```js
const FUNLOOM_ALLOWED_RESULTS = ["perfect", "timeout"];

if (score >= targetScore && mistakes === 0) {
  completeFunloomMinigame("perfect");
}
```

## What Not To Do

- Do not send undeclared custom result names.
- Do not mix basic results into advanced mode unless the creator explicitly declares them as custom advanced results.
- Do not use Chinese result ids.
- Do not infer or fuzzy-match result ids.
- Do not send multiple results.
- Do not call platform APIs.
- Do not require the parent frame to send game state.
- Do not treat directly opening `index.html` as integration proof.

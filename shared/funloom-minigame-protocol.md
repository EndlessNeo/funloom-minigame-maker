# Funloom Minigame Protocol Summary

Funloom minigames are self-contained HTML/CSS/JavaScript games uploaded as ZIP resources. The ZIP root must contain `index.html`.

The game reports exactly one final result to the Funloom player iframe:

```js
parent.postMessage({
  type: "funloom:minigame:complete",
  result
}, "*");
```

Use a one-shot helper so the game cannot emit multiple final results.

## Result Modes

Basic mode:

- `success`
- `failure`

Advanced mode:

- Use only creator-confirmed custom result ids.
- Do not automatically include `success` or `failure`.
- Result ids must use ASCII letters, numbers, `_`, or `-`.
- Chinese text belongs in the creator-facing label inside the Funloom minigame node.

The minigame source only returns result ids. Story variables, mutations, labels, and branch exits are configured in the Funloom minigame node.

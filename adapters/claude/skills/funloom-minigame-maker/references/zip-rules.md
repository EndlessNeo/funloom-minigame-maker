# ZIP Rules

## Required Shape

The ZIP root must contain `index.html`.

Good:

```text
index.html
style.css
main.js
assets/player.png
```

Bad:

```text
my-game/index.html
my-game/style.css
```

## Resource Rules

- Keep all resources inside the ZIP.
- Use relative paths such as `./style.css`, `main.js`, `assets/player.png`.
- Do not use external `http://` or `https://` resources.
- Do not use CDN scripts or remote fonts.
- Keep package size under 50 MB.
- Prefer ASCII file names for generated files.
- Existing Chinese file names are acceptable when references are relative and validation passes.

## Delivery Rule

The real integration test is uploading the ZIP to the Funloom interactive story creator tool:

1. Open the Funloom interactive story creator tool.
2. Upload the ZIP in the minigame resources area.
3. Create or select a minigame node.
4. Select the uploaded resource.
5. For basic mode, keep the default `success` and `failure` exits.
6. For advanced mode, switch the node to advanced mode and declare the complete custom result id and label set confirmed in chat.
7. Configure variable mutations for every declared result that needs them.
8. Connect every declared result exit before publishing to Funloom.
9. Enter the minigame from an option node and verify every declared result path.

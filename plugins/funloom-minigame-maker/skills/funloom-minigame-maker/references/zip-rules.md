# ZIP Rules

## Required shape

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

## Resource rules

- Keep all resources inside the ZIP.
- Use relative paths such as `./style.css`, `main.js`, `assets/player.png`.
- Do not use external `http://` or `https://` resources.
- Do not use CDN scripts or remote fonts.
- Keep package size under 50 MB.
- Prefer ASCII file names for generated files.
- Existing Chinese file names are acceptable when references are relative and validation passes.

## Delivery rule

The real integration test is uploading the ZIP to 002:

1. Open 002 interactive video tool.
2. Upload ZIP in `资源 > 小游戏`.
3. Create or select a minigame node.
4. Select the uploaded resource.
5. Configure variable mutations for the declared result states.
6. Connect every declared exit. Basic mode has `success` and `failure`; advanced mode also needs each custom id, such as `perfect`.
7. Enter the minigame from an option node and verify both branches.

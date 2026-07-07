# Funloom Minigame Maker

Codex plugin marketplace for `funloom-minigame-maker`, a skill that creates, adapts, validates, and packages ZIP minigames for the Funloom/002 minigame node.

The skill defaults to the basic `success` / `failure` node exits. If a creator truly needs advanced outcomes, it first helps define custom result ids, labels, trigger conditions, and story meanings before generating code.

## Contents

```text
.agents/plugins/marketplace.json
plugins/funloom-minigame-maker/.codex-plugin/plugin.json
plugins/funloom-minigame-maker/skills/funloom-minigame-maker/
```

## Try Locally On Windows

PowerShell may block `codex.ps1`, so use `cmd /c`:

```powershell
cmd /c codex plugin marketplace add E:\KuranGameAI\funloom-minigame-maker-plugin-repo
cmd /c codex plugin add funloom-minigame-maker@funloom-codex
```

Start a new Codex thread after installing, then try:

```text
Use $funloom-minigame-maker to create a simple click-target minigame ZIP for the 002 minigame node.
```

## Publish To GitHub

Create an empty GitHub repository first, then run from this folder:

```powershell
git init
git add .
git commit -m "Publish Funloom minigame maker plugin"
git branch -M main
git remote add origin https://github.com/<OWNER>/<REPO>.git
git push -u origin main
```

Optional release tag:

```powershell
git tag v0.1.0
git push origin v0.1.0
```

## Install From GitHub

After the repo is public or accessible to the installer:

```powershell
cmd /c codex plugin marketplace add <OWNER>/<REPO> --ref main
cmd /c codex plugin add funloom-minigame-maker@funloom-codex
```

HTTPS and SSH Git sources are also supported by the Codex CLI:

```powershell
cmd /c codex plugin marketplace add https://github.com/<OWNER>/<REPO> --ref main
```

## Update Installed Copies

After pushing updates to GitHub:

```powershell
cmd /c codex plugin marketplace upgrade funloom-codex
cmd /c codex plugin add funloom-minigame-maker@funloom-codex
```

Start a new Codex thread so the updated skill instructions are loaded.

## Maintainer Checklist

- Update `plugins/funloom-minigame-maker/.codex-plugin/plugin.json` version.
- Update the skill files under `plugins/funloom-minigame-maker/skills/funloom-minigame-maker/`.
- Run the validation commands from the skill's `SKILL.md`.
- Commit, push, and tag a release when useful.
- Tell users to run `codex plugin marketplace upgrade funloom-codex`.

## License

Choose and add a license before broad public distribution. MIT is a common choice for small tooling plugins, but the repository owner should make that decision.

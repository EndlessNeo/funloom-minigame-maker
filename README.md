# Funloom Minigame Maker

面向 Funloom 互动影游创作者工具的小游戏制作助手，用来生成、改造、检查和打包可上传到小游戏节点的网页小游戏 ZIP。

当前仓库提供三种适配：

| 平台 | 形态 | 入口 |
| --- | --- | --- |
| Codex | 插件，内含 skill | `$funloom-minigame-maker` |
| Claude Code | Agent Skill | 自然语言触发或明确要求使用该 skill |
| Cursor | Project Rule | 复制 `.mdc` 规则到项目 `.cursor/rules` |

## 它能做什么

- 根据玩法想法生成轻量 HTML/CSS/JavaScript 小游戏。
- 把已有网页小游戏改造成 Funloom 小游戏节点可接入的 ZIP。
- 检查小游戏包结构，确认 ZIP 根目录包含 `index.html`。
- 检查小游戏是否发送 Funloom 完成消息。
- 打包源码、ZIP 和接入说明。
- 在需要进阶返回状态时，先帮你确认字段、显示名、触发条件和剧情语义；进阶版返回状态完全自定义，不自动包含 `success` / `failure`。

## 返回状态

小游戏结束时只向 Funloom 返回一个结果值。剧情变量变化和后续剧情出口不写在小游戏源码里，而是在 Funloom 互动影游创作者工具的小游戏节点上配置。

普通版默认只有两个返回状态：

| 返回值 id | 显示含义 |
| --- | --- |
| `success` | 成功 |
| `failure` | 失败 |

进阶版使用完全自定义返回状态，不沿用 `success` / `failure` 后再补状态，而是从 0 开始声明这一版小游戏的完整返回状态集合，例如：

| 返回值 id | 显示含义 | 常见触发条件 |
| --- | --- | --- |
| `perfect` | 完美通关 | 达成目标且没有失误 |
| `timeout` | 超时 | 时间耗尽 |
| `draw` | 平局 | 双方条件相同 |

进阶版返回值需要你和 AI 助手先作为完整集合确认清楚，插件或规则不会自动替你发明新的状态。推荐格式是英文、数字、下划线或短横线，例如 `perfect_clear`、`timeout`、`bad_end`。

## 在 Funloom 里怎么配置

1. 使用 Codex、Claude 或 Cursor 生成/改造小游戏 ZIP。
2. 打开 Funloom 互动影游创作者工具，把 ZIP 上传到小游戏资源。
3. 在剧情画布里创建或选择一个小游戏节点。
4. 选择刚上传的小游戏资源。
5. 如果只需要成功/失败，保持普通版即可。
6. 如果需要 `perfect` 这类自定义结果，把小游戏节点切到进阶版，并声明完整一致的返回值 id 和显示名；进阶版不会自动包含 `success` / `failure`。
7. 给每个返回状态配置需要改变的剧情变量。
8. 把每个已声明返回状态的出口连接到后续剧情节点。
9. 在试玩里分别触发每个返回状态，确认能走到预期剧情。

发布到 Funloom 前，请确保所有已声明的返回状态都有后续连线。试玩阶段可以先警告，但正式发布时未连线出口会阻断上传。

## 安装到 Codex

在 Windows PowerShell 里如果 `codex.ps1` 被执行策略拦截，可以使用 `cmd /c`：

```powershell
cmd /c codex plugin marketplace add EndlessNeo/funloom-minigame-maker --ref main
cmd /c codex plugin add funloom-minigame-maker@funloom-codex
```

安装后开启一个新的 Codex 对话，让插件说明被重新加载。

Codex 使用示例：

```text
$funloom-minigame-maker 帮我做一个 30 秒内找线索的小游戏，普通版成功/失败两个出口。
```

## 安装到 Claude Code

Claude 适配位于：

```text
adapters/claude/skills/funloom-minigame-maker
```

安装为当前用户可用的 Claude Skill：

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills"
Copy-Item -Recurse adapters\claude\skills\funloom-minigame-maker "$env:USERPROFILE\.claude\skills\"
```

安装为某个项目专用的 Claude Skill：

```powershell
New-Item -ItemType Directory -Force .claude\skills
Copy-Item -Recurse adapters\claude\skills\funloom-minigame-maker .claude\skills\
```

安装后重启 Claude Code 或开启新会话，然后尝试：

```text
请使用 funloom-minigame-maker skill，帮我做一个普通版成功/失败的 Funloom 小游戏 ZIP。
```

## 安装到 Cursor

Cursor 适配位于：

```text
adapters/cursor/.cursor/rules/funloom-minigame-maker.mdc
```

复制到你正在制作小游戏的项目：

```powershell
New-Item -ItemType Directory -Force .cursor\rules
Copy-Item adapters\cursor\.cursor\rules\funloom-minigame-maker.mdc .cursor\rules\
```

然后在 Cursor 里提出需求，例如：

```text
请按 Funloom Minigame Maker 规则，把这个网页小游戏改成可上传到 Funloom 的 ZIP。
```

## 更新

Codex 已安装用户更新：

```powershell
cmd /c codex plugin marketplace upgrade funloom-codex
cmd /c codex plugin add funloom-minigame-maker@funloom-codex
```

Claude 用户重新复制 `adapters/claude/skills/funloom-minigame-maker` 到 `.claude/skills`。

Cursor 用户重新复制 `adapters/cursor/.cursor/rules/funloom-minigame-maker.mdc` 到目标项目 `.cursor/rules`。

更新后建议开启一个新的 AI 对话。

## 仓库结构

```text
plugins/funloom-minigame-maker/          Codex 插件
adapters/claude/skills/funloom-minigame-maker/
                                         Claude Skill
adapters/cursor/.cursor/rules/           Cursor Project Rule
shared/                                  三平台共同遵守的协议摘要
```

## 注意事项

- ZIP 根目录必须直接包含 `index.html`。
- 小游戏源码只负责返回结果值，不直接修改剧情变量。
- 返回状态 id 要和 Funloom 小游戏节点里声明的 id 完全一致。
- 未声明的返回值不会自动创建出口。
- 使用进阶版时，先设计好每个返回状态的剧情意义，再让 AI 助手写入小游戏逻辑。

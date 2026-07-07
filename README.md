# Funloom Minigame Maker

面向 Funloom 互动影游创作者工具的 Codex 插件，用来生成、改造、检查和打包可上传到小游戏节点的网页小游戏 ZIP。

它适合已经在做互动影游的创作者：你告诉 Codex 想要什么玩法、成功失败条件、是否需要特殊通关状态，插件会帮你产出可上传的小游戏包，并给出在 Funloom 里如何配置节点出口和变量变化的说明。

## 它能做什么

- 根据玩法想法生成轻量 HTML/CSS/JavaScript 小游戏。
- 把已有网页小游戏改造成 Funloom 小游戏节点可接入的 ZIP。
- 检查小游戏包结构，确认 ZIP 根目录包含 `index.html`。
- 检查小游戏是否发送 Funloom 完成消息。
- 打包源码、ZIP 和接入说明。
- 在需要进阶返回状态时，先帮你确认字段、显示名、触发条件和剧情语义。

## 返回状态

小游戏结束时只向 Funloom 返回一个结果值。剧情变量变化和后续剧情出口不写在小游戏源码里，而是在 Funloom 互动影游创作者工具的小游戏节点上配置。

普通版默认只有两个返回状态：

| 返回值 id | 显示含义 |
| --- | --- |
| `success` | 成功 |
| `failure` | 失败 |

进阶版可以追加自定义返回状态，例如：

| 返回值 id | 显示含义 | 常见触发条件 |
| --- | --- | --- |
| `perfect` | 完美通关 | 达成目标且没有失误 |
| `timeout` | 超时 | 时间耗尽 |
| `draw` | 平局 | 双方条件相同 |

自定义返回值需要你和 Codex 先确认清楚，插件不会自动替你发明新的状态。推荐格式是英文、数字、下划线或短横线，例如 `perfect_clear`、`timeout`、`bad_end`。

## 在 Funloom 里怎么配置

1. 在 Codex 里使用 `$funloom-minigame-maker` 生成或改造小游戏 ZIP。
2. 打开 Funloom 互动影游创作者工具，把 ZIP 上传到小游戏资源。
3. 在剧情画布里创建或选择一个小游戏节点。
4. 选择刚上传的小游戏资源。
5. 如果只需要成功/失败，保持普通版即可。
6. 如果需要 `perfect` 这类额外结果，把小游戏节点切到进阶版，并添加完全一致的返回值 id 和显示名。
7. 给每个返回状态配置需要改变的剧情变量。
8. 把每个已声明返回状态的出口连接到后续剧情节点。
9. 在试玩里分别触发每个返回状态，确认能走到预期剧情。

发布到 Funloom 前，请确保所有已声明的返回状态都有后续连线。试玩阶段可以先警告，但正式发布时未连线出口会阻断上传。

## 安装

在 Windows PowerShell 里如果 `codex.ps1` 被执行策略拦截，可以使用 `cmd /c`：

```powershell
cmd /c codex plugin marketplace add EndlessNeo/funloom-minigame-maker --ref main
cmd /c codex plugin add funloom-minigame-maker@funloom-codex
```

安装后开启一个新的 Codex 对话，让插件说明被重新加载。

## 使用示例

```text
$funloom-minigame-maker 帮我做一个 30 秒内找线索的小游戏，普通版成功/失败两个出口。
```

```text
$funloom-minigame-maker 把这个网页小游戏改成能上传到 Funloom 互动影游创作者工具的 ZIP。
```

```text
$funloom-minigame-maker 我需要 success、failure、perfect 三个返回状态，帮我确认字段语义并生成小游戏。
```

## 更新

插件作者发布更新后，已安装用户可以运行：

```powershell
cmd /c codex plugin marketplace upgrade funloom-codex
cmd /c codex plugin add funloom-minigame-maker@funloom-codex
```

更新后同样建议开启一个新的 Codex 对话。

## 注意事项

- ZIP 根目录必须直接包含 `index.html`。
- 小游戏源码只负责返回结果值，不直接修改剧情变量。
- 返回状态 id 要和 Funloom 小游戏节点里声明的 id 完全一致。
- 未声明的返回值不会自动创建出口。
- 使用进阶版时，先设计好每个返回状态的剧情意义，再让插件写入小游戏逻辑。

# Codex 英文文章发布包

状态：已于 2026-09-24 发布到 @LeoGuoLabs。

正式链接：https://x.com/LeoGuoLabs/status/2102969238323597775

发布核验与 X 排版适配见 published.md。

## 标题

Codex: A Practical Guide to Getting Real Work Done

## 副标题

Start with one useful task. Give the agent context and clear boundaries. Verify what it delivers.

## 引导短帖

Getting useful work out of Codex starts with a clear brief: the outcome, context, boundaries, and proof of success.

I put together a practical guide to the first task, project instructions, tools, and verification.

## 正文

使用 article.md。article.html 是离线图文预览，包含目录、全部文字、可复制的提示词与命令、四张概念配图和三张带英文标注的真实截图。点击图片可放大，再选择 Actual size 查看细节。文章从当前 Markdown 重新生成，保留已有正文改动。

## 图片顺序与 ALT

1. images/01-cover.png — 文章开头封面。
   ALT: Editorial illustration of an engineering desk with a laptop, task brief, verification checklist and software block. Title: Codex, a practical field guide. Define the work. Let it run. Verify the result. LeoGuoLabs.
2. images/05-codex-workspace-annotated.png — 第 2 节，第一段后。
   ALT: Author-provided Codex workspace screenshot with five numbered English callouts: projects and tools; project, location and branch; task prompt; permissions; model and reasoning. Full access and the model shown are the author's current selections.
3. images/02-task-brief.png — 第 3 节，提示词模板前。
   ALT: Four parts of a Codex task brief: outcome, context, boundaries and acceptance. Each card asks a concrete question, followed by a three-stage path: inspect, build, verify.
4. images/06-codex-active-task-annotated.png — 第 3 节，结尾。
   ALT: Author-provided screenshot of an active Codex task with four English callouts identifying the brief, visible progress, inspection tools, and the composer and stop control. The note says that progress is not proof of completion.
5. images/04-workspaces.png — 第 5 节，Local、Worktree、Cloud 说明后。
   ALT: Local uses the current checkout, Worktree uses a separate Git working directory, and Cloud uses a remote execution environment. A note explains that a worktree is not a security sandbox. Plan, Goal and Schedule are distinguished along the bottom.
6. images/07-codex-settings-annotated.png — 第 5 节，权限说明后。
   ALT: Author-provided Codex General settings screenshot with four English callouts: permission modes, the Personalization sidebar entry, the projectless task folder, and terminal and sleep preferences. The original toggle states remain visible.
7. images/03-toolbox.png — 第 6 节，术语说明后。
   ALT: Six concepts and their jobs: a model reasons, an agent uses tools, a skill packages a repeatable workflow, MCP connects tools and data, a plugin bundles capabilities, and a CLI runs from a terminal.

四张概念图由内置 ImageGen 新生成，1536 × 1024，提示词见 image-prompts.json。三张截图由用户于 2026-09-24 手工提供，使用内置 ImageGen 添加英文编号、说明框和箭头；标注提示词见 screenshot-prompts.json。未修改原始截图文件，3840 × 2100 原图在 screenshots/originals/，正文含查看原图链接。标注版是用于教学的编辑副本，原图用于核对界面细节。

## 编辑边界

- 此稿按完整长文准备，未假设账号已开通 X Article 发布权限。
- 示例练习与示例验收报告均在正文明确标注，不能改写成作者已经完成的实测结果。
- 已核对官方说明及本机 CLI 帮助；没有实际安装软件、修改 Codex 设置、执行示例任务或部署代码。
- 原文读取、改编与事实修订记录见 editorial-notes.md；研究快照不属于对外发布素材。
- 2026-09-24 已补入用户提供的三张真实本机截图；不再需要通过受限制的应用截图接口获取。

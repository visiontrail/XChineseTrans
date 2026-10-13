# GitHub: From First Commit to Verified Delivery

这是一篇完整的 LeoGuoLabs 英文图文稿，共 15 节，约 4,600 词正文（不含代码和表格），配 7 张新制作或新截取的图片。

## 从这里开始

- `article.html`：排版完成的离线阅读版。正文图片和未编辑的仓库截图已嵌入文件，支持目录跳转、图片放大和手机阅读。
- `article.md`：可继续编辑的英文 Markdown 稿。
- `article.txt`：保留段落、代码、表格内容和参考链接的纯文本稿。
- `images/`：按正文顺序编号的七张 PNG 配图。
- `alt-text.md`：对应的英文 ALT 文本与图注。
- `companion/field-notes/`：可复制出来练习的静态网页项目，包含链接检查器和 Actions 工作流。
- `diagrams/`：两张概念图的 HTML、SVG 和结构化源文件。HTML 支持深浅色切换及图片导出。
- `screenshots/originals/`：四张在这台电脑上、通过 Codex 内置浏览器重新截取的原始网页截图。
- `image-prompts.json`：内置 ImageGen 的封面、截图标注及校正提示词。

## 配图顺序

| 图 | 内容 | 性质 |
|---|---|---|
| 01 | GitHub: From First Commit to Verified Delivery | 全新概念封面，内置 ImageGen 生成 |
| 02 | Where your work lives | 原创 SVG 概念图，导出 PNG |
| 03 | Read a repository with purpose | 本机新截图，加 AI 辅助英文标注；原图另存 |
| 04 | GitHub Code Search | 本机新截图，未编辑 |
| 05 | Flask PR 文件差异 | 本机新截图，未编辑 |
| 06 | A change needs evidence at every handoff | 原创 SVG 流程图，导出 PNG |
| 07 | GitHub Pages 网址类型 | 本机新截图，未编辑 |

## 验证范围

文章的新增技术说明和套餐数据已对照官方资料核查，正文保留直接参考链接。核查日期为 2026-09-27。

练习项目在临时本地仓库中完成 35 条命令检查：正常页面检查通过；缺失文件、错误锚点和根路径三个故障样例均按预期失败；分支、暂存与取消暂存、提交、向本地裸仓库推送和 revert 的结果符合预期。

图文页已在桌面和 390px 窄屏中检查：7 张图片加载、15 个章节、目录锚点、图片放大与关闭、原始截图入口均正常，页面没有横向溢出，宽表格和代码在各自区域滚动。

交付的是文章与本地练习素材。没有创建 GitHub 仓库、运行托管 Actions、部署公共 Pages 或发布 X 内容。

## 编辑与使用

优先编辑 Markdown 正文。编辑后的稿件与 HTML、纯文本和图注需要同步更新。图片 01 为封面，02–07 为正文配图；图 03 的生成式标注版本用于教学阅读，精确界面细节以 `screenshots/originals/01-repository.png` 为准。

将完整目录解压到一个位置后，Markdown 中的相对图片路径可正常解析。`article.html` 可以单独移动和打开，正文图片不依赖网络。官方参考链接需要联网访问。

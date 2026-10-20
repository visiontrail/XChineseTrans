# 首版后的修复记录

首版已于检查前保存为 `first-complete-artifacts.tar.gz`，SHA-256 见 `first-result-manifest.json`。`artifacts/` 是实际交付版本。

## R02 — 响应式布局修复

- 原因：390 px 手机宽度下，Neptune 标题与资料面板中的装饰缩略图重叠；见 `checks/mobile-neptune-before-fix.jpg`。
- 修改：650 px 及以下隐藏资料面板的重复缩略图，仍保留主场景和行星选择器中的天体图形。
- 原因：1280 × 720 较矮桌面视口下，资料面板固定高度不足，底部提示和下一站按钮被裁切。
- 修改：桌面场景最小高度从 485 px 增至 585 px，让面板完整显示；移动端已有独立高度规则。
- 影响文件：`artifacts/styles.css`。提示词、行星数据、JavaScript 交互逻辑未修改。
- 追加用户提示：无。修复来自基本浏览器检查。

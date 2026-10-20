# 基本检查

## 静态与入口

- `node --check app.js`：退出 0。
- HTML 引用的 `styles.css`、`app.js` 均存在；无重复 HTML ID。
- 本地 HTTP 服务 `http://127.0.0.1:8766/` 返回 200，Codex 内置浏览器成功加载网页。
- ZIP 完整性检查通过，包含 index.html、styles.css、app.js、README.md。

## 实际浏览器观察

- 逐个选择全部八颗行星，资料标题均与所选行星一致，见 `planet-selection.json`。
- 在场景中点击太阳，资料面板显示 Sun。
- Neptune 的“Next stop”循环到 Mercury；键盘右箭头从 Mercury 切至 Venus。
- 暂停后模拟时钟在两次 UI 观察间保持 `YEAR 00 · DAY 007`；恢复后推进到 `YEAR 00 · DAY 012`。
- 时间滑块 End 将速度改为 `180 days / sec`。
- 切换 Top down，aria-pressed 显示选中；缩放按钮显示 115%；Labels 开关变为未按下。
- 拖动场景后各行星的屏幕位置改变，实际截图可见视角变化。
- About 弹窗可打开和关闭；重置返回 Earth、100% 缩放、20 days / sec、Perspective 和启用标签及轨道。
- 390 × 844 手机视口下无横向溢出（clientWidth = scrollWidth = 390），修复后 Neptune 名称完整显示，见 `mobile-390.jpg`。
- 1280 × 720 桌面视口修复后面板 clientHeight = scrollHeight = 473，下一站按钮完整位于面板内。
- 默认桌面布局截图见 `desktop.jpg`；DOM 见 `desktop-dom.txt`。
- 应用 console warn/error 读取为空。

## 未测试与检查工具限制

- 真实触摸设备上的双指缩放、完整跨浏览器兼容性、天文数值逐项独立核验：未测试。
- 本作品明确使用示意比例、圆形轨道和艺术初始位置，不宣称星历或物理仿真精度。
- 内置浏览器只允许 HTTP/HTTPS，直接导航 file:// 被浏览器 URL 安全策略拒绝；未尝试绕过。网页启动与交互通过既有本地 HTTP 地址验证；直接双击离线文件未通过自动化实测。
- 一次读取视口的检查脚本访问不可用的 window.screen，得到 TypeError；改用允许的 DOM 尺寸读取，应用本身未因此修改。
- 首版后的布局修复见 ../revisions.md，首次代码仍保存在 ../first-complete-artifacts.tar.gz。

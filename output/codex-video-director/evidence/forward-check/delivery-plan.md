# 下一步交付计划

当前只完成预制作，下一步按以下顺序形成真正可审阅的工程与MP4：

1. 实现按帧渲染源文件和布局配置。首轮只渲染0、36、147、204、258、288、359帧，检查竖屏构图、杯形辨识、衬线字与安全区。
2. 渲染3.0–6.8秒和8.6–9.6秒短片段，查看轮廓成形与品牌显现的速度。按可见缺陷修改形状、时间或字号，保留必要的修订记录。
3. 渲染全部360帧，输出`half-pause-coffee.mp4`。固定白底、黑字/轮廓、1080×1920、30fps、H.264/yuv420p，无音频流。
4. 使用Skill的`check_delivery.py`读取**最终MP4**并对照timeline，检查全部360帧解码、12秒和30fps。该脚本只报告分辨率/音频流，不会自动把本manifest中的画幅或静音意图作为断言，因此另明确核对1080×1920和`audio_present=false`。
5. 实际播放首尾并拖动定位；查看品牌完整停留到末帧。无音轨无需响度目标或音频听感验收。记录播放器与实际完成的覆盖范围。
6. 交付最终MP4及包含源码、配置、timeline、依赖说明、重现命令和验证记录的可编辑工程包。只打包需要重现和审阅的文件，区分工作帧、候选导出和最终导出。

后续检查命令计划：

```bash
python3 /Users/leoguo/.codex/skills/video-director/scripts/check_delivery.py half-pause-coffee.mp4 --timeline timeline.json --out evidence --extract
```

还必须检查该命令生成的`delivery-check.json`中`width==1080`、`height==1920`、`audio_present==false`。不能把本次timeline结构有效写成成片有效。

交付为本地文件。没有发布、上传或外部联系计划。

# 实现选择

## 选择：Python + Pillow → PNG帧序列 → FFmpeg

这是2D文字和几何轮廓片，不需要三维、浏览器、生成式视频、外部素材或付费服务。Pillow可绘制椭圆、圆弧、线段和排版；把每帧的几何状态直接写成`state_at_frame(frame, timeline)`。FFmpeg把确定的360帧编码成MP4。

当前已核实可用：Python3.14.4、Pillow12.2.0、FFmpeg8.1.1、ffprobe，以及`/System/Library/Fonts/Supplemental/Baskerville.ttc`。未安装软件，未访问外部服务。

## 计划中的可编辑工程

```text
project/
  timeline.json          # 唯一时间定义，当前已准备
  film_config.json       # 文字、黑白颜色、布局、字形路径
  render.py              # 逐帧绘制入口
  scene.py               # 几何与按帧状态函数
  requirements.txt       # Pillow==12.2.0
  README.md              # 渲染命令、系统字体依赖、交付说明
  evidence/              # 最终MP4探测与真实视觉审查
```

当前只完成时间定义与实现方案；上列代码文件尚未实现，不把该目录示意当作已经完成的可编辑工程。

按2倍工作分辨率绘制后下采样，以减少弧线和衬线字的锯齿。使用统一缓动函数，在`timeline.json`事件之间计算0–1进度；不依赖系统时间、播放历史或每帧累积。首帧就放置完整主句；文字只做短距离位移。杯身可由参数曲线采样为线段，按弧长推进显示，避免等参数步长导致快慢不均。

所有黑白图形由本项目代码生成。字体作为本机依赖在README中注明，不把系统字体复制进工程包；跨平台复现时由使用者提供可用字形，并重新检查排版。

## 计划中的编码命令

以下是实现后执行的计划，**本次没有执行**：

```bash
python3 render.py --timeline timeline.json --frames build/frames
ffmpeg -framerate 30 -i build/frames/%04d.png -frames:v 360 -an -c:v libx264 -crf 18 -pix_fmt yuv420p -movflags +faststart half-pause-coffee.mp4
```

渲染脚本将命令中的帧率和帧数从timeline读取，避免保存第二份可漂移的时间表。`-an`确保没有音频流，不能用一个全零WAV冒充“无声音”。

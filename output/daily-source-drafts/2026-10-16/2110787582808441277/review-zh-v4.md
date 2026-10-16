# Muse Spark Open v3 审核

格式：原生 Quote Post，引用 https://x.com/AIatMeta/status/2110779754274292212 ，原帖媒体保留在引用内，不额外上传。

来源：@dotey https://x.com/dotey/status/2110787582808441277

本轮反馈：Sentinel_7eb5d706936c819197e1fa9f49cb4438 要求简明解释并加入正文；Sentinel_877312c0951081919bfd2905a00d6e75 要求补充官方推荐部署硬件。保留先前指定删除建议段的修改。当前待审，未发布。

中文对照：
Muse Spark Open 发布了：总参数8160亿，每个token激活420亿，上下文100万token。它可以读取文字、图片、视频和音频，输出文字。

部署时值得注意的是内存。“420亿激活参数”说的是处理一个token时动用哪些参数，并不意味着整个模型只需要420亿参数模型的下载体积或内存。

Meta列出的显存门槛是：NVFP4至少700GB，BF16为2TB。NVFP4是NVIDIA推出的省内存4位格式，BF16是常见的16位格式。官方部署示例分别使用4张NVIDIA B300和8张B300。

苹果设备也有部署路线。Meta表示针对两台M5 Ultra Mac Studio做了优化，每台512GB统一内存，通过Thunderbolt 5连接。它们用MLX，也就是苹果面向自家芯片的AI运行框架，加载的同样是NVFP4版本。权重格式与运行软件是两回事。

权重采用Muse Model License，包含商用条件。附原官方模型卡及许可证链接。

核验：
- https://huggingface.co/meta-models/Muse-Spark-Open-816B-A42B ：700GB/2TB门槛，双M5 Ultra优化说法
- https://dev.meta.ai/docs/muse-spark-open/get-the-model ：4×B300 NVFP4与8×B300 BF16官方部署示例；不是所有场景通用最低GPU张数
- https://dev.meta.ai/docs/muse-spark-open/deploy ：MLX也加载NVFP4；双M5 Ultra每台512GB，或四台每台256GB；Thunderbolt 5互联。正文选双机方案以保持简短
- https://dev.meta.ai/docs/muse-spark-open ：还列AMD与Intel等生态，不概括成只支持NVIDIA/Apple
- https://ml-explore.github.io/mlx/build/html/index.html ：MLX框架定义
- https://developer.nvidia.com/blog/introducing-nvfp4-for-efficient-and-accurate-low-precision-inference/ ：NVFP4定义，4位数值另有缩放元数据，正文为简明解释

未把模型卡的700GB/2TB显存数字套到Mac统一内存，也未宣称给定配置保证所有上下文长度与并发。超过280字符，发布前核对实际权限。媒体沿用v2已核验原生引用方案。

## v4 成本补充（2026-10-16）
用户 Sentinel_a70a18b45bcc8191b929292df7e82a45 要求附加硬件成本估算。
新增正文中文：按10月16日核验，Gatewell的8卡B300整机公开估价每台57.7万–73.5万美元，但最少5台起订，最终价格取决于配置。税费、机房设施和运行费用另计预算；不能把4卡方案算成8卡价格的一半。Apple表示512GB M5 Ultra版10月下旬上市，尚未核实该配置官方价格，因此暂无法可靠给出双机预算。

证据与口径：
- https://gatewellusa.com/ai-compute/p/nvidia-hgx-b300-8gpu ：直接打开页面，10月12日发布估价$577,100–735,000/完整8U整机，含8卡B300，CPU/内存/存储/电源按配置；最少5台起订，非单台零售成交保证，也非NVIDIA官方定价。5台最小批次机器估价$2,885,500–3,675,000，仅用于说明MOQ影响，不写成用户需要买5台。
- https://www.apple.com/newsroom/2026/08/apple-introduces-new-mac-studio-with-m5-max-and-m5-ultra/ ：512GB版10月下旬上市；$5,499是M5 Ultra基础款起价，不能当512GB型号价格，未用它乘2冒充预算。
- https://www.apple.com/shop/buy-mac/mac-studio ：搜索所读官方商品正文同样显示512GB选项10月下旬推出；当前可读取配置页未给该选项可核实价格。最低SSD配置与完整512GB机器价格尚不可确认，不猜测。
- https://www.wiredzone.com/shop/product/10034109-supermicro-sys-822gs-nb3rt-01-g2-hgx-b300-8-gpu-system-16806 ：搜索索引显示$524,626，但直接打开当前显示Email For Price，因此没有把该索引价格写为当前价格。其960GB启动盘也不足存放约1.65TB BF16权重，须额外存储。
- 没找到可核实4卡B300完整机器采购报价；租赁价与推算单卡价不冒充采购价。未联系卖方、未填写询价或购买。
- 本预算为硬件市场参考，并非相同性能或吞吐比较，也不是完整落地总成本或最低可运行成本。保持v3原生Quote与已删除建议段不变，仍待审核。

### v4追加用户允许的上一代价格参考
用户消息 Sentinel_667654a04f948191b7f68378810b0332：“苹果的Mac可以参考上一代的”。因此以Apple官方官翻M3 Ultra作为价格锚，替换原v4苹果无法估价段。这里不是M5实际报价、不宣称同等性能或已验证M3运行本模型。
https://www.apple.com/shop/product/g1ce8ll/a 直接打开于2026-10-16：32核CPU、80核GPU、512GB统一内存、2TB SSD，Apple Certified Refurbished，USD14,869；2台×14,869=29,738，正文约US$30k，税和Thunderbolt互联线材另计，库存有限未保证可买2台。完整机器报价，非内存升级差价。Apple原512GB M5 Ultra10月下旬上市信息保留。
正文新增中文：以苹果上一代官翻机作预算参照：M3 Ultra、512GB内存、2TB SSD每台14,869美元，两台约3万美元，税和线材另算。这是上一代官翻价格，不是M5报价或性能比较。

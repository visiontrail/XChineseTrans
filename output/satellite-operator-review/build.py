"""Build four source-linked, self-contained Chinese satellite diagrams."""
from pathlib import Path
from html import escape
import json

OUT = Path(__file__).resolve().parent
PAPER, INK, MUTED, GOLD, TINT = '#FDFBF7', '#1A4A3A', '#426454', '#80601B', '#F6EDCF'
FONT = "'Geist','Inter','PingFang SC','Microsoft YaHei',sans-serif"
CSS = f"""*{{box-sizing:border-box}}body{{margin:0;background:{PAPER};color:{INK};font-family:{FONT}}}
main{{max-width:1408px;min-width:0;margin:auto;padding:32px 24px 64px}}
h1{{font-size:32px;font-weight:600;margin:16px 0}}h2{{font-size:23px;font-weight:600}}p,li{{font-size:17px;line-height:1.8}}a{{color:{INK};text-underline-offset:4px}}nav{{display:flex;gap:20px;flex-wrap:wrap;margin:20px 0 32px}}
.diagram-container{{width:100%;overflow-x:auto;margin:16px 0 28px}}svg{{width:100%;min-width:1280px;display:block}}
svg text{{font-family:{FONT};fill:{INK}}}.muted{{fill:{MUTED}}}.gold{{fill:{GOLD}}}
.evidence{{max-width:1120px;margin:0 auto 48px;padding:12px 0;border-top:1px solid #CCD6CD}}.evidence p{{margin:8px 0}}.kicker{{font-size:14px;letter-spacing:1px;color:{MUTED}}}
.sources{{font-size:15px}}.sources li{{font-size:15px}}.source-url{{display:block;font-size:13px;overflow-wrap:anywhere;color:{MUTED}}}section{{scroll-margin-top:16px}}.note{{color:{MUTED}}}
@media(max-width:600px){{main{{padding:20px 16px}}h1{{font-size:27px}}}}
@media print{{main{{padding:0}}.diagram-container{{overflow-x:visible;break-inside:avoid}}svg{{min-width:0}}nav{{display:none}}section{{break-before:page}}}}
"""

def txt(x,y,s,size=20,weight=400,color=INK,anchor='start'):
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{color}" text-anchor="{anchor}" style="fill:{color}">{escape(s)}</text>'

def lines(x,y,ss,size=20,gap=29,color=MUTED,weight=400,anchor='start'):
    return ''.join(txt(x,y+i*gap,s,size,weight,color,anchor) for i,s in enumerate(ss))

def rect(x,y,w,h,fill=PAPER,stroke='none',rx=0,attr=''):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" rx="{rx}" {attr}/>'

def line(x1,y1,x2,y2,color=MUTED,width=1.5,arrow=False):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"'+(' marker-end="url(#arr)"' if arrow else '')+'/>'

def elbow(x1,y1,x2,y2,mid,color=MUTED):
    if y1==y2:return line(x1,y1,x2,y2,color,1.5,True)
    sign=1 if y2>y1 else -1
    d=f'M{x1},{y1} H{mid-8} Q{mid},{y1} {mid},{y1+sign*8} V{y2-sign*8} Q{mid},{y2} {mid+8},{y2} H{x2}'
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="1.5" marker-end="url(#arr)"/>'

def label(x,y,s,w=96):
    return rect(x,y,w,24)+txt(x+w/2,y+18,s,16,500,MUTED,'middle')

def node(x,y,w,h,title,body=(),framed=False,focal=False):
    a=f'<g data-node="{escape(title)}">'+rect(x,y,w,h,TINT if focal else PAPER,GOLD if focal else (MUTED if framed else 'none'),0)
    a+=txt(x+20,y+36,title,24,600)
    a+=lines(x+20,y+68,body,18,27)
    return a+'</g>'

def base(slug,n,title,subtitle,body,footer):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" role="img" aria-labelledby="{slug}-title {slug}-desc">
<title id="{slug}-title">{escape(title)}</title><desc id="{slug}-desc">{escape(subtitle)}</desc>
<defs><marker id="arr" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 Z" fill="{MUTED}"/></marker><filter id="grain"><feTurbulence type="fractalNoise" baseFrequency=".82" numOctaves="3" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter></defs>
{rect(0,0,1280,720)}{rect(0,0,1280,720,INK,attr='filter="url(#grain)" opacity=".018"')}
{txt(64,44,f'手机直连卫星 / {n:02d}',16,500,MUTED)}{txt(64,100,title,40,600)}
{txt(64,140,subtitle,20,400,MUTED)}{line(64,164,1216,164,'#CCD6CD',1)}
{body}{line(64,674,1216,674,'#CCD6CD',1)}{txt(64,702,footer,14,400,MUTED)}{txt(1216,702,'LeoGuoLabs',16,500,INK,'end')}
</svg>'''

SOURCES = [
('S1','2026 年政府工作报告','https://www.moe.gov.cn/jyb_xwfb/xw_zt/moe_357/2026/2026_zt03/baogao/202603/t20260314_1430876.html'),
('S2','工信部：向中国联通颁发卫星移动通信业务经营许可（2025-09-08）','https://wap.miit.gov.cn/xwfb/gxdt/sjdt/art/2025/art_ea54d95b58fc49a3be5315c7ddc2fac0.html'),
('S3','工信部：向中国移动颁发卫星移动通信业务经营许可（2025-09-29）','https://www.miit.gov.cn/xwfb/gxdt/sjdt/art/2025/art_a6f24798ae08410d9b4cb3126c319d19.html'),
('S4','中国电信：天通直连卫星系统规模应用（2025-11-10）','https://www.chinatelecom.com.cn/ct/news/jtxw/162457.html'),
('S5','中国电信：三星 S25 Ultra 与中科晶上天通芯片（2025-02-11）','https://www.chinatelecom.com.cn/ct/news/jtxw/152975.html'),
('S6','中国电信：小米 15 Ultra 卫星数据与图片业务（2025-02-28）','https://www.chinatelecom.com.cn/ct/news/jtxw/152980.html'),
('S7','北斗官方：2019 年系统发展报告，区域与全球短报文能力','https://www.beidou.gov.cn/xt/gfxz/201912/P020191227337020425733.pdf'),
('S8','华为：北斗卫星消息操作类常见问题','https://consumer.huawei.com/cn/support/content/zh-cn15986536/'),
('S9','中国联通：ESG 社会报告，低轨窄带物联卫星','https://www.chinaunicom.com.hk/sc/esg/social.php'),
('S10','中国联通：董事长报告书，天通与北斗服务上线','https://www.chinaunicom.com.hk/sc/about/chairman.php'),
('S11','工信部：垣信试验星与中国移动 02 星发射（2026-06-09）','https://wap.miit.gov.cn/jgsj/wgj/gzdt/art/2026/art_047c93af39774b978f0a21cf420b9568.html'),
('S12','中国移动：2024 年半年度报告摘要，01 星与星核验证星','https://www.chinamobileltd.com/en/file/view.php?id=300969'),
('S13','ITU-R M.2177-0：NR-NTN 与 IoT-NTN（2026-02）','https://www.itu.int/epublications/publication/recommendation-itu-r-m-2177-0-02-2026-detailed-specifications-of-the-satellite-radio-interfaces-of-international-mobile-telecommunications-2020-imt-2020'),
('S14','Ericsson：透明转发与再生载荷架构','https://www.ericsson.com/en/blog/2024/10/ntn-payload-architecture'),
('S15','中国电信：2024 MWC 上海，回顾 2023 年 9 月业务发布','https://www.chinatelecom.com.cn/ct/news/jtxw/152882.html'),
]

figs=[]
# 01 / Three service paths. Equal ranks, not an evolution ladder.
b=''.join(txt(x,192,s,16,500,MUTED) for x,s in [(84,'兼容终端'),(468,'接入系统'),(948,'业务形态')])
for y in [208,352,496]:
    b+=line(312,y+56,448,y+56,arrow=True)+line(752,y+56,920,y+56,arrow=True)
rows=[
 ('天通兼容终端',['手机／车载等形态','需支持对应卫星功能'],'天通卫星系统',['GEO 高轨 · 约 3.6 万公里'],'语音与短信',['部分机型可传压缩图片']),
 ('北斗消息终端',['支持定位，不等于','支持短报文通信'],'北斗短报文',['区域与全球服务能力有别'],'报平安与位置消息',['长度以终端和业务为准']),
 ('匹配体制的终端',['频段、射频与协议','都要与网络兼容'],'3GPP NTN',['IoT-NTN 与 NR-NTN'],'物联或宽带数据',['能力取决于具体网络设计'])]
for y,r in zip([208,352,496],rows):
    b+=node(64,y,248,116,r[0],r[1])+node(448,y,304,116,r[2],r[3],True)+node(920,y,296,116,r[4],r[5])
b+=txt(64,650,'轨道高低、空口体制和业务能力，需要分别判断。低轨组网不等于任意手机都能宽带直连。',18,500,GOLD)
figs.append(('01-service-routes','三类业务入口，先看能力边界',base('01-service-routes',1,'三类业务入口，先看能力边界','天通、北斗与蜂窝 NTN 可以并存；它们不是一条从低级到高级的升级路线。',b,'核查截至 2026-10-15 · 依据 S4、S6–S8、S13'),['S4','S6','S7','S8','S13'],
 '北斗区域短报文的系统能力，不能直接写成所有手机可发送的字数；手机支持北斗定位也不能计为支持卫星消息。NTN 可覆盖不同轨道，不能直接与“低轨宽带”画等号。'))
# 02 / Operator emphasis and convergence.
b=''
for y in [208,360,512]: b+=line(304,y+48,400,y+48,arrow=True)
b+=elbow(832,256,1008,356,896)+line(832,408,1008,408,arrow=True)+elbow(832,560,1008,460,928)
for y,title,date in [(208,'中国电信','2023.09 业务商用'),(360,'中国联通','2025.09.08 获牌公告'),(512,'中国移动','2025.09.29 获牌公告')]:
    b+=node(64,y,240,104,title,[date])
for y,title,body in [
 (208,'天通商用与终端生态',['手机、汽车等服务持续扩展','积累高轨业务运营经验']),
 (360,'高轨业务 + 低轨物联探索',['天通／北斗服务上线，合作发射低轨星','窄带物联与宽带直连能力应分开看']),
 (512,'天地网络融合验证',['01 星／星核验证；02 星用于直连试验','02 星于 2026.06.09 发射'])]:
    b+=node(400,y,432,116,title,body)
b+=node(1008,304,208,208,'天地融合服务',['连接用户与行业','认证与接入','计费与运维'],True,True)
b+=txt(64,650,'布局重点为归纳，不表示三家各自只走一条路线；获牌、技术试验和业务商用是不同状态。',18,500,GOLD)
figs.append(('02-operator-paths','三家起点各异，业务入口逐渐融合',base('02-operator-paths',2,'三家起点各异，业务入口逐渐融合','差异在已有资源和推进重点，长期价值在于把空间连接组织成可持续服务。',b,'核查截至 2026-10-15 · 依据 S2–S4、S9–S12、S15；布局重点为归纳'),['S2','S3','S4','S9','S10','S11','S12','S15'],
 '工信部公告先披露联通获牌，再披露移动获牌，原文称联通“补齐最晚”不成立。“星网批发、运营商零售”可作为一种合作理解，不宜画成排他的既定行业分工。资本与合作关系也不能直接推导为网络已可商用。'))
# 03 / Where processing occurs.
b=txt(64,210,'透明转发 · 基站主要在地面',22,600)+txt(64,442,'星上再生 · 这里以完整 gNB 上星作示意',22,600)
for y in [240,472]:
    b+=line(248,y+56,352,y+56,arrow=True)+line(612,y+56,716,y+56,arrow=True)+line(964,y+56,1064,y+56,arrow=True)
    b+=label(252,y+24,'服务链路',96)+label(616,y+24,'馈电链路',96)
for y in [240,472]: b+=node(64,y,184,116,'兼容终端',['收发无线信号'])+node(1064,y,152,116,'核心网',['业务接入'])
b+=node(352,240,260,116,'透明转发载荷',['转发无线信号'],True)
b+=node(716,240,248,116,'地面网关 + gNB',['基站处理主要在地面'],True)
b+=node(352,472,260,116,'星载基站处理',['解调／译码／协议处理'],True,True)
b+=node(716,472,248,116,'地面网关',['连接地面网络'],True)
b+=txt(64,628,'对 XY-2.1 的启发：把星载基带处理、波束协同、功耗与故障恢复放在同一条验证链里。',20,500)
b+=txt(64,655,'逻辑示意省略星间链路等；再生架构也存在功能拆分形式。本图不代表 XY-2.1 全系统定型架构。',16,400,MUTED)
figs.append(('03-payload-architecture','基站放在哪里，决定工程难点',base('03-payload-architecture',3,'基站放在哪里，决定工程难点','“能连卫星”背后，还要分清哪些处理在天上完成，哪些处理留在地面。',b,'技术依据 S13–S14 · XY-2.1 关联为工程解读，非能力或符合性结论'),['S13','S14'],
 '结合 XY-2.1 当前本地架构学习资料与 V0.6 详细设计报告阅读。星载基带只是系统的一部分，不能用单机性能替代端到端通信能力。未复制项目内部器件数量、容量参数、成本、计划或受控接口细节。'))
# 04 / Three decision gates, no invented readiness status.
b=''
for a,z in [(292,332),(444,484),(596,624)]:b+=line(616,a,616,z,arrow=True)
for y,z,m in [(236,358,896),(388,412,928),(540,466,864)]:b+=elbow(736,y,1000,z,m)
for y in [236,388,540]:b+=label(764,y-32,'未通过',80)
for y in [300,452,600]:b+=label(624,y,'通过',56)
for cy,s in [(236,'链路稳定接通？'),(388,'移动中业务连续？'),(540,'具备运营条件？')]:
    b+=f'<g data-node="{s}"><path d="M616,{cy-56} L736,{cy} L616,{cy+56} L496,{cy} Z" fill="{PAPER}" stroke="{MUTED}" stroke-width="1.5"/>'+txt(616,cy+7,s,20,600,INK,'middle')+'</g>'
for y,title,body in [(220,'01  链路与终端',['终端能力、链路预算','频偏／时延补偿、接入成功率']), (372,'02  覆盖与容量',['过境与切换、拥塞下的吞吐','业务波束 × 带宽 × 并发配置']), (524,'03  运维与成本',['功耗热控、故障恢复、计费对账','成本和服务承诺能否持续'])]:
    b+=txt(64,y,title,24,600)+lines(64,y+32,body,20,29)
b+=node(1000,304,216,216,'回到对应环节',['补齐测试证据','修改设计或配置','重复验证'],True)
b+=f'<g data-node="进入商用评估">'+rect(496,624,240,40,TINT,GOLD)+txt(616,652,'进入商用评估',24,600,INK,'middle')+'</g>'
figs.append(('04-commercial-gates','从试验到商用，需要三次判定',base('04-commercial-gates',4,'从试验到商用，需要三次判定','建议的工程评估框架：一次连通、峰值测速或成功发射，都只回答了部分问题。',b,'工程建议 · 各关口应明确场景、门限与证据；本图不表示项目当前进度'),[],
 '建议把端到端用例作为 XY-2.1 的验证主线：终端接入 → 波束生效 → 业务承载 → 切换或异常恢复 → 日志及地面确认。扩波束评估应同时列明带宽、并发、处理与接口余量、功耗以及故障后的可用能力。商业运营关口属于系统与运营层，不应全部变成基带单机承诺。'))

def src_list(ids):
    return '<ul class="sources">'+''.join(f'<li>[{i}] {escape(t)}<span class="source-url">{escape(u)}</span></li>' for i,t,u in SOURCES if i in ids)+'</ul>'

def page(title,content):
    return f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)}</title><style>{CSS}</style></head><body><main>{content}</main></body></html>'

for slug,title,svg,ids,note in figs:
    (OUT/(slug+'.html')).write_text(page(title,f'<h1>{escape(title)}</h1><p class="note">横图可左右滑动。<a href="{slug}.png">打开高清 PNG</a></p><div class="diagram-container">{svg}</div><div class="evidence"><p>{escape(note)}</p>{src_list(ids)}<p><a href="index.html">返回四图总览</a></p></div>'))

corrections=[
 ('有依据，需分清解读','“卫星互联网”与“航空航天”进入政府工作报告','2026 年报告明确提出加快发展卫星互联网，并将航空航天列入新兴支柱产业。“不再是地面网络的补充”是作者的进一步解读，不是报告原文规定的业务定位。','S1'),
 ('需纠正','“天通国产基带芯片只有华力创通一家量产”','中国电信官方披露与中科晶上为三星 S25 Ultra 提供定制天通芯片，不能保留“国产唯一”的表述。','S5'),
 ('需纠正','“联通补齐最晚”','工信部获牌公告：联通为 2025-09-08，移动为 2025-09-29。公告日不必等于许可证签发日。','S2、S3'),
 ('需限定','“北斗短报文能传 1000 个汉字”','这是区域短报文的系统能力口径，全球服务与手机产品的限制不同。华为具体产品的消息长度远小于 1000 字，应按机型、服务和运营商说明。','S7、S8'),
 ('需更新','“天通只解决语音和短信”','部分手机与应用已支持压缩图片和即时消息；这仍不能等同于通用宽带上网。','S6'),
 ('需区分','“北斗芯片出货或定位渗透率”','定位接收能力与短报文通信能力不同，不能把定位终端规模当成卫星通信用户规模。','S7、S8'),
 ('证据不足','“11 / 3.6 Mbps 接近 4G 体验”及其与 04 星的关系','二手报道将该 NR-NTN 试验追溯到 2024 年 2 月。本文未取得足以支持原文拼接关系的一手试验记录，因此不将该速率归因于 2025 年发射的窄带物联 04 星，也不将峰值速率写成连续服务体验。','S9、S13；速率不进入主图'),
 ('仅可作分析','“星网批发、三大运营商零售”','这可描述一种合作模式，不是已核实且排他的行业分工；中国时空信息集团是带宽计费枢纽的说法也未得到本次一手来源支持。','原文分析，非确定事实'),
 ('待核实，主图不采用','芯片具体工艺与功耗、出货量、订单金额、采购禁令、资本持股、2664 颗申报、128 波束和降低 20% 功耗、两极通话','这些口径需要分别追溯公司公告、产品数据表、监管决定、ITU 申报和测试条件。缺少一手证据不等于判定为假，但不宜据此画排名、技术能力或投资结论。','未完成一手核实'),
]
review=''.join(f'<li><strong>{escape(kind)}：{escape(claim)}</strong><br>{escape(why)} <span class="note">[{escape(ref)}]</span></li>' for kind,claim,why,ref in corrections)
content='<p class="kicker">文章阅读与工程解读 · 2026-10-15</p><h1>手机直连卫星：四图看懂路线、布局与落地</h1><p>基于你粘贴的《运营商手机直连卫星业务盘点和展望》整理，并核对关键公开事实。图 1–2 汇总业务与产业，图 3 解释技术架构，图 4 给出工程建议。</p>'
content+='<p class="note">横图可左右滑动；每张图下方可打开 2560 × 1440 高清 PNG。</p><nav>'+''.join(f'<a href="#{s}">{k+1:02d} · {escape(t)}</a>' for k,(s,t,*_) in enumerate(figs))+'</nav>'
for slug,title,svg,ids,note in figs:
    # IDs are already prefixed except defs IDs; namespace those for a shared document.
    svg=svg.replace('id="arr"',f'id="{slug}-arr"').replace('url(#arr)',f'url(#{slug}-arr)').replace('id="grain"',f'id="{slug}-grain"').replace('url(#grain)',f'url(#{slug}-grain)')
    content+=f'<section id="{slug}"><div class="diagram-container">{svg}</div><div class="evidence"><p>{escape(note)}</p><p><a href="{slug}.html">打开单张图</a> · <a href="{slug}.png">打开高清 PNG</a></p>{src_list(ids)}</div></section>'
content+='<section><h2>对这篇文章的建议</h2><p>适合把它当作产业观察的入口。对外引用前，应拆开“系统能力、具体终端能力、试验结果、商用服务”四种口径；运营商布局可保留，未经核实的唯一性、资本和芯片参数应删去或明确标为待核实。</p><ol>'+review+'</ol><h2>结合 XY-2.1，建议优先做的事</h2><p>围绕一条真实业务链组织验证，把接入、波控生效、数据承载、切换、异常恢复与观测证据串起来。讨论扩容时，把波束数、带宽、并发、处理能力、接口负载和功耗放到同一张资源账上。单机验收与运营商的端到端服务目标需要明确分工。</p><h2>阅读与呈现边界</h2><p class="note">文章内容来自用户粘贴，未声称读到被拦截的微信页面。公开事实核查截至 2026-10-15。行业布局有归纳，技术图有简化，工程建议不代表测试已完成。使用 LeoGuoLabs Light v1；中文采用系统无衬线字体。未发布到社交平台。</p></section>'
content+='<section><h2>补充核查来源</h2>'+src_list(['S1','S5'])+'</section>'
(OUT/'index.html').write_text(page('手机直连卫星｜四图阅读',content))
(OUT/'research.json').write_text(json.dumps({'review_date':'2026-10-15','source':{'title':'运营商手机直连卫星业务盘点和展望','url':'https://mp.weixin.qq.com/s/Lj5BTFHSt4TTnn-7JLtzdg','acquisition':'User pasted complete article into chat; blocked original page was not retried'},'scope':'Chinese visual synthesis and engineering advice; no publication requested','design':{'skill':'diagram-design','brand':'LeoGuoLabs Light v1 from project AGENTS.md; overrides default skill colors and serif typography','preset':'slide-16x9','viewbox':[1280,720],'fonts':'Geist, Inter, PingFang SC, Microsoft YaHei, sans-serif; actual platform resolution checked at render time','language':'zh-CN','figures':[{'slug':s,'title':t,'type':'flowchart' if s.startswith('04') else 'architecture','sources':ids,'note':n} for s,t,v,ids,n in figs]},'sources':[{'id':i,'title':t,'url':u}for i,t,u in SOURCES],'claim_review':[{'status':a,'claim':b,'assessment':c,'references':d}for a,b,c,d in corrections],'local_context':['XY-2.1/learn/基带处理组件入门笔记.md','XY-2.1/DesignReports/详细设计报告-CRD/XY2.1-星载基站基带处理组件详细设计报告-V0.6.md'],'privacy':'No internal numeric specification, costs, schedule, or controlled interfaces copied into deliverables.'},ensure_ascii=False,indent=2)+'\n')
print('Built four diagrams, index.html, and research.json')

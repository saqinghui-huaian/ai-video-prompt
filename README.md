# ai-video-prompt

WorkBuddy 用户级 Skill：生成 **30 秒 / 5 镜 AI 视频提示词规格书**（镜数与参考图数可变）。

本仓库的全部模板、规范、脚本与词库，都由**同一份原型**反推而来，不并列其它体系。
**只借结构，不借题材**：原型的年代、地名、人名、年代物件、台词、具体色值都属于那部片，换题必须替换。

## 源画布与原型

- **源画布**：https://app.tapnow.media/canvas/0e561120-5c2d-4bd8-821b-f5c532645ec5 （`Creative Concept (1016)`）
- **原型提示词**：2006 年中国小城高中校园小卖部、李默买水的 30 秒 5 镜 `[STYLE LOCK]` 规格书
- **原文存档**：[`references/golden-example.md`](references/golden-example.md) —— 质量基线，任何产出不得低于它的信息密度

这套画布的核心方法：先用 `[STYLE LOCK]` 锁定摄影规格与色温，再声明参考图边界、空间站位与完整动线，最后逐镜写连续动作并把声音逐镜对账；跨时间线用暖 / 冷色温对立做叙事，角色一致性靠 `Same person as the attached 18-year-old character sheet` 等引用句维持。

## 核心结构（五段，固定顺序）

| 段 | 标题 | 内容 |
|---|---|---|
| 1 | `[STYLE LOCK]` 风格锁 | 七个子槽：年代地点 / 观感 / 运镜体系 / 光位三件套 / 年代物件 / 人气 / 胶片质感与对白规则 |
| 2 | `[参考图锚定]` | 按**挂载顺序**编号，每图三段：是什么 / 提供什么 / 不提供什么 + 冲突裁决句 |
| 3 | `[空间与站位声明]` | 方位锚点（一条一物件）→ 完整动线（`→` 串联）→ 跨镜持续状态 |
| 4 | `CLIP正文（N镜）` | 每镜：机位运镜 → 连续动作（含物理反馈）→ 前景/背景虚焦 → 群演动作 → 画外对白 |
| 5 | `[BGM & 声音设计]` | 底层环境声 + 逐镜音效/对白 + 声场转换 |

默认 30 秒 / 5 镜 / 每镜约 6 秒。用户指定其它时长时按「总时长 ÷ 单镜时长」重算镜数，结构不变。

## 参考图引用协议（`{{Image N}}`）

这是最容易出错、也最容易被忽略的一层。完整规则见 [`references/reference-image-protocol.md`](references/reference-image-protocol.md)，要点：

- **编号 = 挂载顺序**。节点里第 N 个拖入的图就是 `{{Image N}}`，与角色重要性无关；顺序变了编号必须重写，跳号会失效。
- **每张图写三段**：是什么 / 提供什么 / 不提供什么，并附「冲突以正文为准」。只写「仅提供面部参考」不足以阻止参考图把平光、构图、背景带进每一镜。
- **角色与场景不要合成一张图**，否则场景色温会烧到人物脸上，且无法分别声明边界。
- **缺图要降级**：0 张 → 保留段 2 标题写明不使用，并在正文首次出现主体处补一次外观锚点；1 张 → 补缺那一侧的文字描述；3–4 张 → 逐行写并防互相污染；>4 张 → 拆片。
- **必须附对账行**，把编号映射回挂载顺序，否则用户无从核对。脚本 `--manifest` 可直接打印这一行。
- **不确定平台怎么认编号时，跑一次三分钟自验**（协议第九节）：把两张图故意挂反，用最低配置生成一次，看模型按文字还是按顺序认图。换平台必重测。

## 关键设计（从原型提炼，可迁移）

- **风格锁写成规格书**：全片固定项一次锁死，会随镜头变化的内容一律下移到 CLIP 正文。
- **参考图不锁机位**：显式写「各镜机位由正文定义」，避免参考图反向锁死构图。
- **动线闭合**：起点动作 → 经过节点 → 交互 → 离开方向 → 出画方位，并声明跨镜持续状态。
- **动作是物理过程**：每个动作都要有可听可看的物理反馈（水晃、瓶底碰台、硬币轻嗒）。
- **并发动作显式绑定**：写「A 的全过程与 B 同时完成」，防止模型把动作拆成静止分镜。
- **群演与画外对白维持空间真实**：每镜至少一个次要动作 + 一句清晰中文，台词标唇音同步。
- **声画逐镜对账**：段 5 每行都能在段 4 找到对应声源。
- **收束靠动作**：末镜用视线转移 / 低头 / 出画收，不写情绪形容。

## 三份补充库（v6 新增，均为查漏工具）

主线仍是五段结构，这三份只补「词」和「改法」，不改槽位定义、不构成第二套体系：

| 文件 | 治什么 | 怎么用 |
|---|---|---|
| [`references/camera-motion-library.md`](references/camera-motion-library.md) | 段 4 第一成分「机位与运镜」写空、写错 | 34 式运镜：英文对照 / 叙事用途 / 一句式写法 / 反例；取词四条纪律（段 1 定体系、一镜一主运镜、速度写「倍速·整镜用时」、必带主体锚点）；节奏三档；战斗/对话/回忆/探索四类镜头序列；六种失败模式 |
| [`references/action-chain-library.md`](references/action-chain-library.md) | 段 4 第二成分「连续动作」被写成静态姿势 | 20 条**三拍动作链**（起手→过程→反馈），分移动 / 取放 / 递接 / 情绪转折 / 身体状态 / 群像六组，每条自带声音标记；附「单拍扩三拍」五条规则 |
| [`references/abstract-emotion-rewrite.md`](references/abstract-emotion-rewrite.md) | 质检第 17 条：正文出现「孤独 / 紧张 / 高级感」 | 五通道改写（光位 / 材质 / 动作 / 物件 / 声音）+ 25 组对照表；写完正文全文搜一遍抽象词，命中即改 |

三份库的来源与清洗口径写在各自文件头部：原素材 235 条运镜 / 80 条单拍动作 / 80 条情绪词，共删除概念重复 5 对、修正「秒/帧」单位错误 10 处、剔除「8K 高清」类无效参数 16 处。

## 目录结构

```
ai-video-prompt/
├── SKILL.md                             # 技能入口：唯一基准、五段结构、硬约束、工作流
├── assets/
│   ├── video-spec-template.md          # 五段规格书可填骨架（镜数/参考图数可变）
│   ├── example-config.json             # 脚本输入样例：双参考图 / 5 镜 30 秒
│   ├── example-config-single-ref.json  # 脚本输入样例：单参考图 / 4 镜 24 秒
│   └── image-prompt-template.md        # 辅助：单张图提示词模板
├── references/
│   ├── golden-example.md               # ★ 原型原文 + 8 条质量基线 + 原型私有项清单
│   ├── reference-image-protocol.md     # ★ 参考图编号、边界、降级矩阵、对账、失败模式
│   ├── spec-guide.md                   # 五段槽位字典 + 20 项质检
│   ├── style-lock-library.md           # 七槽填空法、三种色温方向、光位、年代物件、声音、一致性
│   ├── camera-motion-library.md        # 补充：运镜 34 式 + 节奏三档 + 场景镜头序列 + 失败模式
│   ├── action-chain-library.md         # 补充：20 条三拍动作链 + 单拍扩三拍规则
│   ├── abstract-emotion-rewrite.md     # 补充：25 组抽象情绪 → 可拍摄改写
│   ├── image-prompt-guide.md           # 辅助：单张图工作流与质检
│   └── dimension-library.md            # 辅助：静态图查漏八步与全部选项
└── scripts/
    └── build_prompt.py                 # JSON → 规格书；--check 校验，--manifest 出对账
```

## 安装

把本仓库内容放到 WorkBuddy 用户技能目录：

```
~/.workbuddy/skills/ai-video-prompt/
```

或使用 GitHub 的 **Download ZIP** 解压到该目录。技能由 `SKILL.md` 的 frontmatter 自动注册。

## 快速开始

```
用 STYLE LOCK 规格书把「面试间送客」写成 30 秒 5 镜
```

批量生成：

```bash
python scripts/build_prompt.py assets/example-config.json --check       # 校验 + 打印对账表
python scripts/build_prompt.py assets/example-config.json -o output.md  # 输出正文
python scripts/build_prompt.py assets/example-config.json --manifest    # 只打印挂载顺序
```

`--check` 校验镜数、时间码合计、必填段、参考图边界字段（`withholds` / `conflict` 为必填，备注不能顶替）与编号连续性；通过后才输出正文。
`reference_images` 整个键可以省略（等价于空列表），即 0 张参考图的降级配置。
`check_profile` 可选 `dialogue` / `no_dialogue` / `product` / `montage`，调整软性质检阈值；写错档位会被当成错误拦下。
提示词正文是英文时，脚本会跳过中文关键词软校验并给出 INFO，不再误报一串 WARN。

### 配置字段速查

| 字段 | 必填 | 说明 |
|---|---|---|
| `style_lock` | ✅ | 段 1 的七个子槽：`era_place` `look` `camera` `lighting` `set_dressing` `crowd` `grade` `dialogue_rule` |
| `reference_images` | ➖ | 参考图数组，可省略或为 `[]`。每项 `name` / `provides` / `withholds` / `conflict` 均必填（`note` 为可选补充，不能顶替） |
| `spatial` | ✅ | `anchors`（数组，一条一物件）/ `blocking`（`→` 串联）/ `continuity`（数组）/ `subject`（主体名，用于「X 动线」） |
| `clips` | ✅ | 每项 `tc`（`MM:SS-MM:SS`）/ `body`；数量任意，时间码须连续 |
| `sound` | ✅ | `bed`（底层环境）+ `per_clip`（数组，行数须等于镜数） |
| `subject` | ➖ | 主体名；与 `spatial.subject` 等价，二者都不写会得到「主体动线」并被 WARN |
| `duration` / `clip_count` | ➖ | 缺省由 `clips` 推导；显式写出则参与校验 |
| `negative` | ➖ | 负面约束数组，缺省会 WARN |
| `check_profile` | ➖ | `dialogue`(默认) / `no_dialogue` / `product` / `montage`；拼错算错误 |
| `title` / `aspect_ratio` / `params` | ➖ | 仅作记录，脚本不读取，供人工附在正文之外 |

## 辅助能力（非主线）

仅当用户明确要求**静态图片提示词 / 设定图 / 定妆照 / 场景空镜**时，才使用 `assets/image-prompt-template.md` 与 `references/image-prompt-guide.md`（查漏八步，骨架沿用主体系七槽）。它是查漏工具与轻量模式，**不是与五段规格书并列的第二套体系**，也不得用它替代主输出。

设定图出完之后还有一步：挂进生成节点、按挂载顺序编号、在段 2 声明边界。见参考图协议第六节。

## 来源与署名

- 全部核心内容整理自自建 TapNow 画布 [`Creative Concept (1016) (copy)`](https://app.tapnow.media/canvas/0e561120-5c2d-4bd8-821b-f5c532645ec5) 的视频节点提示词，原型由仓库所有者提供。
- `references/dimension-library.md` 与 `references/image-prompt-guide.md` 的静态图框架，由仓库所有者按自己的七槽体系重新组织与表述，不复制任何第三方原文、图解或分类层级。
- `references/camera-motion-library.md`、`action-chain-library.md`、`abstract-emotion-rewrite.md` 由一份外部漫剧提示词知识体系文档清洗重写而来，只保留方法与词表，未收录原文与图片。
- 本仓库未附开源许可证，仅供个人学习与创作使用。

## 版本

| 日期 | 内容 |
|---|---|
| 2026-11-08 | v1：从源画布提炼五段规格书，固化原型提示词 |
| 2026-11-08 | v2：一度把辅助框架抬为并列体系（**已撤销**） |
| 2026-11-09 | v3：回归唯一基准，明确源画布链接与原型地位；辅助能力降为非主线；修正署名 |
| 2026-11-09 | v4：补齐参考图引用协议（编号=挂载顺序 / 三段式边界 / 降级矩阵 / 对账）；模板去题材绑定，镜数与图数变量化；脚本支持 0 图与多档 check_profile；新增单参考图样例；质检扩到 20 项 |
| 2026-11-21 | v5：修 4 处校验自相矛盾——缺省 `reference_images` 被误判失败、`withholds`/`conflict` 可被备注顶替、`check_profile` 拼错误只告警、英文正文误报 4 条 WARN；英文正文改走 INFO 跳过；超 4 张图给出告警；时间码解析失败不再连带误报总时长；样例补 `spatial.subject` 避免出现「主体动线」；新增配置字段速查表；修 spec-guide 指向已改名表格的悬空引用与两处多余空格；协议新增第九节「三分钟自验」，明确编号规则是平台行为推断而非普适定律 |
| 2026-11-23 | v6：新增三份补充库（运镜 34 式 / 三拍动作链 20 条 / 抽象情绪改写 25 组）；`dimension-library.md` 运镜表 10 行扩到 20 行并统一速度单位写法；`spec-guide.md` 段 4 加「取词查漏」指引、质检第 17 条挂上改写工具；`SKILL.md` 工作流第 3 步与资源索引接入三库。三库均标注为「补充（查漏用）」，不改五段结构与槽位定义 |
| 2026-11-23 | v7：辅助层除源重写。静态图框架不再沿用外部分类，改按主体系七槽组织为**八步查漏法**（定点 / 定调 / 定光 / 定景 / 定主体 / 定镜头 / 动效 / 排除），原选项库全部子项逐项保留（人物七层、生物五项、物品四项、建筑四项、光源四项、镜头七项、运镜 20 行）；删除第三方版权原图及其全部引用；`image-prompt-guide.md` 原维度表换为八步表，工作流与质检同步；`assets/image-prompt-template.md` 占位符对照改按八步归属；`SKILL.md` 触发词与资源索引、README 来源署名同步。主体系（五段结构、参考图协议、槽位字典、脚本）一字未动 |

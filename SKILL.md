---
name: ai-video-prompt
description: 以 TapNow 画布 0e561120-5c2d-4bd8-821b-f5c532645ec5 的 [STYLE LOCK] 30 秒 5 镜规格书为唯一核心基准，生成可直接粘贴到 Seedance 2.5 / 可灵 / 即梦 / Veo 的 AI 视频提示词。当用户要求写视频提示词、做分镜脚本、固定 STYLE LOCK 模板、把一段场景扩写成 30 秒成片提示词时使用。默认输出五段结构：风格锁 / 参考图锚定 / 空间与站位声明 / CLIP 正文 / BGM 与声音设计。附带静态图片提示词作为辅助模式（影视飓风四维框架），仅在用户明确要求设定图、定妆照、单张图时使用。
agent_created: true
---

# AI 视频提示词生成（30 秒 5 镜规格书）

## 唯一基准

本技能的**全部模板、规范、脚本、词库都由同一份原型反推**：

- 源画布：https://app.tapnow.media/canvas/0e561120-5c2d-4bd8-821b-f5c532645ec5 （`Creative Concept (1016)`）
- 原型提示词：2006 年中国小城高中校园小卖部、李默买水的 30 秒 5 镜 `[STYLE LOCK]` 规格书
- 原文存档：`references/golden-example.md`（**质量基线，任何产出不得低于它的信息密度**）

不得用其它画布或框架替换这套基准。影视飓风《图片提示词》四维框架只是**辅助查漏工具**，不是与它并列的第二套体系；「全频道阻塞干扰」等其它画布不属于本项目来源。

## 五段结构（固定顺序，默认输出格式）

| 段 | 标题 | 作用 |
|---|---|---|
| 1 | `[STYLE LOCK]` 风格锁 | 摄影规格、光位、陈设、人气、胶片质感、对白语言规则 |
| 2 | `[参考图锚定]` | 声明 `{{Image N}}` 提供什么、不提供什么；机位与状态以正文为准 |
| 3 | `[空间与站位声明]` | 方位锚点、完整动线、跨镜状态延续 |
| 4 | `CLIP正文（5镜）` | 逐镜：机位 + 连续动作 + 前后景虚焦 + 群演 + 画外对白 |
| 5 | `[BGM & 声音设计]` | 底层环境声 + 逐镜音效 / 对白 + 声场转换 |

默认 **30 秒 / 5 镜 / 每镜约 6 秒**。用户指定其它时长时，调整镜数与时间码，五段结构不变。

## 默认工作流

1. 读取 `references/golden-example.md`，确认原型的结构与密度；读取 `references/spec-guide.md` 掌握槽位字典。
2. 以 `assets/video-spec-template.md` 为输出骨架；风格词查 `references/style-lock-library.md`。
3. 解析场景描述，按五段固定顺序组装；缺省项用合理默认值补齐，不反问超过一轮。
4. 需要批量或可复现产出时，填写与 `assets/example-config.json` 同构的配置，运行 `scripts/build_prompt.py`。
5. 按 `references/spec-guide.md` 第七节 15 项质检清单核验后输出。

## 硬约束（全部来自原型）

- 风格锁前置，用编号或标签写成**规格书**，不写成散文。
- 参考图只锚外观与空间结构；机位、动作、状态一律以 CLIP 正文为准。
- 空间声明先于分镜；动线贯穿全片，相邻镜不跳轴、不反向。
- 每镜只写一条连续动作链；并发动作写「与…同时完成」。
- 画外对白写清晰中文原句，台词标注「嘴唇开合与声音同步」。
- 声音设计逐镜对账；跨室内外写明声场转换。
- 不写抽象情绪词，改写为可拍摄的光位、材质、动作、物件。
- 主体外观只在风格锁或参考图声明中出现一次，正文用名字或代词指代。
- 末镜留收束动作（视线转移、低头、出画），并交代声场落点。
- 产出后附模型参数建议（模型、时长、比例、分辨率、seed、参考图）。

## 辅助模式（非主线，仅显式触发）

只有用户明确说「图片提示词 / 设定图 / 定妆照 / 场景空镜 / 三视图 / 影视飓风 / 那张思维导图」时，才走静态图片提示词：

- 模板 `assets/image-prompt-template.md`，规范 `references/image-prompt-guide.md`
- 维度选项 `references/dimension-library.md`（时间 / 主体 / 场景 / 风格），原图 `references/visual-dimension-map.jpg` 仅作溯源
- 产出单张图中英双版，100–200 字；**不得用它替代五段规格书**

若用户要「先做设定图再拍 30 秒」，先出辅助图，再把它作为主体系 `{{Image N}}` 的参考图输入，并在参考图锚定段声明边界。

## 资源索引

| 文件 | 归属 | 用途 |
|---|---|---|
| `references/golden-example.md` | **核心基准** | 原型提示词原文 + 8 条质量基线 |
| `references/spec-guide.md` | 核心 | 五段槽位字典、写法纪律、15 项质检 |
| `assets/video-spec-template.md` | 核心 | 五段规格书可填骨架 |
| `references/style-lock-library.md` | 核心 | 暖/冷色温、光位、年代物件、声音、一致性工程 |
| `assets/example-config.json` | 核心 | 脚本输入样例（小卖部 5 镜） |
| `scripts/build_prompt.py` | 核心 | JSON → 完整规格书，`--check` 结构校验 |
| `assets/image-prompt-template.md` | 辅助 | 单张图提示词模板 |
| `references/image-prompt-guide.md` | 辅助 | 单张图工作流与质检 |
| `references/dimension-library.md` | 辅助 | 四维维度选项库（也可用于主体系可选查漏） |
| `references/visual-dimension-map.jpg` | 辅助 | 影视飓风原图，仅溯源 |

## 脚本用法

```
python scripts/build_prompt.py <config.json> [-o output.md] [--check]
```

`--check` 只校验结构（镜数、时间码合计、必填段、参考图编号）不输出正文。

## 输出要求

- 默认给完整可复制的规格书正文，正文块内不用 Markdown 表格。
- 正文之后另附「参数建议」与「质检结果」。
- 走辅助模式时明确标注，避免用户误以为是主体系产出。

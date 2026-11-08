---
name: ai-video-prompt
description: 生成 AI 视觉提示词，内含两套并列且独立的体系：体系 A 为图片提示词（影视飓风四维框架：时间/主体/场景/风格，产出单张静态图的中英双版提示词）；体系 B 为视频分镜规格书（STYLE LOCK/参考图锚定/空间与站位声明/CLIP 正文/BGM 与声音设计，默认 30 秒 5 镜）。当用户要求写图片提示词、角色设定图、场景空镜、做分镜脚本、写视频提示词、固定 STYLE LOCK 模板、把一段场景扩写成可直接粘贴到 Seedance 2.5 / 可灵 / 即梦 / Veo / Midjourney / FLUX 的完整提示词时使用。用户提到「影视飓风」「图片提示词维度」「那张思维导图」时走体系 A，提到「30 秒」「5 镜」「分镜」「声音设计」「一次生成」时走体系 B。
agent_created: true
---

# AI 视觉提示词生成（两套体系）

## 目的

把模糊创意或一段场景描述，扩写成模型可直接执行的提示词。技能包含**两套并列、各自独立**的体系：一套面向静态图片，一套面向视频分镜。两者有不同的维度、模板、工作流与质检标准，**不互相替代，也不把其中一套降为另一套的附属清单**。

## 两套体系对照

| 项 | **体系 A · 图片提示词** | **体系 B · 视频分镜规格书** |
|---|---|---|
| 依据 | 影视飓风《图片提示词》四维框架 | `Creative Concept (1016)` 画布的 `[STYLE LOCK]` 规格书 |
| 维度 | 时间 / 主体 / 场景 / 风格（风格下含光源、景别、角度、构图、摄影机） | 五段：风格锁 / 参考图锚定 / 空间与站位声明 / CLIP 正文 / BGM 与声音设计 |
| 产出 | 单张静态图提示词，100–200 字，中英双版 | 30 秒 / 5 镜规格书，1500–3000 字，含逐镜正文与逐镜声音 |
| 适用 | 角色设定图、场景空镜、道具三视图、主视觉、封面 | 剧情短片、多镜头长片、含对白与动线的一次生成 |
| 目标模型 | 即梦 / Seedream / 可灵图片 / Midjourney / FLUX / SD | Seedance 2.5 / 可灵 / 即梦 / Veo |
| 模板 | `assets/image-prompt-template.md` | `assets/video-spec-template.md` |
| 规范 | `references/image-prompt-guide.md` | `references/spec-guide.md` |
| 黄金示例 | 李默 18 岁定妆照（规范内第五节） | 2006 小卖部 5 镜（`references/golden-example.md`） |
| 生成器 | 模板手填（轻量） | `scripts/build_prompt.py`（可批量、可复现） |

## 路由规则

1. 出现 `分镜 / 5 镜 / 30 秒 / 对白 / 动线 / 声音设计 / STYLE LOCK / 参考图锚定 / 一次生成` 任一信号 → **体系 B**。
2. 出现 `图片提示词 / 设定图 / 定妆照 / 空镜 / 三视图 / 封面 / 影视飓风 / 那张思维导图` 任一信号 → **体系 A**。
3. 用户给出一段含多个连续动作的长场景描述 → **体系 B**；只描述一个画面 → **体系 A**。
4. 两者都可能时（如「先做角色设定图，再拍 30 秒」）→ **按先 A 后 B 串行执行**，A 的产出作为 B 的 `{{Image N}}` 参考图输入，并在 B 的参考图锚定段声明边界。
5. 仍不明确时，用一句提问确认，不反复追问。

## 体系 A 工作流

1. 读取 `references/image-prompt-guide.md` 与 `assets/image-prompt-template.md`；维度选项查 `references/dimension-library.md`。
2. 解析创意，标出已给维度，用合理默认值补齐（傍晚 / 中景或特写 / 黄金时刻自然光 / 电影感写实），不反问超过一轮。
3. 按模板的**书写顺序**拼接，注意「四维分类 ≠ 输出顺序」。
4. 对照四维表查漏，重点查光源三件套（类型 / 位置 / 光质）与镜头四件套（景别 / 角度 / 构图 / 焦段）。
5. 输出中文版 + 英文版 + 一行可调参数；按规范第六节质检。

## 体系 B 工作流

1. 读取 `references/spec-guide.md` 掌握五段结构；读取 `references/dimension-library.md` 末尾的「跨体系交叉核对」作为**可选**补充，不作为从属清单。
2. 以 `assets/video-spec-template.md` 为输出骨架；风格词查 `references/style-lock-library.md`，质量基线对标 `references/golden-example.md`。
3. 解析输入，按固定顺序组装五段：风格锁 → 参考图锚定 → 空间与站位声明 → CLIP 正文 → BGM 与声音设计。
4. 需要批量或可复现产出时，填写 `assets/example-config.json` 同构配置并运行 `scripts/build_prompt.py`。
5. 按 `references/spec-guide.md` 第七节的 15 项质检清单核验后输出。

## 共用规则

- **负面约束**：变形、多手指、面部崩坏、文字、字幕、logo、水印；体系 B 另加跳轴、速度突变、动画感。
- **参数与登记**：模型版本、时长（B）/ 尺寸（A）、比例、分辨率、seed、参考图顺序一律登记；模型迭代后同 prompt 不再等价。
- **参考图边界**：参考图只锚外观与空间结构，机位 / 动作 / 状态以正文为准。
- **不写抽象情绪词**：把「压抑 / 高级感」改写为可拍摄的光位、材质、动作、物件。
- **输出语言**：说明用中文；提示词正文按题材可中可英，体系 A 默认双版。

## 资源索引

| 文件 | 归属 | 用途 |
|---|---|---|
| `assets/image-prompt-template.md` | A | 四维框架可填模板（书写顺序 + 占位符对照） |
| `references/image-prompt-guide.md` | A | 工作流、写法纪律、定妆照黄金示例、9 项质检 |
| `references/dimension-library.md` | A 主 / B 可选 | 四维维度选项库 + 跨体系交叉核对映射 |
| `references/visual-dimension-map.jpg` | A | 影视飓风原版思维导图，仅作溯源凭证 |
| `assets/video-spec-template.md` | B | 五段规格书可填骨架 |
| `references/spec-guide.md` | B | 槽位字典、写法纪律、15 项质检 |
| `references/golden-example.md` | B | 2006 小卖部 5 镜原文 + 8 条质量基线 |
| `references/style-lock-library.md` | B | 暖/冷双色温、光位、年代物件、声音、一致性工程 |
| `assets/example-config.json` | B | 脚本输入样例（小卖部 5 镜） |
| `scripts/build_prompt.py` | B | JSON → 完整规格书，`--check` 结构校验 |

## 脚本用法（体系 B）

```
python scripts/build_prompt.py <config.json> [-o output.md] [--check]
```

`--check` 只校验结构（镜数、时间码合计、必填段、参考图编号）不输出正文。

## 输出要求

- 体系 A：给完整可复制正文，中英双版，附一行可调参数；不输出 Markdown 表格当作提示词。
- 体系 B：给完整可复制规格书正文，正文块内不用表格；之后另附「参数建议」与「质检结果」。
- 明确标注本次走的是哪一体系，便于用户核对与切换。

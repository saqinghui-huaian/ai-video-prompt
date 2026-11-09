# ai-video-prompt

WorkBuddy 用户级 Skill：生成 **30 秒 / 5 镜 AI 视频提示词规格书**。

本仓库的全部模板、规范、脚本与词库，都由**同一份原型**反推而来，不并列其它体系。

## 源画布与原型

- **源画布**：https://app.tapnow.media/canvas/0e561120-5c2d-4bd8-821b-f5c532645ec5 （`Creative Concept (1016)`）
- **原型提示词**：2006 年中国小城高中校园小卖部、李默买水的 30 秒 5 镜 `[STYLE LOCK]` 规格书
- **原文存档**：[`references/golden-example.md`](references/golden-example.md) —— 质量基线，任何产出不得低于它的信息密度

这套画布的核心方法：先用 `[STYLE LOCK]` 锁定摄影规格与色温，再声明参考图边界、空间站位与完整动线，最后逐镜写连续动作并把声音逐镜对账；跨时间线用暖（2000s 校园）/ 冷（2020s 职场）色温对立做叙事，角色一致性靠 `Same person as the attached 18-year-old character sheet` 等引用句维持。

## 核心结构（五段，固定顺序）

| 段 | 标题 | 内容 |
|---|---|---|
| 1 | `[STYLE LOCK]` 风格锁 | 写实电影质感、变形宽银幕、浅景深、全程手持呼吸感；顶灯/门侧光位；CRT 收银终端、价签、冷藏柜等年代物件；对白语言规则 |
| 2 | `[参考图锚定]` | `{{Image 1}}` 仅提供角色面部与校服，`{{Image 2}}` 提供场景空间与光位；**各镜机位由正文定义** |
| 3 | `[空间与站位声明]` | 收银台在中后部、出口在左侧、货架区在右侧与后侧；李默完整动线；镜 5 门内仍有排队队伍 |
| 4 | `CLIP正文（5镜）` | 每镜：机位与手持方式 → 连续动作（含物理细节）→ 前景/背景虚焦 → 群演动作 → 清晰中文画外对白 |
| 5 | `[BGM & 声音设计]` | 底层环境声 + 镜 1–5 逐镜音效/对白 + 室内闷混响转室外开阔的声场转换 |

默认 30 秒 / 5 镜 / 每镜约 6 秒。用户指定其它时长时调整镜数与时间码，五段结构不变。

## 关键设计（从原型提炼）

- **风格锁写成规格书**：全片固定项一次锁死，段落内只写镜头 + 运动 + 连续性，不重述外观。
- **参考图不锁机位**：明确写出「各镜机位由正文定义」，避免参考图反向锁死构图。
- **动线闭合**：拿水 → 绕货架 → 队尾 → 收银 → 出门 → 出画，并显式声明跨镜持续状态。
- **动作是物理过程**：抽瓶时水晃、瓶底碰台两声、硬币掂量两声轻嗒、扫码两声「滴」。
- **并发动作显式绑定**：「掏钱掂钱的全过程与走路同时完成」。
- **群演与画外对白维持空间真实**：每镜至少一个次要动作 + 一句清晰中文，台词标唇音同步。
- **声画逐镜对账**：段 5 每行都能在段 4 找到对应声源。
- **收束靠动作**：末镜「看了一次左侧 → 稍稍低下头 → 眼神回正 → 走出画面」。

## 目录结构

```
ai-video-prompt/
├── SKILL.md                          # 技能入口：唯一基准、五段结构、默认工作流
├── assets/
│   ├── video-spec-template.md       # 五段规格书可填骨架
│   ├── example-config.json          # 脚本输入样例（小卖部 5 镜）
│   └── image-prompt-template.md     # 辅助：单张图提示词模板
├── references/
│   ├── golden-example.md            # ★ 原型提示词原文 + 8 条质量基线
│   ├── spec-guide.md                # 五段槽位字典 + 15 项质检
│   ├── style-lock-library.md        # 暖/冷色温、光位、年代物件、声音、一致性工程
│   ├── image-prompt-guide.md        # 辅助：单张图工作流与质检
│   ├── dimension-library.md         # 辅助：影视飓风四维选项库（可选查漏）
│   └── visual-dimension-map.jpg     # 辅助：原版思维导图，仅溯源
└── scripts/
    └── build_prompt.py              # JSON → 完整规格书，--check 结构校验
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
python scripts/build_prompt.py assets/example-config.json --check
python scripts/build_prompt.py assets/example-config.json -o output.md
```

`--check` 校验镜数、时间码合计、必填段、参考图编号；通过后才输出正文。

## 辅助能力（非主线）

仅当用户明确要求**静态图片提示词 / 设定图 / 定妆照 / 场景空镜**时，才使用 `assets/image-prompt-template.md` 与 `references/image-prompt-guide.md`（维度框架源自影视飓风《图片提示词》思维导图）。它是查漏工具与轻量模式，**不是与五段规格书并列的第二套体系**，也不得用它替代主输出。

## 来源与署名

- 全部核心内容整理自自建 TapNow 画布 [`Creative Concept (1016) (copy)`](https://app.tapnow.media/canvas/0e561120-5c2d-4bd8-821b-f5c532645ec5) 的视频节点提示词，原型由仓库所有者提供。
- `references/visual-dimension-map.jpg` 为影视飓风《图片提示词》思维导图原图，版权归原作者所有，仅作辅助方法溯源；`references/dimension-library.md` 是其可读文本化版本。
- 本仓库未附开源许可证，仅供个人学习与创作使用。

## 版本

| 日期 | 内容 |
|---|---|
| 2026-11-08 | v1：从源画布提炼五段规格书，固化原型提示词 |
| 2026-11-08 | v2：一度把影视飓风四维框架抬为并列体系（**已撤销**） |
| 2026-11-09 | v3：回归唯一基准，明确源画布链接与原型地位；辅助能力降为非主线；修正署名 |

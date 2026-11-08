# ai-video-prompt

WorkBuddy 用户级 Skill：把模糊创意扩写成模型可直接执行的 AI 视觉提示词。

内置**两套并列且独立**的体系，各自有独立的维度、模板、工作流、黄金示例与质检标准，互不替代。

## 两套体系

| 项 | **体系 A · 图片提示词** | **体系 B · 视频分镜规格书** |
|---|---|---|
| 依据 | 影视飓风《图片提示词》四维框架 | TapNow 画布的 `[STYLE LOCK]` 规格书 |
| 维度 | 时间 / 主体 / 场景 / 风格 | 风格锁 / 参考图锚定 / 空间与站位声明 / CLIP 正文 / BGM 与声音设计 |
| 产出 | 单张静态图提示词，中英双版，100–200 字 | 30 秒 5 镜规格书，1500–3000 字，含逐镜声音 |
| 适用 | 角色设定图、场景空镜、道具三视图、主视觉 | 剧情短片、多镜头长片、含对白与动线的一次生成 |
| 目标模型 | 即梦 / Seedream / 可灵图片 / Midjourney / FLUX / SD | Seedance 2.5 / 可灵 / 即梦 / Veo |
| 模板 | `assets/image-prompt-template.md` | `assets/video-spec-template.md` |
| 规范 | `references/image-prompt-guide.md` | `references/spec-guide.md` |
| 黄金示例 | 李默 18 岁定妆照（中英双版） | 2006 小卖部 5 镜原文 |
| 生成器 | 模板手填 | `scripts/build_prompt.py`（可批量、可复现） |

## 路由规则

- `分镜 / 5 镜 / 30 秒 / 对白 / 动线 / 声音设计 / STYLE LOCK / 一次生成` → 体系 B
- `图片提示词 / 设定图 / 定妆照 / 空镜 / 三视图 / 影视飓风 / 那张思维导图` → 体系 A
- 长场景描述 → B；单画面 → A；「先做设定图再拍片」→ A → B 串行，A 的产出作为 B 的 `{{Image N}}` 输入

## 目录结构

```
ai-video-prompt/
├── SKILL.md                          # 技能入口：路由、两套工作流、共用规则
├── assets/
│   ├── image-prompt-template.md     # A：四维框架可填模板
│   ├── video-spec-template.md       # B：五段规格书可填骨架
│   └── example-config.json          # B：脚本输入样例（小卖部 5 镜）
├── references/
│   ├── image-prompt-guide.md        # A：工作流 + 定妆照黄金示例 + 9 项质检
│   ├── dimension-library.md         # A 主维度库 + B 可选交叉核对
│   ├── visual-dimension-map.jpg     # 影视飓风原版思维导图（溯源凭证）
│   ├── spec-guide.md                # B：槽位字典 + 15 项质检
│   ├── style-lock-library.md        # B：暖/冷色温、光位、年代物件、声音、一致性工程
│   └── golden-example.md            # B：2006 小卖部 5 镜原文 + 8 条质量基线
└── scripts/
    └── build_prompt.py              # B：JSON → 完整规格书，--check 结构校验
```

## 安装

把本仓库内容放到 WorkBuddy 用户技能目录：

```
~/.workbuddy/skills/ai-video-prompt/
```

或使用 GitHub 的 **Download ZIP** 解压到该目录。技能由 `SKILL.md` 的 frontmatter 自动注册。

## 快速开始

体系 A：

```
帮我写张图片提示词：2012 年县城高中，18 岁男生李默的定妆照
```

体系 B：

```
用 STYLE LOCK 规格书把「面试间送客」写成 30 秒 5 镜
```

批量生成体系 B：

```bash
python scripts/build_prompt.py assets/example-config.json --check
python scripts/build_prompt.py assets/example-config.json -o output.md
```

`--check` 校验镜数、时间码合计、必填段、参考图编号；通过后才输出正文。

## 关键设计

- **四维分类 ≠ 书写顺序**：体系 A 用四维查漏，按「风格色调 → 时间 → 场景 → 主体 → 镜头 → 光源 → 氛围 → 画质」输出。
- **参考图只锚外观，不锁机位**：体系 B 的 `{{Image N}}` 明确声明边界，机位与动作一律以 CLIP 正文为准。
- **动线先于分镜**：空间与站位声明确立方位锚点和完整动线，防止跨镜跳轴。
- **声画逐镜对账**：段 5 的每一行都能在段 4 找到对应声源，跨室内外写明声场转换。
- **不写抽象情绪词**：一律改写为可拍摄的光位、材质、动作、物件。

## 来源与署名

- 体系 A 的维度框架源自**影视飓风《图片提示词》思维导图**；`references/visual-dimension-map.jpg` 为该导图原图，版权归原作者所有，此处仅作方法溯源。`references/dimension-library.md` 是其可读的文本化版本。
- 体系 B 的黄金示例与风格锁词库整理自自建 TapNow 画布 `Creative Concept (1016)` 与「全频道阻塞干扰」的视频节点提示词。
- 本仓库未附开源许可证，仅供个人学习与创作使用。如需正式开源许可，请联系仓库所有者。

## 版本

| 日期 | 内容 |
|---|---|
| 2026-11-08 | v2：确立两套并列体系；v1 为单镜头四维框架，已并入体系 A |

# 辅助模式 · 图片提示词规范（非主线）

> 影视飓风《图片提示词》四维框架，面向**单张静态图**。仅在用户明确要求设定图 / 定妆照 / 单张图时启用。
> 原图溯源 `references/visual-dimension-map.jpg`；完整维度选项见 `references/dimension-library.md`；可填模板见 `assets/image-prompt-template.md`。
> **不是与主体系并列的第二套体系，也不得替代五段规格书。** 主体系见 `references/spec-guide.md`。

## 一、适用与不适用

| 适用 | 不适用 |
|---|---|
| 角色设定图 / character sheet、场景空镜、道具三视图、单张主视觉、封面图 | 分镜脚本、30 秒成片、含对白的剧情、需跨镜保持动线与声画一致的内容 |
| 即梦 / Seedream / 可灵图片 / Midjourney / FLUX / SD | Seedance / Veo / Kling 的视频生成任务 |

出现「分镜 / 5 镜 / 30 秒 / 对白 / 声音设计 / STYLE LOCK / 参考图锚定」任一信号 → 切到主体系。

## 二、四维框架（查漏用，不是书写顺序）

| 维度 | 子项 |
|---|---|
| **时间** | 年代、季节、时刻 |
| **主体** | 人物（基础 / 脸部 / 身体 / 服装 / 表情 / 气质 / 姿势）、生物、物品 |
| **场景** | 自然（环境 / 植被）、建筑（年代 / 状态 / 结构 / 装潢）、天气 |
| **风格** | 画面风格、氛围、色调、光源（类型 / 位置 / 光质）、景别、拍摄角度、构图、摄影机（机型 / 焦段 / 焦点 / 透视） |

书写顺序见 `assets/image-prompt-template.md`。**维度分类 ≠ 输出顺序**：风格与色调在实际提示词里前置，其余按「时间 → 场景 → 主体 → 动作 → 镜头 → 光源 → 氛围 → 画质」拼接。

## 三、工作流

1. 解析用户创意，标出已给维度；通常只给了 1–2 个（如「一只猫在雨夜街头」）。
2. 用合理默认值补齐其余维度，**不反问超过一轮**；缺省值：傍晚 / 中景或特写 / 缓慢推进或固定 / 黄金时刻自然光或夜景霓虹 / 电影感写实。
3. 按 `assets/image-prompt-template.md` 的骨架拼接；强相关维度写细，弱相关一句带过。
4. 对照四维表查漏，重点查光源三件套（类型 / 位置 / 光质）与镜头四件套（景别 / 角度 / 构图 / 焦段）。
5. 输出中英双版 + 一行「可调参数」。

## 四、写法纪律

- 主体具体到「独一无二」：不写「一个男人」，写「穿藏青色风衣、戴圆框眼镜的中年男人」。
- 只写**一个**主动作；多个动作并列会让模型折中成一个模糊姿态。
- 运镜只选一种；图片提示词里运镜词用得越克制越好（静态图不需要运镜，用景别与角度即可）。
- 景别、角度、构图自洽：「特写 + 俯拍大全景」是矛盾组合。
- 抽象词换成可拍摄对象：「孤独」→「地面湿滑反射霓虹、单人居中偏左、大面积负空间」。
- 负面约束随平台能力附加，不强求。

## 五、黄金示例（角色设定图）

**任务**：为短片主角李默做 18 岁定妆照，需与 32 岁版本共用同一张脸。

**中文**

> 写实电影质感、文艺片色调，冷蓝灰低饱和，Fuji 400H 胶片颗粒。2012 年·秋·午后，中国县城民办高中，影棚内浅灰色地面与深灰蓝渐变背景纸。18 岁中国高三男生李默，瘦高，短黑发，黑框眼镜，白衬衫校服袖口扣到手腕，表情克制、不笑；站姿，双臂自然垂放，肩线略紧。全身入画，正面平视，居中构图，35mm 镜头，头顶留少量空间，脚部完整可见。双柔光箱正面平光 + 侧后方一道弱轮廓光，柔光质，镜片上有细窄高光，背景均匀无阴影。安静、拘谨。ARRI ALEXA 35 质感，浅景深，皮肤纹理真实，高分辨率。变形、多手指、面部崩坏、文字、水印、logo。

**English**

> Documentary-grade photorealistic portrait, art-house colour grading, cold blue-grey low saturation, Fuji 400H film grain. China, autumn 2012, afternoon. Studio with pale grey floor and deep grey-blue gradient backdrop. LI MO, an 18-year-old Chinese high school senior, tall and lean, short black hair, black-framed glasses, white school shirt buttoned at the cuffs, restrained expression, no smile; standing at ease, arms down, slightly tense shoulders. Full-body frontal eye-level shot, centred composition, 35mm lens, headroom preserved, shoes fully visible. Two frontal softboxes plus a weak rim light from behind, soft light quality, thin highlight on the lenses, even shadowless backdrop. Quiet, guarded. ARRI ALEXA 35 look, shallow depth of field, realistic skin texture, high resolution. No deformation, extra fingers, distorted face, text, watermark, logo.

**可调参数**：把「冷蓝灰」换「暖金 Fuji 400H」即切到主体系 里的 2000s 生日宴色温；把「正面平光」换「落地窗逆光」即得到室外版本。

**跨年龄一致性**：生成 32 岁版本时追加 `Same person as the attached 18-year-old character sheet`，并把本图作为参考图传入；详见 `references/style-lock-library.md` 第六节。

## 六、质检清单

1. 四维（时间 / 主体 / 场景 / 风格）均已覆盖或明确缺省。
2. 光源写明类型 + 位置 + 光质，并给出落地效果。
3. 景别、角度、构图、焦段四者自洽。
4. 主体具体到独一无二，只有一个主动作。
5. 无抽象情绪词、无「好看 / 高级感」类模糊表述。
6. 摄影机 / 胶片型号 / 画质参数至少给一项。
7. 负面约束已附；中英双版内容一致。
8. 附一行可调参数。
9. 若用户后续要「做成视频 / 分镜」，提示切换到主体系，不继续堆图。

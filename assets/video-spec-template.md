# 主体系 · 视频分镜规格书模板

> 结构来自唯一基准 https://app.tapnow.media/canvas/0e561120-5c2d-4bd8-821b-f5c532645ec5 的 30 秒 5 镜提示词，**但文本一律重写，不照搬原型的题材名词与句子**。原型原文见 `references/golden-example.md`。
> 五段固定顺序：风格锁 → 参考图锚定 → 空间与站位声明 → CLIP 正文 → BGM 与声音设计。
> 规范 `references/spec-guide.md`；参考图规则 `references/reference-image-protocol.md`（**写段 2 前必读**）；风格词 `references/style-lock-library.md`。
> 复制分隔线以内的正文填写。镜数、参考图数都可变，占位块按需增删行。

---

[STYLE LOCK] {ERA_PLACE}，{LOOK}。{CAMERA}。{LIGHTING}；{SET_DRESSING}；{CROWD}。{GRADE_PHYSICS}，{DIALOGUE_RULE}。

[参考图锚定]
{REF_BLOCK}

[空间与站位声明]
{SPATIAL_ANCHORS}。{SUBJECT_NAME}动线：{BLOCKING}。{CROSS_CLIP_CONTINUITY}

CLIP正文（{N}镜）
{CLIP_BLOCK}

[BGM & 声音设计]
底层环境：{SOUND_BED}
{SOUND_BLOCK}

---

<!-- 以下为填写说明，输出时删除 -->

## 占位块写法

| 占位块 | 怎么填 |
|---|---|
| `{REF_BLOCK}` | 一图一行，张数不限，按**挂载顺序**编号：`{{Image N}} = <是什么>：提供 <锁定什么>；不提供 <不该干涉什么>；冲突以正文为准。` 0 张时写一行 `本片不使用参考图：主体外观与空间结构以段 1 与正文文字描述为准。` |
| `{CLIP_BLOCK}` | 一镜一段，每段以机位开头，五成分顺序固定：机位运镜 → 连续动作 → 前后景虚焦 → 群演 → 画外对白 |
| `{SOUND_BLOCK}` | 一镜一行：`镜N：<音效>·<对白>·<环境声>` |

## 单值占位符

| 占位符 | 填写要点 |
|---|---|
| `ERA_PLACE` | 年代 + 国家/地区 + 具体空间 + 内/外景 |
| `LOOK` | 写实电影质感、色调、画幅、景深 |
| `CAMERA` | 全片统一运镜体系，不逐镜换（如 `全程手持摇晃镜头 Handheld Camera with natural breathing motion`） |
| `LIGHTING` | 光源种类、位置、色温、落地效果——光位三件套最易漏 |
| `SET_DRESSING` | 可辨识年代的具体物件，写到品类与状态，不写「一些货架」 |
| `CROWD` | 时间 + 人群 + 服装 + 行为 |
| `GRADE_PHYSICS` | 胶片质感、偏色、物理真实性 |
| `DIALOGUE_RULE` | 必写 `画外所有说话声均为清晰中文语句`；无对白片写 `本片无对白` |
| `SPATIAL_ANCHORS` | 方位锚点，一条一物件：`<物件>在<方位>·<出口>在<它>的<左/右>` |
| `SUBJECT_NAME` | 主体名字或代称 |
| `BLOCKING` | 完整动线，`→` 串联，覆盖入场到出画 |
| `CROSS_CLIP_CONTINUITY` | 跨镜持续状态，如「末镜背景仍有<谁>在<做什么>」 |
| `N` | 镜数，默认 5，随总时长调整 |
| `SOUND_BED` | 贯穿全片环境声 + 声场转换说明 |

## 硬性检查

风格锁只写全场固定项 · 参考图不锁机位且编号与挂载顺序一致 · 动线不跳轴 · 主体外观不重复描述 · 末镜有收束 · 末尾附负面约束与参数建议（含挂载对账行）。

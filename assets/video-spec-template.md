# 主体系 · 视频分镜规格书模板

> 由唯一基准 https://app.tapnow.media/canvas/0e561120-5c2d-4bd8-821b-f5c532645ec5 的 30 秒 5 镜提示词反推；原型原文见 `references/golden-example.md`。
> 五段固定顺序：风格锁 → 参考图锚定 → 空间与站位声明 → CLIP 正文 → BGM 与声音设计。
> 规范见 `references/spec-guide.md`；质量基线见 `references/golden-example.md`；风格词查 `references/style-lock-library.md`。
> 复制下方分隔线以内的正文填写。首段 `[STYLE LOCK]` 标签可保留（画布视频节点写法），也可按黄金范例去掉，两种格式均有效。

---

[STYLE LOCK] {ERA_PLACE}，{LOOK}。{CAMERA}。{LIGHTING}；{SET_DRESSING}；{CROWD}。{GRADE_PHYSICS}，画外所有说话声均为清晰中文语句。

[参考图锚定]
{{Image 1}} = {CHARACTER_REF_NAME}：仅提供面部与服装参考。本场{CHARACTER_NAME}{STATE_NOTE}（与参考图一致）；{WARDROBE_NOTE}——以本条正文分镜状态为准。
{{Image 2}} = {SCENE_REF_NAME}：提供空间结构（{SPATIAL_ELEMENTS}）、{LIGHT_POSITION}、年代质感与{COLOR_GRADE}——各镜机位由正文定义。
{ADDITIONAL_REFS}

[空间与站位声明]
{SPATIAL_ANCHORS}。{CHARACTER_NAME}动线：{BLOCKING}。{CROSS_CLIP_CONTINUITY}

CLIP正文（{N}镜）
{CLIP_1}
{CLIP_2}
{CLIP_3}
{CLIP_4}
{CLIP_5}

[BGM & 声音设计]
底层环境：{SOUND_BED}
镜1：{SOUND_1}
镜2：{SOUND_2}
镜3：{SOUND_3}
镜4：{SOUND_4}
镜5：{SOUND_5}

---

<!-- 以下为填写说明，输出时删除 -->

| 占位符 | 填写要点 |
|---|---|
| `ERA_PLACE` | 年代 + 国家/地区 + 具体空间 + 内/外景 |
| `LOOK` | 写实电影质感、文艺片色调、画幅、景深 |
| `CAMERA` | 全片统一运镜，如「全程手持摇晃镜头 Handheld Camera with natural breathing motion」 |
| `LIGHTING` | 光源种类、位置、色温、落地效果 |
| `SET_DRESSING` | 可辨识年代的具体物件，不写「一些货架」 |
| `CROWD` | 时间 + 人群 + 服装 + 行为 |
| `GRADE_PHYSICS` | 胶片质感、偏色、物理真实性 |
| `STATE_NOTE` / `WARDROBE_NOTE` | 本场状态（眼镜、发型、衣着）与服装说明 |
| `SPATIAL_ELEMENTS` | 关键物件清单，括号列出 |
| `SPATIAL_ANCHORS` | 方位锚点：「X 在中后部·Y 站 X 后·出口在 X 左侧」 |
| `BLOCKING` | 完整动线，用 `→` 串联，覆盖入场到出画 |
| `CROSS_CLIP_CONTINUITY` | 跨镜持续状态，如「镜5门内仍排着队伍」 |
| `CLIP_n` | 机位 + 连续动作 + 前后景虚焦 + 群演 + 画外对白（中文原句、标注唇音同步） |
| `SOUND_BED` | 贯穿全片环境声 + 声场转换说明 |
| `SOUND_n` | 逐镜音效，与 CLIP 内声音标记一一对应 |

**每镜五成分顺序**：机位与运镜 → 主体连续动作（含物理细节）→ 前景/背景虚焦 → 群演动作 → 画外对白。

**硬性检查**：风格锁只写全场固定项；参考图不锁机位；动线不跳轴；主体外观不重复描述；末镜有收束动作；末尾附负面约束与模型参数。

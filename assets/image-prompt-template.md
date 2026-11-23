# 辅助模式 · 图片提示词模板（非主线）

> 静态图查漏八步（完整选项见 `references/dimension-library.md`）。用于**单张静态图**。
> 八步用于查漏，书写顺序用于输出——两者不要混为一谈。

## 书写顺序（输出时按此拼接）

```
[画面风格 + 色调]，[时间]。[场景 + 天气]，[主体描述]，[动作 / 姿态]。
[镜头语言：景别 + 角度 + 构图]。[光源：类型 + 位置 + 光质]。[氛围]。
[摄影机 / 画质参数]。[负面约束]
```

## 带占位符骨架

```
{STYLE_AND_GRADE}。{TIME_ERA}·{SEASON}·{TIME_OF_DAY}，{SCENE}·{WEATHER}。
{SUBJECT_BASE}；{FACE_DETAIL}；{BODY_DETAIL}；{WARDROBE}；{EXPRESSION}；{POSE}。
{SHOT_SIZE}、{ANGLE}、{COMPOSITION}，{FOCAL}镜头。{LIGHT_TYPE}·{LIGHT_POSITION}·{LIGHT_QUALITY}，{LIGHT_EFFECT}。
{MOOD}。{CAMERA_BODY}质感，{DEPTH_OF_FIELD}，{FILM_STOCK}，{RESOLUTION}。
{NEGATIVE}
```

## 占位符与八步对照

| 占位符 | 所属步骤 | 填写要点 |
|---|---|---|
| `STYLE_AND_GRADE` | 2 定调 | 写实向或动画向的具体门类 + 具体色名，不写「高级感」 |
| `TIME_ERA` / `SEASON` / `TIME_OF_DAY` | 1 定点 | 年代、季节、时刻三选一二即可，不必填满 |
| `SCENE` / `WEATHER` | 4 定景 | 环境 / 建筑形制 / 天气；有年代感时写具体物件 |
| `SUBJECT_BASE` … `POSE` | 5 定主体 | 按「基础→脸部→身体→服装→表情→姿势」七层过；生物 / 物品见 `references/dimension-library.md` |
| `SHOT_SIZE` / `ANGLE` / `COMPOSITION` / `FOCAL` | 6 定镜头 | 景别、角度、构图、焦段四者必须自洽 |
| `LIGHT_TYPE` / `LIGHT_POSITION` / `LIGHT_QUALITY` / `LIGHT_EFFECT` | 3 定光 | **最常漏项**：性质、方位、光质、落地效果 |
| `MOOD` | 2 定调 | 只写可拍摄的氛围词，避免抽象评价 |
| `CAMERA_BODY` / `DEPTH_OF_FIELD` / `FILM_STOCK` / `RESOLUTION` | 6 定镜头 | 机型或胶片型号 + 景深 + 画质参数 |
| `NEGATIVE` | 8 排除 | 变形、多手指、面部崩坏、文字、水印、logo |

## 输出格式

默认给**两版**：中文版（即梦 / Seedream / 可灵图片）与英文版（Midjourney / FLUX / SD）。用户只要一种时只给一种。

```
中文：
<按骨架拼好的一段，100–200 字>

English:
<same content, 80–150 words>

可调参数：把 X 换成 Y 会改变 Z（一行即可）
```

## 边界

需要**多镜头、对白、动线、声音、跨镜一致性**时，不要用本模板累积多张图去拼——切换到**主体系 · 视频规格书**（`assets/video-spec-template.md`）。

#!/usr/bin/env python3
"""Assemble a five-part AI video prompt spec from a JSON config.

Usage:
    python build_prompt.py <config.json> [-o output.md] [--check] [--manifest]

With --check, validate structure only and print a report.
With --manifest, print only the reference-image reconciliation table.

No third-party dependencies; Python 3.9+.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REQUIRED_STYLE_KEYS = (
    "era_place", "look", "camera", "lighting",
    "set_dressing", "crowd", "grade", "dialogue_rule",
)
REQUIRED_TOP_KEYS = (
    "style_lock", "reference_images", "spatial", "clips", "sound",
)

# Soft-check thresholds per style of film. Keys are tokens looked up in clip bodies.
# Not every shot carries every marker: a product film has no off-screen dialogue,
# an empty-scene montage may have no camera handling at all.
CHECK_PROFILES = {
    "dialogue": {"前景": 3, "背景": 3, "手持": 2, "画外": 2},
    "no_dialogue": {"前景": 3, "背景": 3, "手持": 2},
    "product": {"前景": 2, "背景": 2},
    "montage": {"前景": 2, "背景": 2},
}


def load_config(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def parse_tc(span: str) -> float:
    """Parse 'MM:SS-MM:SS' into seconds."""
    m = re.fullmatch(r"(\d{2}):(\d{2})\s*-\s*(\d{2}):(\d{2})", span.strip())
    if not m:
        raise ValueError(f"bad time code: {span!r} (expected MM:SS-MM:SS)")
    a, b, c, d = (int(x) for x in m.groups())
    start, end = a * 60 + b, c * 60 + d
    if end <= start:
        raise ValueError(f"non-positive clip length: {span!r}")
    return end - start


def norm_refs(cfg: dict) -> list[dict]:
    """Normalise reference images.

    Slot is always derived from position: the Nth attached image is Image N.
    Accepts both the short form (name / provides / note) and the full form
    (name / provides / withholds / conflict).
    """
    refs = cfg.get("reference_images") or []
    out: list[dict] = []
    for i, ref in enumerate(refs, 1):
        item = dict(ref)
        item["slot"] = f"Image {i}"
        item["withholds"] = ref.get("withholds") or ""
        item["conflict"] = ref.get("conflict") or ""
        item["note"] = ref.get("note") or ""
        out.append(item)
    return out


def ref_line(ref: dict) -> str:
    """Render one reference row. Structure: what it is; what it locks; what it must not."""
    parts = [ref["provides"]] if ref.get("provides") else []
    if ref.get("withholds"):
        parts.append(ref["withholds"])
    if ref.get("note"):
        parts.append(ref["note"])
    if ref.get("conflict"):
        parts.append(ref["conflict"])
    body = "；".join(p.strip("；。 ") for p in parts if p.strip("；。 ")) or "提供参考"
    return f"{{{{{ref['slot']}}}}} = {ref['name']}：{body}。"


def manifest(cfg: dict) -> str:
    """Reconciliation table: placeholder -> attachment order -> what it locks."""
    refs = norm_refs(cfg)
    if not refs:
        return "参考图挂载顺序：本片不使用参考图（提示词内无 {{Image N}} 占位，需以文字描述主体与场景）。"
    lines = ["参考图挂载顺序（必须与生成节点内图片排列顺序一致，错位则编号全错）："]
    for ref in refs:
        lock = ref.get("provides") or "提供参考"
        lines.append(f"  {ref['slot']} = {ref['name']}（{lock}）")
    return "\n".join(lines)


def validate(cfg: dict) -> list[str]:
    """Return a list of problems. Empty list means valid."""
    problems: list[str] = []
    for key in REQUIRED_TOP_KEYS:
        if key not in cfg:
            problems.append(f"missing top-level key: {key}")
    if problems:
        return problems

    sl = cfg["style_lock"]
    for key in REQUIRED_STYLE_KEYS:
        if not sl.get(key):
            problems.append(f"style_lock.{key} is empty")

    # Zero reference images is a legal configuration (degraded mode), not an error.
    for i, ref in enumerate(cfg.get("reference_images") or [], 1):
        if not ref.get("name"):
            problems.append(f"reference_images[{i}].name is empty")
        if not ref.get("provides"):
            problems.append(f"reference_images[{i}].provides is empty")
        if not (ref.get("withholds") or ref.get("note")):
            problems.append(
                f"reference_images[{i}] has no boundary field: "
                "add 'withholds' (what it must NOT control) or 'note'"
            )
        if not ref.get("conflict") and not ref.get("note"):
            problems.append(
                f"reference_images[{i}] has no conflict rule: "
                "add 'conflict' e.g. '冲突以正文为准'"
            )
        if ref.get("slot") and ref["slot"] != f"Image {i}":
            problems.append(
                f"reference_images[{i}].slot is {ref['slot']!r} but position implies 'Image {i}'; "
                "slot must follow attachment order"
            )

    sp = cfg["spatial"]
    for key in ("anchors", "blocking", "continuity"):
        if not sp.get(key):
            problems.append(f"spatial.{key} is empty")

    clips = cfg["clips"]
    expected = cfg.get("clip_count", len(clips))
    if len(clips) != expected:
        problems.append(f"clip count {len(clips)} != clip_count {expected}")
    total = 0.0
    prev_end = None
    for i, clip in enumerate(clips, 1):
        if not clip.get("body"):
            problems.append(f"clips[{i}].body is empty")
        try:
            dur = parse_tc(clip.get("tc", ""))
            total += dur
            m = re.match(r"(\d{2}):(\d{2})", clip["tc"])
            start = int(m.group(1)) * 60 + int(m.group(2))
            if prev_end is not None and start != prev_end:
                problems.append(f"clips[{i}] time code is not continuous with previous clip")
            prev_end = start + dur
        except (ValueError, KeyError, TypeError) as exc:
            problems.append(f"clips[{i}]: {exc}")

    duration = cfg.get("duration", total)
    if abs(total - duration) > 0.01:
        problems.append(f"time codes sum to {total}s, expected {duration}s")

    sound = cfg["sound"]
    if not sound.get("bed"):
        problems.append("sound.bed is empty")
    per_clip = sound.get("per_clip", [])
    if len(per_clip) != len(clips):
        problems.append(f"sound.per_clip has {len(per_clip)} rows, expected {len(clips)}")
    for i, row in enumerate(per_clip, 1):
        if not row:
            problems.append(f"sound.per_clip[{i}] is empty")

    return problems


def warnings(cfg: dict) -> list[str]:
    """Soft checks at whole-clip level. Thresholds come from check_profile."""
    out: list[str] = []
    clips = cfg.get("clips", [])
    n = len(clips)
    if not n:
        return out

    profile_name = cfg.get("check_profile", "dialogue")
    profile = CHECK_PROFILES.get(profile_name)
    if profile is None:
        out.append(
            f"unknown check_profile {profile_name!r}; "
            f"use one of {sorted(CHECK_PROFILES)}"
        )
        return out

    def count(token: str) -> int:
        return sum(1 for c in clips if token in c.get("body", ""))

    for token, minimum in profile.items():
        got = count(token)
        if got < minimum:
            out.append(f"only {got}/{n} clips carry '{token}'; target >= {minimum}")

    if not cfg.get("negative"):
        out.append("no negative constraints declared")
    return out


def _sentences(value) -> str:
    """Join a list of fragments into one sentence block, without a trailing period."""
    if isinstance(value, list):
        items = [str(x).strip().rstrip("。；") for x in value if str(x).strip()]
        return "。".join(items)
    return str(value).strip().rstrip("。；")


def build(cfg: dict) -> str:
    sl = cfg["style_lock"]
    look = sl["look"]
    look_text = "，".join(look) if isinstance(look, list) else str(look)
    look_text = look_text.strip().rstrip("。；")
    head = (
        f"{_sentences(sl['era_place'])}，{look_text}。{_sentences(sl['camera'])}。"
        f"{_sentences(sl['lighting'])}；{_sentences(sl['set_dressing'])}；{_sentences(sl['crowd'])}。"
        f"{_sentences(sl['grade'])}，{_sentences(sl['dialogue_rule'])}。"
    )

    lines = [head, "[参考图锚定]"]
    refs = norm_refs(cfg)
    if refs:
        for ref in refs:
            lines.append(ref_line(ref))
    else:
        lines.append(
            "本片不使用参考图：主体外观与空间结构以段1与正文文字描述为准，冲突以正文为准。"
        )

    sp = cfg["spatial"]
    anchors = _sentences(sp["anchors"])
    continuity = _sentences(sp["continuity"])
    blocking = _sentences(sp["blocking"])
    subject = cfg.get("subject") or sp.get("subject") or "主体"
    lines.append("[空间与站位声明]")
    lines.append(f"{anchors}。{subject}动线：{blocking}。{continuity}。")

    lines.append(f"CLIP正文（{len(cfg['clips'])}镜）")
    for clip in cfg["clips"]:
        lines.append(clip["body"])

    sound = cfg["sound"]
    lines.append("[BGM & 声音设计]")
    lines.append(f"底层环境：{sound['bed']}")
    for i, row in enumerate(sound["per_clip"], 1):
        lines.append(f"镜{i}：{row}")

    if cfg.get("negative"):
        lines.append("负面约束：" + "、".join(cfg["negative"]) + "。")

    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("config", type=Path, help="path to the JSON config")
    ap.add_argument("-o", "--output", type=Path, help="write prompt to this file")
    ap.add_argument("--check", action="store_true", help="validate only, print report")
    ap.add_argument("--manifest", action="store_true", help="print reference reconciliation only")
    args = ap.parse_args()

    try:
        cfg = load_config(args.config)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot load config: {exc}", file=sys.stderr)
        return 2

    if args.manifest:
        print(manifest(cfg))
        return 0

    problems = validate(cfg)
    soft = warnings(cfg)
    refs = norm_refs(cfg)
    print(f"[check] {args.config.name}: {'PASS' if not problems else 'FAIL'} "
          f"({len(cfg.get('clips', []))} clips, {cfg.get('duration', '?')}s, {len(refs)} refs)")
    for p in problems:
        print(f"  ERROR  {p}")
    for w in soft:
        print(f"  WARN   {w}")
    print("--- MANIFEST ---")
    print(manifest(cfg))

    if problems or args.check:
        return 1 if problems else 0

    text = build(cfg)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
        print(f"[write] {args.output} ({len(text)} chars)")
    else:
        print("--- PROMPT ---")
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

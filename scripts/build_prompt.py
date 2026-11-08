#!/usr/bin/env python3
"""Assemble a five-part AI video prompt spec from a JSON config.

Usage:
    python build_prompt.py <config.json> [-o output.md] [--check]

With --check, validate structure only and print a report.
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

    refs = cfg["reference_images"]
    if not refs:
        problems.append("reference_images is empty")
    for i, ref in enumerate(refs, 1):
        if ref.get("slot") != f"Image {i}":
            problems.append(f"reference_images[{i}].slot should be 'Image {i}'")
        for key in ("name", "provides", "note"):
            if not ref.get(key):
                problems.append(f"reference_images[{i}].{key} is empty")

    sp = cfg["spatial"]
    for key in ("anchors", "blocking", "continuity"):
        if not sp.get(key):
            problems.append(f"spatial.{key} is empty")

    clips = cfg["clips"]
    expected = cfg.get("clip_count", 5)
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

    duration = cfg.get("duration", 30)
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
    """Soft checks at whole-clip level. A single clip need not carry every marker."""
    out: list[str] = []
    clips = cfg.get("clips", [])
    n = len(clips)

    def count(token: str) -> int:
        return sum(1 for c in clips if token in c.get("body", ""))

    # Thresholds follow the golden example: not every shot has dialogue,
    # but depth cues and camera handling must recur throughout the clip.
    for token, minimum, label in (
        ("前景", 3, "foreground blur"),
        ("背景", 3, "background blur"),
        ("手持", 2, "camera handling"),
        ("画外", 2, "off-screen dialogue"),
    ):
        got = count(token)
        if got < minimum:
            out.append(f"only {got}/{n} clips carry '{token}' ({label}); target >= {minimum}")

    if not cfg.get("negative"):
        out.append("no negative constraints declared")
    return out


def build(cfg: dict) -> str:
    sl = cfg["style_lock"]
    look = sl["look"]
    look_text = "，".join(look) if isinstance(look, list) else str(look)
    head = (
        f"{sl['era_place']}，{look_text}。{sl['camera']}。"
        f"{sl['lighting']}；{sl['set_dressing']}；{sl['crowd']}。"
        f"{sl['grade']}，{sl['dialogue_rule']}。"
    )

    lines = [head, "[参考图锚定]"]
    for ref in cfg["reference_images"]:
        lines.append(
            f"{{{{{ref['slot']}}}}} ={ref['name']}：{ref['provides']}。{ref['note']}。"
        )

    sp = cfg["spatial"]
    anchors = "".join(sp["anchors"]) if isinstance(sp["anchors"], list) else sp["anchors"]
    continuity = "".join(sp["continuity"]) if isinstance(sp["continuity"], list) else sp["continuity"]
    lines.append("[空间与站位声明]")
    lines.append(f"{anchors}。{cfg.get('subject', '主体')}动线：{sp['blocking']}。{continuity}")

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
    args = ap.parse_args()

    try:
        cfg = load_config(args.config)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot load config: {exc}", file=sys.stderr)
        return 2

    problems = validate(cfg)
    soft = warnings(cfg)
    print(f"[check] {args.config.name}: {'PASS' if not problems else 'FAIL'} "
          f"({len(cfg.get('clips', []))} clips, {cfg.get('duration', '?')}s)")
    for p in problems:
        print(f"  ERROR  {p}")
    for w in soft:
        print(f"  WARN   {w}")

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

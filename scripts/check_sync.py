from __future__ import annotations

from pathlib import Path

GUIDES = [
    "docs/tutorial_en.md",
    "docs/tutorial_es.md",
    "docs/tutorial_zh-CN.md",
    "docs/tutorial_hi.md",
    "docs/tutorial_pt-BR.md",
    "docs/tutorial_fr.md",
    "docs/tutorial_ar.md",
    "docs/tutorial_ja.md",
    "docs/tutorial_ko.md",
]

REQUIRED_LITERALS = [
    "T1:val",
    "T2:embryo:val_interp",
    "T2:heart:val_extrap",
    "T2:heart:val_interp",
    "T3:gata4",
    "32,285",
    "5,118",
    "583",
    "5,000",
    "25,179",
    "17,616",
    "7,449",
    'obsm["spatial_3D"]',
    "vec_community_baselines.make_baseline",
    "vec_submit_check",
    "vec_local_score",
    "vec_agent_evidence",
    "https://virtualembryo.ai/challenge/data",
    "https://virtualembryo.ai/challenge/rules",
]


def main() -> int:
    failed = False

    for filename in GUIDES:
        path = Path(filename)
        if not path.exists():
            print(f"FAIL missing guide: {filename}")
            failed = True
            continue

        text = path.read_text(encoding="utf-8")
        missing = [literal for literal in REQUIRED_LITERALS if literal not in text]
        if missing:
            print(f"FAIL {filename}: missing {missing}")
            failed = True
        else:
            print(f"PASS {filename}")

    if failed:
        return 1

    print(f"PASS: {len(GUIDES)} synchronized language guides")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

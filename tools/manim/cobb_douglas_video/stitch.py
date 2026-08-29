"""Concatenate the per-scene renders into the full episode (stream copy).

Usage: python stitch.py <media_root> <quality_dir> <out.mp4>
e.g.:  python stitch.py .../media 480p15 episode1_ql.mp4
"""
import subprocess
import sys
import tempfile
from pathlib import Path

EPISODE_ORDER = [
    ("s0_intro", "Intro"),
    ("s1_warmup", "Warmup1D"),
    ("s2_expression", "Expression"),
    ("s34_surface", "SurfaceToIsoquants"),
    ("s5_mrts", "MRTS"),
    ("s6_homothetic", "Homothetic"),
    ("s7_outro", "Outro"),
]


def main(media_root: str, quality: str, out: str) -> None:
    root = Path(media_root) / "videos"
    clips = []
    for module, scene in EPISODE_ORDER:
        p = root / module / quality / f"{scene}.mp4"
        if not p.exists():
            raise SystemExit(f"missing clip: {p}")
        clips.append(p)
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False,
                                     encoding="utf-8") as f:
        for c in clips:
            f.write(f"file '{c.as_posix()}'\n")
        listfile = f.name
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0",
                    "-i", listfile, "-c", "copy", out], check=True)
    print(f"stitched {len(clips)} clips -> {out}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])

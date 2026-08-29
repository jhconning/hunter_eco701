"""Dump frames from a rendered mp4 to PNGs for visual QA.

Usage: python qa_frames.py <video.mp4> <out_dir> [every_n_frames]
"""
import sys
from pathlib import Path

import av


def dump(mp4: str, out_dir: str, every: int = 15) -> None:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    stem = Path(mp4).stem
    with av.open(mp4) as container:
        stream = container.streams.video[0]
        n_saved = 0
        for i, frame in enumerate(container.decode(stream)):
            if i % every == 0:
                frame.to_image().save(out / f"{stem}_f{i:05d}.png")
                n_saved += 1
        # always save the last frame too
        frame.to_image().save(out / f"{stem}_f{i:05d}_last.png")
    print(f"saved {n_saved + 1} frames from {mp4} ({i + 1} total frames) -> {out}")


if __name__ == "__main__":
    dump(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 15)

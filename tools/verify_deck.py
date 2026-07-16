"""
Verification tool: builds a topic's deck.md with the CI-pinned marp-cli,
rasterizes every slide, and flags pages that look like they might have
overflowing content (equations or text running past the canvas edge).

This formalizes a manual loop repeated many times during this project's
conversion sessions: build against the *exact* toolchain CI uses (not
whatever locally-installed marp-cli happens to be newer), rasterize with
PyMuPDF, and look for content bleeding into the margins. See HANDOFF.md's
gotchas for the two failure modes this catches - vertical overflow (a bottom
bullet/footer collision) and horizontal overflow (an equation line running
off the right edge) - both previously only caught by eyeballing every page
by hand.

This is advisory, not a hard pass/fail: it flags pixels near the canvas
edges that differ from the slide's own background color, which is a good
proxy for "content got pushed somewhere it shouldn't be" but can still
have false positives (e.g. a deliberately full-bleed image) or false
negatives (overflow that happens to still be background-colored). Always
look at the flagged pages - and ideally a sample of the rest - before
trusting a deck is clean.

Usage:
    mamba run -n ecopy python tools/verify_deck.py --topic 02_constrained-optimization
    mamba run -n ecopy python tools/verify_deck.py --topic slides/03_production-optimization --dpi 110
    mamba run -n ecopy python tools/verify_deck.py --topic 02_constrained-optimization --keep-pdf

Writes rasterized PNGs + a text report to _verify/<topic>/ at the repo root
(gitignored - this is scratch output, not a deliverable).
"""
import argparse
import os
import subprocess
import sys

import fitz  # PyMuPDF
from PIL import Image

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MARP_VERSION = "4.2.3"  # keep in sync with .github/workflows/deploy-myst.yml
EDGE_FRACTION = 0.012  # fraction of width/height treated as "the margin band"
BG_SAMPLE_SIZE = 6  # px square sampled from each corner to determine background
DEVIATION_THRESHOLD = 40  # per-channel RGB distance from background to count as "content"


def resolve_topic_dir(topic_arg):
    candidate = topic_arg
    if not os.path.isabs(candidate):
        candidate = os.path.join(REPO_ROOT, candidate)
    if os.path.isdir(candidate) and os.path.isfile(os.path.join(candidate, "deck.md")):
        return candidate
    # allow bare folder name, e.g. "02_constrained-optimization"
    candidate2 = os.path.join(REPO_ROOT, "slides", topic_arg)
    if os.path.isdir(candidate2) and os.path.isfile(os.path.join(candidate2, "deck.md")):
        return candidate2
    raise SystemExit(f"Could not find a deck.md for topic '{topic_arg}' "
                      f"(tried {candidate} and {candidate2})")


def build_pdf(deck_dir, out_pdf):
    theme = os.path.join(REPO_ROOT, "slides", "_shared", "eco701-theme.css")
    deck_md = os.path.join(deck_dir, "deck.md")
    print(f"Building with marp-cli v{MARP_VERSION}: {os.path.relpath(deck_md, REPO_ROOT)}")

    if os.name == "nt":
        # Invoke via Git Bash specifically (not cmd.exe, and not whatever "bash" a
        # plain PATH lookup finds first - on a machine with WSL installed, that's
        # WSL's bash, which can't translate Windows drive-letter paths like Y:\...
        # and fails outright). npx's .cmd shim also hits an ESM/CJS resolution
        # error under plain Windows subprocess+shell=True on this machine's Node
        # install, so cmd.exe isn't a fallback either - Git Bash is the one
        # confirmed-working invocation path.
        git_bash_candidates = [
            r"C:\Program Files\Git\bin\bash.exe",
            r"C:\Program Files (x86)\Git\bin\bash.exe",
        ]
        bash_exe = next((p for p in git_bash_candidates if os.path.isfile(p)), None)
        if bash_exe is None:
            raise SystemExit(
                "Could not find Git Bash (checked Program Files and Program Files (x86)). "
                "verify_deck.py needs it to invoke npx reliably on Windows - "
                "install Git for Windows or adjust git_bash_candidates in this script."
            )
        shell_cmd = (
            f'npx --yes @marp-team/marp-cli@{MARP_VERSION} '
            f'"{deck_md}" -o "{out_pdf}" --pdf --allow-local-files --theme-set "{theme}"'
        )
        cmd = [bash_exe, "-lc", shell_cmd]
        result = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    else:
        cmd = [
            "npx", "--yes", f"@marp-team/marp-cli@{MARP_VERSION}",
            deck_md, "-o", out_pdf,
            "--pdf", "--allow-local-files",
            "--theme-set", theme,
        ]
        result = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)

    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
        raise SystemExit(f"marp-cli build failed (exit {result.returncode})")
    if not os.path.isfile(out_pdf):
        raise SystemExit("marp-cli reported success but no PDF was produced")


def edge_band_has_content(img, bg):
    """Check whether any of the four edge bands contain non-background pixels."""
    w, h = img.size
    band_x = max(2, int(w * EDGE_FRACTION))
    band_y = max(2, int(h * EDGE_FRACTION))
    px = img.load()
    flagged_edges = []

    def deviates(p):
        return any(abs(p[i] - bg[i]) > DEVIATION_THRESHOLD for i in range(3))

    # sample every few pixels along each band, not every single pixel (speed)
    step = 3

    def check_region(x_range, y_range, label):
        for x in x_range:
            for y in y_range:
                if deviates(px[x, y]):
                    return True
        return False

    if check_region(range(0, w, step), range(0, band_y), "top"):
        flagged_edges.append("top")
    if check_region(range(0, w, step), range(h - band_y, h), "bottom"):
        flagged_edges.append("bottom")
    if check_region(range(0, band_x), range(0, h, step), "left"):
        flagged_edges.append("left")
    if check_region(range(w - band_x, w), range(0, h, step), "right"):
        flagged_edges.append("right")

    return flagged_edges


def sample_background(img):
    w, h = img.size
    corners = [(0, 0), (w - BG_SAMPLE_SIZE, 0), (0, h - BG_SAMPLE_SIZE), (w - BG_SAMPLE_SIZE, h - BG_SAMPLE_SIZE)]
    px = img.load()
    samples = []
    for cx, cy in corners:
        for dx in range(BG_SAMPLE_SIZE):
            for dy in range(BG_SAMPLE_SIZE):
                samples.append(px[cx + dx, cy + dy][:3])
    # most common corner color, by simple averaging (corners are solid background in every slide seen so far)
    r = sum(s[0] for s in samples) // len(samples)
    g = sum(s[1] for s in samples) // len(samples)
    b = sum(s[2] for s in samples) // len(samples)
    return (r, g, b)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--topic", required=True, help="Topic folder name (e.g. 02_constrained-optimization) or path")
    ap.add_argument("--dpi", type=int, default=110, help="Rasterization DPI (default 110, matches this project's convention)")
    ap.add_argument("--out-dir", default=None, help="Where to write rasters + report (default: _verify/<topic>/)")
    ap.add_argument("--keep-pdf", action="store_true", help="Keep the built PDF in the output dir instead of discarding it")
    args = ap.parse_args()

    deck_dir = resolve_topic_dir(args.topic)
    topic_name = os.path.basename(deck_dir.rstrip("/\\"))
    out_dir = args.out_dir or os.path.join(REPO_ROOT, "_verify", topic_name)
    os.makedirs(out_dir, exist_ok=True)

    pdf_path = os.path.join(out_dir, f"{topic_name}.pdf")
    build_pdf(deck_dir, pdf_path)

    doc = fitz.open(pdf_path)
    print(f"Rasterizing {doc.page_count} pages at {args.dpi} DPI...")

    flagged = []
    for i in range(doc.page_count):
        page = doc[i]
        pix = page.get_pixmap(dpi=args.dpi)
        png_path = os.path.join(out_dir, f"page{i + 1:03d}.png")
        pix.save(png_path)

        img = Image.open(png_path).convert("RGB")
        bg = sample_background(img)
        edges = edge_band_has_content(img, bg)
        if edges:
            flagged.append((i + 1, edges))

    page_count = doc.page_count
    doc.close()
    if not args.keep_pdf:
        os.remove(pdf_path)

    report_path = os.path.join(out_dir, "report.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"Verification report for {topic_name}\n")
        f.write(f"{page_count} pages checked, {len(flagged)} flagged\n\n")
        if flagged:
            for page_num, edges in flagged:
                line = f"page{page_num:03d}.png - possible overflow near: {', '.join(edges)}\n"
                f.write(line)
        else:
            f.write("No edge-bleed detected. Still worth spot-checking a sample by eye.\n")

    print(f"\n{len(flagged)} of {page_count} pages flagged for review:")
    for page_num, edges in flagged:
        print(f"  page{page_num:03d}.png - possible overflow near: {', '.join(edges)}")
    if not flagged:
        print("  (none - but this is a heuristic, not a guarantee; spot-check a sample anyway)")
    print(f"\nRasters + report written to {os.path.relpath(out_dir, REPO_ROOT)}/")


if __name__ == "__main__":
    main()

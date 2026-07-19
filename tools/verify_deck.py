"""
Verification tool: builds a topic's deck (Quarto `deck.qmd`, or the legacy
Marp `deck.md` for any topic not yet migrated), rasterizes every slide, and
flags pages that look like they might have overflowing content (equations
or text running past the canvas edge).

This formalizes a manual loop repeated many times during this project's
conversion sessions: build against the *exact* toolchain CI uses, rasterize
with PyMuPDF, and look for content bleeding into the margins. See
HANDOFF.md's gotchas for the two failure modes this catches - vertical
overflow (a bottom bullet/footer collision) and horizontal overflow (an
equation line running off the right edge) - both previously only caught by
eyeballing every page by hand. The rasterize-and-flag logic below is engine-
agnostic; only the build step differs between Quarto and (legacy) Marp.

This is advisory, not a hard pass/fail: it flags pixels near the canvas
edges that differ from the slide's own background color, which is a good
proxy for "content got pushed somewhere it shouldn't be" but can still
have false positives (e.g. a deliberately full-bleed image) or false
negatives (overflow that happens to still be background-colored). Always
look at the flagged pages - and ideally a sample of the rest - before
trusting a deck is clean.

Usage:
    mamba run -n ecopy python tools/verify_deck.py --topic 01_definitions-and-key-tools
    mamba run -n ecopy python tools/verify_deck.py --topic slides/03_production-optimization --dpi 110
    mamba run -n ecopy python tools/verify_deck.py --topic 02_constrained-optimization --keep-pdf

Writes rasterized PNGs + a text report to _verify/<topic>/ at the repo root
(gitignored - this is scratch output, not a deliverable).
"""
import argparse
import glob
import os
import shutil
import stat
import subprocess
import sys
import time

import fitz  # PyMuPDF
from PIL import Image

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MARP_VERSION = "4.2.3"  # keep in sync with .github/workflows/deploy-myst.yml - legacy decks only
DECKTAPE_SIZE = "1280x720"  # matches this project's Quarto revealjs width/height convention
EDGE_FRACTION = 0.012  # fraction of width/height treated as "the margin band"
BG_SAMPLE_SIZE = 6  # px square sampled from each corner to determine background
DEVIATION_THRESHOLD = 40  # per-channel RGB distance from background to count as "content"


def resolve_topic_dir(topic_arg):
    """Returns (deck_dir, format) where format is 'qmd' or 'md'. Prefers a
    Quarto deck.qmd if both somehow exist (shouldn't happen mid-migration,
    but .qmd is the canonical/current format going forward)."""
    candidates = [topic_arg]
    if not os.path.isabs(topic_arg):
        candidates.append(os.path.join(REPO_ROOT, topic_arg))
    candidates.append(os.path.join(REPO_ROOT, "slides", topic_arg))

    for candidate in candidates:
        if not os.path.isdir(candidate):
            continue
        if os.path.isfile(os.path.join(candidate, "deck.qmd")):
            return candidate, "qmd"
        if os.path.isfile(os.path.join(candidate, "deck.md")):
            return candidate, "md"

    raise SystemExit(f"Could not find a deck.qmd or deck.md for topic '{topic_arg}' "
                      f"(tried: {', '.join(candidates)})")


def _run_via_git_bash_on_windows(shell_cmd, cwd):
    """npx-based tools (decktape) hit an ESM/CJS resolution error under plain
    Windows subprocess+shell=True on this machine's Node install - Git Bash
    is the confirmed-working invocation path (same issue already documented
    for the Marp build below)."""
    git_bash_candidates = [
        r"C:\Program Files\Git\bin\bash.exe",
        r"C:\Program Files (x86)\Git\bin\bash.exe",
    ]
    bash_exe = next((p for p in git_bash_candidates if os.path.isfile(p)), None)
    if bash_exe is None:
        raise SystemExit(
            "Could not find Git Bash (checked Program Files and Program Files (x86)). "
            "This script needs it to invoke npx reliably on Windows - "
            "install Git for Windows or adjust git_bash_candidates in this script."
        )
    return subprocess.run([bash_exe, "-lc", shell_cmd], cwd=cwd, capture_output=True, text=True)


def _rmtree_robust(path, attempts=30, delay=2.0):
    """Quarto's bundled reveal.js assets (font files under deck_files/) can
    land read-only on Windows, which makes a plain shutil.rmtree fail with
    WinError 5 (Access is denied) - clear every file's read-only bit first
    (shutil.rmtree's onerror/onexc callback param is version-dependent
    across Python releases - a manual pre-pass avoids relying on either).

    Separately - confirmed the hard way, after a Puppeteer/Chrome-shutdown
    theory turned out wrong (checked: zero node/chrome/quarto processes were
    running at the moment a "still locked" failure reproduced) - even an
    already-empty directory can transiently fail to rmdir with the identical
    WinError 5. This machine has Google Drive (GoogleDriveFS), Windows
    Search (SearchIndexer/SearchFilterHost), and Defender (MsMpEng) all
    running, any of which routinely locks a freshly-written directory tree
    of many small files (deck_files/libs/... has dozens) while it scans or
    indexes it - a well-known class of Windows dev-environment friction, not
    a lock this script holds. Observed durations varied widely (cleared in
    under a second in some runs, needed closer to a minute in others under
    load) - retry with real headroom rather than fail the verify run over a
    lock that isn't ours and isn't permanent."""
    for root, dirs, files in os.walk(path):
        for name in files + dirs:
            try:
                os.chmod(os.path.join(root, name), stat.S_IWRITE)
            except OSError:
                pass
    for attempt in range(1, attempts + 1):
        try:
            shutil.rmtree(path)
            return
        except OSError:
            if attempt == attempts:
                raise
            time.sleep(delay)


def _cleanup_quarto_artifacts(deck_dir, label="cleanup"):
    """Remove Quarto's own known in-place build-output naming pattern
    (deck.html, deck_files/, deck.quarto_ipynb) - never sweep up arbitrary
    files, since a deck.qmd's own executable cells may legitimately write
    other named assets into this folder.

    This repo lives inside a Google Drive-synced folder ("My Drive\\..."),
    and the failure signature confirms that matters: shutil.rmtree gets all
    the way through removing every file *inside* deck_files/, then the
    final rmdir of the now-empty directory itself fails with WinError 5
    (Access is denied) - not a locked file, a locked directory handle. That
    is the classic symptom of a cloud-sync client (here, GoogleDriveFS)
    holding a directory-change-notification watch on the folder to detect
    edits; the same failure mode is long-reported for build tools writing
    into node_modules/ under Dropbox/OneDrive on Windows. It is NOT
    Puppeteer/Chrome (checked: reproduces with zero node/chrome/quarto
    processes running), and empirically it can outlast even a 60+ second
    retry budget - confirmed by hitting this exact error on a supposedly
    "opportunistic, maximal-elapsed-time" cleanup pass at the top of a
    later, unrelated run.

    Given a lock that can legitimately outlast any wait this script could
    reasonably afford, cleanup here is always best-effort: try briefly (to
    catch the genuinely-transient case), and if it's still locked, log a
    note and move on rather than fail the run over it. The directory is
    gitignored and harmless to leave behind - it is not a precondition
    `quarto render` needs (it overwrites deck_files/ contents as needed),
    only tidiness for the tracked topic folder."""
    deck_html = os.path.join(deck_dir, "deck.html")
    deck_files = os.path.join(deck_dir, "deck_files")

    if os.path.isfile(deck_html):
        try:
            os.remove(deck_html)
        except OSError as e:
            print(f"  (note: couldn't remove stray deck.html during {label} - {e}; harmless, gitignored)")
    if os.path.isdir(deck_files):
        try:
            _rmtree_robust(deck_files, attempts=5, delay=1.0)
        except OSError as e:
            print(f"  (note: couldn't remove stray {os.path.relpath(deck_files, REPO_ROOT)} "
                  f"during {label} - {e}; harmless, gitignored, will retry opportunistically next run)")
    for stray in glob.glob(os.path.join(deck_dir, "deck.quarto_ipynb")):
        try:
            os.remove(stray)
        except OSError:
            pass


def build_pdf_quarto(deck_dir, out_pdf):
    """Render deck.qmd in place (Quarto's natural mode - it writes deck.html
    and deck_files/ next to the source so relative media/ references
    resolve), decktape the result to PDF in out_pdf, then clean up the
    in-place render artifacts so the tracked topic folder isn't left with
    build output."""
    # Opportunistic: if a previous run left artifacts behind, this is a
    # good moment to try clearing them - but never fatal, see
    # _cleanup_quarto_artifacts's docstring.
    _cleanup_quarto_artifacts(deck_dir, label="pre-render cleanup")

    deck_qmd = os.path.join(deck_dir, "deck.qmd")
    print(f"Rendering with Quarto: {os.path.relpath(deck_qmd, REPO_ROOT)}")

    result = subprocess.run(["quarto", "render", "deck.qmd"], cwd=deck_dir,
                             capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
        raise SystemExit(f"quarto render failed (exit {result.returncode})")

    deck_html = os.path.join(deck_dir, "deck.html")
    if not os.path.isfile(deck_html):
        raise SystemExit("quarto render reported success but deck.html was not produced")

    print(f"Exporting to PDF with decktape (size {DECKTAPE_SIZE})...")
    decktape_cmd = f'npx -y decktape reveal --size "{DECKTAPE_SIZE}" "deck.html" "{out_pdf}"'
    try:
        if os.name == "nt":
            result = _run_via_git_bash_on_windows(decktape_cmd, cwd=deck_dir)
        else:
            result = subprocess.run(
                ["npx", "-y", "decktape", "reveal", "--size", DECKTAPE_SIZE, "deck.html", out_pdf],
                cwd=deck_dir, capture_output=True, text=True,
            )
        if result.returncode != 0:
            print(result.stdout)
            print(result.stderr, file=sys.stderr)
            raise SystemExit(f"decktape failed (exit {result.returncode})")
        if not os.path.isfile(out_pdf):
            raise SystemExit("decktape reported success but no PDF was produced")
    finally:
        _cleanup_quarto_artifacts(deck_dir, label="post-render cleanup")


def build_pdf_marp(deck_dir, out_pdf):
    """Legacy path for any topic not yet migrated off Marp."""
    theme = os.path.join(REPO_ROOT, "slides", "_shared", "eco701-theme.css")
    deck_md = os.path.join(deck_dir, "deck.md")
    print(f"Building with marp-cli v{MARP_VERSION}: {os.path.relpath(deck_md, REPO_ROOT)}")

    if os.name == "nt":
        shell_cmd = (
            f'npx --yes @marp-team/marp-cli@{MARP_VERSION} '
            f'"{deck_md}" -o "{out_pdf}" --pdf --allow-local-files --theme-set "{theme}"'
        )
        result = _run_via_git_bash_on_windows(shell_cmd, cwd=REPO_ROOT)
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
    ap.add_argument("--topic", required=True, help="Topic folder name (e.g. 01_definitions-and-key-tools) or path")
    ap.add_argument("--dpi", type=int, default=110, help="Rasterization DPI (default 110, matches this project's convention)")
    ap.add_argument("--out-dir", default=None, help="Where to write rasters + report (default: _verify/<topic>/)")
    ap.add_argument("--keep-pdf", action="store_true", help="Keep the built PDF in the output dir instead of discarding it")
    args = ap.parse_args()

    deck_dir, fmt = resolve_topic_dir(args.topic)
    topic_name = os.path.basename(deck_dir.rstrip("/\\"))
    out_dir = args.out_dir or os.path.join(REPO_ROOT, "_verify", topic_name)
    os.makedirs(out_dir, exist_ok=True)

    pdf_path = os.path.join(out_dir, f"{topic_name}.pdf")
    if fmt == "qmd":
        build_pdf_quarto(deck_dir, pdf_path)
    else:
        print(f"NOTE: {topic_name} is still a legacy Marp deck.md - building with marp-cli.")
        build_pdf_marp(deck_dir, pdf_path)

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
        f.write(f"Verification report for {topic_name} ({fmt})\n")
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

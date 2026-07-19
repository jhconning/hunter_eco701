"""
Step 3 of the topic-conversion pipeline: OCRs equation crops (from
render_equations.py) into LaTeX via the Mathpix API.

Requires a .env file (at the repo root, gitignored) with:
    MATHPIX_APP_ID=...
    MATHPIX_APP_KEY=...

NOTE: this calls a paid third-party API against Jonathan's own account -
each call has a real (small) cost. Don't run this speculatively across a
whole topic's equations without knowing roughly how many there are first
(check shape_census.json's ole_prog_ids count from extract_topic.py).

Usage:
    mamba run -n ecopy python mathpix_ocr.py \
        --eq-dir "Y:\Hunter\Eco 701\Eco701\slides\02_constrained-optimization\raw\media\eq" \
        --out "Y:\Hunter\Eco 701\Eco701\slides\02_constrained-optimization\raw\mathpix.json" \
        --env "Y:\Hunter\Eco 701\Eco701\.env"

Writes --out: a dict keyed by filename, each with Mathpix's "latex_styled",
"text", and "confidence" fields (raw API response, trimmed).
"""
import argparse
import base64
import json
import os
import requests


def load_env(path):
    env = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k] = v
    return env


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--eq-dir", required=True, help="Folder of equation crop PNGs (from render_equations.py)")
    ap.add_argument("--out", required=True, help="Output JSON path")
    ap.add_argument("--env", default=None, help="Path to .env with MATHPIX_APP_ID/MATHPIX_APP_KEY (default: repo root .env)")
    args = ap.parse_args()

    env_path = args.env or os.path.join(os.path.dirname(__file__), "..", ".env")
    env = load_env(env_path)
    app_id = env["MATHPIX_APP_ID"]
    app_key = env["MATHPIX_APP_KEY"]

    files = sorted(f for f in os.listdir(args.eq_dir) if f.lower().endswith((".png", ".jpg", ".jpeg")))
    print(f"Found {len(files)} equation images in {args.eq_dir}")

    url = "https://api.mathpix.com/v3/text"
    headers = {"app_id": app_id, "app_key": app_key, "Content-type": "application/json"}

    results = {}
    for fname in files:
        with open(os.path.join(args.eq_dir, fname), "rb") as f:
            b64 = base64.b64encode(f.read()).decode("ascii")
        payload = {
            "src": f"data:image/png;base64,{b64}",
            "formats": ["text", "latex_styled"],
            "data_options": {"include_latex": True, "include_asciimath": True},
        }
        resp = requests.post(url, headers=headers, data=json.dumps(payload), timeout=30)
        try:
            data = resp.json()
        except Exception:
            data = {"error": "non-json response", "status_code": resp.status_code}
        results[fname] = data
        conf = data.get("confidence", "?")
        latex = data.get("latex_styled", "(no result)")
        print(f"  {fname}: confidence={conf}  {latex}")

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"-> wrote {args.out}")


if __name__ == "__main__":
    main()

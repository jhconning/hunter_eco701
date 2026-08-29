# ECO 701: Course Ecosystem & LMS Infrastructure

**Course:** ECO 701 Microeconomic Theory (Master's Level)  
**Institution:** Hunter College, CUNY  
**Instructor:** Jonathan Conning  

---

## 1. Overview & Tool Ecosystem

This document outlines the basic technical and pedagogical infrastructure for ECO 701. To provide a modern, code-friendly, open, and interactive learning environment while maintaining official institutional record-keeping, the course relies on a multi-tool setup:

* **GitHub Pages & Repository (MyST / Quarto):** Primary hub for course content, Quarto markdown slides, Jupyter Notebooks, and live in-browser interactive execution via `mystmd` and Pyodide.
* **Gradescope:** Primary platform for assignment collection, autograding/manual rubrics, and detailed student feedback.
* **Brightspace (CUNY LMS):** Minimal footprint — used primarily for the official gradebook, roster management, and institutional announcements.

```
+-------------------------------------------------------------------------+
|                  GitHub Pages (Course Site)                             |
|  - Quarto Markdown Slide Decks (.qmd / .md)                             |
|  - Jupyter Notebooks & MyST Markdown (mystmd)                           |
|  - Live In-Browser Execution (Pyodide / JupyterLite / Thebe)            |
+-------------------------------------------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                              Gradescope                                 |
|   (Problem Sets, Autograding, Manual Rubrics, Direct Feedback)          |
+-------------------------------------------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                           Brightspace LMS                               |
|    (Official Gradebook Sync, Roster Sync, Official Announcements)       |
+-------------------------------------------------------------------------+
```

---

## 2. GitHub Pages, Quarto & MyST (`mystmd`)

### Role
Serves as the primary public-facing portal, interactive learning platform, and repository for all course materials.

### Key Components
* **Quarto Markdown Slides:**
  * Authoring slides in Quarto (`.qmd` / markdown).
  * Rendered into clean HTML presentation decks / PDFs hosted on GitHub Pages.
* **MyST Markdown & Interactive Site (`mystmd`):**
  * Modern documentation and textbook layout generated via MyST Markdown.
* **In-Browser Compute (Pyodide / JupyterLite / Thebe):**
  * Live, interactive execution of Python microeconomic models directly inside the browser using Pyodide without requiring local Python installation for students.
* **Jupyter Notebooks:**
  * Static preview and downloadable computational problem sets / demonstrations (`notebooks/`).
* **Course Repository:**
  * Public GitHub repository (`jhconning/hunter_eco701`) for revision history and open materials.

### Useful Notes / Stubs
* *Course Site URL:* `https://jhconning.github.io/hunter_eco701/`
* *Quarto Configuration:* `_quarto.yml` (if rendering Quarto site/slides)
* *MyST Configuration:* `myst.yml` (for `mystmd` site build & Pyodide / JupyterLite integration)
* *Student Access:* Completely open access; zero installation needed for live web interaction.

---

## 3. Gradescope

### Role
Handles submission, autograding, manual rubric grading, and feedback for all problem sets and exams.

### Key Components & Workflows
* **Problem Sets & Assignments:**
  * PDF submissions / Jupyter Notebook (`.ipynb`) / Python script (`.py`) submissions.
  * Question-by-question rubric grading for detailed student feedback.
* **Bulk Download & Python-Based Grading Workflows:**
  1. **Cloud Autograder (In-Gradescope via Docker):**
     * Upload a custom Python autograder script (`run_autograder`, `setup.sh`, `requirements.txt`) directly to Gradescope.
     * Gradescope automatically executes your Python grading script in a container upon submission and generates a `results.json` score file.
  2. **Bulk Export & Local Python Grading:**
     * **Download:** Bulk download all student submissions as a single `.zip` file from the Gradescope assignment management menu (or programmatically via Python APIs / `gradescope-api`).
     * **Evaluate:** Run local Python scripts (`nbgrader`, `pytest`, or custom notebook evaluation scripts) across the unzipped student `.ipynb` / `.py` files.
     * **Upload Scores:** Upload generated scores back to Gradescope via CSV import or update scores via Gradescope API.
* **Handwritten Submissions & OCR / AI-Assisted Grading:**
  * **Native Gradescope AI Grouping:** Gradescope automatically clusters similar handwritten answers, math expressions, and short text across all student submissions so you can apply rubric scores to batches of identical answers simultaneously.
  * **Python + Vision / Math OCR Pipeline:** For custom Python automated grading of handwritten math/diagrams:
    * Download PDF page exports from Gradescope.
    * Use Python with specialized Math OCR (e.g. Mathpix API to extract LaTeX equations) or Multimodal Vision LLMs (e.g. Gemini/GPT-4o Vision API) to parse handwritten math steps, verify mathematical derivations, and evaluate hand-drawn economic graphs.
    * Import scores/feedback back into Gradescope via CSV or API.
* **Regrade Requests & Feedback:**
  * Structured regrade request workflows within established time windows.

### Guidelines for Accurate Handwritten Submissions & OCR
To ensure student handwritten solutions are read accurately by Gradescope AI and local Python/OCR pipelines:

* **Student Formatting Rules:**
  * **Use Dark Pen or #2 Pencil:** Require dark blue/black ink or dark pencil to prevent faint/washed-out scans.
  * **Box Final Mathematical Results:** Require students to draw a bold box around final demand functions, FOC results, or numerical equilibrium values (e.g., \(\mathbf{x_1^*(p, m) = \frac{m}{2 p_1}}\)).
  * **Structured Vertical Work:** Ask students to write algebraic steps sequentially downwards rather than scattering calculations around margins or graphs.
  * **Mobile Scanner Apps:** Require flat, high-contrast document scans (using Apple Notes Scanner, Adobe Scan, etc.) rather than angled or low-light phone photos.
* **Instructor / Assignment Template Best Practices:**
  * **Templated Answer Sheets:** Provide PDF templates with dedicated bounding boxes for each question. Gradescope can crop question boxes automatically.
  * **Image Preprocessing:** In Python scripts, preprocess PDF page images (convert to 300 DPI, apply contrast enhancement) before sending to Mathpix or Vision APIs.
  * **Human-in-the-Loop Thresholds:** Set a confidence score threshold in your grading pipeline (e.g. < 85% OCR confidence) to flag ambiguous handwriting for manual human review in Gradescope.

### Useful Notes / Stubs
* *Course Entry Code / Enrolment:* `[Stub: Add Gradescope Course Entry Code]`
* *Autograder Setup:* `[Stub: Details on Python autograder setup / Docker script location in repo]`
* *Bulk Download & OCR Tooling:* `[Stub: Python script path for batch PDF extraction, Mathpix/Vision OCR processing, and grade import]`
* *Roster Import:* Import roster from Brightspace / CUNYfirst.




---

## 4. Brightspace (LMS)

### Role
Maintained with a **minimalist strategy** to fulfill Hunter College / CUNY administrative requirements without duplicating course content.

### Key Components
* **Official Gradebook:**
  * Final aggregated grades and periodic score updates synced from Gradescope.
* **Administrative Announcements:**
  * Formal institutional notices, syllabus posting, and exam scheduling details.
* **External Links:**
  * Prominent links directing students to GitHub Pages and Gradescope.

### Useful Notes / Stubs
* *Course Page Link:* `[Stub: Add Brightspace Course URL]`
* *Minimal Content Strategy:* Keep modules sparse; redirect students to GitHub Pages for lectures and interactive notebooks.

---

## 5. Workflow & Integration Stubs

* [ ] **Quarto Slide Pipeline:** Set up build scripts / GitHub Actions to compile Quarto slide decks to HTML/PDF.
* [ ] **MyST & Pyodide Setup:** Configure `myst.yml` with `project.jupyter.lite: true` (or Pyodide runtime) for live interactive code cells on GitHub Pages.
* [ ] **Roster Synchronization:** Export student roster from Brightspace / CUNYfirst to Gradescope.
* [ ] **Grade Export / Import:** Export assignment scores from Gradescope via CSV and import to Brightspace Gradebook.
* [ ] **Student Onboarding Guide:** Provide clear instructions in Week 0/Topic 0 on accessing Quarto slides, using live Pyodide notebooks, and submitting assignments on Gradescope.

---

## 6. Recommended Tools & Micro-Theory Exemplars

### Modeling & Interactive Visualization Libraries
* **SymPy (Symbolic Python):** For symbolic microeconomic proofs, utility maximization (Lagrangian setup), solving first-order conditions, deriving Marshallian/Hicksian demand functions, and computing Roy's Identity / Slutsky matrices analytically.
* **SciPy (`scipy.optimize`):** For numerical constrained optimization (e.g. general equilibrium 2x2 Edgeworth box allocations, cost minimization, and welfare changes EV/CV).
* **Plotly / `ipywidgets`:** For dynamic 3D indifference surfaces, budget constraint shifts, and comparative statics sliders embedded in Jupyter/Pyodide.
* **Marimo Notebooks (Alternative to Jupyter):** Reactive Python notebooks stored as pure `.py` scripts, ideal for web-embedded interactive micro apps without hidden cell states.

### Course Models & Exemplars to Emulate
* **QuantEcon (Thomas Sargent & John Stachurski):** Gold standard for open, computational economics web platforms (`quantecon.org`). Demonstrates how to combine open Python notebooks, GitHub workflows, and rich online rendering.
* **CORE Econ (*The Economy / ESPP*):** Exemplary web-native economics textbooks featuring interactive embedded figures and open web access.
* **Florian Oswald's Computational Economics (`floswald.github.io/CompEcon`):** Built entirely with **Quarto** (`_quarto.yml`, `.qmd` documents), Quarto Reveal.js presentation slides, Julia (`Project.toml`), Jupyter/Quarto notebooks, and GitHub Pages automated via GitHub Actions. (Does *not* use `mystmd`).

* **EconGraphs / Interactive Micro Calculators:** Interactive web tools for 3D utility functions, cost curves, and general equilibrium Edgeworth box dynamics.

### Student Discussion & Q&A Tools
* **Ed Discussion / Piazza:** Superior to standard LMS forums for math-intensive courses — natively renders LaTeX math expressions and code blocks for student homework Q&A.

---

## 7. Quarto vs. MyST (`mystmd`) Pipeline Comparison

| Feature / Aspect | Quarto Pipeline (`_quarto.yml`) | MyST Markdown Pipeline (`myst.yml`) |
| :--- | :--- | :--- |
| **Primary Ecosystem** | Posit / Multi-language scientific publishing (R, Python, Julia, Observable) | Executable Books / Jupyter Book 2.0 / Curvenote ecosystem |
| **Slide Generation** | **Native Reveal.js** (`format: revealjs` in `.qmd` files) — built-in speaker notes, transitions, math, and code blocks | Requires external slide generator (e.g. Marp `deck.md` or custom Reveal) |
| **In-Browser Compute** | Requires `quarto-live` Wasm extension or Binder links for browser execution | **Native `thebe-lite`** (`project.jupyter.lite: true` in `myst.yml` via Pyodide) |
| **Document Formats** | `.qmd`, `.ipynb`, `.md` | `.md` (MyST syntax), `.ipynb` |
| **Math & Cross-Refs** | Standard LaTeX math (`$ ... $`, `$$ ... $$`) & Quarto cross-ref tags (`@eq-label`) | Standard LaTeX math & MyST target cross-references (`{eq}`) |
| **Static Site Build** | `quarto render` | `myst build --html` |
| **GitHub Pages Deployment**| `quarto publish gh-pages` or GitHub Actions | `myst build` + GitHub Actions to `gh-pages` branch |

### Architectural Recommendation for ECO 701
* **Option A (MyST Site + Quarto Slides):** Use `mystmd` for the main course site and interactive notebooks (leveraging native `thebe-lite` / Pyodide in-browser compute), while using Quarto (`.qmd`) or Marp (`deck.md`) for lecture slides.
* **Option B (All-in-One Quarto with `quarto-live`):** Use Quarto for both the website and Reveal.js presentation slides, incorporating `quarto-live` for serverless, in-browser Python execution and interactive code widgets.

---

## 8. `quarto-live` & Interactive Python Web Pages

### What is `quarto-live`?
`quarto-live` is an extension for Quarto that embeds WebAssembly execution engines directly into Quarto HTML documents and Reveal.js slides. It uses **Pyodide** to run Python entirely client-side inside the student's browser.

### Key Capabilities for ECO 701
* **Serverless Interactive Web Pages:** Yes, you can create fully interactive Python pages on GitHub Pages with zero backend servers or cloud hosting costs.
* **Editable Code Cells:** Students can modify Python code parameters (e.g. changing income \(m\), price \(p_1\), or elasticity \(\epsilon\)) and run code directly on the webpage.
* **Microeconomic Python Packages:** Loads core scientific Python packages in the browser: `numpy`, `scipy`, `sympy`, `matplotlib`, and `pandas`.
### Slider Mechanism: `quarto-live` (OJS Inputs) vs. `ipywidgets`
* **Does `quarto-live` use `ipywidgets`?** No. `ipywidgets` requires a running Jupyter Comm manager architecture, which does not map cleanly into `quarto-live`'s lightweight WebAssembly runtime.
* **How `quarto-live` creates sliders:** It pairs **Observable JS (OJS) inputs** with Pyodide Python code blocks:
  1. Define UI sliders in OJS (e.g. `viewof price = Inputs.range([1, 20], {label: "Price p1"})`).
  2. Bind the slider value directly into a `quarto-live` Python block using `${price}` syntax.
  3. When a student moves the slider, `quarto-live` reactively updates Python variables and redraws Matplotlib / Plotly graphs automatically.
---

## 9. Deep-Dive: `thebe-lite` & `ipywidgets` in MyST (`mystmd`)

### What is `thebe-lite`?
`thebe-lite` is the client-side WebAssembly compute engine built into **MyST Markdown (`mystmd`)** (the core of Jupyter Book 2.0).
* **Serverless Jupyter Kernel:** Instead of connecting to a remote JupyterHub/Binder server, `thebe-lite` boots a WebAssembly **JupyterLite + Pyodide kernel** directly inside the student's browser.
* **Full Jupyter Protocol:** Because it runs an actual Jupyter kernel client-side, it supports the full Jupyter Comm protocol, enabling native `ipywidgets` (`FloatSlider`, `Dropdown`, `@interact`) without any server infrastructure.

### How to use `ipywidgets` with `thebe-lite`

#### Step 1: Enable `thebe-lite` in `myst.yml`
```yaml
version: 1
project:
  title: ECO 701 Microeconomic Theory
  jupyter:
    lite: true   # Enables in-browser Pyodide kernel for code cells
```

#### Step 2: Write standard Python `ipywidgets` code in your MyST (`.md`) file
```markdown
```{code-cell} python
import ipywidgets as widgets
import matplotlib.pyplot as plt
import numpy as np

def plot_utility(p1=5.0, p2=10.0, m=100.0):
    x1 = np.linspace(0.1, m/p1, 200)
    x2_budget = (m - p1 * x1) / p2
    
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(x1, x2_budget, 'r--', label='Budget Line')
    ax.set_title('Consumer Optimization')
    ax.set_xlabel('Good 1 (x1)')
    ax.set_ylabel('Good 2 (x2)')
    ax.grid(True)
    ax.legend()
    plt.show()

# Standard ipywidgets interact decorator
widgets.interact(
    plot_utility,
    p1=widgets.FloatSlider(value=5.0, min=1.0, max=20.0, step=0.5, description='Price p1:'),
    p2=widgets.FloatSlider(value=10.0, min=1.0, max=20.0, step=0.5, description='Price p2:'),
    m=widgets.FloatSlider(value=100.0, min=20.0, max=200.0, step=10.0, description='Income m:')
)
```
```

#### Step 3: Build & Publish
```bash
myst build --html
```
---

## 10. Live Interactivity on Reveal.js Slides (GitHub Pages)

### Can Reveal.js slides on GitHub Pages be live and interactive?
**YES, absolutely.** You can host fully interactive Reveal.js presentation slides on GitHub Pages using **Quarto + `quarto-live`**.

### How it Works
1. **Quarto Reveal.js Format:** Write slides in a `.qmd` file with `format: revealjs`.
2. **`quarto-live` Extension:** Include the `quarto-live` extension, which boots Pyodide in the browser when the slide deck loads.
3. **Live Execution & Sliders on Slides:**
   * **In-Class Live Demos:** Edit Python code directly on a slide during lecture and click **Run** to update the microeconomic plot live in front of students.
   * **Interactive Sliders:** Add OJS range sliders (`viewof p1 = Inputs.range(...)`) directly on presentation slides to demonstrate comparative statics (e.g. rotating budget lines, shifting indifference curves) live during class.
4. **Serverless GitHub Pages:** Compiles to static HTML/JS assets published directly on GitHub Pages with zero server backend or cloud hosting costs.







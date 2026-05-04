# Neobeam Marp Theme Notes

The `neobeam` theme supports standard Marp directives (like `size: 16:9`, `math: katex`, `<!-- fit -->`, `![bg]`), but also includes several custom CSS tricks designed specifically for this theme:

## 1. Divided Footers
Neobeam intercepts bold text `**` in the footer directive to split the footer into three distinct colored boxes (instead of using the standard `|` pipe character).
**Syntax:** `<!-- footer: "**Left** **Center** **Right**" -->`

## 2. Title Slide Configuration
To trigger the special title slide styling (blue background, centered text), apply the `title` class to the first slide:
**Syntax:** `<!-- _class: title -->`

## 3. Watermark Logos (Title Slide Only)
If you place an image on the title slide with specific alt-text, Neobeam converts it into a faded, tilted watermark in the bottom corner.
*   `![logo](image.png)` -> Bottom right watermark
*   `![logo-left](image.png)` -> Bottom left watermark

## 4. Built-in Image Captions
To neatly caption an image, place a Heading 6 (`######`) immediately following the image. The theme will shrink it, lighten it, and pull it tightly under the image.
**Syntax:**
```markdown
![center](image.png)
###### Figure 1: Caption text goes here
```

## 5. Quick Image Alignment
Use `center`, `left`, or `right` in the image alt-text to automatically float and align standard images without needing extra HTML/CSS.
*   `![center](image.png)` -> Centered
*   `![left](image.png)` -> Floated left
*   `![right](image.png)` -> Floated right

## 6. Definition Blocks
Perfect for theorems and definitions. Wrap a Heading 4 (`####`) inside a blockquote (`>`) to create a colored callout box. If you have multiple on a slide, it cycles colors automatically (Blue -> Green -> Red).
**Syntax:**
```markdown
> #### Definition: Pareto Efficiency
> An allocation is Pareto efficient if...
```

## 7. Highlight Text
Wrap text in `<mark>` tags or `==` (if extended markdown is enabled) to apply the theme's secondary highlight color.
**Syntax:** `<mark>highlighted text</mark>`

## 8. Split Layouts and Background Images (Marp Native)
To place an image side-by-side with text (which is the most reliable way to make an image as large as possible without overflowing the slide), use Marp's native background directives.
*   `![bg right contain](image.png)` -> Splits the slide 50/50, puts text on the left, and scales the image to fit perfectly on the right half without cropping.
*   `![bg left:30%](image.png)` -> Puts the image on the left, taking up exactly 30% of the slide.

## 9. Global Color Override
You can override the base mathematical color seed in the YAML frontmatter to completely re-theme the presentation.
**Syntax:**
```yaml
style: |
  :root {
    --primary: #5a2a82; /* Custom hex color */
  }
```

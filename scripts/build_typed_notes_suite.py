import os
import io
import sys
import shutil
import pypdf
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable, Preformatted
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

# Ensure watermark assets exist
base_images = r'frontend/src/assets/images'
os.makedirs(base_images, exist_ok=True)
logo_icon = os.path.join(base_images, 'revise-x-app-icon.png')
if not os.path.exists(logo_icon):
    # fallback from public if needed
    shutil.copy2('frontend/public/images/revise-x-app-icon.png', logo_icon)

im = Image.open(logo_icon).convert('RGBA')
# 1. Subtle watermark badge (8% opacity)
im_wm = im.resize((160, 160), Image.Resampling.LANCZOS)
r, g, b, a = im_wm.split()
a = a.point(lambda p: int(p * 0.08))
im_wm.putalpha(a)
subtle_wm_path = os.path.join(base_images, 'watermark_logo_subtle.png')
im_wm.save(subtle_wm_path)

# 2. Mini header icon
im_header = im.resize((24, 24), Image.Resampling.LANCZOS)
mini_header_path = os.path.join(base_images, 'header_logo_mini.png')
im_header.save(mini_header_path)

class BrandedCanvas(canvas.Canvas):
    def __init__(self, *args, title="Revise-X Study Notes", **kwargs):
        super().__init__(*args, **kwargs)
        self.pages = []
        self.title = title
        
    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()
        
    def save(self):
        num_pages = len(self.pages)
        for page in self.pages:
            self.__dict__.update(page)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()
        
    def draw_page_decorations(self, total_pages):
        width, height = letter
        
        # Center logo watermark badge
        logo_w, logo_h = 130, 130
        self.drawImage(
            subtle_wm_path,
            (width - logo_w) / 2.0,
            (height - logo_h) / 2.0 + 15,
            width=logo_w,
            height=logo_h,
            mask='auto'
        )
        
        # Center subtle text
        self.saveState()
        self.setFillColor(colors.HexColor('#0f172a'))
        self.setFillAlpha(0.045)
        self.setFont('Helvetica-Bold', 26)
        self.drawCentredString(width / 2.0, (height - logo_h) / 2.0 - 10, 'REVISE-X')
        self.restoreState()
        
        # Top Header Bar
        self.saveState()
        self.drawImage(mini_header_path, 36, height - 26, width=14, height=14, mask='auto')
        self.setFont('Helvetica-Bold', 8)
        self.setFillColor(colors.HexColor('#ea580c'))
        self.drawString(54, height - 22, 'REVISE-X')
        
        self.setFont('Helvetica', 7.5)
        self.setFillColor(colors.HexColor('#64748b'))
        self.drawRightString(width - 36, height - 22, self.title)
        
        self.setStrokeColor(colors.HexColor('#cbd5e1'))
        self.setStrokeAlpha(0.6)
        self.setLineWidth(0.5)
        self.line(36, height - 28, width - 36, height - 28)
        self.restoreState()
        
        # Bottom Footer Bar
        self.saveState()
        self.setStrokeColor(colors.HexColor('#cbd5e1'))
        self.setStrokeAlpha(0.6)
        self.setLineWidth(0.5)
        self.line(36, 28, width - 36, 28)
        
        self.setFont('Helvetica', 7.5)
        self.setFillColor(colors.HexColor('#64748b'))
        self.drawString(36, 17, '© Revise-X • All Rights Reserved')
        self.drawCentredString(width / 2.0, 17, 'www.revise-x.com')
        self.drawRightString(width - 36, 17, f'Page {self._pageNumber} of {total_pages}')
        self.restoreState()

def get_doc_styles():
    styles = getSampleStyleSheet()
    
    styles.add(ParagraphStyle(
        name='MainTitle',
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=10
    ))
    styles.add(ParagraphStyle(
        name='SectionH1',
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    ))
    styles.add(ParagraphStyle(
        name='SectionH2',
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14.5,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=9,
        spaceAfter=4,
        keepWithNext=True
    ))
    styles.add(ParagraphStyle(
        name='BodyTextCustom',
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=colors.HexColor('#1e293b'),
        spaceAfter=5
    ))
    styles.add(ParagraphStyle(
        name='BulletCustom',
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=colors.HexColor('#1e293b'),
        leftIndent=14,
        spaceAfter=3
    ))
    styles.add(ParagraphStyle(
        name='CodeStyle',
        fontName='Courier',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor('#0f172a')
    ))
    styles.add(ParagraphStyle(
        name='FooterNote',
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#64748b'),
        spaceBefore=10
    ))
    return styles

def code_box(code_str, styles):
    cleaned = code_str.strip().replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    p = Paragraph(f"<font face='Courier'>{cleaned.replace(chr(10), '<br/>')}</font>", styles['CodeStyle'])
    t = Table([[p]], colWidths=[540])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8fafc')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 9),
        ('RIGHTPADDING', (0, 0), (-1, -1), 9),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
    ]))
    return t

# =========================================================================
# 1. BUILD TYPED HTML NOTES (Exact 10 Pages matching user's uploaded reference)
# =========================================================================
def build_typed_html_notes(dest_path):
    class CustomHTMLCanvas(BrandedCanvas):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, title="HTML Notes - Typed Version", **kwargs)
            
    doc = SimpleDocTemplate(
        dest_path,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    styles = get_doc_styles()
    story = []
    
    # --- PAGE 1 ---
    story.append(Paragraph("HTML Notes - Typed Version", styles['MainTitle']))
    story.append(Paragraph("<b>Introduction to HTML</b>", styles['SectionH1']))
    story.append(Paragraph("HTML stands for HyperText Markup Language. It is the standard markup language for creating web pages.", styles['BodyTextCustom']))
    story.append(Paragraph("<b>Key Points:</b>", styles['SectionH2']))
    story.append(Paragraph("• HTML describes the structure of a web page using markup (elements/tags)", styles['BulletCustom']))
    story.append(Paragraph("• HTML elements tell the browser how to display content", styles['BulletCustom']))
    story.append(Paragraph("• HTML is not a programming language; it's a markup language", styles['BulletCustom']))
    
    story.append(Paragraph("<b>Basic Structure of HTML Document</b>", styles['SectionH2']))
    story.append(code_box(
"""<!DOCTYPE html>
<html>
<head>
  <title>Page Title</title>
</head>
<body>
  <!-- Content goes here -->
</body>
</html>""", styles))

    story.append(Paragraph("<b>Explanation:</b>", styles['SectionH2']))
    story.append(Paragraph("• <code>&lt;!DOCTYPE html&gt;</code> - Declares the document type and HTML version", styles['BulletCustom']))
    story.append(Paragraph("• <code>&lt;html&gt;</code> - Root element of the HTML page", styles['BulletCustom']))
    story.append(Paragraph("• <code>&lt;head&gt;</code> - Contains meta-information about the document", styles['BulletCustom']))
    story.append(Paragraph("• <code>&lt;title&gt;</code> - Sets the title shown in browser tab", styles['BulletCustom']))
    story.append(Paragraph("• <code>&lt;body&gt;</code> - Contains the visible page content", styles['BulletCustom']))

    story.append(Paragraph("<b>HTML Tags and Elements</b>", styles['SectionH1']))
    story.append(Paragraph("<b>What are Tags?</b>", styles['SectionH2']))
    story.append(Paragraph("• Tags are keywords surrounded by angle brackets like &lt;tagname&gt;", styles['BulletCustom']))
    story.append(Paragraph("• Most tags come in pairs: opening tag and closing tag", styles['BulletCustom']))
    story.append(Paragraph("• Some tags are self-closing (no content)", styles['BulletCustom']))
    story.append(PageBreak())

    # --- PAGE 2 ---
    story.append(Paragraph("<b>Examples:</b>", styles['SectionH2']))
    story.append(code_box(
"""<h1>Heading 1</h1>
<p>This is a paragraph.</p>
<a href="https://example.com">Link</a>
<img src="image.jpg" alt="Description">""", styles))

    story.append(Paragraph("<b>Common HTML Elements</b>", styles['SectionH1']))
    story.append(Paragraph("<b>1. Headings</b>", styles['SectionH2']))
    story.append(code_box(
"""<h1>Main Heading</h1>
<h2>Sub Heading</h2>
<h3>Section Heading</h3>
<h4>Sub-section</h4>
<h5>Small heading</h5>
<h6>Smallest heading</h6>""", styles))

    story.append(Paragraph("<b>2. Paragraphs</b>", styles['SectionH2']))
    story.append(code_box(
"""<p>This is a paragraph of text.</p>
<p>Another paragraph here.</p>""", styles))

    story.append(Paragraph("<b>3. Links (Anchor Tags)</b>", styles['SectionH2']))
    story.append(code_box(
"""<a href="https://www.google.com">Visit Google</a>
<a href="page2.html" target="_blank">Open in new tab</a>""", styles))

    story.append(Paragraph("<b>4. Images</b>", styles['SectionH2']))
    story.append(code_box("""<img src="logo.png" alt="Company Logo" width="200" height="100">""", styles))

    story.append(Paragraph("<b>5. Lists</b>", styles['SectionH2']))
    story.append(Paragraph("<b>Unordered List (Bullet Points):</b>", styles['BodyTextCustom']))
    story.append(code_box(
"""<ul>
  <li>Item 1</li>
  <li>Item 2</li>
  <li>Item 3</li>
</ul>""", styles))
    story.append(Paragraph("<b>Ordered List (Numbered):</b>", styles['BodyTextCustom']))
    story.append(PageBreak())

    # --- PAGE 3 ---
    story.append(code_box(
"""<ol>
  <li>First item</li>
  <li>Second item</li>
  <li>Third item</li>
</ol>""", styles))

    story.append(Paragraph("<b>HTML Attributes</b>", styles['SectionH1']))
    story.append(Paragraph("Attributes provide additional information about HTML elements.", styles['BodyTextCustom']))
    story.append(Paragraph("<b>Common Attributes:</b>", styles['SectionH2']))
    story.append(Paragraph("• <code>href</code> - Specifies URL for links", styles['BulletCustom']))
    story.append(Paragraph("• <code>src</code> - Specifies source path for images", styles['BulletCustom']))
    story.append(Paragraph("• <code>alt</code> - Alternative text for images", styles['BulletCustom']))
    story.append(Paragraph("• <code>width, height</code> - Dimensions", styles['BulletCustom']))
    story.append(Paragraph("• <code>class, id</code> - For styling and scripting", styles['BulletCustom']))
    story.append(Paragraph("• <code>style</code> - Inline CSS styling", styles['BulletCustom']))
    story.append(Paragraph("• <code>title</code> - Tooltip text", styles['BulletCustom']))

    story.append(Paragraph("<b>Example:</b>", styles['SectionH2']))
    story.append(code_box(
"""<a href="https://example.com" title="Visit Example" target="_blank">Click Here</a>
<img src="photo.jpg" alt="My Photo" width="300" height="200">""", styles))

    story.append(Paragraph("<b>Text Formatting Tags</b>", styles['SectionH1']))
    story.append(code_box(
"""<b>Bold text</b> or <strong>Strong text</strong>
<i>Italic text</i> or <em>Emphasized text</em>
<u>Underlined text</u>
<mark>Marked/highlighted text</mark>
<small>Small text</small>
<del>Deleted text</del>
<ins>Inserted text</ins>
<sub>Subscript: H<sub>2</sub>O</sub>
<sup>Superscript: E = mc<sup>2</sup></sup>""", styles))
    story.append(PageBreak())

    # --- PAGE 4 ---
    story.append(Paragraph("<b>HTML Div and Span</b>", styles['SectionH1']))
    story.append(Paragraph("<b>&lt;div&gt; - Block Level Container</b>", styles['SectionH2']))
    story.append(Paragraph("• Used to group block-level elements", styles['BulletCustom']))
    story.append(Paragraph("• Takes full width by default", styles['BulletCustom']))
    story.append(Paragraph("• Commonly used for layout sections", styles['BulletCustom']))
    story.append(code_box(
"""<div style="background-color: lightblue; padding: 20px;">
  <h2>Section Title</h2>
  <p>Content inside div</p>
</div>""", styles))

    story.append(Paragraph("<b>&lt;span&gt; - Inline Container</b>", styles['SectionH2']))
    story.append(Paragraph("• Used to group inline elements", styles['BulletCustom']))
    story.append(Paragraph("• Takes only necessary width", styles['BulletCustom']))
    story.append(Paragraph("• Used for styling parts of text", styles['BulletCustom']))
    story.append(code_box("""<p>This is <span style="color: red;">red text</span> in a paragraph.</p>""", styles))

    story.append(Paragraph("<b>HTML Tables</b>", styles['SectionH1']))
    story.append(code_box(
"""<table border="1">
  <tr>
    <th>Name</th>
    <th>Age</th>
    <th>City</th>
  </tr>
  <tr>
    <td>John</td>
    <td>25</td>
    <td>New York</td>
  </tr>
  <tr>
    <td>Jane</td>
    <td>30</td>
    <td>London</td>
  </tr>
</table>""", styles))
    story.append(PageBreak())

    # --- PAGE 5 ---
    story.append(Paragraph("<b>Table Tags:</b>", styles['SectionH2']))
    story.append(Paragraph("• <code>&lt;table&gt;</code> - Defines the table", styles['BulletCustom']))
    story.append(Paragraph("• <code>&lt;tr&gt;</code> - Table row", styles['BulletCustom']))
    story.append(Paragraph("• <code>&lt;th&gt;</code> - Table header cell", styles['BulletCustom']))
    story.append(Paragraph("• <code>&lt;td&gt;</code> - Table data cell", styles['BulletCustom']))
    story.append(Paragraph("• <code>&lt;thead&gt;</code> - Table header section", styles['BulletCustom']))
    story.append(Paragraph("• <code>&lt;tbody&gt;</code> - Table body section", styles['BulletCustom']))
    story.append(Paragraph("• <code>&lt;tfoot&gt;</code> - Table footer section", styles['BulletCustom']))

    story.append(Paragraph("<b>HTML Forms</b>", styles['SectionH1']))
    story.append(code_box(
"""<form action="/submit" method="POST">
  <label for="name">Name:</label>
  <input type="text" id="name" name="name" required>
  <label for="email">Email:</label>
  <input type="email" id="email" name="email">
  <label for="password">Password:</label>
  <input type="password" id="password" name="password">
  <label for="message">Message:</label>
  <textarea id="message" name="message" rows="4"></textarea>
  <label for="country">Country:</label>
  <select id="country" name="country">
    <option value="india">India</option>
    <option value="usa">USA</option>
    <option value="uk">UK</option>
  </select>
  <input type="radio" id="male" name="gender" value="male">
  <label for="male">Male</label>
  <input type="radio" id="female" name="gender" value="female">
  <label for="female">Female</label>
  <input type="checkbox" id="agree" name="agree">
  <label for="agree">I agree to terms</label>
  <input type="submit" value="Submit">
  <input type="reset" value="Reset">
</form>""", styles))
    story.append(PageBreak())

    # --- PAGE 6 ---
    story.append(Paragraph("<b>Form Input Types:</b>", styles['SectionH2']))
    story.append(Paragraph("• <code>text</code> - Single line text input", styles['BulletCustom']))
    story.append(Paragraph("• <code>password</code> - Password field (hidden characters)", styles['BulletCustom']))
    story.append(Paragraph("• <code>email</code> - Email input with validation", styles['BulletCustom']))
    story.append(Paragraph("• <code>number</code> - Numeric input", styles['BulletCustom']))
    story.append(Paragraph("• <code>date</code> - Date picker", styles['BulletCustom']))
    story.append(Paragraph("• <code>checkbox</code> - Checkbox for multiple selections", styles['BulletCustom']))
    story.append(Paragraph("• <code>radio</code> - Radio buttons for single selection", styles['BulletCustom']))
    story.append(Paragraph("• <code>submit</code> - Submit button", styles['BulletCustom']))
    story.append(Paragraph("• <code>reset</code> - Reset button", styles['BulletCustom']))
    story.append(Paragraph("• <code>file</code> - File upload", styles['BulletCustom']))
    story.append(Paragraph("• <code>hidden</code> - Hidden field", styles['BulletCustom']))

    story.append(Paragraph("<b>Semantic HTML Elements</b>", styles['SectionH1']))
    story.append(Paragraph("Semantic elements clearly describe their meaning to both browser and developer.", styles['BodyTextCustom']))
    story.append(Paragraph("<b>Examples:</b>", styles['SectionH2']))
    story.append(code_box(
"""<header>Website header</header>
<nav>Navigation links</nav>
<main>Main content</main>
<section>Section of content</section>
<article>Independent article</article>
<aside>Sidebar content</aside>
<footer>Footer content</footer>
<figure>
  <img src="image.jpg" alt="Description">
  <figcaption>Image caption</figcaption>
</figure>""", styles))

    story.append(Paragraph("<b>Benefits:</b>", styles['SectionH2']))
    story.append(Paragraph("• Better accessibility", styles['BulletCustom']))
    story.append(Paragraph("• Improved SEO", styles['BulletCustom']))
    story.append(Paragraph("• Easier to read and maintain", styles['BulletCustom']))
    story.append(Paragraph("• Clear document structure", styles['BulletCustom']))
    story.append(PageBreak())

    # --- PAGE 7 ---
    story.append(Paragraph("<b>HTML5 New Features</b>", styles['SectionH1']))
    story.append(Paragraph("<b>New Semantic Elements:</b>", styles['SectionH2']))
    story.append(Paragraph("• <code>&lt;header&gt;</code>, <code>&lt;footer&gt;</code>, <code>&lt;nav&gt;</code>, <code>&lt;main&gt;</code>", styles['BulletCustom']))
    story.append(Paragraph("• <code>&lt;section&gt;</code>, <code>&lt;article&gt;</code>, <code>&lt;aside&gt;</code>", styles['BulletCustom']))
    story.append(Paragraph("• <code>&lt;figure&gt;</code>, <code>&lt;figcaption&gt;</code>", styles['BulletCustom']))
    story.append(Paragraph("• <code>&lt;mark&gt;</code>, <code>&lt;time&gt;</code>, <code>&lt;progress&gt;</code>, <code>&lt;meter&gt;</code>", styles['BulletCustom']))

    story.append(Paragraph("<b>New Form Inputs:</b>", styles['SectionH2']))
    story.append(Paragraph("• <code>type=\"email\"</code>, <code>type=\"url\"</code>, <code>type=\"number\"</code>", styles['BulletCustom']))
    story.append(Paragraph("• <code>type=\"range\"</code>, <code>type=\"color\"</code>, <code>type=\"date\"</code>", styles['BulletCustom']))
    story.append(Paragraph("• <code>type=\"search\"</code>, <code>type=\"tel\"</code>", styles['BulletCustom']))

    story.append(Paragraph("<b>Multimedia:</b>", styles['SectionH2']))
    story.append(code_box(
"""<video controls width="640" height="480">
  <source src="movie.mp4" type="video/mp4">
  Your browser does not support video.
</video>

<audio controls>
  <source src="audio.mp3" type="audio/mpeg">
  Your browser does not support audio.
</audio>""", styles))

    story.append(Paragraph("<b>Graphics:</b>", styles['SectionH2']))
    story.append(Paragraph("• <code>&lt;canvas&gt;</code> - For drawing graphics via JavaScript", styles['BulletCustom']))
    story.append(Paragraph("• <code>&lt;svg&gt;</code> - For vector graphics", styles['BulletCustom']))

    story.append(Paragraph("<b>HTML Block vs Inline Elements</b>", styles['SectionH1']))
    story.append(PageBreak())

    # --- PAGE 8 ---
    story.append(Paragraph("<b>Block-Level Elements:</b>", styles['SectionH2']))
    story.append(Paragraph("• Always start on a new line", styles['BulletCustom']))
    story.append(Paragraph("• Take full width available", styles['BulletCustom']))
    story.append(code_box("""Examples: <div>, <p>, <h1>-<h6>, <ul>, <ol>, <li>, <table>, <form>""", styles))

    story.append(Paragraph("<b>Inline Elements:</b>", styles['SectionH2']))
    story.append(Paragraph("• Do not start on a new line", styles['BulletCustom']))
    story.append(Paragraph("• Take only necessary width", styles['BulletCustom']))
    story.append(code_box("""Examples: <span>, <a>, <img>, <b>, <i>, <strong>, <em>""", styles))

    story.append(Paragraph("<b>HTML Comments</b>", styles['SectionH1']))
    story.append(code_box(
"""<!-- This is a comment -->
<!-- Comments are not displayed in browser -->
<!-- Useful for notes and debugging -->""", styles))

    story.append(Paragraph("<b>HTML Character Entities</b>", styles['SectionH1']))
    story.append(Paragraph("Special characters that need to be escaped:", styles['BodyTextCustom']))
    
    ent_rows = [
        [Paragraph("<b>Character</b>", styles['BodyTextCustom']), Paragraph("<b>Entity</b>", styles['BodyTextCustom']), Paragraph("<b>Description</b>", styles['BodyTextCustom'])],
        [Paragraph("<", styles['BodyTextCustom']), Paragraph("&amp;lt;", styles['BodyTextCustom']), Paragraph("Less than", styles['BodyTextCustom'])],
        [Paragraph(">", styles['BodyTextCustom']), Paragraph("&amp;gt;", styles['BodyTextCustom']), Paragraph("Greater than", styles['BodyTextCustom'])],
        [Paragraph("&", styles['BodyTextCustom']), Paragraph("&amp;amp;", styles['BodyTextCustom']), Paragraph("Ampersand", styles['BodyTextCustom'])],
        [Paragraph('"', styles['BodyTextCustom']), Paragraph("&amp;quot;", styles['BodyTextCustom']), Paragraph("Double quote", styles['BodyTextCustom'])],
        [Paragraph("'", styles['BodyTextCustom']), Paragraph("&amp;apos;", styles['BodyTextCustom']), Paragraph("Single quote", styles['BodyTextCustom'])],
        [Paragraph("©", styles['BodyTextCustom']), Paragraph("&amp;copy;", styles['BodyTextCustom']), Paragraph("Copyright", styles['BodyTextCustom'])],
        [Paragraph("®", styles['BodyTextCustom']), Paragraph("&amp;reg;", styles['BodyTextCustom']), Paragraph("Registered trademark", styles['BodyTextCustom'])],
    ]
    t_e = Table(ent_rows, colWidths=[80, 160, 300])
    t_e.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_e)

    story.append(Paragraph("<b>HTML Best Practices</b>", styles['SectionH1']))
    story.append(Paragraph("1. Always close tags (except self-closing ones)", styles['BulletCustom']))
    story.append(Paragraph("2. Use lowercase for tag names", styles['BulletCustom']))
    story.append(Paragraph("3. Quote attribute values (use \" or ')", styles['BulletCustom']))
    story.append(Paragraph("4. Use semantic elements where possible", styles['BulletCustom']))
    story.append(PageBreak())

    # --- PAGE 9 ---
    story.append(Paragraph("5. Add alt text to images for accessibility", styles['BulletCustom']))
    story.append(Paragraph("6. Indent properly for readability", styles['BulletCustom']))
    story.append(Paragraph("7. Validate your HTML using W3C validator", styles['BulletCustom']))
    story.append(Paragraph("8. Use meaningful class and id names", styles['BulletCustom']))
    story.append(Paragraph("9. Keep structure separate from styling (use CSS)", styles['BulletCustom']))
    story.append(Paragraph("10. Test in multiple browsers", styles['BulletCustom']))

    story.append(Paragraph("<b>Example: Complete HTML Page</b>", styles['SectionH1']))
    story.append(code_box(
"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>My Web Page</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      margin: 0;
      padding: 20px;
    }
    header {
      background-color: #333;
      color: white;
      padding: 20px;
    }
    nav a {
      color: white;
      margin-right: 15px;
    }
  </style>
</head>
<body>
  <header>
    <h1>Welcome to My Website</h1>
    <nav>
      <a href="#home">Home</a>
      <a href="#about">About</a>
      <a href="#contact">Contact</a>
    </nav>
  </header>
  <main>
    <section id="home">
      <h2>Home Section</h2>
      <p>This is the home section content.</p>
    </section>
    <section id="about">
      <h2>About Section</h2>
      <p>Learn more about us here.</p>""", styles))
    story.append(PageBreak())

    # --- PAGE 10 ---
    story.append(code_box(
"""    </section>
  </main>
  <footer>
    <p>&copy; 2026 My Website. All rights reserved.</p>
  </footer>
</body>
</html>""", styles))

    story.append(Paragraph("<b>Quick Reference: Common Tags</b>", styles['SectionH1']))
    
    ref_data = [
        [Paragraph("<b>Tag</b>", styles['BodyTextCustom']), Paragraph("<b>Description</b>", styles['BodyTextCustom'])],
        [Paragraph("&lt;!DOCTYPE&gt;", styles['BodyTextCustom']), Paragraph("Document type declaration", styles['BodyTextCustom'])],
        [Paragraph("&lt;html&gt;", styles['BodyTextCustom']), Paragraph("Root element", styles['BodyTextCustom'])],
        [Paragraph("&lt;head&gt;", styles['BodyTextCustom']), Paragraph("Meta information container", styles['BodyTextCustom'])],
        [Paragraph("&lt;body&gt;", styles['BodyTextCustom']), Paragraph("Visible content container", styles['BodyTextCustom'])],
        [Paragraph("&lt;h1&gt;-&lt;h6&gt;", styles['BodyTextCustom']), Paragraph("Headings", styles['BodyTextCustom'])],
        [Paragraph("&lt;p&gt;", styles['BodyTextCustom']), Paragraph("Paragraph", styles['BodyTextCustom'])],
        [Paragraph("&lt;a&gt;", styles['BodyTextCustom']), Paragraph("Hyperlink", styles['BodyTextCustom'])],
        [Paragraph("&lt;img&gt;", styles['BodyTextCustom']), Paragraph("Image", styles['BodyTextCustom'])],
        [Paragraph("&lt;div&gt;", styles['BodyTextCustom']), Paragraph("Division/section", styles['BodyTextCustom'])],
        [Paragraph("&lt;span&gt;", styles['BodyTextCustom']), Paragraph("Inline container", styles['BodyTextCustom'])],
        [Paragraph("&lt;ul&gt;, &lt;ol&gt;, &lt;li&gt;", styles['BodyTextCustom']), Paragraph("Lists", styles['BodyTextCustom'])],
        [Paragraph("&lt;table&gt;, &lt;tr&gt;, &lt;td&gt;", styles['BodyTextCustom']), Paragraph("Tables", styles['BodyTextCustom'])],
        [Paragraph("&lt;form&gt;, &lt;input&gt;", styles['BodyTextCustom']), Paragraph("Forms", styles['BodyTextCustom'])],
        [Paragraph("&lt;header&gt;, &lt;footer&gt;", styles['BodyTextCustom']), Paragraph("Semantic sections", styles['BodyTextCustom'])],
    ]
    t_ref = Table(ref_data, colWidths=[150, 390])
    t_ref.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_ref)
    story.append(Spacer(1, 10))
    story.append(Paragraph("Notes converted to digital format - HTML Study Material", styles['FooterNote']))

    doc.build(story, canvasmaker=CustomHTMLCanvas)
    print(f"[OK] Compiled 10-page Typed HTML Notes: {dest_path}")

# =========================================================================
# 2. BUILD TYPED CSS NOTES (Following exact 71-page handwritten syllabus)
# =========================================================================
def build_typed_css_notes(dest_path):
    class CustomCSSCanvas(BrandedCanvas):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, title="CSS Notes - Typed Version", **kwargs)
            
    doc = SimpleDocTemplate(
        dest_path,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    styles = get_doc_styles()
    story = []
    
    # --- PAGE 1: Intro to CSS ---
    story.append(Paragraph("CSS Notes - Typed Version", styles['MainTitle']))
    story.append(Paragraph("<b>Introduction to CSS:</b>", styles['SectionH1']))
    story.append(Paragraph("• It is the language to use and style an HTML document", styles['BulletCustom']))
    story.append(Paragraph("• It describes how HTML elements should be displayed", styles['BulletCustom']))
    story.append(Paragraph("• CSS makes a website look pretty", styles['BulletCustom']))
    story.append(Paragraph("<b>Pre-requisites:</b> TAGS, ID, CLASS", styles['BodyTextCustom']))
    story.append(Paragraph("• Introduced in: 1996 by Håkon Wium Lie and W3C", styles['BulletCustom']))
    
    story.append(Paragraph("<b>What is CSS:</b>", styles['SectionH1']))
    story.append(Paragraph("• CSS stands for <b>Cascading Style Sheets</b>", styles['BulletCustom']))
    story.append(Paragraph("  (One by one / To make beautiful / Code written on by CSS)", styles['BulletCustom']))
    story.append(Paragraph("• CSS3 is the latest version. It describes how HTML elements are to be displayed on screen, paper, or in other media.", styles['BulletCustom']))
    story.append(Paragraph("• It saves a lot of work. It can control the layout of multiple web pages all at once.", styles['BulletCustom']))
    story.append(Paragraph("• External style sheets are stored in CSS files.", styles['BulletCustom']))
    
    story.append(Paragraph("<b>Why use CSS?</b>", styles['SectionH1']))
    story.append(Paragraph("• It is used to define styles for your web pages, including the design, layout, and variations in display for different devices and screen sizes.", styles['BulletCustom']))
    story.append(Paragraph("• The style sheets are normally saved in external CSS files.", styles['BulletCustom']))
    story.append(Paragraph("• With external style sheet files, you can change the entire website by changing just one file.", styles['BulletCustom']))
    story.append(PageBreak())
    
    # --- PAGE 2: Three Ways & Syntax ---
    story.append(Paragraph("<b>Three Ways to Add CSS:</b>", styles['SectionH1']))
    story.append(Paragraph("<b>1. Inline CSS:</b>", styles['SectionH2']))
    story.append(Paragraph("• An inline CSS is used to apply a unique style to a single HTML element.", styles['BulletCustom']))
    story.append(Paragraph("• An inline CSS uses the <code>style</code> attribute of an HTML element.", styles['BulletCustom']))
    story.append(code_box("""<h1 style="color: blue; text-align: center;">This is a heading</h1>""", styles))
    
    story.append(Paragraph("<b>2. Internal CSS:</b>", styles['SectionH2']))
    story.append(Paragraph("• An internal CSS is used to define a style for a single HTML page.", styles['BulletCustom']))
    story.append(Paragraph("• Defined in the <code>&lt;head&gt;</code> section within <code>&lt;style&gt;</code> element.", styles['BulletCustom']))
    story.append(code_box(
"""<head>
  <style>
    body { background-color: linen; }
    h1 { color: maroon; margin-left: 40px; }
  </style>
</head>""", styles))

    story.append(Paragraph("<b>3. External CSS:</b>", styles['SectionH2']))
    story.append(Paragraph("• An external style sheet is used to define the style for many pages.", styles['BulletCustom']))
    story.append(Paragraph("• With an external style sheet, you can change the look of an entire website by changing one file!", styles['BulletCustom']))
    story.append(code_box("""<link rel="stylesheet" type="text/css" href="mystyle.css">""", styles))
    
    story.append(Paragraph("<b>CSS Syntax:</b>", styles['SectionH1']))
    story.append(Paragraph("• A CSS rule consists of a <b>Selector</b> and a <b>Declaration block</b>.", styles['BulletCustom']))
    story.append(code_box(
"""/* Selector { property: value; } */
h1 {
  color: blue;
  font-size: 12px;
}""", styles))
    story.append(PageBreak())

    # --- PAGE 3: Selectors & Combinators ---
    story.append(Paragraph("<b>CSS Selectors:</b>", styles['SectionH1']))
    story.append(Paragraph("CSS selectors are used to 'find' (or select) the HTML elements you want to style.", styles['BodyTextCustom']))
    story.append(Paragraph("• <b>Simple Selectors:</b> Select elements based on name, id, class", styles['BulletCustom']))
    story.append(Paragraph("  - Element Selector: <code>p { text-align: center; color: red; }</code>", styles['BulletCustom']))
    story.append(Paragraph("  - ID Selector: <code>#para1 { text-align: center; color: red; }</code> (unique)", styles['BulletCustom']))
    story.append(Paragraph("  - Class Selector: <code>.center { text-align: center; color: red; }</code> (reusable)", styles['BulletCustom']))
    story.append(Paragraph("  - Universal Selector: <code>* { margin: 0; padding: 0; }</code> (targets all)", styles['BulletCustom']))
    story.append(Paragraph("  - Grouping Selector: <code>h1, h2, p { text-align: center; color: red; }</code>", styles['BulletCustom']))

    story.append(Paragraph("<b>CSS Combinators:</b>", styles['SectionH1']))
    story.append(Paragraph("A combinator explains the relationship between selectors:", styles['BodyTextCustom']))
    story.append(Paragraph("• <b>Descendant selector (space):</b> <code>div p</code> - matches all &lt;p&gt; elements inside &lt;div&gt;", styles['BulletCustom']))
    story.append(Paragraph("• <b>Child selector (&gt;):</b> <code>div &gt; p</code> - matches all &lt;p&gt; elements that are direct children of &lt;div&gt;", styles['BulletCustom']))
    story.append(Paragraph("• <b>Adjacent sibling selector (+):</b> <code>div + p</code> - matches &lt;p&gt; placed immediately after &lt;div&gt;", styles['BulletCustom']))
    story.append(Paragraph("• <b>General sibling selector (~):</b> <code>div ~ p</code> - matches all &lt;p&gt; that are siblings of &lt;div&gt;", styles['BulletCustom']))

    story.append(Paragraph("<b>Pseudo-classes & Pseudo-elements:</b>", styles['SectionH2']))
    story.append(Paragraph("• <b>Pseudo-classes:</b> <code>a:hover</code>, <code>a:visited</code>, <code>input:focus</code>, <code>li:first-child</code>, <code>li:nth-child(even)</code>", styles['BulletCustom']))
    story.append(Paragraph("• <b>Pseudo-elements:</b> <code>p::first-line</code>, <code>p::first-letter</code>, <code>h1::before</code>, <code>h1::after</code>", styles['BulletCustom']))
    story.append(PageBreak())

    # --- PAGE 4: CSS Colors ---
    story.append(Paragraph("<b>CSS Colors (RGB, RGBA, HSL, HSLA, HEX):</b>", styles['SectionH1']))
    story.append(Paragraph("In CSS, colors can be specified using color names, RGB, RGBA, HSL, HSLA, or HEX values.", styles['BodyTextCustom']))
    
    story.append(Paragraph("<b>1. RGB Color:</b>", styles['SectionH2']))
    story.append(Paragraph("• Represents Red, Green, and Blue light sources (0 to 255).", styles['BulletCustom']))
    story.append(code_box(
"""h3 {
  color: rgb(255, 99, 71); /* Tomato red */
}""", styles))

    story.append(Paragraph("<b>2. RGBA Color:</b>", styles['SectionH2']))
    story.append(Paragraph("• RGBA color values are an extension of RGB with an Alpha channel (opacity: 0.0 to 1.0).", styles['BulletCustom']))
    story.append(code_box(
"""h3 {
  color: rgba(255, 99, 71, 0.5); /* 50% opacity */
}""", styles))

    story.append(Paragraph("<b>3. HSL Color:</b>", styles['SectionH2']))
    story.append(Paragraph("• In CSS, a color can be specified using HSL (Hue, Saturation, Lightness).", styles['BulletCustom']))
    story.append(Paragraph("  - Hue: degree on the color wheel from 0 to 360 (0=red, 120=green, 240=blue).", styles['BulletCustom']))
    story.append(Paragraph("  - Saturation: percentage value (0% = shade of gray, 100% = full color).", styles['BulletCustom']))
    story.append(Paragraph("  - Lightness: percentage value (0% = black, 50% = normal, 100% = white).", styles['BulletCustom']))
    story.append(code_box(
"""h5 {
  color: hsl(0, 100%, 50%); /* Pure red */
}""", styles))

    story.append(Paragraph("<b>4. HSLA Color:</b>", styles['SectionH2']))
    story.append(Paragraph("• HSLA color values are an extension of HSL with an Alpha channel (opacity 0.0 to 1.0).", styles['BulletCustom']))
    story.append(code_box(
"""p {
  color: hsla(165, 16%, 7%, 0.5);
}""", styles))

    story.append(Paragraph("<b>5. HEX Color:</b>", styles['SectionH2']))
    story.append(code_box("""#p1 { color: #ff0000; /* Red */ }""", styles))
    story.append(PageBreak())

    # --- PAGE 5: CSS Box Model & Backgrounds ---
    story.append(Paragraph("<b>CSS Backgrounds & Box Model:</b>", styles['SectionH1']))
    story.append(Paragraph("<b>Background Properties:</b>", styles['SectionH2']))
    story.append(Paragraph("• <code>background-color</code> - Sets background color", styles['BulletCustom']))
    story.append(Paragraph("• <code>background-image</code> - Sets image: <code>url('bg.jpg')</code>", styles['BulletCustom']))
    story.append(Paragraph("• <code>background-repeat</code> - <code>repeat</code>, <code>no-repeat</code>, <code>repeat-x</code>, <code>repeat-y</code>", styles['BulletCustom']))
    story.append(Paragraph("• <code>background-position</code> - <code>top right</code>, <code>center</code>, etc.", styles['BulletCustom']))
    story.append(Paragraph("• <code>background-size</code> - <code>cover</code>, <code>contain</code>, <code>100% 100%</code>", styles['BulletCustom']))
    story.append(Paragraph("• <code>background-attachment</code> - <code>fixed</code> (parallax), <code>scroll</code>", styles['BulletCustom']))

    story.append(Paragraph("<b>The CSS Box Model:</b>", styles['SectionH1']))
    story.append(Paragraph("All HTML elements can be considered as boxes. The CSS box model is essentially a box that wraps around every HTML element. It consists of:", styles['BodyTextCustom']))
    story.append(Paragraph("1. <b>Content:</b> The content of the box, where text and images appear.", styles['BulletCustom']))
    story.append(Paragraph("2. <b>Padding:</b> Clears an area around the content. The padding is transparent.", styles['BulletCustom']))
    story.append(Paragraph("3. <b>Border:</b> A border that goes around the padding and content.", styles['BulletCustom']))
    story.append(Paragraph("4. <b>Margin:</b> Clears an area outside the border. The margin is transparent.", styles['BulletCustom']))
    story.append(code_box(
"""div {
  width: 300px;
  border: 15px solid green;
  padding: 50px;
  margin: 20px;
  box-sizing: border-box; /* Crucial for modern responsive layout */
}""", styles))
    story.append(PageBreak())

    # --- PAGE 6: Positioning, Display & Flexbox ---
    story.append(Paragraph("<b>Display, Positioning & Flexbox:</b>", styles['SectionH1']))
    story.append(Paragraph("<b>CSS Display Property:</b>", styles['SectionH2']))
    story.append(Paragraph("• <code>display: none;</code> - Element is completely hidden and removed from flow.", styles['BulletCustom']))
    story.append(Paragraph("• <code>visibility: hidden;</code> - Element is hidden but still takes up space.", styles['BulletCustom']))
    story.append(Paragraph("• <code>display: block;</code> - Starts on new line, takes full width (e.g. div, p, h1).", styles['BulletCustom']))
    story.append(Paragraph("• <code>display: inline;</code> - Does not start on new line, takes only required width (e.g. span, a).", styles['BulletCustom']))
    story.append(Paragraph("• <code>display: inline-block;</code> - Formatted as inline, but can set width/height.", styles['BulletCustom']))

    story.append(Paragraph("<b>CSS Positioning:</b>", styles['SectionH1']))
    story.append(Paragraph("• <b>static:</b> Default. Follows normal document flow.", styles['BulletCustom']))
    story.append(Paragraph("• <b>relative:</b> Positioned relative to its normal position.", styles['BulletCustom']))
    story.append(Paragraph("• <b>absolute:</b> Positioned relative to the nearest positioned ancestor.", styles['BulletCustom']))
    story.append(Paragraph("• <b>fixed:</b> Positioned relative to the viewport; stays in place during scroll.", styles['BulletCustom']))
    story.append(Paragraph("• <b>sticky:</b> Toggles between relative and fixed depending on scroll position.", styles['BulletCustom']))
    story.append(Paragraph("• <b>z-index:</b> Specifies the stack order of an element (greater value on top).", styles['BulletCustom']))

    story.append(Paragraph("<b>CSS Flexbox Layout:</b>", styles['SectionH1']))
    story.append(code_box(
""".flex-container {
  display: flex;
  flex-direction: row;            /* row | column */
  justify-content: space-between; /* flex-start | center | flex-end | space-between */
  align-items: center;            /* stretch | center | flex-start | flex-end */
  flex-wrap: wrap;                /* nowrap | wrap */
  gap: 15px;                      /* Spacing between items */
}
.flex-item {
  flex: 1 1 200px;                /* flex-grow, flex-shrink, flex-basis */
}""", styles))
    story.append(PageBreak())

    # --- PAGE 7: CSS Grid, Transitions & Media Queries ---
    story.append(Paragraph("<b>CSS Grid, Transitions & Media Queries:</b>", styles['SectionH1']))
    story.append(Paragraph("<b>CSS Grid Layout:</b>", styles['SectionH2']))
    story.append(code_box(
""".grid-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}""", styles))

    story.append(Paragraph("<b>CSS Transitions & Animations:</b>", styles['SectionH2']))
    story.append(code_box(
"""/* Smooth hover transition */
.btn {
  transition: background-color 0.3s ease, transform 0.2s;
}
.btn:hover {
  background-color: #ea580c;
  transform: translateY(-2px);
}

/* Keyframe Animation */
@keyframes fadeIn {
  from { opacity: 0; }
  to   { opacity: 1; }
}
.banner {
  animation: fadeIn 1s ease-in-out;
}""", styles))

    story.append(Paragraph("<b>Responsive Web Design & Media Queries:</b>", styles['SectionH1']))
    story.append(code_box(
"""/* Desktop First or Mobile First */
@media screen and (max-width: 768px) {
  .flex-container {
    flex-direction: column;
  }
}""", styles))

    story.append(Paragraph("<b>CSS Variables (Custom Properties):</b>", styles['SectionH2']))
    story.append(code_box(
""":root {
  --primary-color: #ea580c;
  --secondary-color: #0f172a;
}
h1 {
  color: var(--primary-color);
}""", styles))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Notes converted to digital format - CSS Study Material", styles['FooterNote']))

    doc.build(story, canvasmaker=CustomCSSCanvas)
    print(f"[OK] Compiled Typed CSS Notes: {dest_path}")

# =========================================================================
# 3. WATERMARK FUNCTION FOR DIGITAL VECTOR PDFS (MONGODB, REACT, AWS)
# =========================================================================
def watermark_existing_pdf(input_path, output_path, title):
    print(f"Watermarking existing PDF: {os.path.basename(input_path)}...")
    reader = pypdf.PdfReader(input_path)
    writer = pypdf.PdfWriter()
    total_pages = len(reader.pages)
    
    for idx, page in enumerate(reader.pages):
        w = float(page.mediabox.width)
        h = float(page.mediabox.height)
        
        # Generate overlay
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=(w, h))
        
        # Center logo watermark badge
        logo_w, logo_h = 130, 130
        can.drawImage(
            subtle_wm_path,
            (w - logo_w) / 2.0,
            (h - logo_h) / 2.0 + 15,
            width=logo_w,
            height=logo_h,
            mask='auto'
        )
        
        can.saveState()
        can.setFillColor(colors.HexColor('#0f172a'))
        can.setFillAlpha(0.045)
        can.setFont('Helvetica-Bold', 26)
        can.drawCentredString(w / 2.0, (h - logo_h) / 2.0 - 10, 'REVISE-X')
        can.restoreState()
        
        # Top Header Bar
        can.saveState()
        can.drawImage(mini_header_path, 36, h - 26, width=14, height=14, mask='auto')
        can.setFont('Helvetica-Bold', 8)
        can.setFillColor(colors.HexColor('#ea580c'))
        can.drawString(54, h - 22, 'REVISE-X')
        
        can.setFont('Helvetica', 7.5)
        can.setFillColor(colors.HexColor('#64748b'))
        can.drawRightString(w - 36, h - 22, title)
        
        can.setStrokeColor(colors.HexColor('#cbd5e1'))
        can.setStrokeAlpha(0.6)
        can.setLineWidth(0.5)
        can.line(36, h - 28, w - 36, h - 28)
        can.restoreState()
        
        # Bottom Footer Bar
        can.saveState()
        can.setStrokeColor(colors.HexColor('#cbd5e1'))
        can.setStrokeAlpha(0.6)
        can.setLineWidth(0.5)
        can.line(36, 28, w - 36, 28)
        
        can.setFont('Helvetica', 7.5)
        can.setFillColor(colors.HexColor('#64748b'))
        can.drawString(36, 17, '© Revise-X • All Rights Reserved')
        can.drawCentredString(w / 2.0, 17, 'www.revise-x.com')
        can.drawRightString(w - 36, 17, f'Page {idx + 1} of {total_pages}')
        can.restoreState()
        
        can.save()
        packet.seek(0)
        overlay_page = pypdf.PdfReader(packet).pages[0]
        page.merge_page(overlay_page)
        writer.add_page(page)
        
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'wb') as f:
        writer.write(f)
    print(f"[OK] Watermarked {total_pages} pages for {os.path.basename(output_path)}")

def main():
    assets_dir = r'frontend/src/assets/notebooks'
    public_dir = r'frontend/public/notebooks'
    backup_dir = r'frontend/src/assets/others/handwritten_backup'
    os.makedirs(assets_dir, exist_ok=True)
    os.makedirs(public_dir, exist_ok=True)
    os.makedirs(backup_dir, exist_ok=True)
    
    # 1. Backup original handwritten scans first so nothing is lost
    orig_html = os.path.join(assets_dir, 'HTML NOTES.pdf')
    orig_css = os.path.join(assets_dir, 'CSS NOTES.pdf')
    if os.path.exists(orig_html) and not os.path.exists(os.path.join(backup_dir, 'HTML NOTES (Handwritten Scans).pdf')):
        shutil.copy2(orig_html, os.path.join(backup_dir, 'HTML NOTES (Handwritten Scans).pdf'))
    if os.path.exists(orig_css) and not os.path.exists(os.path.join(backup_dir, 'CSS NOTES (Handwritten Scans).pdf')):
        shutil.copy2(orig_css, os.path.join(backup_dir, 'CSS NOTES (Handwritten Scans).pdf'))
        
    # 2. Build the 10-page Typed HTML Notes
    temp_html = os.path.join(public_dir, 'temp_html.pdf')
    build_typed_html_notes(temp_html)
    shutil.copy2(temp_html, os.path.join(assets_dir, 'HTML NOTES.pdf'))
    shutil.copy2(temp_html, os.path.join(public_dir, 'html-notes.pdf'))
    os.remove(temp_html)

    # 3. Build the Typed CSS Notes
    temp_css = os.path.join(public_dir, 'temp_css.pdf')
    build_typed_css_notes(temp_css)
    shutil.copy2(temp_css, os.path.join(assets_dir, 'CSS NOTES.pdf'))
    shutil.copy2(temp_css, os.path.join(public_dir, 'css-notes.pdf'))
    os.remove(temp_css)

    # 4. Watermark MONGODB, REACT, and AWS notes with the Revise-X logo badge
    # Keep original in backup or read from assets
    mongo_src = os.path.join(assets_dir, 'MONGODB NOTES.pdf')
    react_src = os.path.join(assets_dir, 'REACT NOTES.pdf')
    aws_src = os.path.join(assets_dir, 'AWS NOTES - EC2, S3, IAM.pdf')
    
    # Process MongoDB
    temp_mongo = os.path.join(public_dir, 'temp_mongo.pdf')
    watermark_existing_pdf(mongo_src, temp_mongo, 'MongoDB & Aggregation Pipeline • Revise-X')
    shutil.copy2(temp_mongo, mongo_src)
    shutil.copy2(temp_mongo, os.path.join(public_dir, 'mongodb-notes.pdf'))
    os.remove(temp_mongo)

    # Process React
    temp_react = os.path.join(public_dir, 'temp_react.pdf')
    watermark_existing_pdf(react_src, temp_react, 'React Architecture & State Guide • Revise-X')
    shutil.copy2(temp_react, react_src)
    shutil.copy2(temp_react, os.path.join(public_dir, 'react-notes.pdf'))
    os.remove(temp_react)

    # Process AWS
    temp_aws = os.path.join(public_dir, 'temp_aws.pdf')
    watermark_existing_pdf(aws_src, temp_aws, 'AWS Cloud Core (IAM, S3, EC2) • Revise-X')
    shutil.copy2(temp_aws, aws_src)
    shutil.copy2(temp_aws, os.path.join(public_dir, 'aws-services-notes.pdf'))
    os.remove(temp_aws)

    # 5. Clean up all unwanted duplicate notes in assets_dir
    allowed_assets = {
        'HTML NOTES.pdf',
        'CSS NOTES.pdf',
        'MONGODB NOTES.pdf',
        'REACT NOTES.pdf',
        'AWS NOTES - EC2, S3, IAM.pdf',
        'README.md'
    }
    for item in os.listdir(assets_dir):
        if item not in allowed_assets:
            path = os.path.join(assets_dir, item)
            if os.path.isfile(path):
                os.remove(path)
                print(f"[REMOVED UNWANTED ASSET] {item}")

    # 6. Clean up public notebooks folder
    allowed_public = {
        'html-notes.pdf',
        'css-notes.pdf',
        'mongodb-notes.pdf',
        'react-notes.pdf',
        'aws-services-notes.pdf',
        'README.md'
    }
    for item in os.listdir(public_dir):
        if item not in allowed_public:
            path = os.path.join(public_dir, item)
            if os.path.isfile(path):
                os.remove(path)
                print(f"[REMOVED UNWANTED PUBLIC] {item}")

    print("\n========================================================")
    print("SUCCESS: Exactly 5 Clean Note PDFs remain in both locations!")
    print("Assets folder:", os.listdir(assets_dir))
    print("Public folder:", os.listdir(public_dir))
    print("========================================================")

if __name__ == '__main__':
    main()

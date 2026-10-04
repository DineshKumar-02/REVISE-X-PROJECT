import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class ReviseXWatermarkCanvas(canvas.Canvas):
    """Custom canvas that applies Revise-X watermark, running header, and footer to every page."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pages = []
        
    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()
        
    def save(self):
        num_pages = len(self.pages)
        for page in self.pages:
            self.__dict__.update(page)
            self.draw_watermark_and_bars(num_pages)
            super().showPage()
        super().save()
        
    def draw_watermark_and_bars(self, total_pages):
        width, height = letter
        
        # 1. Subtle diagonal center watermark (4.2% opacity)
        self.saveState()
        self.translate(width / 2.0, height / 2.0)
        self.rotate(45)
        self.setFillColor(colors.HexColor('#0f172a'))
        self.setFillAlpha(0.042)
        self.setFont('Helvetica-Bold', 54)
        self.drawCentredString(0, 0, 'REVISE-X')
        self.restoreState()
        
        # Skip header/footer on cover page (page 1)
        if self._pageNumber > 1:
            # Top Running Header Bar
            self.saveState()
            self.setStrokeColor(colors.HexColor('#cbd5e1'))
            self.setStrokeAlpha(0.6)
            self.setLineWidth(0.5)
            self.line(36, height - 28, width - 36, height - 28)
            
            self.setFont('Helvetica-Bold', 8)
            self.setFillColor(colors.HexColor('#ea580c'))
            self.drawString(36, height - 23, 'REVISE-X')
            
            self.setFont('Helvetica', 7.5)
            self.setFillColor(colors.HexColor('#64748b'))
            self.drawRightString(width - 36, height - 23, 'HTML5 & Modern CSS3 • Digital Master Edition')
            self.restoreState()
            
            # Bottom Running Footer Bar
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

def build_styles():
    styles = getSampleStyleSheet()
    
    # Custom Palette Styles
    styles.add(ParagraphStyle(
        name='ReviseCoverTitle',
        fontName='Helvetica-Bold',
        fontSize=28,
        leading=34,
        textColor=colors.HexColor('#0f172a'),
        alignment=1, # Center
        spaceAfter=10
    ))
    
    styles.add(ParagraphStyle(
        name='ReviseCoverSubtitle',
        fontName='Helvetica',
        fontSize=13,
        leading=18,
        textColor=colors.HexColor('#ea580c'),
        alignment=1,
        spaceAfter=20
    ))
    
    styles.add(ParagraphStyle(
        name='ReviseCoverMeta',
        fontName='Helvetica',
        fontSize=9,
        leading=14,
        textColor=colors.HexColor('#64748b'),
        alignment=1
    ))
    
    styles.add(ParagraphStyle(
        name='ReviseH1',
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=16,
        spaceAfter=8,
        keepWithNext=True
    ))
    
    styles.add(ParagraphStyle(
        name='ReviseH2',
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor('#ea580c'),
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    ))
    
    styles.add(ParagraphStyle(
        name='ReviseH3',
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor('#1e293b'),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    ))
    
    styles.add(ParagraphStyle(
        name='ReviseBody',
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=colors.HexColor('#334155'),
        spaceAfter=6
    ))
    
    styles.add(ParagraphStyle(
        name='ReviseBullet',
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=colors.HexColor('#334155'),
        leftIndent=15,
        spaceAfter=3
    ))
    
    styles.add(ParagraphStyle(
        name='ReviseCode',
        fontName='Courier',
        fontSize=7.8,
        leading=10.5,
        textColor=colors.HexColor('#f8fafc')
    ))
    
    styles.add(ParagraphStyle(
        name='CalloutText',
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor('#1e293b')
    ))
    
    return styles

def make_code_box(code_text, styles):
    """Wraps code text in a dark syntax card."""
    cleaned = code_text.strip().replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    p = Paragraph(f"<font face='Courier'>{cleaned.replace(chr(10), '<br/>')}</font>", styles['ReviseCode'])
    t = Table([[p]], colWidths=[540])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#0f172a')),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#334155')),
    ]))
    return t

def make_callout(text, styles, alert_type='note'):
    """Generates an elegant tip or note callout box."""
    border_color = colors.HexColor('#ea580c') if alert_type == 'tip' else colors.HexColor('#0284c7')
    bg_color = colors.HexColor('#fff7ed') if alert_type == 'tip' else colors.HexColor('#f0f9ff')
    prefix = "<b>PRO TIP:</b> " if alert_type == 'tip' else "<b>KEY NOTE:</b> "
    p = Paragraph(f"{prefix}{text}", styles['CalloutText'])
    t = Table([[p]], colWidths=[540])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), bg_color),
        ('LINELEFT', (0, 0), (0, 0), 3, border_color),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    return t

def generate_html_css_digital_guide(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=40,
        bottomMargin=38
    )
    
    styles = build_styles()
    story = []
    
    # ------------------ COVER PAGE ------------------
    story.append(Spacer(1, 40))
    # Badge
    badge_p = Paragraph("<font color='#ea580c'><b>REVISE-X OFFICIAL DIGITAL NOTES</b></font>", styles['ReviseCoverMeta'])
    story.append(badge_p)
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("HTML5 & Modern CSS3", styles['ReviseCoverTitle']))
    story.append(Paragraph("Master Cheatsheet & Developer Quick-Reference", styles['ReviseCoverSubtitle']))
    
    story.append(HRFlowable(width="60%", thickness=1.5, color=colors.HexColor('#ea580c'), spaceBefore=10, spaceAfter=20))
    
    desc = (
        "A comprehensive, digital transformation of handwritten and practical developer notes. "
        "Covers Semantic HTML5, Forms, Tables, Complete CSS3 Box Model, Flexbox Architecture, "
        "CSS Grid, Modern Variables, Responsive Media Queries, and Top Interview Questions."
    )
    story.append(Paragraph(desc, styles['ReviseBody']))
    story.append(Spacer(1, 20))
    
    # Overview Table
    summary_data = [
        [Paragraph("<b>Topic</b>", styles['ReviseBody']), Paragraph("<b>Coverage Highlights</b>", styles['ReviseBody'])],
        [Paragraph("HTML5 Core", styles['ReviseBody']), Paragraph("Document lifecycle, tags vs elements, semantic tags, forms & inputs", styles['ReviseBody'])],
        [Paragraph("HTML Tables & Lists", styles['ReviseBody']), Paragraph("Nested lists, colspan, rowspan, table architecture (thead, tbody, tfoot)", styles['ReviseBody'])],
        [Paragraph("CSS3 Fundamentals", styles['ReviseBody']), Paragraph("Box model, specificity, inheritance, selectors & pseudo-classes", styles['ReviseBody'])],
        [Paragraph("Flexbox & Grid", styles['ReviseBody']), Paragraph("1D vs 2D layout systems, alignment matrices, responsive tracks & gap", styles['ReviseBody'])],
        [Paragraph("Modern CSS & RWD", styles['ReviseBody']), Paragraph("CSS Variables, clamp() fluid sizing, transforms, transitions, animations", styles['ReviseBody'])],
    ]
    summary_table = Table(summary_data, colWidths=[140, 400])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f5f9')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 30))
    
    story.append(Paragraph("<b>Edition:</b> 2026 Digital Verified Edition • <b>Platform:</b> Revise-X Developer Hub", styles['ReviseCoverMeta']))
    story.append(PageBreak())
    
    # ------------------ SECTION 1: HTML5 CORE ------------------
    story.append(Paragraph("Chapter 1: HTML5 Architecture & Document Flow", styles['ReviseH1']))
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor('#ea580c'), spaceBefore=2, spaceAfter=8))
    
    story.append(Paragraph(
        "<b>HTML (HyperText Markup Language)</b> is the foundational markup standard used to structure content for the World Wide Web. "
        "It consists of a hierarchy of elements represented by opening and closing tags.",
        styles['ReviseBody']
    ))
    
    story.append(Paragraph("Standard HTML5 Skeleton", styles['ReviseH2']))
    story.append(make_code_box(
"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Revise-X | Study Hub</title>
    <link rel="stylesheet" href="style.css" />
  </head>
  <body>
    <header>
      <h1>Welcome to Revise-X</h1>
    </header>
    <main>
      <p>Master coding with verified study notes.</p>
    </main>
    <footer>
      <p>&copy; 2026 Revise-X</p>
    </footer>
  </body>
</html>""", styles))
    
    story.append(Spacer(1, 6))
    story.append(make_callout("Always include <code>meta viewport</code> for mobile responsiveness and a descriptive <code>title</code> tag for SEO ranking.", styles, 'tip'))
    
    story.append(Paragraph("Tags vs Elements vs Attributes", styles['ReviseH2']))
    story.append(Paragraph("• <b>Tag:</b> The raw markup delimiters, e.g., <code>&lt;p&gt;</code> (start tag) and <code>&lt;/p&gt;</code> (end tag).", styles['ReviseBullet']))
    story.append(Paragraph("• <b>Element:</b> The entire unit starting from the opening tag, inner content, to the closing tag: <code>&lt;p&gt;Hello World&lt;/p&gt;</code>.", styles['ReviseBullet']))
    story.append(Paragraph("• <b>Attribute:</b> Key-value properties specified inside the opening tag: <code>&lt;a href=\"https://revise-x.com\" target=\"_blank\"&gt;</code>.", styles['ReviseBullet']))
    
    story.append(Paragraph("HTML Comments", styles['ReviseH3']))
    story.append(Paragraph("Comments are ignored by browser rendering engines but are essential for documentation:", styles['ReviseBody']))
    story.append(make_code_box(
"""<!-- Single-line comment: Explains this section -->
<!--
  Multi-line Comment:
  Author: Revise-X
  Last Updated: 2026
-->""", styles))

    story.append(Paragraph("Text Formatting Tags", styles['ReviseH2']))
    story.append(Paragraph("• <code>&lt;strong&gt;</code>: Defines important text with strong semantic weight (renders bold).", styles['ReviseBullet']))
    story.append(Paragraph("• <code>&lt;em&gt;</code>: Defines emphasized text (renders italics) with semantic stress.", styles['ReviseBullet']))
    story.append(Paragraph("• <code>&lt;mark&gt;</code>: Highlights text with default yellow background.", styles['ReviseBullet']))
    story.append(Paragraph("• <code>&lt;del&gt;</code> and <code>&lt;ins&gt;</code>: Represents deleted (strikethrough) and inserted (underlined) text.", styles['ReviseBullet']))
    story.append(Paragraph("• <code>&lt;sub&gt;</code> and <code>&lt;sup&gt;</code>: Subscript (e.g. H₂O) and Superscript (e.g. x²).", styles['ReviseBullet']))
    
    story.append(PageBreak())
    
    # ------------------ SECTION 2: HTML STRUCTURES ------------------
    story.append(Paragraph("Chapter 2: Lists, Tables & Forms", styles['ReviseH1']))
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor('#ea580c'), spaceBefore=2, spaceAfter=8))
    
    story.append(Paragraph("1. Ordered, Unordered & Description Lists", styles['ReviseH2']))
    story.append(make_code_box(
"""<!-- Unordered List (Bulleted) -->
<ul>
  <li>HTML5 Core</li>
  <li>CSS3 Styling</li>
</ul>

<!-- Ordered List (Numbered) -->
<ol start="1" type="1">
  <li>Setup project</li>
  <li>Deploy to AWS</li>
</ol>

<!-- Description List -->
<dl>
  <dt>HTML</dt>
  <dd>HyperText Markup Language</dd>
  <dt>CSS</dt>
  <dd>Cascading Style Sheets</dd>
</dl>""", styles))

    story.append(Paragraph("2. HTML Tables & Structural Architecture", styles['ReviseH2']))
    story.append(Paragraph("Accessible tables utilize <code>&lt;thead&gt;</code>, <code>&lt;tbody&gt;</code>, <code>&lt;tfoot&gt;</code>, and <code>scope</code> attributes:", styles['ReviseBody']))
    story.append(make_code_box(
"""<table border="1" cellpadding="8">
  <thead>
    <tr>
      <th scope="col">Subject</th>
      <th scope="col">Pages</th>
      <th scope="col">Price</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>HTML & CSS Guide</td>
      <td>100+</td>
      <td>₹50</td>
    </tr>
    <tr>
      <td colspan="2">Master All-in-One Bundle</td>
      <td>₹199</td>
    </tr>
  </tbody>
</table>""", styles))

    story.append(Spacer(1, 4))
    story.append(make_callout("Use <code>colspan</code> to span across horizontal columns and <code>rowspan</code> to span across vertical rows.", styles, 'note'))

    story.append(Paragraph("3. HTML5 Forms & Comprehensive Input Types", styles['ReviseH2']))
    story.append(make_code_box(
"""<form action="/api/submit" method="POST">
  <label for="student-name">Full Name:</label>
  <input type="text" id="student-name" name="name" required placeholder="John Doe" />

  <label for="student-email">Email Address:</label>
  <input type="email" id="student-email" name="email" required />

  <label for="pwd">Password:</label>
  <input type="password" id="pwd" name="password" minlength="8" required />

  <label for="track">Select Track:</label>
  <select id="track" name="track">
    <option value="frontend">Frontend Master</option>
    <option value="backend">Backend Master</option>
    <option value="cloud">Cloud Architecture</option>
  </select>

  <button type="submit">Enroll Now</button>
</form>""", styles))

    story.append(PageBreak())

    # ------------------ SECTION 3: CSS FUNDAMENTALS ------------------
    story.append(Paragraph("Chapter 3: CSS3 Fundamentals & Selectors", styles['ReviseH1']))
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor('#ea580c'), spaceBefore=2, spaceAfter=8))
    
    story.append(Paragraph("Three Ways to Apply CSS", styles['ReviseH2']))
    story.append(Paragraph("1. <b>Inline CSS:</b> Direct attribute: <code>&lt;h1 style=\"color: #ea580c;\"&gt;</code> (Avoid for large projects).", styles['ReviseBullet']))
    story.append(Paragraph("2. <b>Internal CSS:</b> Embedded in <code>&lt;head&gt;</code> via <code>&lt;style&gt;</code> tag.", styles['ReviseBullet']))
    story.append(Paragraph("3. <b>External CSS (Recommended):</b> Linked via <code>&lt;link rel=\"stylesheet\" href=\"style.css\"&gt;</code>.", styles['ReviseBullet']))

    story.append(Paragraph("CSS Specificity Hierarchy (Calculated Weight)", styles['ReviseH2']))
    story.append(Paragraph("When conflicting styles apply to an element, the browser determines priority by specificity score:", styles['ReviseBody']))
    
    spec_data = [
        [Paragraph("<b>Level</b>", styles['ReviseBody']), Paragraph("<b>Selector Type</b>", styles['ReviseBody']), Paragraph("<b>Example</b>", styles['ReviseBody']), Paragraph("<b>Score</b>", styles['ReviseBody'])],
        [Paragraph("1", styles['ReviseBody']), Paragraph("!important", styles['ReviseBody']), Paragraph("color: red !important;", styles['ReviseBody']), Paragraph("Highest (Override)", styles['ReviseBody'])],
        [Paragraph("2", styles['ReviseBody']), Paragraph("Inline Style", styles['ReviseBody']), Paragraph("style=\"...\"", styles['ReviseBody']), Paragraph("1000", styles['ReviseBody'])],
        [Paragraph("3", styles['ReviseBody']), Paragraph("ID Selector", styles['ReviseBody']), Paragraph("#navbar", styles['ReviseBody']), Paragraph("0100", styles['ReviseBody'])],
        [Paragraph("4", styles['ReviseBody']), Paragraph("Class / Pseudo-class", styles['ReviseBody']), Paragraph(".btn, :hover", styles['ReviseBody']), Paragraph("0010", styles['ReviseBody'])],
        [Paragraph("5", styles['ReviseBody']), Paragraph("Element / Pseudo-element", styles['ReviseBody']), Paragraph("p, div, ::before", styles['ReviseBody']), Paragraph("0001", styles['ReviseBody'])],
    ]
    spec_table = Table(spec_data, colWidths=[40, 160, 200, 140])
    spec_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f5f9')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(spec_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("CSS Selectors Reference", styles['ReviseH2']))
    story.append(make_code_box(
"""/* Universal & Type */
* { margin: 0; padding: 0; box-sizing: border-box; }
p { font-size: 1rem; color: #334155; }

/* Combinators */
div p        { /* Descendant: any <p> inside <div> */ }
div > p      { /* Child: direct child <p> of <div> */ }
h2 + p       { /* Adjacent Sibling: <p> directly following <h2> */ }
h2 ~ p       { /* General Sibling: all <p> following <h2> */ }

/* Pseudo-Classes & Pseudo-Elements */
a:hover      { color: #ea580c; }
li:nth-child(2n+1) { background-color: #f8fafc; /* Odd rows */ }
p::first-letter { font-size: 1.8rem; font-weight: bold; }
button::before  { content: '🚀 '; }""", styles))

    story.append(PageBreak())

    # ------------------ SECTION 4: BOX MODEL & POSITIONING ------------------
    story.append(Paragraph("Chapter 4: CSS Box Model & Positioning", styles['ReviseH1']))
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor('#ea580c'), spaceBefore=2, spaceAfter=8))
    
    story.append(Paragraph("The CSS Box Model Architecture", styles['ReviseH2']))
    story.append(Paragraph(
        "Every element in CSS is rendered as a rectangular box consisting of four distinct layers: "
        "<b>Content</b> (text/media) -> <b>Padding</b> (inner spacing) -> <b>Border</b> -> <b>Margin</b> (outer spacing).",
        styles['ReviseBody']
    ))
    
    story.append(make_code_box(
"""/* Content-Box (Default) vs Border-Box (Best Practice) */

/* Default: width = content ONLY. Padding & border expand total size! */
.old-box {
  box-sizing: content-box;
  width: 300px;
  padding: 20px;
  border: 5px solid #000;
  /* Total rendered width = 300 + 40 + 10 = 350px! */
}

/* Modern Best Practice: width INCLUDES padding and border */
*, *::before, *::after {
  box-sizing: border-box;
}
.modern-box {
  width: 300px;
  padding: 20px;
  border: 5px solid #000;
  /* Total rendered width remains exactly 300px! */
}""", styles))

    story.append(Spacer(1, 6))
    story.append(make_callout("Always reset <code>box-sizing: border-box</code> globally. This prevents padding and borders from breaking responsive layouts.", styles, 'tip'))

    story.append(Paragraph("CSS Positioning Modes & Stacking Context", styles['ReviseH2']))
    
    pos_data = [
        [Paragraph("<b>Position</b>", styles['ReviseBody']), Paragraph("<b>Behavior & Offset</b>", styles['ReviseBody'])],
        [Paragraph("static", styles['ReviseBody']), Paragraph("Default flow. Top/Right/Bottom/Left and Z-Index have no effect.", styles['ReviseBody'])],
        [Paragraph("relative", styles['ReviseBody']), Paragraph("Offsets element relative to its normal position without removing from flow.", styles['ReviseBody'])],
        [Paragraph("absolute", styles['ReviseBody']), Paragraph("Removes element from document flow; positions relative to closest non-static ancestor.", styles['ReviseBody'])],
        [Paragraph("fixed", styles['ReviseBody']), Paragraph("Positions relative to viewport. Stays fixed during scrolling (e.g. sticky navbar).", styles['ReviseBody'])],
        [Paragraph("sticky", styles['ReviseBody']), Paragraph("Toggles between relative and fixed depending on scroll position offset.", styles['ReviseBody'])],
    ]
    pos_table = Table(pos_data, colWidths=[100, 440])
    pos_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f5f9')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(pos_table)
    story.append(Spacer(1, 8))

    story.append(make_code_box(
"""/* Parent Anchor with Absolute Badge */
.card {
  position: relative; /* Defines anchor context */
  padding: 1.5rem;
  border-radius: 12px;
}

.badge {
  position: absolute;
  top: 10px;
  right: 10px;
  z-index: 10; /* Stack on top */
  background-color: #ea580c;
  color: white;
}""", styles))

    story.append(PageBreak())

    # ------------------ SECTION 5: FLEXBOX & CSS GRID ------------------
    story.append(Paragraph("Chapter 5: Flexbox & CSS Grid Mastery", styles['ReviseH1']))
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor('#ea580c'), spaceBefore=2, spaceAfter=8))
    
    story.append(Paragraph("Flexbox (1-Dimensional Layout)", styles['ReviseH2']))
    story.append(Paragraph(
        "Flexbox excels at distributing space along a single axis (either row OR column). "
        "The primary axis is controlled by <code>justify-content</code> and the cross axis by <code>align-items</code>.",
        styles['ReviseBody']
    ))
    
    story.append(make_code_box(
"""/* Flexbox Container Properties */
.flex-container {
  display: flex;
  flex-direction: row;            /* row | row-reverse | column | column-reverse */
  justify-content: space-between; /* flex-start | center | flex-end | space-between | space-around */
  align-items: center;            /* stretch | flex-start | center | flex-end | baseline */
  flex-wrap: wrap;                /* nowrap | wrap | wrap-reverse */
  gap: 1.5rem;                    /* modern spacing between items */
}

/* Flexbox Item Properties */
.flex-item {
  flex-grow: 1;    /* Ability of item to grow if space available */
  flex-shrink: 0;  /* Prevents item from shrinking */
  flex-basis: 250px; /* Initial size before growing/shrinking */
  /* Shorthand: flex: 1 0 250px; */
  align-self: flex-end; /* Overrides container align-items */
}""", styles))

    story.append(Spacer(1, 8))
    story.append(Paragraph("CSS Grid (2-Dimensional Layout)", styles['ReviseH2']))
    story.append(Paragraph(
        "CSS Grid handles rows AND columns simultaneously. It is the gold standard for responsive page layouts.",
        styles['ReviseBody']
    ))
    
    story.append(make_code_box(
"""/* Modern Responsive Auto-Fit Grid (Zero Media Queries!) */
.responsive-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
}

/* Explicit Grid Areas */
.layout-container {
  display: grid;
  grid-template-areas:
    "header header"
    "sidebar main"
    "footer footer";
  grid-template-columns: 240px 1fr;
  grid-template-rows: auto 1fr auto;
  min-height: 100vh;
}

header  { grid-area: header; }
sidebar { grid-area: sidebar; }
main    { grid-area: main; }
footer  { grid-area: footer; }""", styles))

    story.append(Spacer(1, 6))
    story.append(make_callout("Use <code>repeat(auto-fit, minmax(280px, 1fr))</code> for dynamic card grids that adapt perfectly from phone to ultra-wide monitor without any media queries!", styles, 'tip'))

    story.append(PageBreak())

    # ------------------ SECTION 6: MODERN CSS, VARIABLES & RWD ------------------
    story.append(Paragraph("Chapter 6: Modern CSS Variables & Responsive Design", styles['ReviseH1']))
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor('#ea580c'), spaceBefore=2, spaceAfter=8))
    
    story.append(Paragraph("CSS Custom Properties (Variables)", styles['ReviseH2']))
    story.append(Paragraph("Variables enable centralized theme tokens and dynamic runtime switching (e.g. Dark Mode):", styles['ReviseBody']))
    
    story.append(make_code_box(
""":root {
  --brand-primary: #ea580c;
  --brand-secondary: #0284c7;
  --bg-surface: #ffffff;
  --text-main: #0f172a;
  --radius-card: 12px;
  --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.08);
}

[data-theme="dark"] {
  --bg-surface: #0f172a;
  --text-main: #f8fafc;
}

.button-primary {
  background-color: var(--brand-primary);
  color: #ffffff;
  border-radius: var(--radius-card);
  box-shadow: var(--shadow-sm);
  transition: transform 0.2s ease, background 0.2s ease;
}

.button-primary:hover {
  transform: translateY(-2px);
}""", styles))

    story.append(Paragraph("Modern Fluid Typography with clamp()", styles['ReviseH2']))
    story.append(Paragraph("<code>clamp(MIN, PREFERRED, MAX)</code> scales typography smoothly with viewport size:", styles['ReviseBody']))
    story.append(make_code_box(
"""/* Smooth fluid scaling between 1.5rem (phone) and 3rem (desktop) */
h1 {
  font-size: clamp(1.5rem, 4vw + 1rem, 3rem);
}""", styles))

    story.append(Paragraph("Mobile-First Media Queries", styles['ReviseH2']))
    story.append(make_code_box(
"""/* Mobile Default Styles */
.nav-links {
  display: none; /* Collapsed hamburger menu on mobile */
}

/* Tablet & Up (min-width: 768px) */
@media (min-width: 768px) {
  .nav-links {
    display: flex;
    gap: 1.5rem;
  }
}

/* Desktop & Up (min-width: 1024px) */
@media (min-width: 1024px) {
  .hero-container {
    padding: 5rem 2rem;
  }
}""", styles))

    story.append(PageBreak())

    # ------------------ SECTION 7: INTERVIEW CHEATSHEET ------------------
    story.append(Paragraph("Chapter 7: Top 15 Frontend Interview Questions", styles['ReviseH1']))
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor('#ea580c'), spaceBefore=2, spaceAfter=8))
    
    qa_list = [
        ("Q1: What is the difference between display: none and visibility: hidden?",
         "<b>display: none</b> completely removes the element from the document layout flow (takes up 0 space). "
         "<b>visibility: hidden</b> hides the element visually, but the element still preserves its original physical dimensions and spacing in the DOM flow."),
        
        ("Q2: What is the difference between px, em, and rem?",
         "<b>px</b> is an absolute fixed pixel value. <b>em</b> is relative to its immediate parent font-size (compounds in nested elements). "
         "<b>rem</b> is relative to the root (<code>&lt;html&gt;</code>) font-size (predictable and accessibility friendly)."),
        
        ("Q3: What causes a CSS Stacking Context?",
         "Stacking contexts determine layer rendering order along the Z-axis. Formed by: root <code>&lt;html&gt;</code>, elements with <code>position: relative/absolute</code> and <code>z-index != auto</code>, elements with <code>opacity &lt; 1</code>, <code>transform != none</code>, or <code>filter != none</code>."),
        
        ("Q4: What is the difference between Flexbox and CSS Grid?",
         "Flexbox is 1-dimensional (content-driven, row OR column). CSS Grid is 2-dimensional (layout-driven, rows AND columns simultaneously)."),
         
        ("Q5: What is CSS Specificity and how do you calculate it?",
         "Specificity decides which CSS rule applies when multiple rules match. Calculated as (Inline, ID, Class/Attribute/Pseudo-class, Elements). <code>!important</code> takes precedence over standard specificity.")
    ]
    
    for q, a in qa_list:
        story.append(Paragraph(f"<b>{q}</b>", styles['ReviseH3']))
        story.append(Paragraph(a, styles['ReviseBody']))
        story.append(Spacer(1, 4))
        
    story.append(Spacer(1, 15))
    story.append(make_callout("Keep revising with Revise-X! All notes are updated for current web standards and interview criteria.", styles, 'tip'))

    doc.build(story, canvasmaker=ReviseXWatermarkCanvas)
    print(f"[OK] Successfully compiled digital guide: {output_path}")

if __name__ == '__main__':
    pub_path = r'frontend/public/notebooks/html-css-notes.pdf'
    asset_path = r'frontend/src/assets/notebooks/HTML-CSS-DIGITAL-MASTER.pdf'
    generate_html_css_digital_guide(pub_path)
    
    import shutil
    shutil.copy2(pub_path, asset_path)
    print(f"[OK] Saved to both public and src/assets/notebooks")

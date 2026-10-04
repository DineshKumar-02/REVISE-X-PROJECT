import os
import sys
import pypdf
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class BrandedWatermarkCanvas(canvas.Canvas):
    def __init__(self, *args, guide_title="Revise-X Study Notes", **kwargs):
        super().__init__(*args, **kwargs)
        self.pages = []
        self.guide_title = guide_title
        
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
        
        # 1. Subtle, non-intrusive diagonal watermark (4.2% opacity)
        self.saveState()
        self.translate(width / 2.0, height / 2.0)
        self.rotate(45)
        self.setFillColor(colors.HexColor('#0f172a'))
        self.setFillAlpha(0.042)
        self.setFont('Helvetica-Bold', 54)
        self.drawCentredString(0, 0, 'REVISE-X')
        self.restoreState()
        
        if self._pageNumber > 1:
            # Top Header Bar
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
            self.drawRightString(width - 36, height - 23, self.guide_title)
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

def build_styles():
    styles = getSampleStyleSheet()
    
    styles.add(ParagraphStyle(
        name='ReviseCoverTitle',
        fontName='Helvetica-Bold',
        fontSize=26,
        leading=32,
        textColor=colors.HexColor('#0f172a'),
        alignment=1,
        spaceAfter=8
    ))
    
    styles.add(ParagraphStyle(
        name='ReviseCoverSubtitle',
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#ea580c'),
        alignment=1,
        spaceAfter=16
    ))
    
    styles.add(ParagraphStyle(
        name='ReviseCoverMeta',
        fontName='Helvetica',
        fontSize=8.5,
        leading=13,
        textColor=colors.HexColor('#64748b'),
        alignment=1
    ))
    
    styles.add(ParagraphStyle(
        name='ReviseH1',
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    ))
    
    styles.add(ParagraphStyle(
        name='ReviseH2',
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#ea580c'),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    ))
    
    styles.add(ParagraphStyle(
        name='ReviseH3',
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13.5,
        textColor=colors.HexColor('#1e293b'),
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=True
    ))
    
    styles.add(ParagraphStyle(
        name='ReviseBody',
        fontName='Helvetica',
        fontSize=8.8,
        leading=13,
        textColor=colors.HexColor('#334155'),
        spaceAfter=5
    ))
    
    styles.add(ParagraphStyle(
        name='ReviseBullet',
        fontName='Helvetica',
        fontSize=8.8,
        leading=13,
        textColor=colors.HexColor('#334155'),
        leftIndent=14,
        spaceAfter=2.5
    ))
    
    styles.add(ParagraphStyle(
        name='ReviseCode',
        fontName='Courier',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor('#f8fafc')
    ))
    
    styles.add(ParagraphStyle(
        name='CalloutText',
        fontName='Helvetica-Oblique',
        fontSize=8.2,
        leading=12,
        textColor=colors.HexColor('#1e293b')
    ))
    
    return styles

def make_code_box(code_text, styles):
    cleaned = code_text.strip().replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    p = Paragraph(f"<font face='Courier'>{cleaned.replace(chr(10), '<br/>')}</font>", styles['ReviseCode'])
    t = Table([[p]], colWidths=[540])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#0f172a')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 9),
        ('RIGHTPADDING', (0, 0), (-1, -1), 9),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#334155')),
    ]))
    return t

def make_callout(text, styles, alert_type='tip'):
    border_color = colors.HexColor('#ea580c') if alert_type == 'tip' else colors.HexColor('#0284c7')
    bg_color = colors.HexColor('#fff7ed') if alert_type == 'tip' else colors.HexColor('#f0f9ff')
    prefix = "<b>PRO TIP:</b> " if alert_type == 'tip' else "<b>NOTE:</b> "
    p = Paragraph(f"{prefix}{text}", styles['CalloutText'])
    t = Table([[p]], colWidths=[540])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), bg_color),
        ('LINELEFT', (0, 0), (0, 0), 3, border_color),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 9),
        ('RIGHTPADDING', (0, 0), (-1, -1), 9),
    ]))
    return t

def generate_css_typed_guide(output_path):
    class CSSCanvas(BrandedWatermarkCanvas):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, guide_title="CSS3 Core Study Notes • Revise-X", **kwargs)
            
    doc = SimpleDocTemplate(output_path, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=40, bottomMargin=38)
    styles = build_styles()
    story = []
    
    # Cover
    story.append(Spacer(1, 35))
    story.append(Paragraph("<font color='#ea580c'><b>REVISE-X OFFICIAL DIGITAL NOTES</b></font>", styles['ReviseCoverMeta']))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Cascading Style Sheets (CSS3)", styles['ReviseCoverTitle']))
    story.append(Paragraph("Typed & Digitally Formatted Edition (71-Page Syllabus)", styles['ReviseCoverSubtitle']))
    story.append(HRFlowable(width="60%", thickness=1.5, color=colors.HexColor('#ea580c'), spaceBefore=8, spaceAfter=18))
    
    story.append(Paragraph(
        "Comprehensive digital transformation of 71 handwritten CSS pages. "
        "Includes selectors, specificity, colors (HEX, RGB, RGBA, HSL, HSLA), Box Model, "
        "Positioning, Display, Flexbox, CSS Grid, Transitions, Transforms, Animations, and Variables.",
        styles['ReviseBody']
    ))
    story.append(Spacer(1, 15))
    
    # Overview Table
    ov_data = [
        [Paragraph("<b>Chapter</b>", styles['ReviseBody']), Paragraph("<b>Coverage Highlights</b>", styles['ReviseBody'])],
        [Paragraph("1. Introduction", styles['ReviseBody']), Paragraph("What is CSS, History (1996), Inline vs Internal vs External, Syntax", styles['ReviseBody'])],
        [Paragraph("2. Selectors & Specificity", styles['ReviseBody']), Paragraph("Element, ID, Class, Combinators (> + ~), Pseudo-classes & elements", styles['ReviseBody'])],
        [Paragraph("3. Colors & Backgrounds", styles['ReviseBody']), Paragraph("Hex, RGB, RGBA, HSL, HSLA, gradients, background-size (cover/contain)", styles['ReviseBody'])],
        [Paragraph("4. Box Model & Borders", styles['ReviseBody']), Paragraph("Margin, Border, Padding, Content, box-sizing: border-box, border-radius", styles['ReviseBody'])],
        [Paragraph("5. Typography & Units", styles['ReviseBody']), Paragraph("font-family, line-height, units (px, rem, em, %, vw, vh, clamp)", styles['ReviseBody'])],
        [Paragraph("6. Display & Positioning", styles['ReviseBody']), Paragraph("block, inline, inline-block, static, relative, absolute, fixed, sticky, z-index", styles['ReviseBody'])],
        [Paragraph("7. Flexbox & Grid", styles['ReviseBody']), Paragraph("justify-content, align-items, flex-direction, grid-template-columns, fr, gap", styles['ReviseBody'])],
        [Paragraph("8. Transitions & Keyframes", styles['ReviseBody']), Paragraph("transition-duration, transform (translate/scale/rotate), @keyframes", styles['ReviseBody'])],
    ]
    t = Table(ov_data, colWidths=[130, 410])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f5f9')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('RIGHTPADDING', (0, 0), (-1, -1), 7),
    ]))
    story.append(t)
    story.append(Spacer(1, 25))
    story.append(Paragraph("<b>Edition:</b> 2026 Typed Edition • <b>Platform:</b> Revise-X Developer Hub", styles['ReviseCoverMeta']))
    story.append(PageBreak())
    
    # Chapter 1: Introduction to CSS
    story.append(Paragraph("Chapter 1: Introduction to CSS & Syntax", styles['ReviseH1']))
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor('#ea580c'), spaceBefore=2, spaceAfter=8))
    
    story.append(Paragraph("<b>CSS (Cascading Style Sheets)</b> is used to format and style the layout of web pages.", styles['ReviseBody']))
    story.append(Paragraph("• <b>Introduced in:</b> 1996 by Håkon Wium Lie and W3C.", styles['ReviseBullet']))
    story.append(Paragraph("• <b>Pre-requisites:</b> HTML Tags, ID, Class.", styles['ReviseBullet']))
    story.append(Paragraph("• <b>Why use CSS:</b> Enables separation of presentation and document structure. A single stylesheet can style thousands of pages across a website simultaneously.", styles['ReviseBullet']))

    story.append(Paragraph("Three Implementation Methods", styles['ReviseH2']))
    story.append(make_code_box(
"""/* 1. Inline CSS: Applied directly via style attribute */
<h1 style="color: #ea580c; font-size: 24px;">Hello</h1>

/* 2. Internal CSS: Placed inside <style> tags in <head> */
<style>
  h1 { color: #ea580c; }
</style>

/* 3. External CSS (Recommended): Linked via external file */
<link rel="stylesheet" href="styles.css" />""", styles))

    story.append(Paragraph("CSS Syntax Anatomy", styles['ReviseH2']))
    story.append(make_code_box(
"""selector {
  property: value; /* Declaration */
}

/* Example */
p {
  color: #334155;
  font-size: 16px;
  line-height: 1.5;
}""", styles))

    story.append(Paragraph("Chapter 2: CSS Selectors & Combinators", styles['ReviseH1']))
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor('#ea580c'), spaceBefore=2, spaceAfter=8))
    
    story.append(Paragraph("• <b>Universal Selector:</b> <code>* { margin: 0; }</code> (targets every element).", styles['ReviseBullet']))
    story.append(Paragraph("• <b>Element Selector:</b> <code>p { ... }</code> (targets all <code>&lt;p&gt;</code> tags).", styles['ReviseBullet']))
    story.append(Paragraph("• <b>ID Selector:</b> <code>#header { ... }</code> (targets element with <code>id=\"header\"</code>; unique per page).", styles['ReviseBullet']))
    story.append(Paragraph("• <b>Class Selector:</b> <code>.btn { ... }</code> (targets elements with <code>class=\"btn\"</code>; reusable).", styles['ReviseBullet']))
    story.append(Paragraph("• <b>Grouping:</b> <code>h1, h2, h3 { font-family: sans-serif; }</code>", styles['ReviseBullet']))

    story.append(make_code_box(
"""/* Combinators */
div p   { /* Descendant: all <p> inside <div> */ }
div > p { /* Child: direct children <p> only */ }
div + p { /* Adjacent Sibling: first <p> immediately after <div> */ }
div ~ p { /* General Sibling: all <p> following <div> */ }""", styles))

    story.append(PageBreak())

    # Chapter 3: CSS Colors (RGB, RGBA, HSL, HSLA, HEX)
    story.append(Paragraph("Chapter 3: CSS Colors & Backgrounds", styles['ReviseH1']))
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor('#ea580c'), spaceBefore=2, spaceAfter=8))
    
    story.append(Paragraph("In CSS, colors can be specified using several distinct color models:", styles['ReviseBody']))
    
    color_data = [
        [Paragraph("<b>Model</b>", styles['ReviseBody']), Paragraph("<b>Syntax & Example</b>", styles['ReviseBody']), Paragraph("<b>Description</b>", styles['ReviseBody'])],
        [Paragraph("HEX", styles['ReviseBody']), Paragraph("#ea580c or #333", styles['ReviseBody']), Paragraph("Hexadecimal Red-Green-Blue (00 to FF)", styles['ReviseBody'])],
        [Paragraph("RGB", styles['ReviseBody']), Paragraph("rgb(234, 88, 12)", styles['ReviseBody']), Paragraph("Red, Green, Blue integers (0 - 255)", styles['ReviseBody'])],
        [Paragraph("RGBA", styles['ReviseBody']), Paragraph("rgba(234, 88, 12, 0.8)", styles['ReviseBody']), Paragraph("RGB with Alpha transparency (0.0 to 1.0)", styles['ReviseBody'])],
        [Paragraph("HSL", styles['ReviseBody']), Paragraph("hsl(21, 90%, 48%)", styles['ReviseBody']), Paragraph("Hue (0-360), Saturation (0-100%), Lightness (0-100%)", styles['ReviseBody'])],
        [Paragraph("HSLA", styles['ReviseBody']), Paragraph("hsla(21, 90%, 48%, 0.5)", styles['ReviseBody']), Paragraph("HSL with Alpha transparency channel (0.0 to 1.0)", styles['ReviseBody'])],
    ]
    t_col = Table(color_data, colWidths=[70, 180, 290])
    t_col.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f5f9')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('RIGHTPADDING', (0, 0), (-1, -1), 7),
    ]))
    story.append(t_col)
    story.append(Spacer(1, 8))

    story.append(Paragraph("Background Properties", styles['ReviseH2']))
    story.append(make_code_box(
""".hero-banner {
  background-color: #0f172a;
  background-image: url('pattern.svg'), linear-gradient(135deg, #ea580c, #0284c7);
  background-repeat: no-repeat;
  background-position: center;
  background-size: cover; /* or contain, auto */
  background-attachment: fixed; /* Parallax effect */
}""", styles))

    story.append(Paragraph("Chapter 4: CSS Box Model & Sizing", styles['ReviseH1']))
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor('#ea580c'), spaceBefore=2, spaceAfter=8))
    
    story.append(Paragraph("The Box Model consists of 4 layers from inside out: <b>Content</b> -> <b>Padding</b> -> <b>Border</b> -> <b>Margin</b>.", styles['ReviseBody']))
    
    story.append(make_code_box(
"""/* Global Modern Box Sizing Reset */
*, *::before, *::after {
  box-sizing: border-box; /* Width includes padding and border */
  margin: 0;
  padding: 0;
}

.box {
  width: 320px;
  padding: 16px 24px;   /* Vertical Horizontal */
  border: 2px solid #ea580c;
  border-radius: 8px;   /* Rounded corners */
  margin: 20px auto;    /* Centers horizontally */
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}""", styles))

    story.append(PageBreak())

    # Chapter 5: Flexbox & Grid
    story.append(Paragraph("Chapter 5: Modern Flexbox & CSS Grid Layouts", styles['ReviseH1']))
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor('#ea580c'), spaceBefore=2, spaceAfter=8))
    
    story.append(Paragraph("Flexbox (1D System - Row OR Column)", styles['ReviseH2']))
    story.append(make_code_box(
""".flex-row {
  display: flex;
  flex-direction: row;            /* row | column | row-reverse */
  justify-content: space-between; /* start | center | end | space-between | space-around */
  align-items: center;            /* stretch | center | start | end */
  flex-wrap: wrap;                /* nowrap | wrap */
  gap: 1.5rem;                    /* clean gap between items */
}

.flex-child {
  flex: 1 1 280px; /* grow shrink basis */
}""", styles))

    story.append(Paragraph("CSS Grid (2D System - Rows AND Columns)", styles['ReviseH2']))
    story.append(make_code_box(
""".grid-auto {
  display: grid;
  /* Auto-responsive grid columns without media queries */
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 1.5rem;
}

.grid-explicit {
  display: grid;
  grid-template-columns: 200px 1fr;
  grid-template-rows: auto 1fr auto;
  gap: 1rem;
}""", styles))

    story.append(Paragraph("Chapter 6: Transitions, Transforms & Animations", styles['ReviseH1']))
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor('#ea580c'), spaceBefore=2, spaceAfter=8))
    
    story.append(make_code_box(
"""/* Smooth Interactive Transitions */
.card-interactive {
  transition: transform 0.25s ease, box-shadow 0.25s ease;
}
.card-interactive:hover {
  transform: translateY(-4px) scale(1.02);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
}

/* Keyframe Animations */
@keyframes pulseGlow {
  0%   { transform: scale(1); opacity: 1; }
  50%  { transform: scale(1.05); opacity: 0.8; }
  100% { transform: scale(1); opacity: 1; }
}

.glow-btn {
  animation: pulseGlow 2s infinite ease-in-out;
}""", styles))

    doc.build(story, canvasmaker=CSSCanvas)
    print(f"[OK] Successfully built CSS Typed Digital Guide: {output_path}")

def build_all_in_one_bundle(output_path):
    """Combines all 5 note categories into the All-in-One Tech Notes Master Bundle."""
    print("Building All-in-One Master Bundle...")
    public_dir = r'frontend/public/notebooks'
    
    files_to_merge = [
        os.path.join(public_dir, 'html-css-notes.pdf'),
        os.path.join(public_dir, 'javascript-notes.pdf'),
        os.path.join(public_dir, 'react-notes.pdf'),
        os.path.join(public_dir, 'mongodb-notes.pdf'),
        os.path.join(public_dir, 'aws-services-notes.pdf'),
    ]
    
    merger = pypdf.PdfWriter()
    for fpath in files_to_merge:
        if os.path.exists(fpath):
            print(f"  Adding to bundle: {os.path.basename(fpath)}")
            reader = pypdf.PdfReader(fpath)
            for page in reader.pages:
                merger.add_page(page)
        else:
            print(f"  Warning: File missing for bundle: {fpath}")
            
    with open(output_path, 'wb') as out:
        merger.write(out)
        
    print(f"[OK] All-in-One Master Bundle compiled: {output_path} ({len(merger.pages)} pages)")

def main():
    pub_dir = r'frontend/public/notebooks'
    asset_dir = r'frontend/src/assets/notebooks'
    os.makedirs(pub_dir, exist_ok=True)
    os.makedirs(asset_dir, exist_ok=True)
    
    # 1. CSS Typed Digital Guide
    css_typed_path = os.path.join(pub_dir, 'css-notes-digital.pdf')
    generate_css_typed_guide(css_typed_path)
    import shutil
    shutil.copy2(css_typed_path, os.path.join(asset_dir, 'CSS-DIGITAL-NOTES.pdf'))
    
    # 2. Build All-in-One Master Bundle
    bundle_path = os.path.join(pub_dir, 'all-in-one-tech-bundle.pdf')
    build_all_in_one_bundle(bundle_path)
    shutil.copy2(bundle_path, os.path.join(asset_dir, 'ALL-IN-ONE-TECH-BUNDLE.pdf'))
    
    print("[OK] Complete digital suite compiled successfully!")

if __name__ == '__main__':
    main()

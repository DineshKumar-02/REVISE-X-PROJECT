import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class JSWatermarkCanvas(canvas.Canvas):
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
        
        # Diagonal center watermark (4.2% opacity)
        self.saveState()
        self.translate(width / 2.0, height / 2.0)
        self.rotate(45)
        self.setFillColor(colors.HexColor('#0f172a'))
        self.setFillAlpha(0.042)
        self.setFont('Helvetica-Bold', 54)
        self.drawCentredString(0, 0, 'REVISE-X')
        self.restoreState()
        
        if self._pageNumber > 1:
            # Top Header
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
            self.drawRightString(width - 36, height - 23, 'JavaScript Deep Dive (ES6+, Async & Event Loop)')
            self.restoreState()
            
            # Bottom Footer
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
        fontSize=28,
        leading=34,
        textColor=colors.HexColor('#0f172a'),
        alignment=1,
        spaceAfter=10
    ))
    styles.add(ParagraphStyle(
        name='ReviseCoverSubtitle',
        fontName='Helvetica',
        fontSize=13,
        leading=18,
        textColor=colors.HexColor('#f59e0b'),
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

def make_callout(text, styles, alert_type='tip'):
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

def generate_js_digital_guide(output_path):
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
    
    # Cover
    story.append(Spacer(1, 40))
    badge_p = Paragraph("<font color='#f59e0b'><b>REVISE-X OFFICIAL DIGITAL NOTES</b></font>", styles['ReviseCoverMeta'])
    story.append(badge_p)
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("JavaScript Deep Dive", styles['ReviseCoverTitle']))
    story.append(Paragraph("ES6+, Async, Event Loop & Modern Architecture", styles['ReviseCoverSubtitle']))
    story.append(HRFlowable(width="60%", thickness=1.5, color=colors.HexColor('#f59e0b'), spaceBefore=10, spaceAfter=20))
    
    desc = (
        "Comprehensive technical guide to advanced JavaScript engine fundamentals. "
        "Includes Call Stack mechanics, Closures, Microtask vs Callback Queue, "
        "Promise combinators, Prototypal Inheritance, and top interview questions."
    )
    story.append(Paragraph(desc, styles['ReviseBody']))
    story.append(Spacer(1, 20))
    
    summary_data = [
        [Paragraph("<b>Topic</b>", styles['ReviseBody']), Paragraph("<b>Coverage Highlights</b>", styles['ReviseBody'])],
        [Paragraph("Engine Architecture", styles['ReviseBody']), Paragraph("Call Stack, Memory Heap, V8 Garbage Collection & Hoisting", styles['ReviseBody'])],
        [Paragraph("Scope & Closures", styles['ReviseBody']), Paragraph("Lexical environment, Scope chain, Encapsulation, Memory leak avoidance", styles['ReviseBody'])],
        [Paragraph("Async & Event Loop", styles['ReviseBody']), Paragraph("Microtask Queue (Promises) vs Macrotask Queue (setTimeout, I/O)", styles['ReviseBody'])],
        [Paragraph("ES6+ Modern Syntax", styles['ReviseBody']), Paragraph("Destructuring, Rest/Spread, Nullish coalescing, Optional chaining, Immutable methods", styles['ReviseBody'])],
        [Paragraph("Prototypes & OOP", styles['ReviseBody']), Paragraph("Prototype chain, constructor functions, ES6 classes, private identifiers (#)", styles['ReviseBody'])],
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
    story.append(Paragraph("<b>Edition:</b> 2026 Verified Edition • <b>Platform:</b> Revise-X Developer Hub", styles['ReviseCoverMeta']))
    story.append(PageBreak())
    
    # Section 1: Event Loop
    story.append(Paragraph("Chapter 1: The JavaScript Event Loop & Concurrency", styles['ReviseH1']))
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor('#f59e0b'), spaceBefore=2, spaceAfter=8))
    
    story.append(Paragraph(
        "JavaScript is a single-threaded, non-blocking, asynchronous, concurrent language. "
        "It achieves non-blocking I/O via the <b>Call Stack</b>, <b>Web APIs</b>, the <b>Microtask Queue</b>, and the <b>Callback (Macrotask) Queue</b>.",
        styles['ReviseBody']
    ))
    
    story.append(Paragraph("Execution Priority Matrix", styles['ReviseH2']))
    story.append(make_code_box(
"""console.log('1: Synchronous Stack');

setTimeout(() => {
  console.log('4: MacroTask (Timer Queue)');
}, 0);

Promise.resolve().then(() => {
  console.log('3: MicroTask (Promise Resolution)');
});

queueMicrotask(() => {
  console.log('3.1: Microtask (queueMicrotask)');
});

console.log('2: Synchronous Stack');

// Output sequence:
// 1 -> 2 -> 3 -> 3.1 -> 4
// Explanation: The Call Stack empties first.
// The engine then drains ALL microtasks before picking the next macrotask!""", styles))
    
    story.append(Spacer(1, 6))
    story.append(make_callout("Microtasks (Promise.then, MutationObserver, queueMicrotask) always run BEFORE Macrotasks (setTimeout, setInterval, setImmediate, I/O).", styles, 'tip'))

    story.append(Paragraph("Chapter 2: Closures & Lexical Scope", styles['ReviseH1']))
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor('#f59e0b'), spaceBefore=2, spaceAfter=8))
    
    story.append(Paragraph(
        "A <b>Closure</b> is the combination of a function bundled together with references to its surrounding state (lexical environment). "
        "A closure gives an inner function access to an outer function's scope even after the outer function has returned.",
        styles['ReviseBody']
    ))
    
    story.append(make_code_box(
"""function createRateLimiter(maxRequests, windowMs) {
  let requestTimestamps = []; // Enclosed private variable

  return function allowRequest() {
    const now = Date.now();
    // Evict old timestamps outside the window
    requestTimestamps = requestTimestamps.filter(t => now - t < windowMs);

    if (requestTimestamps.length < maxRequests) {
      requestTimestamps.push(now);
      return { allowed: true, remaining: maxRequests - requestTimestamps.length };
    }
    return { allowed: false, remaining: 0 };
  };
}

const limiter = createRateLimiter(5, 60000); // 5 requests per minute
console.log(limiter()); // { allowed: true, remaining: 4 }""", styles))

    story.append(PageBreak())

    # Section 3: Promise Combinators
    story.append(Paragraph("Chapter 3: Promise Combinators & Async Patterns", styles['ReviseH1']))
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor('#f59e0b'), spaceBefore=2, spaceAfter=8))
    
    promise_data = [
        [Paragraph("<b>Combinator</b>", styles['ReviseBody']), Paragraph("<b>Behavior</b>", styles['ReviseBody']), Paragraph("<b>Rejection Handling</b>", styles['ReviseBody'])],
        [Paragraph("Promise.all()", styles['ReviseBody']), Paragraph("Fulfills when ALL promises fulfill.", styles['ReviseBody']), Paragraph("Rejects IMMEDIATELY on first rejection (Fail-Fast).", styles['ReviseBody'])],
        [Paragraph("Promise.allSettled()", styles['ReviseBody']), Paragraph("Waits for ALL promises to complete (fulfilled OR rejected).", styles['ReviseBody']), Paragraph("Never rejects. Returns array of {status, value/reason}.", styles['ReviseBody'])],
        [Paragraph("Promise.race()", styles['ReviseBody']), Paragraph("Settles with the FIRST settled promise.", styles['ReviseBody']), Paragraph("Rejects if the first settled promise rejects.", styles['ReviseBody'])],
        [Paragraph("Promise.any()", styles['ReviseBody']), Paragraph("Fulfills with the FIRST fulfilled promise.", styles['ReviseBody']), Paragraph("Rejects ONLY if ALL promises reject (AggregateError).", styles['ReviseBody'])],
    ]
    p_table = Table(promise_data, colWidths=[120, 240, 180])
    p_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f5f9')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(p_table)
    story.append(Spacer(1, 8))

    story.append(make_code_box(
"""// Safe parallel fetching with Promise.allSettled
async function fetchBatch(ids) {
  const requests = ids.map(id => fetch(`/api/notes/${id}`).then(r => r.json()));
  const results = await Promise.allSettled(requests);

  const successful = results
    .filter(r => r.status === 'fulfilled')
    .map(r => r.value);

  const failed = results
    .filter(r => r.status === 'rejected')
    .map(r => r.reason);

  return { successful, failed };
}""", styles))

    doc.build(story, canvasmaker=JSWatermarkCanvas)
    print(f"[OK] Successfully compiled JS guide: {output_path}")

if __name__ == '__main__':
    pub_path = r'frontend/public/notebooks/javascript-notes.pdf'
    asset_path = r'frontend/src/assets/notebooks/JAVASCRIPT-DIGITAL-MASTER.pdf'
    generate_js_digital_guide(pub_path)
    
    import shutil
    shutil.copy2(pub_path, asset_path)
    print(f"[OK] Saved to both public and src/assets/notebooks")

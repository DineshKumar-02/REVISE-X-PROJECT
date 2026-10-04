import os
import io
import sys
import pypdf
from reportlab.pdfgen import canvas
from reportlab.lib import colors

def create_page_overlay(width, height, page_num, total_pages, is_handwritten=False, title="Revise-X Study Notes"):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=(width, height))
    
    # 1. Elegant diagonal center watermark (subtle, non-disturbing 4.2% alpha)
    can.saveState()
    can.translate(width / 2.0, height / 2.0)
    can.rotate(45)
    can.setFillColor(colors.HexColor('#0f172a'))
    can.setFillAlpha(0.042)
    # Dynamic font size based on page width
    wm_font_size = max(36, int(width * 0.125))
    can.setFont('Helvetica-Bold', wm_font_size)
    can.drawCentredString(0, 0, 'REVISE-X')
    can.restoreState()
    
    if is_handwritten:
        # Handwritten scans may have text near top margin.
        # Use subtle top tags without a heavy cutting rule line.
        can.saveState()
        can.setFont('Helvetica-Bold', 7)
        can.setFillColor(colors.HexColor('#ea580c'))
        can.setFillAlpha(0.85)
        can.drawString(14, height - 12, 'REVISE-X')
        
        can.setFont('Helvetica', 6.5)
        can.setFillColor(colors.HexColor('#64748b'))
        can.setFillAlpha(0.75)
        can.drawRightString(width - 14, height - 12, title)
        can.restoreState()
        
        # Bottom footer bar with subtle separator rule
        can.saveState()
        can.setStrokeColor(colors.HexColor('#cbd5e1'))
        can.setStrokeAlpha(0.5)
        can.setLineWidth(0.5)
        can.line(14, 16, width - 14, 16)
        
        can.setFont('Helvetica', 6.5)
        can.setFillColor(colors.HexColor('#64748b'))
        can.setFillAlpha(0.75)
        can.drawString(14, 8, '© Revise-X • All Rights Reserved')
        can.drawCentredString(width / 2.0, 8, 'www.revise-x.com')
        can.drawRightString(width - 14, 8, f'Page {page_num} of {total_pages}')
        can.restoreState()
    else:
        # Digital vector pages have standard margins.
        # Top running header bar
        can.saveState()
        can.setStrokeColor(colors.HexColor('#cbd5e1'))
        can.setStrokeAlpha(0.6)
        can.setLineWidth(0.5)
        can.line(24, height - 24, width - 24, height - 24)
        
        can.setFont('Helvetica-Bold', 8)
        can.setFillColor(colors.HexColor('#ea580c'))
        can.drawString(24, height - 20, 'REVISE-X')
        
        can.setFont('Helvetica', 7)
        can.setFillColor(colors.HexColor('#64748b'))
        can.drawRightString(width - 24, height - 20, title)
        can.restoreState()
        
        # Bottom running footer bar
        can.saveState()
        can.setStrokeColor(colors.HexColor('#cbd5e1'))
        can.setStrokeAlpha(0.6)
        can.setLineWidth(0.5)
        can.line(24, 24, width - 24, 24)
        
        can.setFont('Helvetica', 7)
        can.setFillColor(colors.HexColor('#64748b'))
        can.drawString(24, 14, '© Revise-X • All Rights Reserved')
        can.drawCentredString(width / 2.0, 14, 'www.revise-x.com')
        can.drawRightString(width - 24, 14, f'Page {page_num} of {total_pages}')
        can.restoreState()
        
    can.save()
    packet.seek(0)
    return pypdf.PdfReader(packet).pages[0]

def process_pdf(input_path, output_path, title, is_handwritten=False):
    print(f"Processing: {os.path.basename(input_path)} -> {os.path.basename(output_path)}...")
    reader = pypdf.PdfReader(input_path)
    writer = pypdf.PdfWriter()
    total_pages = len(reader.pages)
    
    for idx, page in enumerate(reader.pages):
        w = float(page.mediabox.width)
        h = float(page.mediabox.height)
        overlay = create_page_overlay(w, h, idx + 1, total_pages, is_handwritten=is_handwritten, title=title)
        page.merge_page(overlay)
        writer.add_page(page)
        
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'wb') as f:
        writer.write(f)
        
    print(f"  [OK] Finished {total_pages} pages for {os.path.basename(output_path)}")

def main():
    base_src = r'frontend/src/assets/notebooks'
    base_public = r'frontend/public/notebooks'
    
    tasks = [
        {
            'input': os.path.join(base_src, 'HTML NOTES.pdf'),
            'output_public': os.path.join(base_public, 'html-notes.pdf'),
            'output_asset': os.path.join(base_src, 'HTML NOTES (Watermarked).pdf'),
            'title': 'HTML5 Developer Notes • Revise-X',
            'is_handwritten': True
        },
        {
            'input': os.path.join(base_src, 'CSS NOTES.pdf'),
            'output_public': os.path.join(base_public, 'css-notes.pdf'),
            'output_asset': os.path.join(base_src, 'CSS NOTES (Watermarked).pdf'),
            'title': 'CSS3 Developer Notes • Revise-X',
            'is_handwritten': True
        },
        {
            'input': os.path.join(base_src, 'MONGODB NOTES.pdf'),
            'output_public': os.path.join(base_public, 'mongodb-notes.pdf'),
            'output_asset': os.path.join(base_src, 'MONGODB NOTES (Watermarked).pdf'),
            'title': 'MongoDB & Aggregation Guide • Revise-X',
            'is_handwritten': False
        },
        {
            'input': os.path.join(base_src, 'REACT NOTES.pdf'),
            'output_public': os.path.join(base_public, 'react-notes.pdf'),
            'output_asset': os.path.join(base_src, 'REACT NOTES (Watermarked).pdf'),
            'title': 'React 19 & Architecture Guide • Revise-X',
            'is_handwritten': False
        },
        {
            'input': os.path.join(base_src, 'AWS NOTES - EC2, S3, IAM.pdf'),
            'output_public': os.path.join(base_public, 'aws-services-notes.pdf'),
            'output_asset': os.path.join(base_src, 'AWS NOTES (Watermarked).pdf'),
            'title': 'AWS Cloud Core (IAM, S3, EC2) • Revise-X',
            'is_handwritten': False
        },
    ]
    
    for t in tasks:
        if os.path.exists(t['input']):
            process_pdf(t['input'], t['output_public'], t['title'], t['is_handwritten'])
            # Copy to asset watermarked
            import shutil
            shutil.copy2(t['output_public'], t['output_asset'])
        else:
            print(f"Warning: Not found {t['input']}")

if __name__ == '__main__':
    main()

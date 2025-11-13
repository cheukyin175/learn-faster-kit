#!/usr/bin/env python3
"""
Convert exam markdown files to professional PDF documents using reportlab.
"""

import sys
import json
import re
from pathlib import Path
from datetime import datetime


def generate_pdf_reportlab(markdown_path: Path, pdf_path: Path) -> bool:
    """
    Generate PDF using reportlab (simple, no system dependencies).

    Args:
        markdown_path: Path to markdown file
        pdf_path: Output PDF path

    Returns:
        True if successful
    """
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
        from reportlab.lib.enums import TA_CENTER, TA_LEFT

        # Read markdown
        with open(markdown_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Create PDF
        doc = SimpleDocTemplate(
            str(pdf_path),
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )

        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            alignment=TA_CENTER,
            spaceAfter=20
        )
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=10,
            spaceBefore=15
        )
        normal_style = styles['Normal']

        # Build content
        story = []
        lines = content.split('\n')

        for line in lines:
            line = line.strip()
            if not line:
                story.append(Spacer(1, 0.3*cm))
                continue

            # Title
            if line.startswith('# '):
                text = line[2:]
                story.append(Paragraph(text, title_style))

            # Section heading
            elif line.startswith('## '):
                text = line[3:]
                story.append(Paragraph(text, heading_style))

            # Horizontal rule
            elif line == '---':
                story.append(Spacer(1, 0.5*cm))

            # Regular text
            else:
                # Simple bold conversion - properly match pairs
                text = re.sub(r'\*\*([^\*]+)\*\*', r'<b>\1</b>', line)
                story.append(Paragraph(text, normal_style))

        # Generate PDF
        doc.build(story)
        return True

    except ImportError:
        return False


def markdown_to_html(markdown_text: str, title: str) -> str:
    """
    Convert markdown to HTML with exam paper styling (fallback).

    Args:
        markdown_text: Markdown content
        title: Document title

    Returns:
        HTML string with embedded CSS
    """
    import re
    html_content = markdown_text

    # Convert headers
    html_content = html_content.replace('# ', '<h1>')
    html_content = html_content.replace('\n## ', '</h1>\n<h2>')
    html_content = html_content.replace('\n### ', '</h2>\n<h3>')

    # Convert bold and italic
    html_content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html_content)
    html_content = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html_content)

    # Convert horizontal rules
    html_content = html_content.replace('\n---\n', '\n<hr>\n')

    # Convert underscores to input lines
    html_content = re.sub(r'_{3,}', '<span class="blank-line">_________________</span>', html_content)

    # Wrap in paragraphs
    lines = html_content.split('\n')
    processed_lines = []
    for line in lines:
        line = line.strip()
        if line and not line.startswith('<') and not line == '':
            processed_lines.append(f'<p>{line}</p>')
        else:
            processed_lines.append(line)

    html_content = '\n'.join(processed_lines)

    # Professional exam paper CSS
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        @page {{
            size: A4;
            margin: 2cm;
            @bottom-right {{
                content: "Page " counter(page) " of " counter(pages);
            }}
        }}

        body {{
            font-family: 'Times New Roman', Times, serif;
            font-size: 12pt;
            line-height: 1.6;
            color: #000;
            max-width: 100%;
        }}

        h1 {{
            text-align: center;
            font-size: 18pt;
            font-weight: bold;
            margin-bottom: 0.5cm;
            border-bottom: 2px solid #000;
            padding-bottom: 0.3cm;
        }}

        h2 {{
            font-size: 14pt;
            font-weight: bold;
            margin-top: 1cm;
            margin-bottom: 0.5cm;
            border-bottom: 1px solid #333;
        }}

        h3 {{
            font-size: 12pt;
            font-weight: bold;
            margin-top: 0.5cm;
            margin-bottom: 0.3cm;
        }}

        h4 {{
            font-size: 11pt;
            font-weight: bold;
            margin-top: 0.3cm;
        }}

        p {{
            margin: 0.3cm 0;
        }}

        hr {{
            border: none;
            border-top: 1px solid #666;
            margin: 0.5cm 0;
        }}

        strong {{
            font-weight: bold;
        }}

        em {{
            font-style: italic;
        }}

        .blank-line {{
            display: inline-block;
            min-width: 3cm;
            border-bottom: 1px solid #000;
        }}

        /* Answer boxes */
        p:has(.blank-line) {{
            margin: 0.2cm 0;
        }}

        /* Page breaks */
        .page-break {{
            page-break-after: always;
        }}

        /* Question spacing */
        p:contains("**") {{
            margin-top: 0.5cm;
        }}
    </style>
</head>
<body>
{html_content}
</body>
</html>
"""
    return html


def generate_pdf(markdown_path: str) -> bool:
    """
    Generate PDF from markdown exam file.

    Args:
        markdown_path: Path to markdown file

    Returns:
        True if successful, False otherwise
    """
    md_path = Path(markdown_path)

    if not md_path.exists():
        print(json.dumps({
            "status": "error",
            "error": f"File not found: {markdown_path}"
        }))
        return False

    # Determine output path
    pdf_path = md_path.with_suffix('.pdf')
    title = md_path.stem

    # Try reportlab (simple, no system deps)
    if generate_pdf_reportlab(md_path, pdf_path):
        output = {
            "status": "success",
            "pdf_path": str(pdf_path),
            "markdown_path": str(md_path),
            "title": title,
            "llm_directive": "Inform user PDF was generated successfully. Show the file path.",
            "suggested_response": f"✅ PDF generated: {pdf_path.name}"
        }
        print(json.dumps(output, indent=2))
        return True

    # reportlab not available
    output = {
        "status": "error",
        "error": "PDF generation library not available.",
        "llm_directive": "Inform user to install reportlab.",
        "suggested_response": f"❌ PDF library not installed.\n\n💡 Install with: uv pip install reportlab"
    }
    print(json.dumps(output, indent=2))
    return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 generate_exam_pdf.py <path-to-exam.md>")
        sys.exit(1)

    markdown_file = sys.argv[1]
    success = generate_pdf(markdown_file)
    sys.exit(0 if success else 1)

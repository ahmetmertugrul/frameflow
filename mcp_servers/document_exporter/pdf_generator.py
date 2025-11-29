"""
PDF Generator Module
Creates formatted PDF documents for screenplays
"""

from typing import Optional
import os
from datetime import datetime


class ScreenplayPDFGenerator:
    """
    Generates industry-standard screenplay PDFs
    """

    def __init__(self):
        """Initialize PDF generator"""
        self.page_width = 612  # 8.5 inches * 72 points
        self.page_height = 792  # 11 inches * 72 points
        self.margins = {
            "left": 90,    # 1.25 inches
            "right": 72,   # 1 inch
            "top": 72,     # 1 inch
            "bottom": 72   # 1 inch
        }

    def generate_screenplay_pdf(
        self,
        screenplay_text: str,
        output_path: str,
        metadata: Optional[dict] = None
    ) -> str:
        """
        Generate screenplay PDF

        Args:
            screenplay_text: Formatted screenplay text
            output_path: Where to save PDF
            metadata: Optional metadata (title, author, etc.)

        Returns:
            Path to generated PDF
        """
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
            from reportlab.lib.enums import TA_CENTER, TA_LEFT
            from reportlab.pdfgen import canvas

            # Create PDF document
            doc = SimpleDocTemplate(
                output_path,
                pagesize=letter,
                leftMargin=1.25*inch,
                rightMargin=1*inch,
                topMargin=1*inch,
                bottomMargin=1*inch
            )

            # Styles
            styles = getSampleStyleSheet()

            # Title page style
            title_style = ParagraphStyle(
                'Title',
                parent=styles['Heading1'],
                fontSize=24,
                alignment=TA_CENTER,
                spaceAfter=30
            )

            # Screenplay text style (Courier 12pt)
            screenplay_style = ParagraphStyle(
                'Screenplay',
                fontName='Courier',
                fontSize=12,
                leading=14,
                alignment=TA_LEFT
            )

            # Build content
            story = []

            # Title page
            if metadata:
                story.append(Spacer(1, 2*inch))
                story.append(Paragraph(metadata.get("title", "Untitled").upper(), title_style))
                story.append(Spacer(1, 0.5*inch))
                story.append(Paragraph(f"by {metadata.get('author', 'Unknown')}", styles['Normal']))
                story.append(Spacer(1, 0.3*inch))
                story.append(Paragraph(metadata.get("draft", "First Draft"), styles['Normal']))
                story.append(PageBreak())

            # Screenplay content
            # Split into paragraphs and format
            lines = screenplay_text.split('\n')
            for line in lines:
                if line.strip():
                    story.append(Paragraph(line, screenplay_style))
                else:
                    story.append(Spacer(1, 12))

            # Build PDF
            doc.build(story)

            return output_path

        except ImportError:
            # Fallback: create simple text file
            return self._generate_text_fallback(screenplay_text, output_path, metadata)

    def _generate_text_fallback(
        self,
        screenplay_text: str,
        output_path: str,
        metadata: Optional[dict]
    ) -> str:
        """Generate text file fallback if reportlab not available"""
        # Change extension to .txt
        output_path = output_path.replace('.pdf', '.txt')

        with open(output_path, 'w') as f:
            if metadata:
                f.write(f"{metadata.get('title', 'Untitled').upper()}\n")
                f.write(f"by {metadata.get('author', 'Unknown')}\n")
                f.write(f"{metadata.get('draft', 'First Draft')}\n")
                f.write("\n" + "="*60 + "\n\n")

            f.write(screenplay_text)

        return output_path

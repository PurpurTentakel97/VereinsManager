import random
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, PageBreak, Frame, FrameBreak, Paragraph,
)

if __name__ == "__main__":
    style_1 = ParagraphStyle(
        name='Stylo',
        fontName='Helvetica',
        fontSize=10,
        leading=12)
    doc = BaseDocTemplate(
        'test_spacer.pdf',
        showBoundary=1,
        pagesize=A4,
        topMargin=1 * cm,
        bottomMargin=1 * cm,
        leftMargin=1 * cm,
        rightMargin=1 * cm)

    frameWidth = 4 * cm
    frameHeight = doc.height - 0.05 * cm

    frame_list = [
        Frame(
            x1=doc.leftMargin,
            y1=doc.bottomMargin,
            width=doc.width - frameWidth,
            height=frameHeight),
        Frame(
            x1=doc.leftMargin + doc.width - frameWidth,
            y1=doc.bottomMargin,
            width=frameWidth,
            height=frameHeight),
    ]
    doc.addPageTemplates([PageTemplate(id='frames', frames=frame_list), ])

    story = []
    for i, x in enumerate(['A', 'B', 'C']):
        # add text in first frame
        for _ in range(3):
            story.append(
                Paragraph(
                    x * random.randint(50, 100),
                    style_1))

        # jump to next frame
        story.append(FrameBreak())

        # add text in second frame
        story.append(
            Paragraph(
                'This should be on the top of the 2nd Frame! ' + x,
                style_1))

        story.append(PageBreak())

    doc.build(story)

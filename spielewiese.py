from config import config_sheet as c
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, FrameBreak, Paragraph, Spacer, Image,
)

if __name__ == "__main__":
    c.create_config()
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
    footerHeight = 1 * cm

    frame_list = [
        Frame(
            x1=doc.leftMargin,
            y1=doc.bottomMargin + footerHeight,
            width=doc.width - frameWidth,
            height=frameHeight - footerHeight),
        Frame(
            x1=doc.leftMargin + doc.width - frameWidth,
            y1=doc.bottomMargin + footerHeight,
            width=frameWidth,
            height=frameHeight - footerHeight),
        Frame(
            x1=doc.leftMargin,
            y1=doc.bottomMargin,
            width=doc.width,
            height=footerHeight),
    ]
    doc.addPageTemplates([PageTemplate(id='frames', frames=frame_list)])

    story = [Paragraph("Name // Straße // plz / stadt // nummber // mail", style=style_1),
             Paragraph("Name Empfänger<br/>Straße Enpfänger<br/>plz / stadt Empfänger", style=style_1),
             Spacer(0, 1 * cm), Paragraph("Datum", style=style_1), Spacer(0, 0.5 * cm),
             Paragraph("Eintrittsbestätigung", style=style_1), Spacer(0, 1 * cm),
             Paragraph("<<Name>> wurde am <<Datum>> in den <<Vereinsname>> aufgenommen.", style_1), Spacer(0, 1 * cm),
             Paragraph("Informationen:", style_1), Spacer(0, 0.1 * cm),
             Paragraph("Mitgliedsart:<<mitgliedsart>><br/>Jahresbeitrag:<<beitrag>>", style_1), Spacer(0, 1.5 * cm),
             Paragraph("________________________", style_1), Paragraph("Vorstandsmitglied", style_1),
             # next frame
             FrameBreak(),
             Image(c.config.get_icon_path(), frameWidth, frameWidth), Spacer(0, 0.5 * cm), Paragraph(
            "Vorstand name<br/>Vorstand Adresse<br/>Vorstand plz / Stadt<br/>Vorstand mail<br/>Vorstand nummer<br/>homepage"),
             Spacer(0, 0.5 * cm),
             Paragraph("Sondertext für den Briefkopf<br/>* Deutscher Meitser 1987 *<br/>* Bester Coder *"),
             # next frame
             FrameBreak(),
             Paragraph("Bankverbindung", style_1)]


    doc.build(story)

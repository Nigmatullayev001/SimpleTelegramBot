from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER
import os


def generate_file(fmt, uid, items, settings=None):
    """
    settings: {
        "text_size": int,
        "image_size": str ("small","medium","large"),
        "per_page": int
    }
    """
    filename = f"results/{uid}_file.{fmt}"

    text_size = settings.get("text_size", 18) if settings else 18
    img_size = settings.get("image_size", "medium") if settings else "medium"
    per_page = settings.get("per_page", 1) if settings else 1

    # rasm o‘lchamlari
    if img_size == "small":
        img_w, img_h = 250, 180
    elif img_size == "large":
        img_w, img_h = 500, 380
    else:
        img_w, img_h = 380, 280

    if fmt == "pdf":
        doc = SimpleDocTemplate(filename, pagesize=A4)
        story = []

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name="Center", alignment=TA_CENTER, fontSize=text_size, leading=text_size+4))
        styles.add(ParagraphStyle(name="Caption", alignment=TA_CENTER, fontSize=int(text_size*0.8), leading=text_size, textColor="gray"))

        counter = 0
        for item in items:
            if item[0] == "text":
                story.append(Paragraph(item[1], styles["Center"]))
                story.append(Spacer(1, 15))
            elif item[0] == "image":
                if os.path.exists(item[1]):
                    img = Image(item[1], width=img_w, height=img_h)
                    img.hAlign = "CENTER"
                    story.append(img)
                    if item[2]:
                        story.append(Paragraph(item[2], styles["Caption"]))
                    story.append(Spacer(1, 20))

            counter += 1
            if counter >= per_page:
                story.append(PageBreak())
                counter = 0

        doc.build(story)
        return filename

    elif fmt == "docx":
        from docx import Document
        from docx.shared import Pt, Inches

        doc = Document()
        counter = 0

        for item in items:
            if item[0] == "text":
                para = doc.add_paragraph(item[1])
                run = para.runs[0]
                run.font.size = Pt(text_size)
            elif item[0] == "image":
                if os.path.exists(item[1]):
                    doc.add_picture(item[1], width=Inches(img_w/100))
                    if item[2]:
                        para = doc.add_paragraph(item[2])
                        run = para.runs[0]
                        run.font.size = Pt(int(text_size*0.8))

            counter += 1
            if counter >= per_page:
                doc.add_page_break()
                counter = 0

        doc.save(filename)
        return filename

    elif fmt == "pptx":
        from pptx import Presentation
        from pptx.util import Inches, Pt

        prs = Presentation()
        blank_slide_layout = prs.slide_layouts[6]

        for item in items:
            slide = prs.slides.add_slide(blank_slide_layout)
            if item[0] == "text":
                txBox = slide.shapes.add_textbox(Inches(1), Inches(2), Inches(8), Inches(3))
                tf = txBox.text_frame
                p = tf.add_paragraph()
                p.text = item[1]
                p.font.size = Pt(text_size + 10)
                p.alignment = 1
            elif item[0] == "image":
                if os.path.exists(item[1]):
                    slide.shapes.add_picture(item[1], Inches(2), Inches(1.5), Inches(img_w/100), Inches(img_h/100))
                    if item[2]:
                        txBox = slide.shapes.add_textbox(Inches(1), Inches(5.5), Inches(8), Inches(1))
                        tf = txBox.text_frame
                        p = tf.add_paragraph()
                        p.text = item[2]
                        p.font.size = Pt(int(text_size*0.8))
                        p.alignment = 1

        prs.save(filename)
        return filename

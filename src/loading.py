from model.model_loading import Ask
import fitz
ask = Ask()

class Load:
    def __init__(self):
        pass

    def extract_text_from_pdf(self ,pdf_path, start_page=0, end_page=None):
        doc = fitz.open(pdf_path)
        text = ""
        end_page = end_page if end_page else len(doc)
        for page_num in range(start_page, end_page):
            text += doc[page_num].get_text()
        return text.strip()
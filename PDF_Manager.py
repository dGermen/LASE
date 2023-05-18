import os
import re
import fitz

class PDFProcessor:

    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def get_abstract(self, doc):
        abstract_section_started = False
        abstract_text = ""

        for i in range(len(doc)):
            block_text = doc[i]['text']
            if 'ABSTRACT' in block_text or 'abstract' in block_text or 'Abstract' in block_text:
                if i+1 < len(doc):
                    abstract_text = doc[i+1]['text']
                break
        return abstract_text.strip()

    def get_title(self, doc):
        # Assuming if the first section begins with "Published as a", the title is the second section
        if doc[0]['text'].startswith("Published as a"):
            return doc[1]['text']
        # Else, the title is the first section
        else:
            return doc[0]['text']

    def extract_text_from_pdf(self, pdf_path):
        doc = fitz.open(pdf_path)
        in_references = False
        full_text = ""
        for page in doc:
            blocks = page.get_text("blocks")
            for block in blocks:
                block_text = block[4]
                # check if we're in the references section
                if re.search(r"REFERENCES|References|references", block_text):
                    in_references = True
                # if we're not in the references, add the block text to full_text
                if not in_references:
                    # remove non-alphabetic characters and digits
                    block_text = re.sub(r'[^a-zA-Z\s]', '', block_text)
                    # replace sequence of two or more spaces with a single space
                    block_text = re.sub(r'\s{2,}', ' ', block_text)
                    full_text += block_text + ' '
        return full_text.strip()  # .strip() removes leading/trailing spaces

    def process_pdf(self):
        doc = fitz.open(self.pdf_path)
        blocks = [{"bbox": block[:4], "text": block[4]} for page in doc for block in page.get_text("blocks")]
        paper = {}
        paper["id"] = 0
        paper["title"] = self.get_title(blocks)
        paper["abstract"] = self.get_abstract(blocks)
        paper["dir"] = self.pdf_path
        paper["embeddings"] = "" # fill this later
        text = self.extract_text_from_pdf(self.pdf_path)
        return paper, text

# Usage:
# pdf_processor = PDFProcessor('papers2/181_dual_lottery_ticket_hypothesis.pdf')
# metadata, text = pdf_processor.process_pdf()

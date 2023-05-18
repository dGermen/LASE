import os
from whoosh import index
from whoosh.fields import Schema, TEXT
from whoosh.qparser import QueryParser
from whoosh.index import create_in, open_dir
from PyPDF2 import PdfReader


class WhooshIRProcessor:
    def __init__(self, pdf_dir):
        self.index_dir = "index"
        self.pdf_dir = pdf_dir
        self.schema = Schema(title=TEXT(stored=True), content=TEXT(stored=True))

    def create_index(self):
        if not os.path.exists(self.index_dir):
            os.mkdir(self.index_dir)

        ix = create_in(self.index_dir, self.schema)
        writer = ix.writer()

        for root, _, files in os.walk(self.pdf_dir):
            for file in files:
                if file.endswith(".pdf"):
                    pdf_path = os.path.join(root, file)
                    self.index_pdf(writer, pdf_path)

        writer.commit()

    def index_pdf(self, writer, pdf_path):
        with open(pdf_path, 'rb') as file:
            pdf = PdfReader(file)
            text = ''
            for page in pdf.pages:
                text += page.extract_text()

            writer.add_document(title=os.path.basename(pdf_path), content=text)

    def search(self, query_str):
        ix = open_dir(self.index_dir)
        searcher = ix.searcher()
        query = QueryParser("content", ix.schema).parse(query_str)
        results = searcher.search(query)

        for hit in results:
            print(f"Title: {hit['title']}")
            print(f"Score: {hit.score:.4f}")
            # print(f"Content: {hit['content']}\n")

        searcher.close()


"""
# Example usage
if __name__ == '__main__':
    index_directory = 'index'
    pdf_directory = 'papers2'

    processor = WhooshIRProcessor(index_directory, pdf_directory)
    processor.create_index()

    query = input("Enter your search query: ")
    processor.search(query)
"""


import os
from whoosh import index
from whoosh.fields import Schema, TEXT, NUMERIC
from whoosh.qparser import QueryParser
from whoosh.index import create_in, open_dir
from PyPDF2 import PdfReader
import numpy as np


class WhooshIRProcessor:
    def __init__(self, pdf_dir):
        self.index_dir = "index"
        self.pdf_dir = pdf_dir
        self.schema = Schema(id=NUMERIC(stored=True, unique=True), title=TEXT(stored=True), content=TEXT(stored=True))

    
    def add_index(self, pdf_path, doc_id):
        if not os.path.exists(self.index_dir):
            os.mkdir(self.index_dir)

        ix = open_dir(self.index_dir)
        writer = ix.writer()
        self.index_pdf(writer, pdf_path, doc_id)
        writer.commit()

    def index_pdf(self, writer, pdf_path, doc_id):
        with open(pdf_path, 'rb') as file:
            pdf = PdfReader(file)
            text = ''
            for page in pdf.pages:
                text += page.extract_text()

            writer.add_document(id=str(doc_id), title=os.path.basename(pdf_path), content=text)

    def search(self, query_str, k=10):
        ix = open_dir(self.index_dir)
        searcher = ix.searcher()
        query = QueryParser("content", ix.schema).parse(query_str)
        results = searcher.search(query, limit=k)
        top_k_ids = np.array([hit['id'] for hit in results])
        searcher.close()
        return top_k_ids.tolist()        


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


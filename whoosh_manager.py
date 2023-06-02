import os
import whoosh
from whoosh import index
from whoosh.fields import Schema, TEXT, NUMERIC
from whoosh.qparser import QueryParser
from whoosh.index import create_in, open_dir
from PyPDF2 import PdfReader
import numpy as np


class WhooshIRProcessor:

    def __init__(self, index_dir) -> None:
        self.index_dir = index_dir + "/whoosh_index"
        self.schema = Schema(id=NUMERIC(stored=True, unique=True), title=TEXT(stored=True), content=TEXT(stored=True))

        # if index_dir dos not exist, create it
        if not os.path.exists(self.index_dir):
            os.mkdir(self.index_dir)

        try:
            self.index = index.open_dir(self.index_dir)

        except Exception as e:
            print(f"Index not found at {self.index_dir}. Creating new index.")
            self.index = index.create_in(self.index_dir, self.schema)
            print(f"New index created at {self.index_dir}.")


    def add_index(self, pdf_path, doc_id):
        writer = self.index.writer()
        self.index_pdf(writer, pdf_path, doc_id)
        writer.commit() 



    def index_pdf(self, writer, pdf_path, doc_id):
        with open(pdf_path, 'rb') as file:
            pdf = PdfReader(file)
            text = ''
            for page in pdf.pages:
                text += page.extract_text()

            writer.add_document(id=doc_id, title=os.path.basename(pdf_path), content=text)   
    

    def query(self, query_str, k=10):
        ix = open_dir(self.index_dir)
        searcher = ix.searcher()
        query = QueryParser("content", ix.schema).parse(query_str)
        results = searcher.search(query, limit=k)
        top_k_ids = np.array([hit['id'] for hit in results])
        searcher.close()
        return top_k_ids.tolist() 
       
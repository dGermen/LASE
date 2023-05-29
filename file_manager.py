import os
import fitz
import re
import time
import pickle
import numpy as np

'''
vis_data = { <id_1> : { title : <title_1>,
                        abstract: <abstract_1>,
                        path = <path_2>
                        },
            <id_2> : { title : <title_2>,
                        abstract: <abstract_2>,
                        path = <path_2>
                        },

            }
'''

"""
Possible problems:
1. What if the file is deleted from the folder? Saving the vis_data and embed_data might be a problem
2. What if the file is renamed? Saving the vis_data and embed_data might be a problem

"""

class FileManager:

    def __init__(self, paper_dir, index_dir, whoosh_manager, embed_manager, vis_data, embed_data):
        self.paper_dir = paper_dir
        self.index_dir = index_dir
        self.whoosh_manager = whoosh_manager
        self.embed_manager = embed_manager
        self.vis_data = vis_data
        self.embed_data = embed_data

        self.all_papers = set() # keeps all papers added to index 
        self.vis_data_fname = "vis_data.pkl"
        self.embed_data_fname = "embed.npy"

        self.load() # reads the pickled vis_data and embed_data upon initialization. This might be a problem if file deleted or renamed!!
        self.scan() # scans the folder for new files and adds them to the index if new exists


    # will be called upon initialization and when a new file is added to the folder (detected by button press)
    def scan(self):
        new_embeddings = []        
        # Scan the whole folder for new files
        for paper in os.listdir(self.paper_dir):
            if paper in self.all_papers: continue  # PDF already processed                
            try:    
                # Get the path to PDF
                path = os.path.join(self.paper_dir, paper) 
                # Generate id 
                id = self.generate_id()
                # Get the dict for vis_data and text for embedding using process_pdf
                paper_dict, text = self.process_pdf(path)
                # Get the embedding    
                embedding = self.embed_manager.embed(text)
                # Add to index
                # Schema(id=NUMERIC(stored=True, unique=True), title=TEXT(stored=True), content=TEXT(stored=True))
                self.whoosh_manager.add_index(path, id)
                # Update the vis_data
                self.vis_data[id] = paper_dict
                # Update the new_embeddings list (which will become self.embed_data)
                self.embed_data = np.append(self.embed_data, new_embeddings, axis=0)
                # Add the paper to self.all_papers
                self.all_papers.add(paper)
            except Exception as e:
                print(f"Failed to process {paper}: {str(e)}") 

      
        # Save the vis_data and embed_data
        self.save()       
        return self.vis_data, self.embed_data 
    
    # loads the pickled vis_data and embed_data
    def load(self):
        # check if the path: self.index_dir + self.vis_data_fname exists
        vis_data_path = os.path.join(self.index_dir, self.vis_data_fname)  
        if os.path.exists(vis_data_path):
            with open(vis_data_path, 'rb') as f:
                self.vis_data = pickle.load(f)  
        else: 
            self.vis_data = None      

        # check if the path: self.index_dir + self.embed_data_fname exists
        embed_data_path = os.path.join(self.index_dir, self.embed_data_fname)
        if os.path.exists(embed_data_path):
            with open(embed_data_path, 'rb') as f:
                self.embed_data = np.load(f)
        else:
            self.embed_data = np.empty((0, 2), dtype=object)

        # add all papers names to self.all_papers
        for paper in os.listdir(self.paper_dir):
            self.all_papers.add(paper)

        
    def save(self):
        # save the vis_data
        vis_data_path = os.path.join(self.index_dir, self.vis_data_fname)
        with open(vis_data_path, 'wb') as f:
            pickle.dump(self.vis_data, f)

        # save the embed_data
        embed_data_path = os.path.join(self.index_dir, self.embed_data_fname)
        with open(embed_data_path, 'rb') as f:
            self.embed_data = np.load(f)        



    
    def generate_id(self):
        timestamp = time.time()
        id = str(int(timestamp))
        return id
    
    def get_abstract(self, doc):
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
        
    # extracts texts from pdf for embedding: removing parts after references and non-aphanum. chars
    # may be add some more preprocessing here!
    def extract_text_from_pdf_for_embedding(self, pdf_path):
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
    
    def process_pdf(self, path):
        doc = fitz.open(path)
        blocks = [{"bbox": block[:4], "text": block[4]} for page in doc for block in page.get_text("blocks")]
        paper = {}
        paper["title"] = self.get_title(blocks)
        paper["abstract"] = self.get_abstract(blocks)
        paper["dir"] = path
        text = self.extract_text_from_pdf_for_embedding(path)
        return paper, text    

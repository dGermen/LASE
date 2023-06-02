import whoosh_manager
import file_manager
import embed_manager
import vis_manager
import query_manager
import os
import numpy as np
import pickle


class Manager:

    def __init__(self, index_dir = "index", paper_dir = "papers/") -> None:
        self.index_dir = index_dir
        self.paper_dir = paper_dir

        self.vis_data_fname = "vis_data.pkl"
        self.embed_data_fname = "embed.npy"

        # Load "data"s
        self.all_papers = set() # keeps all papers added to index
        self.load_data()

        # Initilizing used modules
        self.whoosh_manager = whoosh_manager.WhooshIRProcessor(
            index_dir = self.index_dir)

        self.embed_manager = embed_manager.EmbedManager(
            embed_data = self.embed_data)
        
        self.file_manager = file_manager.FileManager(
            paper_dir = self.paper_dir,
            index_dir = self.index_dir,
            whoosh_manager = self.whoosh_manager, 
            embed_manager = self.embed_manager,
            vis_data = self.vis_data,
            embed_data = self.embed_data,
            all_papers = self.all_papers)
        
        self.vis_manager = vis_manager.VisManager(
            vis_data = self.vis_data)
        
        self.query_manager = query_manager.QueryManager(
            whoosh = self.whoosh_manager,
            embed_manager = self.embed_manager)

        self.scan()

    def scan(self):
        # Scan the whole folder for new files
        self.file_manager.scan()

    def load_data(self):
        # check if the path: self.index_dir + self.vis_data_fname exists
        vis_data_path = os.path.join(self.index_dir, self.vis_data_fname)  
        if os.path.exists(vis_data_path):
            with open(vis_data_path, 'rb') as f:
                self.vis_data = pickle.load(f)  
        else: 
            self.vis_data = dict()
        
        # fill in self.all_papers with the keys of titles of self.vis_data
        for key in self.vis_data.keys():
            # a = self.vis_data[key]["dir"].split("/")[1]
            self.all_papers.add(self.vis_data[key]["dir"])
        

        # check if the path: self.index_dir + self.embed_data_fname exists
        embed_data_path = os.path.join(self.index_dir, self.embed_data_fname)
        if os.path.exists(embed_data_path):
            with open(embed_data_path, 'rb') as f:
                self.embed_data = np.load(f, allow_pickle=True)
        else:
            self.embed_data = np.empty((0, 1537), dtype=object)
        

    
    def query(self,query):

        result = self.query_manager.query(query)

        return result
    








    


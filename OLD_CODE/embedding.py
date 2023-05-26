import openai
import numpy as np

class embed_manager:

    def __init__(self, openai_apikey = "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",
                model = "text-embedding-ada-002", 
                embeddings_dir = "data/embeddings.csv") -> None:
        
        openai.api_key = openai_apikey
        self.model = model

        # Initilize embeddings csv file
        self.embeddings_dir = embeddings_dir
        self.init_embeddings_file()

        # Load embeddings
        self.load_embeddings()

        pass

    def init_embeddings_file(self):
        # Check if file exists without try
        try:
            with open(self.embeddings_dir, 'r') as f:
                pass
        except FileNotFoundError:
            # Create file
            with open(self.embeddings_dir, 'w') as f:
                f.write("id,embeddings\n")

    def load_embeddings(self):
        # Load embeddings from file
        with open(self.embeddings_dir, 'r') as f:
            self.embeddings = f.readlines()

    def embed_content(self, id, content, save = False):
        # Check if id exists
        for line in self.embeddings:
            if str(id) in line:
                return
            
        response = openai.Embedding.create(
        input=content,
        model=self.model
        )

        embeddings = response['data'][0]['embedding']

        if not save:
            return embeddings

        self.save_embedding(id, embeddings)
    
    def save_embedding(self, id, embeddings):
        
        # Convert embeddings to string
        embeddings = str(embeddings)

        # Remove first and the last character
        embeddings = embeddings[1:-1]

        # Add id and embeddings to csv file
        with open(self.embeddings_dir, 'a') as f:
            f.write(f"{id},{embeddings}\n")

        # Update embeddings with the new one
        self.load_embeddings() # WARNING: This is not efficient
        # Make this efficient



import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import heapq

class embed_manager_2:

    def __init__(self, dir,
                 openai_apikey="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",
                model = "text-embedding-ada-002",
                ) -> None:
        
        self.main_csv_dir = dir

        self.df_embeds = pd.read_csv(self.main_csv_dir)
        self.embeddings = self.df_embeds.iloc[:, 1:].values

        openai.api_key = openai_apikey
        self.model = model
        self.dir = dir

    def embed_content(self, content):
        """Embeds the given text

        Args:
            content (str): content of the pdf
        """
        response = openai.Embedding.create(
        input=content,
        model=self.model
        )

        embeddings = response['data'][0]['embedding']

        return
        
    def get_nearest(self, query_ids: list):
        """ Gets the nearest document ids to the given query ids

        Args:
            query_ids (list): query ids

        Returns:
            list: query_ids
        """
        if len(query_ids) == 1:
        # Get query embedding
            query_embedding = self.get_embedding(query_ids[0])
        else:
            query_embedding = self.process_multiple_ids(query_ids)


        # Get nearest embeddings
        nearest_ids = self.get_nearest_embedding_ids(query_embedding)

        
        return nearest_ids
    
    def process_multiple_ids(self, query_ids: list):
        """ Gets the embedding for each id and returns the mean

        Args:
            query_ids (list): query ids
        """

        # Get embeddings
        embeddings = []
        for id in query_ids:
            embeddings.append(self.get_embedding(id))

        # Get mean
        mean = np.mean(embeddings, axis=0)

        return mean
    
    def get_embedding(self, id):
        """ Gets the embedding for the given id

        Args:
            id (int): id of the document

        Returns:
            list: embedding
        """
            
        # Get embedding
        embedding = self.df_embeds[self.df_embeds['id'] == id].iloc[:, 1:].values[0]

        return embedding
        
            
    def get_nearest_embedding_ids(self, query_embedding, count = 10):
        """ Gets the nearest embedding ids to the given query embedding

        Args:
            query_embedding (list): query embedding

        Returns:
            list: nearest ids
        """

        similarities = cosine_similarity([query_embedding], self.embeddings)

        nearest_indices = heapq.nsmallest(similarities, count)[0][::-1][1:]

        nearest_ids = self.df_embeds.iloc[nearest_indices, 0].values

        return nearest_ids
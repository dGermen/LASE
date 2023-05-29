import openai
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import sklearn

class EmbedManager:

    def __init__(self, 
                embed_data,
                openai_apikey = "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",
                model = "text-embedding-ada-002",
                 ):
        pass

        self.embed_data = embed_data
        openai.api_key = openai_apikey
        self.model = model

    def embed(self, text):

        # Embed the text
        response = openai.Embedding.create(
        input=text,
        model=self.model
        )
        
        # Extract the embeddings
        embeddings = response['data'][0]['embedding']

        # List to numpy array
        embeddings = np.array(embeddings)
        
        return embeddings

    def embed_weighting(self, query_embed, ids, weights = 1):
        # Gets ids of the docs, finds their embeddings
        # Find representative embedding by weighted averaging

        if weights == 1:
            # If weights are not given, use equal weights
            weights = np.ones(len(ids))
        
        # Weight of the query
        weights.append = len(ids) / 2

        # Scale weights
        weights = weights / np.sum(weights)

        embeddings = []
        # Get embeddings
        for id in ids:
            embeddings.append(self.find_embedding(id))

        embeddings.append(query_embed)

        # Get weighted average
        weighted_average = np.average(embeddings, axis=0, weights=weights)

        return weighted_average

        

    def find_embedding(self, id):
        return self.embed_data[self.embed_data[:, 0] == id]
        pass

    def embeddings_knn(self, embedding, k):
        # Return the k nearest neighbor as IDs using embedding and self.embed_data

        # Compute cosine similarity between the random embedding and all embeddings in EMD
        similarities = cosine_similarity(self.embed_data[:, 1:], [embedding])

        # Sort the cosine similarity scores in descending order
        sorted_indices = np.argsort(similarities, axis=0)[::-1]

        # Retrieve the IDs of the top k most similar embeddings
        top_k_ids = self.embed_data[sorted_indices[:k], 0]

        return top_k_ids
    
    def query(self, w_ids, query, n):
        # Get the embedding of the query
        query_embed = self.embed(query)

        # Weigt the embeddings
        weighted_average_embed = self.embed_weighting(query_embed, w_ids)
        
        # Get the top n ids
        top_n_ids = self.embeddings_knn(weighted_average_embed, n)
        
        return top_n_ids
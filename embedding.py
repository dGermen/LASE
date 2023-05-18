import openai

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

    def get_embedding(self, id):


    def get_nearest(self, query_id):
        # Get query embedding
        query_embedding = self.get_embedding(query_id)

        # Get nearest embeddings
        nearest_embeddings = self.get_nearest_embeddings(query_embedding)

        # Get nearest ids
        nearest_ids = self.get_nearest_ids(nearest_embeddings)

        return nearest_ids

class embed_manager_2:

    def __init__(self,
                 openai_apikey="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",
                model = "text-embedding-ada-002", 
                embeddings_dir = "data/embeddings.csv") -> None:
        
        openai.api_key = openai_apikey
        self.model = model

        # Load embeddings
        self.load_embeddings()

    def load_embeddings(self):
        # Scans json files in 
        
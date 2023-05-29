

class QueryManager:

    def __init__(self,whoosh, embed_manager) -> None:
        self.whoosh = whoosh
        self.embed_manager = embed_manager
        pass

    def query(self, query, k = 10, n = 10):
        # Get the results from whoosh
        w_ids = self.whoosh.query(query, k = k)

        # Get the results from embedding
        e_ids = self.embed_manager.query(query, n = n)
        
        return w_ids, e_ids
        
        # Return 10 results from whoosh 10 from embedding IDS
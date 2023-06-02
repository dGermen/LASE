

class QueryManager:

    def __init__(self,whoosh, embed_manager) -> None:
        self.whooshIR = whoosh
        self.embed_manager = embed_manager
        pass

    def query(self, query, k = 10, n = 10):
        # Get the results from whoosh
        w_results = self.whooshIR.query(query, k = k)

        if len(w_ids) == 0:
            return [[], []]

        # Get the results from embedding
        e_results = self.embed_manager.query(w_ids, query, n = n)
        
        # Combine the results
        

        return [w_ids, e_ids]
        
        # Return 10 results from whoosh 10 from embedding IDS
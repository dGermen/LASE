

class QueryManager:

    def __init__(self,whoosh, embed_manager) -> None:
        self.whooshIR = whoosh
        self.embed_manager = embed_manager
        pass

    def query(self, query, k = 10, n = 10):
        # Get the results from whoosh
        w_results = self.whooshIR.query(query, k = k)
        w_ids = [r["id"] for r in w_results]

        if len(w_results) == 0:
            return {"seperated": [], "combined": []}

        # Get the results from embedding
        e_results = self.embed_manager.query(w_ids, query, n = n)
        
        # Combine the results
        c_results = self.combine_results(w_results, e_results)

        return {"seperated": [w_results, e_results], "combined": [c_results]}
        
        # Return 10 results from whoosh 10 from embedding IDS
    
    def combine_results(self, w_results, e_results):
        c = []
        for e, w in zip(e_results, w_results):
            if e["id"] == w["id"]:
                c.append({"id": e["id"], "score": e["s_e_score"] + w["s_w_score"]})
            else:
                e["score"] = e["s_e_score"]
                w["score"] = w["s_w_score"]
                c.append(e)
                c.append(w)

        # Sort c according to score
        c = sorted(c, key=lambda k: k['score'], reverse=True)

        return c

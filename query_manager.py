import itertools

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
            return {"separate": [], "combined": []}

        # Get the results from embedding
        e_results = self.embed_manager.query(w_ids, query, n = n)
        
        # Combine the results
        c_results = self.combine_results(w_results, e_results)

        return {"separate": [w_results, e_results], "combined": c_results}
        
        # Return 10 results from whoosh 10 from embedding IDS
    
    def combine_results(self, w_results, e_results):
        w_dict = {item['id']: item for item in w_results}
        e_dict = {item['id']: item for item in e_results}

        combined = []
        all_ids = set(w_dict.keys()).union(e_dict.keys())

        for id_ in all_ids:
            w_item = w_dict.get(id_)
            e_item = e_dict.get(id_)
            if w_item is not None and e_item is not None:
                combined.append({"id": id_, "score": e_item["s_e_score"] + w_item["s_w_score"], "src": "both"})
            elif e_item is not None:
                e_item["score"] = e_item["s_e_score"]
                e_item["src"] = "embed"
                combined.append(e_item)
            elif w_item is not None:
                w_item["score"] = w_item["s_w_score"]
                w_item["src"] = "whoosh"
                combined.append(w_item)

        # Sort combined according to score
        combined = sorted(combined, key=lambda k: k['score'], reverse=True)

        return combined

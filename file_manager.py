class FileManager:

    def __init__(self, folder_path, pdf_processor, embedder, whoosh, config):
        self.PDF_manager = pdf_processor
        self.whoosh = whoosh
        self.embedder = embedder
        self.folder_path = folder_path
        self.config = config
    

    def file_processor(self, file_name):
        # 1. whoosh processing
        config += 1
        self.whoosh.add_index(file_name, config)

        # 2. pdf extractor 
        # metadata = {title: ,
        #             abstract: ,
        #             dir: }

        metadata, text = self.PDF_manager.process_pdf(file_name)   

        # 3. get embeddings
        text_embed = self.embedder(text)

        # 4. add id and embeddings fields to dict
        metadata["embedding"] = text_embed
        
        metadata["id"] = config

        # 5. return metadata & embeds
        return metadata, text_embed
    



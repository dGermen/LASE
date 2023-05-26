import time

class FileManager:

    def __init__(self, folder_path, pdf_processor, embedder, whoosh):
        self.PDF_manager = pdf_processor
        self.whoosh = whoosh
        self.embedder = embedder
        self.folder_path = folder_path
    

    def process_file(self, file_name):

        file_path = self.folder_path + "/" + file_name

        # Get the current time in seconds
        current_time_seconds = int(time.time())

        # Get the current time with higher precision (microseconds)
        current_time_microseconds = int(time.perf_counter() * 1_000_000)

        # Combine the seconds and microseconds to form the ID
        id = str(current_time_seconds) + str(current_time_microseconds)

        # 1. whoosh processing
        self.whoosh.add_index(file_path, id)

        # 2. pdf extractor 
        # metadata = {title: ,
        #             abstract: ,
        #             dir: }

        metadata, text = self.PDF_manager.process_file(file_path)   

        # 3. get embeddings
        text_embed = self.embedder(text)

        # 4. add id and embeddings fields to dict
        metadata["embedding"] = text_embed
        
        # Add the ID to the metadata
        metadata["id"] = id

        # 5. return metadata & embeds
        return metadata
    



import embedding
import os
import numpy as np
import PDF_Manager
import file_manager
import whoosh_manager

class manager:
    def __init__(self, main_csv_dir = "data/main.csv", papers_dir = "papers/") -> None:
        # TODO Probably you want to initilize visualizer here


        # Initilize whoosh
        self.whoosh_manager = whoosh_manager.WhooshIRProcessor("index")

        self.pdf_manager = PDF_Manager.PDFProcessor()

        self.embed_manager = embedding.embed_manager()

        self.file_manager = file_manager.FileManager(papers_dir, self.pdf_manager, self.embed_manager, self.whoosh_manager)

        
        # Read config file
        self.config = self.read_config()

        

        self.main_csv_dir = main_csv_dir

        # Initilize main csv file
        self.init_main_csv()

        # Load main csv
        self.load_main_csv()

        # Rescan the file and add new files to the csv
        self.rescan()

    def init_main_csv(self):
        # Check if file exists without try
        try:
            with open(self.main_csv_dir, 'r') as f:
                pass
        except FileNotFoundError:
            # Create file
            with open(self.main_csv_dir, 'w') as f:
                f.write("id,title,abstract,dir,embeddings\n")

    def load_main_csv(self):
        # Load csv to memory
        with open(self.main_csv_dir, 'r') as f:
            self.main_csv = f.readlines()

        # Read it to np array
        self.main_csv = np.array(self.main_csv)


    def rescan(self):
        # Get the names of all files in the directory
        files = os.listdir(self.main_csv_dir)

        # Check if the files are in the csv
        for file in files:
            # Check if the file is in the csv
            if not self.is_in_csv(file):
                # Add the file to the csv
                self.process_file(file)

        self.load_main_csv()

    def is_in_csv(self, file):
        # Check if file is in the csv
        for line in self.main_csv_dir:
            if file in line:
                return True

        return False

    def process_file(self, file):
        # TODO
        self.file_manager.process_file(file)
        

    def query(self, query):
        # TODO Pass query to whoosh and get the results
        # TODO Pass the results to embedding knn
        # TODO Pass the results to visualizer
        pass

    

        


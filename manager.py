import embedding
import os
import numpy as np
import PDF_Manager

class manager:
    def __init__(self, main_csv_dir = "data/papars.csv") -> None:
        # TODO Probably you want to initilize visualizer here

        
        self.embed_manager = embedding.embed_manager()

        self.main_csv_dir = main_csv_dir
        self.PDF_manager = PDF_manager(main_csv_dir)

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
                self.add_to_csv(file)

    def is_in_csv(self, file):
        # Check if file is in the csv
        for line in self.main_csv:
            if file in line:
                return True

        return False

    def add_to_csv(self, file):
        metadata, text = self.PDF_manager.process_pdf()

        # Get embedding for the text
        embeddings = self.embed_manager.embed_content(id, text, save = True)




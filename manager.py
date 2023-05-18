import embedding
import os

class manager:
    def __init__(self, main_csv_dir = "data/papars.csv") -> None:
        # TODO Probably you want to initilize visualizer here

        
        self.embed_manager = embedding.embed_manager()

        # Rescan the file and add new files to the csv
        self.rescan()

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
        # TODO
        pass



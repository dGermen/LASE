import whoosh_manager
import file_manager
import embed_manager
import vis_manager
import query_manager

class manager:

    def __init__(self, index_dir, paper_dir) -> None:
        self.index_dir = index_dir
        self.paper_dir = paper_dir

        # Load "data"s

        # Initilizing used modules
        self.whoosh_manager = whoosh_manager.WhooshIRProcessor(
            index_dir = self.index_dir)

        self.embed_manager = embed_manager.EmbedManager(
            index_dir = self.index_dir,
            embed_data = self.embed_data)
        
        self.file_manager = file_manager.FileManager(
            paper_dir = self.paper_dir, 
            whoosh = self.whoosh_manager, 
            embed_manager = self.embed_manager,
            vis_data = self.vis_data,
            embed_data = self.embed_data)
        
        self.vis_manager = vis_manager.VisManager(
            vis_data = self.vis_data)
        
        self.query_manager = query_manager.QueryManager(
            whoosh = self.whoosh_manager,
            embed_manager = self.embed_manager)

        # Initilizing check if folders exist if not create them

        # Load them as variables to self

        # Scan the whole folder for new files
        self.scan()

    def scan(self):
        # Scan the whole folder for new files
        self.file_manager.scan()




    


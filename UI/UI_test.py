import tkinter as tk
from tkinter import ttk

class SearchEngineUI:
    def __init__(self, root):
        self.root = root
        self.root.title('Academic Search Engine')

        # Styling
        style = ttk.Style()
        style.theme_use("clam")  # Using a modern theme
        style.configure("TFrame", background="white")
        style.configure("TLabel", background="white", foreground="blue", font=("Arial", 14))
        style.configure("TEntry", foreground="black", font=("Arial", 14))
        style.configure("TButton", foreground="blue", font=("Arial", 14))
        style.configure("TScrollbar", troughcolor="blue", gripcount=0)

        # Query frame
        self.query_frame = ttk.Frame(self.root)
        self.query_frame.pack(padx=10, pady=10)
        self.query_label = ttk.Label(self.query_frame, text="Enter your query:")
        self.query_label.pack(side=tk.LEFT)
        self.query_entry = ttk.Entry(self.query_frame, width=50)
        self.query_entry.pack(side=tk.LEFT, padx=10)

        # Search button
        self.search_button = ttk.Button(self.query_frame, text="Search", command=self.search)
        self.search_button.pack(side=tk.LEFT)

        # Results frame
        self.results_frame = ttk.Frame(self.root)
        self.results_frame.pack(padx=10, pady=10)
        self.results_label = ttk.Label(self.results_frame, text="Results:")
        self.results_label.pack()
        self.results_text = tk.Text(self.results_frame, width=70, height=20)
        self.results_text.pack()

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.results_frame, command=self.results_text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_text.configure(yscrollcommand=self.scrollbar.set)

    def search(self):
        # Implement your search logic here
        query = self.query_entry.get()
        # results = search(query)
        # self.results_text.insert('end', results)
        pass

root = tk.Tk()
ui = SearchEngineUI(root)
root.mainloop()

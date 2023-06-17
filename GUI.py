from PyQt5 import QtCore, QtGui, QtWidgets
from manager import Manager
import os
import subprocess

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.manager = Manager()

        self.setWindowTitle('IR System')

        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QtWidgets.QVBoxLayout(central_widget)

        self.text = QtWidgets.QLineEdit()
        layout.addWidget(self.text)

        button = QtWidgets.QPushButton('Search')
        layout.addWidget(button)
        button.clicked.connect(self.OnSearch)

        self.switch_button = QtWidgets.QPushButton('Switch to Combined')
        layout.addWidget(self.switch_button)
        self.switch_button.clicked.connect(self.OnSwitch)

        self.stack_layout = QtWidgets.QStackedLayout()
        layout.addLayout(self.stack_layout)

        # Separate view
        self.sep_layout = QtWidgets.QWidget()
        separate_layout = QtWidgets.QHBoxLayout(self.sep_layout)
        self.stack_layout.addWidget(self.sep_layout)

        # Whoosh results
        whoosh_layout = QtWidgets.QVBoxLayout()
        separate_layout.addLayout(whoosh_layout)
        whoosh_label = QtWidgets.QLabel('Whoosh Results')
        whoosh_layout.addWidget(whoosh_label)

        self.whoosh_model = QtGui.QStandardItemModel(self)
        self.whoosh_model.setHorizontalHeaderLabels(['Title', 'Abstract', 'Path', 'Score'])
        self.whoosh_view = QtWidgets.QTableView()
        self.whoosh_view.setModel(self.whoosh_model)
        self.whoosh_view.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        whoosh_layout.addWidget(self.whoosh_view)

        # Embedding results
        embed_layout = QtWidgets.QVBoxLayout()
        separate_layout.addLayout(embed_layout)
        embed_label = QtWidgets.QLabel('Embedding Results')
        embed_layout.addWidget(embed_label)

        self.embed_model = QtGui.QStandardItemModel(self)
        self.embed_model.setHorizontalHeaderLabels(['Title', 'Abstract', 'Path', 'Score'])
        self.embed_view = QtWidgets.QTableView()
        self.embed_view.setModel(self.embed_model)
        self.embed_view.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        embed_layout.addWidget(self.embed_view)

        # Combined view
        self.comb_layout = QtWidgets.QWidget()
        combined_layout = QtWidgets.QVBoxLayout(self.comb_layout)

        # Legend for combined view
        legend_layout = QtWidgets.QHBoxLayout()
        combined_layout.addLayout(legend_layout)
        legend_layout.addWidget(QtWidgets.QLabel('Legend: '))
        legend_layout.addWidget(self.create_legend_label('Embed', QtGui.QColor(255, 230, 232)))
        legend_layout.addWidget(self.create_legend_label('Whoosh', QtGui.QColor(146, 180, 167)))
        legend_layout.addWidget(self.create_legend_label('Both', QtGui.QColor(129, 102, 122)))

        self.comb_model = QtGui.QStandardItemModel(self)
        self.comb_model.setHorizontalHeaderLabels(['Title', 'Abstract', 'Path', 'Score'])
        self.comb_view = QtWidgets.QTableView()
        self.comb_view.setModel(self.comb_model)
        self.comb_view.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        combined_layout.addWidget(self.comb_view)

        self.stack_layout.addWidget(self.comb_layout)
        self.stack_layout.setCurrentWidget(self.sep_layout)

        self.whoosh_view.doubleClicked.connect(self.OnItemActivated)
        self.embed_view.doubleClicked.connect(self.OnItemActivated)
        self.comb_view.doubleClicked.connect(self.OnItemActivated)

    def OnSearch(self):
        query = self.text.text()
        results = self.manager.query(query)

        if results["separate"]:
            self.populate_table(self.whoosh_model, results["separate"][0], "")
            self.populate_table(self.embed_model, results["separate"][1], "")
        else:
            self.clear_table(self.whoosh_model)
            self.clear_table(self.embed_model)
            print("No separate results found for the search query.")

        if results["combined"]:
            self.populate_table(self.comb_model, results["combined"], "combined")
        else:
            self.clear_table(self.comb_model)
            print("No combined results found for the search query.")

    def clear_table(self, model):
        model.removeRows(0, model.rowCount())


    def populate_table(self, model, results, table_type):
        if not isinstance(results, list):
            print("Error: results is not a list")
            return

        if not all(res['id'] in self.manager.vis_data for res in results):
            print("Error: One or more IDs in results are not in self.manager.vis_data")
            return

        model.removeRows(0, model.rowCount())
        for res in results:
            id = res['id']
            paper_dict = self.manager.vis_data[id]
            items = [QtGui.QStandardItem(paper_dict['title']), QtGui.QStandardItem(paper_dict['abstract']), QtGui.QStandardItem(paper_dict['dir']), QtGui.QStandardItem(str(res['score']))]
            if table_type == "combined":
                if res['src'] == "embed":
                    for item in items:                                                
                        item.setBackground(QtGui.QColor(255, 230, 232))
                elif res['src'] == "whoosh":
                    for item in items:
                        item.setBackground(QtGui.QColor(146, 180, 167))
                elif res['src'] == "both":
                    for item in items:
                        item.setBackground(QtGui.QColor(129, 102, 122))
            model.appendRow(items)


    def OnSwitch(self):
        if self.stack_layout.currentWidget() == self.sep_layout:
            self.stack_layout.setCurrentWidget(self.comb_layout)
            self.switch_button.setText('Switch to Separate')
        else:
            self.stack_layout.setCurrentWidget(self.sep_layout)
            self.switch_button.setText('Switch to Combined')

    def OnItemActivated(self, index):
        if index.column() == 1:  # Show the Abstract text in a scrollable MessageBox when double-clicked
            abstract = index.sibling(index.row(), 1).data()
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Abstract")
            msg.setText(abstract)
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.exec_()
        elif index.column() == 2:  # Open the paper only when 'Path' is double clicked

            path = index.sibling(index.row(), 2).data()
            paper = path.split("/")[-1]
            path1 = os.path.join(os.getcwd(), "papers")
            path = os.path.join(path1, paper)

            print("curr path: ", path)

            try:
                if os.path.isfile(path):
                    print("opening file: ", path) 
                    subprocess.Popen([path], shell=True)
            except Exception as e:
                print(f"Failed to open file: {path}, error: {e}")

    def create_legend_label(self, text, color):
        label = QtWidgets.QLabel(text)
        label.setStyleSheet(f'background-color: {color.name()};')
        return label

app = QtWidgets.QApplication([])
window = MyWindow()
window.show()
app.exec_()

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

        results_layout = QtWidgets.QHBoxLayout()
        layout.addLayout(results_layout)

        # IR results title
        ir_title = QtWidgets.QLabel('Whoosh Results')
        ir_layout = QtWidgets.QVBoxLayout()
        results_layout.addLayout(ir_layout)
        ir_layout.addWidget(ir_title)
        self.ir_model = QtGui.QStandardItemModel(self)
        self.ir_model.setHorizontalHeaderLabels(['Title', 'Abstract', 'Path'])
        self.ir_view = QtWidgets.QTableView()
        self.ir_view.setModel(self.ir_model)
        self.ir_view.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.ir_view.horizontalHeader().setHighlightSections(False)
        self.ir_view.verticalHeader().setDefaultSectionSize(3 * self.ir_view.verticalHeader().defaultSectionSize())
        self.ir_view.verticalHeader().setVisible(False)
        self.ir_view.setShowGrid(True)
        self.ir_view.setGridStyle(QtCore.Qt.SolidLine)
        self.ir_view.setStyleSheet("QTableView { gridline-color: black } ")
        ir_layout.addWidget(self.ir_view)

        # Embedding results title
        embed_title = QtWidgets.QLabel('Embedding Results')
        embed_layout = QtWidgets.QVBoxLayout()
        results_layout.addLayout(embed_layout)
        embed_layout.addWidget(embed_title)
        self.embed_model = QtGui.QStandardItemModel(self)
        self.embed_model.setHorizontalHeaderLabels(['Title', 'Abstract', 'Path'])
        self.embed_view = QtWidgets.QTableView()
        self.embed_view.setModel(self.embed_model)
        self.embed_view.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.embed_view.horizontalHeader().setHighlightSections(False)
        self.embed_view.verticalHeader().setDefaultSectionSize(3 * self.embed_view.verticalHeader().defaultSectionSize())
        self.embed_view.verticalHeader().setVisible(False)
        self.embed_view.setShowGrid(True)
        self.embed_view.setGridStyle(QtCore.Qt.SolidLine)
        self.embed_view.setStyleSheet("QTableView { gridline-color: black } ")
        embed_layout.addWidget(self.embed_view)

        self.ir_view.doubleClicked.connect(self.OnItemActivated)
        self.embed_view.doubleClicked.connect(self.OnItemActivated)

    def OnSearch(self):
        query = self.text.text()
        # results = self.manager.query(query)
        results = [[1,2], [3,4] ]
        self.populate_table(self.ir_model, results[0])
        self.populate_table(self.embed_model, results[1])


    def populate_table(self, model, ids):
        model.removeRows(0, model.rowCount())
        for id in ids:
            paper_dict = self.manager.vis_data[id]
            items = [QtGui.QStandardItem(paper_dict['title']), QtGui.QStandardItem(paper_dict['abstract']), QtGui.QStandardItem(paper_dict['dir'])]
            model.appendRow(items)

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

            if os.path.isfile(path):
                subprocess.Popen([path], shell=True)

app = QtWidgets.QApplication([])
window = MyWindow()
window.show()
app.exec_()

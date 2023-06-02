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

        self.view_mode_button = QtWidgets.QPushButton('Switch to combined view')
        layout.addWidget(self.view_mode_button)
        self.view_mode_button.clicked.connect(self.switch_view_mode)

        self.view_mode = 'separate'

        self.stack_layout = QtWidgets.QStackedLayout()
        layout.addLayout(self.stack_layout)

        self.separate_layout = QtWidgets.QWidget()
        separate_layout = QtWidgets.QVBoxLayout(self.separate_layout)
        self.stack_layout.addWidget(self.separate_layout)

        # IR results title
        ir_title = QtWidgets.QLabel('Whoosh Results')
        separate_layout.addWidget(ir_title)
        self.ir_model = QtGui.QStandardItemModel(self)
        self.ir_model.setHorizontalHeaderLabels(['Title', 'Abstract', 'Path', 'Score'])
        self.ir_view = QtWidgets.QTableView()
        self.ir_view.setModel(self.ir_model)
        self.ir_view.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.ir_view.verticalHeader().setDefaultSectionSize(3 * self.ir_view.verticalHeader().defaultSectionSize())
        self.ir_view.verticalHeader().setVisible(False)
        self.ir_view.setShowGrid(True)
        self.ir_view.setGridStyle(QtCore.Qt.SolidLine)
        self.ir_view.setStyleSheet("QTableView { gridline-color: black } ")
        separate_layout.addWidget(self.ir_view)

        # Embedding results title
        embed_title = QtWidgets.QLabel('Embedding Results')
        separate_layout.addWidget(embed_title)
        self.embed_model = QtGui.QStandardItemModel(self)
        self.embed_model.setHorizontalHeaderLabels(['Title', 'Abstract', 'Path', 'Score'])
        self.embed_view = QtWidgets.QTableView()
        self.embed_view.setModel(self.embed_model)
        self.embed_view.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.embed_view.verticalHeader().setDefaultSectionSize(3 * self.embed_view.verticalHeader().defaultSectionSize())
        self.embed_view.verticalHeader().setVisible(False)
        self.embed_view.setShowGrid(True)
        self.embed_view.setGridStyle(QtCore.Qt.SolidLine)
        self.embed_view.setStyleSheet("QTableView { gridline-color: black } ")
        separate_layout.addWidget(self.embed_view)

        self.combined_layout = QtWidgets.QWidget()
        combined_layout = QtWidgets.QVBoxLayout(self.combined_layout)
        self.stack_layout.addWidget(self.combined_layout)

        # Combined results title
        combined_title = QtWidgets.QLabel('Combined Results')
        combined_layout.addWidget(combined_title)
        self.combined_model = QtGui.QStandardItemModel(self)
        self.combined_model.setHorizontalHeaderLabels(['Title', 'Abstract', 'Path', 'Score'])
        self.combined_view = QtWidgets.QTableView()
        self.combined_view.setModel(self.combined_model)
        self.combined_view.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.combined_view.verticalHeader().setDefaultSectionSize(3 * self.combined_view.verticalHeader().defaultSectionSize())
        self.combined_view.verticalHeader().setVisible(False)
        self.combined_view.setShowGrid(True)
        self.combined_view.setGridStyle(QtCore.Qt.SolidLine)
        self.combined_view.setStyleSheet("QTableView { gridline-color: black } ")
        combined_layout.addWidget(self.combined_view)

        self.ir_view.doubleClicked.connect(self.OnItemActivated)
        self.embed_view.doubleClicked.connect(self.OnItemActivated)
        self.combined_view.doubleClicked.connect(self.OnItemActivated)

        # Initialize with the separate view
        self.stack_layout.setCurrentWidget(self.separate_layout)

    def OnSearch(self):
        query = self.text.text()
        # results = self.manager.query(query)
        results = {
            "separate": [[{"id": 1, "score": 0.1}, {"id": 2, "score": 0.2}],
                         [{"id": 1, "score": 0.1}, {"id": 2, "score": 0.2}]],
            "combined": [{"id": 3, "score": 0.5, "src": "embed"}, {"id": 4, "score": 0.2, "src": "whoosh"}]
        }

        if self.view_mode == 'separate':
            self.populate_table(self.ir_model, results['separate'][0], 'whoosh')
            self.populate_table(self.embed_model, results['separate'][1], 'embed')
        else:  # combined view
            self.populate_table(self.combined_model, results['combined'])

    def populate_table(self, model, ids, src='both'):
        model.removeRows(0, model.rowCount())
        for result in ids:
            id = result['id']
            score = result['score']
            paper_dict = self.manager.vis_data[id]
            items = [QtGui.QStandardItem(paper_dict['title']), QtGui.QStandardItem(paper_dict['abstract']), QtGui.QStandardItem(paper_dict['dir']), QtGui.QStandardItem(str(score))]
            row = model.appendRow(items)
            if src == 'whoosh':
                for item in items:
                    item.setBackground(QtGui.QColor(255, 0, 0))
            elif src == 'embed':
                for item in items:
                    item.setBackground(QtGui.QColor(0, 255, 0))
            else:  # both
                for item in items:
                    item.setBackground(QtGui.QColor(0, 0, 255))

    def switch_view_mode(self):
        if self.view_mode == 'separate':
            self.view_mode = 'combined'
            self.view_mode_button.setText('Switch to separate view')
            self.stack_layout.setCurrentWidget(self.combined_layout)
        else:
            self.view_mode = 'separate'
            self.view_mode_button.setText('Switch to combined view')
            self.stack_layout.setCurrentWidget(self.separate_layout)

        self.OnSearch()

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

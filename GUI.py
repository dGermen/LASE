import wx
from manager import Manager
import os
import subprocess

class Mywin(wx.Frame): 
    def __init__(self, parent, title): 
        super(Mywin, self).__init__(parent, title = title, size = (500,500)) 

        self.manager = Manager()

        panel = wx.Panel(self) 
        box = wx.BoxSizer(wx.VERTICAL)

        self.text = wx.TextCtrl(panel, size = (400,30)) 
        box.Add(self.text,0,flag = wx.EXPAND|wx.ALL,border = 5) 

        button = wx.Button(panel, label = "Search") 
        box.Add(button,0,flag = wx.EXPAND|wx.ALL,border = 5) 
        button.Bind(wx.EVT_BUTTON, self.OnSearch)

        # IR results title
        ir_title = wx.StaticText(panel, label="Whoosh Results")
        box.Add(ir_title, 0, flag=wx.ALIGN_CENTER_HORIZONTAL|wx.TOP, border=10)
        self.ir_list_ctrl = wx.ListCtrl(panel, style=wx.LC_REPORT)
        self.ir_list_ctrl.InsertColumn(0, 'Title')
        self.ir_list_ctrl.InsertColumn(1, 'Abstract', width=200)
        self.ir_list_ctrl.InsertColumn(2, 'Path')
        self.ir_list_ctrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated)
        self.ir_list_ctrl.SetColumnWidth(1, wx.LIST_AUTOSIZE_USEHEADER)
        box.Add(self.ir_list_ctrl, 1, flag=wx.EXPAND)

        ir_title = wx.StaticText(panel, label="Embedding Results")
        box.Add(ir_title, 0, flag=wx.ALIGN_CENTER_HORIZONTAL|wx.TOP, border=10)
        self.embed_list_ctrl = wx.ListCtrl(panel, style=wx.LC_REPORT)
        self.embed_list_ctrl.InsertColumn(0, 'Title')
        self.embed_list_ctrl.InsertColumn(1, 'Abstract', width=200)
        self.embed_list_ctrl.InsertColumn(2, 'Path')
        self.embed_list_ctrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated)
        self.ir_list_ctrl.SetColumnWidth(1, wx.LIST_AUTOSIZE_USEHEADER)
        box.Add(self.embed_list_ctrl, 1, flag=wx.EXPAND)
        
        panel.SetSizerAndFit(box)  

        self.Centre() 
        self.Show(True) 


    def OnSearch(self, event):
        query = self.text.GetValue()

        # uncomment this
        #results = self.manager.query(query)

        results = [[1,2], [3,4] ]

        self.ir_list_ctrl.DeleteAllItems()  # clear old results
        self.embed_list_ctrl.DeleteAllItems()  # clear old results


        # process the classical retrieval results from Manager.vis_data   
        for id in results[0]:  
            # get the item with id from self.manager.vis_data
            paper_dict = self.manager.vis_data[id]
            index = self.ir_list_ctrl.InsertItem(self.ir_list_ctrl.GetItemCount(), paper_dict["title"])
            self.ir_list_ctrl.SetItem(index, 1, paper_dict["abstract"])
            self.ir_list_ctrl.SetItem(index, 2, paper_dict["dir"])

        # process the embedding results from Manager.embed_data
        for id in results[1]:
            # get the item with id from self.manager.vis_data
            paper_dict = self.manager.vis_data[id]
            index = self.embed_list_ctrl.InsertItem(self.embed_list_ctrl.GetItemCount(), paper_dict["title"])
            self.embed_list_ctrl.SetItem(index, 1, paper_dict["abstract"])
            self.embed_list_ctrl.SetItem(index, 2, paper_dict["dir"])

    def OnItemActivated(self, event):
        print("clicked")
        item_index = event.GetIndex()  # gets the index of the clicked item
        path = self.ir_list_ctrl.GetItemText(item_index, 2)  # retrieve text from the third column ('Path')

        paper = path.split("/")[-1]

        path1 = os.path.join(os.getcwd(), "papers")
        path = os.path.join(path1, paper)
        print(path)
        if os.path.isfile(path):
            print("opening file")
            os.startfile(path)
             



app = wx.App() 
Mywin(None, 'IR System') 
app.MainLoop()

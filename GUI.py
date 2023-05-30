import wx
from manager import Manager

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

        self.list_ctrl = wx.ListCtrl(panel, style=wx.LC_REPORT)
        self.list_ctrl.InsertColumn(0, 'ID')
        self.list_ctrl.InsertColumn(1, 'Title')
        self.list_ctrl.InsertColumn(2, 'Content')
        box.Add(self.list_ctrl, 1, flag=wx.EXPAND)

        panel.SetSizerAndFit(box)  

        self.Centre() 
        self.Show(True) 

    def OnSearch(self, event):
        query = self.text.GetValue()
        results = self.manager.query(query)
        self.list_ctrl.DeleteAllItems()  # clear old results
        for result in results:
            index = self.list_ctrl.InsertItem(self.list_ctrl.GetItemCount(), str(result['id']))
            self.list_ctrl.SetItem(index, 1, result['title'])
            self.list_ctrl.SetItem(index, 2, result['content'])

app = wx.App() 
Mywin(None, 'IR System') 
app.MainLoop()

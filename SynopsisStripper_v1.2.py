import os
import sys
import wx

versionNumber = 'v1.2'

class ScrolledWindow(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(350, 140), style=wx.DEFAULT_FRAME_STYLE & ~ (wx.RESIZE_BORDER |
                                                wx.RESIZE_BOX | wx.MAXIMIZE_BOX))

        self.panel = wx.Panel(self, wx.ID_ANY)
        self.Show()

        outputtxt3 = '''Drop iTunes TV Container ID Folder:'''
        wx.StaticText(self, -1, outputtxt3, pos=(7, 10), style=wx.ALIGN_CENTRE)

        self.drop_target = MyFileDropTarget(self)
        self.SetDropTarget(self.drop_target)
        self.tc_files = wx.TextCtrl(self, wx.ID_ANY, pos=(10, 40), size=(325, 25))

        self.buttonClose = wx.Button(self.panel, -1, "Close", pos=(5, 75))
        self.buttonClose.Bind(wx.EVT_BUTTON, self.OnClose)

        self.buttonSubmit = wx.Button(self.panel, -1, "Submit", pos=(150, 35), size=(180, 100))
        self.buttonSubmit.Bind(wx.EVT_BUTTON, self.descriptionGrab)

    def descriptionGrab(self, event):
        """Traverses directories in drop target, for every XML that is found, the episode synopsis (description) is
        extracted and stored in the same TXT on user's desktop. TXT is then opened by its default app and program ends"""
        
        finalOutput = ""
        for root, dirs, files in os.walk(self.dropFiles):
            for file1 in files:
                if file1.endswith(".xml") and not file1.startswith("."):
                    filePath = os.path.join(root, file1)

                    with open(filePath) as f:
                        content = f.readlines()

                    for a in content:
                        if "description" in a:
                            STRP_ep_descr = a.strip()
                            STRP_ep_descr = STRP_ep_descr.replace("<description>", "")
                            STRP_ep_descr = STRP_ep_descr.replace("</description>", "")
                            finalOutput += STRP_ep_descr
                            finalOutput += '\r\n' + '\r\n'

        OutputDoc = os.path.expanduser('~/Desktop/Episode_Descriptions.txt')

        new_doc = open(OutputDoc, 'w')
        new_doc.write(str(finalOutput))
        new_doc.close()

        msg = wx.MessageDialog(self, "Your episode synopses have been written to " + OutputDoc +
                               '\n\nThe document will open now...', "Done", wx.OK | wx.ICON_INFORMATION)
        msg.ShowModal()
        msg.Close()

        print 'Status: Complete\nPlease check the document in ' + OutputDoc

        os.system("open " + OutputDoc)

        self.OnClose(ScrolledWindow)

    def setSubmissionDrop(self, dropFiles):
        self.listEmpty = False
        self.tc_files.SetValue(','.join(dropFiles))
        self.dropFiles = dropFiles[0]

    def OnClose(self, e):
        CloseApp()


class MyFileDropTarget(wx.FileDropTarget):
    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.window = window

    def OnDropFiles(self, x, y, filenames):
        self.window.setSubmissionDrop(filenames)

class CloseApp(wx.Frame):
    def __init__(e):
        sys.exit(0)


app = wx.App()
ScrolledWindow(None, -1, 'Synopsis Strippa ' + versionNumber)
app.MainLoop()

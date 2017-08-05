# coding=utf-8
from Functions import *
from SrtDecode import *
from AssDecode import *
from Core import *

import wx
import os

LogText = u"没有加载文件\n"


class MyFrame1(wx.Frame):
    def __init__(self, parent):
        self.Srt = []
        self.Ass = []
        self.AssHead = ""
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"AutoTimeMachine", pos=wx.DefaultPosition,
                          size=wx.Size(1024, 800), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)
        self.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT))
        fgSizer2 = wx.FlexGridSizer(0, 3, 0, 0)
        fgSizer2.SetFlexibleDirection(wx.BOTH)
        fgSizer2.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
        self.m_button19 = wx.Button(self, wx.ID_ANY, u"打开时间轴正确的srt文件", wx.DefaultPosition, wx.DefaultSize, 0)
        self.Bind(wx.EVT_BUTTON, self.OnSrt, self.m_button19)
        fgSizer2.Add(self.m_button19, 0, wx.ALL, 5)
        self.m_button20 = wx.Button(self, wx.ID_ANY, u"打开待调整的ass文件", wx.DefaultPosition, wx.DefaultSize, 0)
        self.Bind(wx.EVT_BUTTON, self.OnAss, self.m_button20)
        fgSizer2.Add(self.m_button20, 0, wx.ALL, 5)
        self.m_button21 = wx.Button(self, wx.ID_ANY, u"开始调整", wx.DefaultPosition, wx.DefaultSize, 0)
        self.Bind(wx.EVT_BUTTON, self.OnMerge, self.m_button21)
        fgSizer2.Add(self.m_button21, 0, wx.ALL, 5)
        self.m_staticText14 = wx.StaticText(self, wx.ID_ANY, u"输出信息", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText14.Wrap(-1)
        fgSizer2.Add(self.m_staticText14, 0, wx.ALL, 5)
        fgSizer2.AddSpacer(1)
        fgSizer2.AddSpacer(1)
        self.m_textCtrl1 = wx.TextCtrl(self, wx.ID_ANY, u"",
                                       wx.Point(3, 80), wx.Size(1000, 600),
                                       wx.HSCROLL | wx.TE_MULTILINE)
        self.SetSizer(fgSizer2)
        self.Layout()
        self.Centre(wx.BOTH)
        self.m_textCtrl1.Value = LogText

    def __del__(self):
        pass

    def OnSrt(self, event):
        file_wildcard = "Srt files(*.srt)|*.srt|All files(*.*)|*.*"
        dlg = wx.FileDialog(self,
                            u"打开srt文件",
                            os.getcwd(),
                            style=wx.FD_OPEN,
                            wildcard=file_wildcard)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
            self.filename = filename
            self.m_textCtrl1.Value = self.m_textCtrl1.Value + u"\n\n打开了作为时间轴标准的srt文件: " + filename
            self.Srt = ReadSrt(self.filename)
            self.m_textCtrl1.Value = self.m_textCtrl1.Value + u"\nsrt已解析完毕 共" + str(len(self.Srt)) + u"句字幕内容"

        dlg.Destroy()

    def OnAss(self, event):
        file_wildcard = "Ass files(*.ass)|*.ass|All files(*.*)|*.*"
        dlg = wx.FileDialog(self,
                            u"打开ass文件",
                            os.getcwd(),
                            style=wx.FD_OPEN,
                            wildcard=file_wildcard)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
            self.filename = filename
            self.m_textCtrl1.Value = self.m_textCtrl1.Value + u"\n\n打开了ass文件: " + filename
            self.AssHead = ReadAssHead(self.filename)
            self.m_textCtrl1.Value = self.m_textCtrl1.Value + u"\nass的头部内容解析完毕"
            self.Ass = ReadAss(self.filename)
            t = len(self.Ass)
            for x in self.Ass:
                if x[1] == -1:
                    t -= 1
            self.m_textCtrl1.Value = self.m_textCtrl1.Value + u"\nass正文解析完毕 共" + str(
                len(self.Ass)) + u"句字幕内容" + u"考虑预处理忽略情况共" + str(t) + u"句内容"

        dlg.Destroy()

    def OnMerge(self, event):
        Ass = Merge(self.Srt, self.Ass)
        self.m_textCtrl1.Value = self.m_textCtrl1.Value + u"\n时间轴调整完毕！"
        file_wildcard = "Ass files(*.ass)|*.ass|All files(*.*)|*.*"
        dlg = wx.FileDialog(self,
                            u"保存修改后的ass文件",
                            os.getcwd(),
                            style=wx.FD_SAVE,
                            wildcard=file_wildcard)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
            self.m_textCtrl1.Value = self.m_textCtrl1.Value + u"\n修改后的ass文件保存至" + filename
            f = codecs.open(filename, "w", "utf_8_sig")
            allText = self.AssHead
            for x in Ass:
                allText += u"Dialogue: 0,%s,%s,%s,,0,0,0,,%s\n" % (strtime(x[3]), strtime(x[4]), x[2], x[6])
            f.write(allText)
            f.close()
            print(u"I/O finished!!\n*****success!*****")

        dlg.Destroy()


if __name__ == "__main__":
    # //要比较的两个字符串
    app = wx.App(False)
    frame = MyFrame1(None)
    frame.Show(True)
    # start the applications
    app.MainLoop()

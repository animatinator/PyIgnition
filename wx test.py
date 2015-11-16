### WX TEST ###
# Copyright David Barker 2010
#
# A simple test of using wxPython to create a gui for PyIgnition


import wx, sys, os, pygame, PyIgnition

class Frame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1)
        self.panel = wx.Panel(self, -1)
        self.hwnd = self.GetChildren()[0].GetHandle()
        os.environ['SDL_VIDEODRIVER'] = 'windib'
        os.environ['SDL_WINDOWID'] = str(self.hwnd)
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(3)
        self.statusbar.SetStatusWidths([-3, -4, -2])
        self.statusbar.SetStatusText("ExeSoft Obsidian", 0)
        self.statusbar.SetStatusText("Look, it's a nifty status bar!!!", 1)
        pygame.display.init()
        self.screen = pygame.display.set_mode()
        self.Bind(wx.EVT_PAINT, self.Draw)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_CLOSE, self.Kill)
        self.val = 0
        self.SetTitle("ExeSoft Obsidian")
        self.size = self.panel.GetSizeTuple()
        self.effect = PyIgnition.ParticleEffect(self.screen, (0, 0), self.size)
        self.source = self.effect.CreateSource((self.size[0] / 2, self.size[1]), initspeed = 5.0, initdirection = 0.0, initspeedrandrange = 2.0, initdirectionrandrange = 0.2, particlesperframe = 10, particlelife = 200, drawtype = PyIgnition.DRAWTYPE_POINT, colour = (255, 255, 200))
        self.grav = self.effect.CreateDirectedGravity(0.0, 0.2, [1, 0])
        self.gravslider = wx.Slider(self, wx.ID_ANY, 0, -50, 50, style = wx.SL_HORIZONTAL | wx.SL_LABELS)
        self.gravslider.SetTickFreq(0.1, 1)
        self.Bind(wx.EVT_SCROLL, self.OnScroll)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.gravslider, 0, flag = wx.EXPAND)
        sizer.Add(self.panel, 1, flag = wx.EXPAND)
        self.SetAutoLayout(True)
        self.SetSizer(sizer)
        self.Layout()

    def Kill(self, event):
        # Make sure Pygame can't be asked to redraw /before/ quitting
        # (Otherwise wx seems to call Draw between quitting Pygame and destroying the frame)
        self.Unbind(event = wx.EVT_PAINT, handler = self.Draw)
        pygame.quit()
        self.Destroy()

    def OnSize(self, event):
        self.Layout()
        self.size = self.panel.GetSizeTuple()
        self.source.CreateKeyframe(self.source.curframe, pos = (self.size[0] / 2, self.size[1]))

    def Draw(self, event):
        self.screen.fill((0, 0, 0))
        self.effect.Update()
        self.effect.Redraw()
        pygame.display.update()
        
        self.val += 1
        self.statusbar.SetStatusText("Frame %i" % self.val, 2)
        #self.statusbar.Refresh()
        #self.gravslider.Refresh()
        self.OnPaint(event)

    def OnScroll(self, event):
        self.grav.CreateKeyframe(self.grav.curframe, strength = float(self.gravslider.GetValue()) / 100.0)

class App(wx.App):
    def OnInit(self):
        self.frame = Frame(parent = None)
        self.frame.Show()
        self.SetTopWindow(self.frame)
        
        return True

if __name__ == "__main__":
    app = App()
    app.MainLoop()

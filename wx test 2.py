### WX TEST ###
# Copyright David Barker 2010
#
# A simple test of using wxPython to create a gui for PyIgnition


import wx, sys, os, pygame, PyIgnition

class PygameDisplay(wx.Window):
    def __init__(self, parent, ID):
        wx.Window.__init__(self, parent, ID)
        self.parent = parent
        self.hwnd = self.GetHandle()
        os.environ['SDL_VIDEODRIVER'] = 'windib'
        os.environ['SDL_WINDOWID'] = str(self.hwnd)
        pygame.display.init()
        self.screen = pygame.display.set_mode()
        self.size = self.GetSizeTuple()
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TIMER, self.Update, self.timer)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.fps = 60.0
        self.timespacing = 1000.0 / self.fps
        self.timer.Start(self.timespacing, False)
        
        self.effect = PyIgnition.ParticleEffect(self.screen, (0, 0), self.size)
        self.source = self.effect.CreateSource((self.size[0] / 2, self.size[1]), initspeed = 5.0, initdirection = 0.0, initspeedrandrange = 2.0, initdirectionrandrange = 0.2, particlesperframe = 10, particlelife = 200, drawtype = PyIgnition.DRAWTYPE_CIRCLE, colour = (255, 20, 200), radius = 0.0)
        self.source.CreateParticleKeyframe(100, radius = 20.0)
        self.source.CreateParticleKeyframe(25, colour = (255, 0, 100))
        self.source.CreateParticleKeyframe(50, colour = (100, 255, 100))
        self.source.CreateParticleKeyframe(75, colour = (0, 100, 255))
        self.source.CreateParticleKeyframe(200, colour = (0, 0, 0))
        self.grav = self.effect.CreateDirectedGravity(0.0, 0.2, [1, 0])
        self.circle = self.effect.CreateCircle((300, 300), (255, 255, 255), 0.5, 50)

    def Update(self, event):
        self.effect.Update()
        self.Redraw()
        if self.parent.val % 30 == 0:
            self.source.ConsolidateKeyframes()
            self.grav.ConsolidateKeyframes()
            self.circle.ConsolidateKeyframes()

    def Redraw(self):
        self.screen.fill((0, 0, 0))
        self.effect.Redraw()
        pygame.display.update()

    def OnPaint(self, event):
        self.Redraw()

    def OnSize(self, event):
        self.size = self.GetSizeTuple()
        newsourcepos = (self.size[0] / 2, self.size[1])
        self.source.SetPos(newsourcepos)
        self.circle.SetPos((newsourcepos[0] - 30, newsourcepos[1] - 200))

    def Kill(self, event):
        # Make sure Pygame can't be asked to redraw /before/ quitting
        # (Otherwise wx seems to call Draw between quitting Pygame and destroying the frame)
        self.Unbind(event = wx.EVT_PAINT, handler = self.OnPaint)
        self.Unbind(event = wx.EVT_TIMER, handler = self.Update, source = self.timer)

class Frame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1)
        self.display = PygameDisplay(self, -1)
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(3)
        self.statusbar.SetStatusWidths([-3, -4, -2])
        self.statusbar.SetStatusText("ExeSoft Obsidian", 0)
        self.statusbar.SetStatusText("Look, it's a nifty status bar!!!", 1)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_CLOSE, self.Kill)
        self.val = 0
        self.SetTitle("ExeSoft Obsidian")
        self.gravslider = wx.Slider(self, wx.ID_ANY, 0, -50, 50, style = wx.SL_HORIZONTAL | wx.SL_LABELS)
        self.gravslider.SetTickFreq(0.1, 1)
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_SCROLL, self.OnScroll)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_TIMER, self.Update, self.timer)
        self.timer.Start((100.0 / self.display.fps))
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.gravslider, 0, flag = wx.EXPAND)
        sizer.Add(self.display, 1, flag = wx.EXPAND)
        self.SetAutoLayout(True)
        self.SetSizer(sizer)
        self.Layout()

    def Kill(self, event):
        self.display.Kill(event)
        pygame.quit()
        self.Destroy()

    def OnSize(self, event):
        self.Layout()

    def Update(self, event):        
        self.val += 1
        self.statusbar.SetStatusText("Frame %i" % self.val, 2)

    def OnScroll(self, event):
        self.display.grav.SetStrength(float(self.gravslider.GetValue()) / 100.0)

class App(wx.App):
    def OnInit(self):
        self.frame = Frame(parent = None)
        self.frame.Show()
        self.SetTopWindow(self.frame)
        
        return True

if __name__ == "__main__":
    app = App()
    app.MainLoop()

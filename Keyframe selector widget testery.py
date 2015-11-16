import wx


class Timeline(wx.Panel):
    def __init__(self, parent, id, max_ = 300):
        wx.Panel.__init__(self, parent, id, style = wx.NO_BORDER)
        self.SetSize((0, 80))
        self.max = max_
        self.curframe = 0
        self.sidepadding = 5
        self.drawpos = (0, 0)
        self.size = (0, 0)
        self.mousetolerance = 5
        self.dragging = False
        self.pointerimg = wx.Image("framepointer.png", wx.BITMAP_TYPE_PNG)
        self.pointerbmp = wx.BitmapFromImage(self.pointerimg)
        self.keypointerimg = wx.Image("keyframepointer.png", wx.BITMAP_TYPE_PNG)
        self.keypointerbmp = wx.BitmapFromImage(self.keypointerimg)
        self.keyedframes = [0, 10, 25, 27, 49, 68, 98, 106, 132]
        
        self.font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_NORMAL, False)
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnClick)
        self.Bind(wx.EVT_LEFT_UP, self.OnRelease)
        self.Bind(wx.EVT_MOTION, self.OnMouseMotion)

    def Update(self, event):
        self.curframe += 1

    def SetMax(self, val):
        self.max = val

    def SetCurframe(self, val):
        self.curframe = val

    def OnClick(self, event):
        p = event.GetPosition()

        foundFrameTarget = False
        for frame in self.keyedframes:
            drawpos = (self.drawpos[0] + int((float(frame) / float(self.max)) * float(self.size[0])), self.drawpos[1] - (self.keypointerbmp.GetHeight()))
            if p[1] > (drawpos[1]) and \
               p[1] < (drawpos[1]+ self.keypointerimg.GetHeight()) and \
               p[0] > (drawpos[0]) and \
               p[0] < (drawpos[0] + self.keypointerbmp.GetWidth()):
                self.curframe = frame
                foundFrameTarget = True
                
        if foundFrameTarget:        
            self.SendSliderEvent()
        
        if p[1] > (self.drawpos[1] - self.mousetolerance) and \
           p[1] < (self.drawpos[1] + self.size[1] + self.pointerbmp.GetHeight()) and \
           p[0] > (self.drawpos[0] - self.mousetolerance) and \
           p[0] < (self.drawpos[0] + self.size[0] + self.mousetolerance):
            self.dragging = True
            self.CaptureMouse()
            self.OnMouseMotion(event)

    def OnRelease(self, event):
        if self.HasCapture():
            self.ReleaseMouse()
            self.dragging = False

    def OnMouseMotion(self, event):
        if self.dragging:
            posx = event.GetPosition()[0] - self.drawpos[0]
            if posx >= self.size[0]:
                self.curframe = self.max
            elif posx <= 0:
                self.curframe = 0
            else:
                self.curframe = int(float(posx) / float(self.size[0]) * self.max)
            self.SendSliderEvent()

    def SendSliderEvent(self):
        event = wx.CommandEvent(wx.EVT_SLIDER.typeId, self.GetId())
        event.SetInt(self.curframe)
        self.GetEventHandler().ProcessEvent(event)

    def OnPaint(self, event):
        self.DoPaint()

    def DoPaint(self):
        windc = wx.ClientDC(self)
        dc = wx.BufferedDC(windc)
        w, h = self.GetSize()

        # Background fill
        #dc.Clear()
        dc.SetBrush(windc.GetBackground())
        dc.DrawRectangle(0, 0, w, h)

        # Slider bar pos/size calculations
        self.drawpos = (self.sidepadding, self.keypointerbmp.GetHeight() + self.sidepadding)
        self.size = (w - (self.sidepadding * 2), 4)

        # Slider bar
        dc.SetPen(wx.Pen('#000000'))
        dc.SetBrush(wx.Brush('#FFFFFF'))
        dc.DrawRectangle(self.drawpos[0], self.drawpos[1], self.size[0], self.size[1])

        # Curframe pointer
        pointerpos = ((self.drawpos[0] + int((float(self.size[0]) * (float(self.curframe) / float(self.max))))) - (self.pointerbmp.GetWidth() / 2), self.drawpos[1])
        #dc.DrawRectangle(pointerpos[0], pointerpos[1], self.pointerbmp.GetWidth(), self.pointerbmp.GetHeight())
        dc.DrawBitmap(self.pointerbmp, pointerpos[0], pointerpos[1])
        
        # Keyed frame pointers
        for frame in self.keyedframes:
            drawpos = (self.drawpos[0] + int((float(frame) / float(self.max)) * float(self.size[0])), self.drawpos[1] - (self.keypointerbmp.GetHeight()))
            dc.DrawBitmap(self.keypointerbmp, drawpos[0], drawpos[1])

        # Current frame text
        #dc.SetFont(self.font)
        string = "Current frame: %i" % self.curframe
        stringwidth, stringheight = dc.GetTextExtent(string)
        dc.DrawText(string, w - (self.sidepadding + stringwidth), h - (self.sidepadding + stringheight))


class Frame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1)
        
        self.panel = wx.Panel(self, -1)
        self.timeline = Timeline(self.panel, -1)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.timeline, 0, flag = wx.EXPAND)

        self.panel.SetSizer(self.sizer)
        self.Layout()
        self.timeline.SetMax(150)

        self.Bind(wx.EVT_CLOSE, self.Exit)
        self.Bind(wx.EVT_SLIDER, self.Slider)

    def Exit(self, event):
        self.timeline.Destroy()
        self.Destroy()

    def Slider(self, event):
        pass#print "Frame = %i" % event.GetInt())


if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = Frame(None)
    frame.SetTitle("ExeSoft Obsidian - timeline widget test")
    frame.Show()
    app.SetTopWindow(frame)
    app.MainLoop()

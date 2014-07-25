#!/usr/bin/env python

############################################################################
#    begin                : Mar 21 2014
#    copyright            : (C) 2014 Valentina Fioretti, Andrea Zoli
#    email                : fioretti@iasfbo.inaf.it, zoli@iasfbo.inaf.it
############################################################################

############################################################################
#                                                                          #
#   This program is free software for non commercial purpose               #
#   and for public research institutes; you can redistribute it and/or     #
#   modify it under the terms of the GNU General Public License.           #
#   For commercial purpose see appropriate license terms                   #
#                                                                          #
############################################################################

# load modules
import pyfits
import Ice
import numpy as np
import sys
import os

# Chaco modules 
from chaco.api import ArrayPlotData, Plot, OverlayPlotContainer, Legend, PlotGraphicsContext
from enable.api import Window, Component, ComponentEditor
from traits.api import HasTraits, Instance
from traitsui.api import Item, Group, View
from chaco.tools.api import PanTool, ZoomTool, LegendTool, \
        TraitsTool, DragZoom

# Load slice definition
confdir=os.environ["CTARTA"]+"/share/viewer/"

Ice.loadSlice(confdir+"RTAViewer.ice")

Ice.updateModules()
import CTA

# open the fits file
hdulist_conf = pyfits.open(confdir+"PROD2_telconfig.fits.gz")
datal0_conf = hdulist_conf[1].data
colsl0_conf = hdulist_conf[1].columns
namesl0_field = colsl0_conf.names

TelID = datal0_conf.field(namesl0_field[1])
TelType = datal0_conf.field(namesl0_field[2])
TelX = datal0_conf.field(namesl0_field[3])
TelY = datal0_conf.field(namesl0_field[4])
TelZ = datal0_conf.field(namesl0_field[5])
#FocalLength = datal0_conf.field(namesl0_field[6])
#FOV = datal0_conf.field(namesl0_field[7])
#CameraScaleFactor = datal0_conf.field(namesl0_field[8])
#CameraCentreOffset = datal0_conf.field(namesl0_field[9])
#CameraRotation = datal0_conf.field(namesl0_field[10])
NPixel = datal0_conf.field(namesl0_field[11])
#NPixel_active = datal0_conf.field(namesl0_field[12])
#NSamples = datal0_conf.field(namesl0_field[13])
#Sample_time_slice = datal0_conf.field(namesl0_field[14])
#NGains = datal0_conf.field(namesl0_field[15])
#HiLoScale = datal0_conf.field(namesl0_field[16])
#HiLoThreshold = datal0_conf.field(namesl0_field[17])
#HiLoOffset = datal0_conf.field(namesl0_field[18])
#NTubesOFF = datal0_conf.field(namesl0_field[19])
#NMirrors = datal0_conf.field(namesl0_field[20])
#MirrorArea = datal0_conf.field(namesl0_field[21])

#datal1_conf = hdulist_conf[2].data
#colsl1_conf = hdulist_conf[2].columns
#namesl1_field = colsl1_conf.names

#XTubeMM = datal1_conf.field(namesl1_field[3])
#YTubeMM = datal1_conf.field(namesl1_field[4])
#RTubeMM = datal1_conf.field(namesl1_field[5])
#XTubeDeg = datal1_conf.field(namesl1_field[6])
#YTubeDeg = datal1_conf.field(namesl1_field[7])
#RTubeDeg = datal1_conf.field(namesl1_field[8])
#TubeOFF = datal1_conf.field(namesl1_field[9])

NTel = len(TelID)
max_NPixel = int(max(NPixel))

# Looking for the telescope types for L, M and S
newTelType = list(set(TelType))
NTelType = np.zeros(len(newTelType))
listTelType = list(TelType)
for jtype in xrange(len(newTelType)):
    NTelType[jtype] = listTelType.count(newTelType[jtype])
    fromLargerToSmaller = np.argsort(NTelType)
    LType = newTelType[fromLargerToSmaller[0]]
    MType = newTelType[fromLargerToSmaller[1]]        
    SType = newTelType[fromLargerToSmaller[2]]
    
TelNames = ["SST", "MST", "LST"]
LSTelID = TelID[np.where(TelType == LType)]
LSTelX = TelX[np.where(TelType == LType)]
LSTelY = TelY[np.where(TelType == LType)]
MSTelID = TelID[np.where(TelType == MType)]
MSTelX = TelX[np.where(TelType == MType)]
MSTelY = TelY[np.where(TelType == MType)]
SSTelID = TelID[np.where(TelType == SType)]
SSTelX = TelX[np.where(TelType == SType)]
SSTelY = TelY[np.where(TelType == SType)]

# Setting the configuration and starting variables
size=(700,700)
title="CTA Quick Look"

class ViewerI(CTA.RTAViewer):
    def __init__(self, viewer):
        CTA.RTAViewer.__init__(self)
        self._viewer = viewer

    def update(self, telescopes, evtnum, current=None):
        self._viewer.jtrig += 1

        LSTindex = []
        MSTindex = []
        SSTindex = []

        TrigLTelX = []
        TrigLTelY = []
        TrigMTelX = []
        TrigMTelY = []
        TrigSTelX = []
        TrigSTelY = []
	         
        for jtrig_tel in xrange(len(telescopes)):
            where_tel = np.where(TelID == telescopes[jtrig_tel])
            trig_tel_type = TelType[where_tel]
            if (trig_tel_type == LType):
                 tempTelX = TelX[where_tel]
                 TrigLTelX.append(tempTelX[0])
                 tempTelY = TelY[where_tel]
                 TrigLTelY.append(tempTelY[0])
                 where_LTelX = np.where((LSTelX == tempTelX))
                 where_LTelX = where_LTelX[0]
                 where_LTelY = np.where((LSTelY == tempTelY))
                 where_LTelY = where_LTelY[0]
                 for jxindex in xrange(len(where_LTelX)):
                     for jyindex in xrange(len(where_LTelY)):
                         if (where_LTelX[jxindex] == where_LTelY[jyindex]):
                             shared_index = where_LTelX[jxindex]
                             break

                 LSTindex.append(shared_index)
 
            if (trig_tel_type == MType):
                tempTelX = TelX[where_tel]
                TrigMTelX.append(tempTelX[0])
                tempTelY = TelY[where_tel]
                TrigMTelY.append(tempTelY[0])
                where_MTelX = np.where((MSTelX == tempTelX))
                where_MTelX = where_MTelX[0]
                where_MTelY = np.where((MSTelY == tempTelY))
                where_MTelY = where_MTelY[0]
                for jxindex in xrange(len(where_MTelX)):
                    for jyindex in xrange(len(where_MTelY)):
                        if (where_MTelX[jxindex] == where_MTelY[jyindex]):
                            shared_index = where_MTelX[jxindex]
                            break

                MSTindex.append(shared_index)
	                      
            if (trig_tel_type == SType):
                tempTelX = TelX[where_tel]
                TrigSTelX.append(tempTelX[0])
                tempTelY = TelY[where_tel]
                TrigSTelY.append(tempTelY[0])
                where_STelX = np.where((SSTelX == tempTelX))
                where_STelX = where_STelX[0]
                where_STelY = np.where((SSTelY == tempTelY))
                where_STelY = where_STelY[0]
                for jxindex in xrange(len(where_STelX)):
                    for jyindex in xrange(len(where_STelY)):
                        if (where_STelX[jxindex] == where_STelY[jyindex]):
                            shared_index = where_STelX[jxindex]
                            break

                SSTindex.append(shared_index)

        restLTelX = np.delete(LSTelX,  LSTindex)
        restLTelY = np.delete(LSTelY,  LSTindex)
        restMTelX = np.delete(MSTelX,  MSTindex)
        restMTelY = np.delete(MSTelY,  MSTindex)
        restSTelX = np.delete(SSTelX,  SSTindex)
        restSTelY = np.delete(SSTelY,  SSTindex)        

        print 'Total LST: ', np.array(LSTelX).size
        print 'Triggered LST: ', np.array(TrigLTelX).size
        print 'Rest LST: ', np.array(restLTelX).size 

        print 'Total MST: ', np.array(MSTelX).size
        print 'Triggered MST: ', np.array(TrigMTelX).size
        print 'Rest MST: ', np.array(restMTelX).size

        print 'Total SST: ', np.array(SSTelX).size
        print 'Triggered SST: ', np.array(TrigSTelX).size
        print 'Rest SST: ', np.array(restSTelX).size

        print 'Total: ', np.array(LSTelX).size + np.array(MSTelX).size + np.array(SSTelX).size
        print 'Total triggered: ', np.array(TrigLTelX).size +  np.array(TrigMTelX).size  +  np.array(TrigSTelX).size
        print 'Total rest: ',np.array(restLTelX).size +  np.array(restMTelX).size + np.array(restSTelX).size

        self._viewer.LSTdefault.set_data('xtel', restLTelX)
        self._viewer.LSTdefault.set_data('ytel', restLTelY)
        self._viewer.plotLST.request_redraw()

        self._viewer.MSTdefault.set_data('xtel', restMTelX)
        self._viewer.MSTdefault.set_data('ytel', restMTelY)
        self._viewer.plotMST.request_redraw()

        self._viewer.SSTdefault.set_data('xtel', restSTelX)
        self._viewer.SSTdefault.set_data('ytel', restSTelY)
        self._viewer.plotSST.request_redraw()

        if (np.array(TrigLTelX).size != 0):
            self._viewer.LSTdata.set_data('xtel', TrigLTelX)
            self._viewer.LSTdata.set_data('ytel', TrigLTelY)
            self._viewer.rLSTdata[0].color = 'red'
            self._viewer.rLSTdata[0].marker_size = 9
            self._viewer.rLSTdata[0].line_width = 0
            self._viewer.plotLSTtrig.request_redraw()        	            
        if (np.array(TrigMTelX).size != 0):
            self._viewer.MSTdata.set_data('xtel', TrigMTelX)
            self._viewer.MSTdata.set_data('ytel', TrigMTelY)
            self._viewer.rMSTdata[0].color = 'red'
            self._viewer.rMSTdata[0].marker_size = 6
            self._viewer.rMSTdata[0].line_width = 0
            self._viewer.plotMSTtrig.request_redraw()
        if (np.array(TrigSTelX).size != 0):
            self._viewer.SSTdata.set_data('xtel', TrigSTelX)
            self._viewer.SSTdata.set_data('ytel', TrigSTelY)
            self._viewer.rSSTdata[0].color = 'red'
            self._viewer.rSSTdata[0].marker_size = 4
            self._viewer.rSSTdata[0].line_width = 0
            self._viewer.plotSSTtrig.request_redraw()

class ChacoViewer(HasTraits, Ice.Application):
    plot = Instance(Component)

    traits_view = View(
                  Group(
                  Item('plot', editor=ComponentEditor(size=size),
                  show_label=False),
                  orientation = "vertical"),
                  resizable=True, title=title,
                  width=size[0], height=size[1])

    def __init__(self, **traits):
        Ice.Application.__init__(self)
        HasTraits.__init__(self,**traits)

        plots = {}
        container = OverlayPlotContainer(padding = 50, fill_padding = True,
                                         bgcolor = "lightgray", use_backbuffer=True)
        self.jtrig = 0

        # Plot all telescopes
        self.LSTdefault = ArrayPlotData()
        self.LSTdefault.set_data('xtel', LSTelX)
        self.LSTdefault.set_data('ytel', LSTelY)
        self.plotLST = Plot(self.LSTdefault)
        self.rLST = self.plotLST.plot(('xtel', 'ytel'), type = "scatter", color = 'black', name = 'LST', marker = 'circle')	  
        self.rLST[0].marker_size = 6    
        self.plotLST.range2d.x_range.high = np.max(TelX + 100.)
        self.plotLST.range2d.x_range.low = np.min(TelX - 100.)
        self.plotLST.range2d.y_range.high = np.max(TelY + 100.)
        self.plotLST.range2d.y_range.low = np.min(TelY - 100.)
        self.plotLST.title = "Triggered telescopes"
 
        container.add(self.plotLST)

        self.MSTdefault = ArrayPlotData()
        self.MSTdefault.set_data('xtel', MSTelX)
        self.MSTdefault.set_data('ytel', MSTelY)
 
        self.plotMST = Plot(self.MSTdefault)
        self.rMST = self.plotMST.plot(('xtel', 'ytel'), type = "scatter", color = 'black', name = 'MST', marker = 'circle')	  
        self.rMST[0].marker_size = 4    
        self.plotMST.range2d = self.plotLST.range2d
 
        container.add(self.plotMST)
 
        self.SSTdefault = ArrayPlotData()
        self.SSTdefault.set_data('xtel', SSTelX)
        self.SSTdefault.set_data('ytel', SSTelY)
 
        self.plotSST = Plot(self.SSTdefault)
        self.rSST = self.plotSST.plot(('xtel', 'ytel'), type = "scatter", color = 'black', name = 'MST', marker = 'circle')	  
        self.rSST[0].marker_size = 1    
        self.plotSST.range2d = self.plotLST.range2d

        container.add(self.plotSST)

        self.plotLST.tools.append(PanTool(self.plotLST))

        # The ZoomTool tool is stateful and allows drawing a zoom
        # box to select a zoom region.
        zoom = ZoomTool(self.plotLST, tool_mode="box", always_on=False)
        self.plotLST.overlays.append(zoom)

        # The DragZoom tool just zooms in and out as the user drags
        # the mouse vertically.
        dragzoom = DragZoom(self.plotLST, drag_button="right")
        self.plotLST.tools.append(dragzoom)

        # Add a legend in the upper right corner, and make it relocatable
        plots["LST"] = self.rLST
        plots["MST"] = self.rMST
        plots["SST"] = self.rSST
        legend = Legend(component=self.plotLST, padding=10, align="ur", line_spacing = 7, font = 'modern 14')
        legend.tools.append(LegendTool(legend, drag_button="right"))
        self.plotLST.overlays.append(legend)
        legend.plots = plots

        # Triggered telescopes
        self.LSTdata = ArrayPlotData()
        self.LSTdata.set_data('xtel', LSTelX)
        self.LSTdata.set_data('ytel', LSTelY)
 
        self.plotLSTtrig = Plot(self.LSTdata)
        self.rLSTdata = self.plotLSTtrig.plot(('xtel', 'ytel'), type = "scatter", marker = 'circle', marker_size = 6)	  
        self.plotLSTtrig.range2d = self.plotLST.range2d
        container.add(self.plotLSTtrig)

        self.MSTdata = ArrayPlotData()
        self.MSTdata.set_data('xtel', MSTelX)
        self.MSTdata.set_data('ytel', MSTelY)
 
        self.plotMSTtrig = Plot(self.MSTdata)
        self.rMSTdata = self.plotMSTtrig.plot(('xtel', 'ytel'), type = "scatter", marker = 'circle', marker_size = 4)	  
        self.plotMSTtrig.range2d = self.plotMST.range2d
 
        container.add(self.plotMSTtrig)
 
        self.SSTdata = ArrayPlotData()
        self.SSTdata.set_data('xtel', SSTelX)
        self.SSTdata.set_data('ytel', SSTelY)

        self.plotSSTtrig = Plot(self.SSTdata)
        self.rSSTdata = self.plotSSTtrig.plot(('xtel', 'ytel'), type = "scatter", marker = 'circle', marker_size = 1)	  
        self.plotSSTtrig.range2d = self.plotSST.range2d

        container.add(self.plotSSTtrig)
 
        # Set the list of plots on the legend
        #legend.plots = plots

        # Add the traits inspector tool to the container
        container.tools.append(TraitsTool(container))

        #draw_png(home_dir + '/Projects/visRTA/Plots/visTrigTel'+str(counter)+'.png', _create_plot_component(self))
        #filename = home_dir + '/Projects/visRTA/Plots/visTrigTel'+str(counter)+'.png'
        #gc = PlotGraphicsContext(size, dpi=72.0)
        #gc.render_component(container)
        #gc.save(filename)

        self.plot = container
        print "end init"

    def run(self, args):
        print "running!"
        if len(args) > 1:
            print(self.appName() + ": too many arguments")
            return 1

        adapter = self.communicator().createObjectAdapter("RTAViewer")
        adapter.add(ViewerI(self), self.communicator().stringToIdentity("viewer"))
        adapter.activate()

		# start the chaco draw loop
        self.configure_traits()

        return 0

if __name__ == "__main__":
    viewer = ChacoViewer()
    sys.exit(viewer.main(sys.argv))

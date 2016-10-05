#!/usr/bin/env python3

import numpy as np
import pandas as pd
import abscplane as absc

class ComplexPlaneNP(absc.AbsComplexPlane):
    def __init__(self, newXmin=-5., newXmax=5., newYmin=-5., newYmax=5., f=lambda x: x):
        self.xmin = newXmin
        self.xmax = newXmax
        self.ymin = newYmin
        self.ymax = newYmax
        self.xlen = 5
        self.ylen = 5
        self.xstep = (self.xmax - self.xmin)/(self.xlen - 1)
        self.ystep = (self.ymax - self.ymin)/(self.ylen - 1)
        self.f = f
        self.refresh()
    def refresh(self):
        planeArray = np.empty([self.xlen,self.ylen], dtype=complex)
        for xpos in range(self.xlen):
            for ypos in range(self.ylen):
                planeArray[(self.ylen-ypos-1),xpos] = self.f( (xpos*self.xstep+self.xmin) + (ypos*self.ystep+self.ymin)*1j )
        ylabels = [str(self.ymax-ypos*self.ystep) for ypos in range(self.ylen)]
        xlabels = [str(xpos*self.xstep+self.xmin) for xpos in range(self.xlen)]
        self.plane = pd.DataFrame(planeArray, index=ylabels, columns=xlabels)
    def zoom(self,newXmin,newXmax,newYmin,newYmax):
        self.xmin = newXmin
        self.xmax = newXmax
        self.ymin = newYmin
        self.ymax = newYmax
        self.refresh()
    def set_f(self, f):
        self.f = f
        self.refresh()

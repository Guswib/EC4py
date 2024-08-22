""" Python module for reading TDMS files produced by LabView and specifically form EC4 DAQ.

    This module contains the public facing API for reading TDMS files produced by EC4 DAQ.
"""
from nptdms import TdmsFile
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter 
from . import util
from .ec_data import EC_Data
from .step_data import Step_Data
from .ec_setup import EC_Setup

from pathlib import Path
import copy
from .util import Quantity_Value_Unit as Q_V
from .util_graph import plot_options,quantity_plot_fix, make_plot_2x,make_plot_1x


STYLE_POS_DL = "bo"
STYLE_NEG_DL = "ro"

class Step_Datas:
    """# Class to analyze CV datas. 
    Class Functions:
    - .plot() - plot data    
    - .bg_corr() to back ground correct.
    
    ### Analysis:
    - .Levich() - plot data    
    - .KouLev() - Koutechy-Levich analysis    
    - .Tafel() - Tafel analysis data    
    
    ### Options args:
    "area" - to normalize to area
    
    ### Options keywords:
    legend = "name"
    """
    def __init__(self, paths:list[Path] | Path, **kwargs):
        
        if isinstance(paths,Path ):
            path_list = [paths]
        else:
            path_list = paths
        self.datas = [Step_Data() for i in range(len(path_list))]
        index=0
        for path in path_list:
            ec = EC_Data(path)
            try:
                self.datas[index].conv(ec,**kwargs)
            finally:
                index=index+1 
        #print(index)
        return
    #############################################################################
    def __getitem__(self, item_index:slice|int) -> Step_Data: 

        if isinstance(item_index, slice):
            step = 1
            start = 0
            stop = len(self.datas)
            if item_index.step:
                step =  item_index.step
            if item_index.start:
                start = item_index.start
            if item_index.stop:
                stop = item_index.stop    
            return [self.datas[i] for i in range(start,stop,step)  ]
        else:
            return self.datas[item_index]
    #############################################################################
    def __setitem__(self, item_index:int, new_Step:Step_Data):
        if not isinstance(item_index, int):
            raise TypeError("key must be an integer")
        self.datas[item_index] = new_Step
    #############################################################################
   
    
################################################################    
    def plot(self, *args, **kwargs):
        """Plot CVs.
            use args to normalize the data
            - area or area_cm
            - rotation
            - rate
            
            #### use kwargs for other settings.
            
            - legend = "name"
            - x_smooth = 10
            - y_smooth = 10
            
            
        """
        #CV_plot = make_plot_1x("CVs")
        p = plot_options(kwargs)
        p.set_title("CVs")
        line, CV_plot = p.exe()
        legend = p.legend
        #analyse_plot.title.set_text('CVs')

        #analyse_plot.title.set_text('Levich Plot')
        
        rot=[]
        y = []
        E = []
        #Epot=-0.5
        y_axis_title =""
        CVs = copy.deepcopy(self.datas)
        #CVs = [CV_Data() for i in range(len(paths))]
        cv_kwargs = kwargs
        for cv in CVs:
            #rot.append(math.sqrt(cv.rotation))
            for arg in args:
                cv.norm(arg)

            cv_kwargs["plot"] = CV_plot
            cv_kwargs["name"] = cv.setup_data.name
            if legend == "_" :
                cv_kwargs["legend"] = cv.setup_data.name
            
            p = cv.plot(**cv_kwargs)
         
        CV_plot.legend()
        return CV_plot
    
    #################################################################################################    
   
    
    ##################################################################################################################
    def Tafel(self, lims=[-1,1], E_for_idl:float=None , *args, **kwargs):
        return
    
    
 
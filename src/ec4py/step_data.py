""" Python module for reading TDMS files produced by LabView and specifically form EC4 DAQ.

    This module contains the public facing API for reading TDMS files produced by EC4 DAQ.
"""
from __future__ import annotations
import math
import numpy as np
from scipy import integrate
from scipy.signal import savgol_filter 

import copy

from .ec_data import EC_Data,index_at_time

from .ec_setup import EC_Setup
from .util_graph import plot_options
from .util import extract_value_unit     
from .util import Quantity_Value_Unit as Q_V

class Step_Data(EC_Setup):

    def __init__(self,*args, **kwargs):
        super().__init__()
        #self._area=2
        #self._area_unit="cm^2"
        #self.rotation =0
        #self.rotation_unit ="/min"
        self.Time=np.array([],dtype=np.float64)
        self.E=np.array([],dtype=np.float64)
        self.i=np.array([],dtype=np.float64)
        self.i_label = "i"
        self.i_unit = "A"
        self.step_Time =[]
        self.step_E =[]
        self.step_Type =[]
        if not args:
            return
        else:
            #print(kwargs)
            self.conv(EC_Data(args[0]),**kwargs)
    #############################################################################   
    
    def conv(self, ec_data: EC_Data, *args, ** kwargs):
        """Converts EC_Data to a CV

        Args:
            ec_data (EC_Data): the data that should be converted.
        """
        #print("Convert:",kwargs)
        
        ch_E ="E"
        for a in args:
            if a == "IR":
                ch_E = "E-IR"
        options = {
            'x_smooth' : 0,
            'y_smooth' : 0,
            'IR': 0
        }
        options.update(kwargs)
        
        try:
            self.setup_data = ec_data.setup_data
            #self.convert(ec_data.Time,ec_data.E,ec_data.i,**kwargs)
            self.Time = ec_data.Time
            self.i =ec_data.i
            self.E = ec_data.E
            
            self.step_Time = self.setup_data._setup["Step.Time"].split(";",-1)
            self.step_E = self.setup_data._setup["Step.E"].split(";",-1)
            self.step_Type = self.setup_data._setup["Step.Type"].split(";",-1)

           
        except ValueError:
            print("no_data")
        #self.setup = data.setup
        #self.set_area(data._area, data._area_unit)
        #self.set_rotation(data.rotation, data.rotation_unit)
        #self.name = data.name
        return
    
    def plot(self, x_channel:str="Time", y_channel:str="i", **kwargs):
        '''
        plots y_channel vs x_channel.\n
        to add to a existing plot, add the argument: \n
        "plot = subplot"\n
        "x_smooth= number" - smoothing of the x-axis. \n
        "y_smooth= number" - smoothing of the y-axis. \n
        
        '''
        #xlable ="wrong channel name"
        #xunit = "wrong channel name"
        #ylable ="wrong channel name"
        #yunit = "wrong channel name"
        
        range = {
            'limit_min' : -1,
            'limit_max' : -1   
        }
        range.update(kwargs)
        #print(kwargs)
        #print(range)
        options = plot_options(kwargs)
        index_min = 0
        if range["limit_min"] >0:
            index_min = self.index_at_time(range["limit_min"])
        index_max = len(self.Time)-1
        if range["limit_max"] >0:
            index_max = self.index_at_time(range["limit_max"])
        
        #max_index = len(self.Time)-1
        #print("index", index_min,index_max)
        try:
            x_data, options.x_label, options.x_unit = self.Time,"t","s"
            options.x_data = x_data[index_min:index_max]
        except NameError:
            print(f"xchannel {x_channel} not supported")
        try:
            y_data, options.y_label, options.y_unit = self.E,"E","V"
            options.y_data = y_data[index_min:index_max]
        except NameError:
            print(f"ychannel {y_channel} not supported")

        return options.exe()
    
    def index_at_time(self, time_s_:float):
        return index_at_time(self.Time, time_s_)
    
    def get_step(self,step_index:int):
        singleStep = Step_Data()
        singleStep.setup_data = self.setup_data
        startT = 0.0
        endT = float(self.step_Time[step_index])
        if(step_index != 0):
            startT = float(self.step_Time[step_index-1]) 
        #print("startT",startT)
        #print("endT",endT)
        
        start_index = self.index_at_time(startT)
        end_index =   self.index_at_time(endT)
        #print("startT",start_index)
        #print("endT",end_index)
        aSize=end_index-start_index+1
        singleStep.E = np.empty(aSize) 
        singleStep.i = np.empty(aSize) 
        singleStep.Time = np.empty(aSize)    
        np.copyto(singleStep.E, self.E[start_index:end_index+1])
        np.copyto(singleStep.i, self.i[start_index:end_index+1])
        np.copyto(singleStep.Time, self.Time[start_index:end_index+1]-self.Time[start_index])
        
        singleStep.step_Time =[singleStep.Time.max()]
        singleStep.step_E =[self.step_E[step_index]]
        singleStep.step_Type =[self.step_Type[step_index]]
        return singleStep
        
        
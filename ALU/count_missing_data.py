from distillate import Distillate
import numpy as np
import qdf

def compute(input_streams):
        good_LA=[]
        bad_LA=[]
        good_LB=[]
        LB = input_streams[0]
        LC=input_streams[1]
        LA=input_streams[2]
        
        idx=0
        while idx < len(LB):
         print LB[idx].time
         break
       
        return[good_LA,bad_LA,good_LB]
        
        
        
# set all data stream, date, distillate name, unit, output folder needed for this job     
opts = { 'input_streams'  : ['upmu/grizzly_new/L1ANG','upmu/grizzly_new/L2ANG','upmu/grizzly_new/L3ANG'],\
         'input_uids'     : ['b4776088-2f85-4c75-90cd-7472a949a8fa','8b80c070-7bb1-44d3-b3a8-301558d573ea',
                             'b653c63b-4acc-45ee-ae3d-1602e6116bc1'], \
         'start_date'     : '2014-10-01T00:00:00.000000', \
         'end_date'       : '2014-10-01T00:00:10.000000', \
         'output_streams' : ['grizzly_LA','grizzly_LB','grizzly_LC'], \
         'output_units'   : ['Degree','Degree','Degree'], \
         'author'         : 'Andrew', \
         'name'           : 'count missing data', \
         'version'        : 2, \
         'algorithm'      : compute }        
qdf.register(Distillate(), opts)
qdf.begin()

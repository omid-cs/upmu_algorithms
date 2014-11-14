from distillate import Distillate
import numpy as np
import qdf

def compute(input_streams):
        LB = input_streams[0]
        LC=input_streams[1]
        LA=input_streams[2]
        LB_check=[]
        LA_check=[]
        LC_check=[]
        idx=1
        while idx < len(LB):
         if LB[idx].time-LB[idx-1].time == 8333333
          print True,LB[idx].time,LB[idx-1].time
         else
          print False,LB[idx].time,LB[idx-1].time
         idx+=1 
         ''' 
         LB_check.append((LB[idx-1].time,0))
         time=LB[idx-1].time
         while (round(LB[idx].time-time))<8333333:
           time+=8333333 
           LB_check.append((time,1))
         idx+=1
        LB_check.append((LB[idx-1].time,0))
        idx=1
        while idx < len(LA):
         LA_check.append((LA[idx-1].time,0))
         time=LA[idx-1].time
         while (round(LA[idx].time-time))<8333333:
           time+=8333333 
           LA_check.append((time,1))
         idx+=1
        LA_check.append((LA[idx-1].time,0))
        idx=1
        while idx < len(LC):
         LC_check.append((LC[idx-1].time,0))
         time=LC[idx-1].time
         while (round(LC[idx].time-time))<8333333:
           time+=8333333 
           LC_check.append((time,1))
         idx+=1
        LC_check.append((LC[idx-1].time,0))
        '''
        return[LA_check,LB_check,LC_check]
        
        
        
# set all data stream, date, distillate name, unit, output folder needed for this job     
opts = { 'input_streams'  : ['upmu/grizzly_new/L1ANG','upmu/grizzly_new/L2ANG','upmu/grizzly_new/L3ANG'],\
         'input_uids'     : ['b4776088-2f85-4c75-90cd-7472a949a8fa','8b80c070-7bb1-44d3-b3a8-301558d573ea',
                             'b653c63b-4acc-45ee-ae3d-1602e6116bc1'], \
         'start_date'     : '2014-10-01T00:59:50.000000', \
         'end_date'       : '2014-10-31T00:00:00.000000', \
         'output_streams' : ['grizzly_LA','grizzly_LB','grizzly_LC'], \
         'output_units'   : ['Degree','Degree','Degree'], \
         'author'         : 'Andrew', \
         'name'           : 'count missing data', \
         'version'        : 14, \
         'algorithm'      : compute }        
qdf.register(Distillate(), opts)
qdf.begin()

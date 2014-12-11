from distillate import Distillate
from pylab import *
import numpy as np
import qdf

def compute(input_streams):
        # data input
        grizzly_L1 = input_streams[0]
        soda_a_L1=input_streams[1]
        grizzly_C1 = input_streams[2]
        soda_a_C1=input_streams[3]
        
        L1ang_GS = []
        C1ang_GS = []
       
        idx1 = 0
        idx2 = 0
        # matching time between data stream and skip the piont when there is no data for that time
        while idx1 < len(grizzly_L1) and idx2 < len(soda_a_L1):
            if grizzly_L1[idx1].time < soda_a_L1[idx2].time:
                idx1 += 1
                continue
            if grizzly_L1[idx1].time > soda_a_L1[idx2].time:
                idx2 += 1
                continue
            # compute angle difference 
            delta = grizzly_L1[idx1].value - soda_a_L1[idx2].value
            
            L1ang_GS.append((grizzly_L1[idx1].time, delta))
            idx1 += 1
            idx2 += 1
            
        idx1 = 0
        idx2 = 0
        # matching time between data stream and skip the piont when there is no data for that time
        while idx1 < len(grizzly_C1) and idx2 < len(soda_a_C1):
            if grizzly_C1[idx1].time < soda_a_C1[idx2].time:
                idx1 += 1
                continue
            if grizzly_C1[idx1].time > soda_a_C1[idx2].time:
                idx2 += 1
                continue
            # compute angle difference 
            delta = grizzly_C1[idx1].value - soda_a_C1[idx2].value
            
            C1ang_GS.append((grizzly_C1[idx1].time, delta))
            idx1 += 1
            idx2 += 1 
        
        
        # return angle difference computed   
        return[L1ang_GS,C1ang_GS]
        
        
        
# set all data stream, date, distillate name, unit, output folder needed for this job     
opts = { 'input_streams'  : ['upmu/grizzly_new/L1MAG','upmu/soda_a/L1MAG','upmu/grizzly_new/C1MAG','upmu/soda_a/C1MAG'], \
         'input_uids'     : ['a64c386e-2dd4-4f17-96cb-1655358cb12c','abffcf07-9e17-404a-98c3-ea4d60042ff3',
                             '425b9c51-9aba-4d1a-a677-85cd7afd6269','9f638ccc-0c73-4e76-a43f-7538058f2974'], \
         'start_date'     : '2014-12-03T00:00:00.000000', \
         'end_date'       : '2014-12-03T11:59:59.000000', \
         'output_streams' : ['Grizzly-Soda_a_VOLT_MAGDIFF_1','Grizzly-Soda_a_CURR_MAGDIFF_1'], \
         'output_units'   : ['V','V'], \
         'author'         : 'Mag Diff', \
         'name'           : 'Grizzly-Soda_a', \
         'version'        : 3, \
         'algorithm'      : compute }        
qdf.register(Distillate(), opts)
qdf.begin()

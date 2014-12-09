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
            if delta > 180:
                delta =delta-360
            if delta <-180:
                delta=delta+360
            if delta ==-180:
                delta=180
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
            if delta > 180:
                delta =delta-360
            if delta <-180:
                delta=delta+360
            if delta ==-180:
                delta=180
            C1ang_GS.append((grizzly_C1[idx1].time, delta))
            idx1 += 1
            idx2 += 1 
        
        
        # return angle difference computed   
        return[L1ang_GS,C1ang_GS]
        
        
        
# set all data stream, date, distillate name, unit, output folder needed for this job     
opts = { 'input_streams'  : ['upmu/grizzly_new/L1ANG','upmu/soda_a/L1ANG','upmu/grizzly_new/C1ANG','upmu/soda_a/C1ANG'], \
         'input_uids'     : ['b4776088-2f85-4c75-90cd-7472a949a8fa','4d6525a9-b8ad-48a4-ae98-b171562cf817',
                             '4b7fec6d-270e-4bd6-b301-0eac6df17ca2','888b8f61-c2a4-44a1-bd5c-9865ea6ea8ca'], \
         'start_date'     : '2014-12-03T12:00:00.000000', \
         'end_date'       : '2014-12-03T13:00:00.000000', \
         'output_streams' : ['Grizzly-Soda_a_VOLT_ANGDIFF_1','Grizzly-Soda_a_CURR_ANGDIFF_1'], \
         'output_units'   : ['Degree','Degree'], \
         'author'         : 'Phase Ang Diff', \
         'name'           : 'Grizzly-Soda_a', \
         'version'        : 1, \
         'algorithm'      : compute }        
qdf.register(Distillate(), opts)
qdf.begin()

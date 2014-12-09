from distillate import Distillate
from pylab import *
import numpy as np
import qdf

def compute(input_streams):
        # data input
        grizzly = input_streams[0]
        switcha6=input_streams[1]
        
        L1ang_GS = []
        idx1 = 0
        idx2 = 0
        # matching time between data stream and skip the piont when there is no data for that time
        while idx1 < len(grizzly) and idx2 < len(switcha6):
            if grizzly[idx1].time < switcha6[idx2].time:
                idx1 += 1
                continue
            if grizzly[idx1].time > switcha6[idx2].time:
                idx2 += 1
                continue
            # compute angle difference 
            delta = grizzly[idx1].value - switcha6[idx2].value
            if delta > 180:
                delta =delta-360
            if delta <-180:
                delta=delta+360
            if delta ==-180:
                delta=180
            L1ang_GS.append((grizzly[idx1].time, delta))
            idx1 += 1
            idx2 += 1
        # return angle difference computed   
        return[L1ang_GS]
        
        
        
# set all data stream, date, distillate name, unit, output folder needed for this job     
opts = { 'input_streams'  : ['upmu/grizzly_new/C3ANG','upmu/switch_a6/C3ANG'], \
         'input_uids'     : ['8b40fe4c-36ee-4b10-8aef-1eef8c471e1d','8a5d0010-4665-4b59-ab6f-e7858c12284a'], \
         'start_date'     : '2014-12-03T12:00:00.000000', \
         'end_date'       : '2014-12-03T13:00:00.000000', \
         'output_streams' : ['Grizzly-SwitchA6_CURR_ANGDIFF_1'], \
         'output_units'   : ['Degree'], \
         'author'         : 'Phase Ang Diff', \
         'name'           : 'Grizzly-Switch_a6', \
         'version'        : 26, \
         'algorithm'      : compute }        
qdf.register(Distillate(), opts)
qdf.begin()

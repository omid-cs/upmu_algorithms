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
opts = { 'input_streams'  : ['upmu/grizzly_new/C1ANG','upmu/switch_a6/C1ANG'], \
         'input_uids'     : ['4b7fec6d-270e-4bd6-b301-0eac6df17ca2','4072af6f-938e-450c-9927-37dee6968446'], \
         'start_date'     : '2014-10-07T02:00:00.000000', \
         'end_date'       : '2014-10-07T03:00:00.000000', \
         'output_streams' : ['Grizzly-SwitchA6_CURR_ANGDIFF_B'], \
         'output_units'   : ['Degree'], \
         'author'         : 'Phase Ang Diff', \
         'name'           : 'Grizzly-Switch_a6', \
         'version'        : 23, \
         'algorithm'      : compute }        
qdf.register(Distillate(), opts)
qdf.begin()

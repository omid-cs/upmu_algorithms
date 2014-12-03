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
opts = { 'input_streams'  : ['upmu/grizzly_new/L2ANG','upmu/switch_a6/L2ANG'], \
         'input_uids'     : ['8b80c070-7bb1-44d3-b3a8-301558d573ea','4f56a8f1-f3ca-4684-930e-1b4d9955f72c'], \
         'start_date'     : '2014-10-07T02:00:00.000000', \
         'end_date'       : '2014-10-07T03:00:00.000000', \
         'output_streams' : ['Grizzly-SwitchA6_VOLT_ANGDIFF_C'], \
         'output_units'   : ['Degree'], \
         'author'         : 'Phase Ang Diff', \
         'name'           : 'Grizzly-Switch_a6', \
         'version'        : 20, \
         'algorithm'      : compute }        
qdf.register(Distillate(), opts)
qdf.begin()

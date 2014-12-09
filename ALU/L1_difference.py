from distillate import Distillate
from pylab import *
import numpy as np
import qdf

def compute(input_streams):
        # data input
        grizzly_L1 = input_streams[0]
        switcha6_L1=input_streams[1]
        grizzly_L2 = input_streams[2]
        switcha6_L2=input_streams[3]
        grizzly_L3 = input_streams[4]
        switcha6_L3=input_streams[5]
        grizzly_C1 = input_streams[6]
        switcha6_C1=input_streams[7]
        grizzly_C2 = input_streams[8]
        switcha6_C2=input_streams[9]
        grizzly_C3 = input_streams[10]
        switcha6_C3=input_streams[11]
        L1ang_GS = []
        L2ang_GS = []
        L3ang_GS = []
        C1ang_GS = []
        C2ang_GS = []
        C3ang_GS = []
        idx1 = 0
        idx2 = 0
        # matching time between data stream and skip the piont when there is no data for that time
        while idx1 < len(grizzly_L1) and idx2 < len(switcha6_L1):
            if grizzly_L1[idx1].time < switcha6_L1[idx2].time:
                idx1 += 1
                continue
            if grizzly_L1[idx1].time > switcha6_L1[idx2].time:
                idx2 += 1
                continue
            # compute angle difference 
            delta = grizzly_L1[idx1].value - switcha6_L1[idx2].value
            if delta > 180:
                delta =delta-360
            if delta <-180:
                delta=delta+360
            if delta ==-180:
                delta=180
            L2ang_GS.append((grizzly_L1[idx1].time, delta))
            idx1 += 1
            idx2 += 1
            
        idx1 = 0
        idx2 = 0
        # matching time between data stream and skip the piont when there is no data for that time
        while idx1 < len(grizzly_L2) and idx2 < len(switcha6_L2):
            if grizzly_L2[idx1].time < switcha6_L2[idx2].time:
                idx1 += 1
                continue
            if grizzly_L2[idx1].time > switcha6_L2[idx2].time:
                idx2 += 1
                continue
            # compute angle difference 
            delta = grizzly_L2[idx1].value - switcha6_L2[idx2].value
            if delta > 180:
                delta =delta-360
            if delta <-180:
                delta=delta+360
            if delta ==-180:
                delta=180
            L3ang_GS.append((grizzly_L2[idx1].time, delta))
            idx1 += 1
            idx2 += 1 
        
        idx1 = 0
        idx2 = 0
        # matching time between data stream and skip the piont when there is no data for that time
        while idx1 < len(grizzly_L3) and idx2 < len(switcha6_L3):
            if grizzly_L3[idx1].time < switcha6_L3[idx2].time:
                idx1 += 1
                continue
            if grizzly_L3[idx1].time > switcha6_L3[idx2].time:
                idx2 += 1
                continue
            # compute angle difference 
            delta = grizzly_L3[idx1].value - switcha6_L3[idx2].value
            if delta > 180:
                delta =delta-360
            if delta <-180:
                delta=delta+360
            if delta ==-180:
                delta=180
            L1ang_GS.append((grizzly_L3[idx1].time, delta))
            idx1 += 1
            idx2 += 1 
        
        idx1 = 0
        idx2 = 0
        # matching time between data stream and skip the piont when there is no data for that time
        while idx1 < len(grizzly_C1) and idx2 < len(switcha6_C1):
            if grizzly_C1[idx1].time < switcha6_C1[idx2].time:
                idx1 += 1
                continue
            if grizzly_C1[idx1].time > switcha6_C1[idx2].time:
                idx2 += 1
                continue
            # compute angle difference 
            delta = grizzly_C1[idx1].value - switcha6_C1[idx2].value
            if delta > 180:
                delta =delta-360
            if delta <-180:
                delta=delta+360
            if delta ==-180:
                delta=180
            C2ang_GS.append((grizzly_C1[idx1].time, delta))
            idx1 += 1
            idx2 += 1
            
        idx1 = 0
        idx2 = 0
        # matching time between data stream and skip the piont when there is no data for that time
        while idx1 < len(grizzly_C2) and idx2 < len(switcha6_C2):
            if grizzly_C2[idx1].time < switcha6_C2[idx2].time:
                idx1 += 1
                continue
            if grizzly_C2[idx1].time > switcha6_C2[idx2].time:
                idx2 += 1
                continue
            # compute angle difference 
            delta = grizzly_C2[idx1].value - switcha6_C2[idx2].value
            if delta > 180:
                delta =delta-360
            if delta <-180:
                delta=delta+360
            if delta ==-180:
                delta=180
            C3ang_GS.append((grizzly_C2[idx1].time, delta))
            idx1 += 1
            idx2 += 1   
            
        idx1 = 0
        idx2 = 0
        # matching time between data stream and skip the piont when there is no data for that time
        while idx1 < len(grizzly_C3) and idx2 < len(switcha6_C3):
            if grizzly_C3[idx1].time < switcha6_C3[idx2].time:
                idx1 += 1
                continue
            if grizzly_C3[idx1].time > switcha6_C3[idx2].time:
                idx2 += 1
                continue
            # compute angle difference 
            delta = grizzly_C3[idx1].value - switcha6_C3[idx2].value
            if delta > 180:
                delta =delta-360
            if delta <-180:
                delta=delta+360
            if delta ==-180:
                delta=180
            C1ang_GS.append((grizzly_C3[idx1].time, delta))
            idx1 += 1
            idx2 += 1    
        # return angle difference computed   
        return[L1ang_GS,L2ang_GS,L3ang_GS,C1ang_GS,C2ang_GS,C3ang_GS]
        
        
        
# set all data stream, date, distillate name, unit, output folder needed for this job     
opts = { 'input_streams'  : ['upmu/grizzly_new/L1ANG','upmu/switch_a6/L1ANG','upmu/grizzly_new/L2ANG','upmu/switch_a6/L2ANG',
                             'upmu/grizzly_new/L3ANG','upmu/switch_a6/L3ANG','upmu/grizzly_new/C1ANG','upmu/switch_a6/C1ANG',
                             'upmu/grizzly_new/C2ANG','upmu/switch_a6/C2ANG','upmu/grizzly_new/C3ANG','upmu/switch_a6/C3ANG'], \
         'input_uids'     : ['b4776088-2f85-4c75-90cd-7472a949a8fa','adf13e17-44b7-4ef6-ae3f-fde8a9152ab7',
                             '8b80c070-7bb1-44d3-b3a8-301558d573ea','4f56a8f1-f3ca-4684-930e-1b4d9955f72c',
                             'b653c63b-4acc-45ee-ae3d-1602e6116bc1','2c07ccef-20c5-4971-87cf-2c187ce5f722',
                             '4b7fec6d-270e-4bd6-b301-0eac6df17ca2','4072af6f-938e-450c-9927-37dee6968446',
                             '9ffeaf2a-46a9-465f-985d-96f84df66283','bf045a36-34df-4bee-a747-b20c3164723a',
                             '8b40fe4c-36ee-4b10-8aef-1eef8c471e1d','8a5d0010-4665-4b59-ab6f-e7858c12284a'], \
         'start_date'     : '2014-12-03T12:00:00.000000', \
         'end_date'       : '2014-12-03T13:00:00.000000', \
         'output_streams' : ['Grizzly-SwitchA6_VOLT_ANGDIFF_1','Grizzly-SwitchA6_VOLT_ANGDIFF_2','Grizzly-SwitchA6_VOLT_ANGDIFF_3',
                             'Grizzly-SwitchA6_CURR_ANGDIFF_1','Grizzly-SwitchA6_CURR_ANGDIFF_2','Grizzly-SwitchA6_CURR_ANGDIFF_3'], \
         'output_units'   : ['Degree','Degree','Degree','Degree','Degree','Degree'], \
         'author'         : 'Phase Ang Diff', \
         'name'           : 'Grizzly-Switch_a6', \
         'version'        : 32, \
         'algorithm'      : compute }        
qdf.register(Distillate(), opts)
qdf.begin()

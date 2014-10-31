from distillate import Distillate
import numpy as np
import qdf

def compute(input_streams):
        
        grizzly = input_streams[0]
        building71=input_streams[1]
        switcha6=input_streams[2]
        sodaa=input_streams[3]
        sodab=input_streams[4]
        L2ang_GB=[]
        idx1 = 0
        idx2 = 0
        while idx1 < len(grizzly) and idx2 < len(building71):
            if grizzly[idx1].time < building71[idx2].time:
                idx1 += 1
                continue
            if grizzly[idx1].time > building71[idx2].time:
                idx2 += 1
                continue
            delta = grizzly[idx1].value - building71[idx2].value
            if delta > 180:
                delta =delta-360
            if delta <-180:
                delta=delta+360
            if delta ==-180:
                delta=180
            L2ang_GB.append((grizzly[idx1].time, delta))
            idx1 += 1
            idx2 += 1

        
        L2ang_GS = []

        idx1 = 0
        idx2 = 0
        while idx1 < len(grizzly) and idx2 < len(switcha6):
            if grizzly[idx1].time < switcha6[idx2].time:
                idx1 += 1
                continue
            if grizzly[idx1].time > switcha6[idx2].time:
                idx2 += 1
                continue
            delta = grizzly[idx1].value - switcha6[idx2].value
            if delta > 180:
                delta =delta-360
            if delta <-180:
                delta=delta+360
            if delta ==-180:
                delta=180
            L2ang_GS.append((grizzly[idx1].time, delta))
            idx1 += 1
            idx2 += 1
        
        L2ang_BS = []

        idx1 = 0
        idx2 = 0
        while idx1 < len(building71) and idx2 < len(switcha6):
            if building71[idx1].time < switcha6[idx2].time:
                idx1 += 1
                continue
            if building71[idx1].time > switcha6[idx2].time:
                idx2 += 1
                continue
            delta = building71[idx1].value - switcha6[idx2].value
            if delta > 180:
                delta =delta-360
            if delta <-180:
                delta=delta+360
            if delta ==-180:
                delta=180
            L2ang_BS.append((building71[idx1].time, delta))
            idx1 += 1
            idx2 += 1
        
        L2ang_SaSb = []

        idx1 = 0
        idx2 = 0
        while idx1 < len(sodaa) and idx2 < len(sodab):
            if sodaa[idx1].time < sodab[idx2].time:
                idx1 += 1
                continue
            if sodaa[idx1].time > sodab[idx2].time:
                idx2 += 1
                continue
            delta = sodaa[idx1].value - sodab[idx2].value
            if delta > 180:
                delta =delta-360
            if delta <-180:
                delta=delta+360
            if delta ==-180:
                delta=180
            L2ang_SaSb.append((sodaa[idx1].time, delta))
            idx1 += 1
            idx2 += 1
        return[L2ang_GB,L2ang_GS,L2ang_BS,L2ang_SaSb]
        
        
        
    
opts = { 'input_streams'  : ['upmu/grizzly_new/L2ANG','upmu/building_71/L2ANG','upmu/switch_a6/L2ANG',
                            'upmu/soda_a/L2ANG','upmu/soda_b/L2ANG'], \
         'input_uids'     : ['8b80c070-7bb1-44d3-b3a8-301558d573ea','f89e77a8-661e-49d2-a868-2071c1fae238',
                             '4f56a8f1-f3ca-4684-930e-1b4d9955f72c','fe580578-854d-43c5-95b4-9f305a70e6a3',
                             '321db464-b05b-4a97-988c-1a9cc5593143'], \
         'start_date'     : '2014-10-01T00:00:00.000000', \
         'end_date'       : '2014-10-19T00:00:00.000000', \
         'output_streams' : ['L2ang_GB','L2ang_GS','L2ang_BS','L2ang_SaSb'], \
         'output_units'   : ['Degree','Degree','Degree','Degree'], \
         'author'         : 'Andrew', \
         'name'           : 'L2_difference', \
         'version'        : 10, \
         'algorithm'      : compute }        
qdf.register(Distillate(), opts)
qdf.begin() 

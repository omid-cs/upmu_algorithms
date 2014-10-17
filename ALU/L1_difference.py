from distillate import Distillate
import numpy as np
import qdf

def compute(input_streams):
        
        grizzly = input_streams[0]
        building71=input_streams[1]
        switcha6=input_streams[2]
        sodaa=input_streams[3]
        sodab=input_streams[4]
        L1ang_GB=[]
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
            L1ang_GB.append((grizzly[idx1].time, delta))
            idx1 += 1
            idx2 += 1

        
        L1ang_GS = []

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
            L1ang_GS.append((grizzly[idx1].time, delta))
            idx1 += 1
            idx2 += 1
        
        L1ang_BS = []

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
            L1ang_BS.append((building71[idx1].time, delta))
            idx1 += 1
            idx2 += 1
        
        L1ang_SaSb = []

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
            L1ang_SaSb.append((sodaa[idx1].time, delta))
            idx1 += 1
            idx2 += 1
        return[L1ang_GB,L1ang_GS,L1ang_BS,L1ang_SaSb]
        
        
        
    
opts = { 'input_streams'  : ['upmu/grizzly_new/L1ANG','upmu/building_71/L1ANG','upmu/switch_a6/L1ANG',
                            'upmu/soda_a/L1ANG','upmu/soda_b/L1ANG'], \
         'input_uids'     : ['8b80c070-7bb1-44d3-b3a8-301558d573ea','66fcb659-c69a-41b5-b874-80ac7d7f669d',
                             'adf13e17-44b7-4ef6-ae3f-fde8a9152ab7','4d6525a9-b8ad-48a4-ae98-b171562cf817',
                             '98435be7-7341-4661-b104-16af89e0333d'], \
         'start_date'     : '2014-10-01T00:00:00.000000', \
         'end_date'       : '2014-10-15T00:00:00.000000', \
         'output_streams' : ['L1ang_GB','L1ang_GS','L1ang_BS','L1ang_SaSb'], \
         'output_units'   : ['Degree','Degree','Degree','Degree'], \
         'author'         : 'Andrew', \
         'name'           : 'L1_difference', \
         'version'        : 15, \
         'algorithm'      : compute }        
qdf.register(Distillate(), opts)
qdf.begin()

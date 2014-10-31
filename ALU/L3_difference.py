from distillate import Distillate
import numpy as np
import qdf

def compute(input_streams):
        
        grizzly = input_streams[0]
        building71=input_streams[1]
        switcha6=input_streams[2]
        sodaa=input_streams[3]
        sodab=input_streams[4]
        L3ang_GB=[]
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
            L3ang_GB.append((grizzly[idx1].time, delta))
            idx1 += 1
            idx2 += 1

        
        L3ang_GS = []

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
            L3ang_GS.append((grizzly[idx1].time, delta))
            idx1 += 1
            idx2 += 1
        
        L3ang_BS = []

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
            L3ang_BS.append((building71[idx1].time, delta))
            idx1 += 1
            idx2 += 1
        
        L3ang_SaSb = []

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
            L3ang_SaSb.append((sodaa[idx1].time, delta))
            idx1 += 1
            idx2 += 1
        return[L3ang_GB,L3ang_GS,L3ang_BS,L3ang_SaSb]
        
        
        
    
opts = { 'input_streams'  : ['upmu/grizzly_new/L3ANG','upmu/building_71/L3ANG','upmu/switch_a6/L3ANG',
                            'upmu/soda_a/L3ANG','upmu/soda_b/L3ANG'], \
         'input_uids'     : ['b653c63b-4acc-45ee-ae3d-1602e6116bc1','65f49c81-dafa-4aa2-8467-1627fb489c0c',
                             '2c07ccef-20c5-4971-87cf-2c187ce5f722','b5279898-5652-4d34-abd6-45c7d697e524',
                             '33b376c8-a59e-4054-a213-e9eb95cc8ad9'], \
         'start_date'     : '2014-10-01T00:00:00.000000', \
         'end_date'       : '2014-10-19T00:00:00.000000', \
         'output_streams' : ['L3ang_GB','L3ang_GS','L3ang_BS','L3ang_SaSb'], \
         'output_units'   : ['Degree','Degree','Degree','Degree'], \
         'author'         : 'Andrew', \
         'name'           : 'L3_difference', \
         'version'        : 6, \
         'algorithm'      : compute }        
qdf.register(Distillate(), opts)
qdf.begin()
 

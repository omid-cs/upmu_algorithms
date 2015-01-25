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
            
            C1ang_GS.append((grizzly_C3[idx1].time, delta))
            idx1 += 1
            idx2 += 1    
        # return angle difference computed   
        return[L1ang_GS,L2ang_GS,L3ang_GS,C1ang_GS,C2ang_GS,C3ang_GS]
        
        
        
# set all data stream, date, distillate name, unit, output folder needed for this job     
opts = { 'input_streams'  : ['upmu/grizzly_new/L1MAG','upmu/switch_a6/L1MAG','upmu/grizzly_new/L2MAG','upmu/switch_a6/L2MAG',
                             'upmu/grizzly_new/L3MAG','upmu/switch_a6/L3MAG','upmu/grizzly_new/C1MAG','upmu/switch_a6/C1MAG',
                             'upmu/grizzly_new/C2MAG','upmu/switch_a6/C2MAG','upmu/grizzly_new/C3MAG','upmu/switch_a6/C3MAG'], \
         'input_uids'     : ['a64c386e-2dd4-4f17-96cb-1655358cb12c','df64af25-a389-4be9-8061-f87c3616f286',
                             'a002295a-32ee-41a1-8ec4-8657d0d1f943','6e6ad513-ddd2-47fb-98c1-16e6477504fc',
                             'db3ea4f7-a337-4874-baeb-17fc2c0cf18b','bcf38098-0e16-46f2-a9fb-9ce481d7d55b',
                             '425b9c51-9aba-4d1a-a677-85cd7afd6269','bf8ea2c0-6d04-4cdd-ba4b-0421eac0cabd',
                             'ca613e9a-1211-4c52-a98f-b8f9f1ce0672','51d4801e-0bb6-4040-8e74-e7839be65156',
                             'b1025f33-97fd-45d6-bc0f-80132e1dc756','249b364d-b0a1-4b65-8aca-ffd68565c1de'], \
         'start_date'     : '2014-12-03T00:00:00.000000', \
         'end_date'       : '2014-12-03T11:59:59.000000', \
         'output_streams' : ['Grizzly-SwitchA6_VOLT_MAGDIFF_3','Grizzly-SwitchA6_VOLT_MAGDIFF_1','Grizzly-SwitchA6_VOLT_MAGDIFF_2',
                             'Grizzly-SwitchA6_CURR_MAGDIFF_3','Grizzly-SwitchA6_CURR_MAGDIFF_1','Grizzly-SwitchA6_CURR_MAGDIFF_2'], \
         'output_units'   : ['V','V','V','V','V','V'], \
         'author'         : 'Mag Diff', \
         'name'           : 'Grizzly-Switch_a6', \
         'version'        : 3, \
         'algorithm'      : compute }        
qdf.register(Distillate(), opts)
qdf.begin()

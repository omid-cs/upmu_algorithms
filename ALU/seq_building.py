from distillate import Distillate
import numpy as np
import qdf

def compute(input_streams):
        
        L1Ang = input_streams[0]
        L1Mag=input_streams[1]
        L2Ang=input_streams[2]
        L2Mag=input_streams[3]
        L3Ang=input_streams[4]
        L3Mag=input_streams[4]
        V0Ang=[]
        V0Mag=[]
        VpAng=[]
        VpMag=[]
        VnAng=[]
        VnMag=[]
        idxL1A=0
        idxL1M=0
        idxL2A=0
        idxL2M=0
        idxL3A=0
        idxL3M=0
        
        while idxL1A < len(L1Ang) and idxL1M < len(L1Mag) and idxL2A < len(L2Ang) and idxL2M < len(L2Mag) \
        and idxL3A < len(L3Ang) and idxL3M < len(L3Mag): 
            if L1Ang[idxL1A].time < L2Ang[idxL2A].time:
                idxL1A += 1
                idxL1M += 1
                continue
            if L1Ang[idxL1A].time > L2Ang[idxL2A].time:
                idxL2A += 1
                idxL2M += 1
                continue
            if L1Ang[idxL1A].time < L3Ang[idxL3A].time:
                idxL1A += 1
                idxL1M += 1
                continue
            if L1Ang[idxL1A].time > L3Ang[idxL3A].time:
                idxL3A += 1
                idxL3M += 1
                continue
            if L2Ang[idxL2A].time < L3Ang[idxL3A].time:
                idxL2A += 1
                idxL2M += 1
                continue
            if L2Ang[idxL2A].time > L3Ang[idxL3A].time:
                idxL3A += 1
                idxL3M += 1
                continue
            v0m=(L1Mag[idxL1M].value+L2Mag[idxL2M].value+L3Mag[idxL3M].value)/3.0
            V0Mag.append((L1Mag[idxL1M].time, v0m))
            VpMag.append((L1Mag[idxL1M].time, v0m))
            VnMag.append((L1Mag[idxL1M].time, v0m))
            v0a=(L1Ang[idxL1A].value+L2Ang[idxL2A].value+L3Ang[idxL3A].value)/3.0
            V0Ang.append((L1Ang[idxL1A].time,v0a))
            vna=(L1Ang[idxL1A].value+L2Ang[idxL2A].value+120+L3Ang[idxL3A].value+240)/3.0
            VnAng.append((L1Ang[idxL1A].time,vna))
            vpa=(L1Ang[idxL1A].value+L2Ang[idxL2A].value+240+L3Ang[idxL3A].value+120)/3.0
            VpAng.append((L1Ang[idxL1A].time,vpa))
            idxL1A+= 1
            idxL1M+= 1
            idxL2A+= 1
            idxL2M+= 1
            idxL3A+= 1
            idxL3M+= 1
        return[V0Ang,V0Mag,VpAng,VpMag,VnAng,VnMag]
        
        
        
    
opts = { 'input_streams'  : ['upmu/building_71/L1ANG','upmu/building_71/L1MAG','upmu/building_71/L2ANG',
                            'upmu/building_71/L2MAG','upmu/building_71/L3ANG','upmu/building_71/L3MAG'], \
         'input_uids'     : ['66fcb659-c69a-41b5-b874-80ac7d7f669d','cc866bb9-849f-4955-9276-241d5732fa0a',
                             'f89e77a8-661e-49d2-a868-2071c1fae238','87b2b0bf-cb23-4381-b6d8-5068fbdf6ebb',
                             '65f49c81-dafa-4aa2-8467-1627fb489c0c','f8b59b00-63be-4e7c-958b-831830df07f4'], \
         'start_date'     : '2014-10-01T00:00:00.000000', \
         'end_date'       : '2014-10-19T00:00:00.000000', \
         'output_streams' : ['building_V0Ang','building_V0Mag','building_V+Ang','building_V+Mag','building_V-Ang','building_V-Mag'], \
         'output_units'   : ['Degree','V','Degree','V','Degree','V'], \
         'author'         : 'Andrew', \
         'name'           : 'Sequense', \
         'version'        : 1, \
         'algorithm'      : compute }        
qdf.register(Distillate(), opts)
qdf.begin()

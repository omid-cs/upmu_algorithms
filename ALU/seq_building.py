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
        
        
        
    
opts = { 'input_streams'  : ['upmu/switch_a6/L1ANG','upmu/switch_a6/L1MAG','upmu/switch_a6/L2ANG',
                            'upmu/switch_a6/L2MAG','upmu/switch_a6/L3ANG','upmu/switch_a6/L3MAG'], \
         'input_uids'     : ['adf13e17-44b7-4ef6-ae3f-fde8a9152ab7','df64af25-a389-4be9-8061-f87c3616f286',
                             '4f56a8f1-f3ca-4684-930e-1b4d9955f72c','6e6ad513-ddd2-47fb-98c1-16e6477504fc',
                             '2c07ccef-20c5-4971-87cf-2c187ce5f722','bcf38098-0e16-46f2-a9fb-9ce481d7d55b'], \
         'start_date'     : '2014-10-01T00:00:00.000000', \
         'end_date'       : '2014-10-19T00:00:00.000000', \
         'output_streams' : ['switch_V0Ang','switch_V0Mag','switch_V+Ang','switch_V+Mag','switch_V-Ang','switch_V-Mag'], \
         'output_units'   : ['Degree','V','Degree','V','Degree','V'], \
         'author'         : 'Andrew', \
         'name'           : 'Sequense', \
         'version'        : 1, \
         'algorithm'      : compute }        
qdf.register(Distillate(), opts)
qdf.begin()

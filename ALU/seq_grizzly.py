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
        
        while idxL1A < len(L1Ang) and idxL1Mag < len(L1Mag) and idxL2A < len(L2Ang) and idxL2Mag < len(L2Mag) \
        and idxL3A < len(L3Ang) and idxL3Mag < len(L3Mag): 
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
            VnAng.append((L1Ang[idxL1A].time,v-a))
            vpa=(L1Ang[idxL1A].value+L2Ang[idxL2A].value+240+L3Ang[idxL3A].value+120)/3.0
            VpAng.append((L1Ang[idxL1A].time,v+a))
            idxL1A+= 1
            idxL1M+= 1
            idxL2A+= 1
            idxL2M+= 1
            idxL3A+= 1
            idxL3M+= 1
        return[V0Ang,V0Mag,VpAng,VpMag,VnAng,VnMag]
        
        
        
    
opts = { 'input_streams'  : ['upmu/grizzly_new/L1ANG','upmu/grizzly_new/L1MAG','upmu/grizzly_new/L2ANG',
                            'upmu/grizzly_new/L2MAG','upmu/grizzly_new/L3ANG','upmu/grizzly_new/L3MAG'], \
         'input_uids'     : ['b4776088-2f85-4c75-90cd-7472a949a8fa','a64c386e-2dd4-4f17-96cb-1655358cb12c',
                             '8b80c070-7bb1-44d3-b3a8-301558d573ea','a002295a-32ee-41a1-8ec4-8657d0d1f943',
                             'b653c63b-4acc-45ee-ae3d-1602e6116bc1','db3ea4f7-a337-4874-baeb-17fc2c0cf18b'], \
         'start_date'     : '2014-10-01T00:00:00.000000', \
         'end_date'       : '2014-10-19T00:00:00.000000', \
         'output_streams' : ['V0Ang','V0Mag','V+Ang','V+Mag','V-Ang','V-Mag'], \
         'output_units'   : ['Degree','V','Degree','V','Degree','V'], \
         'author'         : 'Andrew', \
         'name'           : 'Sequense', \
         'version'        : 1, \
         'algorithm'      : compute }        
qdf.register(Distillate(), opts)
qdf.begin()

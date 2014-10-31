from distillate import Distillate
import numpy as np
import math
import qdf

def compute(input_streams):
        # data input
        L1Ang = input_streams[0]
        L1Mag=input_streams[1]
        L2Ang=input_streams[2]
        L2Mag=input_streams[3]
        L3Ang=input_streams[4]
        L3Mag=input_streams[5]
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
        
        # matching time among all 6 data strams to make sure they are at same time before compute sequence
        while idxL1A < len(L1Ang) and idxL1M < len(L1Mag) and idxL2A < len(L2Ang) and idxL2M < len(L2Mag) \
        and idxL3A < len(L3Ang) and idxL3M < len(L3Mag): 
            if L1Ang[idxL1A].time < L2Ang[idxL2A].time:
                idxL1A += 1
                continue
            if L1Ang[idxL1A].time > L2Ang[idxL2A].time:
                idxL2A += 1
                continue
            if L1Ang[idxL1A].time < L3Ang[idxL3A].time:
                idxL1A += 1
                continue
            if L1Ang[idxL1A].time > L3Ang[idxL3A].time:
                idxL3A += 1
                continue
            if L2Ang[idxL2A].time < L3Ang[idxL3A].time:
                idxL2A += 1
                continue
            if L2Ang[idxL2A].time > L3Ang[idxL3A].time:
                idxL3A += 1
                continue
            if L1Mag[idxL1M].time < L2Mag[idxL2M].time:
                idxL1M += 1
                continue
            if L1Mag[idxL1M].time > L2Mag[idxL2M].time:
                idxL2M += 1
                continue
            if L1Mag[idxL1M].time < L3Mag[idxL3M].time:
                idxL1M += 1
                continue
            if L1Mag[idxL1M].time > L3Mag[idxL3M].time:
                idxL3M += 1
                continue
            if L2Mag[idxL2M].time < L3Mag[idxL3M].time:
                idxL2M += 1
                continue
            if L2Mag[idxL2M].time > L3Mag[idxL3M].time:
                idxL3M += 1
                continue
            if L1Mag[idxL1M].time < L1Ang[idxL1A].time:
                idxL1M += 1
                continue
            if L1Mag[idxL1M].time > L1Ang[idxL1A].time:
                idxL1A += 1
                continue
            if L2Mag[idxL2M].time < L2Ang[idxL2A].time:
                idxL2M += 1
                continue
            if L2Mag[idxL2M].time > L2Ang[idxL2A].time:
                idxL2A += 1
                continue
            if L3Mag[idxL3M].time < L3Ang[idxL3A].time:
                idxL2M += 1
                continue
            if L3Mag[idxL3M].time > L3Ang[idxL3A].time:
                idxL3A += 1
                continue
            # compute sin value for three phase and sin value for l2 and l3 anfter add 120 degree and 240 degree
            sinL1Ang=np.sin(np.radians(L1Ang[idxL1A].value))
            sinL2Ang=np.sin(np.radians(L2Ang[idxL2A].value))
            sinL3Ang=np.sin(np.radians(L3Ang[idxL3A].value))
            sinL2Ang_add120=np.sin(np.radians(L2Ang[idxL2A].value+120))
            sinL2Ang_add240=np.sin(np.radians(L2Ang[idxL2A].value+240))
            sinL3Ang_add120=np.sin(np.radians(L3Ang[idxL3A].value+120))
            sinL3Ang_add240=np.sin(np.radians(L3Ang[idxL3A].value+240))
            
            # compute cosin value for three phase and cosin value for l2 and l3 anfter add 120 degree and 240 degree
            cosL1Ang=np.cos(np.radians(L1Ang[idxL1A].value))
            cosL2Ang=np.cos(np.radians(L2Ang[idxL2A].value))
            cosL3Ang=np.cos(np.radians(L3Ang[idxL3A].value))
            cosL2Ang_add120=np.cos(np.radians(L2Ang[idxL2A].value+120))
            cosL2Ang_add240=np.cos(np.radians(L2Ang[idxL2A].value+240))
            cosL3Ang_add120=np.cos(np.radians(L3Ang[idxL3A].value+120))
            cosL3Ang_add240=np.cos(np.radians(L3Ang[idxL3A].value+240))
            
            # compute V0
            v0imagine=(L1Mag[idxL1M].value*sinL1Ang+L2Mag[idxL2M].value*sinL2Ang+L3Mag[idxL3M].value*sinL3Ang)/3.0
            v0real=(L1Mag[idxL1M].value*cosL1Ang+L2Mag[idxL2M].value*cosL2Ang+L3Mag[idxL3M].value*cosL3Ang)/3.0
            v0mag=np.sqrt(v0imagine**2+v0real**2)
            v0ang=np.degrees(math.atan2(v0imagine,v0real))
            V0Mag.append((L1Mag[idxL1M].time, v0mag))
            V0Ang.append((L1Ang[idxL1A].time,v0ang))
            
            #compute v-
            vnimagine=(L1Mag[idxL1M].value*sinL1Ang+L2Mag[idxL2M].value*sinL2Ang_add120+L3Mag[idxL3M].value*sinL3Ang_add240)/3.0
            vnreal=(L1Mag[idxL1M].value*cosL1Ang+L2Mag[idxL2M].value*cosL2Ang_add120+L3Mag[idxL3M].value*cosL3Ang_add240)/3.0
            vnmag=np.sqrt(vnimagine**2+vnreal**2)
            vnang=np.degrees(math.atan2(vnimagine,vnreal))
            VnMag.append((L1Mag[idxL1M].time, vnmag))
            VnAng.append((L1Ang[idxL1A].time,vnang))
            
            # compute v+
            vpimagine=(L1Mag[idxL1M].value*sinL1Ang+L2Mag[idxL2M].value*sinL2Ang_add240+L3Mag[idxL3M].value*sinL3Ang_add120)/3.0
            vpreal=(L1Mag[idxL1M].value*cosL1Ang+L2Mag[idxL2M].value*cosL2Ang_add240+L3Mag[idxL3M].value*cosL3Ang_add120)/3.0
            vpmag=np.sqrt(vpimagine**2+vpreal**2)
            vpang=np.degrees(math.atan2(vpimagine,vpreal))
            VpMag.append((L1Mag[idxL1M].time, vpmag))
            VpAng.append((L1Ang[idxL1A].time,vpang))
            
            idxL1A+= 1
            idxL1M+= 1
            idxL2A+= 1
            idxL2M+= 1
            idxL3A+= 1
            idxL3M+= 1
        # return V0 V+ V- 
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
         'version'        : 3, \
         'algorithm'      : compute }        
qdf.register(Distillate(), opts)
qdf.begin()

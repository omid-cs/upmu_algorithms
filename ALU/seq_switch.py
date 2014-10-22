from distillate import Distillate
import numpy as np
import qdf

def compute(input_streams):
        
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
            if L1Mag[idxL1M].time > L!Ang[idxL1A].time:
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
        
            sinL1Ang=np.sin(np.radians(L1Ang[idxL1A].value))
            sinL2Ang=np.sin(np.radians(L2Ang[idxL2A].value))
            sinL3Ang=np.sin(np.radians(L3Ang[idxL3A].value))
            sinL2Ang_add120=np.sin(np.radians(L2Ang[idxL2A].value+120))
            sinL2Ang_add240=np.sin(np.radians(L2Ang[idxL2A].value+240))
            sinL3Ang_add120=np.sin(np.radians(L3Ang[idxL3A].value+120))
            sinL3Ang_add240=np.sin(np.radians(L3Ang[idxL3A].value+240))
            
            cosL1Ang=np.cos(np.radians(L1Ang[idxL1A].value))
            cosL2Ang=np.cos(np.radians(L2Ang[idxL2A].value))
            cosL3Ang=np.cos(np.radians(L3Ang[idxL3A].value))
            cosL2Ang_add120=np.cos(np.radians(L2Ang[idxL2A].value+120))
            cosL2Ang_add240=np.cos(np.radians(L2Ang[idxL2A].value+240))
            cosL3Ang_add120=np.cos(np.radians(L3Ang[idxL3A].value+120))
            cosL3Ang_add240=np.cos(np.radians(L3Ang[idxL3A].value+240))
            
            v0imagine=(L1Mag[idxL1M]*sinL1Ang+L2Mag[idxL2M]*sinL2Ang+L3Mag[idxL3M]*sinL3Ang)/3.0
            v0real=(L1Mag[idxL1M]*cosL1Ang+L2Mag[idxL2M]*cosL2Ang+L3Mag[idxL3M]*cosL3Ang)/3.0
            v0mag=np.sqrt(v0imagine**2+v0real**2)
            v0ang=np.degrees(np.atan2(v0imagine,v0real))
            V0Mag.append((L1Mag[idxL1M].time, v0mag))
            V0Ang.append((L1Ang[idxL1A].time,v0ang))
            
            vnimagine=(L1Mag[idxL1M]*sinL1Ang+L2Mag[idxL2M]*sinL2Ang_add120+L3Mag[idxL3M]*sinL3Ang_add240)/3.0
            vnreal=(L1Mag[idxL1M]*cosL1Ang+L2Mag[idxL2M]*cosL2Ang_add120+L3Mag[idxL3M]*cosL3Ang_add240)/3.0
            vnmag=np.sqrt(vnimagine**2+vnreal**2)
            vnang=np.degrees(np.atan2(vnimagine,vnreal))
            VnMag.append((L1Mag[idxL1M].time, vnmag))
            VnAng.append((L1Ang[idxL1A].time,vnang))
            
            vpimagine=(L1Mag[idxL1M]*sinL1Ang+L2Mag[idxL2M]*sinL2Ang_add240+L3Mag[idxL3M]*sinL3Ang_add120)/3.0
            vpreal=(L1Mag[idxL1M]*cosL1Ang+L2Mag[idxL2M]*cosL2Ang_add240+L3Mag[idxL3M]*cosL3Ang_add120)/3.0
            vpmag=np.sqrt(vpimagine**2+vpreal**2)
            vpang=np.degrees(np.atan2(vpimagine,vpreal))
            VpMag.append((L1Mag[idxL1M].time, vpmag))
            VpAng.append((L1Ang[idxL1A].time,vpang))
            
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
         'version'        : 3, \
         'algorithm'      : compute }        
qdf.register(Distillate(), opts)
qdf.begin()

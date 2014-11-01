from distillate import Distillate
import numpy as np
import math
import qdf

def compute(input_streams):
        # data input
        LBAng = input_streams[0]
        LBMag=input_streams[1]
        LCAng=input_streams[2]
        LCMag=input_streams[3]
        LAAng=input_streams[4]
        LAMag=input_streams[5]
        V0Ang=[]
        V0Mag=[]
        VpAng=[]
        VpMag=[]
        VnAng=[]
        VnMag=[]
        idxLBA=0
        idxLBM=0
        idxLCA=0
        idxLCM=0
        idxLAA=0
        idxLAM=0
        
        # matching time among all 6 data strams to make sure they are at same time before compute sequence
        while idxLBA < len(LBAng) and idxLBM < len(LBMag) and idxLCA < len(LCAng) and idxLCM < len(LCMag) \
        and idxLAA < len(LAAng) and idxLAM < len(LAMag): 
            if LBAng[idxLBA].time < LCAng[idxLCA].time:
                idxLBA += 1
                continue
            if LBAng[idxLBA].time > LCAng[idxLCA].time:
                idxLCA += 1
                continue
            if LBAng[idxLBA].time < LAAng[idxLAA].time:
                idxLBA += 1
                continue
            if LBAng[idxLBA].time > LAAng[idxLAA].time:
                idxLAA += 1
                continue
            if LCAng[idxLCA].time < LAAng[idxLAA].time:
                idxLCA += 1
                continue
            if LCAng[idxLCA].time > LAAng[idxLAA].time:
                idxLAA += 1
                continue
            if LBMag[idxLBM].time < LCMag[idxLCM].time:
                idxLBM += 1
                continue
            if LBMag[idxLBM].time > LCMag[idxLCM].time:
                idxLCM += 1
                continue
            if LBMag[idxLBM].time < LAMag[idxLAM].time:
                idxLBM += 1
                continue
            if LBMag[idxLBM].time > LAMag[idxLAM].time:
                idxLAM += 1
                continue
            if LCMag[idxLCM].time < LAMag[idxLAM].time:
                idxLCM += 1
                continue
            if LCMag[idxLCM].time > LAMag[idxLAM].time:
                idxLAM += 1
                continue
            if LBMag[idxLBM].time < LBAng[idxLBA].time:
                idxLBM += 1
                continue
            if LBMag[idxLBM].time > LBAng[idxLBA].time:
                idxLBA += 1
                continue
            if LCMag[idxLCM].time < LCAng[idxLCA].time:
                idxLCM += 1
                continue
            if LCMag[idxLCM].time > LCAng[idxLCA].time:
                idxLCA += 1
                continue
            if LAMag[idxLAM].time < LAAng[idxLAA].time:
                idxLAM += 1
                continue
            if LAMag[idxLAM].time > LAAng[idxLAA].time:
                idxLAA += 1
                continue
            # compute sin value for three phase and sin value for l2 and l3 anfter add 120 degree and 240 degree
            sinLAAng=np.sin(np.radians(LAAng[idxLAA].value-LAAng[idxLAA].value))
            sinLBAng=np.sin(np.radians(LBAng[idxLBA].value-LAAng[idxLAA].value))
            sinLCAng=np.sin(np.radians(LCAng[idxLCA].value-LAAng[idxLAA].value))
            sinLBAng_add120=np.sin(np.radians(LBAng[idxLBA].value+120-LAAng[idxLAA].value))
            sinLBAng_add240=np.sin(np.radians(LBAng[idxLBA].value+240-LAAng[idxLAA].value))
            sinLCAng_add120=np.sin(np.radians(LCAng[idxLCA].value+120-LAAng[idxLAA].value))
            sinLCAng_add240=np.sin(np.radians(LCAng[idxLCA].value+240-LAAng[idxLAA].value))
            
            # compute cosin value for three phase and cosin value for l2 and l3 anfter add 120 degree and 240 degree
            cosLAAng=np.cos(np.radians(LAAng[idxLAA].value-LAAng[idxLAA].value))
            cosLBAng=np.cos(np.radians(LBAng[idxLBA].value-LAAng[idxLAA].value))
            cosLCAng=np.cos(np.radians(LCAng[idxLCA].value-LAAng[idxLAA].value))
            cosLBAng_add120=np.cos(np.radians(LBAng[idxLBA].value+120-LAAng[idxLAA].value))
            cosLBAng_add240=np.cos(np.radians(LBAng[idxLBA].value+240-LAAng[idxLAA].value))
            cosLCAng_add120=np.cos(np.radians(LCAng[idxLCA].value+120-LAAng[idxLAA].value))
            cosLCAng_add240=np.cos(np.radians(LCAng[idxLCA].value+240-LAAng[idxLAA].value))
            
            # compute V0
            v0imagine=(LAMag[idxLAM].value*sinLAAng+LBMag[idxLBM].value*sinLBAng+LCMag[idxLCM].value*sinLCAng)/3.0
            v0real=(LAMag[idxLAM].value*cosLAAng+LBMag[idxLBM].value*cosLBAng+LCMag[idxLCM].value*cosLCAng)/3.0
            v0mag=np.sqrt(v0imagine**2+v0real**2)
            v0ang=np.degrees(math.atan2(v0imagine,v0real))
            V0Mag.append((LAMag[idxLAM].time, v0mag))
            V0Ang.append((LAAng[idxLAA].time,v0ang))
            
            #compute v-
            vpimagine=(LAMag[idxLAM].value*sinLAAng+LBMag[idxLBM].value*sinLBAng_add120+LCMag[idxLCM].value*sinLCAng_add240)/3.0
            vpreal=(LAMag[idxLAM].value*cosLAAng+LBMag[idxLBM].value*cosLBAng_add120+LCMag[idxLCM].value*cosLCAng_add240)/3.0
            vpmag=np.sqrt(vpimagine**2+vpreal**2)
            vpang=np.degrees(math.atan2(vpimagine,vpreal))
            VpMag.append((LAMag[idxLAM].time, vpmag))
            VpAng.append((LAAng[idxLAA].time,vpang))
            
            # compute v+
            vnimagine=(LAMag[idxLAM].value*sinLAAng+LBMag[idxLBM].value*sinLBAng_add240+LCMag[idxLCM].value*sinLCAng_add120)/3.0
            vnreal=(LAMag[idxLAM].value*cosLAAng+LBMag[idxLBM].value*cosLBAng_add240+LCMag[idxLCM].value*cosLCAng_add120)/3.0
            vnmag=np.sqrt(vnimagine**2+vnreal**2)
            vnang=np.degrees(math.atan2(vnimagine,vnreal))
            VnMag.append((LAMag[idxLAM].time, vnmag))
            VnAng.append((LAAng[idxLAA].time,vnang))
            
            idxLAA+= 1
            idxLAM+= 1
            idxLBA+= 1
            idxLBM+= 1
            idxLCA+= 1
            idxLCM+= 1
        # return V0 V+ V- 
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
         'version'        : 4, \
         'algorithm'      : compute }        
qdf.register(Distillate(), opts)
qdf.begin()

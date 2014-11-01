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
            vnimagine=(LAMag[idxLAM].value*sinLAAng+LBMag[idxLBM].value*sinLBAng_add120+LCMag[idxLCM].value*sinLCAng_add240)/3.0
            vnreal=(LAMag[idxLAM].value*cosLAAng+LBMag[idxLBM].value*cosLBAng_add120+LCMag[idxLCM].value*cosLCAng_add240)/3.0
            vnmag=np.sqrt(vnimagine**2+vnreal**2)
            vnang=np.degrees(math.atan2(vnimagine,vnreal))
            VnMag.append((LAMag[idxL1M].time, vnmag))
            VnAng.append((LAAng[idxL1A].time,vnang))
            
            # compute v+
            vpimagine=(LAMag[idxLAM].value*sinLAAng+LBMag[idxLBM].value*sinLBAng_add240+LCMag[idxLCM].value*sinLCAng_add120)/3.0
            vpreal=(LAMag[idxLAM].value*cosLAAng+LBMag[idxLBM].value*cosLBAng_add240+LCMag[idxLCM].value*cosLCAng_add120)/3.0
            vpmag=np.sqrt(vpimagine**2+vpreal**2)
            vpang=np.degrees(math.atan2(vpimagine,vpreal))
            VpMag.append((LAMag[idxL1M].time, vpmag))
            VpAng.append((LAAng[idxL1A].time,vpang))
            
            idxLAA+= 1
            idxLAM+= 1
            idxLBA+= 1
            idxLBM+= 1
            idxLCA+= 1
            idxLCM+= 1
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
         'version'        : 5, \
         'algorithm'      : compute }        
qdf.register(Distillate(), opts)
qdf.begin()

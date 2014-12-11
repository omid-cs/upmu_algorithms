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
        Vn_ubalance_seq=[]
        V0_ubalance_seq=[]
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
            sinLAAng_add120=np.sin(np.radians(LAAng[idxLAA].value+120-LBAng[idxLBA].value))
            sinLAAng_add240=np.sin(np.radians(LAAng[idxLAA].value+240-LBAng[idxLBA].value))
            sinLCAng_add120=np.sin(np.radians(LCAng[idxLCA].value+120-LBAng[idxLBA].value))
            sinLCAng_add240=np.sin(np.radians(LCAng[idxLCA].value+240-LBAng[idxLBA].value))
            
            # compute cosin value for three phase and cosin value for l2 and l3 anfter add 120 degree and 240 degree
            cosLAAng=np.cos(np.radians(LAAng[idxLAA].value-LAAng[idxLAA].value))
            cosLBAng=np.cos(np.radians(LBAng[idxLBA].value-LAAng[idxLAA].value))
            cosLCAng=np.cos(np.radians(LCAng[idxLCA].value-LAAng[idxLAA].value))
            cosLAAng_add120=np.cos(np.radians(LAAng[idxLAA].value+120-LBAng[idxLBA].value))
            cosLAAng_add240=np.cos(np.radians(LAAng[idxLAA].value+240-LBAng[idxLBA].value))
            cosLCAng_add120=np.cos(np.radians(LCAng[idxLCA].value+120-LBAng[idxLBA].value))
            cosLCAng_add240=np.cos(np.radians(LCAng[idxLCA].value+240-LBAng[idxLBA].value))
            
            # compute balance V0
            v0imagine=(LAMag[idxLAM].value*sinLAAng+LBMag[idxLBM].value*sinLBAng+LCMag[idxLCM].value*sinLCAng)/3.0
            v0real=(LAMag[idxLAM].value*cosLAAng+LBMag[idxLBM].value*cosLBAng+LCMag[idxLCM].value*cosLCAng)/3.0
            v0mag=np.sqrt(v0imagine**2+v0real**2)
            v0ang=np.degrees(math.atan2(v0imagine,v0real))
            V0Mag.append((LAMag[idxLAM].time, v0mag))
            V0Ang.append((LAAng[idxLAA].time,v0ang))
            
            #compute balance v+
            vpimagine=(LBMag[idxLBM].value*sinLBAng+LCMag[idxLCM].value*sinLCAng_add120+LAMag[idxLAM].value*sinLAAng_add240)/3.0
            vpreal=(LBMag[idxLBM].value*cosLBAng+LCMag[idxLCM].value*cosLCAng_add120+LAMag[idxLAM].value*cosLAAng_add240)/3.0
            vpmag=np.sqrt(vpimagine**2+vpreal**2)
            vpang=np.degrees(math.atan2(vpimagine,vpreal))
            VpMag.append((LAMag[idxLAM].time, vpmag))
            VpAng.append((LAAng[idxLAA].time,vpang))
            
            # compute balance v-
            vnimagine=(LBMag[idxLBM].value*sinLBAng+LCMag[idxLCM].value*sinLCAng_add240+LAMag[idxLAM].value*sinLAAng_add120)/3.0
            vnreal=(LBMag[idxLBM].value*cosLBAng+LCMag[idxLCM].value*cosLCAng_add240+LAMag[idxLAM].value*cosLAAng_add120)/3.0
            vnmag=np.sqrt(vnimagine**2+vnreal**2)
            vnang=np.degrees(math.atan2(vnimagine,vnreal))
            VnMag.append((LAMag[idxLAM].time, vnmag))
            VnAng.append((LAAng[idxLAA].time,vnang))
            
            # compute unbalance V-
            Vn_ubalance_seq.append((LBMag[idxLBM].time,(vnmag/float(vpmag))*100))
            # compute unbalance v0
            V0_ubalance_seq.append((LBMag[idxLBM].time,(v0mag/float(vpmag))*100))
            
            idxLAA+= 1
            idxLAM+= 1
            idxLBA+= 1
            idxLBM+= 1
            idxLCA+= 1
            idxLCM+= 1
        
        ''' return V0, V+, V-, unbalance V neg seq, unbalance V zero seq
                   C0, C+, C-, unbalance C neg seq, unbalance C zero seq,Totalp_dpf_seq'''
        return[V0Ang,V0Mag,VpAng,VpMag,VnAng,VnMag,Vn_ubalance_seq,V0_ubalance_seq]
        
        
        
    
opts = { 'input_streams'  : ['upmu/grizzly_new/C1ANG','upmu/grizzly_new/C1MAG','upmu/grizzly_new/C2ANG',
                             'upmu/grizzly_new/C2MAG','upmu/grizzly_new/C3ANG','upmu/grizzly_new/C3MAG'], \
         'input_uids'     : ['4b7fec6d-270e-4bd6-b301-0eac6df17ca2','425b9c51-9aba-4d1a-a677-85cd7afd6269',
                             '9ffeaf2a-46a9-465f-985d-96f84df66283','ca613e9a-1211-4c52-a98f-b8f9f1ce0672',
                             '8b40fe4c-36ee-4b10-8aef-1eef8c471e1d','b1025f33-97fd-45d6-bc0f-80132e1dc756'], \
         'start_date'     : '2014-12-03T00:00:00.000000', \
         'end_date'       : '2014-12-03T11:59:59.000000', \
         'output_streams' : ['CURRENT_ZERO_SEQ_ANG','CURRENT_ZERO_SEQ_MAG','CURRENT_POSITIVE_SEQ_ANG',
                             'CURRENT_POSITIVE_SEQ_MAG','CURRENT_NEGATIVE_SEQ_ANG','CURRENT_NEGATIVE_SEQ_MAG',
                             'CURRENT_UNBALANCE_NEG_SEQ','CURRENT_UNBALANCE_ZERO_SEQ'], \
         'output_units'   : ['Degree','V','Degree','V','Degree','V','Precent','Precent'], \
         'author'         : 'Refined Grizzly', \
         'name'           : 'Sequence Components', \
         'version'        : 15, \
         'algorithm'      : compute }        
qdf.register(Distillate(), opts)
qdf.begin()

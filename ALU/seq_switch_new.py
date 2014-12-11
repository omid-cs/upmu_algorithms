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
        LAGAng=input_streams[6]
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
        idxLAGA=0
        
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
            if LAGAng[idxLAGA].time < LAAng[idxLAA].time:
                idxLAGA += 1
                continue
            if LAGAng[idxLAGA].time > LAAng[idxLAA].time:
                idxLAA += 1
                continue
            if LAGAng[idxLAGA].time < LBAng[idxLBA].time:
                idxLAGA += 1
                continue
            if LAGAng[idxLAGA].time > LBAng[idxLBA].time:
                idxLBA += 1
                continue
            if LAGAng[idxLAGA].time < LCAng[idxLCA].time:
                idxLAGA += 1
                continue
            if LAGAng[idxLAGA].time > LCAng[idxLCA].time:
                idxLCA += 1
                continue
            # compute sin value for three phase and sin value for l2 and l3 anfter add 120 degree and 240 degree
            sinLAAng=np.sin(np.radians(LAAng[idxLAA].value-LAGAng[idxLAGA].value))
            sinLBAng=np.sin(np.radians(LBAng[idxLBA].value-LAGAng[idxLAGA].value))
            sinLCAng=np.sin(np.radians(LCAng[idxLCA].value-LAGAng[idxLAGA].value))
            sinLAAng_add120=np.sin(np.radians(LAAng[idxLAA].value+120-LAGAng[idxLAGA].value))
            sinLAAng_add240=np.sin(np.radians(LAAng[idxLAA].value+240-LAGAng[idxLAGA].value))
            sinLCAng_add120=np.sin(np.radians(LCAng[idxLCA].value+120-LAGAng[idxLAGA].value))
            sinLCAng_add240=np.sin(np.radians(LCAng[idxLCA].value+240-LAGAng[idxLAGA].value))
            
            # compute cosin value for three phase and cosin value for l2 and l3 anfter add 120 degree and 240 degree
            cosLAAng=np.cos(np.radians(LAAng[idxLAA].value-LAGAng[idxLAGA].value))
            cosLBAng=np.cos(np.radians(LBAng[idxLBA].value-LAGAng[idxLAGA].value))
            cosLCAng=np.cos(np.radians(LCAng[idxLCA].value-LAGAng[idxLAGA].value))
            cosLAAng_add120=np.cos(np.radians(LAAng[idxLAA].value+120-LAGAng[idxLAGA].value))
            cosLAAng_add240=np.cos(np.radians(LAAng[idxLAA].value+240-LAGAng[idxLAGA].value))
            cosLCAng_add120=np.cos(np.radians(LCAng[idxLCA].value+120-LAGAng[idxLAGA].value))
            cosLCAng_add240=np.cos(np.radians(LCAng[idxLCA].value+240-LAGAng[idxLAGA].value))
            
            # compute V0
            v0imagine=(LAMag[idxLAM].value*sinLAAng+LBMag[idxLBM].value*sinLBAng+LCMag[idxLCM].value*sinLCAng)/3.0
            v0real=(LAMag[idxLAM].value*cosLAAng+LBMag[idxLBM].value*cosLBAng+LCMag[idxLCM].value*cosLCAng)/3.0
            v0mag=np.sqrt(v0imagine**2+v0real**2)
            v0ang=np.degrees(math.atan2(v0imagine,v0real))
            V0Mag.append((LAMag[idxLAM].time, v0mag))
            V0Ang.append((LAAng[idxLAA].time,v0ang))
            
            #compute v-
            vpimagine=(LBMag[idxLBM].value*sinLBAng+LCMag[idxLCM].value*sinLCAng_add120+LAMag[idxLAM].value*sinLAAng_add240)/3.0
            vpreal=(LBMag[idxLBM].value*cosLBAng+LCMag[idxLCM].value*cosLCAng_add120+LAMag[idxLAM].value*cosLAAng_add240)/3.0
            vpmag=np.sqrt(vpimagine**2+vpreal**2)
            vpang=np.degrees(math.atan2(vpimagine,vpreal))
            VpMag.append((LBMag[idxLBM].time, vpmag))
            VpAng.append((LBAng[idxLBA].time,vpang))
            
            # compute v+
            vnimagine=(LBMag[idxLBM].value*sinLBAng+LCMag[idxLCM].value*sinLCAng_add240+LAMag[idxLAM].value*sinLAAng_add120)/3.0
            vnreal=(LBMag[idxLBM].value*cosLBAng+LCMag[idxLCM].value*cosLCAng_add240+LAMag[idxLAM].value*cosLAAng_add120)/3.0
            vnmag=np.sqrt(vnimagine**2+vnreal**2)
            vnang=np.degrees(math.atan2(vnimagine,vnreal))
            VnMag.append((LBMag[idxLBM].time, vnmag))
            VnAng.append((LBAng[idxLBA].time,vnang))
            
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
        # return V0 V+ V- 
        return[V0Ang,V0Mag,VpAng,VpMag,VnAng,VnMag,Vn_ubalance_seq,V0_ubalance_seq]
        
        
        
    
opts = { 'input_streams'  : ['upmu/switch_a6/C1ANG','upmu/switch_a6/C1MAG','upmu/switch_a6/C2ANG',
                            'upmu/switch_a6/C2MAG','upmu/switch_a6/C3ANG','upmu/switch_a6/C3MAG','upmu/grizzly_new/C1ANG'], \
         'input_uids'     : ['4072af6f-938e-450c-9927-37dee6968446','bf8ea2c0-6d04-4cdd-ba4b-0421eac0cabd',
                             'bf045a36-34df-4bee-a747-b20c3164723a','51d4801e-0bb6-4040-8e74-e7839be65156',
                             '8a5d0010-4665-4b59-ab6f-e7858c12284a','249b364d-b0a1-4b65-8aca-ffd68565c1de',
                             '4b7fec6d-270e-4bd6-b301-0eac6df17ca2'], \
         'start_date'     : '2014-12-03T00:00:00.000000', \
         'end_date'       : '2014-12-03T23:59:59.000000', \
         'output_streams' : ['CURRENT_ZERO_SEQ_ANG','CURRENT_ZERO_SEQ_MAG','CURRENT_POSITIVE_SEQ_ANG',
                             'CURRENT_POSITIVE_SEQ_MAG','CURRENT_NEGATIVE_SEQ_ANG','CURRENT_NEGATIVE_SEQ_MAG',
                             'CURRENT_UNBALANCE_NEG_SEQ','CURRENT_UNBALANCE_ZERO_SEQ'], \
         'output_units'   : ['Degree','V','Degree','V','Degree','V','Precent','Precent'], \
         'author'         : 'Refined Switch_a6', \
         'name'           : 'Sequence Components', \
         'version'        : 11, \
         'algorithm'      : compute }        
qdf.register(Distillate(), opts)
qdf.begin()

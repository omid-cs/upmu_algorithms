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
            sinLBAng_add120=np.sin(np.radians(LBAng[idxLBA].value+120-LAGAng[idxLAGA].value))
            sinLBAng_add240=np.sin(np.radians(LBAng[idxLBA].value+240-LAGAng[idxLAGA].value))
            sinLCAng_add120=np.sin(np.radians(LCAng[idxLCA].value+120-LAGAng[idxLAGA].value))
            sinLCAng_add240=np.sin(np.radians(LCAng[idxLCA].value+240-LAGAng[idxLAGA].value))
            
            # compute cosin value for three phase and cosin value for l2 and l3 anfter add 120 degree and 240 degree
            cosLAAng=np.cos(np.radians(LAAng[idxLAA].value-LAGAng[idxLAGA].value))
            cosLBAng=np.cos(np.radians(LBAng[idxLBA].value-LAGAng[idxLAGA].value))
            cosLCAng=np.cos(np.radians(LCAng[idxLCA].value-LAGAng[idxLAGA].value))
            cosLBAng_add120=np.cos(np.radians(LBAng[idxLBA].value+120-LAGAng[idxLAGA].value))
            cosLBAng_add240=np.cos(np.radians(LBAng[idxLBA].value+240-LAGAng[idxLAGA].value))
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
        
        
        
    
opts = { 'input_streams'  : ['upmu/switch_a6/L1ANG','upmu/switch_a6/L1MAG','upmu/switch_a6/L2ANG',
                            'upmu/switch_a6/L2MAG','upmu/switch_a6/L3ANG','upmu/switch_a6/L3MAG','upmu/grizzly_new/L1ANG'], \
         'input_uids'     : ['adf13e17-44b7-4ef6-ae3f-fde8a9152ab7','df64af25-a389-4be9-8061-f87c3616f286',
                             '4f56a8f1-f3ca-4684-930e-1b4d9955f72c','6e6ad513-ddd2-47fb-98c1-16e6477504fc',
                             '2c07ccef-20c5-4971-87cf-2c187ce5f722','bcf38098-0e16-46f2-a9fb-9ce481d7d55b',
                             'b4776088-2f85-4c75-90cd-7472a949a8fa'], \
         'start_date'     : '2014-12-03T00:00:00.000000', \
         'end_date'       : '2014-12-03T59:59:59.000000', \
         'output_streams' : ['VOLTAGE_ZERO_SEQ_ANG','VOLTAGE_ZERO_SEQ_MAG','VOLTAGE_POSITIVE_SEQ_ANG',
                             'VOLTAGE_POSITIVE_SEQ_MAG','VOLTAGE_NEGATIVE_SEQ_ANG','VOLTAGE_NEGATIVE_SEQ_MAG',
                             'VOLTAGE_UNBALANCE_NEG_SEQ','VOLTAGE_UNBALANCE_ZERO_SEQ'], \
         'output_units'   : ['Degree','V','Degree','V','Degree','V','Precent','Precent'], \
         'author'         : 'Refined Switch_a6', \
         'name'           : 'Sequence Components', \
         'version'        : 9, \
         'algorithm'      : compute }        
qdf.register(Distillate(), opts)
qdf.begin()

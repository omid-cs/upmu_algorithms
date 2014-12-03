from distillate import Distillate
import numpy as np
import math
import qdf

def compute(input_streams):
        # data input
        CBAng=input_streams[0]
        CBMag=input_streams[1]
        CCAng=input_streams[2]
        CCMag=input_streams[3]
        CAAng=input_streams[4]
        CAMag=input_streams[5]
        C0Ang=[]
        C0Mag=[]
        CpAng=[]
        CpMag=[]
        CnAng=[]
        CnMag=[]
        Cn_ubalance_seq=[]
        C0_ubalance_seq=[]
        idxCBA=0
        idxCBM=0
        idxCCA=0
        idxCCM=0
        idxCAA=0
        idxCAM=0
        
        # start repeat the computation above for current
        while idxCBA < len(CBAng) and idxCBM < len(CBMag) and idxCCA < len(CCAng) and idxCCM < len(CCMag) \
        and idxCAA < len(CAAng) and idxCAM < len(CAMag): 
            if CBAng[idxCBA].time < CCAng[idxCCA].time:
                idxCBA += 1
                continue
            if CBAng[idxCBA].time > CCAng[idxCCA].time:
                idxCCA += 1
                continue
            if CBAng[idxCBA].time < CAAng[idxCAA].time:
                idxCBA += 1
                continue
            if CBAng[idxCBA].time > CAAng[idxCAA].time:
                idxCAA += 1
                continue
            if CCAng[idxCCA].time < CAAng[idxCAA].time:
                idxCCA += 1
                continue
            if CCAng[idxCCA].time > CAAng[idxCAA].time:
                idxCAA += 1
                continue
            if CBMag[idxCBM].time < CCMag[idxCCM].time:
                idxCBM += 1
                continue
            if CBMag[idxCBM].time > CCMag[idxCCM].time:
                idxCCM += 1
                continue
            if CBMag[idxCBM].time < CAMag[idxCAM].time:
                idxCBM += 1
                continue
            if CBMag[idxCBM].time > CAMag[idxCAM].time:
                idxCAM += 1
                continue
            if CCMag[idxCCM].time < CAMag[idxCAM].time:
                idxCCM += 1
                continue
            if CCMag[idxCCM].time > CAMag[idxCAM].time:
                idxCAM += 1
                continue
            if CBMag[idxCBM].time < CBAng[idxCBA].time:
                idxCBM += 1
                continue
            if CBMag[idxCBM].time > CBAng[idxCBA].time:
                idxCBA += 1
                continue
            if CCMag[idxCCM].time < CCAng[idxCCA].time:
                idxCCM += 1
                continue
            if CCMag[idxCCM].time > CCAng[idxCCA].time:
                idxCCA += 1
                continue
            if CAMag[idxCAM].time < CAAng[idxCAA].time:
                idxCAM += 1
                continue
            if CAMag[idxCAM].time > CAAng[idxCAA].time:
                idxCAA += 1
                continue
            # compute sin value for three current and sin value for l2 and l3 anfter add 120 degree and 240 degree
            sinCAAng=np.sin(np.radians(CAAng[idxCAA].value-CAAng[idxCAA].value))
            sinCBAng=np.sin(np.radians(CBAng[idxCBA].value-CAAng[idxCAA].value))
            sinCCAng=np.sin(np.radians(CCAng[idxCCA].value-CAAng[idxCAA].value))
            sinCBAng_add120=np.sin(np.radians(CBAng[idxCBA].value+120-CAAng[idxCAA].value))
            sinCBAng_add240=np.sin(np.radians(CBAng[idxCBA].value+240-CAAng[idxCAA].value))
            sinCCAng_add120=np.sin(np.radians(CCAng[idxCCA].value+120-CAAng[idxCAA].value))
            sinCCAng_add240=np.sin(np.radians(CCAng[idxCCA].value+240-CAAng[idxCAA].value))
            
            # compute cosin value for three current and cosin value for l2 and l3 anfter add 120 degree and 240 degree
            cosCAAng=np.cos(np.radians(CAAng[idxCAA].value-CAAng[idxCAA].value))
            cosCBAng=np.cos(np.radians(CBAng[idxCBA].value-CAAng[idxCAA].value))
            cosCCAng=np.cos(np.radians(CCAng[idxCCA].value-CAAng[idxCAA].value))
            cosCBAng_add120=np.cos(np.radians(CBAng[idxCBA].value+120-CAAng[idxCAA].value))
            cosCBAng_add240=np.cos(np.radians(CBAng[idxCBA].value+240-CAAng[idxCAA].value))
            cosCCAng_add120=np.cos(np.radians(CCAng[idxCCA].value+120-CAAng[idxCAA].value))
            cosCCAng_add240=np.cos(np.radians(CCAng[idxCCA].value+240-CAAng[idxCAA].value))
            
            # compute balance C0
            c0imagine=(CAMag[idxCAM].value*sinCAAng+CBMag[idxCBM].value*sinCBAng+CCMag[idxCCM].value*sinCCAng)/3.0
            c0real=(CAMag[idxCAM].value*cosCAAng+CBMag[idxCBM].value*cosCBAng+CCMag[idxCCM].value*cosCCAng)/3.0
            c0mag=np.sqrt(c0imagine**2+c0real**2)
            c0ang=np.degrees(math.atan2(c0imagine,c0real))
            C0Mag.append((CAMag[idxCAM].time, c0mag))
            C0Ang.append((CAAng[idxCAA].time,c0ang))
            
            #compute balance C-
            cpimagine=(CAMag[idxCAM].value*sinCAAng+CBMag[idxCBM].value*sinCBAng_add120+CCMag[idxCCM].value*sinCCAng_add240)/3.0
            cpreal=(CAMag[idxCAM].value*cosCAAng+CBMag[idxCBM].value*cosCBAng_add120+CCMag[idxCCM].value*cosCCAng_add240)/3.0
            cpmag=np.sqrt(cpimagine**2+cpreal**2)
            cpang=np.degrees(math.atan2(cpimagine,cpreal))
            CpMag.append((CAMag[idxCAM].time, cpmag))
            CpAng.append((CAAng[idxCAA].time,cpang))
            
            # compute balance C+
            cnimagine=(CAMag[idxCAM].value*sinCAAng+CBMag[idxCBM].value*sinCBAng_add240+CCMag[idxCCM].value*sinCCAng_add120)/3.0
            cnreal=(CAMag[idxCAM].value*cosCAAng+CBMag[idxCBM].value*cosCBAng_add240+CCMag[idxCCM].value*cosCCAng_add120)/3.0
            cnmag=np.sqrt(cnimagine**2+cnreal**2)
            cnang=np.degrees(math.atan2(cnimagine,cnreal))
            CnMag.append((CAMag[idxCAM].time, cnmag))
            CnAng.append((CAAng[idxCAA].time,cnang))
            
            # compute unbalance C-
            Cn_ubalance_seq.append((CAMag[idxCAM].time,(cnmag/float(cpmag))*100))
            # compute unbalance C0
            C0_ubalance_seq.append((CAMag[idxCAM].time,(c0mag/float(cpmag))*100))
            
            idxCAA+= 1
            idxCAM+= 1
            idxCBA+= 1
            idxCBM+= 1
            idxCCA+= 1
            idxCCM+= 1
        
        ''' return C0, C+, C-, unbalance C neg seq, unbalance C zero seq,Totalp_dpf_seq'''
        return[C0Ang,C0Mag,CpAng,CpMag,CnAng,CnMag,Cn_ubalance_seq,C0_ubalance_seq]
        
        
        
    
opts = { 'input_streams'  : ['upmu/grizzly_new/C1ANG','upmu/grizzly_new/C1MAG','upmu/grizzly_new/C2ANG',
                             'upmu/grizzly_new/C2MAG','upmu/grizzly_new/C3ANG','upmu/grizzly_new/C3MAG'], \
         'input_uids'     : ['4b7fec6d-270e-4bd6-b301-0eac6df17ca2','425b9c51-9aba-4d1a-a677-85cd7afd6269',
                             '9ffeaf2a-46a9-465f-985d-96f84df66283','ca613e9a-1211-4c52-a98f-b8f9f1ce0672',
                             '8b40fe4c-36ee-4b10-8aef-1eef8c471e1d','b1025f33-97fd-45d6-bc0f-80132e1dc756'], \
         'start_date'     : '2014-10-07T02:00:00.000000', \
         'end_date'       : '2014-10-07T03:00:00.000000', \
         'output_streams' : ['CURRENT_ZERO_SEQ_ANG','CURRENT_ZERO_SEQ_MAG','CURRENT_POSITIVE_SEQ_ANG','CURRENT_POSITIVE_SEQ_MAG',
                             'CURRENT_NEGATIVE_SEQ_ANG','CURRENT_NEGATIVE_SEQ_MAG',
                             'CURRENT_UNBALANCE_NEG_SEQ','CURRENT_UNBALANCE_ZERO_SEQ '], \
         'output_units'   : ['Degree','Degree','Degree','Degree','Degree','Degree','Precent','Precent'], \
         'author'         : 'Refined Grizzly', \
         'name'           : 'Sequence Components', \
         'version'        : 3, \
         'algorithm'      : compute }        
qdf.register(Distillate(), opts)
qdf.begin()

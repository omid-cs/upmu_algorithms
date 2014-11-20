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
        CBAng=input_streams[6]
        CBMag=input_streams[7]
        CCAng=input_streams[8]
        CCMag=input_streams[9]
        CAAng=input_streams[10]
        CAMag=input_streams[11]
        V0Ang=[]
        V0Mag=[]
        VpAng=[]
        VpMag=[]
        VnAng=[]
        VnMag=[]
        Vn_ubalance_seq=[]
        V0_ubalance_seq=[]
        Totalp_dpf_seq=[]
        idxLBA=0
        idxLBM=0
        idxLCA=0
        idxLCM=0
        idxLAA=0
        idxLAM=0
        idxCBA=0
        idxCBM=0
        idxCCA=0
        idxCCM=0
        idxCAA=0
        idxCAM=0
        idxCT=0
        idxLT=0
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
            
            # compute balance V0
            v0imagine=(LAMag[idxLAM].value*sinLAAng+LBMag[idxLBM].value*sinLBAng+LCMag[idxLCM].value*sinLCAng)/3.0
            v0real=(LAMag[idxLAM].value*cosLAAng+LBMag[idxLBM].value*cosLBAng+LCMag[idxLCM].value*cosLCAng)/3.0
            v0mag=np.sqrt(v0imagine**2+v0real**2)
            v0ang=np.degrees(math.atan2(v0imagine,v0real))
            V0Mag.append((LAMag[idxLAM].time, v0mag))
            V0Ang.append((LAAng[idxLAA].time,v0ang))
            
            #compute balance v-
            vpimagine=(LAMag[idxLAM].value*sinLAAng+LBMag[idxLBM].value*sinLBAng_add120+LCMag[idxLCM].value*sinLCAng_add240)/3.0
            vpreal=(LAMag[idxLAM].value*cosLAAng+LBMag[idxLBM].value*cosLBAng_add120+LCMag[idxLCM].value*cosLCAng_add240)/3.0
            vpmag=np.sqrt(vpimagine**2+vpreal**2)
            vpang=np.degrees(math.atan2(vpimagine,vpreal))
            VpMag.append((LAMag[idxLAM].time, vpmag))
            VpAng.append((LAAng[idxLAA].time,vpang))
            
            # compute balance v+
            vnimagine=(LAMag[idxLAM].value*sinLAAng+LBMag[idxLBM].value*sinLBAng_add240+LCMag[idxLCM].value*sinLCAng_add120)/3.0
            vnreal=(LAMag[idxLAM].value*cosLAAng+LBMag[idxLBM].value*cosLBAng_add240+LCMag[idxLCM].value*cosLCAng_add120)/3.0
            vnmag=np.sqrt(vnimagine**2+vnreal**2)
            vnang=np.degrees(math.atan2(vnimagine,vnreal))
            VnMag.append((LAMag[idxLAM].time, vnmag))
            VnAng.append((LAAng[idxLAA].time,vnang))
            
            # compute unbalance V-
            Vn_ubalance_seq.append((LAMag[idxLAM].time,(vnmag/float(vpmag))*100))
            # compute unbalance v0
            V0_ubalance_seq.append((LAMag[idxLAM].time,(v0mag/float(vpmag))*100))
            
            idxLAA+= 1
            idxLAM+= 1
            idxLBA+= 1
            idxLBM+= 1
            idxLCA+= 1
            idxLCM+= 1
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
            cosCBAng=np.cos(np.radians(CBAng[idxLBA].value-CAAng[idxCAA].value))
            cosCCAng=np.cos(np.radians(CCAng[idxCCA].value-CAAng[idxCAA].value))
            cosCBAng_add120=np.cos(np.radians(CBAng[idxCBA].value+120-CAAng[idxCAA].value))
            cosCBAng_add240=np.cos(np.radians(CBAng[idxCBA].value+240-CAAng[idxCAA].value))
            cosCCAng_add120=np.cos(np.radians(CCAng[idxCCA].value+120-CAAng[idxCAA].value))
            cosCCAng_add240=np.cos(np.radians(CCAng[idxCCA].value+240-CAAng[idxCAA].value))
            
            # compute balance V0
            c0imagine=(CAMag[idxCAM].value*sinCAAng+CBMag[idxCBM].value*sinCBAng+CCMag[idxCCM].value*sinCCAng)/3.0
            c0real=(CAMag[idxCAM].value*cosCAAng+CBMag[idxCBM].value*cosCBAng+CCMag[idxCCM].value*cosCCAng)/3.0
            c0mag=np.sqrt(c0imagine**2+c0real**2)
            c0ang=np.degrees(math.atan2(c0imagine,c0real))
            C0Mag.append((CAMag[idxCAM].time, c0mag))
            C0Ang.append((CAAng[idxCAA].time,c0ang))
            
            #compute balance v-
            cpimagine=(CAMag[idxCAM].value*sinCAAng+CBMag[idxCBM].value*sinCBAng_add120+CCMag[idxCCM].value*sinCCAng_add240)/3.0
            cpreal=(CAMag[idxCAM].value*cosCAAng+CBMag[idxCBM].value*cosCBAng_add120+CCMag[idxCCM].value*cosCCAng_add240)/3.0
            cpmag=np.sqrt(cpimagine**2+cpreal**2)
            cpang=np.degrees(math.atan2(cpimagine,cpreal))
            CpMag.append((CAMag[idxCAM].time, cpmag))
            CpAng.append((CAAng[idxCAA].time,cpang))
            
            # compute balance v+
            cnimagine=(CAMag[idxCAM].value*sinCAAng+CBMag[idxCBM].value*sinCBAng_add240+CCMag[idxCCM].value*sinCCAng_add120)/3.0
            cnreal=(CAMag[idxCAM].value*cosCAAng+CBMag[idxCBM].value*cosCBAng_add240+CCMag[idxCCM].value*cosCCAng_add120)/3.0
            cnmag=np.sqrt(cnimagine**2+cnreal**2)
            cnang=np.degrees(math.atan2(cnimagine,cnreal))
            CnMag.append((CAMag[idxCAM].time, cnmag))
            CnAng.append((CAAng[idxCAA].time,cnang))
            
            # compute unbalance V-
            Cn_ubalance_seq.append((CAMag[idxCAM].time,(cnmag/float(cpmag))*100))
            # compute unbalance v0
            C0_ubalance_seq.append((CAMag[idxCAM].time,(c0mag/float(cpmag))*100))
            
            idxCAA+= 1
            idxCAM+= 1
            idxCBA+= 1
            idxCBM+= 1
            idxCCA+= 1
            idxCCM+= 1
        
        # comput Totalp_dpf_seq
        while idxCT < len(CpAng) and idxLT < len(VpAng):
            if CpAng[idxCT].time < VpAng[idxLT].time:
                idxCT += 1
                continue
            if CpAng[idxCT].time > VpAng[idxLT].time:
                idxLT += 1
                continue  
            total=np.cos(np.radians(VpAng[idxLT].value-CpAng[idxCT].value))
            Totalp_dpf_seq.append((CpAng[idxCT].time,total))
            idxLT+=1
            idxCT+=1
        ''' return V0, V+, V-, unbalance V neg seq, unbalance V zero seq
                   C0, C+, C-, unbalance C neg seq, unbalance C zero seq,Totalp_dpf_seq'''
        return[V0Ang,V0Mag,VpAng,VpMag,VnAng,VnMag,Vn_ubalance_seq,V0_ubalance_seq,
               C0Ang,C0Mag,CpAng,CpMag,CnAng,CnMag,Cn_ubalance_seq,C0_ubalance_seq,Totalp_dpf_seq]
        
        
        
    
opts = { 'input_streams'  : ['upmu/grizzly_new/L1ANG','upmu/grizzly_new/L1MAG','upmu/grizzly_new/L2ANG',
                             'upmu/grizzly_new/L2MAG','upmu/grizzly_new/L3ANG','upmu/grizzly_new/L3MAG',
                             'upmu/grizzly_new/C1ANG','upmu/grizzly_new/C1MAG','upmu/grizzly_new/C2ANG',
                             'upmu/grizzly_new/C2MAG','upmu/grizzly_new/C3ANG','upmu/grizzly_new/C3MAG'], \
         'input_uids'     : ['b4776088-2f85-4c75-90cd-7472a949a8fa','a64c386e-2dd4-4f17-96cb-1655358cb12c',
                             '8b80c070-7bb1-44d3-b3a8-301558d573ea','a002295a-32ee-41a1-8ec4-8657d0d1f943',
                             'b653c63b-4acc-45ee-ae3d-1602e6116bc1','db3ea4f7-a337-4874-baeb-17fc2c0cf18b'
                             '4b7fec6d-270e-4bd6-b301-0eac6df17ca2','425b9c51-9aba-4d1a-a677-85cd7afd6269'
                             '9ffeaf2a-46a9-465f-985d-96f84df66283','ca613e9a-1211-4c52-a98f-b8f9f1ce0672'
                             '8b40fe4c-36ee-4b10-8aef-1eef8c471e1d','b1025f33-97fd-45d6-bc0f-80132e1dc756'], \
         'start_date'     : '2014-10-01T00:00:00.000000', \
         'end_date'       : '2014-10-19T00:00:00.000000', \
         'output_streams' : ['grizzly_V0Ang','grizzly_V0Mag','grizzly_V+Ang','grizzly_V+Mag','grizzly_V-Ang','grizzly_V-Mag',
                             'grizzly_unbalance_Vneq_seq','grizzly_unbalance_Vzero_seq',
                             'grizzly_C0Ang','grizzly_C0Mag','grizzly_C+Ang','grizzly_C+Mag','grizzly_C-Ang','grizzly_C-Mag',
                             'grizzly_unbalance_Cneq_seq','grizzly_unbalance_Czero_seq','grizzly_totalp_dpf_seq'], \
         'output_units'   : ['Degree','V','Degree','V','Degree','V','Precent','Precent',
                             'Degree','V','Degree','V','Degree','V','Precent','Precent','Precent'], \
         'author'         : 'Andrew', \
         'name'           : 'Sequence_new', \
         'version'        : 10, \
         'algorithm'      : compute }        
qdf.register(Distillate(), opts)
qdf.begin()

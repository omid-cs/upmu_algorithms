from distillate import Distillate
import numpy as np
import qdf

def compute(input_streams):
        # data input
        LBMag = input_streams[0]
        CBMag=input_streams[1]
        LCMag=input_streams[2]
        CCMag=input_streams[3]
        LAMag=input_streams[4]
        CAMag=input_streams[5]
        DPF_A=input_streams[6]
        DPF_B=input_streams[7]
        DPF_C=input_streams[8]
        FUND_POWER_A=[]
        FUND_POWER_B=[]
        FUND_POWER_C=[]
        idxCA=0
        idxLA=0
        idxDA=0
        idxCB=0
        idxLB=0
        idxDB=0
        idxCC=0
        idxLC=0
        idxDC=0
        # matching time among all 6 data strams to make sure they are at same time before compute sequence
        while idxCA < len(CAMag) and idxLA < len(LAMag) and idxDA < len(DPF_A):
            if CAMag[idxCA].time < LAMag[idxLA].time:
                idxCA += 1
                continue
            if CAMag[idxCA].time > LAMag[idxLA].time:
                idxLA += 1
                continue
            if CAMag[idxCA].time < DPF_A[idxDA].time:
                idxCA += 1
                idxLA += 1
                continue
            if CAMag[idxCA].time > DPF_A[idxDA].time:
                idxDA += 1
                continue
           # compute FUND_POWER_A
            fpa=LAMag[idxLA].value*CAMag[idxCA].value*DPF_A[idxDA].value
            FUND_POWER_A.append((DPF_A[idxDA].time,fpa))
            idxCA+=1
            idxLA+=1
            idxDA+=1
            
        while idxCB < len(CBMag) and idxLB < len(LBMag) and idxDB < len(DPF_B):
            if CBMag[idxCB].time < LBMag[idxLB].time:
                idxCB += 1
                continue
            if CBMag[idxCB].time > LBMag[idxLB].time:
                idxLB += 1
                continue
            if CBMag[idxCB].time < DPF_B[idxDB].time:
                idxCB += 1
                idxLB += 1
                continue
            if CBMag[idxCB].time > DPF_B[idxDB].time:
                idxDB += 1
                continue
           # compute FUND_POWER_B
            fpb=LBMag[idxLB].value*CBMag[idxCB].value*DPF_B[idxDB].value
            FUND_POWER_B.append((DPF_B[idxDB].time,fpb))
            idxCB+=1
            idxLB+=1
            idxDB+=1
            
        while idxCC < len(CCMag) and idxLC < len(LCMag) and idxDC < len(DPF_C):
            if CCMag[idxCC].time < LCMag[idxLC].time:
                idxCC += 1
                continue
            if CCMag[idxCC].time > LCMag[idxLC].time:
                idxLC += 1
                continue
            if CCMag[idxCC].time < DPF_C[idxDC].time:
                idxCC += 1
                idxLC += 1
                continue
            if CCMag[idxCC].time > DPF_C[idxDC].time:
                idxDC += 1
                continue
           # compute FUND_POWER_C
            fpc=LCMag[idxLC].value*CCMag[idxCC].value*DPF_C[idxDC].value
            FUND_POWER_C.append((DPF_C[idxDC].time,fpc))
            idxCC+=1
            idxLC+=1
            idxDC+=1
            
        ''' FUND_POWER_A,FUND_POWER_B,FUND_POWER_C'''
        return[FUND_POWER_A,FUND_POWER_B,FUND_POWER_C]
        
        
        
    
opts = { 'input_streams'  : ['upmu/grizzly_new/L1MAG','upmu/grizzly_new/C1MAG','upmu/grizzly_new/L2MAG',
                             'upmu/grizzly_new/C2MAG','upmu/grizzly_new/L3MAG','upmu/grizzly_new/C3MAG',
                             'Refined Grizzly/Displacement Power Factor/L1_DPF','Refined Grizzly/Displacement Power Factor/L2_DPF',
                             'Refined Grizzly/Displacement Power Factor/L3_DPF'], \
         'input_uids'     : ['a64c386e-2dd4-4f17-96cb-1655358cb12c','425b9c51-9aba-4d1a-a677-85cd7afd6269',
                             'a002295a-32ee-41a1-8ec4-8657d0d1f943','ca613e9a-1211-4c52-a98f-b8f9f1ce0672',
                             'db3ea4f7-a337-4874-baeb-17fc2c0cf18b','b1025f33-97fd-45d6-bc0f-80132e1dc756',
                             '56f447e0-4fc5-4ff0-82e3-4eb2e1603849','171413d5-986c-4a6f-af93-30a3f4cbfb21',
                             'a4addc30-1438-446e-b6cf-744c63d83750'], \
         'start_date'     : '2014-12-03T12:00:00.000000', \
         'end_date'       : '2014-12-03T13:00:00.000000', \
         'output_streams' : ['FUND_POWER_L1','FUND_POWER_L2','FUND_POWER_L3'], \
         'output_units'   : ['Watts','Watts','Watts'], \
         'author'         : 'Refined Grizzly', \
         'name'           : 'Power Flow', \
         'version'        : 7, \
         'algorithm'      : compute }        
qdf.register(Distillate(), opts)
qdf.begin()

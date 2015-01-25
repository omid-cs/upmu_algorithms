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
        DPF_A=input_streams[8]
        DPF_B=input_streams[6]
        DPF_C=input_streams[7]
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
            fpa=LAMag[idxLA].value*CAMag[idxCA].value*DPF_A[idxDA].value/100.0
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
            fpb=LBMag[idxLB].value*CBMag[idxCB].value*DPF_B[idxDB].value/100.0
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
            fpc=LCMag[idxLC].value*CCMag[idxCC].value*DPF_C[idxDC].value/100.0
            FUND_POWER_C.append((DPF_C[idxDC].time,fpc))
            idxCC+=1
            idxLC+=1
            idxDC+=1
            
        ''' FUND_POWER_A,FUND_POWER_B,FUND_POWER_C'''
        return[FUND_POWER_A,FUND_POWER_B,FUND_POWER_C]
        
        
        
    
opts = { 'input_streams'  : ['upmu/bank_514/L1MAG','upmu/switch_a6/C1MAG','upmu/bank_514/L2MAG',
                             'upmu/bank_514/C2MAG','upmu/bank_514/L3MAG','upmu/bank_514/C3MAG',
                             'Calculated Bank_514/Displacement Power Factor/L1_DPF','Calculated Bank_514/Displacement Power Factor/L2_DPF',
                             'Calculated Bank_514/Displacement Power Factor/L3_DPF'], \
         'input_uids'     : ['3c73baa6-80ba-11e4-b1c9-002590e8ec24','3c73be2a-80ba-11e4-b1c9-002590e8ec24',
                             '3c73b70e-80ba-11e4-b1c9-002590e8ec24','3c73d4be-80ba-11e4-b1c9-002590e8ec24',
                             '3c73c1c2-80ba-11e4-b1c9-002590e8ec24','3c73d1b2-80ba-11e4-b1c9-002590e8ec24',
                             'dfe780c4-5468-4720-8e56-7b240320e981','d7fe8eb2-a9c2-4ef9-b9df-56ac30b919db',
                             '77b3054d-753e-4cbc-969f-c974ff14cf27'], \
         'start_date'     : '2014-12-12T12:00:00.000000', \
         'end_date'       : '2014-12-12T13:59:59.000000', \
         'output_streams' : ['FUND_POWER_L3','FUND_POWER_L1','FUND_POWER_L2'], \
         'output_units'   : ['Watts','Watts','Watts'], \
         'author'         : 'Calculated Bank_514', \
         'name'           : 'Power Flow', \
         'version'        : 19, \
         'algorithm'      : compute }        
qdf.register(Distillate(), opts)
qdf.begin()

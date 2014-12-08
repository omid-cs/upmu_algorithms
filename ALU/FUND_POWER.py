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
        
        
        
    
opts = { 'input_streams'  : ['upmu/switch_a6/L1MAG','upmu/switch_a6/C1MAG','upmu/switch_a6/L2MAG',
                             'upmu/switch_a6/C2MAG','upmu/switch_a6/L3MAG','upmu/switch_a6/C3MAG',
                             'Refined Switch_a6/Displacement Power Factor/L1_DPF','Refined Switch_a6/Displacement Power Factor/L2_DPF',
                             'Refined Switch_a6/Displacement Power Factor/L3_DPF'], \
         'input_uids'     : ['df64af25-a389-4be9-8061-f87c3616f286','bf8ea2c0-6d04-4cdd-ba4b-0421eac0cabd',
                             '6e6ad513-ddd2-47fb-98c1-16e6477504fc','51d4801e-0bb6-4040-8e74-e7839be65156',
                             'bcf38098-0e16-46f2-a9fb-9ce481d7d55b','249b364d-b0a1-4b65-8aca-ffd68565c1de',
                             '14e16f50-6ee3-4e7d-8eaa-53a89d49c0ef','d456eb31-1ced-4199-b252-16059cb8e0e0',
                             '1e1806c1-3baa-4942-99c5-52c724adfe80'], \
         'start_date'     : '2014-12-03T12:00:00.000000', \
         'end_date'       : '2014-12-03T13:00:00.000000', \
         'output_streams' : ['FUND_POWER_L1','FUND_POWER_L2','FUND_POWER_L3'], \
         'output_units'   : ['Watts','Watts','Watts'], \
         'author'         : 'Refined Switch_a6', \
         'name'           : 'Power Flow', \
         'version'        : 8, \
         'algorithm'      : compute }        
qdf.register(Distillate(), opts)
qdf.begin()

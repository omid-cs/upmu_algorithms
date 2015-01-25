from distillate import Distillate
import numpy as np
import math
import qdf


                             
def compute(input_streams):
        # data input
        LBAng = input_streams[0]
        LBMag = input_streams[1]
        CBAng=input_streams[2]
        CBMag=input_streams[3]
        LCAng=input_streams[4]
        LCMag=input_streams[5]
        CCAng=input_streams[6]
        CCMag=input_streams[7]
        LAAng=input_streams[8]
        LAMag=input_streams[9]
        CAAng=input_streams[10]
        CAMag=input_streams[11]
        Lstate=input_streams[12]
        VoltA_MAG=[]
        VoltA_ANG=[]
        VoltB_MAG=[]
        VoltB_ANG=[]
        VoltC_MAG=[]
        VoltC_ANG=[]
        CurrA_MAG=[]
        CurrA_ANG=[]
        CurrB_MAG=[]
        CurrB_ANG=[]
        CurrC_MAG=[]
        CurrC_ANG=[]
        LSTATE=[]
        idx=0
        while idx<len(LAMag):
          VoltA_MAG.append((LAMag[idx].time,LAMag[idx].value))
          idx+=1
        idx=0
        while idx<len(LAAng):
          VoltA_ANG.append((LAAng[idx].time,LAAng[idx].value))
          idx+=1
        idx=0
        while idx<len(LBMag):
          VoltB_MAG.append((LBMag[idx].time,LBMag[idx].value))
          idx+=1
        idx=0
        while idx<len(LBAng):
          VoltB_ANG.append((LBAng[idx].time,LBAng[idx].value))
          idx+=1
        idx=0
        while idx<len(LCMag):
          VoltC_MAG.append((LCMag[idx].time,LCMag[idx].value))
          idx+=1
        idx=0  
        while idx<len(LCAng):
          VoltC_ANG.append((LCAng[idx].time,LCAng[idx].value))
          idx+=1
        idx=0
        while idx<len(CAMag):
          CurrA_MAG.append((CAMag[idx].time,CAMag[idx].value))
          idx+=1
        idx=0
        while idx<len(CAAng):
          CurrA_ANG.append((CAAng[idx].time,CAAng[idx].value))
          idx+=1
        idx=0
        while idx<len(CBMag):
          CurrB_MAG.append((CBMag[idx].time,CBMag[idx].value))
          idx+=1
        idx=0
        while idx<len(CBAng):
          CurrB_ANG.append((CBAng[idx].time,CBAng[idx].value))
          idx+=1
        idx=0
        while idx<len(CCMag):
          VoltC_MAG.append((CCMag[idx].time,CCMag[idx].value))
          idx+=1
        idx=0
        while idx<len(CCAng):
          CurrC_ANG.append((CCAng[idx].time,CCAng[idx].value))
          idx+=1
        idx=0
        while idx<len(Lstate):
          LSTATE.append((Lstate[idx].time,Lstate[idx].value))
          idx+=1
        return[VoltA_MAG,VoltA_ANG,VoltB_MAG,VoltB_ANG,VoltC_MAG,VoltC_ANG,
               CurrA_MAG,CurrA_ANG,CurrB_MAG,CurrB_ANG,CurrC_MAG,CurrC_ANG,
                             LSTATE]
        
        
        
    
opts = { 'input_streams'  : ['upmu/switch_a6/L1ANG','upmu/switch_a6/L1MAG','upmu/switch_a6/C1ANG','upmu/switch_a6/C1MAG',
                             'upmu/switch_a6/L2ANG','upmu/switch_a6/L2MAG','upmu/switch_a6/C2ANG','upmu/switch_a6/C2MAG',
                             'upmu/switch_a6/L3ANG','upmu/switch_a6/L3MAG','upmu/switch_a6/C3ANG','upmu/switch_a6/C3MAG',
                             'upmu/switch_a6/LSTATE'], \
         'input_uids'     : ['adf13e17-44b7-4ef6-ae3f-fde8a9152ab7','df64af25-a389-4be9-8061-f87c3616f286',
                             '4072af6f-938e-450c-9927-37dee6968446','bf8ea2c0-6d04-4cdd-ba4b-0421eac0cabd',
                             '4f56a8f1-f3ca-4684-930e-1b4d9955f72c','6e6ad513-ddd2-47fb-98c1-16e6477504fc',
                             'bf045a36-34df-4bee-a747-b20c3164723a','51d4801e-0bb6-4040-8e74-e7839be65156',
                             '2c07ccef-20c5-4971-87cf-2c187ce5f722','bcf38098-0e16-46f2-a9fb-9ce481d7d55b',
                             '8a5d0010-4665-4b59-ab6f-e7858c12284a','249b364d-b0a1-4b65-8aca-ffd68565c1de',
                             '33eb7c04-6357-4de8-aa44-6f5a6abab7e6'], \
         'start_date'     : '2014-10-07T02:00:00.000000', \
         'end_date'       : '2014-10-07T03:00:00.000000', \
         'output_streams' : ['VoltA_MAG','VoltA_ANG','VoltB_MAG','VoltB_ANG','VoltC_MAG','VoltC_ANG',
                             'CurrA_MAG','CurrA_ANG','CurrB_MAG','CurrB_ANG','CurrC_MAG','CurrC_ANG',
                             'LSTATE'], \
         'output_units'   : ['v','deg','v','deg','v','deg','v','deg','v','deg','v','deg','bitmap'], \
         'author'         : 'Refined Switch_a6', \
         'name'           : 'Original Data', \
         'version'        : 3, \
         'algorithm'      : compute }        
qdf.register(Distillate(), opts)
qdf.begin()

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
        
        
        
    
opts = { 'input_streams'  : ['upmu/grizzly_new/L1ANG','upmu/grizzly_new/L1MAG','upmu/grizzly_new/C1ANG','upmu/grizzly_new/C1MAG',
                             'upmu/grizzly_new/L2ANG','upmu/grizzly_new/L2MAG','upmu/grizzly_new/C2ANG','upmu/grizzly_new/C2MAG',
                             'upmu/grizzly_new/L3ANG','upmu/grizzly_new/L3MAG','upmu/grizzly_new/C3ANG','upmu/grizzly_new/C3MAG',
                             'upmu/grizzly_new/LSTATE'], \
         'input_uids'     : ['b4776088-2f85-4c75-90cd-7472a949a8fa','a64c386e-2dd4-4f17-96cb-1655358cb12c',
                             '4b7fec6d-270e-4bd6-b301-0eac6df17ca2','425b9c51-9aba-4d1a-a677-85cd7afd6269',
                             '8b80c070-7bb1-44d3-b3a8-301558d573ea','a002295a-32ee-41a1-8ec4-8657d0d1f943',
                             '9ffeaf2a-46a9-465f-985d-96f84df66283','ca613e9a-1211-4c52-a98f-b8f9f1ce0672',
                             'b653c63b-4acc-45ee-ae3d-1602e6116bc1','db3ea4f7-a337-4874-baeb-17fc2c0cf18b',
                             '8b40fe4c-36ee-4b10-8aef-1eef8c471e1d','b1025f33-97fd-45d6-bc0f-80132e1dc756',
                             '89d1c0a1-aa97-4f5b-bdfb-0d04b1dc94f8'], \
         'start_date'     : '2014-10-07T02:00:00.000000', \
         'end_date'       : '2014-10-07T03:00:00.000000', \
         'output_streams' : ['VoltA_MAG','VoltA_ANG','VoltB_MAG','VoltB_ANG','VoltC_MAG','VoltC_ANG',
                             'CurrA_MAG','CurrA_ANG','CurrB_MAG','CurrB_ANG','CurrC_MAG','CurrC_ANG',
                             'LSTATE'], \
         'output_units'   : ['v','deg','v','deg','v','deg','v','deg','v','deg','v','deg','bitmap'], \
         'author'         : 'Refined Grizzly', \
         'name'           : 'Original Data', \
         'version'        : 2, \
         'algorithm'      : compute }        
qdf.register(Distillate(), opts)
qdf.begin()

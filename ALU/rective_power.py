from distillate import Distillate
import numpy as np
import math
import qdf


                             
def compute(input_streams):
        # data input
        LBAng = input_streams[0]
        CBAng=input_streams[1]
        LCAng=input_streams[2]
        CCAng=input_streams[3]
        LAAng=input_streams[4]
        CAAng=input_streams[5]
        DPF_A=[]
        DPF_B=[]
        DPF_C=[]
        idxCA=0
        idxLA=0
        idxCB=0
        idxLB=0
        idxCC=0
        idxLC=0
        # matching time among all 6 data strams to make sure they are at same time before compute sequence
        while idxCA < len(CAAng) and idxLA < len(LAAng):
            if CAAng[idxCA].time < LAAng[idxLA].time:
                idxCA += 1
                continue
            if CAAng[idxCA].time > LAAng[idxLA].time:
                idxLA += 1
                continue
           # compute cosin value of the differnece between voltage angle and current angle and dpf
            dpfa=(np.sin(np.radians(LAAng[idxLA].value-CAAng[idxCA].value)))*100
            DPF_A.append((LAAng[idxLA].time,dpfa))
            idxCA+=1
            idxLA+=1
            
        while idxCB < len(CBAng) and idxLB < len(LBAng):
            if CBAng[idxCB].time < LBAng[idxLB].time:
                idxCB += 1
                continue
            if CBAng[idxCB].time > LBAng[idxLB].time:
                idxLB += 1
                continue
           # compute cosin value of the differnece between voltage angle and current angle and dpf
            dpfb=(np.sin(np.radians(LBAng[idxLB].value-CBAng[idxCB].value)))*100
            DPF_B.append((LBAng[idxLB].time,dpfb))
            idxCB+=1
            idxLB+=1
            
        while idxCC < len(CCAng) and idxLC < len(LCAng):
            if CCAng[idxCC].time < LCAng[idxLC].time:
                idxCC += 1
                continue
            if CCAng[idxCC].time > LCAng[idxLC].time:
                idxLC += 1
                continue
           # compute cosin value of the differnece between voltage angle and current angle and dpf
            dpfc=(np.sin(np.radians(LCAng[idxLC].value-CCAng[idxCC].value)))*100
            DPF_C.append((LCAng[idxLC].time,dpfc))
            idxCC+=1
            idxLC+=1
            
        ''' DPF_A,DPF_B,DPF_C'''
        return[DPF_A,DPF_B,DPF_C]
        
        
        
    
opts = { 'input_streams'  : ['upmu/switch_a6/L1ANG','upmu/switch_a6/C1ANG','upmu/switch_a6/L2ANG',
                             'upmu/switch_a6/C2ANG','upmu/switch_a6/L3ANG','upmu/switch_a6/C3ANG'], \
         'input_uids'     : ['adf13e17-44b7-4ef6-ae3f-fde8a9152ab7','4072af6f-938e-450c-9927-37dee6968446',
                             '4f56a8f1-f3ca-4684-930e-1b4d9955f72c','bf045a36-34df-4bee-a747-b20c3164723a',
                             '2c07ccef-20c5-4971-87cf-2c187ce5f722','8a5d0010-4665-4b59-ab6f-e7858c12284a'], \
         'start_date'     : '2014-12-03T00:00:00.000000', \
         'end_date'       : '2014-12-03T23:59:59.000000', \
         'output_streams' : ['L3_Rective_power','L1_Rective_power','L2_Rective_power'], \
         'output_units'   : ['Precent','Precent','Precent'], \
         'author'         : 'Andrew', \
         'name'           : 'Reactive power', \
         'version'        : 3, \
         'algorithm'      : compute }        
qdf.register(Distillate(), opts)
qdf.begin()

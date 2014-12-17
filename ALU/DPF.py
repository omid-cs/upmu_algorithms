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
            dpfa=(np.cos(np.radians(LAAng[idxLA].value-CAAng[idxCA].value)))*100
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
            dpfb=(np.cos(np.radians(LBAng[idxLB].value-CBAng[idxCB].value)))*100
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
            dpfc=(np.cos(np.radians(LCAng[idxLC].value-CCAng[idxCC].value)))*100
            DPF_C.append((LCAng[idxLC].time,dpfc))
            idxCC+=1
            idxLC+=1
            
        ''' DPF_A,DPF_B,DPF_C'''
        return[DPF_A,DPF_B,DPF_C]
        
        
        
    
opts = { 'input_streams'  : ['upmu/bank_514/L1ANG','upmu/bank_514/C1ANG','upmu/bank_514/L2ANG',
                             'upmu/bank_514/C2ANG','upmu/bank_514/L3ANG','upmu/bank_514/C3ANG'], \
         'input_uids'     : ['3c73d7ca-80ba-11e4-b1c9-002590e8ec24','3c73c866-80ba-11e4-b1c9-002590e8ec24',
                             '3c73cb86-80ba-11e4-b1c9-002590e8ec24','3c73ce92-80ba-11e4-b1c9-002590e8ec24',
                             '3c73af34-80ba-11e4-b1c9-002590e8ec24','3c73c514-80ba-11e4-b1c9-002590e8ec24'], \
         'start_date'     : '2014-12-12T12:00:00.000000', \
         'end_date'       : '2014-12-12T13:59:59.000000', \
         'output_streams' : ['L3_DPF','L1_DPF','L2_DPF'], \
         'output_units'   : ['Precent','Precent','Precent'], \
         'author'         : 'Calculated Bank_514', \
         'name'           : 'Displacement Power Factor', \
         'version'        : 16, \
         'algorithm'      : compute }        
qdf.register(Distillate(), opts)
qdf.begin()

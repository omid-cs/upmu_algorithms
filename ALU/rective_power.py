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
        
        
        
    
opts = { 'input_streams'  : ['upmu/grizzly_new/L1ANG','upmu/grizzly_new/C1ANG','upmu/grizzly_new/L2ANG',
                             'upmu/grizzly_new/C2ANG','upmu/grizzly_new/L3ANG','upmu/grizzly_new/C3ANG'], \
         'input_uids'     : ['b4776088-2f85-4c75-90cd-7472a949a8fa','4b7fec6d-270e-4bd6-b301-0eac6df17ca2',
                             '8b80c070-7bb1-44d3-b3a8-301558d573ea','9ffeaf2a-46a9-465f-985d-96f84df66283',
                             'b653c63b-4acc-45ee-ae3d-1602e6116bc1','8b40fe4c-36ee-4b10-8aef-1eef8c471e1d'], \
         'start_date'     : '2014-12-03T00:00:00.000000', \
         'end_date'       : '2014-12-03T23:59:59.000000', \
         'output_streams' : ['L3_Rective_power','L1_Rective_power','L2_Rective_power'], \
         'output_units'   : ['Precent','Precent','Precent'], \
         'author'         : 'Andrew', \
         'name'           : 'Reactive power_g', \
         'version'        : 4, \
         'algorithm'      : compute }        
qdf.register(Distillate(), opts)
qdf.begin()

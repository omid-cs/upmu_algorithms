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
        
        return[CAAng,LAAng,CBAng]
        
        
        
    
opts = { 'input_streams'  : ['upmu/grizzly_new/L1ANG','upmu/grizzly_new/C1ANG','upmu/grizzly_new/L2ANG',
                             'upmu/grizzly_new/C2ANG','upmu/grizzly_new/L3ANG','upmu/grizzly_new/C3ANG'], \
         'input_uids'     : ['b4776088-2f85-4c75-90cd-7472a949a8fa','4b7fec6d-270e-4bd6-b301-0eac6df17ca2',
                             '8b80c070-7bb1-44d3-b3a8-301558d573ea','9ffeaf2a-46a9-465f-985d-96f84df66283',
                             'b653c63b-4acc-45ee-ae3d-1602e6116bc1','8b40fe4c-36ee-4b10-8aef-1eef8c471e1d'], \
         'start_date'     : '2014-10-01T00:00:00.000000', \
         'end_date'       : '2014-10-19T00:00:00.000000', \
         'output_streams' : ['CAANG','LAANG','CBANG'], \
         'output_units'   : ['Precent','Precent','Precent'], \
         'author'         : 'Andrew', \
         'name'           : 'lebel', \
         'version'        : 1, \
         'algorithm'      : compute }        
qdf.register(Distillate(), opts)
qdf.begin()

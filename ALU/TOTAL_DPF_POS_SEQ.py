from distillate import Distillate
import numpy as np
import math
import qdf

def compute(input_streams):
        # data input
        VpAng=input_streams[0]
        CpAng=input_streams[1]
        Total_dpf_pos_seq=[]
        idxVp=0
        idxCp=0
        
        # time matching
        while idxVp < len(VpAng) and idxCp < len(CpAng):
            if VpAng[idxVp].time < CpAng[idxCp].time:
                idxVp += 1
                continue
            if VpAng[idxVp].time < CpAng[idxCp].time:
                idxCp += 1
                continue
            
            # compute Total_dpf_pos_seq
            total=np.cos(np.radians(VpAng[idxVp].value-CpAng[idxCp].value))
            Total_dpf_pos_seq.append((VpAng[idxVp].time,total))
            
            idxVp+= 1
            idxCp+= 1
        
        ''' return Totalp_dpf_seq'''
        return[Total_dpf_pos_seq]
        
        
        
    
opts = { 'input_streams'  : ['Distillate/Andrew/Sequence_new/grizzly_V+Ang','Distillate/Andrew/Sequence_new/grizzly_C+Ang'], \
         'input_uids'     : ['55ec9d08-887d-4626-bba1-0be2a5e6d08f','91d5d281-c796-4f86-a75d-47d1ed137501'], \
         'start_date'     : '2014-10-01T00:00:00.000000', \
         'end_date'       : '2014-10-19T00:00:00.000000', \
         'output_streams' : ['grizzly_totalp_dpf_seq'], \
         'output_units'   : ['Precent'], \
         'author'         : 'Andrew', \
         'name'           : 'Sequence_new', \
         'version'        : 1, \
         'algorithm'      : compute }        
qdf.register(Distillate(), opts)
qdf.begin()

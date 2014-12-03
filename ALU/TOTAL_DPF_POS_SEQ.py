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
        
        
        
    
opts = { 'input_streams'  : ['Refined Grizzly/Sequence Components/VOLTAGE _POSITIVE_SEQ_ANG',
                             'Refined Grizzly/Sequence Components/CURRENT_POSITIVE_SEQ_ANG'], \
         'input_uids'     : ['8ac16cac-f935-42bd-a375-ed7c74a89913','ee3ad881-09fe-4ad0-ae02-44a9555c1600'], \
         'start_date'     : '2014-10-07T02:00:00.000000', \
         'end_date'       : '2014-10-07T03:00:00.000000', \
         'output_streams' : ['TOTAL_DPF_POS_SEQ'], \
         'output_units'   : ['Precent'], \
         'author'         : 'Refined Grizzly', \
         'name'           : 'Sequence Components', \
         'version'        : 2, \
         'algorithm'      : compute }        
qdf.register(Distillate(), opts)
qdf.begin()

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
        
        
        
    
opts = { 'input_streams'  : ['Refined Switch_a6/Sequence Components/VOLTAGE _POSITIVE_SEQ_ANG',
                             'Refined Switch_a6/Sequence Components/CURRENT_POSITIVE_SEQ_ANG'], \
         'input_uids'     : ['491a1f4f-3ebc-47de-ae18-8ebc0afe036d','feb3ae36-16f2-4a71-8f86-375c3c1b9c9f'], \
         'start_date'     : '2014-10-07T02:00:00.000000', \
         'end_date'       : '2014-10-07T03:00:00.000000', \
         'output_streams' : ['TOTAL_DPF_POS_SEQ'], \
         'output_units'   : ['Precent'], \
         'author'         : 'Refined Switch_a6', \
         'name'           : 'Sequence Components', \
         'version'        : 4, \
         'algorithm'      : compute }        
qdf.register(Distillate(), opts)
qdf.begin()

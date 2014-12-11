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
        
        
        
    
opts = { 'input_streams'  : ['Refined Switch_a6/Sequence Components/VOLTAGE_POSITIVE_SEQ_ANG',
                             'Refined Switch_a6/Sequence Components/CURRENT_POSITIVE_SEQ_ANG'], \
         'input_uids'     : ['978ffd60-f4ed-4d29-a13d-882f3f0196ff','5cfb3c7c-161e-46d1-b39b-e1a30c3e558e'], \
         'start_date'     : '2014-12-03T00:00:00.000000', \
         'end_date'       : '2014-12-03T11:59:59.000000', \
         'output_streams' : ['TOTAL_DPF_POS_SEQ'], \
         'output_units'   : ['Precent'], \
         'author'         : 'Refined Switch_a6', \
         'name'           : 'Sequence Components', \
         'version'        : 14, \
         'algorithm'      : compute }        
qdf.register(Distillate(), opts)
qdf.begin()

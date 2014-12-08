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
        
        
        
    
opts = { 'input_streams'  : ['Refined Grizzly/Sequence Components/VOLTAGE_POSITIVE_SEQ_ANG',
                             'Refined Grizzly/Sequence Components/CURRENT_POSITIVE_SEQ_ANG'], \
         'input_uids'     : ['3ec9622e-4dfb-437b-98af-d0d9ed825a21','4d480922-819d-462d-b814-38d9ba0f53ed'], \
         'start_date'     : '2014-12-03T12:00:00.000000', \
         'end_date'       : '2014-12-03T13:00:00.000000', \
         'output_streams' : ['TOTAL_DPF_POS_SEQ'], \
         'output_units'   : ['Precent'], \
         'author'         : 'Refined Grizzly', \
         'name'           : 'Sequence Components', \
         'version'        : 8, \
         'algorithm'      : compute }        
qdf.register(Distillate(), opts)
qdf.begin()

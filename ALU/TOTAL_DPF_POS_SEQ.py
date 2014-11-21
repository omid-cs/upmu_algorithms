from distillate import Distillate
import numpy as np
import math
import qdf

def compute(input_streams):
        # data input
        V0Ang=input_streams[0]
        C0Ang=input_streams[1]
        Total_dpf_pos_seq=[]
        idxV0=0
        idxC0=0
        
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
        
        
        
    
opts = { 'input_streams'  : ['Distillate/Andrew/Sequence_new/grizzly_V0Ang','Distillate/Andrew/Sequence_new/grizzly_C0Ang'], \
         'input_uids'     : ['f8b5154b-fdc5-4b0a-82cb-bcc04b28adad','bee7fd99-e292-42da-a89f-af57dd32ce59'], \
         'start_date'     : '2014-10-01T00:00:00.000000', \
         'end_date'       : '2014-10-19T00:00:00.000000', \
         'output_streams' : [], \
         'output_units'   : ['Precent'], \
         'author'         : 'Andrew', \
         'name'           : 'Sequence_new', \
         'version'        : 1, \
         'algorithm'      : compute }        
qdf.register(Distillate(), opts)
qdf.begin()

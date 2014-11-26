import numpy as np
import math
def DPF(input_streams):
  Input=[]
  Output=[]
  i=0
  while i<len(input_streams):
        Input.append(input_streams[i])
        i=+1
  interaction=0
  stream_number=0
  while interaction<(len(input_streams)/2):
        out=[]
        idxC=0
        idxL=0
        while idxC < len(Input[stream_number]) and idxL < len(Input[stream_number+1]):
            if Input[stream_number].time < Input[stream_number+1].time:
                idxC += 1
                continue
            if Input[stream_number].time > Input[stream_number+1].time:
                idxL += 1
                continue
           # compute cosin value of the differnece between voltage angle and current angle and dpf
            dpf=(np.cos(np.radians(Input[stream_number+1].value-Input[stream_number].value)))*100
            out.append((Input[stream_number].time,dpf))
            idxC+=1
            idxL+=1
        Out.append(out) 
        interaction+=1
        stream_number+=2
  return Out[0],Out[1],Out[2]

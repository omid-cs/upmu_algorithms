import qdf
from distillate import Distillate

def scale(input_streams):
  # only one input stream
  input_values = input_streams[0]
  
  scale_factor = 1.2

  scaled_values = []
  i = 0
  while i < len(input_values):
    scaled_value = input_values[i].value * scale_factor
    scaled_values.append((input_values[i].time, scaled_value))
    i += 1

  return [scaled_values]

opts = { 'input_streams'  : ['upmu/grizzly_new/L1MAG'], \
         'input_uids'     : ['a64c386e-2dd4-4f17-96cb-1655358cb12c'], \
         'start_date'     : '2014-08-28T00:00:00.000000', \
         'end_date'       : '2014-08-28T02:00:00.000000', \
         'output_streams' : ['grizzly_new_L1Mag_scale_1.2'], \
         'output_units'   : ['V'], \
         'author'         : 'CAB', \
         'name'           : 'dev_scale', \
         'version'        : 1, \
         'algorithm'      : scale }
qdf.register(Distillate(), opts)
qdf.begin()

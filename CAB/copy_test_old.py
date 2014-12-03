import qdf
from distillate import Distillate

def scale(input_streams):
  # only one input stream
  input_values = input_streams[0]
  
  i = 0
  while i < len(input_values):
    scaled_values.append((input_values[i].time, input_values[i].value))
    i += 1

  return [scaled_values]

opts = { 'input_streams'  : ['B71_L2ANG'],
         'input_uids'     : ['f89e77a8-661e-49d2-a868-2071c1fae238'],
         'start_date'     : '2014-10-01T00:00:00.000000',
         'end_date'       : '2014-10-01T01:00:00.000000',
         'output_streams' : ['B71_L2ANG_copy_old'],
         'output_units'   : ['Degrees'],
         'author'         : 'CAB',
         'name'           : 'dev_copy_old',
         'version'        : 1,
         'algorithm'      : scale }
qdf.register(Distillate(), opts)
qdf.begin()

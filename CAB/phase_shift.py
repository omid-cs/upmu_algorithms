import qdf
from distillate import Distillate

def scale(input_streams):
  # only one input stream
  input_values = input_streams[0]
  
  shift_amount = 180 

  shifted_values = []
  i = 0
  while i < len(input_values):
    shifted_value = input_values[i].value + shift_amount
    if shifted_value > 360:
      shifted_value -= 360
    shifted_values.append((input_values[i].time, shifted_value))
    i += 1

  return [shifted_values]

opts = { 'input_streams'  : ['upmu/grizzly_new/L1ANG'],
         'input_uids'     : ['b4776088-2f85-4c75-90cd-7472a949a8fa'],
         'start_date'     : '2014-12-01T00:00:00.000000',
         'end_date'       : '2014-12-01T02:00:00.000000',
         'output_streams' : ['grizzly_new_L1ANG_shift_180'],
         'output_units'   : ['Degrees'],
         'author'         : 'CAB',
         'name'           : 'dev_phase_shift',
         'version'        : 1,
         'algorithm'      : scale }
qdf.register(Distillate(), opts)
qdf.begin()

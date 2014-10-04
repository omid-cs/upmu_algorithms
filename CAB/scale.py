import qdf
from distillate import Distillate

def scale(input_streams, output_streams):
  # only one input stream
  input_values = input_streams[0]
  
  # only one output stream
  output_stream = output_streams[0]
  
  scale_factor = 9

  scaled_values = []
  i = 0
  while i < len(input_values):
    scaled_value = input_values[i].value * scale_factor
    scaled_values.append((input_values[i].time, scaled_value))
    if len(scaled_values) >= qdf.OPTIMAL_BATCH_SIZE:
      yield (scaled_values, False)
      scaled_values = []
    i += 1

  yield (scaled_values, True)

opts = { 'input_streams'  : ['upmu/grizzly_new/L1MAG'], \
         'input_uids'     : ['a64c386e-2dd4-4f17-96cb-1655358cb12c'], \
         'start_date'     : '2014-09-07T00:00:00.000000', \
         'end_date'       : '2014-09-07T00:40:00.000000', \
         'output_streams' : ['grizzly_new_L1Mag_scale_9.0'], \
         'output_units'   : ['V'], \
         'author'         : 'CAB', \
         'name'           : 'Scale', \
         'version'        : 9.0, \
         'algorithm'      : scale }
qdf.register(Distillate(), opts)
qdf.begin()

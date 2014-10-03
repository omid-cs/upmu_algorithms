import qdf
from distillate import Distillate

def scale(input_streams, output_streams):
  # only one input stream
  input_values = input_streams[0]
  
  # only one output stream
  output_stream = output_streams[0]

  scaled_values = []
  i = 0
  while i < len(input_values):
    scaled_value = input_values[i].value * self.scale_factor
    scaled_values.append((input_values[i].time, scaled_value))
    if len(scaled_values) >= qdf.OPTIMAL_BATCH_SIZE:
      yield self.stream_insert_multiple(self.output_stream, scaled_values)
      scaled_values = []
    i += 1

  yield self.stream_insert_multiple(self.output_stream, scaled_values)  

opts = { 'input_streams'  : ['L1MAG'], \
         'input_uids'     : ['abffcf07-9e17-404a-98c3-ea4d60042ff3'], \
         'start_dates'    : ['2014-09-07T00:00:00.000000'], \
         'end_dates'      : ['2014-09-08T00:00:00.000000'], \
         'output_streams' : ['soda_a_L1MAG_6.0'], \
         'output_units'   : ['V'], \
         'scale_factor'   : 6.0, \
         'version'        : 5, \
         'algorithm'      : scale }
qdf.register(Distillate(), opts)
qdf.begin()

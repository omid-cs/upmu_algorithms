import qdf
from distillate import Distillate

def algorithm(input_streams):
  first_input_stream = input_streams[0]
  second_input_stream = input_streams[1]
  third_input_stream = input_streams[2]

  first_output_stream = []
  second_output_stream = []
  
  """
    This example algorithm calculates the minimum and maximium of each input stream.
      - first_output_stream: min values
      - second_output_stream: max values
    It naively assumes that all streams are in synch (no dropped or extra points in the stream)
  """
  i = 0
  while i<len(first_input_stream) or i<len(second_input_stream) or i<len(third_input_stream):
    time = first_input_stream[i].time

    x1 = first_input_stream[i].value
    x2 = second_input_stream[i].value
    x3 = third_input_stream[i].value

    min_x = min(x1, x2, x3)
    max_x = max(x1, x2, x3)
    
    first_output_stream.append((time, min_x))
    second_output_stream.append((time, max_x))

    i += 1
  return [freqs]

opts = { 'input_streams'  : ['in1', 'in2', 'in3'],
         'input_uids'     : ['00000000-0000-0000-0000-000000000000', \
                             '00000000-0000-0000-0000-000000000000', \
                             '00000000-0000-0000-0000-000000000000'],
         'start_date'     : '2014-10-06T00:00:00.000000',
         'end_date'       : '2014-10-06T02:30:00.000000',
         'output_streams' : ['out1, out2, out3'],
         'output_units'   : ['Unit', 'Unit', 'Unit'],
         'author'         : 'CAB',
         'name'           : 'New Output Frequency',
         'version'        : 6,
         'algorithm'      : algorithm}
qdf.register(Distillate(), opts)
qdf.begin()

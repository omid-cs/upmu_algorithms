import qdf
from distillate_new import Distillate
from twisted.internet import defer

@defer.inlineCallbacks
def frequency(input_streams, output_streams):
  # only one input stream
  input_stream = input_streams[0]

  # only one output stream
  output_stream = output_streams[0]

  sampling_freq = input_stream.sampling_freq #Hz
  delta_time = 1 #second

  i = 0
  while i + sampling_freq*delta_time < len(input_stream):
    point1 = yield input_stream[i]
    point2 = yield input_stream[i+sampling_freq*delta_time]
    if point1 == None or point2 == None:
      i += 1
      continue
    phase_diff = point2.value - point1.value
    if phase_diff > 180:
      phase_diff -= 360
    elif phase_diff < -180:
      phase_diff += 360
    is_full = output_stream.append((point1.time, (phase_diff/delta_time)/360 + 60))
    if is_full:
      yield output_stream.flush()
    i += 1

opts = { 'input_streams'  : ['grizzly_new_L2ANG'],
         'input_uids'     : ['8b80c070-7bb1-44d3-b3a8-301558d573ea'],
         'start_dates'    : ['2014-12-01T00:00:00.000000'],
         'end_dates'      : ['2014-12-02T00:00:00.000000'],
         'output_streams' : ['grizzly_new_L2ANG_freq'],
         'output_units'   : ['Hz'],
         'author'         : 'CAB',
         'name'           : 'dev_freq_new',
         'version'        : 5,
         'algorithm'      : frequency }
qdf.register(Distillate(), opts)
qdf.begin()

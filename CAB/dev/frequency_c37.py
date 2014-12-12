import qdf
from distillate_new import Distillate
from twisted.internet import defer

@defer.inlineCallbacks
def frequency_c37(input_streams, output_streams):
  # only one input stream
  input_stream = input_streams[0]

  # only one output stream
  output_stream = output_streams[0]

  sampling_freq = input_stream.sampling_freq

  i = 0
  while i + 3 < len(input_stream):
    point1 = yield input_stream[i]
    point2 = yield input_stream[i+1]
    point3 = yield input_stream[i+2]
    point4 = yield input_stream[i+3]
    if point1 == None or point2 == None or point3 == None:
      i += 1
      continue
    # adjust values for wrapping
    v1 = angle_diff(point3.value, point4.value)
    v2 = angle_diff(point2.value, point3.value)
    v3 = angle_diff(point1.value, point2.value)

    frequency = NOMINAL_FREQUENCY+((sampling_freq/360.0)*(6.0*(v1)+3.0*(v2)+0.1*(v3)))
    
    is_full = output_stream.append((point4.time, frequency))
    if is_full:
      yield output_stream.flush()
    i += 1

def angle_diff(v1, v2):
  # assumes angles wrap from
  phase_diff = v2-v1
  if phase_diff > 180:
      phase_diff -= 360
  elif phase_diff < -180:
      phase_diff += 360
  return phase_diff

opts = { 'input_streams'  : ['grizzly_new_L2ANG'],
         'input_uids'     : ['8b80c070-7bb1-44d3-b3a8-301558d573ea'],
         'start_dates'    : ['2014-12-01T00:00:00.000000'],
         'end_dates'      : ['2014-12-02T00:00:00.000000'],
         'output_streams' : ['grizzly_new_L2ANG_freq'],
         'output_units'   : ['Hz'],
         'author'         : 'CAB',
         'name'           : 'dev_freq_c37',
         'version'        : 1,
         'algorithm'      : frequency_c37 }
qdf.register(Distillate(), opts)
qdf.begin()

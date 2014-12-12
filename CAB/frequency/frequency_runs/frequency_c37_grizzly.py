import qdf
from distillate import Distillate
from twisted.internet import defer

NOMINAL_FREQUENCY = 60 #hz

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
    if point1 == None or point2 == None or point3 == None or point4 == None:
      i += 1
      continue
    # adjust values for wrapping
    v1 = angle_diff(point3.value, point4.value)
    v2 = angle_diff(point2.value, point3.value)
    v3 = angle_diff(point1.value, point2.value)

    frequency = NOMINAL_FREQUENCY+((sampling_freq/360.0)*(6.0*(v1)+3.0*(v2)+1.0*(v3))/10)
    
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

opts = { 'input_streams'  : ['grizzly_new_L1ANG'],
         'input_uids'     : ['b4776088-2f85-4c75-90cd-7472a949a8fa'],
         'start_dates'    : ['2014-12-03T00:00:00.000000'],
         'end_dates'      : ['2014-12-04T00:00:00.000000'],
         'output_streams' : ['grizzly_new_L1ANG_freq_c37'],
         'output_units'   : ['Hz'],
         'author'         : 'Calculated Grizzly',
         'name'           : 'FREQ_C37',
         'version'        : 1,
         'algorithm'      : frequency_c37 }
qdf.register(Distillate(), opts)
qdf.begin()

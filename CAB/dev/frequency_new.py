import qdf
from distillate import Distillate

def frequency(input_streams):
  # only one stream
  input_points_capnp = input_streams[0]
  
  sampling_freq = 60 #Hz

  freqs = []
  
  i = 0
  while i < len(input_points)-sampling_freq:
    delta_samples = sampling_freq #upper bound, does not account for double-values
    t1 = input_points[i].time
    t2 = input_points[i+delta_samples].time
    while ((t2 - t1) > 1e9 and t2 > t1): #catch zeroed or missing samples
      delta_samples -= 1 #decrement ~one sample per missing sample in interval
      t2 = input_points[i+delta_samples].time
    if t2 - t1 < 1e9: #if sample 1 second from now is missing, skip
      i += 1
      continue
    x1 = input_points[i].value
    x2 = input_points[i+delta_samples].value
    phase_diff = x2 - x1
    delta_time = t2 - t1
    if phase_diff > 180:
      phase_diff -= 360
    elif phase_diff < -180:
      phase_diff += 360
    freqs.append((t2, (phase_diff/delta_time)*1e9/360 + 60))
    i += 1

  #save trailing values for next batch
  overflow_points = []
  for i in range(len(input_points)-sampling_freq, len(input_points)):
    overflow_points.append(input_points[i])
  return [freqs]

opts = { 'input_streams'  : ['upmu/grizzly_new/L2ANG'], \
         'input_uids'     : ['8b80c070-7bb1-44d3-b3a8-301558d573ea'], \
         'start_date'     : '2014-10-01T00:00:00.000000', \
         'output_streams' : ['grizzly_new_L2Ang_frequency'], \
         'output_units'   : ['Hz'], \
         'author'         : 'CAB', \
         'name'           : 'Test2', \
         'version'        : 1, \
         'algorithm'      : frequency }
qdf.register(Distillate(), opts)
qdf.begin()

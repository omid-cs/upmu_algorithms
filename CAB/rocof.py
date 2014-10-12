import qdf
from distillate import Distillate

overflow_points = []

def frequency(input_streams):
  global overflow_points
  
  # only one stream
  input_points_capnp = input_streams[0]
  
  # convert input_points to an array and prepend overflow_points
  # TEMP: naive solution, find better one!
  input_points = overflow_points
  for point in input_points_capnp:
    input_points.append(point)
    

  sampling_freq = 120 #Hz

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
    diff = x2 - x1
    delta_time = t2 - t1
    freqs.append((t1, (diff/delta_time)*1e9))
    i += 1

 return freqs

opts = { 'input_streams'  : ['grizzly_new_L1Ang_freq'], \
         'input_uids'     : ['f6b24d9a-167f-4eed-8873-2ba577dcca6b'], \
         'start_date'     : '2014-08-28T00:00:00.000000', \
         'end_date'       : '2014-08-28T02:00:00.000000', \
         'output_streams' : ['grizzly_new_L2Ang_rocof'], \
         'output_units'   : ['Hz/s'], \
         'author'         : 'CAB', \
         'name'           : 'Test1', \
         'version'        : 4, \
         'algorithm'      : frequency }
qdf.register(Distillate(), opts)
qdf.begin()

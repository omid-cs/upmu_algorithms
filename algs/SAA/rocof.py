import qdf
from distillate import Distillate

overflow_points = []

class Rocof(input_streams):

  def initialize(section, name):
    self.set_section(section)
    self.set_name(name)
    self.set_version(1)
    self.register_input

  def rocof(input_streams):
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

    return [freqs]

opts = { 'input_streams'  : ['grizzly_new_L2Ang_freq'],
         'input_uids'     : ['377af6b1-1733-4a30-a280-6cf69591d257'],
         'start_date'     : '2014-12-01T00:00:00.000000',
         'end_date'       : '2014-12-01T01:00:00.000000',
         'output_streams' : ['grizzly_new_L2Ang_rocof'],
         'output_units'   : ['Hz/s'],
         'author'         : 'CAB',
         'name'           : 'dev_rocof_old',
         'version'        : 1,
         'algorithm'      : rocof }
qdf.register(Distillate(), opts)
qdf.begin()

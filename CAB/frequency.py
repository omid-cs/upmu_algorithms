import qdf
from distillate import Distillate

def frequency(input_streams):
  # only one input stream
  input_phases = input_streams[0]

  sampling_freq = 120 #Hz

  freqs = []
  i = 0
  while i < len(input_phases)-sampling_freq:
    delta_samples = sampling_freq #upper bound
    t1 = input_phases[i].time
    t2 = input_phases[i+delta_samples].time
    while ((t2 - t1) > 1e9 and t2 > t1): #catch zeroed or missing samples
      delta_samples -= 1 #decrement ~one sample per missing sample in interval
      t2 = input_phases[i+delta_samples].time
    if t2 - t1 < 1e9: #if sample 1 second from now is missing, skip
      i += 1
      continue
    x1 = input_phases[i].value
    x2 = input_phases[i+delta_samples].value
    phase_diff = x2 - x1
    delta_time = t2 - t1
    if phase_diff > 180:
      phase_diff -= 360
    elif phase_diff < -180:
      phase_diff += 360
    freqs.append((t1, (phase_diff/delta_time)*1e9/360 + 60))

    if len(freqs) >= qdf.OPTIMAL_BATCH_SIZE:
      yield [freqs] # must yield list
      freqs = []
    i += 1

  yield None

opts = { 'input_streams'  : ['upmu/grizzly_new/L1ANG'], \
         'input_uids'     : ['b4776088-2f85-4c75-90cd-7472a949a8fa'], \
         'start_date'     : '2014-09-07T00:00:00.000000', \
         'end_date'       : '2014-09-08T00:00:00.000000', \
         'output_streams' : ['grizzly_new_L1Mag_frequency'], \
         'output_units'   : ['Hz'], \
         'author'         : 'CAB', \
         'name'           : 'Frequency', \
         'version'        : 2, \
         'algorithm'      : frequency }
qdf.register(Distillate(), opts)
qdf.begin()

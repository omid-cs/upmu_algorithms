import qdf
from distillate import Distillate

overflow_points = [[],[],[],[],[],[]]
def frequency(input_streams):
  global overflow_points
  output_streams = []
  
  for j in range(len(input_streams)):
      # convert input_points to an array and prepend overflow_points
      # TEMP: naive solution, find better one!
      input_points = overflow_points[j]
      for point in input_streams[j]:
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
        phase_diff = x2 - x1
        delta_time = t2 - t1
        if phase_diff > 180:
          phase_diff -= 360
        elif phase_diff < -180:
          phase_diff += 360
        freqs.append((t2, (phase_diff/delta_time)*1e9/360 + 60))
        i += 1

      #save trailing values for next batch
      overflow_points[j] = []
      for i in range(len(input_points)-sampling_freq, len(input_points)):
        overflow_points[j].append(input_points[i])
      output_streams.append(freqs)
  return output_streams

opts = { 'input_streams'  : ['C1ANG', 'C2ANG', 'C3ANG', 'L1ANG', 'L2ANG', 'L3ANG'],
         'input_uids'     : ['4072af6f-938e-450c-9927-37dee6968446',
                             'bf045a36-34df-4bee-a747-b20c3164723a',
                             '8a5d0010-4665-4b59-ab6f-e7858c12284a',
                             'adf13e17-44b7-4ef6-ae3f-fde8a9152ab7',
                             '4f56a8f1-f3ca-4684-930e-1b4d9955f72c',
                             '2c07ccef-20c5-4971-87cf-2c187ce5f722'],
         'start_date'     : '2014-09-30T00:00:00.000000',
         'end_date'       : '2014-09-30T08:00:00.000000',
         'output_streams' : ['C1ANG', 'C2ANG', 'C3ANG', 'L1ANG', 'L2ANG', 'L3ANG'],
         'output_units'   : ['Hz', 'Hz', 'Hz', 'Hz', 'Hz', 'Hz'],
         'author'         : 'FREQ_1SEC_IN_HZ',
         'name'           : 'switch_a6',
         'version'        : 3,
         'algorithm'      : frequency }
qdf.register(Distillate(), opts)
qdf.begin()

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
        overflow_points[j].append(input_points[j])
      output_streams.append(freqs)
  return output_streams

opts = { 'input_streams'  : ['C1ANG', 'C2ANG', 'C3ANG', 'L1ANG', 'L2ANG', 'L3ANG'],
         'input_uids'     : ['5747fe6b-3300-4737-b7f6-4a699251ce2a',
                             '5f7400b1-694c-4e03-8d84-235943db1b75',
                             '1b1a6c56-0509-4031-ac5a-ca2346ae5178',
                             '98435be7-7341-4661-b104-16af89e0333d',
                             '321db464-b05b-4a97-988c-1a9cc5593143',
                             '33b376c8-a59e-4054-a213-e9eb95cc8ad9'],
         'start_date'     : '2014-09-30T00:00:00.000000',
         'end_date'       : '2014-09-30T08:00:00.000000',
         'output_streams' : ['C1ANG', 'C2ANG', 'C3ANG', 'L1ANG', 'L2ANG', 'L3ANG'],
         'output_units'   : ['Hz', 'Hz', 'Hz', 'Hz', 'Hz', 'Hz'],
         'author'         : 'FREQ_1SEC_IN_HZ',
         'name'           : 'soda_b',
         'version'        : 2,
         'algorithm'      : frequency }
qdf.register(Distillate(), opts)
qdf.begin()

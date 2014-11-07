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
         'input_uids'     : ['888b8f61-c2a4-44a1-bd5c-9865ea6ea8ca',
                             '9f004502-3f99-4bef-b936-7f860b53bfdf',
                             'bd46f563-a6e1-4b93-9899-0faf8a70a1b3',
                             '4d6525a9-b8ad-48a4-ae98-b171562cf817',
                             'fe580578-854d-43c5-95b4-9f305a70e6a3',
                             'b5279898-5652-4d34-abd6-45c7d697e524'],
         'start_date'     : '2014-09-30T00:00:00.000000',
         'end_date'       : '2014-09-30T08:00:00.000000',
         'output_streams' : ['C1ANG', 'C2ANG', 'C3ANG', 'L1ANG', 'L2ANG', 'L3ANG'],
         'output_units'   : ['Hz', 'Hz', 'Hz', 'Hz', 'Hz', 'Hz'],
         'author'         : 'FREQ_1SEC_IN_HZ',
         'name'           : 'soda_a',
         'version'        : 2,
         'algorithm'      : frequency }
qdf.register(Distillate(), opts)
qdf.begin()

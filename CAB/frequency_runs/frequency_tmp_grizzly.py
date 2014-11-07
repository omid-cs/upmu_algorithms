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
         'input_uids'     : ['4b7fec6d-270e-4bd6-b301-0eac6df17ca2',
                             '9ffeaf2a-46a9-465f-985d-96f84df66283',
                             '8b40fe4c-36ee-4b10-8aef-1eef8c471e1d',
                             'b4776088-2f85-4c75-90cd-7472a949a8fa',
                             '8b80c070-7bb1-44d3-b3a8-301558d573ea',
                             'b653c63b-4acc-45ee-ae3d-1602e6116bc1'],
         'start_date'     : '2014-09-30T00:00:00.000000',
         'end_date'       : '2014-09-30T08:00:00.000000',
         'output_streams' : ['C1ANG', 'C2ANG', 'C3ANG', 'L1ANG', 'L2ANG', 'L3ANG'],
         'output_units'   : ['Hz', 'Hz', 'Hz', 'Hz', 'Hz', 'Hz'],
         'author'         : 'FREQ_1SEC_IN_HZ',
         'name'           : 'grizzly_new',
         'version'        : 2,
         'algorithm'      : frequency }
qdf.register(Distillate(), opts)
qdf.begin()

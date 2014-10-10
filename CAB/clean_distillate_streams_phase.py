import qdf
from distillate import Distillate

def clean(input_streams):
  # only one input stream
  input_points = input_streams[0]

  max_delta_mag = 2.0 #degrees
  
  clean_points = []
  error_points = []

  #first catch initial case
  #Resolve initial point edge-case
  #  Possibilities:
  #    use fetch point -1 from stream (requires -1 point to exist)
  #    interpret error using first three points:
  """
  first = input_points[0].value
  second = input_points[1].value
  third = input_points[2].value
  second_error = abs(second-first) > max_delta_mag
  third_error = abs(third-second) > max_delta_mag
  first_error = (second_error) and (not third_error)
  """
  
  i = 1
  while i < len(input_points):
    prev = input_points[i-1].value
    cur = input_points[i].value
    delta_mag = abs(cur-prev)
    if delta_mag > max_delta_mag:
      error_points.append((input_points[i].time, 1))
    else:
      clean_points.append((input_points[i].time, input_points[i].value))

    if len(error_points) + len(clean_points) >= qdf.OPTIMAL_BATCH_SIZE:
      yield [clean_points, error_points] # keep order as specified in opts
      clean_points = []
      error_points = []
    i += 1
  yield [clean_points, error_points]

opts = { 'input_streams'  : ['upmu/grizzly_new/L1ANG'], \
         'input_uids'     : ['b4776088-2f85-4c75-90cd-7472a949a8fa'], \
         'start_date'     : '2014-08-28T00:00:00.000000', \
         'end_date'       : '2014-08-29T00:00:00.000000', \
         'output_streams' : ['grizzly_new_L1Ang_clean', 'grizzly_new_L1Ang_errors'], \
         'output_units'   : ['Degrees', 'error'], \
         'author'         : 'CAB', \
         'name'           : 'Clean', \
         'version'        : 7, \
         'algorithm'      : clean }
qdf.register(Distillate(), opts)
qdf.begin()
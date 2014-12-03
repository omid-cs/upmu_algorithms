import qdf
from distillate import Distillate

prev_point = None
def clean(input_streams):
  # only one input stream
  input_points = input_streams[0]

  max_delta_mag = .1 #degrees
  
  clean_points = []
  error_points = []

  #first catch initial case
  #Resolve initial point edge-case
  #  Possibilities:
  #    use fetch point -1 from stream (requires -1 point to exist)
  #    interpret error using first three points:
  #
  #
  # ignore this edge case for now
  """
  first = input_points[0].value
  second = input_points[1].value
  third = input_points[2].value
  second_error = abs(second-first) > max_delta_mag
  third_error = abs(third-second) > max_delta_mag
  first_error = (second_error) and (not third_error)
  """
  
  #dirty fix for batching
  global prev_point
  if prev_point is not None:
    prev = prev_point.value
    cur=input_points[0].value
    delta_mag = abs(cur-prev)
    if delta_mag > 360-max_delta_mag and delta_mag < 360+max_delta_mag:
        # account for wrapping
        delta_mag = abs(360-delta_mag)
    if delta_mag > max_delta_mag:
      error_points.append((input_points[0].time, 1))
    else:
      clean_points.append((input_points[0].time, input_points[0].value))

  # main algorithm
  i = 1
  while i < len(input_points):
    prev = input_points[i-1].value
    cur = input_points[i].value
    delta_mag = abs(cur-prev)
    if delta_mag > 360-max_delta_mag and delta_mag < 360+max_delta_mag:
        # account for wrapping
        delta_mag = abs(360-delta_mag)
    if delta_mag > max_delta_mag:
      error_points.append((input_points[i].time, 1))
    else:
      clean_points.append((input_points[i].time, input_points[i].value))
    i += 1

  # save last point as reference for next point
  # this poor fix will be fixed by distiller stream class
  global prev_point
  prev_point = input_points[-1]
  return [clean_points, error_points]

opts = { 'input_streams'  : ['upmu/grizzly_new/L1ANG'],
         'input_uids'     : ['b4776088-2f85-4c75-90cd-7472a949a8fa'],
         'start_date'     : '2014-08-28T00:00:00.000000',
         'end_date'       : '2014-08-28T02:00:00.000000',
         'output_streams' : ['grizzly_new_L1Ang_clean', 'grizzly_new_L1Ang_errors'],
         'output_units'   : ['Degrees', 'error'],
         'author'         : 'CAB',
         'name'           : 'dev_remove_outliers_phase',
         'version'        : 1,
         'algorithm'      : clean }
qdf.register(Distillate(), opts)
qdf.begin()

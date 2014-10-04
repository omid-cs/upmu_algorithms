import qdf
from distillate import Distillate

def clean(input_streams):
  # only one input stream
  input_points = input_streams[0]

  lower_bound = 0
  upper_bound = 500
  
  clean_points = []
  error_points = []

  i = 0
  while i < len(input_points):
    if input_points[i].value >= lower_bound and input_points[i].value <= upper_bound:
      clean_points.append((input_points[i].time, input_points[i].value))
      error_points.append((input_points[i].time, 0))
    else:
      error_points.append((input_points[i].time, 1))

    if len(error_points) >= qdf.OPTIMAL_BATCH_SIZE:
      yield [clean_points, error_points] # keep order as specified in opts
      clean_points = []
      error_points = []
    i += 1

  yield None

opts = { 'input_streams'  : ['upmu/grizzly_new/L1MAG'], \
         'input_uids'     : ['a64c386e-2dd4-4f17-96cb-1655358cb12c'], \
         'start_date'     : '2014-09-07T00:00:00.000000', \
         'end_date'       : '2014-09-08T00:00:00.000000', \
         'output_streams' : ['grizzly_new_L1Mag_clean', 'grizzly_new_L1Mag_errors'], \
         'output_units'   : ['V', 'error'], \
         'author'         : 'CAB', \
         'name'           : 'Clean', \
         'version'        : 2, \
         'algorithm'      : clean }
qdf.register(Distillate(), opts)
qdf.begin()

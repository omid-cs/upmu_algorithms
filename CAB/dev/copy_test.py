import qdf
from distillate_new import Distillate
from twisted.internet import defer

@defer.inlineCallbacks
def copy(input_streams, output_streams):
  # only one stream
  stream = input_streams[0]
  copy_stream = output_streams[0]

  i = 0
  for i in range(120*60*60*10): # 10 hours of datapoints
    datapoint = stream[i]
    if datapoint != None:
      copy_stream.append(datapoint)


opts = { 'input_streams'  : ['B71_L2ANG'],
         'input_uids'     : ['f89e77a8-661e-49d2-a868-2071c1fae238'],
         'start_dates'    : ['2014-10-01T00:00.000000'],
         'end_dates'      : ['2014-10-01T10:00.000000'],
         'output_streams' : ['B71_L2ANG_copy'],
         'output_units'   : ['Degrees'],
         'author'         : 'CAB',
         'name'           : 'Dev',
         'version'        : 1,
         'algorithm'      : copy }
qdf.register(Distillate(), opts)
qdf.begin()

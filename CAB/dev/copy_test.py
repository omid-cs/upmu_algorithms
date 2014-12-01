import qdf
from distillate_new import Distillate
from twisted.internet import defer

@defer.inlineCallbacks
def copy(input_streams, output_streams):
  # only one input stream
  stream = input_streams[0]

  # only one output stream
  copy_stream = output_streams[0]

  i = 0
  for i in range(120*60*60*1): # 1 hour of datapoints
    datapoint = yield stream[i]
    if datapoint != None:
      is_full = copy_stream.append(datapoint)
      if is_full:
        yield copy_stream.flush()


opts = { 'input_streams'  : ['B71_L2ANG'],
         'input_uids'     : ['f89e77a8-661e-49d2-a868-2071c1fae238'],
         'start_dates'    : ['2014-10-01T00:00.000000'],
         'end_dates'      : ['2014-10-01T01:00.000000'],
         'output_streams' : ['B71_L2ANG_copy'],
         'output_units'   : ['Degrees'],
         'author'         : 'CAB',
         'name'           : 'Dev',
         'version'        : 9,
         'algorithm'      : copy }
qdf.register(Distillate(), opts)
qdf.begin()

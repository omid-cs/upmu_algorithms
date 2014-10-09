import qdf # imports the qdf module so we can use it (ex. "qdf.[function or constant]")
from distillate import Distillate # imports the generalized distillate class

def algorithm(input_streams): # can change name 'algorithm', the name doesn't matter
  # this is where you name the input data streams that have already been openned and queried
  # the order of input streams is the same order as specified in the 'opts' dictionary
  first_input_stream = input_streams[0]
  second_input_stream = input_streams[1]
  third_input_stream = input_streams[2]

  # defined arrays for each output streams that we will yield
  # the order of output streams is the same order as specified in teh 'opts' dictionary
  first_output_stream = []
  second_output_stream = []
  
  # This is where your algorithm will be implemented. Using the data from the input streams
  #  and whatever other variables you define locally, calculate the output and store it in
  #  the output stream arrays.
  """
    This example algorithm calculates the minimum and maximium of each input stream.
      - first_output_stream: min values
      - second_output_stream: max values
    It naively assumes that all streams are in synch (no dropped or extra points in the stream)
  """
  i = 0
  while i<len(first_input_stream) or i<len(second_input_stream) or i<len(third_input_stream):
    # find the 'time' of the points being compared
    # Note: this example incorrectly assumes the 'time' of each point is the same
    #   this might not be the case and so cannot be assume in a real distillate
    time = first_input_stream[i].time

    # find the 'value' of each point
    x1 = first_input_stream[i].value
    x2 = second_input_stream[i].value
    x3 = third_input_stream[i].value

    # calculate the min and max of the values
    min_x = min(x1, x2, x3)
    max_x = max(x1, x2, x3)
    
    # store min and max values in output arrays
    first_output_stream.append((time, min_x))
    second_output_stream.append((time, max_x))

    # increment the index counter so that the next point is processed
    i += 1

  # after the algorithm loop finishes, we need to return out output data so it can be stored
  #   on the server
  yield [freqs]


# This is where all the meta-data and input and output names and dates are defined
# These key-value pairs are used to open and query input data stream, and store output data.
# All of these keys must be present for the program to run. Edit the values according to the
#   needs of the algorithm

         # string names paired to uuids. Must all be unique
opts = { 'input_streams'  : ['in1', 'in2', 'in3'],

         # uuids of input streams. Order matters
         'input_uids'     : ['00000000-0000-0000-0000-000000000000', \
                             '00000000-0000-0000-0000-000000000000', \
                             '00000000-0000-0000-0000-000000000000'],

         # start date for input streams. Format must match: 'yyyy-mm-ddThh:mm:ss.ssssss'
         'start_date'     : '2014-10-06T00:00:00.000000',

         # end date for input streams. Format must match: 'yyyy-mm-ddThh:mm:ss.ssssss'
         'end_date'       : '2014-10-06T02:30:00.000000',

         # string names of output streams.
         'output_streams' : ['out1, out2, out3'],

         # List of units for each output stream
         'output_units'   : ['Unit', 'Unit', 'Unit'],

         # The programmer who wrote this distillate. First level directory name
         'author'         : 'CAB',

         # The name of the type algorithm implemented. Second level directory name
         'name'           : 'New Output Frequency',

         # The version of the code. Increment this to overwrite existing data from an older 
         #   version of this code
         'version'        : 6,

         # Plaintext name of the function defined above. This passes a 'function reference'
         #   that can be called in another program
         'algorithm'      : algorithm }

# The following two lines instantiate the distillate class and begin begin the distillation
qdf.register(Distillate(), opts) #instantiates an object with your parameters and algorithm
qdf.begin() # enters the program and runs the distillation program

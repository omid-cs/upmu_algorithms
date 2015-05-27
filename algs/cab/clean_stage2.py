# Takes the annotated stream and
# delete points in raw stream (overlaps in case 1 and 3)
# and shifts points in raw stream after a gap in case 2 and before a gap in case 3

__author__ = 'aliao'
import qdf
import numpy as np
from math import ceil

print ("defining clean_stage2.CleanSweep")
class CleanSweep (qdf.QDF2Distillate):
  def initialize(self, section="Filter", name="default",stream_type="ANG"):
    self.set_section(section)
    self.set_name(name)
    self.set_version(4)

    if 'ANG' in stream_type:
      units = 'deg'
    elif 'MAG' in stream_type:
      if 'C' in stream_type:
        units = 'A'
      else:
        units = 'V'
    elif 'LSTATE' in stream_type:
      units = 'bitmap'
    else:
      units = 'arb'

    self.register_output("CLEAN_SHIFTED",units)
    self.register_input("CLEAN1_OUT")
    self.register_input("RAW_DATA")

  def compute(self, changed_ranges, input_streams, params, report):
    sweep_out = report.output("CLEAN_SHIFTED")
    #lstates = input_streams["LSTATE"]
    sweep_in = input_streams["CLEAN1_OUT"]
    raw_data = input_streams["RAW_DATA"]

    # case 1: delete at timestamp of annotation
    # case1_inds is list of all indexes for case 1
    # case1_inds = [ind for ind,x in enumerate(sweep_in) if x[1] == 1]

    # case 2: left-shift everything at and after the annotation
    # case2_inds = [ind for ind,x in enumerate(sweep_in) if x[1] == 2]

    # case 3: left-shift everyhing before the annotation
    # case3_indx = [ind for ind,x in enumerate(sweep_in) if x[1] == 3]

    i = 0
    raw_index = 0
    #first_pt_processed = False
    shift_mode = False
    while i < len(raw_data):
       try:    
          if sweep_in[i][1] == 0:
             i += 1
             continue
          elif sweep_in[i][1] == 1:
             # delete this point and unity for raw to clean up to this point
             while raw_index < i:
                   current_raw_t = raw_data[raw_index][0]
                   sweep_out.addreading(current_raw_t,raw_data[raw_index][1])    
		   sweep_out.addbounds(current_raw_t, current_raw_t + 1)
                   raw_index += 1
             raw_index += 1
             i += 1
          elif sweep_in[i][1] == 2:
             # start of shift_mode, shift current data point
             # all previous data points are unity
	     
             while raw_index < i-1:
                   current_raw_t = raw_data[raw_index][0]
                   current_raw_datapoint = raw_data[raw_index][1]
                   sweep_out.addreading(current_raw_t, current_raw_datapoint)
                   sweep_out.addbounds(current_raw_t, current_raw_t + 1)
                   raw_index += 1
             raw_index += 2
             if raw_index != i: 
                raise Exception('problem in clean_stage2, raw_index = %i and i = %i' % (raw_index,i))
             shifted_raw_t = raw_data[raw_index][0] - 1
             current_raw_datapoint = raw_data[raw_index][1]
             sweep_out.addreading(shifted_raw_t, current_raw_datapoint)
             sweep_out.addbounds(shifted_raw_t, shifted_raw_t + 1)
          elif shift_mode == True:
             # in shift mode
             # check for end of shift mode: last data point or a case 3 annotation
             # for last data point, can treat as regular shift_mode procedure
             # For case 3 annotation, end shift mode and delete current point

             if sweep_in[i][1] == 3:
                shift_mode == False
                i += 1
                raw_index += 1
             else:
                shifted_raw_t = raw_data[raw_index][0] - 1
                current_raw_datapoint = raw_data[raw_index][1]
                sweep_out.addreading(shifted_raw_t, current_raw_datapoint)
                sweep_out.addbounds(shifted_raw_t, shifted_raw_t + 1)
                i += 1
                raw_index += 1
          elif sweep_in[i][1] == 3 and raw_index == 0:
             # delete data at this annotation left-shift everything before this annotation
             # this case is only if the case 3 annotation is the first annotation
             # otherwise, left-shifting should have been handled in shift_mode
             while raw_index < i:
                   shifted_raw_t = raw_data[raw_index][0] - 1
	           current_raw_datapoint = raw_data[raw_index][1]
                   sweep_out.addreading(shifted_raw_t, current_raw_datapoint)
		   sweep_out.addbounds(shifted_raw_t, shifted_raw_t + 1)
          else:
             # sweep_in[i] is empty
             i += 1
       except:
          e = sys.exc_info()[0]
          print "Error: %s, i=%i" % (e,i)
    
    print "done computing clean_stage2"

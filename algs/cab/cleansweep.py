import qdf
import numpy as np
from math import ceil

class CleanSweep (qdf.QDF2Distillate):
  def initialize(self, section="Filter", name="default"):
    self.set_section(section)
    self.set_name(name)
    self.set_version(5)
    self.register_output("OFFSET_SWEEP_OUT", 'bitmap')
    self.register_input("LSTATE")
    self.register_input("OFFSET_SWEEP_IN")

  def prereqs(self, changed_ranges):
    for changed_range in changed_ranges:
      if changed_range[1] == "LSTATE":
        changed_range_lstate = changed_range
      elif changed_range[1] == "OFFSET_SWEEP_IN":
        changed_range_offset = changed_range
    offset_uuid = changed_ranges[0][0]
    offset_name = changed_ranges[0][1]
    offset_rngs = []
    for rng in changed_range_offset[2]:
      offset_rngs.append([rng[-1], rng[-1]+(qdf.MINUTE*10)])
    return [changed_range_lstate, [offset_uuid, offset_name, offset_rngs]]

  def compute(self, changed_ranges, input_streams, params, report):
    sweep_out = report.output("OFFSET_SWEEP_OUT")
    lstates = input_streams["LSTATE"]
    sweep_in = input_streams["OFFSET_SWEEP_IN"]

    # initial sweep
    i = 0
    while i < len(lstates):
      lstate = lstates[i]
      time = lstate[0]
      value = lstate[1]
      
      if time % qdf.SECOND != 0:
        # skip datapoints unless whole second time
        i += 1
        continue

      if value == 8:
        # if there is a time shift, inspect previous and next lstates
        prev_time, prev_value = 0, 0
        next_time, next_value = 0, 0
        if i > 0:
          prev_lstate = lstates[i-1]
          prev_time = prev_lstate[0]
          prev_value = prev_lstate[1]
        if i+1 < len(lstates):
          next_lstate = lstates[i+1]
          next_time = next_lstate[0]
          next_value = next_lstate[1]

        if time == next_time:
          # skip the next point in following loop if same timestamp
          i += 1

        if time == next_time and next_value == 8:
          # case 1: timeshift block of block length exactly 1 second
          sweep_out.addreading(time, 1.0)
          i += 1
        elif time != next_time and time != prev_time and time > prev_time + (qdf.SECOND*.9):
          # case 2: the beginning of a time shifted block
          sweep_out.addreading(time, 2.0)
        elif (time == next_time and next_value != 8) or (time == prev_time and prev_value != 8):
          # case 3: the end of a time shifted block
          sweep_out.addreading(time, 3.0)
        else:
          # something went very wrong....
          print("time: {0}\tvalue: {1}".format(time, value))
          print("prev_time: {0}\tprev_value{1}".format(prev_time, prev_value))
          print("next_time: {0}\tnext_value: {1}".format(next_time, next_value))
          raise RuntimeError("lockstate 8 but does not match known cases")
      else:
        sweep_out.addreading(time, 0.0)
      i += 1
    sweep_out.addbounds(*changed_ranges['LSTATE'])

    # annotate stream
    for offset in sweep_in:


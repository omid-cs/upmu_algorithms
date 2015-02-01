import qdf
import numpy as np

class Phase_Difference (qdf.QDF2Distillate):
  def initialize(self, section="Phase_Difference", name="default"):
    print('Begin initializing algorithm')
    self.set_section(section)
    self.set_name(name)
    self.set_version(2)
    self.register_output("phase_difference", "Degrees")
    self.register_input("phase1")
    self.register_input("phase2")
    print('Finished initializing algorithm')

  def compute(self, changed_ranges, input_streams, params, report):
    phase_diff_output = report.output("phase_difference")

    print "compute invoked:"
    phase1 = input_streams["phase1"]
    phase2 = input_streams["phase2"]


    print "changed_ranges: ", changed_ranges
    print "params: ", params

    i1 = 0
    i2 = 0
    print "algorithm successfully prepped for calculation"
    while i1 < len(phase1) and i2 < len(phase2):
      if not (phase1[i1].time == phase2[i2].time):
        # if times do not align, iteratively increment trailing stream until equal
        max_time = max(phase1[i1].time, phase2[i2].time)
        if phase1[i1].time < max_time:
          i1 += 1
        if phase2[i2].time < max_time:
          i2 += 1
        continue

      # Calculate reactive power
      time = phase1[i1].time
      pd = phase1[i1].value - phase2[i2].value
      reactive_power_output.addreading(time, pd)

      #increment counters and loop
      i1 += 1
      i2 += 1

    reactive_power_output.addbounds(*changed_ranges["phase1"])
    reactive_power_output.addbounds(*changed_ranges["phase2"])

import qdf
import numpy as np

class Phase_Difference (qdf.QDF2Distillate):
  def initialize(self, section="Phase_Difference", name="default"):
    self.set_section(section)
    self.set_name(name)
    self.set_version(5)
    self.register_output("phase_difference", "Degrees")
    self.register_input("phase1")
    self.register_input("phase2")

  def compute(self, changed_ranges, input_streams, params, report):
    phase_diff_output = report.output("phase_difference")

    phase1 = input_streams["phase1"]
    phase2 = input_streams["phase2"]

    i1 = 0
    i2 = 0
    while i1 < len(phase1) and i2 < len(phase2):
      if not (phase1[i1][0] == phase2[i2][0]):
        # if times do not align, iteratively increment trailing stream until equal
        max_time = max(phase1[i1][0], phase2[i2][0])
        if phase1[i1][0] < max_time:
          i1 += 1
        if phase2[i2][0] < max_time:
          i2 += 1
        continue

      # Calculate phase difference
      time = phase1[i1][0]
      pd = phase1[i1][1] - phase2[i2][1]
      if pd > 180:
        pd -= 360
      elif pd < -180:
        pd += 360
      phase_diff_output.addreading(time, pd)

      #increment counters and loop
      i1 += 1
      i2 += 1

    phase_diff_output.addbounds(*changed_ranges["phase1"])
    phase_diff_output.addbounds(*changed_ranges["phase2"])

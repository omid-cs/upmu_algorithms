import qdf
import numpy as np

class Magnitude_Difference (qdf.QDF2Distillate):
  def initialize(self, section="Magnitude_Difference", name="default"):
    self.set_section(section)
    self.set_name(name)
    self.set_version(1)
    self.register_output("MAG-DIFFERENCE", "Volts")
    self.register_input("magnitude1")
    self.register_input("magnitude2")

  def compute(self, changed_ranges, input_streams, params, report):
    mag_diff_output = report.output("MAG-DIFFERENCE")

    mag1 = input_streams["magnitude1"]
    mag2 = input_streams["magnitude2"]

    i1 = 0
    i2 = 0
    while i1 < len(mag1) and i2 < len(mag2):
      if not (mag1[i1][0] == mag2[i2][0]):
        # if times do not align, iteratively increment trailing stream until equal
        max_time = max(mag1[i1][0], mag2[i2][0])
        if mag1[i1][0] < max_time:
          i1 += 1
        if mag2[i2][0] < max_time:
          i2 += 1
        continue

      # Calculate magnitude difference
      time = mag1[i1][0]
      md = mag1[i1][1] - mag2[i2][1]
      mag_diff_output.addreading(time, md)

      #increment counters and loop
      i1 += 1
      i2 += 1

    mag_diff_output.addbounds(*changed_ranges["magnitude1"])
    mag_diff_output.addbounds(*changed_ranges["magnitude2"])

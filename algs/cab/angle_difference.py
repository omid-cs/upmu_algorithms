import qdf
import numpy as np

class Angle_Difference (qdf.QDF2Distillate):
  def initialize(self, section="Angle_Difference", name="default"):
    self.set_section(section)
    self.set_name(name)
    self.set_version(1)
    self.register_output("ANGLE_DIFFERENCE", "Degrees")
    self.register_input("angle1")
    self.register_input("angle2")

  def compute(self, changed_ranges, input_streams, params, report):
    angle_diff_output = report.output("ANGLE_DIFFERENCE")

    angle1 = input_streams["angle1"]
    angle2 = input_streams["angle2"]

    i1 = 0
    i2 = 0
    while i1 < len(angle1) and i2 < len(angle2):
      if not (angle1[i1][0] == angle2[i2][0]):
        # if times do not align, iteratively increment trailing stream until equal
        max_time = max(angle1[i1][0], angle2[i2][0])
        if angle1[i1][0] < max_time:
          i1 += 1
        if angle2[i2][0] < max_time:
          i2 += 1
        continue

      # Calculate angle difference
      time = angle1[i1][0]
      pd = angle1[i1][1] - angle2[i2][1]
      if pd > 180:
        pd -= 360
      elif pd < -180:
        pd += 360
      angle_diff_output.addreading(time, pd)

      #increment counters and loop
      i1 += 1
      i2 += 1

    angle_diff_output.addbounds(*changed_ranges["angle1"])
    angle_diff_output.addbounds(*changed_ranges["angle2"])

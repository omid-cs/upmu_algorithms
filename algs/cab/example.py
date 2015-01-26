import qdf
import numpy as np

class Phaseshift (qdf.QDF2Distillate):
  def initialize(self, name="phaseshift", shift=0):
    self.set_section("Development")
    self.set_name(name)
    self.set_version(1)
    self.register_output("out", "arb_units")
    self.register_input("sinusoid")

    self.shift = int(shift)

  def compute(self, changed_ranges, input_streams, params, report):
    out = report.output("out")

    print "compute invoked:"
    print "changed_ranges: ", changed_ranges
    print "params: ", params

    for point in input_streams["sinusoid"]:
      time = point[0]
      val = point[1]
      val += self.shift
      if val > 180:
        val -= 360
      out.addreading(time, val)

    out.addbounds(*changed_ranges["sinusoid"])

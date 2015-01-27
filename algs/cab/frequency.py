import qdf
import numpy as np

class Frequency (qdf.QDF2Distillate):
  def initialize(self, name="frequency", output="frequency", dt="1.0"):
    self.set_section("Development/foobar")
    self.set_name(name)
    self.set_version(12)
    self.register_output(output, "Hz")
    self.register_input("phase")

    self.dt = float(dt)*qdf.SECOND

  def prereqs(self, changed_ranges):
    uuid = changed_ranges[0][0]
    name = changed_ranges[0][1]
    rngs = []
    for rng in changed_ranges[0][2]:
      rngs.append([rng[0]-self.dt, rng[1]])
    return [[uuid, name, rngs]]

  def compute(self, changed_ranges, input_streams, params, report):
    out = report.output("frequency")

    print "compute invoked:"
    print "changed_ranges: ", changed_ranges
    print "params: ", params

    i1 = 0
    i2 = 120
    while i1 < len(input_streams["phase"])-120 and i2 < len(input_streams["phase"]):
      p1 = input_streams["phase"][i1]
      p2 = input_streams["phase"][i2]

      # check that points are exactly dt apart
      if round((float((p2[0]-p1[0]))/qdf.SECOND)) < 1:
        i2 += 1
        continue
      if round((float((p2[0]-p1[0]))/qdf.SECOND)) > 1:
        i1 += 1
        continue

      time = p2[0]
      delta_phase = p2[1]-p1[1]
      if delta_phase > 180:
        delta_phase -= 360
      if delta_phase < -180:
        delta_phase += 360
      freq = (delta_phase/self.dt*qdf.SECOND)/360.0 + 60.0
      out.addreading(time, freq)
      i1 += 1
      i2 += 1

    out.addbounds(*changed_ranges["phase"])

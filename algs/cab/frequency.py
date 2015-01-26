import qdf
import numpy as np

class Frequency (qdf.QDF2Distillate):
  def initialize(self, name="frequency", output="frequency", dt="1.0"):
    self.set_section("Development")
    self.set_name(name)
    self.set_version(1)
    self.register_output(output, "Hz")
    self.register_input("phase")

    self.dt = float(dt)

  def prereqs(self, changed_ranges):
    name = changed_ranges[0]
    uuid = changed_ranges[1]
    rngs = []
    for rng in changes_ranges[2]:
      rngs.append([rng[0]-self.dt, rng[1]])
    return (name, uuid, rngs)

  def compute(self, changed_ranges, input_streams, params, report):
    out = report.output("frequency")

    print "compute invoked:"
    print "changed_ranges: ", changed_ranges
    print "params: ", params

    i1 = 0
    i2 = 120
    while i1 < len(input_streams-120) and i2 < len(input_streams):
      p1 = intput_streams[i]
      p2 = intput_streams[i+120]

      # check that points are exactly dt apart
      if round(((p2[i2]-p1[i1])/qdf.SECOND*120)) < 1:
        i2 += 1
        continue
      if round(((p2[i2]-p1[i1])/qdf.SECOND*120)) > 1:
        i1 += 1
        continue

      time = int(p2[0])
      delta_phase = p2[1]-p1[1]
      if delta_phase > 180:
        delta_phase -= 360
      if delta_phase < -180:
        delta_phase += 360
      freq = (delta_phase/self.dt)/360 + 60
      out.addreading(time, freq)
      i1 += 1
      i2 += 1

    out.addbounds(*changed_ranges["phase"])

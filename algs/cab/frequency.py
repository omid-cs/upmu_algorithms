import qdf
import numpy as np

class Frequency (qdf.QDF2Distillate):
  def initialize(self, section="Frequency", name="frequency"):
    self.set_section(section)
    self.set_name(name)
    self.set_version(15)
    self.register_output("1-Sec", "Hz")
    self.register_output("C37", "Hz")
    self.register_input("phase")

  def prereqs(self, changed_ranges):
    uuid = changed_ranges[0][0]
    name = changed_ranges[0][1]
    rngs = []
    for rng in changed_ranges[0][2]:
      rngs.append([rng[0]-qdf.SECOND, rng[1]])
    return [[uuid, name, rngs]]

  def compute(self, changed_ranges, input_streams, params, report):
    sec = report.output("1-Sec")
    c37 = report.output("C37")

    phase = input_streams["phase"]

    # C37 Frequency
    i = 120
    while i < len(phase):
      p1 = phase[i]
      p2 = phase[i-1]
      p3 = phase[i-2]
      p4 = phase[i-3]

      # check that points are exactly 1/120 seconds apart
      if round((120*float(p1[0]-p2[0])/qdf.SECOND)) < 1 or \
         round((120*float(p2[0]-p3[0])/qdf.SECOND)) < 1 or \
         round((120*float(p3[0]-p4[0])/qdf.SECOND)) < 1:
        i += 1
        continue

      # adjust values for wrapping
      v1 = angle_diff(p1[1], p2[1])
      v2 = angle_diff(p2[1], p3[1])
      v3 = angle_diff(p3[1], p4[1])

      time = p1[0]
      freq = 60 + (((6.0*(v1)+3.0*(v2)+1.0*(v3))/10)*((120.0/360.0)))

      c37.addreading(time, freq)
      i += 1


    # 1-Sec Frequency
    i1 = 0
    i2 = 120
    while i1 < len(phase)-120 and i2 < len(phase):
      p1 = phase[i1]
      p2 = phase[i2]

      # check that points are exactly 1 second apart
      if round((float((p2[0]-p1[0]))/qdf.SECOND)) < 1:
        print "increments i2"
        i2 += 1
        continue
      if round((float((p2[0]-p1[0]))/qdf.SECOND)) > 1:
        print "increments i1"
        i1 += 1
        continue

      time = p2[0]
      delta_phase = angle_diff(p2[1], p1[1])

      freq = delta_phase/360.0 + 60.0
      sec.addreading(time, freq)
      
      i1 += 1
      i2 += 1

    c37.addbounds(*changed_ranges["phase"])
    sec.addbounds(*changed_ranges["phase"])

def angle_diff(v1, v2):
  # assumes angles wrap from
  phase_diff = v1-v2
  if phase_diff > 180:
    phase_diff -= 360
  elif phase_diff < -180:
    phase_diff += 360
  return phase_diff

import qdf
import numpy as np

class Frequency (qdf.QDF2Distillate):
  def initialize(self, name="angle difference"):
    self.set_section("Development/foobar")
    self.set_name(name)
    self.set_version(1)
    self.register_output("Grizzly-SwitchA6_VOLT_ANGDIFF_1", "Degree")
    self.register_output("Grizzly-SwitchA6_VOLT_ANGDIFF_2", "Degree")
    self.register_output("Grizzly-SwitchA6_VOLT_ANGDIFF_3", "Degree")
    self.register_output("Grizzly-SwitchA6_CURR_ANGDIFF_1", "Degree")
    self.register_output("Grizzly-SwitchA6_CURR_ANGDIFF_1", "Degree")
    self.register_output("Grizzly-SwitchA6_CURR_ANGDIFF_1", "Degree")
    self.register_input("building1_L1")
    self.register_input("building1_L2")
    self.register_input("building1_L3")
    self.register_input("building1_C1")
    self.register_input("building1_C2")
    self.register_input("building1_C3")


  def compute(self, changed_ranges, input_streams, params, report):
    out1 = report.output("Grizzly-SwitchA6_VOLT_ANGDIFF_1")
    out2 = report.output("Grizzly-SwitchA6_VOLT_ANGDIFF_2")
    out3 = report.output("Grizzly-SwitchA6_VOLT_ANGDIFF_3")
    out4 = report.output("Grizzly-SwitchA6_CURR_ANGDIFF_1")
    out5 = report.output("Grizzly-SwitchA6_CURR_ANGDIFF_2")
    out6 = report.output("Grizzly-SwitchA6_CURR_ANGDIFF_3")
    print "compute invoked:"
    print "changed_ranges: ", changed_ranges
    print "params: ", params

    idx1 = 0
    idx2 = 0
    # matching time between data stream and skip the piont when there is no data for that time
    while idx1 < len(input_streams["building1_L1"]) and idx2 < len(input_streams["building2_L1"]):
            if grizzly_L1[idx1].time < switcha6_L1[idx2].time:
                idx1 += 1
                continue
            if grizzly_L1[idx1].time > switcha6_L1[idx2].time:
                idx2 += 1
                continue
            # compute angle difference 
            delta = grizzly_L1[idx1].value - switcha6_L1[idx2].value
            if delta > 180:
                delta =delta-360
            if delta <-180:
                delta=delta+360
            if delta ==-180:
                delta=180
            L2ang_GS.append((grizzly_L1[idx1].time, delta))
            idx1 += 1
            idx2 += 1
            
    while i1 < len(input_streams["phase"])-120 and i2 < len(input_streams["phase"]):
      p1 = input_streams["phase"][i1]
      p2 = input_streams["phase"][i2]

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
      delta_phase = p2[1]-p1[1]
      if delta_phase > 180:
        delta_phase -= 360
      if delta_phase < -180:
        delta_phase += 360
      freq = delta_phase/360.0 + 60.0
      out.addreading(time, freq)
      i1 += 1
      i2 += 1

    out.addbounds(*changed_ranges["phase"])

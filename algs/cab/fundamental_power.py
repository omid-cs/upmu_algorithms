import qdf
import numpy as np

class Fundamental_Power (qdf.QDF2Distillate):
  def initialize(self, name="default"):
    self.set_section("fund_power")
    self.set_name(name)
    self.set_version(1)
    self.register_input("voltage")
    self.register_input("current")
    self.register_input("dpf")
    self.register_output("Fundamental_Power", "Watts")

  def compute(self, changed_ranges, input_streams, params, report):
    voltage = input_streams["voltage"]
    current = input_streams["current"]
    dpf =     input_streams["dpf"]

    fundamental_power_output = report.output("Fundamental_Power")

    print "compute invoked:"
    print "changed_ranges: ", changed_ranges
    print "params: ", params

    i_vol = 0
    i_cur = 0
    i_dpf = 0
    while i_vol < len(voltage) and i_cur < len(current) and i_dpf < len(dpf):
      if not (voltage[i_vol].time == current[i_cur].time == dpf[i_dpf].time):
        # if times do not align, iteratively increment trailing streams until equal
        max_time = max(voltage[i_vol].time, current[i_cur].time, dpf[i_dpf].time)
        if voltage[i_vol].time < max_time:
          i_vol += 1
        if current[i_cur].time < max_time:
          i_cur += 1
        if dpf[i_dpf].time < max_time:
          i_dpf += 1
        continue

      # Calculate fundamental power
      time = voltage[i_vol].time
      fundamental_power = voltage[i_vol].value * current[i_cur].value * dpf[i_dpf].value
      fundamental_power_output.addreading(time, fundamental_power)

      #increment counters and loop
      i_vol += 1
      i_cur += 1
      i_dpf += 1

    fundamental_power_output.addbounds(*changed_ranges["voltage"])
    fundamental_power_output.addbounds(*changed_ranges["current"])
    fundamental_power_output.addbounds(*changed_ranges["dpf"])

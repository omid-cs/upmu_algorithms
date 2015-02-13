import qdf
import numpy as np

class Fundamental_Power (qdf.QDF2Distillate):
  def initialize(self, section="Fundamental_Power", name="fundamental_power"):
    self.set_section(section)
    self.set_name(name)
    self.set_version(1)
    self.register_input("voltage_phase")
    self.register_input("current_phase")
    self.register_input("dpf")
    self.register_output("Fundamental_Power", "Watts")

  def compute(self, changed_ranges, input_streams, params, report):
    voltage = input_streams["voltage_phase"]
    current = input_streams["current_phase"]
    dpf =     input_streams["dpf"]

    fundamental_power_output = report.output("Fundamental_Power")

    i_vol = 0
    i_cur = 0
    i_dpf = 0
    while i_vol < len(voltage) and i_cur < len(current) and i_dpf < len(dpf):
      if not (voltage[i_vol][0] == current[i_cur][0] == dpf[i_dpf][0]):
        # if times do not align, iteratively increment trailing streams until equal
        max_time = max(voltage[i_vol][0], current[i_cur][0], dpf[i_dpf][0])
        if voltage[i_vol][0] < max_time:
          i_vol += 1
        if current[i_cur][0] < max_time:
          i_cur += 1
        if dpf[i_dpf][0] < max_time:
          i_dpf += 1
        continue

      # Calculate fundamental power
      time = voltage[i_vol][0]
      fp = voltage[i_vol][1] * current[i_cur][1] * dpf[i_dpf][1]/100
      fundamental_power_output.addreading(time, fp)

      #increment counters and loop
      i_vol += 1
      i_cur += 1
      i_dpf += 1

    fundamental_power_output.addbounds(*changed_ranges["voltage_phase"])
    fundamental_power_output.addbounds(*changed_ranges["current_phase"])
    fundamental_power_output.addbounds(*changed_ranges["dpf"])

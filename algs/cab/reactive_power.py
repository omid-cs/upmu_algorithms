import qdf
import numpy as np

class Reactive_Power (qdf.QDF2Distillate):
  def initialize(self, section="Reactive_Power", name="reactive_power"):
    self.set_section(section)
    self.set_name(name)
    self.set_version(1)
    self.register_input("voltage_phase")
    self.register_input("current_phase")
    self.register_output("Reactive_Power", "VAR")

  def compute(self, changed_ranges, input_streams, params, report):
    voltage_phase = input_streams["voltage_phase"]
    current_phase = input_streams["current_phase"]

    reactive_power_output = report.output("Reactive_Power")

    i_vol = 0
    i_cur = 0
    while i_vol < len(voltage_phase) and i_cur < len(current_phase):
      if not (voltage_phase[i_vol][0] == current_phase[i_cur][0]):
        # if times do not align, iteratively increment trailing stream until equal
        max_time = max(voltage_phase[i_vol][0], current_phase[i_cur][0])
        if voltage_phase[i_vol][0] < max_time:
          i_vol += 1
        if current_phase[i_cur][0] < max_time:
          i_cur += 1
        continue

      # Calculate reactive power
      time = voltage_phase[i_vol][0]
      rp = np.sin(np.radians(voltage_phase[i_vol][1]-current_phase[i_cur][1])) #mult by magV and magC
      reactive_power_output.addreading(time, rp)

      #increment counters and loop
      i_vol += 1
      i_cur += 1

    reactive_power_output.addbounds(*changed_ranges["voltage_phase"])
    reactive_power_output.addbounds(*changed_ranges["current_phase"])

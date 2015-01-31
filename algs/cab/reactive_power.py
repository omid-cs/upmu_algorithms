import qdf
import numpy as np

class Reactive_Power (qdf.QDF2Distillate):
  def initialize(self, name="default"):
    self.set_section("reactive_power")
    self.set_name(name)
    self.set_version(1)
    self.register_input("voltage_phase")
    self.register_input("current_phase")
    self.register_output("Reactive_Power", "Watts")

  def compute(self, changed_ranges, input_streams, params, report):
    voltage_phase = input_streams["voltage_phase"]
    current_phase = input_streams["current_phase"]

    reactive_power_output = report.output("Reactive_Power")

    print "compute invoked:"
    print "changed_ranges: ", changed_ranges
    print "params: ", params

    i_vol = 0
    i_cur = 0
    while i_vol < len(voltage_phase) and i_cur < len(current_phase):
      if not (voltage_phase[i_vol].time == current_phase[i_cur].time):
        # if times do not align, iteratively increment trailing stream until equal
        max_time = max(voltage_phase[i_vol].time, current_phase[i_cur].time)
        if voltage_phase[i_vol].time < max_time:
          i_vol += 1
        if current_phase[i_cur].time < max_time:
          i_cur += 1
        continue

      # Calculate reactive power
      time = voltage_phase[i_vol].time
      rp = np.sin(np.radians(voltage_phase[i_vol].value-current_phase[i_cur].value))
      reactive_power_output.addreading(time, rp)

      #increment counters and loop
      i_vol += 1
      i_cur += 1

    reactive_power_output.addbounds(*changed_ranges["voltage_phase"])
    reactive_power_output.addbounds(*changed_ranges["current_phase"])

import qdf
import numpy as np

class Reactive_Power (qdf.QDF2Distillate):
  def initialize(self, section="Reactive_Power", name="reactive_power"):
    self.set_section(section)
    self.set_name(name)
    self.set_version(1)
    self.register_input("voltage_phase")
    self.register_input("current_phase")
    self.register_input("voltage_mag")
    self.register_input("current_mag")
    self.register_output("REACTIVE_POWER", "VAR")

  def compute(self, changed_ranges, input_streams, params, report):
    voltage_phase = input_streams["voltage_phase"]
    current_phase = input_streams["current_phase"]
    voltage_mag = input_streams["voltage_mag"]
    current_mag = input_streams["current_mag"]

    reactive_power_output = report.output("REACTIVE_POWER")

    i_vol_phase = 0
    i_cur_phase = 0
    i_vol_mag = 0
    i_cur_mag = 0
    
    while i_vol_phase < len(voltage_phase) and i_cur_phase < len(current_phase) and i_vol_mag < len(voltage_mag) and i_cur_mag < len(current_mag):
      if not (voltage_phase[i_vol_phase][0] == current_phase[i_cur_phase][0] == voltage_mag[i_vol_mag][0] == current_mag[i_cur_mag][0]):
        # if times do not align, iteratively increment trailing stream until equal
        max_time = max(voltage_phase[i_vol_phase][0], current_phase[i_cur_phase][0],voltage_mag[i_vol_mag][0],current_mag[i_cur_mag][0])
        if voltage_phase[i_vol][0] < max_time:
          i_vol_phase += 1
        if current_phase[i_cur][0] < max_time:
          i_cur_phase += 1
        if voltage_mag[i_vol_mag][0] < max_time:
          i_vol_mag += 1
        if current_mag[i_cur_mag][0] < max_time:
          i_cur_mag += 1
        continue

      # Calculate reactive power
      time = voltage_phase[i_vol_phase][0]
      rp = voltage_mag[i_vol_mag][1]*current_mag[i_cur_mag][1]*np.sin(np.radians(voltage_phase[i_vol_phase][1]- voltage_phase[i_cur_phase][1]))
      #rp = np.sin(np.radians(voltage_phase[i_vol][1]-current_phase[i_cur][1])) #mult by magV and magC
      reactive_power_output.addreading(time, rp)

      #increment counters and loop
      i_vol_mag += 1
      i_cur_mag += 1
      i_vol_phase += 1
      i_cur_phase += 1

    reactive_power_output.addbounds(*changed_ranges["voltage_phase"])
    reactive_power_output.addbounds(*changed_ranges["current_phase"])
    reactive_power_output.addbounds(*changed_ranges["voltage_mag"])
    reactive_power_output.addbounds(*changed_ranges["current_mag"])

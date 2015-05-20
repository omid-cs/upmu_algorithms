import qdf
import numpy as np

class RPFP (qdf.QDF2Distillate):
  def initialize(self, section="Reactive_Power", name="reactive_power"):
    self.set_section(section)
    self.set_name(name)
    self.set_version(1)
    self.register_input("voltage_phase")
    self.register_input("current_phase")
    self.register_input("voltage_mag")
    self.register_input("current_mag")
    self.register_output("REACTIVE-POWER", "VAR")
    self.register_output("FUNDAMENTAL-POWER", "W")

  def compute(self, changed_ranges, input_streams, params, report):
    voltage_phase = input_streams["voltage_phase"]
    current_phase = input_streams["current_phase"]
    voltage_mag = input_streams["voltage_mag"]
    current_mag = input_streams["current_mag"]

    REACTIVE_POWER = report.output("REACTIVE-POWER")
    FUNDAMENTAL_POWER = report.output("FUNDAMENTAL-POWER")
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
      fp = voltage_mag[i_vol_mag][1]*current_mag[i_cur_mag][1]*np.cos(np.radians(voltage_phase[i_vol_phase][1])- np.radians(current_phase[i_cur_phase][1]))
      rp = voltage_mag[i_vol_mag][1]*current_mag[i_cur_mag][1]*np.sin(np.radians(voltage_phase[i_vol_phase][1])- np.radians(current_phase[i_cur_phase][1]))
      REACTIVE_POWER.addreading(time, rp)
      FUNDAMENTAL_POWER.addreading(time, fp)

      #increment counters and loop
      i_vol_mag += 1
      i_cur_mag += 1
      i_vol_phase += 1
      i_cur_phase += 1

    REACTIVE_POWER.addbounds(*changed_ranges["voltage_phase"])
    REACTIVE_POWER.addbounds(*changed_ranges["current_phase"])
    REACTIVE_POWER.addbounds(*changed_ranges["voltage_mag"])
    REACTIVE_POWER.addbounds(*changed_ranges["current_mag"])
    FUNDAMENTAL_POWER.addbounds(*changed_ranges["voltage_phase"])
    FUNDAMENTAL_POWER.addbounds(*changed_ranges["current_phase"])
    FUNDAMENTAL_POWER.addbounds(*changed_ranges["voltage_mag"])
    FUNDAMENTAL_POWER.addbounds(*changed_ranges["current_mag"])

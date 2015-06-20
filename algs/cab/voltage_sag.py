import qdf
import numpy as np

class Voltage_Sag(qdf.QDF2Distillate):
	def initialize(self, section = "EventDetection", name = "default"):
		self.set_section(section)
		self.set_name(name)
		self.set_version(6)
		self.register_input("Mag")
		self.register_output("outliers_output", "none")


	def compute(self, changed_ranges, input_streams, params, report):
		voltage_mag = input_streams["Mag"]
		i_vol_mag = 0
		count = 0
		nominal_voltage = 120
		voltage_sag_boolean = False
		mag_list = []
		outliers_output = report.output("outliers_output")
		
		while i_vol_mag < len(voltage_mag):
			mag = voltage_mag[i_vol_mag][1]
			time = voltage_mag[i_vol_mag][0]

			#check if voltage_sag_boolean is true or not if true add reading of 1 after every 60 seconds or 120 samples assuming nothing lost
			if voltage_sag_boolean:
				outliers_output.addreading(time,1)
			else:
				outliers_output.addreading(time,0)

			mag_list.extend([mag])
			count += 1

			if count >= 2 and max(mag_list) <= 0.98 * nominal_voltage:
				voltage_sag_boolean = True
				#skip ahead to next minute if that is the case
				i_vol_mag = i_vol_mag + (120 - count)
			elif count >= 24 and max(mag_list) <= 0.7 * nominal_voltage:
				voltage_sag_boolean = True
				i_vol_mag = i_vol_mag + (120 - count)
			elif count >= 32 and max(mag_list) <= 0.8 * nominal_voltage:
				voltage_sag_boolean = True
				i_vol_mag = i_vol_mag + (120 - count)
			else:
				i_vol_mag += 1

			if count == 120:
				#reinitialize count and mag array
				count = 0
				mag_list = []
				voltage_sag_boolean = False

		
		outliers_output.addbounds(*changed_ranges["Mag"])


		#overcurrent in I1,2,3 more than %500 than previous time steps (determine previous number of time steps 10 time step.)
		#correlation between V1,2,3 and I1,2,3 what is the meaning of V and I correlation sys impedance
		#Phase angle difference between V and I 
		#Same for the other PMU
		#correlation
		#download data for one day Tuesday February 17th
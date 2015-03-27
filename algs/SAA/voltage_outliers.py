import qdf
import numpy as np

class Voltage_Outliers(qdf.QDF2Distillate):
	def initialize(self, section = "EventDetection", name = "default"):
		self.set_section(section)
		self.set_name(name)
		self.set_version(3)
		self.register_input("Mag")
		self.register_output("outliers_output", "none")


	def compute(self, changed_ranges, input_streams, params, report):
		#outliers in V1,3,4 mg +- 10 percent of Voltage
		voltage_mag = input_streams["Mag"]
		i_vol_mag = 0
		outliers_output = report.output("outliers_output")
		while i_vol_mag < len(voltage_mag):
			time = voltage_mag[i_vol_mag][0]
			mag = voltage_mag[i_vol_mag][1]
			if mag < 108 or mag > 132:
				outliers_output.addreading(time,1)
			else:
				outliers_output.addreading(time,0)

			i_vol_mag += 1
		
		outliers_output.addbounds(*changed_ranges["Mag"])


		#overcurrent in I1,2,3 more than %500 than previous time steps (determine previous number of time steps 10 time step.)
		#correlation between V1,2,3 and I1,2,3 what is the meaning of V and I correlation sys impedance
		#Phase angle difference between V and I 
		#Same for the other PMU
		#correlation
		#download data for one day Tuesday February 17th 


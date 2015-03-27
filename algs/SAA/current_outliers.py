import qdf
import numpy as np

class Current_Outliers(qdf.QDF2Distillate):
	def initialize(section, name):
		self.set_section(section)
		self.set_name(name)
		self.set_version(2)
		self.register_input("Mag")
		self.register_output("outliers_output", "none")


	def compute(self, changed_ranges, input_streams, params, report):
		current_mag = input_streams["Mag"]
		i_cur_mag = 0
		outliers_output = report.output("outliers_output")
		while i_cur_mag < len(current_mag):
			#first calculate average of previous 10 time-steps
			total = 0
			for i_prev in range(i_cur_mag - 10, i_cur_mag):
				total += current_mag[i_prev][1]
			avg= total/10
			threshold = avg*5
			time = current_mag[i_cur_mag][0]
			mag = current_mag[i_cur_mag][1]
			if mag < threshold:
				outliers_output.addreading(time,1)
			else:
				outliers_output.addreading(time,0)

			i_cur_mag += 1
		
		outliers_output.addbounds(*changed_ranges["Mag"])
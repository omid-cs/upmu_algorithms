import qdf
import numpy as np

class svd(qdf.QDF2Distillate):
	def initialize(self, section , name ):
		self.set_section(section)
		self.set_name(name)
		self.set_version(1)
		self.register_input("L1-E")
		self.register_input("L2-E")
		self.register_input("L3-E")
		self.register_input("C1")
		self.register_input("C2")
		self.register_input("C3")
		self.register_input("L1-E_angle")
		self.register_input("L2-E_angle")
		self.register_input("L3-E_angle")
		self.register_input("C1_angle")
		self.register_input("C2_angle")
		self.register_input("C3_angle")
		self.register_output("svd_output","none")
		#take the two signals impose a window on them and 


	def compute(self, changed_ranges, input_streams, params, report):
		#outliers in V1,3,4 mg +- 10 percent of Voltage
		L1_E = input_streams["L1-E"]
		L2_E = input_streams["L2-E"]
		L3_E = input_streams["L3-E"]
		C1 = input_streams["C1"]
		C2 = input_streams["C2"]
		C3 = input_streams["C3"]
		L1_E_angle = input_streams["L1-E_angle"]
		L2_E_angle = input_streams["L2-E_angle"]
		L3_E_angle = input_streams["L3-E_angle"]
		C1_angle = input_streams["C1_angle"]
		C2_angle = input_streams["C2_angle"]
		C3_angle = input_streams["C3_angle"]
		svd_output = report.output("svd_output")
		


		#initialize index vector
		ind_vector = [0]*12
		#initialize ind_vector list
		ind_vector_list = []
		#define window size
		windowsize = 12


		while len(ind_vector_list) < windowsize:
			#now get the time vector
			time_vector = [L1_E[ind_vector[0]][0], L2_E[ind_vector[1]][0], L3_E[ind_vector[2]][0],C1[ind_vector[3]][0],C2[ind_vector[4]][0],C3[ind_vector[5]][0],L1_E_angle[ind_vector[6]][0],L2_E_angle
[ind_vector[7]][0],L3_E_angle[ind_vector[8]][0],C1_angle[ind_vector[9]][0],C2_angle[ind_vector[10]][0],C3_angle[ind_vector[11]][0]]
			#check if all elements of timevector the same
			lined_up = all(x == time_vector[0] for x in time_vector)
			#if the vectors are not lined up find the signal that is furthest in time
			if not lined_up:
				m = max(time_vector)
				#used the above to get the signals that need to be shifted
				shifted_signals = [i for i, j in enumerate(time_vector) if j != m]
				#now shift these signals
				for i in shifted_signals:
					ind_vector[i]+=1
			else:
				#record the index vector if they have indeed lined up.
				ind_vector_list.extend([ind_vector])
				#now shift the whole ind_vector over by one
				ind_vector = [x + 1 for x in ind_vector]
				#continue this up until you get the first window



		length_vector = [len(L1_E), len(L2_E), len(L3_E), len(C1), len(C2), len(C3), len(L1_E_angle), len(L2_E_angle), len(L3_E_angle), len(C1_angle), len(C2_angle),len(C3_angle)]
		#once the window is lined up perform the svd calculation this first involves building the matrix necessary for the svd function
		lined_up = True
		while all(np.less(ind_vector,length_vector)):

			if lined_up:
				mag_vector = []
				mag_vector_list = []
				for i in range(0,len(ind_vector_list)):
					ind_vector = ind_vector_list[i]
					mag_vector = [L1_E[ind_vector[0]][1], L2_E[ind_vector[1]][1], L3_E[ind_vector[2]][1],C1[ind_vector[3]][1],C2[ind_vector[4]][1],C3[ind_vector[5]][1],L1_E_angle[ind_vector[6]][1],L2_E_angle
		[ind_vector[7]][1],L3_E_angle[ind_vector[8]][1],C1_angle[ind_vector[9]][1],C2_angle[ind_vector[10]][1],C3_angle[ind_vector[11]][1]]
					mag_vector_list.extend([mag_vector])
					mag_vector = []

				mag_matrix = np.array(mag_vector_list)
				#now that matrix is created use in build svd function
				U,s,V = np.linalg.svd(mag_matrix)
				#get the time for which to assign the reading time should be the same for all values in a row therefore
				time = L1_E[ind_vector_list[0][0]][0]
				svd_output.addreading(time,s[0])
				#now shift over everything by one
				ind_vector_list = ind_vector_list[1:]



			time_vector = [L1_E[ind_vector[0]][0], L2_E[ind_vector[1]][0], L3_E[ind_vector[2]][0],C1[ind_vector[3]][0],C2[ind_vector[4]][0],C3[ind_vector[5]][0],L1_E_angle[ind_vector[6]][0],L2_E_angle
[ind_vector[7]][0],L3_E_angle[ind_vector[8]][0],C1_angle[ind_vector[9]][0],C2_angle[ind_vector[10]][0],C3_angle[ind_vector[11]][0]]
			lined_up = all(x == time_vector[0] for x in time_vector)
			#if the vectors are not lined up find the signal that is furthest in time
			if not lined_up:
				m = max(time_vector)
				#used the above to get the signals that need to be shifted
				shifted_signals = [i for i, j in enumerate(time_vector) if j == m]
				#now shift these signals
				for i in shifted_signals:
					ind_vector[i]+=1
			else:
				#record the index vector if they have indeed lined up.
				ind_vector_list.extend([ind_vector])
				#now shift the whole ind_vector over by one
				ind_vector = [x + 1 for x in ind_vector]
				#continue this up until you get the first window




		svd_output.addbounds(*changed_ranges["L1-E"])
		svd_output.addbounds(*changed_ranges["L2-E"])
		svd_output.addbounds(*changed_ranges["L3-E"])
		svd_output.addbounds(*changed_ranges["C1"])
		svd_output.addbounds(*changed_ranges["C2"])
		svd_output.addbounds(*changed_ranges["C3"])
		svd_output.addbounds(*changed_ranges["L1-E_angle"])
		svd_output.addbounds(*changed_ranges["L2-E_angle"])
		svd_output.addbounds(*changed_ranges["L3-E_angle"])
		svd_output.addbounds(*changed_ranges["C1_angle"])
		svd_output.addbounds(*changed_ranges["C2_angle"])
		svd_output.addbounds(*changed_ranges["C3_angle"])
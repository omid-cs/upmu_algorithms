import qdf
import numpy as np

class Correlation(qdf.QDF2Distillate):
	def initialize(self, section , name ):
		self.set_section(section)
		self.set_name(name)
		self.set_version(3)
		self.register_input("Signal1")
		self.register_input("Signal2")
		self.register_output("correlation_output","none")
		#take the two signals impose a window on them and 


	def compute(self, changed_ranges, input_streams, params, report):
		#outliers in V1,3,4 mg +- 10 percent of Voltage
		Signal1 = input_streams["Signal1"]
		Signal2 = input_streams["Signal2"]
		correlation_output = report.output("correlation_output")
		i_correlation = 0
		i_Signal1 = 0
		i_Signal2 = 0
		windowsize = 600
		while i_Signal1 < (len(Signal1) - 1200) and i_Signal2 < (len(Signal2) - 1200): #this should be replaced with a time restriction
			#construct a signal for which 10 elements are lined up so that the correlation may be calculated
			#first construct array of n number of elements which line up
			i_Signal1_array = np.array([])
			i_Signal2_array = np.array([])
			#600 elements
			#line up window
			while len(i_Signal1_array)< windowsize and len(i_Signal2_array) < windowsize:
				#if the time at a particular index of signal 1 is not equal to the time at the index of signal 2 increment the index of one of the
				# signal for which the time is lower
				if not (Signal1[i_Signal1][0] == Signal2[i_Signal2][0]):
					max_time = max(Signal1[i_Signal1][0],Signal2[i_Signal2][0])
					if Signal1[i_Signal1][0] < max_time:
						i_Signal1 += 1
					elif Signal2[i_Signal2][0] < max_time:
						i_Signal2 += 1
				else:
					i_Signal1_array = np.append(i_Signal1_array,i_Signal1)
					i_Signal2_array = np.append(i_Signal2_array,i_Signal2)

			#once window has been lined up perform calculation
			print type(Signal1)
			print type(i_Signal1_array)
			covariance_matrix = np.cov(Signal1[i_Signal1_array],Signal2[i_Signal2_array])
			co = covariance_matrix[0,1]
			window_starttime = Signal1[i_Signal1_array[0]][0]
			window_endtime = Signal1[i_Signal1_array[-1]][0]
			correlation_output.addreading(window_starttime,co)
			#shift window over by 1 step and recalculate covariance
			i_Signal1 = i_Signal1_array[1]
			i_Signal2 = i_Signal2_array[1]
			i_correlation += 1
		

		outliers_output.addbounds(*changed_ranges["Signal1"])
		outliers_output.addbounds(*changed_ranges["Signal2"])

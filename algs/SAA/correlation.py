import qdf
import numpy as np

class Correlation(qdf.QDF2Distillate):
	def initialize(self, section , name ):
		self.set_section(section)
		self.set_name(name)
		self.set_version(5)
		self.register_input("Signal1")
		self.register_input("Signal2")
		self.register_output("correlation_output","none")
		#take the two signals impose a window on them and 


	def compute(self, changed_ranges, input_streams, params, report):
		#outliers in V1,3,4 mg +- 10 percent of Voltage
		Signal1 = input_streams["Signal1"]
		Signal2 = input_streams["Signal2"]
		correlation_output = report.output("correlation_output")
		i_Signal1 = 0
		i_Signal2 = 0
		windowsize = 10

		i_Signal1_array = []
		i_Signal2_array = []

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
				i_Signal1_array.extend([i_Signal1])
				i_Signal2_array.extend([i_Signal2])
				i_Signal1 += 1
				i_Signal2 += 1


		print i_Signal1_array
		print i_Signal2_array
		print len(i_Signal1_array)
		print len(i_Signal2_array)
		i_Signal1end = i_Signal1_array[-1]
		i_Signal2end = i_Signal2_array[-1]
		i_Signal1 = i_Signal1_array[0]
		i_Signal2 = i_Signal2_array[0]
		
		while i_Signal1end < (len(Signal1)) and i_Signal2end < (len(Signal2)): #this should be replaced with a time restriction


			#once window has been lined up perform calculation
			windowed_signal1 = [Signal1[i][1] for i in i_Signal1_array]
			windowed_signal2 = [Signal2[i][1] for i in i_Signal2_array]
			covariance_matrix = np.cov(windowed_signal1,windowed_signal2)
			co = covariance_matrix[0,1]
			window_starttime = Signal1[i_Signal1_array[0]][0]
			window_endtime = Signal1[i_Signal1_array[-1]][0]
			correlation_output.addreading(window_starttime,co)
			#shift over start of window
			i_Signal1_array = i_Signal1_array[1:]
			i_Signal2_array = i_Signal1_array[1:]
			i_Signal1 = i_Signal1_array[-1]
			i_Signal2 = i_Signal2_array[-1]
			#find suitable end point of window by finding index at which they line up

			while len(i_Signal1_array)< windowsize and len(i_Signal2_array) < windowsize:
			#if the time at a particular index of signal 1 is not equal to the time at the index of signal 2 increment the index of one of the
			# signal for which the time is lower
				if i_Signal1 > len(Signal1) or i_Signal2 > len(Signal2):
					break
				if not (Signal1[i_Signal1][0] == Signal2[i_Signal2][0]):
					max_time = max(Signal1[i_Signal1][0],Signal2[i_Signal2][0])
					if Signal1[i_Signal1][0] < max_time:
							i_Signal1 += 1
					elif Signal2[i_Signal2][0] < max_time:
							i_Signal2 += 1
				else:
					i_Signal1_array.extend([i_Signal1])
					i_Signal2_array.extend([i_Signal2])
					i_Signal1 +=1
					i_Signal2 +=1

			i_Signal1end = i_Signal1_array[-1]
			i_Signal2end = i_Signal2_array[-1]

		

		outliers_output.addbounds(*changed_ranges["Signal1"])
		outliers_output.addbounds(*changed_ranges["Signal2"])

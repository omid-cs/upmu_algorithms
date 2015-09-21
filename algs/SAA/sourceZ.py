import qdf
import numpy as np

class sourceZ (qdf.QDF2Distillate):

	def initialize(self, section, name):
		self.set_section(section)
		self.set_name(name)
		self.set_version(1)
		self.register_input("voltage_phase")
		self.register_input("current_phase")
		self.register_input("voltage_mag")
		self.register_input("current_mag")
		self.register_output("tanAng", "deg")
		self.register_output("MagZ", "Ohm")

    def compute(self, changed_ranges, input_streams, params, report):
	    voltage_phase = input_streams["voltage_phase"]
	    current_phase = input_streams["current_phase"]
	    voltage_mag = input_streams["voltage_mag"]
	    current_mag = input_streams["current_mag"]

	    tanAng = report.output("tanAng")
	    MagZ = report.output("MagZ")
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

		    #now peform calculation and output stream
		    time = voltage_phase[i_vol_phase][0]
		    tanAng = np.degrees(np.tan(voltage_mag[i_vol_phase] - current_phase[i_cur_phase]))
		    MagZ = np.divide(voltage_mag[i_vol_mag],current_mag[i_cur_mag])
		    tanAng.addreading(time,tanAng)
		    MagZ.addreading(time,tanAng)

	    	#increment counter now that calculation is performed for this data point
	    	i_vol_phase += 1
	    	i_cur_phase += 1
	    	i_vol_mag += 1
	    	i_cur_mag += 1
	    

	    MagZ.addbounds(*changed_ranges["voltage_phase"])
	    MagZ.addbounds(*changed_ranges["current_phase"])
	    MagZ.addbounds(*changed_ranges["voltage_mag"])
	    MagZ.addbounds(*changed_ranges["current_mag"])
	    tanAng.addbounds(*changed_ranges["voltage_phase"])
	    tanAng.addbounds(*changed_ranges["current_phase"])
	    tanAng.addbounds(*changed_ranges["voltage_mag"])
	    tanAng.addbounds(*changed_ranges["current_mag"])

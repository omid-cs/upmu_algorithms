import qdf
import numpy as np
class DPF (qdf.QDF2Distillate):
    def initialize(self, section, name):
        self.set_section(section)
        self.set_name(name)
        self.set_version(6)
        self.register_output("DPF", "Percent")
        self.register_input("voltage_phase")
        self.register_input("current_phase")

    def compute(self, changed_ranges, input_streams, params, report):
        DPF = report.output("DPF")
        print "compute invoked:"
        print "changed_ranges: ", changed_ranges
        print "params: ", params
        idx_voltage=0
        idx_current=0

        voltage = input_streams["voltage_phase"]
        current = input_streams["current_phase"]

        while idx_voltage < len(voltage) and idx_current < len(current) :
            if current[idx_current][0] < voltage[idx_voltage][0]:
                idx_current += 1
            if voltage[idx_voltage][0] < current[idx_current][0]:
                idx_voltage += 1

            # compute cosin value of the differnece between voltage angle and current angle and dpf
            dpf1=(np.cos(np.radians(voltage[idx_voltage][1]-current[idx_current][1])))*100
            DPF.addreading(voltage[idx_voltage][0],dpf1)
            idx_voltage += 1
            idx_current += 1

        DPF.addbounds(*changed_ranges["voltage_phase"])
        DPF.addbounds(*changed_ranges["current_phase"])

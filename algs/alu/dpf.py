import qdf
import numpy as np
class sequence (qdf.QDF2Distillate):
    def initialize(self, section, name):
        self.set_section(section)
        self.set_name(name)
        self.set_version(1)
        self.register_output("L1_DPF", "Precent")
        self.register_output("L2_DPF", "Precent")
        self.register_output("L3_DPF", "Precent")
        self.register_input("L1")
        self.register_input("L2")
        self.register_input("L3")
        self.register_input("C1")
        self.register_input("C2")
        self.register_input("C3")

    def compute(self, changed_ranges, input_streams, params, report):
        L1_DPF = report.output("L1_DPF")
        L2_DPF = report.output("L2_DPF")
        L3_DPF = report.output("L3_DPF")
        print "compute invoked:"
        print "changed_ranges: ", changed_ranges
        print "params: ", params
        idxL1=0
        idxL2=0
        idxL3=0
        idxC1=0
        idxC2=0
        idxC3=0

        L1=input_streams["L1"]
        L2=input_streams["L2"]
        L3=input_streams["L3"]
        C1=input_streams["C1"]
        C2=input_streams["C2"]
        C3=input_streams["C3"]

        while idxC1 len(C1) and idxL1< len(L1) :
            if not (C1[idxC1].time == L1[idxL1].time):
                max_time=max(C1[idxC1].time,L1[idxL1].time)
                if C1[idxC1].time < max_time:
                    idxC1 += 1
                if L1[idxL1].time < max_time:
                    idxL1 += 1
                continue
            # compute cosin value of the differnece between voltage angle and current angle and dpf
            dpf1=(np.cos(np.radians(L1[idxL1].value-C1[idxC1].value)))*100
            L1_DPF.addreading((L1[idxL1].time,dpf1))
            idxL1+=1
            idxC1+=1
            
        while idxC2 len(C2) and idxL2< len(L2) :
            if not (C2[idxC2].time == L2[idxL2].time):
                max_time=max(C2[idxC2].time,L2[idxL2].time)
                if C2[idxC2].time < max_time:
                    idxC2 += 1
                if L2[idxL2].time < max_time:
                    idxL2 += 1
                continue
            # compute cosin value of the differnece between voltage angle and current angle and dpf
            dpf2=(np.cos(np.radians(L2[idxL2].value-C2[idxC2].value)))*100
            L2_DPF.addreading((L2[idxL2].time,dpf2))
            idxL2+=1
            idxC2+=1
            
        while idxC3 len(C3) and idxL3< len(L3) :
            if not (C3[idxC3].time == L3[idxL3].time):
                max_time=max(C3[idxC3].time,L3[idxL3].time)
                if C3[idxC3].time < max_time:
                    idxC3 += 1
                if L3[idxL3].time < max_time:
                    idxL3 += 1
                continue
            # compute cosin value of the differnece between voltage angle and current angle and dpf
            dpf3=(np.cos(np.radians(L3[idxL3].value-C3[idxC3].value)))*100
            L3_DPF.addreading((L3[idxL3].time,dpf3))
            idxL3+=1
            idxC3+=1    
        l1_DPF.addbounds(*changed_ranges["L1"])
        L1_DPF.addbounds(*changed_ranges["C1"])
        l2_DPF.addbounds(*changed_ranges["L2"])
        L2_DPF.addbounds(*changed_ranges["C2"])
        L3_DPF.addbounds(*changed_ranges["L3"])
        L3_DPF.addbounds(*changed_ranges["C3"])

from distillate import Distillate
import numpy as np
import math
import qdf


class DPF(qdf.QDF2Distillate):
    def initialize(self, name="default"):
        self.set_section("DPF")
        self.set_name(name)
        self.set_version(1)
        self.register_input("Grizzly-SwitchA6_VOLT_ANGDIFF")
        self.register_input("Grizzly-SwitchA6_CURR_ANGDIFF")
        self.register_output("dpf", "percent")                     

    def compute(input_streams):
        # data input
        LAAng = input_streams["Grizzly-SwitchA6_VOLT_ANGDIFF"]
        CAAng = input_streams["Grizzly-SwitchA6_CURR_ANGDIFF"]
        dpf_output = report.output("dpf")
        idxCA=0
        idxLA=0
        # matching time among all 6 data strams to make sure they are at same time before compute sequence
        while idxCA < len(CAAng) and idxLA < len(LAAng):
            if CAAng[idxCA].time < LAAng[idxLA].time:
                idxCA += 1
                continue
            if CAAng[idxCA].time > LAAng[idxLA].time:
                idxLA += 1
                continue
           # compute cosin value of the differnece between voltage angle and current angle and dpf
            dpfa=(np.cos(np.radians(LAAng[idxLA].value-CAAng[idxCA].value)))*100
            dpf_output.addreading((LAAng[idxLA][0],dpfa))
            idxCA+=1
            idxLA+=1
        dpf_output.addbounds(*changedranges["LAAng"])
        dpf_output.addbounds(*changedranges["CAAng"])
            

        
        
        
    
# opts = { 'input_streams'  : ['upmu/bank_514/L1ANG','upmu/bank_514/C1ANG','upmu/bank_514/L2ANG',
#                              'upmu/bank_514/C2ANG','upmu/bank_514/L3ANG','upmu/bank_514/C3ANG'], \
#          'input_uids'     : ['3c73d7ca-80ba-11e4-b1c9-002590e8ec24','3c73c866-80ba-11e4-b1c9-002590e8ec24',
#                              '3c73cb86-80ba-11e4-b1c9-002590e8ec24','3c73ce92-80ba-11e4-b1c9-002590e8ec24',
#                              '3c73af34-80ba-11e4-b1c9-002590e8ec24','3c73c514-80ba-11e4-b1c9-002590e8ec24'], \
#          'start_date'     : '2015-01-01T00:00:00.000000', \
#          'end_date'       : '2015-01-20T12:59:59.000000', \
#          'output_streams' : ['L3_DPF','L1_DPF','L2_DPF'], \
#          'output_units'   : ['Precent','Precent','Precent'], \
#          'author'         : 'Calculated Bank_514', \
#          'name'           : 'Displacement Power Factor', \
#          'version'        : 17, \
#          'algorithm'      : compute }        
# qdf.register(Distillate(), opts)
# qdf.begin()

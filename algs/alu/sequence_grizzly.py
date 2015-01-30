import qdf
import numpy as np
class Frequency (qdf.QDF2Distillate):
def initialize(self, name="sequence"):
self.set_section("Calculated Grizzly/Sequence Components")
self.set_name(name)
self.set_version(1)
self.register_output("VOLTAGE_ZERO_SEQ_ANG", "Degree")
self.register_output("VOLTAGE_ZERO_SEQ_MAG", "V")
self.register_output("VOLTAGE_POSITIVE_SEQ_ANG", "Degree")
self.register_output("VOLTAGE_POSITIVE_SEQ_MAG", "V")
self.register_output("VOLTAGE_NEGATIVE_SEQ_ANG", "Degree")
self.register_output("VOLTAGE_NEGATIVE_SEQ_MAG", "V")
self.register_output("VOLTAGE_UNBALANCE_NEG_SEQ", "Precent")
self.register_output("VOLTAGE_UNBALANCE_ZERO_SEQ", "Precent")

self.register_input("ML1")
self.register_input("ML2")
self.register_input("ML3")
self.register_input("AL1")
self.register_input("AL2")
self.register_input("AL3")
self.register_input("MC1")
self.register_input("MC2")
self.register_input("MC3")
self.register_input("AC1")
self.register_input("AC2")
self.register_input("AC3")
def compute(self, changed_ranges, input_streams, params, report):
out1 = report.output("VOLTAGE_ZERO_SEQ_ANG")
out2 = report.output("VOLTAGE_ZERO_SEQ_MAG")
out3 = report.output("VOLTAGE_POSITIVE_SEQ_ANG")
out4 = report.output("VOLTAGE_POSITIVE_SEQ_MAG")
out5 = report.output("VOLTAGE_NEGATIVE_SEQ_ANG")
out6 = report.output("VOLTAGE_NEGATIVE_SEQ_MAG")
out7 = report.output("VOLTAGE_UNBALANCE_NEG_SEQ")
out8 = report.output("VOLTAGE_UNBALANCE_ZERO_SEQ")
print "compute invoked:"
print "changed_ranges: ", changed_ranges
print "params: ", params

idxLBA=0
idxLBM=0
idxLCA=0
idxLCM=0
idxLAA=0
idxLAM=0


# matching time between data stream and skip the piont when there is no data for that time
while idx1 < len(input_streams["building1_L1"]) and idx2 < len(input_streams["building2_L1"]):
b1=input_streams["building1_L1"][idx1]
b2=input_streams["building2_L1"][idx2]
if b1[0] < b2[0]:
idx1 += 1
continue
if b1[0] > b2[0]:
idx2 += 1
continue
# compute angle difference
delta = b1[1] - b2[1]
if delta > 180:
delta =delta-360
if delta <-180:
delta=delta+360
if delta ==-180:
delta=180
out1.addreading(b1[0], delta)
idx1 += 1
idx2 += 1
idx1 = 0
idx2 = 0
# matching time between data stream and skip the piont when there is no data for that time
while idx1 < len(input_streams["building1_L2"]) and idx2 < len(input_streams["building2_L2"]):
b1=input_streams["building1_L2"][idx1]
b2=input_streams["building2_L2"][idx2]
if b1[0] < b2[0]:
idx1 += 1
continue
if b1[0] > b2[0]:
idx2 += 1
continue
# compute angle difference
delta = b1[1] - b2[1]
if delta > 180:
delta =delta-360
if delta <-180:
delta=delta+360
if delta ==-180:
delta=180
out2.addreading(b1[0], delta)
idx1 += 1
idx2 += 1
idx1 = 0
idx2 = 0
# matching time between data stream and skip the piont when there is no data for that time
while idx1 < len(input_streams["building1_L3"]) and idx2 < len(input_streams["building2_L3"]):
b1=input_streams["building1_L3"][idx1]
b2=input_streams["building2_L3"][idx2]
if b1[0] < b2[0]:
idx1 += 1
continue
if b1[0] > b2[0]:
idx2 += 1
continue
# compute angle difference
delta = b1[1] - b2[1]
if delta > 180:
delta =delta-360
if delta <-180:
delta=delta+360
if delta ==-180:
delta=180
out3.addreading(b1[0], delta)
idx1 += 1
idx2 += 1
idx1 = 0
idx2 = 0
# matching time between data stream and skip the piont when there is no data for that time
while idx1 < len(input_streams["building1_C1"]) and idx2 < len(input_streams["building2_C1"]):
b1=input_streams["building1_C1"][idx1]
b2=input_streams["building2_C1"][idx2]
if b1[0] < b2[0]:
idx1 += 1
continue
if b1[0] > b2[0]:
idx2 += 1
continue
# compute angle difference
delta = b1[1] - b2[1]
if delta > 180:
delta =delta-360
if delta <-180:
delta=delta+360
if delta ==-180:
delta=180
out4.addreading(b1, delta)
idx1 += 1
idx2 += 1
idx1 = 0
idx2 = 0
# matching time between data stream and skip the piont when there is no data for that time
while idx1 < len(input_streams["building1_C2"]) and idx2 < len(input_streams["building2_C2"]):
b1=input_streams["building1_C2"][idx1]
b2=input_streams["building2_C2"][idx2]
if b1[0] < b2[0]:
idx1 += 1
continue
if b1[0] > b2[0]:
idx2 += 1
continue
# compute angle difference
delta = b1[1] - b2[1]
if delta > 180:
delta =delta-360
if delta <-180:
delta=delta+360
if delta ==-180:
delta=180
out5.addreading(b1, delta)
idx1 += 1
idx2 += 1
idx1 = 0
idx2 = 0
# matching time between data stream and skip the piont when there is no data for that time
while idx1 < len(input_streams["building1_C3"]) and idx2 < len(input_streams["building2_C3"]):
b1=input_streams["building1_C3"][idx1]
b2=input_streams["building2_C3"][idx2]
if b1[0] < b2[0]:
idx1 += 1
continue
if b1[0] > b2[0]:
idx2 += 1
continue
# compute angle difference
delta = b1[1] - b2[1]
if delta > 180:
delta =delta-360
if delta <-180:
delta=delta+360
if delta ==-180:
delta=180
out6.addreading(b1, delta)
idx1 += 1
idx2 += 1
out.addbounds(*changed_ranges["building1_L1"])
out.addbounds(*changed_ranges["building1_L2"])
out.addbounds(*changed_ranges["building1_L3"])
out.addbounds(*changed_ranges["building1_C1"])
out.addbounds(*changed_ranges["building1_C2"])
out.addbounds(*changed_ranges["building1_C3"])
out.addbounds(*changed_ranges["building2_L1"])
out.addbounds(*changed_ranges["building2_L2"])
out.addbounds(*changed_ranges["building2_L3"])
out.addbounds(*changed_ranges["building2_C1"])
out.addbounds(*changed_ranges["building2_C2"])
out.addbounds(*changed_ranges["building2_C3"])

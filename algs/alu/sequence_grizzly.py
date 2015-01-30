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

idxML1=0
idxML2=0
idxML3=0
idxAL1=0
idxAL2=0
idxAL3=0
idxMC1=0
idxMC2=0
idxMC3=0
idxAC1=0
idxAC2=0
idxAC3=0


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


while idxML1< len(input_streams[""]) and idxAL1< len(input_streams[""]) and idxML2< len(input_streams[""]) \
and idxAL2< len(input_streams[""]) and idxML3 < len(input_streams[""]) and idxAL3 < len(input_streams[""]):

if LBAng[idxLBA].time < LCAng[idxLCA].time:
idxLBA += 1
continue
if LBAng[idxLBA].time > LCAng[idxLCA].time:
idxLCA += 1
continue
if LBAng[idxLBA].time < LAAng[idxLAA].time:
idxLBA += 1
continue
if LBAng[idxLBA].time > LAAng[idxLAA].time:
idxLAA += 1
continue
if LCAng[idxLCA].time < LAAng[idxLAA].time:
idxLCA += 1
continue
if LCAng[idxLCA].time > LAAng[idxLAA].time:
idxLAA += 1
continue
if LBMag[idxLBM].time < LCMag[idxLCM].time:
idxLBM += 1
continue
if LBMag[idxLBM].time > LCMag[idxLCM].time:
idxLCM += 1
continue
if LBMag[idxLBM].time < LAMag[idxLAM].time:
idxLBM += 1
continue
if LBMag[idxLBM].time > LAMag[idxLAM].time:
idxLAM += 1
continue
if LCMag[idxLCM].time < LAMag[idxLAM].time:
idxLCM += 1
continue
if LCMag[idxLCM].time > LAMag[idxLAM].time:
idxLAM += 1
continue
if LBMag[idxLBM].time < LBAng[idxLBA].time:
idxLBM += 1
continue
if LBMag[idxLBM].time > LBAng[idxLBA].time:
idxLBA += 1
continue
if LCMag[idxLCM].time < LCAng[idxLCA].time:
idxLCM += 1
continue
if LCMag[idxLCM].time > LCAng[idxLCA].time:
idxLCA += 1
continue
if LAMag[idxLAM].time < LAAng[idxLAA].time:
idxLAM += 1
continue
if LAMag[idxLAM].time > LAAng[idxLAA].time:
idxLAA += 1
continue
# compute sin value for three phase and sin value for l2 and l3 anfter add 120 degree and 240 degree
sinLAAng=np.sin(np.radians(LAAng[idxLAA].value-LBAng[idxLBA].value))
sinLBAng=np.sin(np.radians(LBAng[idxLBA].value-LBAng[idxLBA].value))
sinLCAng=np.sin(np.radians(LCAng[idxLCA].value-LBAng[idxLBA].value))
sinLAAng_add120=np.sin(np.radians(LAAng[idxLAA].value+120-LBAng[idxLBA].value))
sinLAAng_add240=np.sin(np.radians(LAAng[idxLAA].value+240-LBAng[idxLBA].value))
sinLCAng_add120=np.sin(np.radians(LCAng[idxLCA].value+120-LBAng[idxLBA].value))
sinLCAng_add240=np.sin(np.radians(LCAng[idxLCA].value+240-LBAng[idxLBA].value))
# compute cosin value for three phase and cosin value for l2 and l3 anfter add 120 degree and 240 degree
cosLAAng=np.cos(np.radians(LAAng[idxLAA].value-LBAng[idxLBA].value))
cosLBAng=np.cos(np.radians(LBAng[idxLBA].value-LBAng[idxLBA].value))
cosLCAng=np.cos(np.radians(LCAng[idxLCA].value-LBAng[idxLBA].value))
cosLAAng_add120=np.cos(np.radians(LAAng[idxLAA].value+120-LBAng[idxLBA].value))
cosLAAng_add240=np.cos(np.radians(LAAng[idxLAA].value+240-LBAng[idxLBA].value))
cosLCAng_add120=np.cos(np.radians(LCAng[idxLCA].value+120-LBAng[idxLBA].value))
cosLCAng_add240=np.cos(np.radians(LCAng[idxLCA].value+240-LBAng[idxLBA].value))
# compute balance V0
v0imagine=(LAMag[idxLAM].value*sinLAAng+LBMag[idxLBM].value*sinLBAng+LCMag[idxLCM].value*sinLCAng)/3.0
v0real=(LAMag[idxLAM].value*cosLAAng+LBMag[idxLBM].value*cosLBAng+LCMag[idxLCM].value*cosLCAng)/3.0
v0mag=np.sqrt(v0imagine**2+v0real**2)
v0ang=np.degrees(math.atan2(v0imagine,v0real))
V0Mag.append((LAMag[idxLAM].time, v0mag))
V0Ang.append((LAAng[idxLAA].time,v0ang))
#compute balance v+
vpimagine=(LBMag[idxLBM].value*sinLBAng+LCMag[idxLCM].value*sinLCAng_add120+LAMag[idxLAM].value*sinLAAng_add240)/3.0
vpreal=(LBMag[idxLBM].value*cosLBAng+LCMag[idxLCM].value*cosLCAng_add120+LAMag[idxLAM].value*cosLAAng_add240)/3.0
vpmag=np.sqrt(vpimagine**2+vpreal**2)
vpang=np.degrees(math.atan2(vpimagine,vpreal))
VpMag.append((LAMag[idxLAM].time, vpmag))
VpAng.append((LAAng[idxLAA].time,vpang))
# compute balance v-
vnimagine=(LBMag[idxLBM].value*sinLBAng+LCMag[idxLCM].value*sinLCAng_add240+LAMag[idxLAM].value*sinLAAng_add120)/3.0
vnreal=(LBMag[idxLBM].value*cosLBAng+LCMag[idxLCM].value*cosLCAng_add240+LAMag[idxLAM].value*cosLAAng_add120)/3.0
vnmag=np.sqrt(vnimagine**2+vnreal**2)
vnang=np.degrees(math.atan2(vnimagine,vnreal))
VnMag.append((LAMag[idxLAM].time, vnmag))
VnAng.append((LAAng[idxLAA].time,vnang))
# compute unbalance V-
Vn_ubalance_seq.append((LBMag[idxLBM].time,(vnmag/float(vpmag))*100))
# compute unbalance v0
V0_ubalance_seq.append((LBMag[idxLBM].time,(v0mag/float(vpmag))*100))
idxLAA+= 1
idxLAM+= 1
idxLBA+= 1
idxLBM+= 1
idxLCA+= 1
idxLCM+= 1
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

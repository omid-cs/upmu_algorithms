import qdf
import numpy as np
class sequence (qdf.QDF2Distillate):
def initialize(self, section name):
self.set_section(section)
self.set_name(name)
self.set_version(1)
self.register_output("ZERO_SEQ_ANG", "Degree")
self.register_output("ZERO_SEQ_MAG", "V")
self.register_output("POSITIVE_SEQ_ANG", "Degree")
self.register_output("POSITIVE_SEQ_MAG", "V")
self.register_output("NEGATIVE_SEQ_ANG", "Degree")
self.register_output("NEGATIVE_SEQ_MAG", "V")
self.register_output("UNBALANCE_NEG_SEQ", "Precent")
self.register_output("UNBALANCE_ZERO_SEQ", "Precent")

self.register_input("M1")
self.register_input("M2")
self.register_input("M3")
self.register_input("A1")
self.register_input("A2")
self.register_input("A3")

def compute(self, changed_ranges, input_streams, params, report):
zero_seq_angle = report.output("ZERO_SEQ_ANG")
zero_seq_magnitude = report.output("ZERO_SEQ_MAG")
postive_seq_angle = report.output("POSITIVE_SEQ_ANG")
postive_seq_magnitude = report.output("POSITIVE_SEQ_MAG")
negative_seq_angle = report.output("NEGATIVE_SEQ_ANG")
negative_seq_magnitude = report.output("NEGATIVE_SEQ_MAG")
unblance_negative_seq = report.output("UNBALANCE_NEG_SEQ")
unblance_zero_seq = report.output("UNBALANCE_ZERO_SEQ")
print "compute invoked:"
print "changed_ranges: ", changed_ranges
print "params: ", params

idxM1=0
idxM2=0
idxM3=0
idxA1=0
idxA2=0
idxA3=0

M1=input_streams["M1"]
A1=input_streams["A1"]
M2=input_streams["M2"]
A2=input_streams["A2"]
M3=input_streams["M3"]
A3=input_streams["A3"]



while idxM1 len(M1) and idxA1< len(A1) and idxM2< len(M2) and idxA2< len(A2) and idxM3 < len(M3) and idxA3 < len(A3):
  if not (A1[idxA1].time == M1[idxM1].time and M1[idxM1].time==A2[idxA2].time and A2[idxA2].time==M2[idxM2].time and
     M2[idxM2].time==A3[idxA3].time and A3[idA3].time==M3[idxM3].time):
       
    max_time=max(A1[idxA1].time,M1[idxM1].time,A2[idxA2].time,M2[idxM2].time,A3[idxA3].time,M3[idxM3].time)
    if A1[idxA1].time < max_time:
      idxA1 += 1
    if A2[idxA2].time < max_time:
      idxA2 += 1
    if A3[idxA3].time < max_time:
      idxA3 += 1
    if M1[idxM1].time < max_time:
      idxM1 += 1
    if M2[idxM2].time < max_time:
      idxM2 += 1
    if M3[idxM3].time < max_time:
      idxM3 += 1
    continue
# compute sin value for three phase and sin value for l2 and l3 anfter add 120 degree and 240 degree
  sinA3=np.sin(np.radians(A3[idxA3].value-A1[idxA1].value))
  sinA1=np.sin(np.radians(A1[idxA1].value-A1[idxA1].value))
  sinA2=np.sin(np.radians(A2[idxA2].value-A1[idxA1].value))
  sinA3_add120=np.sin(np.radians(A3[idxA3].value+120-A1[idxA1].value)
  sinA3_add240=np.sin(np.radians(A3[idxA3].value+240-A1[idxA1].value)
  sinA2_add120=np.sin(np.radians(A2[idxA2].value+120-A1[idxA1].value)
  sinA2_add240=np.sin(np.radians(A2[idxA2].value+240-A1[idxA1].value)
# compute cosin value for three phase and cosin value for l2 and l3 anfter add 120 degree and 240 degree
  cosA3=np.cos(np.radians(A3[idxA3].value-A1[idxA1].value))
  cosA1=np.cos(np.radians(A1[idxA1].value-A1[idxA1].value))
  cosA2=np.cos(np.radians(A2[idxA2].value-A1[idxA1].value))
  cosA3_add120=np.cos(np.radians(A3[idxA3].value+120-A1[idxA1].value))
  cosA3_add240=np.cos(np.radians(A3[idxA3].value+240-A1[idxA1].value))
  cosA2_add120=np.cos(np.radians(A2[idxA2].value+120-A1[idxA1].value))
  cosA2_add240=np.cos(np.radians(A2[idxA2].value+240-A1[idxA1].value))
# compute balance V0
  v0imagine=(M3[idxM3].value*sinA3+M1[M1].value*sinA1+M2[idxM2].value*sinA2)/3.0
  v0real=(M3[idxM3].value*cosA3+M1[idxM1].value*cosA1+M2[idxM2].value*cosA2)/3.0
  v0mag=np.sqrt(v0imagine**2+v0real**2)
  v0ang=np.degrees(math.atan2(v0imagine,v0real))
  zero_seq_angle.addreading(A1[idxA1].time, v0mag)
  reactive_power_output.addreading(A1[idxA1].time, v0ang)
  
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

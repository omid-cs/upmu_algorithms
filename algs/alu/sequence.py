import qdf
import numpy as np
class sequence (qdf.QDF2Distillate):
  def initialize(self, section, name):
    self.set_section(section)
    self.set_name(name)
    self.set_version(6)
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
    self.register_input("Reference_Angle")

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
    idxAref=0
    M1=input_streams["M1"]
    A1=input_streams["A1"]
    M2=input_streams["M2"]
    A2=input_streams["A2"]
    M3=input_streams["M3"]
    A3=input_streams["A3"]
    Reference_Angle=input_streams["Reference_Angle"]

    while idxM1<len(M1) and idxA1< len(A1) and idxM2< len(M2) and idxA2< len(A2) and idxM3 < len(M3) and idxA3 < len(A3) and idxAref<len(Reference_Angle):
      if not (A1[idxA1][0] == M1[idxM1][0] and M1[idxM1][0]==A2[idxA2][0] and A2[idxA2][0]==M2[idxM2][0] and
      M2[idxM2][0]==A3[idxA3][0] and A3[idA3][0]==M3[idxM3][0] and M3[idxM3][0]==Reference_Angle[idxAref][0]):
        max_time=max(A1[idxA1][0],M1[idxM1][0],A2[idxA2][0],M2[idxM2][0],A3[idxA3][0],M3[idxM3][0])
        if A1[idxA1][0] < max_time:
          idxA1 += 1
        if A2[idxA2][0] < max_time:
          idxA2 += 1
        if A3[idxA3][0] < max_time:
          idxA3 += 1
        if M1[idxM1][0] < max_time:
          idxM1 += 1
        if M2[idxM2][0] < max_time:
          idxM2 += 1
        if M3[idxM3][0] < max_time:
          idxM3 += 1
        if Reference_Angle[idxAref][0] < max_time:
          idxAref += 1  
        continue
      # compute sin value for three phase and sin value for l2 and l3 anfter add 120 degree and 240 degree
      sinA3=np.sin(np.radians(A3[idxA3][1]-Reference_Angle[idxAref][1]))
      sinA1=np.sin(np.radians(A1[idxA1][1]-Reference_Angle[idxAref][1]))
      sinA2=np.sin(np.radians(A2[idxA2][1]-Reference_Angle[idxAref][1]))
      sinA3_add120=np.sin(np.radians(A3[idxA3][1]+120-Reference_Angle[idxAref][1]))
      sinA3_add240=np.sin(np.radians(A3[idxA3][1]+240-Reference_Angle[idxAref][1]))
      sinA2_add120=np.sin(np.radians(A2[idxA2][1]+120-Reference_Angle[idxAref][1]))
      sinA2_add240=np.sin(np.radians(A2[idxA2][1]+240-Reference_Angle[idxAref][1]))
      # compute cosin value for three phase and cosin value for l2 and l3 anfter add 120 degree and 240 degree
      cosA3=np.cos(np.radians(A3[idxA3][1]-Reference_Angle[idxAref][1]))
      cosA1=np.cos(np.radians(A1[idxA1][1]-Reference_Angle[idxAref][1]))
      cosA2=np.cos(np.radians(A2[idxA2][1]-Reference_Angle[idxAref][1]))
      cosA3_add120=np.cos(np.radians(A3[idxA3][1]+120-Reference_Angle[idxAref][1]))
      cosA3_add240=np.cos(np.radians(A3[idxA3][1]+240-Reference_Angle[idxAref][1]))
      cosA2_add120=np.cos(np.radians(A2[idxA2][1]+120-Reference_Angle[idxAref][1]))
      cosA2_add240=np.cos(np.radians(A2[idxA2][1]+240-Reference_Angle[idxAref][1]))
      # compute balance V0
      v0imagine=(M3[idxM3][1]*sinA3+M1[M1][1]*sinA1+M2[idxM2][1]*sinA2)/3.0
      v0real=(M3[idxM3][1]*cosA3+M1[idxM1][1]*cosA1+M2[idxM2][1]*cosA2)/3.0
      v0mag=np.sqrt(v0imagine**2+v0real**2)
      v0ang=np.degrees(math.atan2(v0imagine,v0real))
      zero_seq_magnitude.addreading(A1[idxA1][0], v0mag)
      zero_seq_angle.addreading(A1[idxA1][0], v0ang)
      #compute balance v+
      vpimagine=(M1[idxM1][1]*sinA1+M2[idxM2][1]*sinA2_add120+M3[idxM3][1]*sinA3_add240)/3.0
      vpreal=(M1[idxM1][1]*cosA1+M2[idxM2][1]*cosA2_add120+M3[idxM3][1]*cosA3_add240)/3.0
      vpmag=np.sqrt(vpimagine**2+vpreal**2)
      vpang=np.degrees(math.atan2(vpimagine,vpreal))
      postive_seq_magnitude.addreading(A1[idxA1][0], vpmag)
      postive_seq_angle.addreading(A1[idxA1][0], vpang)
      # compute balance v-
      vnimagine=(M1[idxM1][1]*sinA1+M2[idxM2][1]*sinA2_add240+M3[idxM3][1]*sinA3_add120)/3.0
      vnreal=(M1[idxM1][1]*cosA1+M2[idxM2][1]*cosA2_add240+M3[idxM3][1]*cosA3_add120)/3.0
      vnmag=np.sqrt(vnimagine**2+vnreal**2)
      vnang=np.degrees(math.atan2(vnimagine,vnreal))
      negative_seq_magnitude.addreading(A1[idxA1][0], vnmag)
      negative_seq_angle.addreading(A1[idxA1][0], vnang)
      # compute unbalance V-
      unblance_negative_seq.addreading((A1[idxA1][0],(vnmag/float(vpmag))*100))
      # compute unbalance v0
      unblance_zero_seq.addreading((A1[idxA1][0],(v0mag/float(vpmag))*100))
      idxA1+= 1
      idxA2+= 1
      idxA3+= 1
      idxM1+= 1
      idxM2+= 1
      idxM3+= 1
      idxAref+=1
    zero_seq_angle.addbounds(*changed_ranges["M1"])
    zero_seq_angle.addbounds(*changed_ranges["M2"])
    zero_seq_angle.addbounds(*changed_ranges["M3"])
    zero_seq_angle.addbounds(*changed_ranges["A1"])
    zero_seq_angle.addbounds(*changed_ranges["A2"])
    zero_seq_angle.addbounds(*changed_ranges["A3"])
    zero_seq_angle.addbounds(*changed_ranges["Reference_Angle"])
    
    zero_seq_magnitude.addbounds(*changed_ranges["M1"])
    zero_seq_magnitude.addbounds(*changed_ranges["M2"])
    zero_seq_magnitude.addbounds(*changed_ranges["M3"])
    zero_seq_magnitude.addbounds(*changed_ranges["A1"])
    zero_seq_magnitude.addbounds(*changed_ranges["A2"])
    zero_seq_magnitude.addbounds(*changed_ranges["A3"])
    zero_seq_magnitude.addbounds(*changed_ranges["Reference_Angle"])
    
    postive_seq_angle.addbounds(*changed_ranges["M1"])
    postive_seq_angle.addbounds(*changed_ranges["M2"])
    postive_seq_angle.addbounds(*changed_ranges["M3"])
    postive_seq_angle.addbounds(*changed_ranges["A1"])
    postive_seq_angle.addbounds(*changed_ranges["A2"])
    postive_seq_angle.addbounds(*changed_ranges["A3"])
    postive_seq_angle.addbounds(*changed_ranges["Reference_Angle"])
    
    postive_seq_magnitude.addbounds(*changed_ranges["M1"])
    postive_seq_magnitude.addbounds(*changed_ranges["M2"])
    postive_seq_magnitude.addbounds(*changed_ranges["M3"])
    postive_seq_magnitude.addbounds(*changed_ranges["A1"])
    postive_seq_magnitude.addbounds(*changed_ranges["A2"])
    postive_seq_magnitude.addbounds(*changed_ranges["A3"])
    postive_seq_magnitude.addbounds(*changed_ranges["Reference_Angle"])
    
    negative_seq_angle.addbounds(*changed_ranges["M1"])
    negative_seq_angle.addbounds(*changed_ranges["M2"])
    negative_seq_angle.addbounds(*changed_ranges["M3"])
    negative_seq_angle.addbounds(*changed_ranges["A1"])
    negative_seq_angle.addbounds(*changed_ranges["A2"])
    negative_seq_angle.addbounds(*changed_ranges["A3"])
    negative_seq_angle.addbounds(*changed_ranges["Reference_Angle"])
    
    negative_seq_magnitude.addbounds(*changed_ranges["M1"])
    negative_seq_magnitude.addbounds(*changed_ranges["M2"])
    negative_magnitude.addbounds(*changed_ranges["M3"])
    negative_seq_magnitude.addbounds(*changed_ranges["A1"])
    negative_seq_magnitude.addbounds(*changed_ranges["A2"])
    negative_seq_magnitude.addbounds(*changed_ranges["A3"])
    negative_seq_magnitude.addbounds(*changed_ranges["Reference_Angle"])
    
    unblance_negative_seq.addbounds(*changed_ranges["M1"])
    unblance_negative_seq.addbounds(*changed_ranges["M2"])
    unblance_negative_seq.addbounds(*changed_ranges["M3"])
    unblance_negative_seq.addbounds(*changed_ranges["A1"])
    unblance_negative_seq.addbounds(*changed_ranges["A2"])
    unblance_negative_seq.addbounds(*changed_ranges["A3"])
    unblance_negative_seq.addbounds(*changed_ranges["Reference_Angle"])
    
    unblance_zero_seq.addbounds(*changed_ranges["M1"])
    unblance_zero_seq.addbounds(*changed_ranges["M2"])
    unblance_zero_seq.addbounds(*changed_ranges["M3"])
    unblance_zero_seq.addbounds(*changed_ranges["A1"])
    unblance_zero_seq.addbounds(*changed_ranges["A2"])
    unblance_zero_seq.addbounds(*changed_ranges["A3"])
    unblance_zero_seq.addbounds(*changed_ranges["Reference_Angle"])

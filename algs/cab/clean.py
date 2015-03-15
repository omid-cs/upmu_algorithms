import qdf
import numpy as np

class Clean (qdf.QDF2Distillate):
  def initialize(self, section="Clean", name="default"):
    self.set_section(section)
    self.set_name(name)
    self.set_version(1)

    self.names = ["C1ANG", "C1MAG", "C2ANG", "C2MAG", "C3ANG", "C3MAG",
                  "L1ANG", "L1MAG", "L2ANG", "L2MAG", "L3ANG", "L3MAG", "LSTATE"]
    units      = ['deg', 'A', 'deg', 'A', 'deg', 'A',
                  'deg', 'A', 'deg', 'A', 'deg', 'A', 'bitmap']

    for i in xrange(len(self.names)):
      self.register_output(self.names[i], units[i])
      self.register_input(self.names[i])

  def compute(self, changed_ranges, input_streams, params, report):
    raw_list  = [input_streams[name] for name in self.names]
    clean_list = [report.output(name) for name in self.names]

    for i in xrange(len(raw_list)):
      raw_stream = raw_list[i]
      clean_stream = clean_list[i]
      for point in raw_stream:
        # where cleaning happens
        clean_stream.addreading(point[0], point[1])
      clean_stream.addbounds(*changed_ranges[self.names[i]])

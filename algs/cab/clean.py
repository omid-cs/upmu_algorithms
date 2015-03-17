import qdf

class Clean (qdf.QDF2Distillate):
  def initialize(self, section="Clean", name="default", stream_type="ANG"):
    self.set_section(section)
    self.set_name(name)
    self.set_version(1)

    if 'ANG' in stream_type:
      units = 'deg'
    elif 'MAG' in stream_type:
      if 'C' in stream_type:
        units = 'A'
      else:
        units = 'V'
    elif 'LSTATE' in stream_type:
      units = 'bitmap'
    else:
      units = 'arb'

    self.register_output('CLEAN', units)
    self.register_input('raw')

  def compute(self, changed_ranges, input_streams, params, report):
    raw = input_streams['raw']
    clean = report.output('CLEAN')

    for point in raw:
      # where cleaning happens
      clean.addreading(point[0], point[1])

    clean.addbounds(*changed_ranges['raw'])

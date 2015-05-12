import qdf
import numpy as np

class PhaseShift (qdf.QDF2Distillate):
  def initialize(self, section="Frequency", name="frequency", shift_amt='60'):
    self.set_section(section) # first part of path to output stream
    self.set_name(name) # second part of path to output stream
    self.set_version(1) # increment on update to wipe data and recompute
    self.register_output("SHIFTED", "deg")
    self.register_input("angle")

    self.shift_amt = float(shift_amt)

  """
  # leftover from frequency
  def prereqs(self, changed_ranges):
    uuid = changed_ranges[0][0]
    name = changed_ranges[0][1]
    rngs = []
    for rng in changed_ranges[0][2]:
      rngs.append([rng[0]-qdf.SECOND, rng[1]])
    return [[uuid, name, rngs]]
  """
def compute(self, changed_ranges, input_streams, params, report):
    # changed_ranges: [start, end] for start and end of the range of data for this run
    # input_streams: dictionary of {name:[data,...,]} pairs, named from initialized inputs
    # params: same params as initialize
    # report: the set of StreamData objects to store data from output
    shifted = report.output("SHIFTED")
    phase = input_streams["angle"]


    for point in phase:
      # addreading(time, value)
      # timestamp: point[0]
      # value: point[1]
      shifted.addreading(point[0], point[1]+self.shift_amt)

    # range of data that has changed. Will be erased and overwirtten by new data
    # addbounds(start_time, end_time)
    shifted.addbounds(*changed_ranges["angle"])

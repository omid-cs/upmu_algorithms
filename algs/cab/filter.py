import qdf
import numpy as np
from math import ceil

class Filter (qdf.QDF2Distillate):
  def initialize(self, section="Filter", name="default", units='arb', window_time='1', accuracy='.9'):
    self.set_section(section)
    self.set_name(name)
    self.set_version(1)
    self.register_output("FILTERED", units)
    self.register_input("UNFILTERED")

    self.win_time = int(window_time)*qdf.SECOND
    self.win_width = int(window_time)*120 #seconds * pts/second
    self.accuracy = accuracy

  def prereqs(self, changed_ranges):
    uuid = changed_ranges[0][0]
    name = changed_ranges[0][1]
    rngs = []
    for rng in changed_ranges[0][2]:
      rngs.append([rng[0]-(self.win_time/2), rng[1]+(self.win_time/2)])
    return [[uuid, name, rngs]]

  def compute(self, changed_ranges, input_streams, params, report):
    filtered = report.output("FILTERED")
    unfiltered = input_streams["UNFILTERED"]

    # initialize minimum time as time of first point in array
    min_time = unfiltered[0]-self.win_time/2
    mid_time = unfiltered[0]
    max_time = unfiltered[0]+self.win_time/2

    # calculate points required for accuracy threshold, rounded up
    pts_needed = int(ceil(self.win_width * self.accuracy))

    # initialize starting and ending points
    start = 0
    end = 0
    tot_pts = 0
    total_val = 0.0

    # loop over all midpoint times
    while not (end == len(unfiltered) and end-start < pts_needed)
      # search for start point, removing trailing points if outside range
      while (start < len(unfiltered) and unfiltered[start][0] < min_time):
        tot_pts -= 1
        total_val -= unfiltered[start][1]
        start += 1
      
      # search for end point, adding leading points if inside range
      while (end < len(unfiltered) and unfiltered[end][0] < max_time):
        tot_pts += 1
        total_val += unfiltered[end][1]
        end += 1

      if total_pts >= pts_needed:
        filtered.addreading(mid_time, total_val/total_pts)

      min_time = update_time(min_time)
      mid_time = update_time(mid_time)
      max_time = update_time(max_time)

    filtered.addbounds(*changed_ranges["UNFILTERED"])

def update_time(time):
  delta = qdf.SECOND/120
  if time % 10 == 6:
    delta += 1 #hack to account compounding rounding error
  return time + delta

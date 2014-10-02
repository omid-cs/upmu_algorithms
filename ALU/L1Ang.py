__author__ = 'immesys'

import numpy as np
import qdf
from twisted.internet import defer

class ExampleDelta(qdf.QuasarDistillate):

    def setup(self, xopts):
        """
        This constructs your distillate algorithm
        """
        #This is the first level in the distillate tree
        self.set_author("Andrew")

        #This is the second level. This name should be unique for every algorithm you write
        self.set_name("L1Ang")

        #This is the final level. You can have multiple of these
        self.add_stream("L1ang", unit="Degrees")

        self.use_stream("1hz", "2942433b-6511-4298-a0b2-2886456cff4f")
        self.use_stream("2hz", "74182356-6d1e-4123-b312-5cc70da89840")

        #If this is incremented, it is assumed that the whole distillate is invalidated, and it
        #will be deleted and discarded. In addition all 'persist' data will be removed
        self.set_version(3)

    @defer.inlineCallbacks
    def compute(self):
        """
        This is called to compute your algorithm.

        This example generates the difference between two streams
        """

        if self.unpersist("done",False):
            print "Already done"
            return 

        start_date = self.date("2014-8-17T03:00:00.000000")
        end_date = self.date("2014-8-17T06:00:00.000000")

        hz1_version, hz1_values = yield self.stream_get("1hz", start_date, end_date)
        hz2_version, hz2_values = yield self.stream_get("2hz", start_date, end_date)
        delta_values = []

        idx1 = 0
        idx2 = 0
        while idx1 < len(hz1_values) and idx2 < len(hz2_values):
            if hz1_values[idx1].time < hz2_values[idx2].time:
                idx1 += 1
                continue
            if hz1_values[idx1].time > hz2_values[idx2].time:
                idx2 += 1
                continue
            delta = hz1_values[idx1].value - hz2_values[idx2].value
            if delta > 180:
                delta =delta-360
            if delta <-180:
                delta=delta+360
            delta_values.append((hz1_values[idx1].time, delta))
            if len(delta_values) >= qdf.OPTIMAL_BATCH_SIZE:
                yield self.stream_insert_multiple("L1ang", delta_values)
                delta_values = []
            idx1 += 1
            idx2 += 1

        yield self.stream_insert_multiple("L1ang", delta_values)

        #Now that we are done, save the time we finished at
        self.persist("done", True)
    

qdf.register(ExampleDelta())
qdf.begin()

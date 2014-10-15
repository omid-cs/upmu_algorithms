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
        self.set_name("L3difference")

        #This is the final level. You can have multiple of these
        self.add_stream("L3ang_GB", unit="Degrees")
        self.add_stream("L3ang_GS", unit="Degrees")
        self.add_stream("L3ang_BS", unit="Degrees")
        self.add_stream("L3ang_SaSb", unit="Degrees")
        self.use_stream("1hz", "b653c63b-4acc-45ee-ae3d-1602e6116bc1")
        self.use_stream("2hz", "65f49c81-dafa-4aa2-8467-1627fb489c0c")
        self.use_stream("3hz", "2c07ccef-20c5-4971-87cf-2c187ce5f722")
        self.use_stream("4hz", "b5279898-5652-4d34-abd6-45c7d697e524")
        self.use_stream("5hz", "33b376c8-a59e-4054-a213-e9eb95cc8ad9")
        

        #If this is incremented, it is assumed that the whole distillate is invalidated, and it
        #will be deleted and discarded. In addition all 'persist' data will be removed
        self.set_version(5)

    @defer.inlineCallbacks
    def compute(self):
        """
        This is called to compute your algorithm.

        This example generates the difference between two streams
        """

        if self.unpersist("done",False):
            print "Already done"
            return 

        start_date = self.date("2014-10-01T00:00:00.000000")
        end_date = self.date("2014-10-01T00:30:00.000000")

        hz1_version, hz1_values = yield self.stream_get("1hz", start_date, end_date)
        hz2_version, hz2_values = yield self.stream_get("2hz", start_date, end_date)
        hz3_version, hz3_values = yield self.stream_get("3hz", start_date, end_date)
        hz4_version, hz4_values = yield self.stream_get("4hz", start_date, end_date)
        hz5_version, hz5_values = yield self.stream_get("5hz", start_date, end_date)
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
            if delta ==-180:
                delta=180
            delta_values.append((hz1_values[idx1].time, delta))
            if len(delta_values) >= qdf.OPTIMAL_BATCH_SIZE:
                yield self.stream_insert_multiple("L3ang_GB", delta_values)
                delta_values = []
            idx1 += 1
            idx2 += 1

        yield self.stream_insert_multiple("L3ang_GB", delta_values)
        
        delta_values = []

        idx1 = 0
        idx2 = 0
        while idx1 < len(hz1_values) and idx2 < len(hz3_values):
            if hz1_values[idx1].time < hz3_values[idx2].time:
                idx1 += 1
                continue
            if hz1_values[idx1].time > hz3_values[idx2].time:
                idx2 += 1
                continue
            delta = hz1_values[idx1].value - hz3_values[idx2].value
            if delta > 180:
                delta =delta-360
            if delta <-180:
                delta=delta+360
            if delta ==-180:
                delta=180
            delta_values.append((hz1_values[idx1].time, delta))
            if len(delta_values) >= qdf.OPTIMAL_BATCH_SIZE:
                yield self.stream_insert_multiple("L3ang_GS", delta_values)
                delta_values = []
            idx1 += 1
            idx2 += 1

        yield self.stream_insert_multiple("L3ang_GS", delta_values)
        #Now that we are done, save the time we finished at
        delta_values = []

        idx1 = 0
        idx2 = 0
        while idx1 < len(hz2_values) and idx2 < len(hz3_values):
            if hz2_values[idx1].time < hz3_values[idx2].time:
                idx1 += 1
                continue
            if hz2_values[idx1].time > hz3_values[idx2].time:
                idx2 += 1
                continue
            delta = hz2_values[idx1].value - hz3_values[idx2].value
            if delta > 180:
                delta =delta-360
            if delta <-180:
                delta=delta+360
            if delta ==-180:
                delta=180
            delta_values.append((hz2_values[idx1].time, delta))
            if len(delta_values) >= qdf.OPTIMAL_BATCH_SIZE:
                yield self.stream_insert_multiple("L3ang_BS", delta_values)
                delta_values = []
            idx1 += 1
            idx2 += 1

        yield self.stream_insert_multiple("L3ang_BS", delta_values)
        
        delta_values = []

        idx1 = 0
        idx2 = 0
        while idx1 < len(hz4_values) and idx2 < len(hz5_values):
            if hz4_values[idx1].time < hz5_values[idx2].time:
                idx1 += 1
                continue
            if hz4_values[idx1].time > hz5_values[idx2].time:
                idx2 += 1
                continue
            delta = hz4_values[idx1].value - hz5_values[idx2].value
            if delta > 180:
                delta =delta-360
            if delta <-180:
                delta=delta+360
            if delta ==-180:
                delta=180
            delta_values.append((hz4_values[idx1].time, delta))
            if len(delta_values) >= qdf.OPTIMAL_BATCH_SIZE:
                yield self.stream_insert_multiple("L3ang_SaSb", delta_values)
                delta_values = []
            idx1 += 1
            idx2 += 1

        yield self.stream_insert_multiple("L3ang_SaSb", delta_values)
        self.persist("done", True)
    

qdf.register(ExampleDelta())
qdf.begin()

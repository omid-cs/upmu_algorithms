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
        self.set_name("L1difference")

        #This is the final level. You can have multiple of these
        self.add_stream("L1ang_GB", unit="Degrees")
        self.add_stream("L1ang_GS", unit="Degrees")
        self.add_stream("L1ang_BS", unit="Degrees")
        self.add_stream("L1ang_SaSb", unit="Degrees")
        self.use_stream("1hz", "b4776088-2f85-4c75-90cd-7472a949a8fa")
        self.use_stream("2hz", "66fcb659-c69a-41b5-b874-80ac7d7f669d")
        self.use_stream("3hz", "adf13e17-44b7-4ef6-ae3f-fde8a9152ab7")
        self.use_stream("4hz", "4d6525a9-b8ad-48a4-ae98-b171562cf817")
        self.use_stream("5hz", "98435be7-7341-4661-b104-16af89e0333d")
        
        #If this is incremented, it is assumed that the whole distillate is invalidated, and it
        #will be deleted and discarded. In addition all 'persist' data will be removed
        self.set_version(12)

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
        end_date = self.date("2014-10-02T00:00:00.000000")

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
                yield self.stream_insert_multiple("L1ang_GB", delta_values)
                delta_values = []
            idx1 += 1
            idx2 += 1

        yield self.stream_insert_multiple("L1ang_GB", delta_values)
        
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
                yield self.stream_insert_multiple("L1ang_GS", delta_values)
                delta_values = []
            idx1 += 1
            idx2 += 1

        yield self.stream_insert_multiple("L1ang_GS", delta_values)
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
                yield self.stream_insert_multiple("L1ang_BS", delta_values)
                delta_values = []
            idx1 += 1
            idx2 += 1

        yield self.stream_insert_multiple("L1ang_BS", delta_values)
        
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
                yield self.stream_insert_multiple("L1ang_SaSb", delta_values)
                delta_values = []
            idx1 += 1
            idx2 += 1

        yield self.stream_insert_multiple("L1ang_SaSb", delta_values)
        
        self.persist("done", True)
    
        
qdf.register(ExampleDelta())
qdf.begin()

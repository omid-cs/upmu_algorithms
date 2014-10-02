__author__ = 'immesys'

import numpy as np
import qdf
from twisted.internet import defer

class Distillate(qdf.QuasarDistillate):


    def setup(self, opts):
        """
        Initializes distillate parameters options from dictionary 'opts'
        Creates dataset in appropraite path
        """
        self.input_stream = opts['input_stream']
        self.start_date = self.date(opts['start_date'])
        self.end_date = self.date(opts['end_date'])
        self.output_stream = opts['output_stream']
        output_unit = opts['output_unit']
        input_uid = opts['input_uid']
        version = opts['version']
        self.scale_factor = opts['scale_factor']

        #This is the first level in the distillate tree
        self.set_author("CAB")

        #This is the second level. This name should be unique for every algorithm you write
        self.set_name("Scale_Amp")

        #This is the final level. You can have multiple of these
        self.add_stream(self.output_stream, unit=output_unit)

        self.use_stream(self.input_stream, input_uid)

        #If this is incremented, it is assumed that the whole distillate is invalidated, and it
        #will be deleted and discarded. In addition all 'persist' data will be removed
        self.set_version(version)

    @defer.inlineCallbacks
    def compute(self):
        """
        This is called to compute your algorithm.

        This distillate scales an input stream by a constant factor
        """

        if self.unpersist("done",False):
            print "Already done"
            return

        input_version, input_values = yield self.stream_get(self.input_name, \
                                                            self.start_date, \
                                                            self.end_date)

        #This is where the algorithm is implemented for the distillate
        scaled_values = []
        i = 0
        while i < len(input_values):
            scaled_value = input_values[i].value * self.scale_factor
            scaled_values.append((input_values[i].time, scaled_value))
            if len(scaled_values) >= qdf.OPTIMAL_BATCH_SIZE:
                yield self.stream_insert_multiple(self.output_stream, scaled_values)
                scaled_values = []
            i += 1

        yield self.stream_insert_multiple(self.output_stream, scaled_values)

        #Now that we are done, save the time we finished at
        self.persist("done", True)

# Input information for distillate
opts = { 'input_stream'  : 'L1MAG', \
         'input_uid'     : 'abffcf07-9e17-404a-98c3-ea4d60042ff3', \
         'start_date'    : '2014-09-07T00:00:00.000000', \
         'end_date'      : '2014-09-08T00:00:00.000000', \
         'output_stream' : 'soda_a_L1MAG_6.0', \
         'output_unit'   : 'V', \
         'scale_factor'  : 6.0, \
         'version'       : 5 }
qdf.register(Distillate(), options=opts)
qdf.begin()

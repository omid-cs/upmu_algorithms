__author__ = 'immesys'

import numpy as np
import qdf
from twisted.internet import defer
from Stream_Reader import Stream_Reader
from Stream_Writer import Stream_Writer

class Distillate(qdf.QuasarDistillate):


    def setup(self, opts):
        """
        Initializes distillate parameters options from dictionary 'opts'
        Creates dataset in appropraite path
        """
        #save opts as class attribute
        self.opts = opts

        #This is the first level in the distillate tree
        self.set_author(opts['author'])

        #This is the second level. This name should be unique for every algorithm you write
        self.set_name(opts['name'])

        #This is the final level. You can have multiple of these
        for i in range(len(opts['output_streams'])):
          self.add_stream(opts['output_streams'][i], opts['output_units'][i])

        for i in range(len(opts['input_streams'])):
          self.use_stream(opts['input_streams'][i], opts['input_uids'][i])

        #If this is incremented, it is assumed that the whole distillate is invalidated, and it
        #will be deleted and discarded. In addition all 'persist' data will be removed
        self.set_version(opts['version'])

    @defer.inlineCallbacks
    def compute(self):
        """
        This is called to compute your algorithm.

        This distillate scales an input stream by a constant factor
        """

        if self.unpersist("done",False):
            print "Already done"
            return

        input_streams = []
        for i in range(len(self.opts['input_streams'])):
          input_stream = self.opts['input_streams'][i]
          start_date = self.date(self.opts['start_dates'][i])
          end_date = self.date(self.opts['end_dates'][i])
          input_streams.append(Stream_Reader(self, input_stream, start_date, end_date))

        output_streams = []
        for i in range(len(self.opts['output_streams'])):
          output_stream = self.opts['output_streams'][i]
          output_streams.append(Stream_Writer(self, output_stream))

        yield self.opts['algorithm'](input_streams, output_streams)

        #Now that we are done, save the time we finished at
        self.persist("done", True)

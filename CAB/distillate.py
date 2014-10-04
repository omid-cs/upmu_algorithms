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

        input_versions = []
        input_streams = []
        
        current_date = self.date(self.opts['start_date'])
        end_date = self.date(self.opts['end_date'])

        # take 15 minute windows
        while current_date < end_date:
          window_end = current_date + 15 * qdf.MINUTE

          # final window edge case
          if window_end > end_date:
            window_end = end_date
          
          # fill input_streams array with all streams for a 15 minute time window
          for i in range(len(self.opts['input_streams'])):
            input_name = self.opts['input_streams'][i]
            input_version, input_values = yield self.stream_get(input_name, current_date, window_end)
            input_versions.append(input_version)
            input_streams.append(input_values)

          #opts['algorithm']() is a function where the algorithm is implememted for the distillate
          #when this function returns, all data from input streams will have been processed,
          #  and the results passed into the output streams for the 15 minute window of data
          self.opts['algorithm'](input_streams, self.opts['output_streams'])
          
          #reset input versions and streams
          input_versions = []
          input_streams = []

          current_date += 15 * qdf.MINUTE

        #Now that we are done, save the time we finished at
        self.persist("done", True)

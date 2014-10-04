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

        input_versions, input_streams = [], []

        # take 15 minute windows
        current_date = start_date
        while current < end_date:
          window_end = current_date + 15 * qdf.MINUTE

          # final window edge case
          if window_end > end:
            window_end = end
          
          # fill input_streams array with all streams for a 15 minute time window
          for i in range(len(opts['input_names'])):
            input_name = opts['input_names'][i]
            start_date = opts['start_dates'][i]
            end_date   = opts['end_dates'][i]
            input_version, input_values = yield self.stream_get(input_name, current, window_end)
            input_versions.append(input_version)
            input_stream.append(input_values)

          #opts['algorithm']() is a function where the algorithm is implememted for the distillate
          #when this function returns, all data from input streams will have been processed,
          #  and the results passed into the output streams for the 15 minute window of data
          opts['algorithm'](input_streams, opts['output_streams'])

          current += 15 * qdf.MINUTE

        #Now that we are done, save the time we finished at
        self.persist("done", True)

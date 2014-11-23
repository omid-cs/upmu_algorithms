__author__ = 'immesys'

import numpy as np
import qdf
from twisted.internet import defer

class DeleteStream(qdf.QuasarDistillate):

    def setup(self, opts):
        """
        This constructs your distillate algorithm
        """
        #This is the first level in the distillate tree
        self.set_author("CAB")

        #This is the second level. This name should be unique for every algorithm you write
        self.set_name("dev")

        #This is the final level. You can have multiple of these
        self.use_stream("del", "589f0dbe-8855-49f2-b30e-3c64440673de")

        #If this is incremented, it is assumed that the whole distillate is invalidated, and it
        #will be deleted and discarded. In addition all 'persist' data will be removed
        self.set_version(4)

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
        end_date = self.date("2014-10-01T00:01:00.000000")

        self.stream_delete_range("dev", start_date, end_date)

        #Now that we are done, save the time we finished at
        self.persist("done", True)


qdf.register(DeleteStream())
qdf.begin()

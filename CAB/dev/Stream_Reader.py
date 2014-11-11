import numpy as np
import qdf
from twisted.internet import defer

"""
Constants
""" 
SAMPLE_RATE = 120 # samples per second
CACHE_ENTRIES = 4
BLOCK_SIZE = 15*60*SAMPLE_RATE

CACHE_INDEX_TAG = 0
CACHE_INDEX_DATA = 1

class Stream_Reader():
  """
  This class requests data from a database by managing a cache
  IO for the object is similar to python lists, and implementation of caching is
  hidden from the user.

  Cache details:
    directly mapped
    15 minute block size (max 54000 data points)
    uses first timestamp of block as faux tag

  Notes:
    Will thrash if points are (n*qdf.HOUR +- 15 minutes), where n in an integer
  """
  def __init__(self, quasar, name, start_date, end_date):
    """
    initializes stream with empty caches

    params --
      QuasarDistillate quasar:
        object with stream acquisition and storage methods
      str name:
        the name of the stream to read from 
      int start_date:
        the date-time of the begining of the stream
      int end_date:
        the date-time of the end of the stream
    """
    self.quasar = quasar
    self.name = name
    self.start = start_date
    self.end = end_date

    self.cache = [[None, None] for x in range(CACHE_ENTRIES)]

  @defer.inlineCallbacks
  def __getitem__(self, key):
    """
    returns the point specified by the slicing index

    Calculates offset, index, and tag to identify a cache hit or cache miss, and to index into
      the cache to return the correct value

    The tag is the initial timestamp of the block

    On miss, queries data from database to update the cache
    """
    if isinstance(key, int):
      if key < 0:
        raise IndexError('Cannot index less than 0')
      offset = key % BLOCK_SIZE
      index = (key/BLOCK_SIZE) % CACHE_ENTRIES
      tag = self.start + ((((key/BLOCK_SIZE)*BLOCK_SIZE)/SAMPLE_RATE)*qdf.SECOND)
      if self.cache[index][CACHE_INDEX_TAG] == None:
        #cache entry is empty
        yield self._query_data(index, tag)
      elif self.cache[index][CACHE_INDEX_TAG] != tag:
        #cache miss
        yield self._query_data(index, tag)
      datapoint = self.cache[index][CACHE_INDEX_DATA][offset]
      if datapoint.time > self.end:
        raise IndexError('Requested date past end-date:\n'+
                         'End-Date: '+str(self.end)+'\n'+
                         'Requested-Date: '+str(self.cache[index][offset].time))
      defer.returnValue(datapoint)

    elif isinstance(key, slice):
      #not implemented yet
      raise TypeError('list indices must be integers, not '+type(key))
    else: #slice error
      raise TypeError('list indices must be integers, not '+type(key))

  @defer.inlineCallbacks
  def _query_data(self, index, tag):
    """
    Queries data from database, storing it into cache index specified
    Write back is NOT implemented as this stream is read-only

    Data is preprocessed such that indices correspond to times, not datapoints
    """
    version, datapoints = yield self.quasar.stream_get(self.name, tag, tag+(15*qdf.MINUTE))
    values = np.empty((BLOCK_SIZE,), dtype=(type(datapoints[0])))
    time_index[:] = None
    
    for point in datapoints:
      time = float(point.time - tag)
      time_index = int(round(time*SAMPLE_RATE/qdf.SECOND))
      values[time_index] = point

    self.cache[index][CACHE_INDEX_TAG] = tag
    self.cache[index][CACHE_INDEX_DATA] = values

  def __iter__(self):
    i = 0
    time = self[i].time
    while time < self.end:
      point = self[i]
      i += 1
      time = point.time
      yield point

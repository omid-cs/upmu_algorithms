import numpy as np
import qdf

"""
Constants
""" 
CACHE_ENTRIES = 4
BLOCK_SIZE = 15*60*60
SAMPLE_RATE = 60

class Stream_Reader():
  """
  This class requests data from a database by managing a cache
  IO for the object is similar to python lists, and implementation of caching is
  hidden from the user.

  Cache details:
    directly mapped
    15 minute block size (54000 data points)
    uses first timestamp of block as faux tag

  Notes:
    Will thrash if points are (n*qdf.HOUR +- 15 minutes), where n in an integer
  """
  def __init__(self, quasar, name, start_date, end_date):
    """
    initializes stream with empty caches

    params --
      QuasarDistillate quasar:
        object with stream aquisition and storage methods
      str name:
        the name of the stream to read from 
    """
    self.quasar = quasar
    self.name = name
    self.start = start_date
    self.end = end_date

    self.cache = np.zeros([CACHE_ENTRIES, BLOCK_SIZE])

  def __getitem__(self, key):
    """
    returns the point specified by the slicing index

    Calculates offset, index, and tag to identify a cache hit or cache miss, and to index into
      the cache to return the correct value

    On miss, queries data from database to update the cache
    """
    if isinstance(key, int):
      offset = (key % BLOCK_SIZE)
      index = (key/BLOCK_SIZE) % 4
      tag = (((key/BLOCK_SIZE)*BLOCK_SIZE) / SAMPLE_RATE * qdf.SECOND)
      if self.cache[index][0] == 0:
        #cache entry is empty
        self._query_data(index, tag)
      elif self.cache[index][0] != tag:
        #cache miss
        self._query_data(index, tag)
      return self.cache[index][offset]

    elif isinstance(key, slice):
      #not implemented yet
      return 0
    else: #slice error
      return 1
    
  def _query_data(self, index, tag):
    """
    Queries data from database, storing it into cache index specified
    Write back is NOT implemented as this stream is read-only
    """
    version, values = yield quasar.stream_get(self.name, tag, tag+(15*qdf.MINUTE))
    self.cache[index] = values

  def __iter__(self):
    i = 0
    time = quasar.date(self[i].time)
      while time < self.end_date:
        point = self[i]
        i += 1
        time = quasar.date(point.time)
        yield point

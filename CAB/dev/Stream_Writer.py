import qdf

class Stream_Writer():
  """
  This class stores data into a database by managing a buffer for output.
  IO for the object is similar to python lists, and implementation of caching is
  hidden from the user.

  Buffer details:
    length: qdf.OPTIMAL_BATCH_SIZE

  """
  def __init__(self, quasar, name):
    """
    initializes stream with an empty buffer

    params --
      QuasarDistillate quasar:
        object with stream aquisition and storage methods
      str name:
        the name of the stream to write to 
    """
    self.quasar = quasar
    self.name = name

    self.buf = []

  def append(self, point):
    """
    Saves point specified by the slicing index

    When buffer is full, it is flushed to the stream
    """
    self.buf.append(point)
    if len(self.buf) == qdf.OPTIMAL_BATCH_SIZE:
      quasar.stream_insert_multiple(self.name, self.buf)
      buf = []

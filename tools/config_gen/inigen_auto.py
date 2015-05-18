from inigen import IniGen
import algorithm_fields
from os import mkdir
import re

# CONSTANTS
MINTIME = '2014-12-01T00:00:00'
MAXTIME = '2016-12-01T00:00:00'
CHUNKING = 'parallel'

class IniGenAutomation():
  """
    This class automates the process of generating distillate parameter files ('ini' files) when
     a uPMU with raw data streams is brought online.

      - all raw streams are 'cleaned' first.
        + all requested algorithms are run from clean data stream
      - assumes every upmu samples at 120hz
      - assumes every upmu has 13 channels: C1-3MAG, C1-3ANG, L1-3MAG, L1-3ANG, and LSTATE
      - sets mintime to Dec 1st, 2014
      - sets maxtime to Dec 1st, 2016
  """
  def __init__(self, location, name, uuid_map, ref_name, reference_uuid_map,
               algs=['frequency','angle_difference']):
    """
      str location: the abbreviation for the location of the upmu (e.g. "LBNL")

      str ref_name: the abbreviation for the name of the reference upmu (e.g. "A6_BUS2")

      str name: the abbreviation for the name of the upmu (e.g. "A6_BUS2")

      dict<String,String> uuid_map: a mapping of stream names to corresponding uuid
        (e.g. {'C1MAG':'00000000-0000-0000-0000-000000000000', 'L3ANG':...})

      str reference_uuid_map: a mapping of reference stream names to corresponding uuid
        (e.g. {'C1MAG':'00000000-0000-0000-0000-000000000000', 'L3ANG':...})


      str[] algs: list of algorithms to run on this stream. Dictates what ini's gen generated
        NOTE: 'clean' is always run so is implicitly part of this list.
    """
    # build a mapping from string name of algorithm to object method
    self.alg_map = {
      'frequency' : self.frequency,
      'angle_difference' : self.angle_difference
    }

    # verify parameter types
    assert type(location) == str
    assert type(name) == str
    assert type(uuid_map) == dict
    assert type(ref_name) == str
    assert type(reference_uuid_map) == dict
    assert type(algs) == list
    for alg in algs:
      assert (alg in self.alg_map)

    self.location = location
    self.name = name
    self.uuid_map = uuid_map
    self.ref_name = ref_name
    self.reference_uuid_map = reference_uuid_map
    self.algs = algs

    # create a new directory for ini files and store the directory name
    self.dirname = self.create_directory()

    # start the automation
    self.generate_runs()

  def generate_runs(self):
    clean_uuid_map = self.clean()
    self.uuid_map = clean_uuid_map

    for alg in algs:
      self.alg_map[alg]()

  def clean(self):
    """
      generates the 'clean' distillates file
      13 runs, one for each stream
      returns a mapping from original names to newly created clean uuids
    """
    inigen = IniGen()
    fields = algorithm_fields.algorithms['clean']

    # list of output uuids for cleaning distillate
    clean_uuid_map = {}

    # set up global parameters
    algorithm_path = fields['path']
    enabled = "True"
    inigen.emit_global(algorithm_path, enabled)

    for label in self.uuid_map:
      # header
      inigen.emit_run_header(label, CHUNKING, MINTIME, MAXTIME)

      # body
      dep_label = label
      dep_name = fields['deps'][0]
      dep_uuid = self.uuid_map[label]
      deps = [[dep_label, dep_name, dep_uuid]]

      param_section_name = fields['params'][0]
      param_section_value = "Development" # [CB] Need naming convention
      param_name_name = fields['params'][1]
      param_name_value = "inigen_automation/clean" # [CB] Need naming convention
      param_type_name = fields['params'][2]
      param_type_value = get_stream_type(label)
      params = [[param_section_name, param_section_value],
                [param_name_name, param_name_value],
                [param_type_name, param_type_value]]

      outputs = fields['outputs']

      emitted = inigen.emit_run_body(deps, params, outputs)

      clean_uuid_map[label] = emitted[-2][-36:]

    filename = "{0}/CLEAN_{1}.ini".format(self.dirname, self.name)
    inigen.generate_file(filename)
    return clean_uuid_map

  def frequency(self):
    """
      generates the 'frequency' distillates file
      1 run, on L1ANG
    """
    inigen = IniGen()
    fields = algorithm_fields.algorithms['frequency']

    # set up global parameters
    algorithm_path = fields['path']
    enabled = "True"
    inigen.emit_global(algorithm_path, enabled)

    for label in self.uuid_map:
      # header
      inigen.emit_run_header(label, CHUNKING, MINTIME, MAXTIME)

      # body
      dep_label = label
      dep_name = fields['deps'][0]
      dep_uuid = self.uuid_map[label]
      deps = [[dep_label, dep_name, dep_uuid]]

      param_section_name = fields['params'][0]
      param_section_value = "Development" # [CB] Need naming convention
      param_name_name = fields['params'][1]
      param_name_value = "inigen_automation/frequency" # [CB] Need naming convention
      params = [[param_section_name, param_section_value],
                [param_name_name, param_name_value]]

      outputs = fields['outputs']

      inigen.emit_run_body(deps, params, outputs)

    filename = "{0}/FREQ_{1}.ini".format(self.dirname, self.name)
    inigen.generate_file(filename)

  def angle_difference(self):
    """
      generates the 'angle_difference' distillates file
      6 runs, one for each ANG stream
      Difference calculated relative to reference upmu
    """
    inigen = IniGen()
    fields = algorithm_fields.algorithms['angle_difference'] # [CB] implement in algorithm_fields.py

    # set up global parameters
    algorithm_path = fields['path']
    enabled = "True"
    inigen.emit_global(algorithm_path, enabled)

    for label in self.uuid_map:
      # header
      inigen.emit_run_header(label, CHUNKING, MINTIME, MAXTIME)

      # body
      dep_ref_label = "{0} {1}".format(label, self.ref_name)
      dep_ref_name = fields['deps'][0]
      dep_ref_uuid = self.reference_uuid_map[label]
      dep_label = "{0} {1}".format(label, self.name)
      dep_name = fields['deps'][1]
      dep_uuid = self.uuid_map[label]
      deps = [[dep_ref_label, dep_ref_name, dep_ref_uuid], [dep_label, dep_name, dep_uuid]]

      param_section_name = fields['params'][0]
      param_section_value = "Development" # [CB] Need naming convention
      param_name_name = fields['params'][1]
      param_name_value = "inigen_automation/angle_difference" # [CB] Need naming convention
      params = [[param_section_name, param_section_value],
                [param_name_name, param_name_value]]

      outputs = fields['outputs']

      inigen.emit_run_body(deps, params, outputs)

    filename = "{0}/ANG-DIFF_{1}.ini".format(self.dirname, self.name)
    inigen.generate_file(filename)

  def fundamental_power(self):
    """
      generates the 'fundamental_power' distillates file
      1 run for a single line in a uPMU
    """
    raise NotImplementedError
 
  def reactive_power(self):
    """
      generates the 'reactive_power' distillates file
      1 run for a single line in a uPMU
    """
    raise NotImplementedError

  def dpf(self):
    """
      generates the 'dpf' distillates file
      1 run for a single line in a uPMU
    """
    raise NotImplementedError

  def sequence(self):
    """
      generates the 'dpf' distillates file
      1 run for a single line in a uPMU
    """
    raise NotImplementedError

  def create_directory(self):
    """
      creates a new directory with the same name as the uPMU name
      if directory already exists, append counter to end until free name is found
      returns the name of the directory created
    """
    dirname = self.name+"_distillates"
    i = 1
    while True:
      try:
        mkdir(dirname)
        return dirname
      except OSError:
        dirname = name+"_distillates_{0}".format(i)
        i += 1

def get_stream_type(label):
  pattern_CANG = re.compile('C[0-9]ANG')
  pattern_CMAG = re.compile('C[0-9]MAG')
  pattern_LANG = re.compile('L[0-9]ANG')
  pattern_LMAG = re.compile('L[0-9]MAG')
  match_CANG = re.match(pattern_CANG, label)
  match_CMAG = re.match(pattern_CMAG, label)
  match_LANG = re.match(pattern_LANG, label)
  match_LMAG = re.match(pattern_LMAG, label)

  if match_CANG:
    return "CANG"
  if match_CMAG:
    return "CMAG"
  if match_LANG:
    return "LANG"
  if match_LMAG:
    return "LMAG"
  else:
    return "ARB"

if __name__ == "__main__":
  location = "LOCation"
  name = "test_Name"
  uuid_map = {'C1MAG' : '00', 'C2MAG' : '11', 'L1ANG' : '22', 'L2ANG' : '33'}
  ref_name = "test_Ref_Name"
  reference_uuid_map = {'C1MAG' : '44', 'C2MAG' : '55', 'L1ANG' : '66', 'L2ANG' : '77'}
  algs = ['frequency', 'angle_difference']
  iniGenAutomation = IniGenAutomation(location, name, uuid_map, ref_name, reference_uuid_map, algs=['frequency', 'angle_difference'])


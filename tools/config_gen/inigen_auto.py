from inigen import IniGen
import algorithm_fields
from os import mkdir
import re

# CONSTANTS
MINTIME = '2014-12-13T00:00:00'
MAXTIME = '2014-12-15T00:00:00'
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
  def __init__(self, location, name_raw, name, uuid_map, ref_name, reference_uuid_map, algs):
    """
      str location: the abbreviation for the location of the upmu (e.g. "LBNL")

      str name_raw: the original name of the upmu as dictated by the raw stream (e.g. "bank_514")

      str name: the abbreviation for the name of the upmu (e.g. "A6_BUS2")

      dict<String,String> uuid_map: a mapping of stream names to corresponding uuid
        (e.g. {'C1MAG':'00000000-0000-0000-0000-000000000000', 'L3ANG':...})

      str ref_name: the abbreviation for the name of the reference upmu (e.g. "A6_BUS2")

      str reference_uuid_map: a mapping of reference stream names to corresponding uuid
        (e.g. {'C1MAG':'00000000-0000-0000-0000-000000000000', 'L3ANG':...})

      str[] algs: list of algorithms to run on this stream. Dictates what ini's gen generated
        NOTE: 'clean' is always run so is implicitly part of this list.
    """
    # verify parameter types
    assert type(location) == str
    assert type(name_raw) == str
    assert type(name) == str
    assert type(uuid_map) == dict
    assert type(ref_name) == str
    assert type(reference_uuid_map) == dict
    assert type(algs) == list

    self.location = location
    self.name_raw = name_raw
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

    if 'frequency' in self.algs:
      self.frequence_uuid_map = self.frequency()
    if 'angle_difference' in self.algs:
      self.angle_difference_uuid_map = self.angle_difference()
    if 'dpf' in self.algs:
      self.dpf_uuid_map = self.dpf()
    if 'rpfp' in self.algs:
      self.rpfp_uuid_map = self.rpfp()
    if 'sequence' in self.algs:
      self.sequence_uuid_map = self.sequence()
    if 'sequence_ref' in self.algs:
      self.sequence_ref_uuid_map = self.sequence_ref()
    if 'filter' in self.algs:
      self.filter_uuid_map = self.filter()

  def clean(self):
    """
      generates the 'clean' distillates file
      13 runs, one for each stream
      returns a mapping from original names to newly created clean uuids
    """
    inigen = IniGen()
    fields = algorithm_fields.algorithms['clean']

    # list of output uuids for cleaning distillate
    output_uuid_map = {}

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
      param_section_value = "Clean/{0}".format(self.name_raw)
      param_name_name = fields['params'][1]
      param_name_value = label
      param_type_name = fields['params'][2]
      param_type_value = get_stream_type(label)
      params = [[param_section_name, param_section_value],
                [param_name_name, param_name_value],
                [param_type_name, param_type_value]]

      outputs = fields['outputs']

      emitted = inigen.emit_run_body(deps, params, outputs)

      output_uuid_map[label] = emitted[-2][-36:]

    filename = "{0}/CLEAN_{1}.ini".format(self.dirname, self.name)
    inigen.generate_file(filename)
    return output_uuid_map

  def frequency(self):
    """
      generates the 'frequency' distillates file
      1 run, on L1ANG
    """
    inigen = IniGen()
    fields = algorithm_fields.algorithms['frequency']

    output_uuid_map = {}

    # set up global parameters
    algorithm_path = fields['path']
    enabled = "True"
    inigen.emit_global(algorithm_path, enabled)

    for label in self.uuid_map:
      if label == 'LSTATE':
        distillate_label = label
      else:
        distillate_label = get_distillate_label([label])

      # header
      inigen.emit_run_header(label, CHUNKING, MINTIME, MAXTIME)

      # body
      dep_label = label
      dep_name = fields['deps'][0]
      dep_uuid = self.uuid_map[label]
      deps = [[dep_label, dep_name, dep_uuid]]

      param_section_name = fields['params'][0]
      param_section_value = "Production/{0}/{1}".format(self.location, distillate_label)
      param_name_name = fields['params'][1]
      param_name_value = "FREQ"
      params = [[param_section_name, param_section_value],
                [param_name_name, param_name_value]]

      outputs = fields['outputs']

      emitted = inigen.emit_run_body(deps, params, outputs)

      output_uuid_map[label+"_1-SEC"] = emitted[-3][-36:]
      output_uuid_map[label+"_C37"] = emitted[-2][-36:]

    filename = "{0}/FREQ_{1}.ini".format(self.dirname, self.name)
    inigen.generate_file(filename)
    return output_uuid_map

  def angle_difference(self):
    """
      generates the 'angle_difference' distillates file
      6 runs, one for each ANG stream
      Difference calculated relative to reference upmu
    """
    inigen = IniGen()
    fields = algorithm_fields.algorithms['angle_difference']

    output_uuid_map = {}

    # set up global parameters
    algorithm_path = fields['path']
    enabled = "True"
    inigen.emit_global(algorithm_path, enabled)

    for label in self.uuid_map:
      if label == 'LSTATE':
        distillate_label = label
      else:
        distillate_label = get_distillate_label([label])

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
      param_section_value = "Production/{0}/{1}/{2}/{3}".format(self.location, self.ref_name, self.name, distillate_label)
      param_name_name = fields['params'][1]
      param_name_value = "ANGLE-DIFF"
      params = [[param_section_name, param_section_value], [param_name_name, param_name_value]]

      outputs = fields['outputs']

      emitted = inigen.emit_run_body(deps, params, outputs)

      output_uuid_map[label] = emitted[-2][-36:]

    filename = "{0}/ANG-DIFF_{1}.ini".format(self.dirname, self.name)
    inigen.generate_file(filename)
    return output_uuid_map

  def dpf(self):
    """
      generates the 'dpf' distillates file
      3 runs, 1 run for a each line in a uPMU
    """
    inigen = IniGen()
    fields = algorithm_fields.algorithms['dpf']

    output_uuid_map = {}

    # set up global parameters
    algorithm_path = fields['path']
    enabled = "True"
    inigen.emit_global(algorithm_path, enabled)

    for i in xrange(1,4):
      label = "DPF{0}".format(str(i))
      lAng_label = 'L{0}ANG'.format(str(i))
      cAng_label = 'C{0}ANG'.format(str(i))
      distillate_label = get_distillate_label([lAng_label, cAng_label])

      # header
      inigen.emit_run_header(label, CHUNKING, MINTIME, MAXTIME)

      # body
      dep_lAng_label = lAng_label
      dep_lAng_name = fields['deps'][0]
      dep_lAng_uuid = self.uuid_map[lAng_label]
      dep_cAng_label = cAng_label
      dep_cAng_name = fields['deps'][1]
      dep_cAng_uuid = self.uuid_map[cAng_label]
      deps = [[dep_lAng_label, dep_lAng_name, dep_lAng_uuid],
              [dep_cAng_label, dep_cAng_name, dep_cAng_uuid]]

      param_section_name = fields['params'][0]
      param_section_value = "Production/{0}/{1}/{2}".format(self.location, self.name, distillate_label)
      param_name_name = fields['params'][1]
      param_name_value = "DPF"
      params = [[param_section_name, param_section_value], [param_name_name, param_name_value]]

      outputs = fields['outputs']

      emitted = inigen.emit_run_body(deps, params, outputs)

      output_uuid_map[label] = emitted[-2][-36:]

    filename = "{0}/DPF_{1}.ini".format(self.dirname, self.name)
    inigen.generate_file(filename)
    return output_uuid_map

  def rpfp(self):
    """
      generates the 'rpfp' distillates file
      3 runs, 1 for each line in a uPMU
    """
    inigen = IniGen()
    fields = algorithm_fields.algorithms['rpfp']

    output_uuid_map = {}

    # set up global parameters
    algorithm_path = fields['path']
    enabled = "True"
    inigen.emit_global(algorithm_path, enabled)

    for i in xrange(1,4):
      label = "RPFP{0}".format(str(i))
      distillate_label = "L{0}-E_C{1}".format(str(i),str(i))
      lAng_label = 'L{0}ANG'.format(str(i))
      cAng_label = 'C{0}ANG'.format(str(i))
      lMag_label = 'C{0}MAG'.format(str(i))
      cMag_label = 'C{0}MAG'.format(str(i))
      distillate_label = get_distillate_label([lAng_label, cAng_label, lMag_label, cMag_label])

      # header
      inigen.emit_run_header(label, CHUNKING, MINTIME, MAXTIME)

      # body
      dep_lAng_label = lAng_label
      dep_lAng_name = fields['deps'][0]
      dep_lAng_uuid = self.uuid_map[lAng_label]
      dep_cAng_label = cAng_label
      dep_cAng_name = fields['deps'][1]
      dep_cAng_uuid = self.uuid_map[cAng_label]
      dep_lMag_label = lMag_label
      dep_lMag_name = fields['deps'][2]
      dep_lMag_uuid = self.uuid_map[lMag_label]
      dep_cMag_label = cMag_label
      dep_cMag_name = fields['deps'][3]
      dep_cMag_uuid = self.uuid_map[cMag_label]
       
      deps = [[dep_lAng_label, dep_lAng_name, dep_lAng_uuid],
              [dep_lMag_label, dep_lMag_name, dep_lMag_uuid],
              [dep_cAng_label, dep_cAng_name, dep_cAng_uuid],
              [dep_cMag_label, dep_cMag_name, dep_cMag_uuid]]

      param_section_name = fields['params'][0]
      param_section_value = "Production/{0}/{1}/{2}".format(self.location, self.name, distillate_label)
      param_name_name = fields['params'][1]
      param_name_value = "RPFP"
      params = [[param_section_name, param_section_value], [param_name_name, param_name_value]]

      outputs = fields['outputs']

      emitted = inigen.emit_run_body(deps, params, outputs)

      output_uuid_map['REAC_PWR{0}'.format(i)] = emitted[-3][-36:]
      output_uuid_map['FUND_PWR{0}'.format(i)] = emitted[-2][-36:]

    filename = "{0}/RPFP_{1}.ini".format(self.dirname, self.name)
    inigen.generate_file(filename)
    return output_uuid_map

  def sequence(self):
    """
      generates the 'sequence' distillates file
      1 run for a uPMU
    """
    inigen = IniGen()
    fields = algorithm_fields.algorithms['sequence']

    output_uuid_map = {}

    # set up global parameters
    algorithm_path = fields['path']
    enabled = "True"
    inigen.emit_global(algorithm_path, enabled)

    label = "SEQ"
    for t in ['C','L']:
      run_label = label+'_'+t
      t1Mag_label = '{0}1MAG'.format(t)
      t2Mag_label = '{0}2MAG'.format(t)
      t3Mag_label = '{0}3MAG'.format(t)
      t1Ang_label = '{0}1ANG'.format(t)
      t2Ang_label = '{0}2ANG'.format(t)
      t3Ang_label = '{0}3ANG'.format(t)
      distillate_label = "{0}-ALL".format(t)

      # header
      inigen.emit_run_header(run_label, CHUNKING, MINTIME, MAXTIME)

      # body
      dep_1Mag_label = t1Mag_label
      dep_1Mag_name = fields['deps'][0]
      dep_1Mag_uuid = self.uuid_map[t1Mag_label]

      dep_2Mag_label = t2Mag_label
      dep_2Mag_name = fields['deps'][1]
      dep_2Mag_uuid = self.uuid_map[t2Mag_label]

      dep_3Mag_label = t3Mag_label
      dep_3Mag_name = fields['deps'][2]
      dep_3Mag_uuid = self.uuid_map[t3Mag_label]

      dep_1Ang_label = t1Ang_label
      dep_1Ang_name = fields['deps'][3]
      dep_1Ang_uuid = self.uuid_map[t1Ang_label]

      dep_2Ang_label = t2Ang_label
      dep_2Ang_name = fields['deps'][4]
      dep_2Ang_uuid = self.uuid_map[t2Ang_label]

      dep_3Ang_label = t3Ang_label
      dep_3Ang_name = fields['deps'][5]
      dep_3Ang_uuid = self.uuid_map[t3Ang_label]
      
      deps = [[dep_1Mag_label, dep_1Mag_name, dep_1Mag_uuid],
              [dep_2Mag_label, dep_2Mag_name, dep_2Mag_uuid],
              [dep_3Mag_label, dep_3Mag_name, dep_3Mag_uuid],
              [dep_1Ang_label, dep_1Ang_name, dep_1Ang_uuid],
              [dep_2Ang_label, dep_2Ang_name, dep_2Ang_uuid],
              [dep_3Ang_label, dep_3Ang_name, dep_3Ang_uuid]]

      param_section_name = fields['params'][0]
      param_section_value = "Production/{0}/{1}/{2}".format(self.location, self.name, distillate_label)
      param_name_name = fields['params'][1]
      param_name_value = "SEQ"
      params = [[param_section_name, param_section_value], [param_name_name, param_name_value]]

      outputs = fields['outputs']

      emitted = inigen.emit_run_body(deps, params, outputs)

      output_uuid_map["ZER_{0}ANG".format(t)] = emitted[-9][-36:]
      output_uuid_map["ZER_{0}MAG".format(t)] = emitted[-8][-36:]
      output_uuid_map["POS_{0}ANG".format(t)] = emitted[-7][-36:]
      output_uuid_map["POS_{0}MAG".format(t)] = emitted[-6][-36:]
      output_uuid_map["NEG_{0}ANG".format(t)] = emitted[-5][-36:]
      output_uuid_map["NEG_{0}MAG".format(t)] = emitted[-4][-36:]
      output_uuid_map["UNB_{0}NEG".format(t)] = emitted[-3][-36:]
      output_uuid_map["UNB_{0}ZER".format(t)] = emitted[-2][-36:]

    filename = "{0}/SEQ_{1}.ini".format(self.dirname, self.name)
    inigen.generate_file(filename)
    return output_uuid_map

  def sequence_ref(self):
    return None

  def filter(self):
    return None

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
        dirname = self.name+"_distillates_{0}".format(i)
        i += 1

def get_distillate_label(labels):
  distillate_label_list = []
  for label in labels:
    pattern = re.compile('(C|L)([0-9])(ANG|MAG)')
    match = re.match(pattern, label)
    if match.group(1) == 'L':
      distillate_label_list.append("{0}{1}-E-{2}".format(match.group(1), match.group(2), match.group(3)))
    else:
      distillate_label_list.append("{0}{1}-{2}".format(match.group(1), match.group(2), match.group(3)))
  return "_".join(distillate_label_list)


def get_stream_type(label):
  pattern = re.compile('(C|L)([0-9])(ANG|MAG)')
  match = re.match(pattern, label)
  if match:
    return match.group(1) + match.group(3)
  else:
     return "ARB"

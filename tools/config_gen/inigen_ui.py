from algorithm_fields import algorithms
from inigen import IniGen
import re
from uuid import UUID

gen = IniGen()

print "* * *     Welcome to the config file generation UI     * * *\n"
print "- - -     Global Settings     - - - "
prompt_text = 'Generated config file name: '
filename = raw_input(prompt_text)

prompt_text = ['Algorithm:']
for alg in algorithms.keys():
  prompt_text.append('\t- {0}'.format(alg))
prompt_text.append('-> ')
prompt_text = "\n".join(prompt_text)
while True:
  algorithm = raw_input(prompt_text)
  if algorithm not in algorithms.keys():
    print "Invalid algorithm. Select one from the list"
  else:
    break

prompt_text = 'Enabled (True or False): '
while True:
  enabled = raw_input(prompt_text)
  if enabled not in ['True', 'False']:
    print "Invalid boolean. Select 'True' or 'False'"
  else:
    break

p = re.compile('^[0-9][0-9][0-9][0-9]\-[0-9][0-9]\-[0-9][0-9]T[0-9][0-9]\:[0-9][0-9]\:[0-9][0-9]$')
prompt_text = 'Min Time [yyyy-mm-ddThh:mm:ss]: '
while True:
  mintime = raw_input(prompt_text)
  if not p.match(mintime):
    print "Invalid timestamp. Select time in form yyyy-mm-ddThh:mm:ss"
  else:
    break


prompt_text = 'Max Time [yyyy-mm-ddThh:mm:ss]: '
while True:
  maxtime = raw_input(prompt_text)
  if not p.match(maxtime):
    print "Invalid timestamp. Select time in form yyyy-mm-ddThh:mm:ss"
  else:
    break

prompt_text = 'Number of runs: '
while True:
  num_runs = raw_input(prompt_text)
  try:
    num_runs = int(num_runs)
    if num_runs < 0:
      raise ValueError
  except ValueError:
    print "Invalid runs. Select a positive integer value"
    continue
  break

settings = algorithms[algorithm]
gen.emit_global(settings['path'], enabled)

run_num = 1
while run_num <= num_runs:
  print "- - -     Run Settings: run {0}     - - - ".format(str(run_num))
  prompt_text = "Run Label: "
  label = raw_input(prompt_text)

  deps_info = []
  print "Dependencies: "
  for dep in settings['deps']:
    prompt_text = "\t{0} (description): ".format(dep)
    comment = raw_input(prompt_text)

    prompt_text = "\t{0} (uuid): ".format(dep)
    while True:
      uuid = raw_input(prompt_text)
      try:
        UUID(uuid)
        uuid = uuid.lower()
        break
      except ValueError:
        print "\tInvalid uuid format. Select an appropriate uuid dependency"
        continue

    deps_info.append([comment, dep, uuid])

  params_info = []
  print "Parameters"
  for param in settings['params']:
    prompt_text = "\t{0}: ".format(param)
    param_val = raw_input(prompt_text)
    
    params_info.append([param, param_val])

  gen.emit_run_header(label, 'parallel', mintime, maxtime)
  gen.emit_run_body(deps_info, params_info, settings['outputs'])

  run_num += 1

gen.generate_file(filename)

from uuid import uuid4 as uuid

class IniGen():
  def __init__(self):
    self.emitted = []

  def emit_global(self, algorithm, enabled):
    emitted = []
    emitted.append("[ global ]")
    emitted.append("algorithm = {0}".format(algorithm))
    emitted.append("enabled = {0}".format(enabled))
    emitted.append("")

    for line in emitted:
      self.emitted.append(line)

    return emitted

  def emit_run_header(self, label, chunking, mintime, maxtime):
    emitted = []
    emitted.append("[ " + label + " ]")
    emitted.append("  chunking = {0}".format(chunking))
    emitted.append("  paramver = 1")
    emitted.append("")
    emitted.append("  mintime = {0}".format(str(mintime)))
    emitted.append("  maxtime = {0}".format(str(maxtime)))
    emitted.append("")

    for line in emitted:
      self.emitted.append(line)

    return emitted

  def emit_run_body(self, deps, params, outputs):
    emitted = []

    emitted.append("  [[ deps ]]")
    for dep in deps:
      emitted.append("  #{0}".format(dep[0]))
      emitted.append("  {0} = {1}".format(dep[1], dep[2]))
    emitted.append("")

    emitted.append("  [[ params ]]")
    for param in params:
      emitted.append("  {0} = {1}".format(param[0], param[1]))
    emitted.append("")

    emitted.append("  [[ outputs ]]")
    for output in outputs:
      emitted.append("  {0} = {1}".format(output, str(uuid())))
    emitted.append("")

    for line in emitted:
      self.emitted.append(line)

    return emitted

  def generate_file(self, filename):
    out_string = "\n".join(self.emitted)
    f = open(filename, 'w')
    f.write(out_string)
    f.close()

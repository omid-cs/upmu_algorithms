from uuid import uuid4 as uuid

class IniGen():
  def __init__(self):
    self.output = []

  def emit_global(self, algorithm, enabled):
    self.output.append("[ global ]")
    self.output.append("algorithm = {0}".format(algorithm))
    self.output.append("enabled = {0}".format(enabled))
    self.output.append("")

  def emit_run_header(self, label, chunking, mintime, maxtime):
    self.output.append("[ " + label + " ]")
    self.output.append("  chunking = {0}".format(chunking))
    self.output.append("  paramver = 1")
    self.output.append("")
    self.output.append("  mintime = {0}".format(str(mintime)))
    self.output.append("  maxtime = {0}".format(str(maxtime)))
    self.output.append("")

  def emit_run_body(self, deps, params, outputs):
    self.output.append("  [[ deps ]]")
    for dep in deps:
      self.output.append("  #{0}".format(dep[0]))
      self.output.append("  {0} = {1}".format(dep[1], dep[2]))
    self.output.append("")

    self.output.append("  [[ params ]]")
    for param in params:
      self.output.append("  {0} = {1}".format(param[0], param[1]))
    self.output.append("")

    self.output.append("  [[ outputs ]]")
    for output in outputs:
      self.output.append("  {0} = {1}".format(output, str(uuid())))
    self.output.append("")

  def generate_file(self, filename):
    out_string = "\n".join(self.output)
    f = open(filename, 'w')
    f.write(out_string)
    f.close()

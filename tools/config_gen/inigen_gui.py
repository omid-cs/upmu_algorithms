from algorithm_fields import algorithms
from inigen import IniGen
import re
from uuid import UUID

from Tkinter import Tk, E, W, N, S, Text, END, Scrollbar, RIGHT, LEFT, BOTH, Y, Checkbutton, IntVar
from ttk import Frame, Button, Label, Style, Combobox
from ttk import Entry

class IniGenGui(Frame):

  def __init__(self, parent):
    Frame.__init__(self, parent)
    self.parent = parent
    self.inigen = IniGen()
    self.initUIGlobals()

  def initUIGlobals(self):
    """
      This is the first part of the window to be rendered. After these have been
       set by the user and 'Emit Globals' has been clicked, the given algorithm
       can then specify how to generate the second part of the window. All fields
       are disabled for user input after globals have been emitted.

      Information in Global Parameters:
        Algorithm
          - name of the algorithm to use
        File Name
          - name of the output file to be generated
        Min Time
          - Minimum Time for distillers to run
        Max Time
          - Maximum Time for distillers to run
        Set Enabled:
          - checkbox to specify if the distiller should be enabled True or False
    """
    self.parent.title("Ini Generator")

    Style().configure("TButton", padding=(0, 5, 0, 5), font='serif 10')

    # initialize row counter. This is incremented after each element added to grid
    row = 0

    # Globals: entries for info common to all runs
    label_globals = Label(self, text="Globals")
    label_globals.grid(row=row, column=0)
    row += 1

    label_alg = Label(self, text="Algorithm")
    label_alg.grid(row=row, column=0, sticky=E+W)
    row += 1
    self.cbox_alg = Combobox(self, values=algorithms.keys(), state='readonly')
    self.cbox_alg.current(0)
    self.cbox_alg.grid(row=row, column=0, sticky=E+W+S+N)
    row += 1

    label_filename = Label(self, text="Output File Name")
    label_filename.grid(row=row, column=0, sticky=E+W)
    row += 1
    self.entry_filename = Entry(self)
    self.entry_filename.grid(row=row, column=0, sticky=W+E)
    row += 1

    label_mintime = Label(self, text="Min Time")
    label_mintime.grid(row=row, column=0, sticky=E+W)
    row += 1
    self.entry_mintime = Entry(self)
    self.entry_mintime.grid(row=row, column=0, sticky=W+E)
    row += 1

    label_maxtime = Label(self, text="Max Time")
    label_maxtime.grid(row=row, column=0, sticky=W+E)
    row += 1
    self.entry_maxtime = Entry(self)
    self.entry_maxtime.grid(row=row, column=0, sticky=W+E)
    row += 1

    self.enabled = IntVar()
    self.check_enabled = Checkbutton(self, text="set enabled", variable=self.enabled)
    self.check_enabled.grid(row=row, column=0, sticky=W+E)
    row += 1

    # Control: buttons used to emmiting text and generating file
    self.button_emit_globals = Button(self, text="Emit Globals", command=self.emit_globals)
    self.button_emit_globals.grid(row=row, column=0, sticky=W+E)
    row += 1

    button_addrun = Button(self, text="Add Run", command=self.emit_run)
    button_addrun.grid(row=row, column=0, sticky=W+E)
    row += 1

    button_generate = Button(self, text="Generate File", command=self.generate_file)
    button_generate.grid(row=row, column=0, sticky=W+E)
    row += 1

    self.pack()

  def initUIRuns(self):
    """
      Second part of gui to be rendered. This contains all the fields needed to emit
       a single run within a distiller file. Multiple runs can be added by clicking
       'Add Run' multiple times.

      Information in Run Parameters:
        Run Name
          - header name for run
        Dependencies
          - description and uuid fields for each dependency in the algorithm
        Params
          - parameter fields for each parameter in the algorithm
    """

    self.entry_run_name = None
    self.entries_dep_description = []
    self.entries_dep_uuid = []
    self.entries_param = []

    row = 0
    column = 1

    label_runs = Label(self, text="Runs")
    label_runs.grid(row=row, column=column)
    row += 1

    label_run_name = Label(self, text="Run Name")
    label_run_name.grid(row=row, column=column, sticky=W+E)
    row += 1

    self.entry_run_name = Entry(self)
    self.entry_run_name.grid(row=row, column=column, sticky=W+E)
    row += 1

    algorithm = self.cbox_alg.get()
    settings = algorithms[algorithm]

    for dep in settings['deps']:

      label_dep_description = Label(self, text="{0} (description)".format(dep))
      label_dep_description.grid(row=row, column=column, sticky=W+E)
      row += 1

      entry_dep_description = Entry(self)
      entry_dep_description.grid(row=row, column=column, sticky=W+E)
      row += 1

      label_dep_uuid = Label(self, text="{0} (uuid)".format(dep))
      label_dep_uuid.grid(row=row, column=column, sticky=W+E)
      row += 1

      entry_dep_uuid = Entry(self)
      entry_dep_uuid.grid(row=row, column=column, sticky=W+E)
      row += 1

      self.entries_dep_description.append(entry_dep_description)
      self.entries_dep_uuid.append(entry_dep_uuid)

    for param in settings['params']:

      label_param = Label(self, text=param)
      label_param.grid(row=row, column=column, sticky=W+E)
      row += 1

      entry_param = Entry(self)
      entry_param.grid(row=row, column=column, sticky=W+E)
      row += 1

      self.entries_param.append(entry_param)

    self.text_file = Text(self)
    self.text_file.grid(row=0, column=3, rowspan=row, sticky=W+E+N+S, padx=5, pady=5)
    scrollbar = Scrollbar(self, command=self.text_file.yview)
    self.text_file.config(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=0, column=4, rowspan=row, sticky=N+S)

    self.pack()

  def emit_globals(self):
    self.algorithm = algorithms[self.cbox_alg.get()]
    path = self.algorithm['path']
    if self.enabled.get():
      enabled = 'True'
    else:
      enabled = 'False'

    lines = self.inigen.emit_global(path, enabled)

    self.mintime = self.entry_mintime.get()
    self.maxtime = self.entry_maxtime.get()

    self.cbox_alg.configure(state='disabled')
    self.entry_filename.configure(state='disabled')
    self.entry_mintime.configure(state='disabled')
    self.entry_maxtime.configure(state='disabled')
    self.check_enabled.configure(state='disabled')
    self.button_emit_globals.configure(state='disabled')

    self.initUIRuns()
    self.update_text(lines)

  def emit_run(self):
    label = self.entry_run_name.get()
    chunking = 'parallel' #hardcoded for now
    mintime = self.mintime
    maxtime = self.maxtime
    lines = self.inigen.emit_run_header(label, chunking, mintime, maxtime)
    self.update_text(lines)

    deps = []
    for i in range(len(self.entries_dep_description)):
      deps.append([self.entries_dep_description[i].get(),
                   self.algorithm['deps'][i],
                   self.entries_dep_uuid[i].get()])
    params = []
    for i in range(len(self.entries_param)):
      params.append([self.algorithm['params'][i],
                     self.entries_param[i].get()])
    outputs = self.algorithm['outputs']
    lines = self.inigen.emit_run_body(deps, params, outputs)
    self.update_text(lines)

  def generate_file(self):
    self.inigen.generate_file(self.entry_filename.get())
    self.quit()

  def update_text(self, lines):
    self.text_file.configure(state='normal')
    string = "\n".join(lines)
    self.text_file.insert(END, string)
    self.text_file.configure(state='disabled')



def main():
  root = Tk()
  app = IniGenGui(root)
  root.mainloop()

if __name__ == '__main__':
  main()

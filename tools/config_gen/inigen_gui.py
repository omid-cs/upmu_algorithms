from algorithm_fields import algorithms
from inigen import IniGen
import re
from uuid import UUID

from Tkinter import Tk, E, W, N, S, Text, END, Scrollbar, RIGHT, LEFT, BOTH, Y
from ttk import Frame, Button, Label, Style, Combobox
from ttk import Entry

class IniGenGui(Frame):

  def __init__(self, parent):
    Frame.__init__(self, parent)
    self.parent = parent
    self.initUI()

    self.run = 1

  def initUI(self):
    self.parent.title("Ini Generator")

    Style().configure("TButton", padding=(0, 5, 0, 5), font='serif 10')

    self.columnconfigure(0, pad=3)
    self.columnconfigure(1, pad=3)
    self.columnconfigure(2, pad=3)

    self.rowconfigure(0, pad=3)
    self.rowconfigure(1, pad=3)
    self.rowconfigure(2, pad=3)
    self.rowconfigure(3, pad=3)
    self.rowconfigure(4, pad=3)
    self.rowconfigure(5, pad=3)
    self.rowconfigure(6, pad=3)
    self.rowconfigure(7, pad=3)
    self.rowconfigure(8, pad=3)
    self.rowconfigure(9, pad=3)
    self.rowconfigure(10, pad=3)

    label_globals = Label(self, text="Globals")
    label_globals.grid(row=0, column=0)

    label_alg = Label(self, text="Algorithm")
    label_alg.grid(row=1, column=0, sticky=E+W)
    cbox_alg = Combobox(self, values=algorithms.keys(), state='readonly')
    cbox_alg.current(0)
    cbox_alg.grid(row=2, column=0, sticky=E+W+S+N)

    label_mintime = Label(self, text="Min Time")
    label_mintime.grid(row=3, column=0, sticky=E+W)
    entry_mintime = Entry(self)
    entry_mintime.grid(row=4, column=0, sticky=W+E)

    label_maxtime = Label(self, text="Max Time")
    label_maxtime.grid(row=5, column=0, sticky=W+E)
    entry_maxtime = Entry(self)
    entry_maxtime.grid(row=6, column=0, sticky=W+E)

    button_addrun = Button(self, text="Add Run", command=self.emit_run)
    button_addrun.grid(row=7, column=0, sticky=W+E)

    button_generate = Button(self, text="Generate File")
    button_generate.grid(row=8, column=0, sticky=W+E)

    label_runs = Label(self, text="Runs")
    label_runs.grid(row=0, column=1)

    label_name = Label(self, text="Run Label")
    label_name.grid(row=1, column=1, sticky=W+E)
    entry_name = Entry(self)
    entry_name.grid(row=2, column=1, sticky=W+E)

    label_desc = Label(self, text="Description")
    label_desc.grid(row=3, column=1, sticky=W+E)
    entry_desc = Entry(self)
    entry_desc.grid(row=4, column=1, sticky=W+E)

    label_uuid = Label(self, text="UUID")
    label_uuid.grid(row=5, column=1, sticky=W+E)
    entry_uuid = Entry(self)
    entry_uuid.grid(row=6, column=1, sticky=W+E)

    label_section = Label(self, text="Section")
    label_section.grid(row=7, column=1, sticky=W+E)
    entry_section = Entry(self)
    entry_section.grid(row=8, column=1, sticky=W+E)

    label_name = Label(self, text="Name")
    label_name.grid(row=9, column=1, sticky=W+E)
    entry_name = Entry(self)
    entry_name.grid(row=10, column=1, sticky=W+E)

    self.text_file = Text(self)
    self.text_file.grid(column=3, row=0, rowspan=11, sticky=W+E+N+S, padx=5, pady=5)
    self.text_file.configure(state='disabled')

    self.pack()

  def emit_run(self):
    self.text_file.configure(state='normal')
    self.text_file.insert(END, "Run {0}\n".format(str(self.run)))
    self.text_file.configure(state='disabled')
    self.run += 1

def main():
  root = Tk()
  app = IniGenGui(root)
  root.mainloop()

if __name__ == '__main__':
  main()

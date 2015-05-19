from algorithm_fields import algorithms, locations
from inigen import IniGen
import re
from uuid import UUID

from Tkinter import Tk, E, W, N, S, Text, END, Scrollbar, RIGHT, LEFT, BOTH, Y, Checkbutton, IntVar, Radiobutton, StringVar, Listbox, Frame, DISABLED, NORMAL
from ttk import Frame, Button, Label, Style, Combobox, Entry
import tkMessageBox

class IniGenGui(Frame):

  def __init__(self, parent):
    Frame.__init__(self, parent)
    self.parent = parent
    self.inigen = IniGen()
    self.initUIGlobals()

  def initUIGlobals(self):
   
    self.parent.title("Ini Generator")

    Style().configure("TButton", padding=(0, 0, 0, 0), font='serif 10')

    # initialize row counter. This is incremented after each element added to grid
    row = 0

    f11 = Frame(self)
    f11.grid(row=0, column=0, sticky=N+E+W)

    f12 = Frame(self)
    f12.grid(row=1, column=0, sticky=S+E+W)

    label_algs = Label(f11, text="Algorithms to Run")
    label_algs.grid(row=row, column=0)
    row += 1

    self.check_algs_value_list = []
    self.check_algs_map = {}
    for alg in algorithms:
      check_alg_value = IntVar()
      check_alg = Checkbutton(f11, text=alg, variable=check_alg_value)
      check_alg.grid(row=row, column=0, sticky=W+E)
      self.check_algs_value_list.append(check_alg_value)
      self.check_algs_map[alg] = check_alg_value
      row += 1

    f111 = Frame(f11)
    f111.grid(row=row, column=0)

    button_checkall = Button(f111, text="All", command=self.checkall)
    button_checkall.grid(row=0, column=0, sticky=W+E)
    button_uncheckall = Button(f111, text="None", command=self.uncheckall)
    button_uncheckall.grid(row=0, column=1, sticky=W+E)

    row = 0

    label_loc = Label(f12, text="Location of uPMU")
    label_loc.grid(row=row, column=0)
    row += 1

    self.radio_loc_string = StringVar()
    locations.append('Other Location')
    for loc in locations:
      radio_loc = Radiobutton(f12, text=loc, variable=self.radio_loc_string, value=loc, command=self.set_loc)
      radio_loc.grid(row=row, column=0, sticky=W+E)
      row += 1

    self.entry_otherloc = Entry(f12)

    f2 = Frame(self)
    f2.grid(row=0, column=1, rowspan=2)
    row = 0

    label_name = Label(f2, text="Name of uPMU")
    label_name.grid(row=row, column=1, columnspan=2)
    row += 1

    self.entry_namesearch = Entry(f2)
    self.entry_namesearch.grid(row=row, column=1, sticky=E+W)

    button_namesearch = Button(f2, text="Search", command=self.namesearch)
    button_namesearch.grid(row=row, column=2, sticky=W+E)
    row += 1

    self.lstbx_namelist = Listbox(f2)
    self.lstbx_namelist.bind("<Double-Button-1>", self.namelist_select)
    self.lstbx_namelist.grid(row=row, column=1, columnspan=2, sticky=W+E)
    row += 1

    label_nameselected = Label(f2, text="Selected:")
    label_nameselected.grid(row=row, column=1)

    self.entry_nameselected = Entry(f2, state=DISABLED)
    self.entry_nameselected.grid(row=row, column=2, sticky=W+E)
    row += 1

    label_refname = Label(f2, text="Name of Reference uPMU")
    label_refname.grid(row=row, column=1, columnspan=2)
    row += 1

    self.entry_refnamesearch = Entry(f2)
    self.entry_refnamesearch.grid(row=row, column=1, sticky=E+W)

    button_refnamesearch = Button(f2, text="Search", command=self.refnamesearch)
    button_refnamesearch.grid(row=row, column=2, sticky=W+E)
    row += 1

    self.lstbx_refnamelist = Listbox(f2)
    self.lstbx_refnamelist.bind("<Double-Button-1>", self.refnamelist_select)
    self.lstbx_refnamelist.grid(row=row, column=1, columnspan=2, sticky=W+E)
    row += 1

    label_refnameselected = Label(f2, text="Selected:")
    label_refnameselected.grid(row=row, column=1)

    self.entry_refnameselected = Entry(f2, state=DISABLED)
    self.entry_refnameselected.grid(row=row, column=2, sticky=W+E)
    row += 1

    button_gen = Button(self, text="Generate Files", command=self.generate_files)
    button_gen.grid(row=2, column=0, columnspan=2, sticky=W+E)

    self.pack()

  def generate_files(self):
    algs = []
    for alg in self.check_algs_map:
      if self.check_algs_map[alg].get() == 1:
        algs.append(alg)

    if self.radio_loc_string.get() == "Other Location":
      location = self.entry_otherloc.get()
    else:
      location = self.radio_loc_string.get()

    name = self.entry_nameselected.get()
    refname = self.entry_refnameselected.get()

    print "algs: "+str(algs)
    print "location: "+location
    print "name: "+name
    print "ref name: "+refname

  def namesearch(self):
    searchterm = self.entry_namesearch.get()
    if "A6" in searchterm:
      self.lstbx_namelist.delete(0, END)
      self.lstbx_namelist.insert(0, 'A6_BUS1', 'A6_BUS2')
    else:
      tkMessageBox.showwarning('Search Error', 'No matches from search for \'{0}\''.format(searchterm))

  def refnamesearch(self):
    searchterm = self.entry_refnamesearch.get()
    if "GP" in searchterm:
      self.lstbx_refnamelist.delete(0, END)
      self.lstbx_refnamelist.insert(0, 'GP_BUS1', 'GP_BUS2')
    else:
      tkMessageBox.showwarning('Search Error', 'No matches from search for \'{0}\''.format(searchterm))

  def set_loc(self):
    if self.radio_loc_string.get() == "Other Location":
      self.entry_otherloc.grid(sticky=W+E)
    else:
      self.entry_otherloc.grid_forget()

  def checkall(self):
    for check in self.check_algs_value_list:
      check.set(1)
  
  def uncheckall(self):
    for check in self.check_algs_value_list:
      check.set(0)

  def namelist_select(self, event):
    selected_index = self.lstbx_namelist.curselection()
    selected = self.lstbx_namelist.get(selected_index)
    self.entry_nameselected.configure(state=NORMAL)
    self.entry_nameselected.delete(0, END)
    self.entry_nameselected.insert(0, selected)
    self.entry_nameselected.configure(state=DISABLED)

  def refnamelist_select(self, event):
    selected_index = self.lstbx_refnamelist.curselection()
    selected = self.lstbx_refnamelist.get(selected_index)
    self.entry_refnameselected.configure(state=NORMAL)
    self.entry_refnameselected.delete(0, END)
    self.entry_refnameselected.insert(0, selected)
    self.entry_refnameselected.configure(state=DISABLED)

def main():
  root = Tk()
  app = IniGenGui(root)
  root.mainloop()

if __name__ == '__main__':
  main()

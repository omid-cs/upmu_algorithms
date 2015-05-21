from inigen_auto import IniGenAutomation
from algorithm_fields import algorithms, locations
import re
from uuid import UUID

from Tkinter import Tk, E, W, N, S, Text, END, Scrollbar, RIGHT, LEFT, BOTH, Y, Checkbutton, IntVar, Radiobutton, StringVar, Listbox, Frame, DISABLED, NORMAL, LabelFrame
from ttk import Frame, Button, Label, Style, Combobox, Entry
import tkMessageBox

class IniGenGui(Frame):

  def __init__(self, parent):
    Frame.__init__(self, parent)
    self.parent = parent
    self.initUIGlobals()

  def initUIGlobals(self):
   
    self.parent.title("Ini Generator")

    Style().configure("TButton", padding=(0, 0, 0, 0), font='serif 10')

    f1 = Frame(self)
    f1.grid(row=0, column=0, padx=10, sticky=N+S+E+W)

    f11 = LabelFrame(f1, text="Algorithms to Run")
    f11.grid(row=0, column=0)
    row = 0

    self.check_algs_value_list = []
    self.check_algs_map = {}
    for alg in algorithms:
      check_alg_value = IntVar()
      check_alg = Checkbutton(f11, text=alg, variable=check_alg_value, justify=LEFT, width=25)
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

    f12 = Frame(f1)
    f12.grid(row=1, column=0, pady=20, sticky=S+W+E)

    f121 = LabelFrame(f12, text='Location of uPMU')
    f121.grid(row=0, column=0)

    self.radio_loc_string = StringVar()
    locations.append('Other Location')
    for loc in locations:
      radio_loc = Radiobutton(f121, text=loc, variable=self.radio_loc_string, value=loc, command=self.set_loc, justify=LEFT, width=25)
      radio_loc.grid(row=row, column=0, sticky=W+E)
      row += 1

    self.entry_otherloc = Entry(f121)

    f2 = Frame(self)
    f2.grid(row=0, column=1, padx=10, sticky=N+S+E+W)

    f21 = LabelFrame(f2, text='Name of uPMU (raw)')
    f21.grid(row=0)
    row = 0

    f211 = Frame(f21)
    f211.grid(row=row)
    row += 1

    self.entry_namesearch = Entry(f211)
    self.entry_namesearch.grid(row=0, column=0, sticky=E+W)

    button_namesearch = Button(f211, text="Search", command=self.namesearch)
    button_namesearch.grid(row=0, column=1, sticky=W+E)

    self.lstbx_namelist = Listbox(f21)
    self.lstbx_namelist.bind("<Double-Button-1>", self.namelist_select)
    self.lstbx_namelist.grid(row=row, sticky=W+E)
    row += 1

    f212 = Frame(f21)
    f212.grid(row=row)
    row += 1

    label_nameselected = Label(f212, text="Selected:")
    label_nameselected.grid(row=0, column=0)

    self.entry_nameselected = Entry(f212, state=DISABLED)
    self.entry_nameselected.grid(row=0, column=1, sticky=W+E)

    f22 = LabelFrame(f2, text="Name of uPMU (path)")
    f22.grid(row=1, sticky=W+E, pady=10)
    self.entry_name = Entry(f22, width=30)
    self.entry_name.grid(row=0, column=0, sticky=E+W)

    f23 = LabelFrame(f2, text="Name of Reference uPMU (path)")
    f23.grid(row=2, pady=10)
    row = 0

    f231 = Frame(f23)
    f231.grid(row=row)
    row += 1

    self.entry_refnamesearch = Entry(f231)
    self.entry_refnamesearch.grid(row=0, column=0, sticky=E+W)

    button_refnamesearch = Button(f231, text="Search", command=self.refnamesearch)
    button_refnamesearch.grid(row=0, column=1, sticky=W+E)

    self.lstbx_refnamelist = Listbox(f23)
    self.lstbx_refnamelist.bind("<Double-Button-1>", self.refnamelist_select)
    self.lstbx_refnamelist.grid(row=row, sticky=W+E)
    row += 1

    f232 = Frame(f23)
    f232.grid(row=row)
    row += 1

    label_refnameselected = Label(f232, text="Selected:")
    label_refnameselected.grid(row=0, column=0)

    self.entry_refnameselected = Entry(f232, state=DISABLED)
    self.entry_refnameselected.grid(row=0, column=1, sticky=W+E)

    button_gen = Button(self, text="Generate Files", command=self.generate_files)
    button_gen.grid(row=1, column=0, columnspan=2, sticky=W+E)

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

    name_raw = self.entry_nameselected.get()
    name = self.entry_name.get()
    ref_name = self.entry_refnameselected.get()

    uuid_map = self.get_uuid_map(name)
    reference_uuid_map = self.get_uuid_map(ref_name)

    print "algs: "+str(algs)
    print "location: "+location
    print "name: "+name
    print "ref name: "+ref_name

    IniGenAutomation(location, name_raw, name, uuid_map, ref_name, reference_uuid_map, algs)

    print "Automation Complete!"

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

  def get_uuid_map(self, path):
    uuid_map = {}
    uuid_map['C1ANG'] = '0'
    uuid_map['C2ANG'] = '1'
    uuid_map['C3ANG'] = '2'
    uuid_map['L1ANG'] = '3'
    uuid_map['L2ANG'] = '4'
    uuid_map['L3ANG'] = '5'
    uuid_map['C1MAG'] = '6'
    uuid_map['C2MAG'] = '7'
    uuid_map['C3MAG'] = '8'
    uuid_map['L1MAG'] = '9'
    uuid_map['L2MAG'] = 'a'
    uuid_map['L3MAG'] = 'b'
    uuid_map['LSTATE'] = 'c'
    for key in uuid_map:
      uuid_map[key] += '_path'
    return uuid_map

def main():
  root = Tk()
  app = IniGenGui(root)
  root.mainloop()

if __name__ == '__main__':
  main()

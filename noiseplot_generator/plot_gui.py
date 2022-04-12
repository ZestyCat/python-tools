import functions as fn
import noiseline as nl
from interpolate import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd

class InputFrame(ttk.Frame): # Make frame containing all input parameters
    def __init__(self, master):
        super().__init__(master) # Initialize parent class
        self.sv_nm = tk.StringVar() # Create backend variables
        self.ac = tk.StringVar()
        self.pwr = tk.StringVar()
        self.pwr_2 = tk.StringVar()
        self.units = tk.StringVar()

        self.sv_nm.set("./noise_plot.png") # Set variable defaults
        self.ac.set("Select AC")
        self.pwr.set(None)
        self.pwr_2.set(None)
        self.units.set("      ")

        self.sv_frame = ttk.Frame() # Make frames
        self.ac_frame = ttk.Frame()
        self.pwr_frame = ttk.Frame()
        
        self.sv_ent = tk.Entry(self.sv_frame) # Make widgets in frames
        self.sv_btn = tk.Button(self.sv_frame, command = self.set_sv_nm, \
                                text = "Save as", width = 4, height = 0)
        self.pwr_lab = tk.Label(self.pwr_frame, text = "Power setting:")
        self.pwr_ent = tk.Entry(self.pwr_frame)
        self.pwr_unit = tk.Label(self.pwr_frame, text = "      ")
        self.pwr_lab_2 = tk.Label(self.pwr_frame, text = "Power setting 2:")
        self.pwr_ent_2 = tk.Entry(self.pwr_frame)
        self.pwr_unit_2 = tk.Label(self.pwr_frame, text = "      ")
        self.ac_lab = tk.Label(self.ac_frame, text = "Aircraft:")
        self.ac_drp = tk.OptionMenu(self.ac_frame, self.ac, *fn.list_aircraft(),
                                    command = self.set_units)
        self.plt_btn = tk.Button(command = self.make_plot, text = "Plot", \
                                 width = 4, height = 0)

        self.sv_ent["textvariable"] = self.sv_nm # Link widgets to variables
        self.pwr_ent["textvariable"] = self.pwr
        self.pwr_ent_2["textvariable"] = self.pwr_2
        self.pwr_unit["textvariable"] = self.units
        self.pwr_unit_2["textvariable"] = self.units

        self.sv_ent.grid(row = 0, column = 0, columnspan = 2) # Manage geometry
        self.sv_btn.grid(row = 0, column = 2)
        self.sv_frame.grid(row = 0, column = 0)
        self.pwr_lab.grid(row = 0, column = 0)
        self.pwr_ent.grid(row = 0, column = 1)
        self.pwr_unit.grid(row = 0, column = 2)
        self.pwr_lab_2.grid(row = 1, column = 0)
        self.pwr_ent_2.grid(row = 1, column = 1)
        self.pwr_unit_2.grid(row = 1, column = 2)
        self.pwr_frame.grid(row = 2, column = 0)
        self.ac_drp.grid(row = 0, column = 1)
        self.ac_lab.grid(row = 0, column = 0)
        self.ac_frame.grid(row = 1, column = 0)
        self.plt_btn.grid()

    def make_plot(self): # make a dataframe, call plotting function 
        self.df = interpolate(ac = self.ac.get(), pwr = float(self.pwr.get()),
                              units = self.units.get())
        self.df_2 = None if self.pwr_2.get().isnumeric() == False else \
                interpolate(pwr = float(self.pwr_2.get()))
        self.fig = nl.plot(self.df, save_name = self.sv_nm.get()) \
            if self.df_2 is None else \
            nl.plot(self.df, self.df_2, save_name = self.sv_nm.get())
        return(self.fig)
    def set_sv_nm(self): # Open save dialog, set sv_nm/s_ent to selected name
        nm = fd.asksaveasfilename()
        self.sv_nm.set(nm)
    def set_units(self, selected): # Get units of selected aircraft
        self.units.set(fn.get_units(selected))

class Text(tk.Entry): # make TextInput class inherit from tk.Entry
    def __init__(self, master, value): 
        super().__init__(master) # Access methods of super class (ttk.Frame)
        self.var = tk.StringVar() # make a string variable
        self.var.set(value) # set var to value
        self["textvariable"] = self.var # link entry to variable
        self.bind("<Key-Return>", self.print_contents)
    def print_contents(self, event): # callback to test variable
        print("Current content is:", self.var.get())
        print(interpolate())

class Save(ttk.Frame):
    def __init__(self, master, placeholder):
        super().__init__(master)
        self.entry = tk.Entry()
        self.entry.pack()
        self.text = tk.StringVar()
        self.entry["textvariable"] = self.text
        self.text.set(placeholder)
        self.btn = tk.Button(command = self.get_file, text = "Save as", width = 5, height = 1)
        self.btn.pack()
    def get_file(self):
        file = fd.asksaveasfilename()
        self.text.set(file)

class Selection(ttk.Frame):
    def __init__(self, master, placeholder):
        super().__init__(master)
        self.var = tk.StringVar()
        self.var.set(placeholder)
        self.drop = tk.OptionMenu(master, self.var, *fn.list_aircraft()).pack()
        self.lab = tk.Label(master, text = "Select an aircraft").pack()
class App(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.save = Save(self, "Save file name")
        self.power = Text(self, "Power setting").pack()
        self.aircraft = Selection(self, "Aircraft")
        self.plot_btn = tk.Button(self, text = "Make a plot", command = self.plot).pack() 
        self.pack()
    def plot(self):
        ac = self.aircraft.var.get()
        print(ac)
root = tk.Tk()
a = InputFrame(root)
a.mainloop()

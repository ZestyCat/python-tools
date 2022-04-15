import functions as fn
import noiseline as nl
from interpolate import *
import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
from tkinter import filedialog as fd
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)

class InputFrame(ttk.Frame): # Make frame containing all input parameters
    def __init__(self, master):
        super().__init__(master) # Initialize parent class
        self.sv_nm = tk.StringVar() # Create backend variables
        self.ac    = tk.StringVar()
        self.pwr   = tk.StringVar()
        self.pwr_2 = tk.StringVar()
        self.desc  = tk.StringVar()
        self.units = tk.StringVar()
        self.eng   = tk.StringVar()

        self.sv_nm.set("./noise_plot.png") # Set variable defaults
        self.ac.set("Select AC")
        self.pwr.set("")
        self.pwr_2.set("")
        self.desc.set("")
        self.units.set("Units")

        self.input_frame = ttk.Frame() # Make frames
        self.fig_frame   = ttk.Frame()

        self.sv_lab     = tk.Label(self.input_frame, text = "Filename:") # Make widgets
        self.sv_ent     = tk.Entry(self.input_frame, width = 14)
        self.sv_btn     = tk.Button(self.input_frame, command = self.set_sv_nm,
                                    text = "Browse", width = 4, height = 0)
        self.pwr_lab    = tk.Label(self.input_frame, text = "Power setting 1:")
        self.pwr_ent    = tk.Entry(self.input_frame, width = 10)
        self.pwr_unit   = tk.Label(self.input_frame, text = "Power units")
        self.pwr_lab_2  = tk.Label(self.input_frame, text = "Power setting 2:")
        self.pwr_ent_2  = tk.Entry(self.input_frame, width = 10)
        self.pwr_unit_2 = tk.Label(self.input_frame, text = "Power units")
        self.desc_lab   = tk.Label(self.input_frame, text = "Power description:")
        self.desc_ent   = tk.Entry(self.input_frame, width = 10)
        self.ac_lab     = tk.Label(self.input_frame, text = "Select aircraft:")
        self.ac_drp     = ttk.OptionMenu(self.input_frame, self.ac, *["Select AC"],
                                         *fn.list_aircraft(), command = self.set_info)
        self.plt_btn    = tk.Button(self.input_frame, command = self.show_plot, 
                                    text = "Plot", width = 4, height = 0)

        self.sv_ent["textvariable"]     = self.sv_nm # Link widgets to variables
        self.pwr_ent["textvariable"]    = self.pwr
        self.pwr_ent_2["textvariable"]  = self.pwr_2
        self.pwr_unit["textvariable"]   = self.units
        self.pwr_unit_2["textvariable"] = self.units
        self.desc_ent["textvariable"]   = self.desc

        self.ac_drp.grid(row      = 0, column = 1, sticky = "WE") # Manage geometry
        self.ac_lab.grid(row      = 0, column = 0, sticky = "E")
        self.pwr_lab.grid(row     = 1, column = 0, sticky = "E")
        self.pwr_ent.grid(row     = 1, column = 1, sticky = "WE")
        self.pwr_unit.grid(row    = 1, column = 2, sticky = "W")
        self.pwr_lab_2.grid(row   = 2, column = 0, sticky = "E")
        self.pwr_ent_2.grid(row   = 2, column = 1, sticky = "WE")
        self.pwr_unit_2.grid(row  = 2, column = 2, sticky = "W")
        self.desc_lab.grid(row    = 3, column = 0, sticky = "E")
        self.desc_ent.grid(row    = 3, column = 1, sticky = "WE")
        self.sv_lab.grid(row      = 4, column = 0, sticky = "E")
        self.sv_ent.grid(row      = 4, column = 1, sticky = "WE")
        self.sv_btn.grid(row      = 4, column = 2,)
        self.plt_btn.grid(row     = 5, column = 1, sticky = "W")
        self.input_frame.grid(row = 0, column = 0) # Frame geometry
        self.fig_frame.grid(row   = 1, column = 0)

    def make_plot(self): # make a dataframe, call plotting function 
        self.df = interpolate(ac = self.ac.get(), pwr = float(self.pwr.get()),
                              units = self.units.get(), eng = self.eng.get())
        self.df_2 = None if self.pwr_2.get().isnumeric() == False else \
                  interpolate(ac = self.ac.get(), pwr = float(self.pwr_2.get()),
                              units = self.units.get(), eng = self.eng.get())
        try: # Try to make a figure from dataframes
            self.fig = nl.plot(self.df, save_name = self.sv_nm.get()) \
                if self.df_2 is None else \
                nl.plot(self.df, self.df_2, save_name = self.sv_nm.get(),
                        ps_name = self.desc.get())
            return(self.fig)
        except: # Show error if dataframes are out of range
            err = self.df if type(self.df) == str else self.df_2
            self.show_error("Out of range", err)
            raise Exception("Could not make a plot out of those power settings. Perhaps they were out of range?") 

    def show_plot(self):
        fig = self.make_plot()
        self.canvas = FigureCanvasTkAgg(fig, master = self.fig_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row = 1, column = 0)
    
    def set_sv_nm(self): # Open save dialog, set sv_nm/s_ent to selected name
        nm = fd.asksaveasfilename()
        self.sv_nm.set(nm)
    
    def set_info(self, selected): # Get units and engine of selected aircraft
        self.units.set(fn.get_info(selected)["units"])
        self.eng.set(fn.get_info(selected)["engine"])
    
    def show_error(self, header, message):
        tkinter.messagebox.showinfo(header, message)

root = tk.Tk()
a = InputFrame(root)
a.mainloop()

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

        self.pwr_lab    = tk.Label(self.input_frame, text = "Power setting 1:") # Make widgets
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
                                    text = "Preview plot", height = 0)
        self.csv_btn    = tk.Button(self.input_frame, command = self.save_data,
                                    text = "Save CSV data")
        self.sv_btn     = tk.Button(self.input_frame, command = self.save_plot,
                                    text = "Save plot", height = 0)
        self.help_btn   = tk.Button(self.input_frame, command = self.show_help,
                                    text = "Show help", height = 0)

        self.pwr_ent["textvariable"]    = self.pwr # Link widgets to variables
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
        self.plt_btn.grid(row     = 4, column = 0, sticky = "WE")
        self.sv_btn.grid(row      = 4, column = 1, sticky = "WE")
        self.csv_btn.grid(row     = 5, column = 0, sticky = "WE")
        self.help_btn.grid(row    = 5, column = 1, sticky = "WE")
        self.input_frame.grid(row = 0, column = 0) # Geometry of frames
        self.fig_frame.grid(row   = 1, column = 0)

    def make_plot(self, save_name = None): # make a dataframe, call plotting function 
        self.df = interpolate(ac = self.ac.get(), pwr = float(self.pwr.get()),
                              units = self.units.get(), eng = self.eng.get())
        self.df_2 = None if self.pwr_2.get().isnumeric() == False else \
                  interpolate(ac = self.ac.get(), pwr = float(self.pwr_2.get()),
                              units = self.units.get(), eng = self.eng.get())
        try: # Try to make a figure from dataframes
            self.fig = nl.plot(self.df, ps_name = self.desc.get(), 
                                save_name = save_name) \
                if self.df_2 is None else \
                nl.plot(self.df, self.df_2, ps_name = self.desc.get(), 
                                save_name = save_name)
            return(self.fig)
        except: # Show error if power settings are out of range
            err = self.df if type(self.df) == str else self.df_2
            self.show_message("Out of range", err)
            raise Exception("Could not make a plot out of those power settings. Perhaps they were out of range?") 

    def show_plot(self): # Preview the plot on canvas
        fig = self.make_plot(save_name = None)
        self.canvas = FigureCanvasTkAgg(fig, master = self.fig_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row = 1, column = 0)

    def save_plot(self): # Save plot
            self.fig = self.make_plot(save_name = fd.asksaveasfilename())
 
    def save_data(self): # make a dataframe, save as csv 
        self.df = interpolate(ac = self.ac.get(), pwr = float(self.pwr.get()),
                              units = self.units.get(), eng = self.eng.get(),
                              desc = self.desc.get())
        self.df_2 = None if self.pwr_2.get().isnumeric() == False else \
                  interpolate(ac = self.ac.get(), pwr = float(self.pwr_2.get()),
                              units = self.units.get(), eng = self.eng.get(),
                              desc = self.desc.get())
        if type(self.df) != str and type(self.df_2) == str: # Try to save dataframes
            self.df.to_csv(fd.asksaveasfilename())
        elif type(self.df) != str and type(self.df_2) != str:
             file = fd.asksaveasfilename()
             self.df.to_csv(file, mode = 'w', index = False)
             self.df_2.to_csv(file, mode = 'a', index = False, header = False)
        else: 
            err = self.df if type(self.df) == str else self.df_2 # Show message if error
            self.show_message("Out of range", err)
            raise Exception("Could not make a plot out of those power settings. Perhaps they were out of range?")    
    
    def set_info(self, selected): # Get units and engine of selected aircraft
        self.units.set(fn.get_info(selected)["units"])
        self.eng.set(fn.get_info(selected)["engine"])
    
    def show_message(self, header, message):
        tkinter.messagebox.showinfo(header, message)

    def show_help(self):
        msg = \
        '''
Instructions:\n
1.    Select aircraft from the drop-down.\n
2.    Enter power setting values.
          - To plot a single power setting,
            leave "Power setting 2" blank.
          - To plot a range between two power
            settings, enter a value for
            "Power setting 2".\n
4.    Enter the name of the power setting in
       the "Power description" field.\n
5.    Show the plot in the window using
       the "Preview plot" button.\n
6.    Save the plot to a specified file using
       the "Save plot" button.\n
7.    Save the raw data file in csv format
       to a specified location using the 
       "Save CSV data" button.

        '''
        self.show_message("Help", msg)

root = tk.Tk()
a = InputFrame(root)
a.mainloop()

import functions as fn
import pandas as pd
import noiseline as nl
from interpolate import *
import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
from tkinter import filedialog as fd
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
import os
import sys

def main():
    class App(ttk.Frame): # Make frame containing all input parameters
        def __init__(self, master):
            super().__init__(master) # Initialize parent class
            self.sv_nm = tk.StringVar() # Create backend variables
            self.ac    = tk.StringVar()
            self.pwr   = tk.StringVar()
            self.pwr_2 = tk.StringVar()
            self.desc  = tk.StringVar()
            self.units = tk.StringVar()
            self.eng   = tk.StringVar()

            self.help_img = tk.PhotoImage(file = "./img/help.png") # Load images
            self.play_img = tk.PhotoImage(file = "./img/go.png") 
            self.file_img = tk.PhotoImage(file = "./img/file.png")
            self.tabs_img = tk.PhotoImage(file = "./img/tabs.png")
            self.drop_img = tk.PhotoImage(file = "./img/drop.png")
            self.del_img  = tk.PhotoImage(file = "./img/del.png")
            self.logo     = tk.PhotoImage(file = "./img/aeso_padded.png")

            self.sv_nm.set("./noise_plot.png") # Set variable defaults
            self.ac.set("Select AC")
            self.pwr.set("")
            self.pwr_2.set("")
            self.desc.set("")
            self.units.set("Units")
            self.eng.set("")
    
            self.input_frame  = tk.Frame(highlightbackground = "black", highlightthickness = 1) # Make frames
            self.fig_frame    = tk.Frame(highlightbackground = "black", highlightthickness = 1, bg = "darkgrey")

            self.aeso_logo  = tk.Label(self.input_frame, image = self.logo)
            self.pwr_lab    = tk.Label(self.input_frame, text = "Power setting 1:") # Make widgets
            self.pwr_ent    = tk.Entry(self.input_frame, width = 10)
            self.pwr_unit   = tk.Label(self.input_frame, text = "Power units", width = 7, anchor = "w")
            self.pwr_lab_2  = tk.Label(self.input_frame, text = "Power setting 2:")
            self.pwr_ent_2  = tk.Entry(self.input_frame, width = 10)
            self.pwr_unit_2 = tk.Label(self.input_frame, text = "Power units", width = 7, anchor = "w")
            self.desc_lab   = tk.Label(self.input_frame, text = "Power description:")
            self.desc_ent   = tk.Entry(self.input_frame, width = 10)
            self.ac_lab     = tk.Label(self.input_frame, text = "Select aircraft:")
            self.ac_drp     = tk.OptionMenu(self.input_frame, self.ac, *["Select AC"],
                                             *fn.list_aircraft(), command = self.set_info)
            self.plt_btn    = tk.Button(self.input_frame, command = self.show_plot, 
                                        text = "Preview plot", image = self.play_img,
                                        compound = "right", height = 0)
            self.del_btn    = tk.Button(self.input_frame, command = self.remove_plot,
                                        text = "Delete plot", image = self.del_img,
                                        compound = "right", height = 0)
            self.csv_btn    = tk.Button(self.input_frame, command = self.save_data,
                                        text = "Write to CSV", image = self.tabs_img,
                                        compound = "right", height = 0)
            self.sv_btn     = tk.Button(self.input_frame, command = self.save_plot,
                                        text = "Save plot", image = self.file_img,
                                        compound = "right", height = 0)
            self.help_btn   = tk.Button(self.input_frame, command = self.show_help,
                                        text = "Show help", image = self.help_img, 
                                        compound = "right", height = 0)

            self.pwr_ent["textvariable"]    = self.pwr # Link widgets to variables
            self.pwr_ent_2["textvariable"]  = self.pwr_2
            self.pwr_unit["textvariable"]   = self.units
            self.pwr_unit_2["textvariable"] = self.units
            self.desc_ent["textvariable"]   = self.desc

            self.ac_drp.grid(row      = 0, column = 1, sticky = "WE") # Manage geometry
            self.ac_lab.grid(row      = 0, column = 0, sticky = "E")
            self.aeso_logo.grid(row   = 0, column = 4, rowspan = 4, sticky = "SW")
            self.pwr_lab.grid(row     = 1, column = 0, sticky = "E")
            self.pwr_ent.grid(row     = 1, column = 1, sticky = "WE")
            self.pwr_unit.grid(row    = 1, column = 2, sticky = "W")
            self.pwr_lab_2.grid(row   = 2, column = 0, sticky = "E")
            self.pwr_ent_2.grid(row   = 2, column = 1, sticky = "WE")
            self.pwr_unit_2.grid(row  = 2, column = 2, sticky = "W")
            self.desc_lab.grid(row    = 3, column = 0, sticky = "E")
            self.desc_ent.grid(row    = 3, column = 1, sticky = "WE")
            self.plt_btn.grid(row     = 4, column = 0, rowspan = 2, sticky = "WE")
            self.sv_btn.grid(row      = 4, column = 1, rowspan = 2, sticky = "WE")
            self.del_btn.grid(row     = 4, column = 2, rowspan = 2, sticky = "WE")
            self.csv_btn.grid(row     = 4, column = 3, rowspan = 2, sticky = "WE")
            self.help_btn.grid(row    = 4, column = 4, rowspan = 2, sticky = "WE")
            self.input_frame.grid(row = 0, column = 0, sticky = "WE") # Geometry of frames
            self.fig_frame.grid(row   = 1, column = 0)

            self.ac_drp.config(indicatoron = False, image = self.drop_img, compound = "right")

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
            self.fig = self.make_plot(save_name = None)
            self.canvas = FigureCanvasTkAgg(self.fig, master = self.fig_frame)
            self.canvas.draw()
            self.canvas.get_tk_widget().grid(row = 1, column = 0)
            self.master.geometry("")

        def save_plot(self): # Save plot
                self.fig = self.make_plot(save_name = fd.asksaveasfilename(defaultextension = ".png", 
                                                                filetypes =[("image files", ".png")]))
     
        def remove_plot(self):
            self.fig_frame.destroy()
            self.fig_frame = tk.Frame(highlightbackground = "black", highlightthickness = 1, bg = "darkgrey")
            self.fig_frame.grid(row = 1, column = 0)

        def save_data(self): # make a dataframe, save as csv 
            self.df   = None if self.pwr.get().isnumeric() == False else \
                        interpolate(ac = self.ac.get(), pwr = float(self.pwr.get()),
                                    units = self.units.get(), eng = self.eng.get(),
                                    desc = self.desc.get())
            self.df_2 = None if self.pwr_2.get().isnumeric() == False else \
                        interpolate(ac = self.ac.get(), pwr = float(self.pwr_2.get()),
                                    units = self.units.get(), eng = self.eng.get(),
                                    desc = self.desc.get())
            if type(self.df) != str or type(self.df_2) != str: # If numeric entry for ps 1 or ps 2
                self.file = fd.asksaveasfilename(defaultextension = ".csv", 
                                            filetypes = [("comma separated value", ".csv")])
                self.cols = pd.DataFrame(columns = ["ac", "eng", "pwr", "desc", "unit", "spd", 
                                                    "dist", "lmax", "sel"])
                self.cols.to_csv(self.file, index = False) # Write headers to csv file
                try: # Append df 1 data
                    self.df.to_csv(self.file, mode = 'a', index = False, header = False)
                except:
                    print("Invalid entry or blank power setting 1.")
                try: # Append df 2 data
                    self.df_2.to_csv(self.file, mode = 'a', index = False, header = False)
                except:
                    print("Invalid entry or blank power setting 2.")
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
2.    Enter power setting values.\n
2a.   To plot a single power setting, leave "Power setting 2" blank.\n
2b.   To plot a range between two power settings, enter a value for "Power setting 2".\n
4.    Enter the name of the power setting in the "Power description" field.\n
5.    Show the plot in the window using the "Preview plot" button.\n
6.    Save the plot to a specified file using the "Save plot" button.\n
7.    Save the raw data file in csv format to a specified location using the "Write to CSV" button.

            '''
            self.show_message("Help", msg)

    root = tk.Tk()
    root.configure(bg = "darkgrey")
    root.title("AESO Noiseplot")
    root.option_add('*Dialog.msg.font', 'Helvetica 12')
    a = App(root)
    a.input_frame.grid(sticky = "WE")
    a.mainloop()

if __name__ == '__main__': # Try to work from the pyinstaller tempfile directory
    if hasattr(sys, '_MEIPASS'):
        saved_dir = os.getcwd()
        os.chdir(sys._MEIPASS)
        try:
            main()
        finally:
            os.chdir(saved_dir) # If it fails, just use the current directory
    else:
        main()



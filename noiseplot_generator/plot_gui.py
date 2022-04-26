import pandas as pd
import noiseline as nl
import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
from tkinter import filedialog as fd
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
import os
import sys
import subprocess

def main():

    # Get aircraft code, power units, engine for all aircraft except those in ignore file
    def get_aircraft(file = "./data/acdata.csv", ignore = "./data/bad_ac_list.csv"):
        df = pd.read_csv(file)
        df_2 = pd.read_csv(ignore, header = None)
        ignore = "|".join(df_2[0].tolist()) # Make regex for all aircraft to ignore
        return(df[df["aircraft"].str.contains(ignore) == False])

    # Return aircraft info for specified aircraft (engine, power units, code)
    def get_info(df, aircraft = "F-18E/F"):
        return(df[df["aircraft"] == aircraft].iloc[0])

    # Write o10 input file, call subprocess to run o10
    def run_o10(aircraft = "F-18E/F", power = 90, description = "Cruise", 
                    speed_kts = 160, temp = 59, rel_hum_pct = 70,
                    path = "./", input = 'input.o10_input', log = "log.o10_log", 
                    output = "output.o10_noise", ac_file = "./data/acdata.csv", 
                    os = "Windows"):

        # Find the corresponding code for aircraft in codes list file
        ac_data = pd.read_csv(ac_file)
        code  = ac_data[ac_data["aircraft"] == aircraft]["code"].item() # read csv, get code/units of aircraft
        units = ac_data[ac_data["aircraft"] == aircraft]["units"].item()
        
        # Pad params with spaces so they fit the Omega10 input format
        pwr_pad = " " * (10 - len(format(power, '.2f'))) + format(power, '.2f')
        units_pad = units + " " * (10 - len(units))
        speed_pad = " " * (3 - len(str(speed_kts))) + str(speed_kts)
        
        # Concatenate params into string
        command = "\n{}  {}   {} W  1  0.0\nF{}00{} {} VARIABLE   {}\n" \
            .format(code, temp, rel_hum_pct, code, pwr_pad, units_pad, speed_kts)
       
        # Write o10_input file
        with open(path + input, 'w') as file:
            file.write(command)
            file.close()
        
        # Run omega10
        if os == "Windows":
            subprocess.Popen(["omega10", input, log, output]).wait()
            return(output)
        elif os == "Linux":
            subprocess.Popen(["wine", bat]).wait()
            return(output)
        else:
            raise Exception("OS must be set to Windows or Linux")

    # Read o10 output file, return a dataframe
    def read_o10(file = "./output.o10_noise"):
        with open(file) as file:
            lines = file.readlines()
            ac = []
            eng = []
            pwr = []
            unit = []
            spd = []
            dist  = []
            sel   = []
            lmax  = []
            for i, line in enumerate(lines):
                if line.strip() != "": # Remove blank lines
                    l = (" ".join(line.split()).split()) # Remove extra space and split into list
                    if i == 2:
                        ac.append(l[3])
                    elif i == 3:
                        eng.append(l[2])
                    elif i == 11:
                        unit.append(line[42:52].strip())
                        spd.append(line[57:61].strip())
                        pwr.append(l[2])
                    elif i > 14: # Get the data
                        dist.append(float(l[0]))
                        sel.append(float(l[1]))
                        lmax.append(float(l[6]))
            df = pd.DataFrame( \
                 { "ac"   : ac[0],
                   "eng"  : eng[0],
                   "pwr"  : pwr[0],
                   "unit" : unit[0],
                   "spd"  : spd[0],
                   "dist" : dist,
                   "lmax" : lmax,
                   "sel"  : sel})
            
            return(df)

    # Main application window
    class App(ttk.Frame): 
        def __init__(self, master):
            super().__init__(master) # Initialize parent class
            
            # Initialize variables
            self.sv_nm  = tk.StringVar() 
            self.ac     = tk.StringVar()
            self.pwr    = tk.StringVar()
            self.pwr_2  = tk.StringVar()
            self.desc   = tk.StringVar()
            self.units  = tk.StringVar()
            self.eng    = tk.StringVar()
            self.speed  = tk.IntVar()
            self.temp   = tk.IntVar()
            self.rh_pct = tk.IntVar()
            
            # Load images
            self.help_img = tk.PhotoImage(file = "./img/help.png")
            self.play_img = tk.PhotoImage(file = "./img/go.png") 
            self.file_img = tk.PhotoImage(file = "./img/file.png")
            self.tabs_img = tk.PhotoImage(file = "./img/tabs.png")
            self.drop_img = tk.PhotoImage(file = "./img/drop.png")
            self.del_img  = tk.PhotoImage(file = "./img/del.png")
            self.logo     = tk.PhotoImage(file = "./img/aeso_padded.png")

            # Set variable defaults
            self.sv_nm.set("./noise_plot.png") 
            self.ac.set("Select AC")
            self.pwr.set("")
            self.pwr_2.set("")
            self.desc.set("")
            self.units.set("")
            self.eng.set("")
            self.speed.set(160)
            self.temp.set(59)
            self.rh_pct.set(70)
            
            # Make frames
            self.input_frame  = tk.Frame(highlightbackground = "black", highlightthickness = 1)
            self.fig_frame    = tk.Frame(highlightbackground = "black", highlightthickness = 1, bg = "darkgrey")

            # Make widgets
            self.aeso_logo  = tk.Label(self.input_frame, image = self.logo)
            self.speed_lab  = tk.Label(self.input_frame, text = "Aircraft speed (kts.):")
            self.speed_ent  = tk.Entry(self.input_frame, width = 10)
            self.temp_lab   = tk.Label(self.input_frame, text = "Air temperature (F):")
            self.temp_ent   = tk.Entry(self.input_frame, width = 10)
            self.rh_pct_lab = tk.Label(self.input_frame, text = "Relative humidity (%):")
            self.rh_pct_ent = tk.Entry(self.input_frame, width = 10)
            self.pwr_lab    = tk.Label(self.input_frame, text = "Power setting 1:") 
            self.pwr_ent    = tk.Entry(self.input_frame, width = 10)
            self.pwr_unit   = tk.Label(self.input_frame, text = "Power units", width = 7, anchor = "w")
            self.pwr_lab_2  = tk.Label(self.input_frame, text = "Power setting 2:")
            self.pwr_ent_2  = tk.Entry(self.input_frame, width = 10)
            self.pwr_unit_2 = tk.Label(self.input_frame, text = "Power units", width = 7, anchor = "w")
            self.desc_lab   = tk.Label(self.input_frame, text = "Power description:")
            self.desc_ent   = tk.Entry(self.input_frame, width = 10)
            self.ac_lab     = tk.Label(self.input_frame, text = "Select aircraft:")
            self.ac_drp     = ttk.Combobox(self.input_frame, textvariable = self.ac)
            self.ac_drp.bind('<<ComboboxSelected>>', self.set_info)
            self.ac_drp.bind('<KeyRelease>', self.set_info)
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

            # Link widgets to variables
            self.speed_ent['textvariable']   = self.speed
            self.temp_ent['textvariable']    = self.temp
            self.rh_pct_ent['textvariable']  = self.rh_pct
            self.pwr_ent["textvariable"]     = self.pwr 
            self.pwr_ent_2["textvariable"]   = self.pwr_2
            self.pwr_unit["textvariable"]    = self.units
            self.pwr_unit_2["textvariable"]  = self.units
            self.desc_ent["textvariable"]    = self.desc
            self.ac_drp["values"] = get_aircraft()["aircraft"].tolist()

            self.ac_drp.grid(row      = 0, column = 1, sticky = "WE") # Manage geometry
            self.ac_lab.grid(row      = 0, column = 0, sticky = "E")
            self.aeso_logo.grid(row   = 0, column = 6, rowspan = 4, sticky = "SW")
            self.temp_lab.grid(row    = 1, column = 3, sticky = "E")
            self.temp_ent.grid(row    = 1, column = 4, sticky = "W")
            self.pwr_lab.grid(row     = 1, column = 0, sticky = "E")
            self.pwr_ent.grid(row     = 1, column = 1, sticky = "WE")
            self.pwr_unit.grid(row    = 1, column = 2, sticky = "W")
            self.rh_pct_lab.grid(row  = 2, column = 3, sticky = "E")
            self.rh_pct_ent.grid(row  = 2, column = 4, sticky = "W")
            self.pwr_lab_2.grid(row   = 2, column = 0, sticky = "E")
            self.pwr_ent_2.grid(row   = 2, column = 1, sticky = "WE")
            self.pwr_unit_2.grid(row  = 2, column = 2, sticky = "W")
            self.speed_lab.grid(row   = 3, column = 3, sticky = "E")
            self.speed_ent.grid(row   = 3, column = 4, sticky = "W")
            self.desc_lab.grid(row    = 3, column = 0, sticky = "E")
            self.desc_ent.grid(row    = 3, column = 1, sticky = "WE")
            self.plt_btn.grid(row     = 4, column = 0, rowspan = 2, sticky = "WE")
            self.sv_btn.grid(row      = 4, column = 1, rowspan = 2, sticky = "WE")
            self.del_btn.grid(row     = 4, column = 2, rowspan = 2, sticky = "WE")
            self.csv_btn.grid(row     = 4, column = 3, rowspan = 2, sticky = "WE")
            self.help_btn.grid(row    = 4, column = 4, rowspan = 2, sticky = "WE")
            self.input_frame.grid(row = 0, column = 0, sticky = "WE") # Geometry of frames
            self.fig_frame.grid(row   = 1, column = 0)

        def make_plot(self, save_name = None): # make a dataframe, call plotting function 
            
            # Run omega10 and return the output filename
            out   = run_o10(aircraft = self.ac.get(), power = int(self.pwr.get()),
                       speed_kts = self.speed.get(), temp = self.temp.get(),
                       rel_hum_pct = self.rh_pct.get()) \
                       if self.pwr.get().isnumeric() == True \
                       else None
                       
            # Run omega10 and return the output filename
            out_2 = run_o10(aircraft = self.ac.get(), power = int(self.pwr_2.get()),
                       speed_kts = self.speed.get(), temp = self.temp.get(),
                       input = "input_2.o10_input", log = "log_2.o10_log",
                       output = "output_2.o10_output", rel_hum_pct = self.rh_pct.get()) \
                       if self.pwr_2.get().isnumeric() == True \
                       else None
            
            # Show a popup if no entry 
            if out is None and out_2 is None:
                self.m = "Please enter some power setting data."
                self.show_message("Entry needed", self.m)
                return(None)
            
            # Make dataframes from o10 output
            self.df   = None if out is None else read_o10(out)
            self.df_2 = None if out_2 is None else read_o10(out_2)
            
            # Plot 
            self.fig  = nl.plot(self.df, ps_name = self.desc.get(), 
                                save_name = save_name) \
                if self.df_2 is None else \
                nl.plot(self.df, self.df_2, ps_name = self.desc.get(), 
                                save_name = save_name)
            return(self.fig)
                
        def show_plot(self): # Preview the plot on canvas
            self.fig = self.make_plot(save_name = None)
            if self.fig == None: # Do not show plot if there is no data to plot
                return(None)
            else:
                self.canvas = FigureCanvasTkAgg(self.fig, master = self.fig_frame)
                self.canvas.draw()
                self.canvas.get_tk_widget().grid(row = 1, column = 0)
                self.master.geometry("")

        def save_plot(self): # Save plot
                if self.pwr.get().isnumeric() == False and self.pwr_2.get().isnumeric() == False:
                    self.m = "Please enter some power setting data."
                    self.show_message("Entry needed", self.m)
                    return(None)
                else:
                    self.fig = self.make_plot(save_name = fd.asksaveasfilename(defaultextension = ".png", 
                                                                filetypes =[("image files", ".png")]))
     
        def remove_plot(self): # Destroy and remake fig_frame
            self.fig_frame.destroy()
            self.fig_frame = tk.Frame(highlightbackground = "black", highlightthickness = 1, bg = "darkgrey")
            self.fig_frame.grid(row = 1, column = 0)

        def save_data(self): # make a dataframe, save as csv 
            
            # Run omega10 and return the output filename
            out = run_o10(aircraft = self.ac.get(), power = int(self.pwr.get()),
                       speed_kts = self.speed.get(), temp = self.temp.get(),
                       rel_hum_pct = self.rh_pct.get()) \
                       if self.pwr.get().isnumeric() == True \
                       else None
                       
            # Run omega10 and return the output filename  
            out_2 = run_o10(aircraft = self.ac.get(), power = int(self.pwr_2.get()),
                       speed_kts = self.speed.get(), temp = self.temp.get(),
                       input = "input_2.o10_input", log = "log_2.o10_log",
                       output = "output_2.o10_output", rel_hum_pct = self.rh_pct.get()) \
                       if self.pwr_2.get().isnumeric() == True \
                       else None
            
            # Show a popup if no entry 
            if out is None and out_2 is None:
                self.m = "Please enter some power setting data."
                self.show_message("Entry needed", self.m)
                return(None)

            self.df = None if out is None else read_o10(out)
            self.df_2 = None if out_2 is None else read_o10(out_2)
            
            self.file = fd.asksaveasfilename(defaultextension = ".csv", 
                                            filetypes = [("comma separated value", ".csv")])
            self.cols = pd.DataFrame(columns = ["ac", "eng", "pwr", "unit", "spd", 
                                                    "dist", "lmax", "sel", "desc"])
            self.cols.to_csv(self.file, index = False) # Write headers to csv file
            
            if self.df is not None:
                self.df["desc"] = self.desc.get()
                self.df.to_csv(self.file, mode = 'a', index = False, header = False)
            
            if self.df_2 is not None:
                self.df_2["desc"] = self.desc.get()
                self.df_2.to_csv(self.file, mode = 'a', index = False, header = False)
                
        def set_info(self, event): # Get units and engine of selected aircraft
            try:
                self.units.set(get_info(get_aircraft(), self.ac.get())["units"])
                self.eng.set(get_info(get_aircraft(), self.ac.get())["engine"])
            except:
                pass
                
        def show_message(self, header, message):
            tkinter.messagebox.showinfo(header, message)

        def show_help(self):
            msg = \
            '''
    Instructions:\n
1.    Select or type aircraft in the drop-down.\n
2.    Enter values for specified parameters.\n
2a.   To plot a single power setting, leave "Power setting 2" blank.\n
2b.   To plot a range between two power settings, enter a value for "Power setting 2".\n
4.    Enter the name of the power setting in the "Power description" field.\n
5.    Show the plot in the window using the "Preview plot" button.\n
6.    Save the plot using the "Save plot" button.\n
7.    Save the raw data file using the "Write to CSV" button.

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



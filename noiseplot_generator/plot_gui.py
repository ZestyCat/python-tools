import pandas as pd
import noiseline as nl
import noisecontour as nc
import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
from tkinter import filedialog as fd
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
import os
import sys
import subprocess

def main():

    # Check if a string is a float
    def is_number(string):
        try:
            float(string)
            return True
        except ValueError:
            return False

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
        temp_pad = " " * (4 - len(str(temp))) + str(temp)
        rh_pad = " " * (4 - len(str(rel_hum_pct))) + str(rel_hum_pct)
        speed_pad = " " * (3 - len(str(speed_kts))) + str(speed_kts)
        
        # Concatenate params into string
        command = "\n{}{}{} W  1  0.0\nF{}00{} {} VARIABLE   {}\n" \
            .format(code, temp_pad, rh_pad, code, pwr_pad, units_pad, speed_kts)
       
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
                        sel.append(float(line[7:16].strip()))
                        lmax.append(float(line[39:48].strip()))
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

    def run_o11(aircraft = "F-18E/F", power = 90, description = "Cruise", 
                    inches_hg = 29.92, temp = 59, rel_hum_pct = 70,
                    path = "./", input = 'input.o11_input', log = "log.o11_log", 
                    output = "output.o11_noise", ac_file = "./data/acdata.csv", 
                    os = "Windows"):

        # Find the corresponding code for aircraft in codes list file
        ac_data = pd.read_csv(ac_file)
        code  = ac_data[ac_data["aircraft"] == aircraft]["code"].item() # read csv, get code/units of aircraft
        units = ac_data[ac_data["aircraft"] == aircraft]["units"].item()
        
        # Pad params with spaces so they fit the Omega10 input format
        pwr_pad = " " * (10 - len(format(power, '.2f'))) + format(power, '.2f')
        units_pad = units + " " * (10 - len(units))
        temp_pad = " " * (4 - len(str(temp))) + str(temp)
        inches_hg_pad = " " * (6 - len(str(inches_hg))) + str(inches_hg)
        rh_pad = " " * (5 - len(str(rel_hum_pct))) + str(rel_hum_pct)
        
        # Concatenate params into string
        command = "\n{}{}{}{}   W    1 0.0\nR{}00{} {} VARIABLE\n" \
            .format(code, temp_pad, rh_pad, inches_hg_pad, code, pwr_pad, units_pad)
       
        #Write o11_input file
        with open(path + input, 'w') as file:
            file.write(command)
            file.close()
        
        # Run omega11
        if os == "Windows":
            subprocess.Popen(["omega11", input, log, output]).wait()
            return(output)
        elif os == "Linux":
            subprocess.Popen(["wine", bat]).wait()
            return(output)
        else:
            raise Exception("OS must be set to Windows or Linux")

    def read_o11(file = "./output.o11_noise"):
        with open(file) as file:
            lines = file.readlines()
            data = []
            for i, line in enumerate(lines):
                if i > 67: # ALMX dBA WITHOUT EXCESS SOUND ATTENUATION
                    data.append(line.split())
                if i == 90:
                    break
            df = pd.DataFrame(data[1:], columns = data[0]).set_index("(ft)", drop = True)
            return(df)
            
    # Main application window
    class App(ttk.Frame): 
        def __init__(self, master):
            super().__init__(master) # Initialize parent class
            
            # Initialize variables
            self.sv_nm     = tk.StringVar()
            self.ac        = tk.StringVar()
            self.pwr       = tk.StringVar()
            self.pwr_2     = tk.StringVar()
            self.desc      = tk.StringVar()
            self.units     = tk.StringVar()
            self.eng       = tk.StringVar()
            self.speed     = tk.IntVar()
            self.temp      = tk.IntVar()
            self.rh_pct    = tk.IntVar()
            self.bar_p     = tk.DoubleVar()
            self.p_type    = tk.StringVar()
            self.levels    = tk.StringVar()
            self.n_grids   = tk.IntVar()
            self.extent_ft = tk.IntVar()
            
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
            self.bar_p.set(29.92)
            self.p_type.set(1)
            self.levels.set("65, 75, 85, 95")
            self.n_grids.set(6)
            self.extent_ft.set(5000)
            
            # Make frames
            self.input_frame  = tk.Frame(highlightbackground = "black", highlightthickness = 1)
            self.fig_frame    = tk.Frame(highlightbackground = "black", highlightthickness = 1, bg = "darkgrey")
            self.ac_frame     = tk.Frame(self.input_frame, highlightbackground = "black", highlightthickness = 1)
            self.amb_frame    = tk.Frame(self.input_frame, highlightbackground = "black", highlightthickness = 1)
            self.button_frame = tk.Frame(self.input_frame, highlightbackground = "black", highlightthickness = 0)
            self.img_frame    = tk.Frame(self.input_frame, highlightbackground = "black", highlightthickness = 0, bg = "darkgrey")
            self.p_type_frame = tk.Frame(self.ac_frame)
            self.static_frame = tk.Frame(self.input_frame, highlightbackground = "black", highlightthickness = 1)

            # Make widgets
            self.aeso_logo  = tk.Label(self.img_frame, image = self.logo)
            self.ac_lab     = tk.Label(self.ac_frame, text = "Select aircraft:")
            self.ac_drp     = ttk.Combobox(self.ac_frame, textvariable = self.ac)
            self.ac_drp.bind('<<ComboboxSelected>>', self.set_info)
            self.ac_drp.bind('<KeyRelease>', self.set_info)
            self.pwr_lab    = tk.Label(self.ac_frame, text = "Power setting 1:") 
            self.pwr_ent    = tk.Entry(self.ac_frame, width = 13)
            self.pwr_unit   = tk.Label(self.ac_frame, text = "Power units", width = 7, anchor = "w")
            self.pwr_lab_2  = tk.Label(self.ac_frame, text = "Power setting 2:")
            self.pwr_ent_2  = tk.Entry(self.ac_frame, width = 13)
            self.pwr_unit_2 = tk.Label(self.ac_frame, text = "Power units", width = 7, anchor = "w")
            self.desc_lab   = tk.Label(self.ac_frame, text = "Power description:")
            self.desc_ent   = tk.Entry(self.ac_frame)
            self.p_type_lab = tk.Label(self.p_type_frame, text = "Plot type:")
            self.plt_type_1 = tk.Radiobutton(self.p_type_frame, variable = self.p_type, 
                    value = 1, command = self.flip_state, text = "Flyover")
            self.plt_type_2 = tk.Radiobutton(self.p_type_frame, variable = self.p_type, 
                    value = 2, command = self.flip_state, text = "Static")
            self.temp_lab   = tk.Label(self.amb_frame, text = "Air temperature:")
            self.temp_ent   = tk.Entry(self.amb_frame, width = 20)
            self.temp_unit  = tk.Label(self.amb_frame, text = "degrees F")
            self.bar_p_lab  = tk.Label(self.amb_frame, text = "Barometric pressure:")
            self.bar_p_ent  = tk.Entry(self.amb_frame, width = 20)
            self.bar_p_unit = tk.Label(self.amb_frame, text = "inches Hg")
            self.rh_pct_lab = tk.Label(self.amb_frame, text = "Relative humidity:")
            self.rh_pct_ent = tk.Entry(self.amb_frame, width = 20)
            self.rh_pct_unit= tk.Label(self.amb_frame, text = "%")
            self.speed_lab  = tk.Label(self.amb_frame, text = "Aircraft speed:")
            self.speed_ent  = tk.Entry(self.amb_frame, width = 20)
            self.speed_unit = tk.Label(self.amb_frame, text = "knots")
            self.extent_lab = tk.Label(self.amb_frame, text = "Extent:")
            self.extent_ent = tk.Entry(self.amb_frame, width = 20)
            self.extent_unit= tk.Label(self.amb_frame, text = "feet")
            self.levels_lab = tk.Label(self.amb_frame, text = "Contour levels:")
            self.levels_ent = tk.Entry(self.amb_frame, width = 20)
            self.levels_unit= tk.Label(self.amb_frame, text = "dB")
            self.grids_lab  = tk.Label(self.amb_frame, text = "Number of grids:")
            self.grids_ent  = tk.Entry(self.amb_frame, width = 4)
            self.plt_btn    = tk.Button(self.button_frame, command = self.show_plot, 
                                        text = "Preview plot ", image = self.play_img,
                                        compound = "right", height = 0)
            self.sv_btn     = tk.Button(self.button_frame, command = self.save_plot,
                                        text = "Save plot ", image = self.file_img,
                                        compound = "right", height = 0)
            self.del_btn    = tk.Button(self.button_frame, command = self.remove_plot,
                                        text = "Delete plot ", image = self.del_img,
                                        compound = "right", height = 0)
            self.csv_btn    = tk.Button(self.button_frame, command = self.save_data,
                                        text = "Write to CSV ", image = self.tabs_img,
                                        compound = "right", height = 0)
            
            self.help_btn   = tk.Button(self.button_frame, command = self.show_help,
                                        text = "Show help ", image = self.help_img, 
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
            self.bar_p_ent["textvariable"]   = self.bar_p
            self.ac_drp["values"] = get_aircraft()["aircraft"].tolist()
            self.extent_ent["textvariable"]  = self.extent_ft
            self.levels_ent["textvariable"]  = self.levels
            self.grids_ent["textvariable"]   = self.n_grids

            self.ac_drp.grid(row      = 0, column = 1, sticky = "W") # Manage geometry
            self.ac_lab.grid(row      = 0, column = 0, sticky = "E")
            self.aeso_logo.grid(row   = 0, column = 4, rowspan = 5, sticky = "SW")
            self.temp_lab.grid(row    = 0, column = 0, sticky = "E")
            self.temp_ent.grid(row    = 0, column = 1, sticky = "W")
            self.temp_unit.grid(row   = 0, column = 2, sticky = "W")
            self.bar_p_lab.grid(row   = 1, column = 0, sticky = "E")
            self.bar_p_ent.grid(row   = 1, column = 1, sticky = "W")
            self.bar_p_unit.grid(row  = 1, column = 2, sticky = "W")
            self.pwr_lab.grid(row     = 1, column = 0, sticky = "E")
            self.pwr_ent.grid(row     = 1, column = 1, sticky = "W")
            self.pwr_unit.grid(row    = 1, column = 1, sticky = "E")
            self.rh_pct_lab.grid(row  = 2, column = 0, sticky = "E")
            self.rh_pct_ent.grid(row  = 2, column = 1, sticky = "W")
            self.rh_pct_unit.grid(row = 2, column = 2, sticky = "W")
            self.pwr_lab_2.grid(row   = 2, column = 0, sticky = "E")
            self.pwr_ent_2.grid(row   = 2, column = 1, sticky = "W")
            self.pwr_unit_2.grid(row  = 2, column = 1, sticky = "E")
            self.speed_lab.grid(row   = 3, column = 0, sticky = "E")
            self.speed_ent.grid(row   = 3, column = 1, sticky = "W")
            self.speed_unit.grid(row  = 3, column = 2, sticky = "W")
            self.desc_lab.grid(row    = 3, column = 0, sticky = "E")
            self.desc_ent.grid(row    = 3, column = 1, sticky = "W")
            self.p_type_lab.grid(row  = 0, column = 0, sticky = "E")
            self.plt_type_1.grid(row  = 0, column = 1, sticky = "W")
            self.plt_type_2.grid(row  = 0, column = 2, sticky = "W")
            self.extent_lab.grid(row  = 4, column = 0, sticky = "E") 
            self.extent_ent.grid(row  = 4, column = 1, sticky = "W")
            self.extent_unit.grid(row = 4, column = 2, sticky = "W")
            self.levels_lab.grid(row  = 5, column = 0, sticky = "E")
            self.levels_ent.grid(row  = 5, column = 1, sticky = "W")
            self.levels_unit.grid(row = 5, column = 2, sticky = "W")
            self.grids_lab.grid(row   = 6, column = 0, sticky = "E")
            self.grids_ent.grid(row   = 6, column = 1, sticky = "W")
            self.plt_btn.grid(row     = 0, column = 0, sticky = "WE")
            self.sv_btn.grid(row      = 1, column = 0, sticky = "WE")
            self.del_btn.grid(row     = 2, column = 0, sticky = "WE")
            self.csv_btn.grid(row     = 3, column = 0, sticky = "WE")
            self.help_btn.grid(row    = 4, column = 0, sticky = "WE")
            self.input_frame.grid(row = 0, column = 0, sticky = "WE") # Geometry of frames
            self.fig_frame.grid(row   = 3, column = 0)
            self.ac_frame.grid(row    = 0, column = 0, pady = (10, 3), padx = (10, 3), columnspan = 1, sticky = "W")
            self.amb_frame.grid(row   = 1, column = 0, pady = (3, 3), padx = (10, 3), columnspan = 1, sticky = "WE")
            self.p_type_frame.grid(row= 4, column = 0, pady = (3, 3), padx = (10, 10), columnspan = 2, sticky = "WE")
            self.button_frame.grid(row= 1, column = 1, pady = (3, 10), padx = (3, 10), columnspan = 2, sticky = "WE")
            self.img_frame.grid(row   = 0, column = 1, padx = (0, 10), rowspan = 2, sticky = "NE")
            self.static_frame.grid(row = 3, padx = (10, 10), sticky = "WE")
            
            self.flip_state() 

        def flip_state(self): # Disable non-flyover/static entries
            self.test = self.p_type.get()
            if self.test == "1":
                print("Flyover")
                self.temp_ent['state']   = 'normal'
                self.bar_p_ent['state']  = 'disabled'
                self.rh_pct_ent['state'] = 'normal'
                self.speed_ent['state']  = 'normal'
                self.extent_ent['state'] = 'disabled'
                self.levels_ent['state'] = 'disabled'
                self.grids_ent['state']  = 'disabled'
                self.pwr_ent_2['state']  = 'normal'

            if self.test == "2":
                print("Static")
                self.pwr_ent_2['state']  = 'disabled'
                self.temp_ent['state']   = 'normal'
                self.bar_p_ent['state']  = 'normal'
                self.rh_pct_ent['state'] = 'normal'
                self.speed_ent['state']  = 'disabled'
                self.extent_ent['state'] = 'normal'
                self.levels_ent['state'] = 'normal'
                self.grids_ent['state']  = 'normal'


        def make_plot(self, save_name = None): # make a dataframe, call plotting function 
            if self.temp.get() > 200:
                self.warn_high_temp(self.temp.get())
            if self.p_type.get() == "1":
                # Run omega10 and return the output filename
                out   = run_o10(aircraft = self.ac.get(), power = round(float(self.pwr.get()), 2),
                           speed_kts = self.speed.get(), temp = self.temp.get(),
                           rel_hum_pct = self.rh_pct.get()) \
                           if is_number(self.pwr.get()) \
                           else None
                           
                # Run omega10 and return the output filename
                out_2 = run_o10(aircraft = self.ac.get(), power = round(float(self.pwr_2.get()), 2),
                           speed_kts = self.speed.get(), temp = self.temp.get(),
                           input = "input_2.o10_input", log = "log_2.o10_log",
                           output = "output_2.o10_output", rel_hum_pct = self.rh_pct.get()) \
                           if is_number(self.pwr_2.get()) \
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
                                    save_name = save_name, spd = self.speed.get())
                return(self.fig)
                
            elif self.p_type.get() == "2":
                out = run_o11(aircraft = self.ac.get(), power = round(float(self.pwr.get()), 2),
                            inches_hg = round(self.bar_p.get(), 2), temp = self.temp.get()) \
                            if is_number(self.pwr.get()) \
                            else None
                            
                if out is None:
                    self.m = "Please enter some power setting data."
                    self.show_message("Entry needed", self.m)
                    return(None)
                    
                df  = None if out is None else read_o11(out)
                
                self.fig = nc.plot_contour(df, aircraft = self.ac.get(), engine = self.eng.get(),
                                power = self.pwr.get() + self.units.get(), n_grids = self.n_grids.get(),
                                levels = [int(l) for l in self.levels.get().split(", ")],
                                extent_ft = self.extent_ft.get(), save_name = save_name)
                
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
                if is_number(self.pwr.get()) == False and is_number(self.pwr_2.get()) == False:
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
            if self.temp.get() > 200:
                self.warn_high_temp(self.temp.get())
            
            # Run omega10 and return the output filename
            out = run_o10(aircraft = self.ac.get(), power = round(float(self.pwr.get()), 2),
                       speed_kts = self.speed.get(), temp = self.temp.get(),
                       rel_hum_pct = self.rh_pct.get()) \
                       if is_number(self.pwr.get()) \
                       else None
                       
            # Run omega10 and return the output filename  
            out_2 = run_o10(aircraft = self.ac.get(), power = round(float(self.pwr_2.get()), 2),
                       speed_kts = self.speed.get(), temp = self.temp.get(),
                       input = "input_2.o10_input", log = "log_2.o10_log",
                       output = "output_2.o10_output", rel_hum_pct = self.rh_pct.get()) \
                       if is_number(self.pwr_2.get()) \
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
            
        def warn_high_temp(self, temp):
            msg = "You have entered an ambient temperature of {}. \nPlease be aware that Omega10 may exhibit strange behavior at very high ambient temperatures." \
                    .format(temp)
            self.show_message("Warning", msg)

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



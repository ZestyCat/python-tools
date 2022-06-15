import pandas as pd
import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
from tkinter import filedialog as fd
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
import os
import sys
import subprocess

def main():
    import functions as fn # After chdir to _MEIPASS
    import noiseline as nl
    import noisecontour as nc
    
    # Main application window
    class App(ttk.Frame): 
        def __init__(self, master):
            super().__init__(master) # Initialize parent class (Tk)
            
            # Initialize variables
            self.sv_nm     = tk.StringVar()
            self.ac        = tk.StringVar()
            self.pwr       = tk.StringVar()
            self.pwr_2     = tk.StringVar()
            self.desc      = tk.StringVar()
            self.units     = tk.StringVar()
            self.eng       = tk.StringVar()
            self.p_type    = tk.StringVar()
            self.levels    = tk.StringVar()
            self.speed     = tk.IntVar()
            self.temp      = tk.IntVar()
            self.rh_pct    = tk.IntVar()
            self.n_grids   = tk.IntVar()
            self.extent_ft = tk.IntVar()
            self.bar_p     = tk.DoubleVar()
            
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
            self.param_frame  = tk.Frame(self.input_frame, highlightbackground = "black", highlightthickness = 1)
            self.button_frame = tk.Frame(self.input_frame, highlightbackground = "black", highlightthickness = 0)
            self.img_frame    = tk.Frame(self.input_frame, highlightbackground = "black", highlightthickness = 0, bg = "darkgrey")
            self.p_type_frame = tk.Frame(self.ac_frame)

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
            self.temp_lab   = tk.Label(self.param_frame, text = "Air temperature:")
            self.temp_ent   = tk.Entry(self.param_frame, width = 20)
            self.temp_unit  = tk.Label(self.param_frame, text = "degrees F")
            self.bar_p_lab  = tk.Label(self.param_frame, text = "Barometric pressure:")
            self.bar_p_ent  = tk.Entry(self.param_frame, width = 20)
            self.bar_p_unit = tk.Label(self.param_frame, text = "inches Hg")
            self.rh_pct_lab = tk.Label(self.param_frame, text = "Relative humidity:")
            self.rh_pct_ent = tk.Entry(self.param_frame, width = 20)
            self.rh_pct_unit= tk.Label(self.param_frame, text = "%")
            self.speed_lab  = tk.Label(self.param_frame, text = "Aircraft speed:")
            self.speed_ent  = tk.Entry(self.param_frame, width = 20)
            self.speed_unit = tk.Label(self.param_frame, text = "knots")
            self.extent_lab = tk.Label(self.param_frame, text = "Extent:")
            self.extent_ent = tk.Entry(self.param_frame, width = 20)
            self.extent_unit= tk.Label(self.param_frame, text = "feet")
            self.levels_lab = tk.Label(self.param_frame, text = "Contour levels:")
            self.levels_ent = tk.Entry(self.param_frame, width = 20)
            self.levels_unit= tk.Label(self.param_frame, text = "dB")
            self.grids_lab  = tk.Label(self.param_frame, text = "Number of grids:")
            self.grids_ent  = tk.Entry(self.param_frame, width = 4)
            self.plt_btn    = tk.Button(self.button_frame, command = self.show_plot, 
                                        text = "Preview plot ", image = self.play_img,
                                        compound = "right", width = 110)
            self.sv_btn     = tk.Button(self.button_frame, command = self.save_plot,
                                        text = "Save plot ", image = self.file_img,
                                        compound = "right", width = 110)
            self.del_btn    = tk.Button(self.button_frame, command = self.remove_plot,
                                        text = "Delete plot ", image = self.del_img,
                                        compound = "right", width = 110)
            self.csv_btn    = tk.Button(self.button_frame, command = self.save_data,
                                        text = "Write to CSV ", image = self.tabs_img,
                                        compound = "right", width = 110)
            self.help_btn   = tk.Button(self.button_frame, command = self.show_help,
                                        text = "Show help ", image = self.help_img, 
                                        compound = "right", width = 110)

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
            self.extent_ent["textvariable"]  = self.extent_ft
            self.levels_ent["textvariable"]  = self.levels
            self.grids_ent["textvariable"]   = self.n_grids

            # Manage geometry
            self.ac_drp.grid(row      = 0, column = 1, sticky = "W") 
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
            self.sv_btn.grid(row      = 0, column = 1, sticky = "WE")
            self.del_btn.grid(row     = 0, column = 2, sticky = "WE")
            self.csv_btn.grid(row     = 0, column = 3, sticky = "WE")
            self.help_btn.grid(row    = 0, column = 4, sticky = "WE")
            
            # Geometry of frames
            self.input_frame.grid(row = 0, column = 0, sticky = "WE") 
            self.fig_frame.grid(row   = 3, column = 0)
            self.ac_frame.grid(row    = 0, column = 0, pady = (10, 3), padx = (10, 3), columnspan = 1, sticky = "W")
            self.param_frame.grid(row = 1, column = 0, pady = (3, 3), padx = (10, 3), columnspan = 1, sticky = "WE")
            self.p_type_frame.grid(row= 4, column = 0, pady = (3, 3), padx = (10, 10), columnspan = 2, sticky = "WE")
            self.button_frame.grid(row= 4, column = 0, pady = (3, 10), padx = (3, 10), columnspan = 2, sticky = "WE")
            self.img_frame.grid(row   = 0, column = 1, padx = (0, 10), rowspan = 2, sticky = "NE")
            
            self.flip_state() # After the app has loaded, disable static options and populate drop-down.

        def flip_state(self): # Disable non-flyover/static entries 
            self.test = self.p_type.get()
            if self.test == "1":
                self.temp_ent['state']   = 'normal'
                self.bar_p_ent['state']  = 'disabled'
                self.rh_pct_ent['state'] = 'normal'
                self.speed_ent['state']  = 'normal'
                self.extent_ent['state'] = 'disabled'
                self.levels_ent['state'] = 'disabled'
                self.grids_ent['state']  = 'disabled'
                self.pwr_ent_2['state']  = 'normal'
            if self.test == "2":
                self.pwr_ent_2['state']  = 'disabled'
                self.temp_ent['state']   = 'normal'
                self.bar_p_ent['state']  = 'normal'
                self.rh_pct_ent['state'] = 'normal'
                self.speed_ent['state']  = 'disabled'
                self.extent_ent['state'] = 'normal'
                self.levels_ent['state'] = 'normal'
                self.grids_ent['state']  = 'normal'
                self.pwr_2.set("")
            self.ac_drp["values"] = fn.get_aircraft(type = int(self.test))["aircraft"].tolist() # Re-populate drop-down 

        def make_plot(self, save_name = None): # make a dataframe, call plotting function 
            if self.temp.get() > 200:
                self.warn_high_temp(self.temp.get())
                
            # Show a popup if no entry 
            if fn.is_number(self.pwr.get()) == False & fn.is_number(self.pwr_2.get()) == False:
                self.m = "Please enter some power setting data."
                self.show_message("Entry needed", self.m)
                return(None)
                
            if self.p_type.get() == "1": # Flyover plot
                # Run omega10 and return the output filename
                out   = fn.run_o10(aircraft = self.ac.get(), power = round(float(self.pwr.get()), 2),
                           speed_kts = self.speed.get(), temp = self.temp.get(),
                           rel_hum_pct = self.rh_pct.get()) \
                           if fn.is_number(self.pwr.get()) \
                           else None
                           
                # Run omega10 and return the output filename
                out_2 = fn.run_o10(aircraft = self.ac.get(), power = round(float(self.pwr_2.get()), 2),
                           speed_kts = self.speed.get(), temp = self.temp.get(),
                           input = "input_2.o10_input", log = "log_2.o10_log",
                           output = "output_2.o10_output", rel_hum_pct = self.rh_pct.get()) \
                           if fn.is_number(self.pwr_2.get()) \
                           else None
                
                # Make dataframes from o10 output
                self.df   = None if out is None else fn.read_o10(out)
                self.df_2 = None if out_2 is None else fn.read_o10(out_2)
                
                # Plot 
                self.fig  = nl.plot(self.df, ps_name = self.desc.get(), 
                                    save_name = save_name) \
                    if self.df_2 is None else \
                    nl.plot(self.df, self.df_2, ps_name = self.desc.get(), 
                                    save_name = save_name, spd = self.speed.get())
                return(self.fig)
            
            elif self.p_type.get() == "2": # Static plot
                self.check_static_range(self.ac.get(), self.pwr.get()) # Is pwr within range? If not, correct it  
                def try_fig(df):
                    try:
                        fig = nc.plot_contour(df, aircraft = self.ac.get(), engine = self.eng.get(),
                                        description = self.desc.get(), power = self.pwr.get() + self.units.get(), 
                                        n_grids = self.n_grids.get(), levels = [float(l.strip()) for l in self.levels.get().split(",")],
                                        extent_ft = self.extent_ft.get(), save_name = save_name)
                        
                        return(fig)
                    except:
                        msg = "Please enter comma-separated contour dB values"
                        self.show_message("Entry error", msg)
                        return(None)
                        
                try: # Try running with primary units
                    df = self.run_o11_unit("")
                    return(try_fig(df))
                except: # Try running through every possible power setting unit
                    pass
                    # units_list = ['NF', '% RPM', 'LBS', '% NC', 'KNOTS', 'PLA', 'LBS/HR', 'RPM', 'C TIT', 'HP', 
                    # '% NF', 'EPR', '% N1', '%Q-BPA', '%QQBPA', '% NR', 'POWER', 'ISHP', '% N2', '% ETR',                          
                    # '% TORQUE', 'IN HG', '% SLTT', 'ESHP', '% Torque', ""]
                    # for u in units_list:
                        # try:
                            # df = self.run_o11_unit(u)
                            # fig = try_fig(df)
                            # print("made fig")
                            # return(fig)
                        # except:
                            # print("failed to make fig")
                            # pass
                    print("None of these units worked, try something else")
               
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
                if fn.is_number(self.pwr.get()) == False and fn.is_number(self.pwr_2.get()) == False:
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
            
            # Show a popup if no entry 
            if fn.is_number(self.pwr.get()) == False & fn.is_number(self.pwr_2.get()) == False:
                self.m = "Please enter some power setting data."
                self.show_message("Entry needed", self.m)
                return(None)
            
            if self.p_type.get() == "1":
                # Run omega10 and return the output filename
                out = fn.run_o10(aircraft = self.ac.get(), power = round(float(self.pwr.get()), 2),
                           speed_kts = self.speed.get(), temp = self.temp.get(),
                           rel_hum_pct = self.rh_pct.get()) \
                           if fn.is_number(self.pwr.get()) \
                           else None
                           
                # Run omega10 and return the output filename  
                out_2 = fn.run_o10(aircraft = self.ac.get(), power = round(float(self.pwr_2.get()), 2),
                           speed_kts = self.speed.get(), temp = self.temp.get(),
                           input = "input_2.o10_input", log = "log_2.o10_log",
                           output = "output_2.o10_output", rel_hum_pct = self.rh_pct.get()) \
                           if fn.is_number(self.pwr_2.get()) \
                           else None

                self.df = None if out is None else fn.read_o10(out)
                self.df_2 = None if out_2 is None else fn.read_o10(out_2)
                
                self.file = fd.asksaveasfilename(defaultextension = ".csv", 
                                                filetypes = [("comma separated value", ".csv")])
                self.cols = pd.DataFrame(columns = ["ac", "eng", "pwr", "unit", "spd", 
                                                        "dist", "lmax", "sel", "desc", "temp",
                                                        "rh_pct"])
                self.cols.to_csv(self.file, index = False) # Write headers to csv file
                
                if self.df is not None:
                    self.df["desc"] = self.desc.get()
                    self.df["temp_F"] = self.temp.get()
                    self.df["rh_pct"] = self.rh_pct.get()
                    self.df.to_csv(self.file, mode = 'a', index = False, header = False)
                
                if self.df_2 is not None:
                    self.df_2["desc"] = self.desc.get()
                    self.df_2["temp_F"] = self.temp.get()
                    self.df_2["rh_pct"] = self.rh_pct.get()
                    self.df_2.to_csv(self.file, mode = 'a', index = False, header = False)
                    
            elif self.p_type.get() == "2":
                # out = fn.run_o11(aircraft = self.ac.get(), power = round(float(self.pwr.get()), 2),
                            # inches_hg = round(self.bar_p.get(), 2), temp = self.temp.get(), units = self.units.get()) \
                            # if fn.is_number(self.pwr.get()) \
                            # else None
                
                # self.df = fn.read_o11(out)
                file = fd.asksaveasfilename(defaultextension = ".csv",
                        filetypes = [("comma separated value", ".csv")])
                        
                def write_file(df, file):
                    header = pd.DataFrame(columns = [self.ac.get(), self.eng.get(), 
                        str(self.pwr.get()) + self.units.get(), self.desc.get(), 
                        str(self.rh_pct.get()) + "% RH", str(self.temp.get()) + "Deg. F",
                        str(self.bar_p.get()) + "Inches Hg"])
                    
                    header.to_csv(file, mode = "w")
                    df.to_csv(file, mode = "a")
                
                try: # Try running with primary units
                    df = self.run_o11_unit(self.units.get())
                    write_file(df, file)
                    return
                except: # Try running through every possible power setting unit
                    units_list = ['NF', '% RPM', 'LBS', '% NC', 'KNOTS', 'PLA', 'LBS/HR', 'RPM', 'C TIT', 'HP', 
                    '% NF', 'EPR', '% N1', '%Q-BPA', '%QQBPA', '% NR', 'POWER', 'ISHP', '% N2', '% ETR',                          
                    '% TORQUE', 'IN HG', '% SLTT', 'ESHP', '% Torque', ""]
                    for u in units_list:
                        try:
                            df = self.run_o11_unit(u)
                            write_file(df, file)
                            return
                        except:
                            pass
                    print("None of these units worked, try something else")
                
                
                    
        def set_info(self, event): # Get units and engine of selected aircraft
            try:
                self.units.set(fn.get_info(fn.get_aircraft(type = int(self.p_type.get())), self.ac.get())["units"])
                self.eng.set(fn.get_info(fn.get_aircraft(), self.ac.get())["engine"])
            except:
                pass
                
        def run_o11_unit(self, unit, save_name = None): # Run o11 with specified units. Sometimes o11 runs but does produces an error if unit is blank
                    out = fn.run_o11(aircraft = self.ac.get(), power = round(float(self.pwr.get()), 2), # Run o11
                                inches_hg = round(self.bar_p.get(), 2), temp = self.temp.get(), units = unit) \
                                if fn.is_number(self.pwr.get()) \
                                else None
                        
                    self.df  = fn.read_o11(out) # Read o11 output file
                    return(self.df)
                        
        # Get minimum and maximum values for static. Check whether user input is out of range. If so, correct the entry
        def check_static_range(self, ac, pwr, file = "./data/static_power_setting_list.csv"):
            p = float(pwr)
            df = pd.read_csv(file)
            ps = list(map(float, df[df["Aircraft"] == ac]["Power"].tolist())) # get a list of ps for that ac
            rng = min(ps), max(ps)
            if p > rng[0] and p < rng[1]: # if pwr is in range
                pass
            elif p < rng[0]: # if pwr is lower than range
                self.pwr.set(rng[0]) # set to lower bounds
            elif p > rng[1]: # if it is above range
                self.pwr.set(rng[1]) # set to upper bounds
            else:
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
    print("about to check if meipass")
    if hasattr(sys, '_MEIPASS'):
        print("Yes meipass")
        saved_dir = os.getcwd()
        os.chdir(sys._MEIPASS)
        try:
            main()
        finally:
            os.chdir(saved_dir) 
    else:
        print("Not meipass, running main")
        main()
        print("Not meipass, main just finished")



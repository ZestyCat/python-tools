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
    import noiseplot as nplot
    
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
            self.op_type   = tk.StringVar()
            self.interp    = tk.StringVar()
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
            self.op_type.set(1)
            self.interp.set(1)
            self.levels.set("65, 75, 85, 95")
            self.n_grids.set(6)
            self.extent_ft.set(5000)
            self.units.set("Units")
            
            # Make frame
            self.input_frame  = tk.Frame(highlightthickness = 1)
            self.fig_frame    = tk.Frame(highlightbackground = "black", highlightthickness = 1, bg = "darkgrey")
            self.param_frame     = tk.Frame(self.input_frame, highlightbackground = "black", highlightthickness = 1)
            self.button_frame = tk.Frame(self.input_frame, highlightbackground = "black", highlightthickness = 0)
            self.img_frame    = tk.Frame(self.input_frame, highlightbackground = "black", highlightthickness = 0, bg = "darkgrey")
            self.radials_frame = tk.Frame(self.param_frame)

            # Make widgets
            self.aeso_logo  = tk.Label(self.img_frame, image = self.logo)
            self.ac_lab     = tk.Label(self.param_frame, text = "Select aircraft:")
            self.ac_drp     = ttk.Combobox(self.param_frame, textvariable = self.ac, width = 17)
            self.ac_drp.bind('<<ComboboxSelected>>', self.set_info)
            self.ac_drp.bind('<KeyRelease>', self.set_info)
            self.pwr_lab    = tk.Label(self.param_frame, text = "Power settings:") 
            self.pwr_ent    = tk.Entry(self.param_frame, width = 8)
            self.to_lab     = tk.Label(self.param_frame, text = "to")
            self.pwr_ent_2  = tk.Entry(self.param_frame, width = 8)
            self.pwr_unit   = ttk.Combobox(self.param_frame, textvariable = self.units, width = 9)
            self.fixed_lab  = tk.Label(self.param_frame, text = "Fixed power:") 
            self.fixed_pwr  = ttk.Combobox(self.param_frame, textvariable = self.pwr, width = 17)
            self.fixed_pwr.bind('<<ComboboxSelected>>', self.set_info)
            self.desc_lab   = tk.Label(self.param_frame, text = "Power description:")
            self.desc_ent   = tk.Entry(self.param_frame)
            self.op_type_lab = tk.Label(self.radials_frame, text = "Operation type:")
            self.op_type_1 = tk.Radiobutton(self.radials_frame, variable = self.op_type, 
                    value = 1, command = self.set_type, text = "Flyover")
            self.op_type_2 = tk.Radiobutton(self.radials_frame, variable = self.op_type, 
                    value = 2, command = self.set_type, text = "Static")
            self.interp_lab = tk.Label(self.radials_frame, text = "Interpolation:")
            self.interp_1 = tk.Radiobutton(self.radials_frame, variable = self.interp, 
                    value = 1, command = self.set_fixed, text = "Variable")
            self.interp_2 = tk.Radiobutton(self.radials_frame, variable = self.interp, 
                    value = 2, command = self.set_fixed, text = "Fixed")
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

            # Link widgets to variables
            self.speed_ent['textvariable']   = self.speed
            self.temp_ent['textvariable']    = self.temp
            self.rh_pct_ent['textvariable']  = self.rh_pct
            self.pwr_ent["textvariable"]     = self.pwr 
            self.pwr_ent_2["textvariable"]   = self.pwr_2
            self.pwr_unit["textvariable"]    = self.units
            self.desc_ent["textvariable"]    = self.desc
            self.bar_p_ent["textvariable"]   = self.bar_p
            self.extent_ent["textvariable"]  = self.extent_ft
            self.levels_ent["textvariable"]  = self.levels
            self.grids_ent["textvariable"]   = self.n_grids

            # Geometry of widgets
            self.ac_drp.grid(row      = 1, column = 1, sticky = "W", columnspan = 3) 
            self.ac_lab.grid(row      = 1, column = 0, sticky = "E")
            self.aeso_logo.grid(row   = 0, column = 4, rowspan = 5, sticky = "SW")
            self.temp_lab.grid(row    = 5, column = 0, sticky = "E")
            self.temp_ent.grid(row    = 5, column = 1, sticky = "W", columnspan = 3)
            self.temp_unit.grid(row   = 5, column = 4, sticky = "W")
            self.bar_p_lab.grid(row   = 6, column = 0, sticky = "E")
            self.bar_p_ent.grid(row   = 6, column = 1, sticky = "W", columnspan = 3)
            self.bar_p_unit.grid(row  = 6, column = 4, sticky = "W")
            self.pwr_lab.grid(row     = 2, column = 0, sticky = "E")
            self.pwr_ent.grid(row     = 2, column = 1, sticky = "W")
            self.to_lab.grid(row      = 2, column = 2)
            self.pwr_ent_2.grid(row   = 2, column = 3, sticky = "E")
            self.pwr_unit.grid(row    = 2, column = 4, sticky = "E")
            self.rh_pct_lab.grid(row  = 7, column = 0, sticky = "E")
            self.rh_pct_ent.grid(row  = 7, column = 1, sticky = "W", columnspan = 3)
            self.rh_pct_unit.grid(row = 7, column = 4, sticky = "W")
            self.speed_lab.grid(row   = 8, column = 0, sticky = "E")
            self.speed_ent.grid(row   = 8, column = 1, sticky = "W", columnspan = 3)
            self.speed_unit.grid(row  = 8, column = 4, sticky = "W")
            self.fixed_lab.grid(row   = 3, column = 0, sticky = "E")
            self.fixed_pwr.grid(row   = 3, column = 1, sticky = "W", columnspan = 3)
            self.desc_lab.grid(row    = 4, column = 0, sticky = "E")
            self.desc_ent.grid(row    = 4, column = 1, sticky = "W", columnspan = 3)
            self.op_type_lab.grid(row = 0, column = 0, sticky = "E")
            self.op_type_1.grid(row   = 0, column = 1, sticky = "W")
            self.op_type_2.grid(row   = 0, column = 2, sticky = "W")
            self.interp_lab.grid(row  = 1, column = 0, sticky = "E")
            self.interp_1.grid(row    = 1, column = 1, sticky = "W")
            self.interp_2.grid(row    = 1, column = 2, sticky = "W")
            self.extent_lab.grid(row  = 9, column = 0, sticky = "E") 
            self.extent_ent.grid(row  = 9, column = 1, sticky = "W", columnspan = 3)
            self.extent_unit.grid(row = 9, column = 4, sticky = "W")
            self.levels_lab.grid(row  = 10, column = 0, sticky = "E")
            self.levels_ent.grid(row  = 10, column = 1, sticky = "W", columnspan = 3)
            self.levels_unit.grid(row = 10, column = 4, sticky = "W")
            self.grids_lab.grid(row   = 11, column = 0, sticky = "E")
            self.grids_ent.grid(row   = 11, column = 1, sticky = "W", columnspan = 3)
            self.plt_btn.grid(row     = 0, column = 0, sticky = "WE")
            self.sv_btn.grid(row      = 0, column = 1, sticky = "WE")
            self.del_btn.grid(row     = 0, column = 2, sticky = "WE")
            self.csv_btn.grid(row     = 0, column = 3, sticky = "WE")
            
            # Geometry of frames
            self.input_frame.grid(row = 0, column = 0, sticky = "WE") 
            self.fig_frame.grid(row   = 3, column = 0)
            self.param_frame.grid(row    = 0, column = 0, pady = (10, 3), padx = (10, 3), columnspan = 1, sticky = "W")
            self.radials_frame.grid(row= 0, column = 0, pady = (3, 3), padx = (10, 10), columnspan = 4, sticky = "WE")
            self.button_frame.grid(row= 4, column = 0, pady = (3, 10), padx = (3, 10), columnspan = 2, sticky = "WE")
            self.img_frame.grid(row   = 0, column = 1, padx = (0, 10), rowspan = 2, sticky = "NE")
            
            self.set_type() # After the app has loaded, disable static options and populate drop-down.
            self.set_fixed()

        def populate_list(self, op_type):
            df = fn.get_operations(type = int(op_type))
            print(df)
            if self.interp.get() == "1": # Variable
                self.ac_drp["values"] = pd.unique(df[df.interpolation == "VARIABLE"]["aircraft"]).tolist()
            elif self.interp.get() == "2": # Fixed
                self.ac_drp["values"] = pd.unique(df[df.interpolation == "FIXED"]["aircraft"]).tolist() 
            else:
                pass
                
        def set_type(self): # Disable non-flyover/static entries 
            test_op  = self.op_type.get()
            if test_op == "1":
                self.temp_ent['state']   = 'normal'
                self.bar_p_ent['state']  = 'disabled'
                self.rh_pct_ent['state'] = 'normal'
                self.speed_ent['state']  = 'normal'
                self.extent_ent['state'] = 'disabled'
                self.levels_ent['state'] = 'disabled'
                self.grids_ent['state']  = 'disabled'
                self.pwr_ent_2['state']  = 'normal'
                self.to_lab['text']      = 'to'
            if test_op == "2":
                self.pwr_ent_2['state']  = 'disabled'
                self.temp_ent['state']   = 'normal'
                self.bar_p_ent['state']  = 'normal'
                self.rh_pct_ent['state'] = 'normal'
                self.speed_ent['state']  = 'disabled'
                self.extent_ent['state'] = 'normal'
                self.levels_ent['state'] = 'normal'
                self.grids_ent['state']  = 'normal'
                self.to_lab['text']      = ''
                self.pwr_2.set("")
            self.populate_list(test_op)
            self.set_info(None)

        def set_fixed(self):
            test_int = self.interp.get() 
            if test_int == "1":
                self.pwr_ent['state']    = 'normal'
                self.pwr_ent_2['state']  = 'normal'
                self.fixed_pwr['state']  = 'disabled'
                self.to_lab['text']      = 'to'
            if test_int == "2":
                self.pwr_ent['state']    = 'disabled'
                self.pwr_ent_2['state']  = 'disabled'
                self.fixed_pwr['state']  = 'normal'
                self.to_lab['text']      = ''
            self.set_info(None)
            self.populate_list(self.op_type.get())
                
        def set_info(self, event): # Get units and engine of selected aircraft
            try:
                ops = fn.get_operations(type = int(self.op_type.get()))
                info = fn.get_info(ops, self.ac.get())
                units = [u for u in [info.unit_1, info.unit_2, info.unit_3] if pd.isna(u) == False]
                self.units.set(info["unit_1"])
                self.eng.set(info["engine"])
                self.pwr_unit["values"] = units
                op = "FLIGHT" if self.op_type.get() == "1" else "STATIC" 
                fixed_ops = ops[(ops.aircraft == self.ac.get()) & (ops.operation_type == op) & (ops.interpolation == "FIXED")]
                fixed = fixed_ops.power_1.tolist()
                self.fixed_pwr["values"] = fixed
            except:
                pass
                
        def make_plot(self, save_name = None): # make a dataframe, call plotting function 
            if self.temp.get() > 200:
                self.warn_high_temp(self.temp.get())
            
            i = "VARIABLE" if self.interp.get() == "1" else "FIXED" # Fixed or variable interpolation?
            
            if i == "VARIABLE":
                self.correct_range(self.ac.get(), self.pwr.get()) # Correct to power setting within variable range if variable interpolation
            else:
                pass
                
            # Show a popup if no entry 
            if fn.is_number(self.pwr.get()) == False & fn.is_number(self.pwr_2.get()) == False:
                self.m = "Please enter some power setting data."
                self.show_message("Entry needed", self.m)
                return(None)
                
            if self.op_type.get() == "1": # Flyover plot
                # Run omega10 and return the output filename
                out   = fn.run_o10(aircraft = self.ac.get(), power = round(float(self.pwr.get()), 2),
                           speed_kts = self.speed.get(), temp = self.temp.get(), interpolation = i,
                           rel_hum_pct = self.rh_pct.get(), units = self.units.get()) \
                           if fn.is_number(self.pwr.get()) \
                           else None
                           
                # Run omega10 and return the output filename
                out_2 = fn.run_o10(aircraft = self.ac.get(), power = round(float(self.pwr_2.get()), 2),
                           speed_kts = self.speed.get(), temp = self.temp.get(), interpolation = i,
                           input = "input_2.o10_input", log = "log_2.o10_log",
                           output = "output_2.o10_noise", rel_hum_pct = self.rh_pct.get(),
                           units = self.units.get()) \
                           if fn.is_number(self.pwr_2.get()) \
                           else None
                
                # Make dataframes from o10 output
                self.df   = None if out is None else fn.read_o10("./omega/" + out)
                self.df_2 = None if out_2 is None else fn.read_o10("./omega/" + out_2)
                
                # Plot 
                self.fig  = nplot.plot_line(self.df, ps_name = self.desc.get(), 
                                    save_name = save_name) \
                    if self.df_2 is None else \
                    nplot.plot_line(self.df, self.df_2, ps_name = self.desc.get(), 
                                    save_name = save_name, spd = self.speed.get())
                return(self.fig)
            
            elif self.op_type.get() == "2": # Static plot
                out = fn.run_o11(aircraft = self.ac.get(), power = round(float(self.pwr.get()), 2),
                            inches_hg = round(self.bar_p.get(), 2), temp = self.temp.get(), 
                            units = self.units.get(), interpolation = i) \
                            if fn.is_number(self.pwr.get()) \
                            else None
                
                df = fn.read_o11("./omega/" + out)
                
                try:
                    fig = nplot.plot_contour(df, aircraft = self.ac.get(), engine = self.eng.get(),
                                    description = self.desc.get(), power = self.pwr.get() + self.units.get(), 
                                    n_grids = self.n_grids.get(), levels = [float(l.strip()) for l in self.levels.get().split(",")],
                                    extent_ft = self.extent_ft.get(), save_name = save_name)
                    
                    return(fig)
                except:
                    msg = "Please enter comma-separated contour dB values"
                    self.show_message("Entry error", msg)
                    return(None)
               
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
                
            i = "VARIABLE" if self.interp.get() == "1" else "FIXED" # Fixed or variable interpolation?
            
            if i == "VARIABLE":
                self.correct_range(self.ac.get(), self.pwr.get()) # Correct to power setting within variable range if variable interpolation
            else:
                pass
            
            # Show a popup if no entry 
            if fn.is_number(self.pwr.get()) == False & fn.is_number(self.pwr_2.get()) == False:
                self.m = "Please enter some power setting data."
                self.show_message("Entry needed", self.m)
                return(None)
            
            if self.op_type.get() == "1":
                # Run omega10 and return the output filename
                out = fn.run_o10(aircraft = self.ac.get(), power = round(float(self.pwr.get()), 2),
                           speed_kts = self.speed.get(), temp = self.temp.get(), interpolation = i,
                           rel_hum_pct = self.rh_pct.get(), units = self.units.get()) \
                           if fn.is_number(self.pwr.get()) \
                           else None
                           
                # Run omega10 and return the output filename  
                out_2 = fn.run_o10(aircraft = self.ac.get(), power = round(float(self.pwr_2.get()), 2),
                           speed_kts = self.speed.get(), temp = self.temp.get(), interpolation = i,
                           input = "input_2.o10_input", log = "log_2.o10_log",
                           output = "output_2.o10_output", rel_hum_pct = self.rh_pct.get(), 
                           units = self.units.get()) \
                           if fn.is_number(self.pwr_2.get()) \
                           else None

                self.df = None if out is None else fn.read_o10("./omega/" + out)
                self.df_2 = None if out_2 is None else fn.read_o10("./omega/" + out_2)
                
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
                    
            elif self.op_type.get() == "2":
                out = fn.run_o11(aircraft = self.ac.get(), power = round(float(self.pwr.get()), 2),
                            inches_hg = round(self.bar_p.get(), 2), temp = self.temp.get(), 
                            units = self.units.get(), interpolation = i) \
                            if fn.is_number(self.pwr.get()) \
                            else None
                
                df = fn.read_o11("./omega/" + out)
                file = fd.asksaveasfilename(defaultextension = ".csv",
                        filetypes = [("comma separated value", ".csv")])
                        
                def write_file(df, file):
                    header = pd.DataFrame(columns = [self.ac.get(), self.eng.get(), 
                        str(self.pwr.get()) + self.units.get(), self.desc.get(), 
                        str(self.rh_pct.get()) + "% RH", str(self.temp.get()) + "Deg. F",
                        str(self.bar_p.get()) + "Inches Hg"])
                    
                    header.to_csv(file, mode = "w")
                    df.to_csv(file, mode = "a")
                
                try: 
                    write_file(df, file)
                    return
                except: 
                    print("Couldn't save that data")
                        
        # Get minimum and maximum values for static. Check whether user input is out of range. If so, correct the entry
        def correct_range(self, ac, pwr, file = "./data/operation_data.csv"):
            p = float(pwr)
            df = pd.read_csv(file)
            s = df[(df.aircraft == ac) & (df.operation_type == "STATIC") & (df.interpolation == "VARIABLE")] \
                if self.op_type.get() == "2" else \
                df[(df.aircraft == ac) & (df.operation_type == "FLIGHT") & (df.interpolation == "VARIABLE")]
            # Get corresponding power settings for selected units
            power = "power_1" if self.units.get() in s.unit_1.tolist() else \
                    "power_2" if self.units.get() in s.unit_2.tolist() else \
                    "power_3" if self.units.get() in s.unit_3.tolist() else None
            ps = list(map(float, s[power].tolist())) # get a list of static/variable ps for that ac
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
            os.chdir(saved_dir) 
    else:
        main()



import pandas as pd
import subprocess
import os
import sys

# Miscellaneous functions to make the gui work
    
def get_aircraft(file = "./data/acdata.csv", ignore = "./data/bad_ac_list.csv"):
    df = pd.read_csv(file)
    df_2 = pd.read_csv(ignore, header = None)
    ignore = "|".join(df_2[0].tolist()) # Make regex for all aircraft to ignore
    return(df[df["aircraft"].str.contains(ignore) == False])

def get_info(df, aircraft = "F-18E/F"):
    return(df[df["aircraft"] == aircraft].iloc[0])

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

# Write o11 input file, call subprocess to run o11
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
   
    print(command)
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

#print(read_o11().iloc[0])

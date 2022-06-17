import pandas as pd
import subprocess
import os
import sys
    
# Check if a string is a float
def is_number(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

# Get code, units, engine for all aircraft (ac) except those in ignore file, filter by type flight/static
def get_operations(file = "./data/operation_data.csv", type = 1):
    df = pd.read_csv(file).sort_values('aircraft')
    if type == 1:
        return(df[df["operation_type"] == "FLIGHT"])
    elif type == 2:
        return(df[df["operation_type"] == "STATIC"])

# Return aircraft info for specified aircraft (engine, power units, code)
def get_info(df, aircraft):
    return(df[df["aircraft"] == aircraft].iloc[0])

# Write o10 input file, call subprocess to run o10
def run_o10(aircraft = "F-18E/F", power = 90, description = "Cruise", interpolation = "VARIABLE",
                speed_kts = 160, temp = 59, rel_hum_pct = 70, units = "% NC",
                path = "./", input = 'input.o10_input', log = "log.o10_log", 
                output = "output.o10_noise", ac_file = "./data/operation_data.csv"):

    ac_data = pd.read_csv(ac_file)
    
    # Find the corresponding code for aircraft in codes list file
    code  = pd.unique(ac_data[ac_data["aircraft"] == aircraft]["aircraft_code"]).item()
    
    # Pad params with spaces so they fit the Omega10 input format
    t = " " * (4 - len(str(temp))) + str(temp)
    r = " " * (4 - len(str(rel_hum_pct))) + str(rel_hum_pct)
    p = " " * (10 - len(format(power, '.2f'))) + format(power, '.2f')
    u = units + " " * (10 - len(units))
    n = interpolation + " " * (8 - len(interpolation)) 
    s = " " * (3 - len(str(speed_kts))) + str(speed_kts)
    
    # Concatenate params into string
    cmd = "\n{}{}{} W  1  0.0\nF{}00{} {} {}   {}\n" \
        .format(code, t, r, code, p, u, n, s)
   
    os.chdir("./omega/")
   
    # Write o10_input file
    with open(path + input, 'w') as file:
        file.write(cmd)
        file.close()
    
    # Run omega10
    subprocess.Popen(["omega10", input, log, output]).wait()
    os.chdir("..")
    print(os.getcwd())
    return(output)
        

# Read o10 output file, return a dataframe
def read_o10(file = "./omega/output.o10_noise"):
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

def run_o11(aircraft = "F-18E/F", power = 90, description = "Cruise", interpolation = "VARIABLE",
                inches_hg = 29.92, temp = 59, rel_hum_pct = 70, units = "% NC",
                path = "./", input = 'input.o11_input', log = "log.o11_log", 
                output = "output.o11_noise", ac_file = "./data/operation_data.csv"):
    
    ac_data = pd.read_csv(ac_file)
   
    # Find the corresponding code for aircraft in codes list file
    code  = pd.unique(ac_data[ac_data["aircraft"] == aircraft]["aircraft_code"]).item() # read csv, get code of aircraft
    
    # Pad params with spaces so they fit the Omega11 input format
    t = " " * (4 - len(str(temp))) + str(temp)
    r = " " * (5 - len(str(rel_hum_pct))) + str(rel_hum_pct)
    i = " " * (6 - len(str(inches_hg))) + str(inches_hg)
    p = " " * (10 - len(format(power, '.2f'))) + format(power, '.2f')
    u = units + " " * (10 - len(units))
    n = interpolation + " " * (8 - len(interpolation)) 
    
    # Concatenate params into string
    command = "\n{}{}{}{}   W    1 0.0\nR{}00{} {} {}\n" \
        .format(code, t, r, i, code, p, u, n)
   
    os.chdir("./omega/")
    
    #Write o11_input file
    with open(path + input, 'w') as file:
        file.write(command)
        file.close()
    
    # Run omega11
    subprocess.Popen(["omega11", input, log, output]).wait()
    os.chdir("..")
    return(output)

def read_o11(file = "./omega/output.o11_noise"):
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
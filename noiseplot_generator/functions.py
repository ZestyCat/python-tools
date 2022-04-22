import pandas as pd
import subprocess

# Miscellaneous functions to make the gui work

def list_aircraft(file = "./data/noisefile.csv"):
    csv = pd.read_csv(file)
    ac  = csv[csv.retired == False].ac.unique()
    return(ac)

def get_info(aircraft, file = "./data/noisefile.csv"):
    csv = pd.read_csv(file)
    power = csv[csv.ac == aircraft].iloc[1].power
    percent = "%" in power
    units = power.split(" ")[-1][:-1] if not percent else \
            "% "+ power.split(" ")[-1][:-1]
    engine = csv[csv.ac == aircraft].iloc[1].eng
    return({"units" : units, "engine" : engine})

def run_Omega10(aircraft = "F-18E/F", power = 90, description = "Cruise", 
                units = "% NC", speed_kts = "160", temp = 59, rel_hum_pct = 70,
                path = "./", input_file = 'input.o10_input', bat_file = "run_o10.bat", 
                codes = "./data/ac_codes.csv"):

    # Find the corresponding code for aircraft in codes list file
    codes = pd.read_csv(codes)
    code  = codes[codes["aircraft"] == aircraft]["code"].item() # read csv, get code of aircraft

    # Pad params with spaces so they fit the Omega10 input format
    pwr_pad = " " * (10 - len(format(power, '.2f'))) + format(power, '.2f')
    units_pad = units + " " * (10 - len(units))
    speed_pad = " " * (3 - len(str(speed_kts))) + str(speed_kts)
    
    # Concatenate params into string
    command = "\n{}  {}   {} W  1  0.0\nF{}00{} {} VARIABLE   {}\n" \
        .format(code, temp, rel_hum_pct, code, pwr_pad, units_pad, speed_kts)
   
    # Write o10_input file
    with open(path + input_file, 'w') as file:
        file.write(command)

    # Write the batch file
    with open(path + bat_file, 'w') as file:
        file.write('omega10 {} log.o10_log output.o10_noise'.format(input_file))
    
    # Run the batch file
    subprocess.call([path + bat_file])


path = "/mnt/c/Users/gregory.bizup/Documents/AESO/Noise/84 noise report/presentation/"
run_Omega10(path = path)

import pandas as pd

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

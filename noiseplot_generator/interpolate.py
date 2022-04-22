import pandas as pd

def test_func():
    print("Module loaded")

def interpolate(file = "./data/noisefile.csv", ac = "A-3", eng = "J57-P-10", 
                pwr = 90, desc = "Cruise", units = "% RPM", spd = "160 kts."):
    """Interpolates between every noise value at a given power setting"""
    df = pd.read_csv(file)
    df = df[df.ac == ac]
   
    if (pwr < min(set(df.ps_num))) | (pwr > max(set(df.ps_num))):
        n = min(set(df.ps_num))
        x = max(set(df.ps_num))
        return("A power setting you entered is out of range for the {}.\nUse a value between {} and {}.".format(ac, n, x))

    # If power setting already has data, return that and do not interpolate
    if pwr in list(df.ps_num):
        y = pd.DataFrame( \
            {"ac"   : ac,
             "eng"  : eng,
             "pwr"  : pwr,
             "desc" : desc,
             "unit" : units,
             "spd"  : spd,
             "dist" : sorted(list(set(df["Dist ft."]))), 
             "lmax" : df[df.ps_num == pwr]["ALM A-G (dB)"], 
             "sel"  : df[df.ps_num == pwr]["SEL A-G (dB)"]})
        return(y.reset_index())
    else:
        # Find the closest vals in ps_num greater than and less than pwr
        b = sorted([p for p in set(df.ps_num) if p > pwr])[0], \
            sorted([p for p in set(df.ps_num) if p < pwr])[-1]
        print(b)
        # Dataframe tuple for ps_num == b[0] and ps_num == b[1]
        d = df[(df.ps_num == b[0])].reset_index(), \
            df[(df.ps_num == b[1])].reset_index()

        # Find the slope between the two lmax sets
        m = {"lmax" : (d[1]["ALM A-G (dB)"] - d[0]["ALM A-G (dB)"]) / 
                      (d[1].ps_num - d[0].ps_num),                    
             "sel"  : (d[1]["SEL A-G (dB)"] - d[0]["SEL A-G (dB)"]) / 
                      (d[1].ps_num - d[0].ps_num)}

        # Linear inerpolation from m and pwr
        y = pd.DataFrame( \
            {"ac"   : ac,
             "eng"  : eng,
             "pwr"  : pwr,
             "desc" : desc,
             "unit" : units,
             "spd"  : spd,
             "dist" : sorted(list(set(df["Dist ft."]))), 
             "lmax" : -m["lmax"] * (d[0].ps_num - pwr) + d[0]["ALM A-G (dB)"], 
             "sel"  : -m["sel"]  * (d[0].ps_num - pwr) + d[0]["SEL A-G (dB)"]})
        
        return(y)

# # -*- coding: utf-8 -*-
# """
# Created on Mon Jan 24 09:57:30 2022

# @author: AESO 1
# """
# import pandas as pd
# # What percent of the noise data in flight01.dat is estimated?

# # Meas = 0
# # Est = 0

# # with open('C:/Noisemap/NMap/flight01.dat') as file:
    # # for i, line in enumerate(file):
        # # if (i + 4) % 5 == 0: # Get the second out of every fifth line
            # # if "MEASURED" in line:
                # # Meas += 1
            # # if "ESTIMATED" in line:
                # # Est += 1
                
# #Est_pct = 100 * (Est / Meas)

# #print(Est_pct)

# # Expected output: 15.275994865211809

# with open('flight01.dat') as file:
    # lines = file.readlines()
    # data = {"code"     : [],
            # "aircraft" : [],
            # "engine"   : [],
            # "units"    : []}
    # for i, line in enumerate(lines):
        # if i % 5 == 0:
            # data["code"].append(line[10:16])
        # if i % 5 == 1:
            # data["aircraft"].append(" ".join(line.split()).split()[0])
            # data["engine"].append(" ".join(line.split()).split()[1])
        # if i % 5 == 2:
            # data["units"].append(line[30:40].strip())
    # df = pd.DataFrame(data).drop_duplicates().reset_index(drop = True)
    # print(df)
    # df.to_csv("./data/acdata.csv")
    
# #info = pd.read_csv("C:/Users/AESO 1/Documents/GitHub/python-tools/noiseplot_generator/data/ac_info.csv")
# #codes = pd.read_csv("C:/Users/AESO 1/Documents/GitHub/python-tools/noiseplot_generator/data/ac_codes.csv")
# #data = pd.merge(codes[["code", "aircraft"]], info[["aircraft", "engine", "units"]], on = "aircraft", how = "inner")
# #data.to_csv("ac_list.csv")
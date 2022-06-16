import re
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator)

def fmt_plot(ax):
    plt.grid(axis='x', which='minor', color='0.85', linewidth=0.3)
    plt.grid(axis='x', color='0.8', linewidth=0.5)
    plt.grid(axis='y', which='minor', color='0.85', linewidth=0.3)
    plt.grid(axis='y', color='0.8', linewidth=0.5)
    plt.xticks(fontsize=8,                                            
        ticks=[0, 5000, 10000, 15000, 20000, 25000],                  
        labels=['0', '5,000', '10,000', '15,000', '20,000', '25,000'])
    plt.xlabel('Slant distance (ft.)', fontsize=8)
    plt.ylabel('SEL & LAMAX (dB)')
    plt.yticks(fontsize=8)
    plt.xlim(0, 26000)
    plt.ylim(20, 140)
    ax.xaxis.set_minor_locator(MultipleLocator(1000))
    ax.yaxis.set_minor_locator(MultipleLocator(10))
    ax.set_facecolor('#f8f8ff')

def fmt_title(ax, df, df_2 = None, ps_name = None, spd = 160):
    # Construct power setting string based on arguments
    power = "{} ({} - {}{})".format(ps_name, df.pwr[0], 
                                        df_2.pwr[0], df.unit[0])           \
            if ps_name is not None and df_2 is not None else               \
            "{} ({} - {}{})".format(df.desc[0], df.pwr[0], 
                                        df_2.pwr[0], df.unit[0])           \
            if ps_name is None and df_2 is not None else                   \
            "{} ({}{})".format(ps_name, df.pwr[0], df.unit[0])           \
            if ps_name is not None and df_2 is None else                   \
            "{} ({}{})".format(df.desc[0], df.pwr[0], df.unit[0])        
    power = re.sub("%", "\\%", power) # Escape special characters
    power = re.sub(" ", "\\ ", power)
    title_1 = r"$\bf{" + df.ac[0]     + "}$" + '\n' + df.eng[0]
    title_2 = r"$\bf{" + power + "}$" + '\n' + str(spd) + " kts."
    ax.set_title(title_1, pad=8, loc='left',fontsize=10)
    ax.set_title(title_2, pad=8, loc='right',fontsize=10)  

def fmt_leg(ax, df_1 = None, df_2 = None):
    leg = ax.legend(["SEL ({}{})".format(df_1.pwr[0], df_1.unit[0]),       \
                     "LAMAX ({}{})".format(df_1.pwr[0], df_1.unit[0]),     \
                     "SEL ({}{})".format(df_2.pwr[0], df_2.unit[0]),       \
                     "LAMAX ({}{})".format(df_2.pwr[0], df_2.unit[0])],    \
                     fontsize = 7, ncol = 2)                               \
                     if df_1 is not None and df_2 is not None else         \
                     ax.legend(["LMAX", "SEL"], fontsize = 8)
    leg.set_title("Noise metric", prop = {"size" : 8})
    leg.get_frame().set_edgecolor("black")

def plot(df, df_2 = None, ps_name = None, save_name = None, spd = 160): #df from interpolate()
    fig, ax = plt.subplots()
    if df_2 is not None: # If two dataframes are detected, make a filled plot
        plt.plot(df.dist, df.sel, "C0-", df.dist, df.lmax, "C1-",
            lw = 0.7, markerfacecolor = 'none', markeredgewidth = 0.7, ms = 4)
        plt.plot(df_2.dist, df_2.sel, "C0--", df_2.dist, df_2.lmax, "C1--",
            lw = 0.7, markerfacecolor = 'none', markeredgewidth = 0.7, ms = 4)
        ax.fill_between(df.dist, df.sel,  df_2.sel, color = "C0",  alpha=0.5, zorder=3)
        ax.fill_between(df.dist, df.lmax, df_2.lmax, color= "C1", alpha=0.5, zorder=3)    
    else: # Else just make a line plot
        plt.plot(df.dist, df.lmax, "o-", df.dist, df.sel, "x-", linewidth = 0.7,
             markerfacecolor = 'none', markeredgewidth = 0.7, ms = 4)
    fmt_plot(ax)
    fmt_title(ax, df, df_2, ps_name = ps_name, spd = spd)
    fmt_leg(ax, df, df_2)
    if save_name:
        plt.savefig(save_name, bbox_inches = 'tight', dpi = 500)
    return(fig)

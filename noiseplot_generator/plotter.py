from interpolate import *
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator)

df_1 = interpolate("./data/noisefile.csv", ac = "F-35B", eng = "F135-PW-600", desc = "Cruise", units = "\ EPR", pwr = 95)
df_2 = interpolate("./data/noisefile.csv", ac = "F-35B", eng = "F135-PW-600", desc = "Cruise", units = "\ EPR", pwr = 135)

def format_plot(ax):
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

def format_title(ax, ac, eng, desc, pwr, unit, spd = "160 kts."):
    # Construct power setting string, escape percent if it has one
    power = "{}\ ({}\{})".format(desc, str(pwr), unit)   \
             if "%" in unit else                         \
            "{}\ ({}{})".format(desc, str(pwr), unit)

    title_1 = r"$\bf{" + ac    + "}$" + '\n' + eng
    title_2 = r"$\bf{" + power + "}$" + '\n' + spd
    ax.set_title(title_1, pad=8, loc='left',fontsize=10)
    ax.set_title(title_2, pad=8, loc='right',fontsize=10)  

def plot_line(df): # Takes df returned by interpolate(). power as string
    fig, ax = plt.subplots()
    plt.plot(df.dist, df.lmax, "o-", df.dist, df.sel, "x-", linewidth = 0.7,
             markerfacecolor = 'none', markeredgewidth = 0.7, ms = 4)
    format_plot(ax, df)
    format_title(ax, df.ac[0], df.eng[0], df.desc[0], df.pwr[0], df.unit[0])
    return(fig)

def plot_filled(df_1, df_2):
    fig, ax = plt.subplots()
    plt.plot(df_1.dist, df_1.sel, "C0-", df_1.dist, df_1.lmax, "C1-",
             lw = 0.7, markerfacecolor = 'none', markeredgewidth = 0.7, ms = 4)
    plt.plot(df_2.dist, df_2.sel, "C0--", df_2.dist, df_2.lmax, "C1--",
             lw = 0.7, markerfacecolor = 'none', markeredgewidth = 0.7, ms = 4)
    ax.fill_between(df_1.dist, df_1.sel,  df_2.sel,  alpha=0.5, zorder=3)
    ax.fill_between(df_1.dist, df_1.lmax, df_2.lmax, alpha=0.5, zorder=3)    
    format_plot(ax)
    return(fig)

def save_plot(name):
    plt.savefig(name, bbox_inches = 'tight', dpi = 500)

b = plot_filled(df_1, df_2)
b.show()

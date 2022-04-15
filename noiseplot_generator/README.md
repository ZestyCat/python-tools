This program generates aircraft noise plots.

The plots compare slant distance with noise from an aircraft operating at a given power setting.

Noise is plotted using two metrics: 
    1. Sound Exposure level (SEL) 
    2. Maximum Sound Level (LAMAX)

The program calculates noise from the NOISEMAP input data.
Results from this program are identical to those produced by the DoD Omega10 model.
Unfortunately, the Omega10 model is cumbersome to operate and not very user-friendly.
This program provides a quick and easy user interface that anyone can use.
The NOISEMAP input data consists of discrete noise measurements for each aircraft at various power settings.
Each aircraft has a limited number of noise data points associated with it.
Linear interpolation is used to generate noise data between noise measurements of different power settings.

These are the basic steps of the calculation performed:
    1. Get user input for the desired power setting
    2. Find the measured data points with the next lowest and next highest power setting to the user input
    3. Calculate the slope between the data points
    

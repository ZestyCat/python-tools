This program generates aircraft noise plots.

The plots compare slant distance with noise from an aircraft operating at a given power setting.

Noise is plotted using two metrics: 
    1. Sound Exposure level (SEL) 
    2. Maximum Sound Level (LAMAX)

Predict and plot aircraft noise at any given power setting.
Noise metrics are calculated at each slant distance by interpolating over disparate measured data points from the NOISEMAP input data.
This accomplishes the same end goal as running the the NOISEMAP preprocessor, Omega10.
For quality assurance, results from this program have proven to be identical to those from Omega10.
Unfortunately, the Omega10 preprocessor is cumbersome to operate unfriendly for quick use.
Moreover, plotting the data to AESO specifications requires some prior experience with Python.
This program provides an easy-to-use and repeatable solution to the problem.

The basic concept of the calculation is described below:
    1. The input data file contains noise data for a handful of aircraft, each aircraft having data for a few power settings. 
       The noise data is reported in LMAX and SEL, at distances ranging from 200 to 25,000 feet.
    2. Each aircraft only has a few power settings associated with it. Linear interpolation is used
       to determine noise data for unspecified power settings. For example, if one aircraft only has noise data
       for 50% RPM, 80% RPM, and 95% RPM, how are we supposed to determine the noise when the aircraft is running at 87% RPM?

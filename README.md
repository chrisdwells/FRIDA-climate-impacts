This repository is to contain any processing needed related to multiple climate impacts in FRIDA.

Currently for FRIDAv2.1:

collate_parameter_sets.py collates the uncertainty parameter sets for the climate impacts which are
literature-derived with uncertainty.

plot_damage_functions.py plots a multipanel of the damage functions, for Figure 2 in the climate impacts documentation paper.

The output pickle files need to be brought in from the repos which produce them for each impact separately:
https://github.com/chrisdwells/climate-energy-supply
https://github.com/chrisdwells/temperature-mortality
https://github.com/chrisdwells/extremes-exposure

The code here assumes these repos are kept in the same place as this one.
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab

import pandas as pd
import pickle
import numpy as np
import string
string.ascii_lowercase

from matplotlib import font_manager


# For combined Figure 1 in the climate impacts documentation paper

# some have "sampled percentiles", others just on 3 levels, with
# uncertainty ranges internally calibrated


font_path = r"C:\Users\earcwel\AppData\Local\Microsoft\Windows\Fonts\OpenSans-VariableFont_wdth,wght.ttf"
font_manager.fontManager.addfont(font_path)
prop = font_manager.FontProperties(fname=font_path)

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = prop.get_name()

fontsize = 18

plt.rcParams.update({'font.size': fontsize})
params = {'legend.fontsize': fontsize,
         'axes.labelsize': fontsize,
         'axes.titlesize':fontsize,
         'xtick.labelsize':fontsize,
         'ytick.labelsize':fontsize}
pylab.rcParams.update(params)

ytext_x = -0.06
ytext_y = 0.5
xtext_x = 0.5
xtext_y = -0.07

ctext_x_left = 0.01
ctext_x_right = 0.99

ctext_y_bot = 0.05
ctext_y_top = 0.93

params_in = pd.read_csv('../data/sampleParmsParscaleRanged.csv')
params_in = params_in[['Variable', 'Value', 'Min', 'Max']]


percentiles = np.linspace(0.025, 0.975, 11)

colors_p = {p:'grey' for p in percentiles}
colors_p[0.5] = 'red'
zorders_p = {p:1 for p in percentiles}
zorders_p[0.5] = 2


levels = ['low', 'medium', 'high']

colors_l = {l:'grey' for l in levels}
colors_l['medium'] = 'red'
zorders_l = {l:1 for l in levels}
zorders_l['medium'] = 2


sta_plot = np.linspace(0, 4.5, 50)
abs_t_plot = np.linspace(14, 20, 50)
co2_plot = np.linspace(400, 800, 50)
co2_plot_cf1980 = co2_plot - co2_plot[0]


#%%

fig, axs = plt.subplots(1, 1, figsize=(4, 4))

i = 0

# Crops

T_fix = 15
CO2_fix = 400
T_fix_sta = 0

param_file = '../../climate-crops-impacts/data/outputs/crops_output_dict.pickle'
with open(param_file, 'rb') as handle:
    pkl_in = pickle.load(handle)

assert pkl_in['Percentiles'].all() == percentiles.all()

a = pkl_in['Crop.rel change in crop productivity intercept[1]']
b = pkl_in['Crop.crop prod linear temp effect[1]']
c = pkl_in['Crop.crop prod squared temp effect[1]']
d = pkl_in['Crop.crop prod linear CO2 effect[1]']

for p_i, perc in enumerate(percentiles):
    resp = a[p_i] + b[p_i]*abs_t_plot + c[p_i]*abs_t_plot**2 + d[p_i]*CO2_fix
    plt.plot(abs_t_plot, resp, color=colors_p[perc], zorder=zorders_p[perc])
    

plt.xticks(ticks=[plt.xticks()[0][1], plt.xticks()[0][-2]], labels = [plt.xticks()[1][1], plt.xticks()[1][-2]])
plt.yticks(ticks=[plt.yticks()[0][1], plt.yticks()[0][-2]], labels = [plt.yticks()[1][1], plt.yticks()[1][-2]])

plt.text(ytext_x, ytext_y, '% prod. change', transform=axs.transAxes, rotation=90, 
     horizontalalignment='center', verticalalignment='center')

plt.text(xtext_x, xtext_y, r'Abs. Temp. ($^{\circ}$C)', transform=axs.transAxes,
     horizontalalignment='center', verticalalignment='center')

plt.text(ctext_x_left, ctext_y_bot, fr'CO$_{2}$ = {CO2_fix} ppm', transform=axs.transAxes,
     horizontalalignment='left', verticalalignment='center')


plt.tight_layout()
plt.savefig(
    "../figures/separate/figure2_crops_tas.png", dpi=100, transparent=True
)
plt.clf()

#%%

fig, axs = plt.subplots(1, 1, figsize=(4, 4))



for p_i, perc in enumerate(percentiles):
    resp = a[p_i] + b[p_i]*T_fix + c[p_i]*T_fix**2 + d[p_i]*co2_plot
    plt.plot(co2_plot, resp, color=colors_p[perc], zorder=zorders_p[perc])
    
plt.xticks(ticks=[plt.xticks()[0][1], plt.xticks()[0][-2]], labels = [plt.xticks()[1][1], plt.xticks()[1][-2]])
plt.yticks(ticks=[plt.yticks()[0][1], plt.yticks()[0][-2]], labels = [plt.yticks()[1][1], plt.yticks()[1][-2]])

plt.text(ytext_x, ytext_y, '% prod. change', transform=axs.transAxes, rotation=90, 
     horizontalalignment='center', verticalalignment='center')

plt.text(xtext_x, xtext_y, r'CO$_{2}$ (ppm)', transform=axs.transAxes,
     horizontalalignment='center', verticalalignment='center')

plt.text(ctext_x_left, ctext_y_top, f'Crops, Temp = {T_fix} ' + r'$^{\circ}$C', transform=axs.transAxes,
     horizontalalignment='left', verticalalignment='center')



plt.tight_layout()
plt.savefig(
    "../figures/separate/figure2_crops_co2.png", dpi=100, transparent=True
)
plt.clf()

#%%

fig, axs = plt.subplots(1, 1, figsize=(4, 4))


# Labour productivity

## Low-exposure


# a = np.asarray([-16, -2.08262027, -5])
# b = np.asarray([-2 , -1.56936859, 0.1])

params_df = params_in.loc[params_in['Variable'] == 'Employment.Temperature effect on low exposure productivity[1]']
a = np.asarray([params_df['Min'], params_df['Value'], params_df['Max']])

params_df = params_in.loc[params_in['Variable'] == 'Employment.Temperature squared effect on low exposure productivity[1]']
b = np.asarray([params_df['Min'], params_df['Value'], params_df['Max']])




for l_i, lev in enumerate(levels):
    resp = a[l_i]*sta_plot + b[l_i]*sta_plot**2
    plt.plot(sta_plot, resp, color=colors_l[lev], zorder=zorders_l[lev])
    

plt.xticks(ticks=[plt.xticks()[0][1], plt.xticks()[0][-2]], labels = [plt.xticks()[1][1], plt.xticks()[1][-2]])
plt.yticks(ticks=[plt.yticks()[0][1], plt.yticks()[0][-2]], labels = [plt.yticks()[1][1], plt.yticks()[1][-2]])

plt.text(ytext_x, ytext_y, '% prod. change', transform=axs.transAxes, rotation=90, 
     horizontalalignment='center', verticalalignment='center')

plt.text(xtext_x, xtext_y, 'STA (K)', transform=axs.transAxes,
     horizontalalignment='center', verticalalignment='center')

plt.text(ctext_x_left, ctext_y_bot, 'Low Exp.', transform=axs.transAxes,
     horizontalalignment='left', verticalalignment='center')




plt.tight_layout()
plt.savefig(
    "../figures/separate/figure2_labour_low.png", dpi=100, transparent=True
)
plt.clf()

#%%

fig, axs = plt.subplots(1, 1, figsize=(4, 4))


## High-exposure


# a = np.asarray([-25, -6.13282138, -4])
# b = np.asarray([-1.5, -1.06197873, -1])

params_df = params_in.loc[params_in['Variable'] == 'Employment.Temperature effect on high exposure productivity[1]']
a = np.asarray([params_df['Min'], params_df['Value'], params_df['Max']])

params_df = params_in.loc[params_in['Variable'] == 'Employment.Temperature squared effect on high exposure productivity[1]']
b = np.asarray([params_df['Min'], params_df['Value'], params_df['Max']])


for l_i, lev in enumerate(levels):
    resp = a[l_i]*sta_plot + b[l_i]*sta_plot**2
    plt.plot(sta_plot, resp, color=colors_l[lev], zorder=zorders_l[lev])
    
plt.xticks(ticks=[plt.xticks()[0][1], plt.xticks()[0][-2]], labels = [plt.xticks()[1][1], plt.xticks()[1][-2]])
plt.yticks(ticks=[plt.yticks()[0][1], plt.yticks()[0][-2]], labels = [plt.yticks()[1][1], plt.yticks()[1][-2]])

plt.text(ytext_x, ytext_y, '% prod. change', transform=axs.transAxes, rotation=90, 
     horizontalalignment='center', verticalalignment='center')

plt.text(xtext_x, xtext_y, 'STA (K)', transform=axs.transAxes,
     horizontalalignment='center', verticalalignment='center')

plt.text(ctext_x_left, ctext_y_bot, 'High Exp.', transform=axs.transAxes,
     horizontalalignment='left', verticalalignment='center')



plt.tight_layout()
plt.savefig(
    "../figures/separate/figure2_labour_high.png", dpi=100, transparent=True
)
plt.clf()

#%%
fig, axs = plt.subplots(1, 1, figsize=(4, 4))


# Energy Supply

param_file = '../../climate-energy-supply/data/outputs/energy_suppy_output_dict.pickle'
with open(param_file, 'rb') as handle:
    pkl_in = pickle.load(handle)

assert pkl_in['Percentiles'].all() == percentiles.all()

## Thermoelectric



a = pkl_in['efficiency reduction in power plants.effect of STA on river cooled thermal powerplant energy capacity efficiency slope[1]']
b = pkl_in['efficiency reduction in power plants.effect of STA on river cooled thermal power energy capacity efficiency quadratic[1]']

for p_i, perc in enumerate(percentiles):
    resp = a[p_i]*sta_plot + b[p_i]*sta_plot**2
    plt.plot(sta_plot, resp, color=colors_p[perc], zorder=zorders_p[perc])
    
plt.title('Thermoelectric')
plt.ylabel('% efficiency change')
plt.xlabel('STA (K)')  

plt.tight_layout()
plt.savefig(
    "../figures/separate/figure2_thermo.png", dpi=100, transparent=True
)
plt.clf()

#%%
fig, axs = plt.subplots(1, 1, figsize=(4, 4))

## Hydroelectric



a = pkl_in['efficiency reduction in power plants.effect of STA on hydropower energy capacity efficiency slope[1]']
b = pkl_in['efficiency reduction in power plants.effect of STA on hydropower energy capacity efficiency quadratic[1]']

for p_i, perc in enumerate(percentiles):
    resp = a[p_i]*sta_plot + b[p_i]*sta_plot**2
    plt.plot(sta_plot, resp, color=colors_p[perc], zorder=zorders_p[perc])
    
plt.title('Hydroelectric')
plt.ylabel('% efficiency change')
plt.xlabel('STA (K)')  

plt.tight_layout()
plt.savefig(
    "../figures/separate/figure2_hydro.png", dpi=100, transparent=True
)
plt.clf()

#%%
fig, axs = plt.subplots(1, 1, figsize=(4, 4))

# Energy Demand

## CDD


a = 704.2
# b = np.asarray([230, 287.8469604, 330])

params_df = params_in.loc[params_in['Variable'] == 'energy demand.CDD linear coefficient[1]']
b = np.asarray([params_df['Min'], params_df['Value'], params_df['Max']])

for l_i, lev in enumerate(levels):
    resp = a + b[l_i]*sta_plot
    plt.plot(sta_plot, resp, color=colors_l[lev], zorder=zorders_l[lev])
    
plt.xticks(ticks=[plt.xticks()[0][1], plt.xticks()[0][-2]], labels = [plt.xticks()[1][1], plt.xticks()[1][-2]])
plt.yticks(ticks=[plt.yticks()[0][1], plt.yticks()[0][-2]], labels = [plt.yticks()[1][1], plt.yticks()[1][-2]])

plt.text(ytext_x, ytext_y, 'CDD', transform=axs.transAxes, rotation=90, 
     horizontalalignment='center', verticalalignment='center')

plt.text(xtext_x, xtext_y, 'STA (K)', transform=axs.transAxes,
     horizontalalignment='center', verticalalignment='center')

plt.tight_layout()
plt.savefig(
    "../figures/separate/figure2_cdd.png", dpi=100, transparent=True
)
plt.clf()

#%%
fig, axs = plt.subplots(1, 1, figsize=(4, 4))


## HDD

a = 1376
# b = np.asarray([-0.5, -0.232561095, -0.01])

params_df = params_in.loc[params_in['Variable'] == 'energy demand.HDD exponential coefficient[1]']
b = np.asarray([params_df['Min'], params_df['Value'], params_df['Max']])


for l_i, lev in enumerate(levels):
    resp = a*np.exp(b[l_i]*sta_plot)
    plt.plot(sta_plot, resp, color=colors_l[lev], zorder=zorders_l[lev])
    
plt.xticks(ticks=[plt.xticks()[0][1], plt.xticks()[0][-2]], labels = [plt.xticks()[1][1], plt.xticks()[1][-2]])
plt.yticks(ticks=[plt.yticks()[0][1], plt.yticks()[0][-2]], labels = [plt.yticks()[1][1], plt.yticks()[1][-2]])

plt.text(ytext_x, ytext_y, 'HDD', transform=axs.transAxes, rotation=90, 
     horizontalalignment='center', verticalalignment='center')

plt.text(xtext_x, xtext_y, 'STA (K)', transform=axs.transAxes,
     horizontalalignment='center', verticalalignment='center')

plt.tight_layout()
plt.savefig(
    "../figures/separate/figure2_hdd.png", dpi=100, transparent=True
)
plt.clf()

#%%
fig, axs = plt.subplots(1, 1, figsize=(4, 4))


# Mortality

param_file = '../../temperature-mortality/data/outputs/mortality_output_dict.pickle'
with open(param_file, 'rb') as handle:
    pkl_in = pickle.load(handle)

assert pkl_in['Percentiles'].all() == percentiles.all()

## Cold



a = pkl_in['Demographics.Cold mortality sensitivity to T[1]']
b = pkl_in['Demographics.Cold mortality sensitivity to T2[1]']

for p_i, perc in enumerate(percentiles):
    resp = a[p_i]*sta_plot + b[p_i]*sta_plot**2
    plt.plot(sta_plot, resp, color=colors_p[perc], zorder=zorders_p[perc])
    
plt.title('Cold Mortality')
plt.ylabel('% change')
plt.xlabel('STA (K)')  

plt.tight_layout()
plt.savefig(
    "../figures/separate/figure2_mort_cold.png", dpi=100, transparent=True
)
plt.clf()

#%%
fig, axs = plt.subplots(1, 1, figsize=(4, 4))


## Hot



a = pkl_in['Demographics.Hot mortality sensitivity to T[1]']
b = pkl_in['Demographics.Hot mortality sensitivity to T2[1]']

for p_i, perc in enumerate(percentiles):
    resp = a[p_i]*sta_plot + b[p_i]*sta_plot**2
    plt.plot(sta_plot, resp, color=colors_p[perc], zorder=zorders_p[perc])
    
plt.title('Hot Mortality')
plt.ylabel('% change')
plt.xlabel('STA (K)')  

plt.tight_layout()
plt.savefig(
    "../figures/separate/figure2_mort_hot.png", dpi=100, transparent=True
)
plt.clf()

#%%
fig, axs = plt.subplots(1, 1, figsize=(4, 4))



# Extremes Exposure

param_file = '../../extremes-exposure/data/outputs/exposure_output_dict.pickle'

with open(param_file, 'rb') as handle:
    pkl_in = pickle.load(handle)

assert pkl_in['Percentiles'].all() == percentiles.all()



a = pkl_in['Energy Balance Model.T effect on population exposure to record breaking indices[1]']
b = pkl_in['Energy Balance Model.T2 effect on population exposure to record breaking indices[1]']

for p_i, perc in enumerate(percentiles):
    resp = a[p_i]*sta_plot + b[p_i]*sta_plot**2
    plt.plot(sta_plot, resp, color=colors_p[perc], zorder=zorders_p[perc])
    
plt.title('Extremes Exposure')
plt.ylabel('Per person per year')
plt.xlabel('STA (K)')  

plt.tight_layout()
plt.savefig(
    "../figures/separate/figure2_extremes_exposure.png", dpi=100, transparent=True
)
plt.clf()

#%%
fig, axs = plt.subplots(1, 1, figsize=(4, 4))


# Loan failure


# a = np.asarray([0.1, 0.580674151, 1.1])

params_df = params_in.loc[params_in['Variable'] == 'Finance.sensitivity of effect of sta on failure rate[1]']
a = np.asarray([params_df['Min'], params_df['Value'], params_df['Max']])

for l_i, lev in enumerate(levels):
    resp = 1 + a[l_i]*sta_plot
    plt.plot(sta_plot, resp, color=colors_l[lev], zorder=zorders_l[lev])
    
plt.xticks(ticks=[plt.xticks()[0][1], plt.xticks()[0][-2]], labels = [plt.xticks()[1][1], plt.xticks()[1][-2]])
plt.yticks(ticks=[plt.yticks()[0][1], plt.yticks()[0][-2]], labels = [plt.yticks()[1][1], plt.yticks()[1][-2]])

plt.text(ytext_x, ytext_y, 'Scaling factor', transform=axs.transAxes, rotation=90, 
     horizontalalignment='center', verticalalignment='center')

plt.text(xtext_x, xtext_y, 'STA (K)', transform=axs.transAxes,
     horizontalalignment='center', verticalalignment='center')

plt.tight_layout()
plt.savefig(
    "../figures/separate/figure2_loan_failure.png", dpi=100, transparent=True
)
plt.clf()

#%%
fig, axs = plt.subplots(1, 1, figsize=(4, 4))

# Government spending

# a = np.asarray([0, 0.068134916, 0.2])

params_df = params_in.loc[params_in['Variable'] == 'Government.sensitivity of STA on public consumption[1]']
a = np.asarray([params_df['Min'], params_df['Value'], params_df['Max']])

for l_i, lev in enumerate(levels):
    resp = 1 + a[l_i]*sta_plot
    plt.plot(sta_plot, resp, color=colors_l[lev], zorder=zorders_l[lev])
    
plt.xticks(ticks=[plt.xticks()[0][1], plt.xticks()[0][-2]], labels = [plt.xticks()[1][1], plt.xticks()[1][-2]])
plt.yticks(ticks=[plt.yticks()[0][1], plt.yticks()[0][-2]], labels = [plt.yticks()[1][1], plt.yticks()[1][-2]])

plt.text(ytext_x, ytext_y, 'Scaling factor', transform=axs.transAxes, rotation=90, 
     horizontalalignment='center', verticalalignment='center')

plt.text(xtext_x, xtext_y, 'STA (K)', transform=axs.transAxes,
     horizontalalignment='center', verticalalignment='center')


plt.tight_layout()
plt.savefig(
    "../figures/separate/figure2_govt_spending.png", dpi=100, transparent=True
)
plt.clf()

#%%
fig, axs = plt.subplots(1, 1, figsize=(4, 4))


# Evapotranspiration



# a = np.asarray([0.02, 0.064352435, 0.1])

params_df = params_in.loc[params_in['Variable'] == 'Freshwater.sensitivity of surface temperature anomaly on water used per Mtcrop[1]']
a = np.asarray([params_df['Min'], params_df['Value'], params_df['Max']])

for l_i, lev in enumerate(levels):
    resp = 1 + a[l_i]*sta_plot
    plt.plot(sta_plot, resp, color=colors_l[lev], zorder=zorders_l[lev])
    

plt.xticks(ticks=[plt.xticks()[0][1], plt.xticks()[0][-2]], labels = [plt.xticks()[1][1], plt.xticks()[1][-2]])
plt.yticks(ticks=[plt.yticks()[0][1], plt.yticks()[0][-2]], labels = [plt.yticks()[1][1], plt.yticks()[1][-2]])

plt.text(ytext_x, ytext_y, 'Scaling factor', transform=axs.transAxes, rotation=90, 
     horizontalalignment='center', verticalalignment='center')

plt.text(xtext_x, xtext_y, 'STA (K)', transform=axs.transAxes,
     horizontalalignment='center', verticalalignment='center')

plt.tight_layout()
plt.savefig(
    "../figures/separate/figure2_evapo.png", dpi=100, transparent=True
)
plt.clf()

#%%
fig, axs = plt.subplots(1, 1, figsize=(4, 4))


# Soil Carbon

# a = np.asarray([40, 60, 60])
# b = np.asarray([290, 290.0287445, 320])

params_df = params_in.loc[params_in['Variable'] == 'soil carbon decay.temp response[1]']
a = np.asarray([params_df['Min'], params_df['Value'], params_df['Max']])

b = 290.0287445

for l_i, lev in enumerate(levels):
    resp = np.exp(b*(1.0/(a[l_i]+10)-1.0/(abs_t_plot+a[l_i])))
    
    plt.plot(abs_t_plot, resp, color=colors_l[lev], zorder=zorders_l[lev])
    

plt.xticks(ticks=[plt.xticks()[0][1], plt.xticks()[0][-2]], labels = [plt.xticks()[1][1], plt.xticks()[1][-2]])
plt.yticks(ticks=[plt.yticks()[0][1], plt.yticks()[0][-2]], labels = [plt.yticks()[1][1], plt.yticks()[1][-2]])

plt.text(ytext_x, ytext_y, 'Scaling factor', transform=axs.transAxes, rotation=90, 
     horizontalalignment='center', verticalalignment='center')

plt.text(xtext_x, xtext_y, r'Abs. Temp. ($^{\circ}$C)', transform=axs.transAxes,
     horizontalalignment='center', verticalalignment='center')

plt.tight_layout()
plt.savefig(
    "../figures/separate/figure2_soil_carbon.png", dpi=100, transparent=True
)
plt.clf()

#%%
fig, axs = plt.subplots(1, 1, figsize=(4, 4))


# Durability of Concrete 


# a = np.asarray([-15, -7.5, -5])

params_df = params_in.loc[params_in['Variable'] == 'Concrete.CLIMATE IMPACT ON CONCRETE LIFETIME[1]']
a = np.asarray([params_df['Min'], params_df['Value'], params_df['Max']])


for l_i, lev in enumerate(levels):
    resp = 1 + 100*a[l_i]*sta_plot
    plt.plot(sta_plot, resp, color=colors_l[lev], zorder=zorders_l[lev])
    
plt.xticks(ticks=[plt.xticks()[0][1], plt.xticks()[0][-2]], labels = [plt.xticks()[1][1], plt.xticks()[1][-2]])
plt.yticks(ticks=[plt.yticks()[0][1], plt.yticks()[0][-2]], labels = [plt.yticks()[1][1], plt.yticks()[1][-2]])

plt.text(ytext_x, ytext_y, '% change', transform=axs.transAxes, rotation=90, 
     horizontalalignment='center', verticalalignment='center')

plt.text(xtext_x, xtext_y, 'STA cf 1980', transform=axs.transAxes,
     horizontalalignment='center', verticalalignment='center')

plt.tight_layout()
plt.savefig(
    "../figures/separate/figure2_concrete.png", dpi=100, transparent=True
)
plt.clf()

#%%
fig, axs = plt.subplots(1, 1, figsize=(4, 4))


# Energy Infrastructure Damage

# a = np.asarray([0, 0.00005096093, 8]) 
# b = np.asarray([1, 2, 3])

params_df = params_in.loc[params_in['Variable'] == 'Damages.Slope of Capital Damage Function[1]']
a = np.asarray([params_df['Min'], params_df['Value'], params_df['Max']])

params_df = params_in.loc[params_in['Variable'] == 'Damages.Exponent of Capital Damage Function[1]']
b = np.asarray([params_df['Min'], params_df['Value'], params_df['Max']])


for l_i, lev in enumerate(levels):
    resp = a[l_i]*sta_plot**b[l_i]
    
    plt.plot(sta_plot, resp, color=colors_l[lev], zorder=zorders_l[lev])
    
plt.xticks(ticks=[plt.xticks()[0][1], plt.xticks()[0][-2]], labels = [plt.xticks()[1][1], plt.xticks()[1][-2]])
plt.yticks(ticks=[plt.yticks()[0][1], plt.yticks()[0][-2]], labels = [plt.yticks()[1][1], plt.yticks()[1][-2]])

plt.text(ytext_x, ytext_y, 'Annual Frac.', transform=axs.transAxes, rotation=90, 
     horizontalalignment='center', verticalalignment='center')

plt.text(xtext_x, xtext_y, 'STA (K)', transform=axs.transAxes,
     horizontalalignment='center', verticalalignment='center')


plt.tight_layout()
plt.savefig(
    "../figures/separate/figure2_energy_infra.png", dpi=100, transparent=True
)
plt.clf()

#%%
fig, axs = plt.subplots(1, 1, figsize=(4, 4))


# Net Primary Production; 2 2d slices, 2 types (4)

## Forest



# a = np.asarray([0.01, 0.125348729, 0.13])
# b = np.asarray([-0.05, -0.023015026, -0.01])
# c = np.asarray([0.0005, 0.001, 0.001])

params_df = params_in.loc[params_in['Variable'] == 'Forest.STA tree net primary production parameter[1]']
a = np.asarray([params_df['Min'], params_df['Value'], params_df['Max']])

params_df = params_in.loc[params_in['Variable'] == 'Forest.STA squared tree net primary production parameter[1]']
b = np.asarray([params_df['Min'], params_df['Value'], params_df['Max']])

params_df = params_in.loc[params_in['Variable'] == 'Forest.CO2 tree net primary production parameter[1]']
c = np.asarray([params_df['Min'], params_df['Value'], params_df['Max']])


for l_i, lev in enumerate(levels):
    resp = a[l_i]*sta_plot + b[l_i]*sta_plot**2 + c[l_i]*0 # CO2 cf 1980
    
    plt.plot(sta_plot, resp, color=colors_l[lev], zorder=zorders_l[lev])
    

plt.xticks(ticks=[plt.xticks()[0][1], plt.xticks()[0][-2]], labels = [plt.xticks()[1][1], plt.xticks()[1][-2]])
plt.yticks(ticks=[plt.yticks()[0][1], plt.yticks()[0][-2]], labels = [plt.yticks()[1][1], plt.yticks()[1][-2]])

plt.text(ytext_x, ytext_y-0.05, 'Frac. Change', transform=axs.transAxes, rotation=90, 
     horizontalalignment='center', verticalalignment='center')

plt.text(xtext_x-0.05, xtext_y, 'STA cf 1980', transform=axs.transAxes,
     horizontalalignment='center', verticalalignment='center')

plt.text(ctext_x_left, ctext_y_bot, fr'Forest; CO$_{2}$ as 1980', transform=axs.transAxes,
     horizontalalignment='left', verticalalignment='center')


plt.tight_layout()
plt.savefig(
    "../figures/separate/figure2_npp_forest_tas.png", dpi=100, transparent=True
)
# plt.clf()

#%%
fig, axs = plt.subplots(1, 1, figsize=(4, 4))



for l_i, lev in enumerate(levels):
    resp = a[l_i]*T_fix_sta + b[l_i]*T_fix_sta**2 + c[l_i]*co2_plot_cf1980
    
    plt.plot(co2_plot_cf1980, resp, color=colors_l[lev], zorder=zorders_l[lev])
    
plt.xticks(ticks=[plt.xticks()[0][1], plt.xticks()[0][-2]], labels = [plt.xticks()[1][1], plt.xticks()[1][-2]])
plt.yticks(ticks=[plt.yticks()[0][1], plt.yticks()[0][-2]], labels = [plt.yticks()[1][1], plt.yticks()[1][-2]])

plt.text(ytext_x, ytext_y, 'Frac. Change', transform=axs.transAxes, rotation=90, 
     horizontalalignment='center', verticalalignment='center')

plt.text(xtext_x, xtext_y, f'CO$_{2}$ cf 1980 (ppm)', transform=axs.transAxes,
     horizontalalignment='center', verticalalignment='center')

plt.text(ctext_x_left, ctext_y_top, 'Forest; STA as 1980', transform=axs.transAxes,
     horizontalalignment='left', verticalalignment='center')


plt.tight_layout()
plt.savefig(
    "../figures/separate/figure2_npp_forest_co2.png", dpi=100, transparent=True
)
plt.clf()

#%%
fig, axs = plt.subplots(1, 1, figsize=(4, 4))


## Grass



a = np.asarray([0.01, 0.126281692, 0.13])
b = np.asarray([-0.05, -0.034654395, -0.01])
c = np.asarray([0.0005, 0.000963654, 0.001])

for l_i, lev in enumerate(levels):
    resp = a[l_i]*sta_plot + b[l_i]*sta_plot**2 + c[l_i]*0 # CO2 cf 1980
    
    plt.plot(sta_plot, resp, color=colors_l[lev], zorder=zorders_l[lev])
    

plt.xticks(ticks=[plt.xticks()[0][1], plt.xticks()[0][-2]], labels = [plt.xticks()[1][1], plt.xticks()[1][-2]])
plt.yticks(ticks=[plt.yticks()[0][1], plt.yticks()[0][-2]], labels = [plt.yticks()[1][1], plt.yticks()[1][-2]])

plt.text(ytext_x, ytext_y-0.05, 'Frac. Change', transform=axs.transAxes, rotation=90, 
     horizontalalignment='center', verticalalignment='center')

plt.text(xtext_x-0.08, xtext_y, 'STA cf 1980 (K)', transform=axs.transAxes,
     horizontalalignment='center', verticalalignment='center')

plt.text(ctext_x_left, ctext_y_bot, fr'Grass; CO$_{2}$ as 1980', transform=axs.transAxes,
     horizontalalignment='left', verticalalignment='center')


plt.tight_layout()
plt.savefig(
    "../figures/separate/figure2_npp_grass_tas.png", dpi=100, transparent=True
)
plt.clf()

#%%
fig, axs = plt.subplots(1, 1, figsize=(4, 4))


for l_i, lev in enumerate(levels):
    resp = a[l_i]*T_fix_sta + b[l_i]*T_fix_sta**2 + c[l_i]*(co2_plot_cf1980)
    
    plt.plot(co2_plot_cf1980, resp, color=colors_l[lev], zorder=zorders_l[lev])
    
plt.xticks(ticks=[plt.xticks()[0][1], plt.xticks()[0][-2]], labels = [plt.xticks()[1][1], plt.xticks()[1][-2]])
plt.yticks(ticks=[plt.yticks()[0][1], plt.yticks()[0][-2]], labels = [plt.yticks()[1][1], plt.yticks()[1][-2]])

plt.text(ytext_x, ytext_y, 'Frac. Change', transform=axs.transAxes, rotation=90, 
     horizontalalignment='center', verticalalignment='center')

plt.text(xtext_x, xtext_y, f'CO$_{2}$ cf 1980 (ppm)', transform=axs.transAxes,
     horizontalalignment='center', verticalalignment='center')

plt.text(ctext_x_left, ctext_y_top, 'Grass; STA as 1980', transform=axs.transAxes,
     horizontalalignment='left', verticalalignment='center')


plt.tight_layout()
plt.savefig(
    "../figures/separate/figure2_npp_grass_co2.png", dpi=100, transparent=True
)
plt.clf()

#%%
fig, axs = plt.subplots(1, 1, figsize=(4, 4))



# Forest Biomass



a = np.asarray([0.2, 0.253488316, 0.35])
b = np.asarray([-0.08, -0.048709811, -0.02])

for l_i, lev in enumerate(levels):
    resp = a[l_i]*sta_plot + b[l_i]*sta_plot**2
    plt.plot(sta_plot, resp, color=colors_l[lev], zorder=zorders_l[lev])
    

plt.xticks(ticks=[plt.xticks()[0][1], plt.xticks()[0][-2]], labels = [plt.xticks()[1][1], plt.xticks()[1][-2]])
plt.yticks(ticks=[plt.yticks()[0][1], plt.yticks()[0][-2]], labels = [plt.yticks()[1][1], plt.yticks()[1][-2]])

plt.text(ytext_x, ytext_y, 'Scaling factor', transform=axs.transAxes, rotation=90, 
     horizontalalignment='center', verticalalignment='center')

plt.text(xtext_x, xtext_y, 'STA (K)', transform=axs.transAxes,
     horizontalalignment='center', verticalalignment='center')

plt.tight_layout()
plt.savefig(
    "../figures/separate/figure2_npp_forest_biomass.png", dpi=100, transparent=True
)
plt.clf()


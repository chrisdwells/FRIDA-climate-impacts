import matplotlib.pyplot as plt
import pandas as pd
import pickle
import numpy as np
import string
string.ascii_lowercase
# For appendix figure in the climate impacts documentation paper
# remove the natural climate feedback plots

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


params_in = pd.read_csv('../data/sampleParmsParscaleRanged.csv')
params_in = params_in[['Variable', 'Value', 'Min', 'Max']]


sta_plot = np.linspace(0, 5, 50)
abs_t_plot = np.linspace(14, 20, 50)
co2_plot = np.linspace(400, 800, 50)
co2_plot_cf1980 = co2_plot - co2_plot[0]

nx = 4 #5 with natural feedbacks
ny = 4 #5 with natural feedbacks
fig, axs = plt.subplots(nx, ny, figsize=(15, 15))

axs = axs.ravel()

for j in np.arange(nx*ny):
    axs[j].text(-0.15, 1.05, f'({string.ascii_lowercase[j]})', transform=axs[j].transAxes)

i = 0


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
    axs[i].plot(sta_plot, resp, color=colors_p[perc], zorder=zorders_p[perc])
    
axs[i].set_title('Thermoelectric')
axs[i].set_ylabel('% efficiency change')
axs[i].set_xlabel('STA (K)')  


## Hydroelectric

i += 1

a = pkl_in['efficiency reduction in power plants.effect of STA on hydropower energy capacity efficiency slope[1]']
b = pkl_in['efficiency reduction in power plants.effect of STA on hydropower energy capacity efficiency quadratic[1]']

for p_i, perc in enumerate(percentiles):
    resp = a[p_i]*sta_plot + b[p_i]*sta_plot**2
    axs[i].plot(sta_plot, resp, color=colors_p[perc], zorder=zorders_p[perc])
    
axs[i].set_title('Hydroelectric')
axs[i].set_ylabel('% efficiency change')
axs[i].set_xlabel('STA (K)')  


# Energy Demand

## CDD
i += 1


a = 704.2
# b = np.asarray([230, 287.8469604, 330])

params_df = params_in.loc[params_in['Variable'] == 'energy demand.CDD linear coefficient[1]']
b = np.asarray([params_df['Min'], params_df['Value'], params_df['Max']])

for l_i, lev in enumerate(levels):
    resp = a + b[l_i]*sta_plot
    axs[i].plot(sta_plot, resp, color=colors_l[lev], zorder=zorders_l[lev])
    
axs[i].set_title('Cooling Degree Days')
axs[i].set_ylabel('CDD')
axs[i].set_xlabel('STA (K)')  


## HDD
i += 1

a = 1376
# b = np.asarray([-0.5, -0.232561095, -0.01])

params_df = params_in.loc[params_in['Variable'] == 'energy demand.HDD exponential coefficient[1]']
b = np.asarray([params_df['Min'], params_df['Value'], params_df['Max']])

for l_i, lev in enumerate(levels):
    resp = a*np.exp(b[l_i]*sta_plot)
    axs[i].plot(sta_plot, resp, color=colors_l[lev], zorder=zorders_l[lev])
    
axs[i].set_title('Heating Degree Days')
axs[i].set_ylabel('HDD')
axs[i].set_xlabel('STA (K)')  


# Energy Infrastructure Damage

i += 1

# a = np.asarray([0, 0.00005096093, 8]) 
# b = np.asarray([1, 2, 3])

params_df = params_in.loc[params_in['Variable'] == 'Damages.Slope of Capital Damage Function[1]']
a = np.asarray([params_df['Min'], params_df['Value'], params_df['Max']])

params_df = params_in.loc[params_in['Variable'] == 'Damages.Exponent of Capital Damage Function[1]']
b = np.asarray([params_df['Min'], params_df['Value'], params_df['Max']])


for l_i, lev in enumerate(levels):
    resp = a[l_i]*sta_plot**b[l_i]
    
    axs[i].plot(sta_plot, 100*resp, color=colors_l[lev], zorder=zorders_l[lev])
    
axs[i].set_title('Energy Infrastructure')
axs[i].set_ylabel('Annual Damage Percentage')
axs[i].set_xlabel('STA (K)')  



# Extremes Exposure

i += 1

param_file = '../../extremes-exposure/data/outputs/exposure_output_dict.pickle'

with open(param_file, 'rb') as handle:
    pkl_in = pickle.load(handle)

assert pkl_in['Percentiles'].all() == percentiles.all()

a = pkl_in['Energy Balance Model.T effect on population exposure to record breaking indices[1]']
b = pkl_in['Energy Balance Model.T2 effect on population exposure to record breaking indices[1]']

for p_i, perc in enumerate(percentiles):
    resp = a[p_i]*sta_plot + b[p_i]*sta_plot**2
    axs[i].plot(sta_plot, resp, color=colors_p[perc], zorder=zorders_p[perc])
    
axs[i].set_title('Extremes Exposure')
axs[i].set_ylabel('Per person per year')
axs[i].set_xlabel('STA (K)')  



# Durability of Concrete 

i += 1

# a = np.asarray([-15, -7.5, -5])

params_df = params_in.loc[params_in['Variable'] == 'Concrete.CLIMATE IMPACT ON CONCRETE LIFETIME[1]']
a = np.asarray([params_df['Min'], params_df['Value'], params_df['Max']])

for l_i, lev in enumerate(levels):
    resp = 1 + 100*a[l_i]*sta_plot
    axs[i].plot(sta_plot, resp, color=colors_l[lev], zorder=zorders_l[lev])
    
axs[i].set_title('Concrete Lifetime')
axs[i].set_ylabel('% change')
axs[i].set_xlabel('STA (K)')  



# Mortality

param_file = '../../temperature-mortality/data/outputs/mortality_output_dict.pickle'
with open(param_file, 'rb') as handle:
    pkl_in = pickle.load(handle)

assert pkl_in['Percentiles'].all() == percentiles.all()

## Cold

i += 1

a = pkl_in['Demographics.Cold mortality sensitivity to T[1]']
b = pkl_in['Demographics.Cold mortality sensitivity to T2[1]']

for p_i, perc in enumerate(percentiles):
    resp = a[p_i]*sta_plot + b[p_i]*sta_plot**2
    axs[i].plot(sta_plot, 100*resp, color=colors_p[perc], zorder=zorders_p[perc])
    
axs[i].set_title('Cold Mortality')
axs[i].set_ylabel('% change')
axs[i].set_xlabel('STA (K)')  

## Hot

i += 1

a = pkl_in['Demographics.Hot mortality sensitivity to T[1]']
b = pkl_in['Demographics.Hot mortality sensitivity to T2[1]']

for p_i, perc in enumerate(percentiles):
    resp = a[p_i]*sta_plot + b[p_i]*sta_plot**2
    axs[i].plot(sta_plot, 100*resp, color=colors_p[perc], zorder=zorders_p[perc])
    
axs[i].set_title('Hot Mortality')
axs[i].set_ylabel('% change')
axs[i].set_xlabel('STA (K)')  



# Labour productivity

## Low-exposure
i += 1

# a = np.asarray([-16, -2.08262027, -5])
# b = np.asarray([-2 , -1.56936859, 0.1])

params_df = params_in.loc[params_in['Variable'] == 'Employment.Temperature effect on low exposure productivity[1]']
a = np.asarray([params_df['Min'], params_df['Value'], params_df['Max']])

params_df = params_in.loc[params_in['Variable'] == 'Employment.Temperature squared effect on low exposure productivity[1]']
b = np.asarray([params_df['Min'], params_df['Value'], params_df['Max']])



for l_i, lev in enumerate(levels):
    resp = a[l_i]*sta_plot + b[l_i]*sta_plot**2
    axs[i].plot(sta_plot, resp, color=colors_l[lev], zorder=zorders_l[lev])
    
axs[i].set_title('Labour Low Exp')
axs[i].set_ylabel('% productivity change')
axs[i].set_xlabel('STA (K)')  


## High-exposure
i += 1

# a = np.asarray([-25, -6.13282138, -4])
# b = np.asarray([-1.5, -1.06197873, -1])

params_df = params_in.loc[params_in['Variable'] == 'Employment.Temperature effect on high exposure productivity[1]']
a = np.asarray([params_df['Min'], params_df['Value'], params_df['Max']])

params_df = params_in.loc[params_in['Variable'] == 'Employment.Temperature squared effect on high exposure productivity[1]']
b = np.asarray([params_df['Min'], params_df['Value'], params_df['Max']])

for l_i, lev in enumerate(levels):
    resp = a[l_i]*sta_plot + b[l_i]*sta_plot**2
    axs[i].plot(sta_plot, resp, color=colors_l[lev], zorder=zorders_l[lev])
    
axs[i].set_title('Labour High Exp')
axs[i].set_ylabel('% productivity change')
axs[i].set_xlabel('STA (K)')  




# Loan failure

i += 1

# a = np.asarray([0.1, 0.580674151, 1.1])

params_df = params_in.loc[params_in['Variable'] == 'Finance.sensitivity of effect of sta on failure rate[1]']
a = np.asarray([params_df['Min'], params_df['Value'], params_df['Max']])

for l_i, lev in enumerate(levels):
    resp = 1 + a[l_i]*sta_plot
    axs[i].plot(sta_plot, resp, color=colors_l[lev], zorder=zorders_l[lev])
    
axs[i].set_title('Indirect Economic Effects')
axs[i].set_ylabel('Scaling factor')
axs[i].set_xlabel('STA (K)')  


# Government spending

i += 1

# a = np.asarray([0, 0.068134916, 0.2])

params_df = params_in.loc[params_in['Variable'] == 'Government.sensitivity of STA on public consumption[1]']
a = np.asarray([params_df['Min'], params_df['Value'], params_df['Max']])

for l_i, lev in enumerate(levels):
    resp = 1 + a[l_i]*sta_plot
    axs[i].plot(sta_plot, resp, color=colors_l[lev], zorder=zorders_l[lev])
    
axs[i].set_title('Government Spending')
axs[i].set_ylabel('Scaling factor')
axs[i].set_xlabel('STA (K)')  



# Crops

i += 1

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
    axs[i].plot(abs_t_plot, resp, color=colors_p[perc], zorder=zorders_p[perc])
    
axs[i].set_title(fr'Crops, CO$_{2}$ = {CO2_fix} ppm')
axs[i].set_ylabel('% productivity change')
axs[i].set_xlabel(r'Absolute Temperature ($^{\circ}$C)')

i += 1

for p_i, perc in enumerate(percentiles):
    resp = a[p_i] + b[p_i]*T_fix + c[p_i]*T_fix**2 + d[p_i]*co2_plot
    axs[i].plot(co2_plot, resp, color=colors_p[perc], zorder=zorders_p[perc])
    
axs[i].set_title(f'Crops, Temp = {T_fix} ' + r'$^{\circ}$C')
axs[i].set_ylabel('% productivity change')
axs[i].set_xlabel(r'CO$_{2}$ (ppm)')    



# Evapotranspiration

i += 1

# a = np.asarray([0.02, 0.064352435, 0.1])

params_df = params_in.loc[params_in['Variable'] == 'Freshwater.sensitivity of surface temperature anomaly on water used per Mtcrop[1]']
a = np.asarray([params_df['Min'], params_df['Value'], params_df['Max']])

for l_i, lev in enumerate(levels):
    resp = 1 + a[l_i]*sta_plot
    axs[i].plot(sta_plot, resp, color=colors_l[lev], zorder=zorders_l[lev])
    
axs[i].set_title('Evapotranspiration')
axs[i].set_ylabel('Scaling factor')
axs[i].set_xlabel('STA (K)')  


# # Soil Carbon

# i += 1

# # a = np.asarray([40, 60, 60])
# # b = np.asarray([290, 290.0287445, 320])

# params_df = params_in.loc[params_in['Variable'] == 'soil carbon decay.temp response[1]']
# a = np.asarray([params_df['Min'], params_df['Value'], params_df['Max']])

# params_df = params_in.loc[params_in['Variable'] == 'soil carbon decay.e0[1]']
# b = np.asarray([params_df['Min'], params_df['Value'], params_df['Max']])

# b = b[::-1]

# for l_i, lev in enumerate(levels):
#     resp = np.exp(b[l_i]*(1.0/(a[l_i]+10)-1.0/(abs_t_plot+a[l_i])))
    
#     axs[i].plot(abs_t_plot, resp, color=colors_l[lev], zorder=zorders_l[lev])
    
    
    
    
# axs[i].set_title('Soil Carbon Decay')
# axs[i].set_ylabel('Scaling factor')
# axs[i].set_xlabel(r'Absolute Temperature ($^{\circ}$C)')





# # Net Primary Production; 2 2d slices, 2 types (4)

# ## Forest

# i += 1

# # a = np.asarray([0.01, 0.125348729, 0.13])
# # b = np.asarray([-0.05, -0.023015026, -0.01])
# # c = np.asarray([0.0005, 0.001, 0.001])

# params_df = params_in.loc[params_in['Variable'] == 'Forest.STA tree net primary production parameter[1]']
# a = np.asarray([params_df['Min'], params_df['Value'], params_df['Max']])

# params_df = params_in.loc[params_in['Variable'] == 'Forest.STA squared tree net primary production parameter[1]']
# b = np.asarray([params_df['Min'], params_df['Value'], params_df['Max']])

# params_df = params_in.loc[params_in['Variable'] == 'Forest.CO2 tree net primary production parameter[1]']
# c = np.asarray([params_df['Min'], params_df['Value'], params_df['Max']])



# for l_i, lev in enumerate(levels):
#     resp = a[l_i]*sta_plot + b[l_i]*sta_plot**2 + c[l_i]*0 # CO2 cf 1980
    
#     axs[i].plot(sta_plot, resp, color=colors_l[lev], zorder=zorders_l[lev])
    
# axs[i].set_title(fr'NPP Forest, CO$_{2}$ as 1980')
# axs[i].set_ylabel('Fractional Change')
# axs[i].set_xlabel('STA cf 1980 (K)')  

# i += 1

# for l_i, lev in enumerate(levels):
#     resp = a[l_i]*T_fix_sta + b[l_i]*T_fix_sta**2 + c[l_i]*co2_plot_cf1980
    
#     axs[i].plot(co2_plot_cf1980, resp, color=colors_l[lev], zorder=zorders_l[lev])
    
# axs[i].set_title('NPP Forest, STA as 1980')
# axs[i].set_ylabel('Fractional Change')
# axs[i].set_xlabel(f'CO$_{2}$ cf 1980 (ppm)')  



# ## Grass

# i += 1


# # a = np.asarray([0.01, 0.126281692, 0.13])
# # b = np.asarray([-0.05, -0.034654395, -0.01])
# # c = np.asarray([0.0005, 0.000963654, 0.001])


# params_df = params_in.loc[params_in['Variable'] == 'Grass.STA grass net primary production parameter[1]']
# a = np.asarray([params_df['Min'], params_df['Value'], params_df['Max']])

# params_df = params_in.loc[params_in['Variable'] == 'Grass.STA squared grass net primary production parameter[1]']
# b = np.asarray([params_df['Min'], params_df['Value'], params_df['Max']])

# params_df = params_in.loc[params_in['Variable'] == 'Grass.CO2 grass net primary production parameter[1]']
# c = np.asarray([params_df['Min'], params_df['Value'], params_df['Max']])



# for l_i, lev in enumerate(levels):
#     resp = a[l_i]*sta_plot + b[l_i]*sta_plot**2 + c[l_i]*0 # CO2 cf 1980
    
#     axs[i].plot(sta_plot, resp, color=colors_l[lev], zorder=zorders_l[lev])
    
# axs[i].set_title(fr'NPP Grass, CO$_{2}$ as 1980')
# axs[i].set_ylabel('Fractional Change')
# axs[i].set_xlabel('STA cf 1980 (K)')  

# i += 1

# for l_i, lev in enumerate(levels):
#     resp = a[l_i]*T_fix_sta + b[l_i]*T_fix_sta**2 + c[l_i]*co2_plot_cf1980
    
#     axs[i].plot(co2_plot_cf1980, resp, color=colors_l[lev], zorder=zorders_l[lev])
    
# axs[i].set_title('NPP Grass, STA as 1980')
# axs[i].set_ylabel('Fractional Change')
# axs[i].set_xlabel(r'CO$_{2}$ cf 1980 (ppm)')  


# # Forest Biomass

# i += 1

# # a = np.asarray([0.2, 0.253488316, 0.35])
# # b = np.asarray([-0.08, -0.048709811, -0.02])


# params_df = params_in.loc[params_in['Variable'] == 'Forest.STA maximum aboveground biomass per area parameter[1]']
# a = np.asarray([params_df['Min'], params_df['Value'], params_df['Max']])

# params_df = params_in.loc[params_in['Variable'] == 'Forest.STA squared maximum aboveground biomass per area parameter[1]']
# b = np.asarray([params_df['Min'], params_df['Value'], params_df['Max']])

# for l_i, lev in enumerate(levels):
#     resp = a[l_i]*sta_plot + b[l_i]*sta_plot**2
#     axs[i].plot(sta_plot, resp, color=colors_l[lev], zorder=zorders_l[lev])
    
# axs[i].set_title('Forest Biomass')
# axs[i].set_ylabel('Scaling factor')
# axs[i].set_xlabel('STA (K)')  

while i+1 < nx*ny:
    i += 1
    axs[i].set_visible(False)
    
plt.tight_layout()
plt.savefig(
    "../figures/figure2_panels_nonatural.png"
)

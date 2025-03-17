import pandas as pd
import numpy as np
import pickle

percentiles = np.linspace(0.025, 0.975, 11)


pkl_files = [
    '../../climate-energy-supply/data/outputs/energy_suppy_output_dict.pickle',
    '../../temperature-mortality/data/outputs/mortality_output_dict.pickle',
    '../../extremes-exposure/data/outputs/exposure_output_dict.pickle',
    '../../climate-crops-impacts/data/outputs/crops_output_dict.pickle',
    ]

columns = list(percentiles)
columns.insert(0, 'Variable')

df = pd.DataFrame(columns = columns)

for f in pkl_files:
    with open(f, 'rb') as handle:
        pkl_in = pickle.load(handle)
      
    assert pkl_in['Percentiles'].all() == percentiles.all()
    
    for var in pkl_in.keys():
        if var != 'Percentiles':
            
            row_in = list(pkl_in[var])
            row_in.insert(0, var[:-3])
            
            df.loc[len(df)] = row_in


#df = df.T.reset_index(drop=True).T

df.to_csv('../outputs/climate_impacts_parameter_sets.csv', index=False)




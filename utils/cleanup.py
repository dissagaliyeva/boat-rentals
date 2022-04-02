import numpy as np
import pandas as pd


def clean_group(listings):
    
    mode = lambda x: x.mode() 

    fill = listings.groupby('Boat Type').agg({'Material': mode, 'Type': mode, 
                                              'Length': np.median, 'Width': np.median,
                                              'Manufacturer': mode})
    material = fill['Material'].to_dict()
    types = fill['Type'].to_dict()
    length = fill['Length'].to_dict()
    width = fill['Width'].to_dict()
    manufacturer = fill['Manufacturer'].to_dict()
    
    # Type
    missing = listings[listings['Type'].isna()]

    for idx in missing.index:
        val = types[listings.loc[idx, 'Boat Type']]

        if len(val) > 1:
            val = val[0]

        listings.loc[idx, 'Type'] = val

    # Material
    missing = listings[listings['Material'].isna()]

    for idx in missing.index:
        val = material[listings.loc[idx, 'Boat Type']]

        if len(val) == 0:
            val = 'Uknown'
        listings.loc[idx, 'Material'] = val

    # Length
    missing = listings[listings['Length'].isna()]

    for idx in missing.index:
        listings.loc[idx, 'Length'] = length[listings.loc[idx, 'Boat Type']]

    # Width
    missing = listings[listings['Width'].isna()]

    for idx in missing.index:
        listings.loc[idx, 'Width'] = width[listings.loc[idx, 'Boat Type']]


    # Manufacturer
    missing = listings[listings['Manufacturer'].isna()]

    for idx in missing.index:
        val = manufacturer[listings.loc[idx, 'Boat Type']]

        if len(val) > 1:
            val = val[0]

        if len(val) == 0:
            val = 'Uknown'

        listings.loc[idx, 'Manufacturer'] = val

        
def prettify_locations(x):
    if 'United Kingdom' in x:
        return 'United Kingdom'
    if 'United Arab Emirates' in x:
        return 'United Arab Emirates'
    if 'Slovak Republic' in x:
        return 'Slovak Republic'
    if 'Russian Federation' in x:
        return 'Russian Federation'
    if 'Czech Republic' in x:
        return 'Czech Republic'
    if x.startswith('Lago') or x.startswith('Ital'):
        return 'Italy'
    if x.startswith('Lake Constance') or 'Brandenburg' in x or 'Donau' in x:
        return 'Germany'
    if 'Lake Geneva' in x or 'Avenches' in x:
        return 'Switzerland'
    if 'United States' in x:
        return 'United States'

    if ' ' in x:
        return x.split(' ')[0]
    return x


def change_type(x):
    if x in ['Diesel', 'Unleaded', 'Electric']:
        return x
    if ',' in x:
        return x.split(',')[-1]
    return 'Uknown'
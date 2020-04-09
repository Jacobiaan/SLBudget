#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Read monthly steric sea level data from IPA.
    Compute yearly averages.
    Output results in a single netcdf file. """

import numpy as np
import xarray as xr

Dir = '/Users/dewilebars/Projects/SLBudget/data/DataSteric/DataStericIAP/'

# Choose the area and time of interest
year_min, year_max = 1940, 2019

for year in range(year_min, year_max+1):
    ifiles = 'Steric_IAP_2000m_year_'+str(year)+ '_month_*.nc'
    print('Working on files:'+ifiles)
    ds = xr.open_mfdataset(Dir+ifiles)
    
    len_ds = len(ds.time)
    if len_ds != 12:
        print('WARNING: MISSING FILE(S), number files:')
        print(len_ds)
        print('Should be 12')
    
    mean_ds = ds.mean(dim='time')
    
    if year == year_min:
        full_ds = mean_ds
    else:
        full_ds = xr.concat((full_ds, mean_ds),dim='time')

full_ds['time'] = np.arange(year_min, year_max+1)
full_ds.to_netcdf(Dir+'Steric_IAP_2000m_yearly_'+str(year_min)+'_'
                  +str(year_max)+'.nc', mode='w')

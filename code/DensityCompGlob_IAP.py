#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Read monthly temperature and salinity from IAP data. 
    Compute the density with GSW package.
    Output yearly average results into a netcdf file. """

import numpy as np
import xarray as xr
import gsw

path = '/Users/dewilebars/Projects/SLBudget/data/DataSteric/'
Dir_in = path + 'DataTS_IAP/'
Dir_out = path +'density_teos10_IAP/'

# Define functions #############################################################
# def rotate_longitude(ds):
#     ds = ds.roll(longitude=180, roll_coords=True)
#     ds['longitude'] = np.where(ds['longitude']>180, ds['longitude']-360, ds['longitude'])
#     return ds
def rotate_longitude(ds, name_lon):
    ds[name_lon].values = (((ds[name_lon] + 180 ) % 360) - 180)
    ds = ds.sortby(ds[name_lon])
    return ds

################################################################################

# Choose time of interest
year_min, year_max = 1940, 2020 # Not including last year

for year in range(year_min, year_max):
    file_temp = 'Temp/CZ16_1_2000m_Temp_year_'+str(year)+'_month_*.nc'
    file_sal = 'salinity/CZ16_1_2000m_salinity_year_'+str(year)+'_month_*.nc'
    print('Working on files:')
    print(file_temp)
    print(file_sal)
    temp_ds = xr.open_mfdataset(Dir_in+file_temp)
    sal_ds = xr.open_mfdataset(Dir_in+file_sal)
    
    temp_ds = rotate_longitude(temp_ds, 'lon')
    sal_ds = rotate_longitude(sal_ds, 'lon')

    temp = temp_ds.temp.mean(dim='time')
    sal = sal_ds.salinity.mean(dim='time')
    
    # Calculate pressure from depth, depth should be positive upward
    depth_a = np.array(temp.depth_std).copy()
    depth_a = depth_a.reshape( len(temp.depth_std), 1)
    pres = gsw.p_from_z(-depth_a, temp.lat)
    
    # Reshape arrays for broadcasting
    #pres = np.array(pres)
    pres = pres.reshape( pres.shape[1], 1, pres.shape[0])
    
    rho = gsw.rho_t_exact(sal, temp, pres)
    
    # Add metadata and plot with xarray
    rho_at = {'long_name' : 'in-situ density', 'units' : 'kg/m3'}
    
    rho   = xr.DataArray(rho, coords=[ temp.lat, temp.lon, temp.depth_std], \
                    dims=['lat', 'lon', 'depth'], name='density', attrs=rho_at)

    rho = rho.transpose('depth', 'lat', 'lon')
    
    rho.to_netcdf(Dir_out+'density_teos10_iap_'+ str(year) + '.nc')

###############################################################################
# To compute the thermal expansion and haline contraction coefficients as 
# well as the dentisty the in-situ temperature needs to be converted to 
# conservative temperature with gsw.CT_from_t and then the following 
# function can be used:
#rho, alpha, beta = gsw.rho_alpha_beta(sa, ct, pres)

# Add metadata and plot with xarray
    
# alpha_at = {'long_name' : 'thermal expansion coefficient with respect to Conservative Temperature' \
#             , 'units' : '1/K' }
# alpha = xr.DataArray(alpha, coords=[temp.depth, temp.lat, temp.lon], \
#                      dims=['depth', 'lat', 'lon'], name='alpha', attrs=alpha_at)
# beta_at = {'long_name' : 'saline (i.e. haline) contraction coefficient at constant'+ \
#            'Conservative Temperature', 'units' : 'kg/g'}
# beta  = xr.DataArray(beta, coords=[temp.depth, temp.lat, temp.lon], \
#                      dims=['depth', 'lat', 'lon'], name='beta', attrs=beta_at)

# Add all variables into one dataset and export as NetCDF
# Use following line to include multiple variables into the dataset:
#if year == year_min:
#    RHO = rho
#    ALPHA = alpha
#    BETA = beta
#else:
#    RHO = xr.concat((RHO, rho),dim='time')
#    ALPHA = xr.concat((ALPHA, alpha),dim='time')
#    BETA = xr.concat((BETA, beta),dim='time')

#DENS_d = xr.merge((RHO, ALPHA, BETA))
#DENS_d['time'] = range(year_min, year_max)
#DENS_d.to_netcdf('density_teos10_en4_'+ str(year_min) + '_' + str(year_max) + '.nc')
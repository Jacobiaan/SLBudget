import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xarray as xr
import xesmf as xe                     # package for regridding 
#import cartopy.crs as ccrs              # for the regridding test(now only to understand how it works later maybe more - probably I can do a lot with this package

#import gravity toolkit 
import gravity_toolkit as gravtk

#from scipy import signal              #not sure if I need those
#import importlib
import sys
sys.path.append('../code')

def sealevelfunctions(meltrates, lon_target, lat_target, landsea):
    #Uses as input the regridded melt values and the landseamaks with the same dimensions
    
    th = (90 - lat_target)*np.pi/180.0
    LMAX = 360
    LOVE = gravtk.load_love_numbers(LMAX)
    PLM, dPLM = gravtk.plm_holmes(LMAX, np.cos(th))
    #LOVE0 = (LOVE[0]-LOVE[0], LOVE[1]-LOVE[1], LOVE[2]-LOVE[2]) # not needed? 

    Ylms = gravtk.gen_stokes(meltrates.data.T, lon_target, lat_target, UNITS=3, LMIN=0, LMAX=LMAX, LOVE=LOVE, PLM=PLM)

    rsl = gravtk.sea_level_equation(Ylms.clm, Ylms.slm, lon_target, lat_target, landsea.data.T,
    LMAX=LMAX, PLM=PLM, LOVE=LOVE, ITERATIONS=6, POLAR=True)

    rsl_da = xr.DataArray(
        data=rsl.T,              # transpose if needed
        dims=["lat", "lon"],     # match array shape
        coords={"lat": lat_target, "lon": lon_target}
    )

    rsl_da = rsl_da.where(landsea != 1, np.nan)

    return rsl_da


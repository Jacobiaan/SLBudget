# Produce a csv file of global sea level contributions from steric, glaciers and ice sheets since 1950 to use to make maps of sea level for the GTSM project.

import numpy as np
import pandas as pd
import SeaLevelContrib as slc
import matplotlib.pyplot as plt

glac_df = slc.glaciers_m15(tg_id = None, extrap=True, del_green=True)
ant_df = slc.ant_rignot19_glo()  #imbie or rignot19
#ant_df = slc.ant_imbie_glo(extrap=True) 
green_df = slc.green_mouginot19_glo()
tws_df = slc.TWS_glo()

sealevel_df = slc.LevitusSL(extrap_back = True)
sealevel_df = sealevel_df.join([glac_df, ant_df, green_df, tws_df], how='outer')
sealevel_df = sealevel_df - sealevel_df.loc[1950]

sealevel_df['Total'] = sealevel_df.sum(axis=1)
sealevel_df.index.names = ['time']

sealevel_df.loc[1950:].to_csv('GlobSLContrib_ForGTSM2019.csv')
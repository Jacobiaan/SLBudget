def tide_gauge_mean(tg_id=[20, 22, 23, 24, 25, 32]):
    '''Read a list of tide gauge data and compute the average. 
    By default use the 6 tide gauges from the zeespiegelmonitor''' 
    
    tg_data_dir = '/Users/dewi/Work/Project_SeaLevelBudgets/rlr_annual'
    names_col = ('id', 'lat', 'lon', 'name', 'coastline_code', 'station_code', 'quality')
    filelist_df = pd.read_csv(tg_data_dir + '/filelist.txt', sep=';', header=None, names=names_col)
    filelist_df = filelist_df.set_index('id')

    names_col2 = ('time', 'height', 'interpolated', 'flags')
    names_col3 = []

    tg_data = {}
    for i in range(len(tg_id)):
        interm     = pd.read_csv(tg_data_dir + '/data/' + str(tg_id[i]) + '.rlrdata', sep=';', 
                                 header=None, names=names_col2)
        interm     = interm.set_index('time')
        tg_data[i] = (interm.height - interm.height.mean())*0.1 # Convert from mm to cm 
        names_col3.append(filelist_df['name'].loc[tg_id[i]].strip())

    tg_data_df = pd.concat(tg_data, axis=1 )
    tg_data_df.columns = names_col3
    tg_data_df = tg_data_df[tg_data_df.index >= 1890].copy()
    # 1890 is to follow the choice of the zeespiegelmonitor
    # Alternatively use 1948 to fit with NCEP1 starting date, 
    tg_data_df_mean = tg_data_df.mean(axis=1)  # This returns a series instead of a DataFrame
    tg_data_df_mean = pd.DataFrame(tg_data_df_mean)
    tg_data_df_mean.columns = ['height']
    return tg_data_df_mean
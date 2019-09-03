import numpy as np
import matplotlib.pyplot as plt
import os 

from netCDF4 import Dataset
from datetime import datetime

# Get an array of coordinates (lat, lon)
def get_coordinates(lat_in, lon_in):
    lat = lat_in
    lon = lon_in
    lat_lon_coordinates = [lat, lon]
    return lat_lon_coordinates

def get_elaf(obs, fcst_land, fcst_sea,
        time_of_day = 12, loc_id = 17):
    
    diff_land_sea = np.zeros(len(obs[:,time_of_day, loc_id]))
    diff_obs_sea = np.zeros(len(obs[:,time_of_day, loc_id]))
    elaf = np.zeros(len(obs[:,time_of_day, loc_id]))

    for i in range(len(obs)):
        diff_land_sea[i] = fcst_land[i, time_of_day, loc_id] - fcst_sea[i, time_of_day, loc_id]
        diff_obs_sea[i] = obs[i, time_of_day, loc_id] - fcst_sea[i, time_of_day, loc_id]
        elaf[i] = diff_obs_sea[i] / diff_land_sea[i]
        
        if elaf[i] > 1.0:
            elaf[i] = 1.0
        elif elaf[i] < 0.0:
            elaf[i] = 0.0
        else:
            elaf[i] = round(elaf[i], 2)
    return elaf

def get_diff(fcst_1, fcst_2): #fcst_1 the reference, fcst_2 the subtractor
    diff = np.zeros(len(fcst_1))
    for i in range(len(fcst_1)):
        diff[i] = fcst_1[i] - fcst_2[i]
    return diff

def main():
    #Get datasets
    nn = Dataset('nn.nc')
    land = Dataset('land.nc')
    sea = Dataset('sea.nc')

    #Jomfruland coordinates
    jmfrlnd = get_coordinates(58.857878, 9.585044)

    # Reference Forecast
    fcst_ref = nn.variables['fcst']     # forecast nearest neighbor
    lat = nn.variables['lat']           # Latitude
    lon = nn.variables['lon']           # Lonitude
    obs = nn.variables['obs']           # Observations
    unixtime = nn.variables['time']     # Time
    location = nn.variables['location'] # location id
    altitude = nn.variables['altitude'] # altitude
    leadtime = nn.variables['leadtime'] # leadtime 

    # Sea Forecast
    fcst_sea = sea.variables['fcst'][:]

    # Land Forecast
    fcst_land = land.variables['fcst'][:]

    # Convert unixtime to datetime
    time = []
    timestamp = []
    for i in range(len(unixtime[:])):
        #time.append(datetime.utcfromtimestamp(int(unixtime[i])).strftime('%Y-%m-%d %H:%M:%S'))
        time.append(datetime.utcfromtimestamp(int(unixtime[i])).strftime('%Y%m%d'))
        timestamp.append(datetime.utcfromtimestamp(int(unixtime[i])))
    # Get temperature forecast difference between land and ocean
    fcst_diff = get_diff(fcst_land[:,12,17], fcst_sea[:,12,17])

    # Get ELAF
    elaf = get_elaf(obs, fcst_land, fcst_sea)
    """
    # Print Results 
    def print_results(start = 0, end = len(obs[:,12,17]),
            temp_diff_threshold = 0):

        data = []
        title = 'loc id', 'date', 'l time', 'lat', 'lon', 'alt', 'fcst L', 'fcst S', 'fcst R', 'obs', 'Elaf', 'delta T', 'laf n'
        
        if os.path.exists('output.txt'):
            os.remove('output.txt')

        with open('output.txt', 'w') as txt_file:
            for line in title:
                txt_file.write(' '.join(line) + '\n')

        for j in range(len(obs[0,0,:])):
            # Get temperature froecast difference between land and ocean 
            fcst_diff = get_diff(fcst_land[:,12,j], fcst_sea[:,12,j])

            # Get Expected Land Area Fraction (ELAF)
            elaf = get_elaf(obs, fcst_land, fcst_sea, loc_id = j)

            laf_nn = get_elaf(fcst_ref, fcst_land, fcst_sea, loc_id = j)
             
            for i in range(len(obs[:,0,0])):
                if timestamp[i].month == 4:
                    if not np.isnan(fcst_land[i,12,j]):
                        if not np.isnan(fcst_sea[i,12,j]):
                            if not np.isnan(fcst_ref[i,12,j]):
                                if not np.isnan(obs[i,12,j]):
                                    if fcst_land[i,12,j] != '--':
                                        data.append([str(location[j]), str(time[i]), str(leadtime[12]), str(lat[j]), str(lon[j]), str(altitude[j]), str(fcst_land[i,12,j]), str(fcst_sea[i,12,j]), str(fcst_ref[i,12,j]), str(obs[i,12,j]), str(elaf[i]), str(fcst_diff[i]), str(laf_nn[i])])
                else:
                    pass 
                    #print(type(fcst_land[i,12,j]))
            with open('output.txt', 'w') as txt_file:
                for line in data:
                    txt_file.write('\t'.join(line) + '\n')
            print(j)

    print_results(0, len(time[:]), temp_diff_threshold = 0)
    """
    data = []
    title = 'loc id', 'date', 'l time', 'lat', 'lon', 'alt', 'fcst L', 'fcst S', 'fcst R', 'obs', 'Elaf', 'delta T', 'laf n'

    for j in range(len(obs[0,0,:])):
        
        fcst_diff = get_diff(fcst_land[:,12,j], fcst_sea[:,12,j])

        elaf = get_elaf(obs, fcst_land, fcst_sea, loc_id = j)

        laf_nn = get_elaf(fcst_ref, fcst_land, fcst_sea, loc_id = j)
             
        for i in range(len(obs[:,0,0])):
            if timestamp[i].month == 4:
                if not np.isnan(fcst_land[i,12,j]):
                    if not np.isnan(fcst_sea[i,12,j]):
                        if not np.isnan(fcst_ref[i,12,j]):
                            if not np.isnan(obs[i,12,j]):
                                if fcst_land[i,12,j] != '--':
                                    data.append([str(location[j]), str(time[i]), str(leadtime[12]), str(lat[j]), str(lon[j]), str(altitude[j]), str(fcst_land[i,12,j]), str(fcst_sea[i,12,j]), str(fcst_ref[i,12,j]), str(obs[i,12,j]), str(elaf[i]), str(fcst_diff[i]), str(laf_nn[i])])
        
            if j == 0:
                if os.path.exists('output.txt'):
                    os.remove('output.txt')

            with open('output.txt', 'w') as txt_file:
                if j == 0:
                    for line in title:
                        txt_file.write('\t'.join(line) + '\n')
                for line in data:
                    txt_file.write('\t'.join(line) + '\n')
    
        print(j)

    plt.plot(fcst_diff, elaf, 'o')
    plt.show()
main()

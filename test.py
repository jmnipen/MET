import numpy as np
import matplotlib.pyplot as plt 
from netCDF4 import Dataset 

#Jomfrulandet coordinates
lat = 58.857878
lon = 9.585044

#Fetch dataset for nearest neighbour, land, sea
nn = Dataset('nn.nc')
land = Dataset('land.nc')
sea = Dataset('sea.nc')

# Define variables
var = ['fcst', 'lat', 'lon']
#obj = [fcst, lat, lon]

# Fetch variables
fcst_nn = nn.variables[var[0]]
lat_nn = nn.variables[var[1]]
lon_nn = nn.variables[var[2]]
obs_nn = nn.variables['obs']
time_nn = nn.variables['time'] 

fcst_land = land.variables[var[0]]
lat_land = land.variables[var[1]]
lon_land = land.variables[var[2]]
obs_land = land.variables['obs']

fcst_sea = sea.variables[var[0]]
lat_sea = sea.variables[var[1]]
lon_sea = sea.variables[var[2]]

#for i in range(len(var)):
#    obj[i] = nn.variables[var[i]]

fcst_land = land.variables['fcst']

lat_array = lat_nn[:]
lon_array = lon_nn[:]

i = np.abs(lon_array - lon).argmin()
j = np.abs(lat_array - lat).argmin()


def print_variables():
    print(' --- VARIABLES --- ')
    print(nn.variables)
    print('  ')
#print_variables()

def print_info():
    print(i,j)

    print(fcst_nn[0,17,17])
    print(fcst_land[0,17,17])

    print(obs_nn[0,17,17])

    print(lat_nn[17])
    print(lon_nn[17])
    print(lat_nn.dimensions)
    print(lon_nn.dimensions)
    print(fcst_nn.dimensions)
#print_info()

def check_equality():
    for i in range(len(obs_nn[:,17,17])):
        if obs_nn[i,17,17] != obs_land[i,17,17]:
            print('False')
            return False 

def main():
    check_equality()
    print(len(obs_nn[:,17,17]))
    
    
    len_obs = len(obs_nn[:,17,17])


    total_diff = np.zeros(len_obs)
    obs_diff = np.zeros(len_obs)
    obs_div = np.zeros(len_obs)

    for i in range(len_obs):
        total_diff[i] = fcst_sea[i,17,17] - fcst_land[i,17,17]

    for i in range(len_obs):
        obs_diff[i] = obs_land[i,17,17] - fcst_land[i,17,17]

    for i in range(len_obs):
        obs_div[i] = float(obs_diff[i]) / total_diff[i]
        if obs_div[i] > 1.0:
            obs_div[i] = 1.0
        elif obs_div[i] < 0.0:
            obs_div[i] = 0.0
        else:
            obs_div[i] = round(obs_div[i], 2)
        

    for i in range(20):
        print('time ' + str(i))
        print(fcst_sea[i, 17, 17])
        print(fcst_land[i,17, 17])
        print(obs_land[i, 17, 17])
        print(' ')

    print(fcst_nn[0,17,17])
    print(obs_nn[0,17,17])
    print(fcst_land[0,17,17])
    print(obs_land[0,17,17])

    for i in range(10):
        print(obs_div[i*100:(i+1)*100])

#main()
print_info()
print_variables()

print(time_nn[:])

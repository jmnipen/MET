import numpy as np
import matplotlib.pyplot as plt 
from netCDF4 import Dataset 

#Jomfrulandet coordinates
lat = 58.857878
lon = 9.585044

temp = Dataset('nn.nc')

temp_l = temp.variables['fcst']
lat_l = temp.variables['lat']
lon_l = temp.variables['lon']

lat_array = lat_l[:]
lon_array = lon_l[:]

i = np.abs(lon_array - lon).argmin()
j = np.abs(lat_array - lat).argmin()

print(i,j)

print(temp_l[0,17,17])
print(lat_l[17])
print(lon_l[17])
print(lat_l.dimensions)
print(lon_l.dimensions)
print(temp_l.dimensions)

#print(temp)
#print(temp.dimensions['time'])
#print(temp.variables['fcst'])
#print(temp.dimensions['location'])


import numpy as np
from netCDF4 import Dataset

sea = Dataset('sea.nc', 'w', format='NETCDF4')
land = Dataset('land.nc', 'w', format ='NETCDF4')

print(sea.data_model)

#print(sea.shape)
#print(land.shape)





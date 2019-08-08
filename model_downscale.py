"""
laf 			# Land-Area_fraction (LAF) 2.5x2.5km 
t_arome			# temperature (T) of the grid laf (2.5x2.5km)

t_laf_3_low		# T of lowest LAF grid for 7.5x7.5km grid
t_laf_3_high	# T of highest LAF grid for 7.5x7.5km grid
t_laf_5_low		# T of lowest LAF grid for 12.5x12.5km grid
t_laf_5_high	# T of highest LAF grid for 12.5x12.5km grid
t_laf_7_low		# T of lowest LAF grid for 17.5x17.5km grid
t_laf_7_high 	# T of highest LAF grid for 17.5x17.5km grid

laf_3 			# LAF at a 3x3grid (7.5x7.5km)
laf_5 			# LAF at a 5x5grid (12.5x12.5km)
laf_7 			# LAF at a 7x7grid (17.5x17.5km)

t_laf_3 		# CALCULATE calculated scenario temperature 
t_laf_5 		# CALCULATE calculated scaneria temeprature
t_laf_7   		# CALCULATE calclated scenario temperature

laf_1x1 		# LAF of 1x1km grid
t_laf_1x1		# CALCULATE the calculated temperature of the land area fraction

t_forecast 		# CALCULATE Final temperature forecast for the downscaled grid
"""

import numpy as np 
import matplotlib.pyplot as plt 

def get_temperature_gradient(high_laf, low_laf, t_high_laf, t_low_laf):
	""" Finds the temperature gradient, i.e. the change in temperatur
		with respect to the change in LAF """
	if high_laf - 0.1 >= low_laf:
		t_gradient = (t_high_laf - t_low_laf)/(high_laf - low_laf) 
	else:
		t_gradient = 0.0
	return t_gradient

def get_temperature_at_laf0(t_low_laf, low_laf, t_gradient):
	""" returns the temperature at which the LAF is 0 """
	t_laf0 =  t_low_laf - low_laf * t_gradient	
	return t_laf0

def get_t_laf_1x1(laf_1x1, t_gradient, t_laf0):
	t_laf_1x1 = t_laf0 + t_gradient*laf_1x1 
	return t_laf_1x1 

def get_t_laf(laf_area, t_gradient, t_laf0):
	t_laf = t_laf0 + t_gradient * laf_area 
	return t_laf 

def get_downscaled_t(t_gradient, t_laf0, t_arome, 
	laf_1x1, laf_3, laf_5, laf_7,
	a1, a2, a3, a4, a5): # LAF 
	""" get downscaled temperature t_star as function of t at 1x1km"""

	### Get temperatures from different grid scales
	t_laf_1x1 = get_t_laf(laf_1x1, t_gradient, t_laf0)
 	#t_arome = t_arome #Given
	t_laf_3 = get_t_laf(laf_3, t_gradient, t_laf0)
	t_laf_5 = get_t_laf(laf_5, t_gradient, t_laf0)
	t_laf_7 = get_t_laf(laf_7, t_gradient, t_laf0)

	t_forecast = 	(a1 * t_laf_1x1 + 
					a2 * t_arome + 
					a3 * t_laf_3 + 
					a4 * t_laf_5 + 
					a5 * t_laf_7 )

	return t_forecast

laf_max = 0.9
laf_min = 0.1
laf_1x1 = 0.7 
alpha1 = 0.5
alpha2 = 0.5 

temp_arome = np.zeros(24); temp_laf_low = np.zeros(24); temp_laf_high = np.zeros(24)
temp_1x1 = np.zeros(24)

temp_model_average = np.zeros(24)

temp_arome[:] = [10, 10, 10, 10, 9, 9, 10, 10, 12, 13, 14, 15, 15, 15, 15, 14, 14, 14, 13, 12, 12, 12, 11, 11]
temp_laf_low[:] = [11, 11, 11, 11, 11, 10, 10, 10, 11, 11, 12, 12, 12, 13, 13, 13, 13, 12, 12, 12, 12, 12, 12, 11]
temp_laf_high[:] = [8, 8, 8, 7, 7, 6, 6, 6, 9, 12, 17, 19, 22, 24, 24, 23, 23, 23, 18, 15, 13, 10, 8, 8]

gradient = np.zeros(len(temp_arome))
for i in range(0,len(temp_arome)):
	gradient[i] = get_temperature_gradient(laf_max, laf_min, temp_laf_high[i], temp_laf_low[i])

temp_laf_0 = np.zeros(len(temp_arome))
temp_laf_1 = np.zeros(len(temp_arome))

for i in range(0, len(temp_arome)):
	temp_laf_0[i] = temp_laf_low[i] - gradient[i] * laf_min 
	temp_laf_1[i] = temp_laf_low[i] + gradient[i] * ( 1-laf_min )
	temp_1x1[i] = temp_laf_0[i] + gradient[i] * laf_1x1  

for i in range(0, len(temp_arome)):
	temp_model_average[i] = alpha1 * temp_1x1[i] + alpha2 * temp_arome[i] 



x = range(24)
plt.plot(x, temp_laf_0)
plt.plot(x, temp_laf_1)
plt.plot(x, temp_laf_low)
plt.plot(x, temp_laf_high)
plt.plot(x, temp_1x1)
plt.plot(x, temp_arome)
plt.plot(x, temp_model_average, lw=4)
plt.grid('on')
plt.savefig('temp.png')

def main():
	temp_arome = np.zeros(24); temp_laf_low = np.zeros(24); temp_laf_high = np.zeros(24)
	temp_arome[:] = [10, 10, 10, 10, 9, 9, 10, 10, 12, 13, 14, 15, 15, 15, 15, 14, 14, 14, 13, 12, 12, 12, 11, 11]
	temp_laf_low[:] = [11, 11, 11, 11, 11, 10, 10, 10, 11, 11, 12, 12, 12, 13, 13, 13, 13, 12, 12, 12, 12, 12, 12, 11]
	temp_laf_high[:] = [8, 8, 8, 7, 7, 6, 6, 6, 9, 12, 17, 19, 22, 24, 24, 24, 24, 24, 23, 21, 16, 11, 8, 8]

	laf_1x1 = 0.9
	laf_arome = 0.3
	laf_3 = 0.5
	laf_5 = 0.6
	laf_7 = 0.6

	print(temp_arome)
	print(temp_laf_low)
	print(temp_laf_high)
	x = range(24)

	plt.plot(x, temp_arome)
	plt.savefig('temp.png')
	plt.show()

#main()
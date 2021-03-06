#Renewable Energy Technology
#Power (and Irradiance) Function
#Calculates power for every 5 minute interval throughout the year

import math as m
import renew as rn

def YearlyPower(lat, long_std, long_loc, beta, gamma, area_panel, n_panels, eff):
	irradiance = []
	power = []
	irradiance_ratio_horiz = []
	theta_i_array = []
	for N in range(1,366):
		# print('day:', N)
		I_0 = rn.I_0(N)
		delta = rn.Declination(N)
		irradiance.append([])
		power.append([])
		irradiance_ratio_horiz.append([])
		theta_i_array.append([])
		for time in range(0,24*12+1):
			solar_time = rn.LocalToSolarTime(time/12, long_std, long_loc, N)
			# print('solar time:', solar_time)
			omega = rn.HourAngle(solar_time)
			# print('hour angle:', omega)
			theta_z = rn.ZenithAngle(delta, lat, omega)
			# print('zenith angle:', theta_z)
			alpha = rn.Altitude(delta, lat, omega)

			#this section accounts for the inverse trig function looking in the wrong quadrant under certain conditions
			gamma_s = rn.SolarAzimuth(delta, omega, alpha)
			if N >= 90 and N <= 266 and N != 1 and gamma_s < gamma_s_old:
				if gamma_s <= 0:
					gamma_s_mod = -180 - gamma_s
				elif gamma_s > 0:
					gamma_s_mod = 180 - gamma_s
			else:
				gamma_s_mod = gamma_s
			# print('gamma_s:', gamma_s)
			# print('gamma_s:', gamma_s_mod)

			theta_i = rn.AngleOfIncidence(alpha, beta, gamma, gamma_s)
			theta_i_array[N-1].append(theta_i)
			# print('angle of incidence:', theta_i)

			if theta_z > 90:
				tau_b = 0
			else:
				tau_b = rn.BeamTransmissivity(theta_z, N)
			# print('beam transmissivity:', tau_b)
			tau_d = rn.DiffuseTransmissivity(tau_b)
			# print('tau_d:', tau_d)

			if theta_i > 90: #if the sun is below the horizon
				I_c_b = 0
			else:
				I_c_b = rn.I_c_b(I_0, tau_b, theta_i)
			# print('I_c_b:', I_c_b)	
			I_c_d = 0	
			I_c_d = rn.I_c_d(tau_d, I_0, theta_z, beta)
			# print('I_c_d:', I_c_d)
			I_c_b_horiz = rn.I_c_b(I_0, tau_b, theta_z) #calculates clear day beam irradiance for a horizontal surface for bullet 4 of case 1
			I_c_d_horiz = rn.I_c_d(tau_d, I_0, theta_z, 0) #calculate clear day diffuse irradiance for a horizontal surface for bullet 4 of case 1
			irradiance_ratio_horiz[N-1].append(I_c_b_horiz/I_c_d_horiz) #calculates the ratio of beam irradiance to diffuse irradiance for bullet 4 of case 1

			if alpha < 0:
				irradiance[N-1].append(0)
			else:
				irradiance[N-1].append(I_c_b + I_c_d)
			power[N-1].append(irradiance[N-1][time]*eff*area_panel*n_panels)

			gamma_s_old = gamma_s
		# print(irradiance[N-1])
	return irradiance, power, irradiance_ratio_horiz, theta_i_array
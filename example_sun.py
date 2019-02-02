import astropy.units as u
from telescopy import Telescope, Filter, BlackBody, Imager, SkyModel
from astropy.constants import R_sun
import numpy as np

T_eff = 5777 * u.K
distance = 1 * u.AU
radius = 1 * R_sun
aperture_diameter = 2 * np.sqrt(1/np.pi) * u.m  # Area = 1 m^2
exp_time = 1 * u.s

target = BlackBody(T_eff, radius, distance)
sky = SkyModel.from_cerro_paranal()
telescope = Telescope(aperture_diameter=aperture_diameter, throughput=0.9)

aperture = np.pi * (telescope.aperture_diameter/2)**2


wavelengths = np.linspace(10, 10000, 1000) * u.nm

delta_lambda = (np.median(np.diff(wavelengths)) *
                np.ones(len(wavelengths)))

import matplotlib.pyplot as plt

plt.plot(wavelengths, target.irradiance(wavelengths))
plt.show()

energy_rate = (target.irradiance(wavelengths) *
               np.pi * u.sr * (target.radius/target.distance)**2
               * delta_lambda)

print(np.sum(energy_rate).to(u.W/u.m**2))
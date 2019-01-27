import astropy.units as u
import matplotlib.pyplot as plt
from telescopy import Telescope, Filter, BlackBody, Imager
from astropy.constants import R_sun

fig, ax = plt.subplots()

T_eff = 2511 * u.K
distance = 12 * u.parsec
radius = 0.11 * R_sun
aperture_diameter = 3.5 * u.m
exp_time = 45 * u.s

r = Filter.from_name('SDSS_z')
target = BlackBody(T_eff, radius, distance)
telescope = Telescope(aperture_diameter=aperture_diameter, throughput=0.9)
imager = Imager(quantum_efficiency=0.8, gain=2)
print('nphotons: \t', imager.counts(telescope, target, exp_time, r))
print('measured: \t', 891164)

# path = '/Users/bmmorris/data/Q2UW01/UT160619/trappist-1.0044.fits'
# (img[560:600, 610:650] - np.median(img[560:600, 610:650])).sum()
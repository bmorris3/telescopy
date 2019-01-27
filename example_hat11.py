import astropy.units as u
from astropy.constants import R_sun
import matplotlib.pyplot as plt
from telescopy import Telescope, Filter, BlackBody, Imager

fig, ax = plt.subplots()

T_eff = 4780 * u.K
distance = 36 * u.parsec
radius = 0.75 * R_sun
aperture_diameter = 3.5 * u.m
exp_time = 5 * u.s

r = Filter.from_name('SDSS_r')
target = BlackBody(T_eff, radius, distance)
telescope = Telescope(aperture_diameter=aperture_diameter, throughput=0.9)
imager = Imager(quantum_efficiency=0.8, gain=2)

print('nphotons: \t', imager.counts(telescope, target, exp_time, r))
print('measured:  \t', 13453145)

# path = '/Users/bmmorris/data/Q2UW01/UT180528/test.0003.fits'
# (img[390:490, 800:930] - np.median(img[390:490, 800:930])).sum()

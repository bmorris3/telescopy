import astropy.units as u
import matplotlib.pyplot as plt
from telescopy import Telescope, Filter, vega, Target, Imager

fig, ax = plt.subplots()

# print(Filter.available_filters())

z = Filter.from_name('SDSS_z')
target = Target(magnitude=21.42, filter=z)
telescope = Telescope(aperture_diameter=3.5*u.m, throughput=1.0)
arctic = Imager(plate_scale=2*0.114*u.arcsec, seeing=1*u.arcsec, binning=3,
                quantum_efficiency=0.5, gain=2)

exposure_duration = 45 * u.s

image = arctic.image(telescope, target, exposure_duration)
print('image sum:    ', image.sum())
print('max:          ', image.max())
print('measured:     ', 891164)
# import matplotlib.pyplot as plt
# plt.imshow(image)
# plt.show()

# path = '/Users/bmmorris/data/Q2UW01/UT160619/trappist-1.0044.fits'
# (img[560:600, 610:650] - np.median(img[560:600, 610:650])).sum()
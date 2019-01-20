import astropy.units as u
import matplotlib.pyplot as plt
from telescopy import Telescope, Filter, vega, Target, Imager

fig, ax = plt.subplots()

# print(Filter.available_filters())

r = Filter.from_name('SDSS_r')
target = Target(magnitude=9.066, filter=r)  # vizier:II/336/apass9
telescope = Telescope(aperture_diameter=3.5*u.m, throughput=0.9)
arctic = Imager(plate_scale=0.114*u.arcsec, seeing=1*u.arcsec, binning=2,
                quantum_efficiency=0.8)

exposure_duration = 5 * u.s

image = arctic.image(telescope, target, exposure_duration)
print('image sum:    ', image.sum())
print('max:          ', image.max())
print('measured:     ', 13453145)
# import matplotlib.pyplot as plt
# plt.imshow(image)
# plt.show()

# path = '/Users/bmmorris/data/Q2UW01/UT180528/test.0003.fits'
# (img[390:490, 800:930] - np.median(img[390:490, 800:930])).sum()

import astropy.units as u
import numpy as np

__all__ = ['Imager']


def gaussian_2d(x, y, x0, y0, std):
    amp = 1/(2*np.pi*std**2)
    return amp * np.exp(-0.5 * ((x - x0)**2 + (y - y0)**2)/std**2)


class Imager(object):
    @u.quantity_input(plate_scale=u.arcsec, seeing=u.arcsec)
    def __init__(self, plate_scale=None, seeing=None, binning=None):
        self.plate_scale = plate_scale
        self.seeing = seeing
        if binning is None:
            binning = 1
        self.binning = binning

    @u.quantity_input(exposure_duration=u.s)
    def image(self, telescope, target, exposure_duration, n=20):
        total_photons = telescope.photons(target, exposure_duration)

        x, y = np.mgrid[:n, :n]
        print('total photons:', total_photons)
        spread = float(self.seeing / self.plate_scale / self.binning)
        img = gaussian_2d(x - n/2, y - n/2, 0, 0, spread) * total_photons

        return np.array(img, dtype=int)

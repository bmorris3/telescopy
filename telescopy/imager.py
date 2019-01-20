import astropy.units as u
import numpy as np

__all__ = ['Imager']


def gaussian_2d(x, y, x0, y0, std):
    amp = 1/(2*np.pi*std**2)
    return amp * np.exp(-0.5 * ((x - x0)**2 + (y - y0)**2)/std**2)


class Imager(object):
    @u.quantity_input(plate_scale=u.arcsec, seeing=u.arcsec)
    def __init__(self, plate_scale=None, seeing=None, binning=None,
                 quantum_efficiency=None, gain=None):
        self.plate_scale = plate_scale
        self.seeing = seeing

        if quantum_efficiency is None:
            quantum_efficiency = 1.0
        self.quantum_efficiency = quantum_efficiency

        if binning is None:
            binning = 1
        self.binning = binning

        if gain is None:
            gain = 1.0
        self.gain = gain

    @u.quantity_input(exposure_duration=u.s)
    def image(self, telescope, target, exposure_duration, n=20):
        total_electrons = (telescope.photons(target, exposure_duration) *
                           self.quantum_efficiency / self.gain)

        x, y = np.mgrid[:n, :n]
        spread = float(self.seeing / self.plate_scale / self.binning)
        img = gaussian_2d(x - n/2, y - n/2, 0, 0, spread) * total_electrons
        return np.array(img, dtype=int)

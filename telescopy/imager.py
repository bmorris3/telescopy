import astropy.units as u
import numpy as np

__all__ = ['Imager']


def gaussian_2d(x, y, x0, y0, std):
    amp = 1/(2*np.pi*std**2)
    return amp * np.exp(-0.5 * ((x - x0)**2 + (y - y0)**2)/std**2)


class Imager(object):
    """
    Container for an imager.
    """
    @u.quantity_input(plate_scale=u.arcsec, seeing=u.arcsec)
    def __init__(self, plate_scale=None, seeing=None, binning=None,
                 quantum_efficiency=None, gain=None):
        """
        Parameters
        ----------
        plate_scale : `~astropy.units.Quantity`
            Plate scale of detector in units of arcsec (per pixel)
        seeing : `~astropy.units.Quantity`
            Astronomical seeing at time of observation
        binning : int
            Pixel binning factor
        quantum_efficiency : float
            Quantum efficiency of the detector
        gain : float
            Gain of the detector (e-'s per ADU)
        """
        self.plate_scale = plate_scale  # arcsec / pixel
        self.seeing = seeing

        if quantum_efficiency is None:
            quantum_efficiency = 1.0
        self.quantum_efficiency = quantum_efficiency

        if binning is None:
            binning = 1
        self.binning = binning  # assumes square?

        if gain is None:
            gain = 1.0
        self.gain = gain  # e- / ADU

    @u.quantity_input(exposure_duration=u.s)
    def image(self, telescope, target, exposure_duration, n=20):
        """
        Generate an image of ``target`` observed by ``telescope``.

        Parameters
        ----------
        telescope : `~telescopy.Telescope`
            Telescope object
        target : `~telescopy.Target`
            Target object
        exposure_duration : `~astropy.units.Quantity`
            Exposure duration (s, or compatible unit)
        n : int
            Pixel length of a side of the image returned

        Returns
        -------
        image : `~numpy.ndarray`
            Simulated image of ``target``.
        """
        total_counts = self.counts(telescope, target, exposure_duration)
        x, y = np.mgrid[:n, :n]
        spread = float(self.seeing / self.plate_scale / self.binning)
        img = gaussian_2d(x - n/2, y - n/2, 0, 0, spread) * total_counts
        return np.array(img, dtype=int)

    def counts(self, telescope, target, exposure_duration):
        """
        Number of ADU detected by the detector.

        Parameters
        ----------
        telescope : `~telescopy.Telescope`
            Telescope object
        target : `~telescopy.Target`
            Target object
        exposure_duration : `~astropy.units.Quantity`
            Exposure duration (s, or compatible unit)

        Returns
        -------
        total_counts : float
            Number of counts estimated in the exposure.
        """
        total_electrons = (telescope.photons(target, exposure_duration) *
                           self.quantum_efficiency)
        total_counts = total_electrons / self.gain
        return total_counts
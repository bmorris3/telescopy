import numpy as np
import os
import astropy.units as u

__all__ = ['SkyModel']


cerro_paranal_X15_path = os.path.join(os.path.dirname(__file__), 'data',
                                      'CerroParanalAdvancedSkyModel_X1.5.txt')

cerro_paranal_X10_path = os.path.join(os.path.dirname(__file__), 'data',
                                      'CerroParanalAdvancedSkyModel_X1.0.txt')


class SkyModel(object):
    def __init__(self, wavelength, transmittance):
        self.wavelength = wavelength
        self.transmittance = transmittance

    @classmethod
    def from_cerro_paranal(cls, airmass=1.0):
        """
        Noll et al. (2012, A&A 543, A92), Jones et al. (2013, A&A 560, A91), Moehler et al. (2014, A&A 568, A9)

        https://www.eso.org/observing/etc/bin/gen/form?INS.MODE=swspectr+INS.NAME=SKYCALC
        """
        if airmass == 1:
            cerro_paranal_path = cerro_paranal_X10_path
        elif airmass == 1.5:
            cerro_paranal_path = cerro_paranal_X15_path
        else:
            raise ValueError('`Airmass` presently only supports X=1 or 1.5.')

        wavelength, transmittance = np.loadtxt(cerro_paranal_path,
                                               unpack=True)
        return cls(wavelength * u.nm, transmittance)

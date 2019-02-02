import numpy as np
import astropy.units as u
from astropy.constants import h, c
from scipy.stats import binned_statistic

__all__ = ['Telescope']


def relative_flux(m1, m2):
    return 10**(0.4 * (m2 - m1))


class Telescope(object):
    """
    Container for information about a telescope.
    """
    @u.quantity_input(aperture_diameter=u.m)
    def __init__(self, aperture_diameter=None, throughput=None):
        """
        Parameters
        ----------
        aperture_diameter : `~astropy.units.Quantity`
            (Effective) Diameter of the primary mirror
        throughput : float
            Telescope throughput
        """
        self.aperture_diameter = aperture_diameter
        self.throughput = throughput

    @u.quantity_input(exposure_duration=u.s)
    def photons(self, target, exposure_duration, filter, sky_model=None):

        delta_lambda = (np.median(np.diff(filter.wavelength)) *
                        np.ones(len(filter.wavelength)))

        if sky_model is not None:
            bins = np.linspace(filter.wavelength.min() - delta_lambda[0]/2,
                               filter.wavelength.max() + delta_lambda[0]/2,
                               len(filter.wavelength)+1)

            sky_bs = binned_statistic(sky_model.wavelength.to(u.Angstrom).value,
                                      sky_model.transmittance,
                                      bins=bins.to(u.Angstrom).value, statistic='mean')
            sky_model_mean = sky_bs.statistic
        else:
            sky_model_mean = np.ones(len(filter.wavelength))

        aperture = np.pi * (self.aperture_diameter/2)**2

        energy_rate = (target.irradiance(filter.wavelength) * sky_model_mean *
                       np.pi * u.sr * (target.radius/target.distance)**2 * aperture *
                       delta_lambda)

        energy = energy_rate * exposure_duration

        nu = c / filter.wavelength
        n_photons_per_wl = (energy / (h * nu)).decompose()

        return int(self.throughput * np.sum(filter.transmissivity * n_photons_per_wl))


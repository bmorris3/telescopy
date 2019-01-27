import numpy as np
import astropy.units as u
from astropy.constants import h, c

from .vega import vega

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

    # @u.quantity_input(exposure_duration=u.s)
    # def photons(self, target, exposure_duration):
    #     """
    #     Compute the number of photons detected in an ``exposure_duration``
    #     exposure of ``target``.
    #
    #     Parameters
    #     ----------
    #     target : `~telescopy.Target`
    #         Target object
    #     exposure_duration : `~astropy.units.Quantity`
    #         Length of the exposure
    #
    #     Returns
    #     -------
    #     n_photons : int
    #         Number of photons observed.
    #     """
    #     flux_scale = relative_flux(target.magnitude,
    #                                vega.mag(target.filter.name))
    #
    #     telescope_aperture = np.pi * (self.aperture_diameter / 2)**2
    #     energy = (flux_scale * vega.integrate_filter(target.filter) *
    #               telescope_aperture * self.throughput * exposure_duration)
    #     nu = c / target.filter.lam0
    #     n_photons = int(energy / (h * nu))
    #     return n_photons

    @u.quantity_input(exposure_duration=u.s)
    def photons(self, target, exposure_duration, filter):
        delta_lambda = np.median(np.diff(filter.wavelength))

        aperture = np.pi * (self.aperture_diameter/2)**2

        energy_rate = (target.irradiance(filter.wavelength) * np.pi * u.sr *
                       (target.radius/target.distance)**2 * aperture * delta_lambda)

        energy = energy_rate * exposure_duration

        nu = c / filter.wavelength
        n_photons_per_wl = (energy / (h * nu)).decompose()

        return int(self.throughput * np.sum(filter.transmissivity * n_photons_per_wl))


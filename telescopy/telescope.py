import numpy as np
import astropy.units as u
from astropy.constants import h, c

from .vega import vega

__all__ = ['Telescope', 'Target']


def relative_flux(m1, m2):
    return 10**(0.4 * (m2 - m1))


class Telescope(object):
    @u.quantity_input(aperture_diameter=u.m)
    def __init__(self, aperture_diameter=None, throughput=None):
        self.aperture_diameter = aperture_diameter
        self.throughput = throughput

    @u.quantity_input(exposure_duration=u.s)
    def photons(self, target, exposure_duration):
        flux_scale = relative_flux(target.magnitude,
                                   vega.mag(target.filter.name))

        telescope_aperture = np.pi * (self.aperture_diameter / 2)**2
        energy = (flux_scale * vega.integrate_filter(target.filter) *
                  telescope_aperture * self.throughput * exposure_duration)
        nu = c / target.filter.lam0
        n_photons = int((energy / (h * nu)).decompose())
        return n_photons


class Target(object):
    def __init__(self, magnitude=None, filter=None):
        self.magnitude = magnitude
        self.filter = filter

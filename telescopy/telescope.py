import numpy as np
import astropy.units as u
from astropy.constants import h, c

from .vega import vega

__all__ = ['Telescope', 'Target']


def relative_flux(m1, m2):
    return 10**(-0.4 * (m1 - m2))


class Telescope(object):
    @u.quantity_input(aperture_diameter=u.m)
    def __init__(self, aperture_diameter=None):
        self.aperture = aperture_diameter

    @u.quantity_input(exposure_duration=u.s)
    def photons(self, target, exposure_duration):
        flux_scale = relative_flux(target.magnitude,
                                   vega.mag(target.filter.name))
        photon = (flux_scale * vega.integrate_filter(target.filter) *
                  (self.aperture/2)**2)
        nu = c / target.filter.lam0
        return (exposure_duration * photon / (h * nu) ).decompose()

class Target(object):
    def __init__(self, magnitude=None, filter=None):
        self.magnitude = magnitude
        self.filter = filter

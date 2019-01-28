from astropy.modeling.blackbody import blackbody_lambda
import astropy.units as u
import numpy as np

__all__ = ['BlackBody']


class BlackBody(object):
    @u.quantity_input(T_eff=u.K, distance=u.m)
    def __init__(self, T_eff, radius, distance):
        """
        Parameters
        ----------
        T_eff : `~astropy.units.Quantity`
            Effective temperature of the blackbody
        distance : `~astropy.units.Quantity`
            Distance to the blackbody
        """

        self.irradiance = lambda x: blackbody_lambda(x, T_eff) * u.sr
        self.radius = radius
        self.distance = distance
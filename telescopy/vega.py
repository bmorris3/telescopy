import os
from astropy.io import fits
import matplotlib.pyplot as plt
import astropy.units as u
import numpy as np
from json import load

__all__ = ['vega']

vega_path = os.path.join(os.path.dirname(__file__), 'data',
                         'alpha_lyr_stis_008.fits')

mags_path = os.path.join(os.path.dirname(__file__), 'data', 'mags', 'vega.json')


class Vega(object):
    def __init__(self):
        vega = fits.getdata(vega_path)
        self.wavelength = vega['WAVELENGTH'] * u.Angstrom
        self.flux = vega['FLUX'] * u.erg / u.s / u.cm**2 / u.Angstrom

    def plot(self, ax=None):
        if ax is None:
            fig, ax = plt.subplots()
        ax.semilogx(self.wavelength, self.flux)
        ax.set(xlabel='Wavelength [Angstrom]',
               ylabel=r'$F_\lambda$ [{0}]'.format(self.flux.unit))
        return ax

    def integrate_filter(self, filter):
        interp_transmissivity = np.interp(self.wavelength, filter.wavelength,
                                          filter.transmissivity,
                                          left=0, right=0)
        flux = self.flux * self.wavelength * interp_transmissivity
        return np.sum(flux)

    def mag(self, filter_name):
        return load(open(mags_path))[filter_name]

vega = Vega()

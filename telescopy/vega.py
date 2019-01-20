import os
from astropy.io import fits
import matplotlib.pyplot as plt
import astropy.units as u
import numpy as np
from json import load

__all__ = ['vega']

vega_path = os.path.join(os.path.dirname(__file__), 'data',
                         'alpha_lyr_stis_008.fits')

# https://classic.sdss.org/dr7/algorithms/sdssUBVRITransform.html#vega_sun_colors
mags_path = os.path.join(os.path.dirname(__file__), 'data', 'mags', 'vega.json')


class Vega(object):
    """
    Container object for the spectrum of Vega.
    """
    def __init__(self):
        # TODO: lazy load
        vega = fits.getdata(vega_path)
        self.wavelength = vega['WAVELENGTH'] * u.Angstrom
        self.flam = vega['FLUX'] * u.erg / u.s / u.cm**2 / u.Angstrom
        self._mags = None

    def plot(self, ax=None):
        """
        Plot Vega's flux-calibrated spectrum.

        Parameters
        ----------
        ax : `~matplotlib.pyplot.Axes` or None
            Axis object.

        Returns
        -------
        ax : `~matplotlib.pyplot.Axes`
            Plot with spectrum  of Vega
        """
        if ax is None:
            fig, ax = plt.subplots()
        ax.semilogx(self.wavelength, self.flam)
        ax.set(xlabel='Wavelength [Angstrom]',
               ylabel=r'$F_\lambda$ [{0}]'.format(self.flux.unit))
        return ax

    def integrate_filter(self, filter):
        """
        Integrate Vega's spectral flux density within ``filter``.

        Parameters
        ----------
        filter : `~telescopy.Filter`
            Filter object

        Returns
        -------
        flux : `~astropy.units.Quantity`
            Flux within ``filter``
        """
        interp_transmissivity = np.interp(self.wavelength, filter.wavelength,
                                          filter.transmissivity,
                                          left=0, right=0)
        flux = self.flam * self.wavelength * interp_transmissivity
        return np.sum(flux)

    def mag(self, filter_name):
        """
        Vega's magnitude in filter ``filter_name``

        Parameters
        ----------
        filter_name : str
            Name of filter. Must be one of the filters returned by
            `~telescopy.Filter.available_filters()`.

        Returns
        -------
        mag : float
            Magnitude of Vega in ``filter_name``
        """
        if self._mags is None:
            self._mags = load(open(mags_path))
        return self._mags[filter_name]

vega = Vega()

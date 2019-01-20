import os
from glob import glob
import numpy as np
import astropy.units as u
import matplotlib.pyplot as plt

__all__ = ['Filter']


filter_path = os.path.join(os.path.dirname(__file__), 'data', 'filters')


class Filter(object):
    """
    Transmissivity curve for a filter.
    """
    def __init__(self, wavelength=None, transmissivity=None, path=None,
                 name=None):
        """
        Parameters
        ----------
        wavelength : `~astropy.units.Quantity`
            Wavelength array for the transmissivity curve.
        transmissivity : `~numpy.ndarray`
            Transmissivity of the filter
        path : str
            Path to text transmissivity file
        name : str
            Name of the filter
        """
        self.path = path
        self.name = name

        if path is not None:
            wavelength, transmissivity = np.loadtxt(self.path, unpack=True)
            self.wavelength = wavelength * u.Angstrom
            self.transmissivity = transmissivity
        else:
            self.wavelength = wavelength
            self.transmissivity = transmissivity

        self.lam0 = (np.sum(wavelength * transmissivity) /
                     np.sum(transmissivity) * u.Angstrom)

    @classmethod
    def from_name(cls, name):
        """
        Transmissivity of a built-in filter.

        Parameters
        ----------
        name : str
            Must be one of the filters returned by
            `~telescopy.Filter.available_filters()`.
        """
        path = os.path.join(filter_path, '*' + name.replace('_', '.') + '.txt')
        globbed_path = glob(path)
        if len(globbed_path) < 1:
            raise ValueError('No filter found matching name "{0}"'.format(name))
        return cls(path=globbed_path[0], name=name)

    @staticmethod
    def available_filters():
        """
        Available filters stored in telescopy.

        Returns
        -------
        filters : list
            List of available filter names
        """
        return [i.split('_')[1].replace('.', '_')[:-4]
                for i in glob(os.path.join(filter_path, '*'))]

    def plot(self, ax=None):
        """
        Plot the transmissivity curve of a filter

        Parameters
        ----------
        ax : `~matplotlib.pyplot.Axes` or None
            Axis object.

        Returns
        -------
        ax : `~matplotlib.pyplot.Axes`
            Plot with transmissivity curve
        """
        if ax is None:
            fig, ax = plt.subplots()
        ax.plot(self.wavelength, self.transmissivity)
        ax.set(xlabel='Wavelength [Angstrom]', ylabel='Transmissivity')
        return ax
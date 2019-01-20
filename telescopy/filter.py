import os
from glob import glob
import numpy as np
import astropy.units as u
import matplotlib.pyplot as plt

__all__ = ['Filter']


filter_path = os.path.join(os.path.dirname(__file__), 'data', 'filters')


class Filter(object):
    def __init__(self, path, name=None):
        self.path = path
        self.name = name
        wavelength, transmissivity = np.loadtxt(self.path, unpack=True)
        self.wavelength = wavelength * u.Angstrom
        self.transmissivity = transmissivity
        self.lam0 = np.sum(wavelength * transmissivity) / np.sum(transmissivity) * u.Angstrom

    @classmethod
    def from_name(cls, name):
        path = os.path.join(filter_path, '*' + name.replace('_', '.') + '.txt')
        globbed_path = glob(path)
        if len(globbed_path) < 1:
            raise ValueError('No filter found matching name "{0}"'.format(name))
        return cls(globbed_path[0], name=name)

    def plot(self, ax=None):
        if ax is None:
            fig, ax = plt.subplots()
        ax.plot(self.wavelength, self.transmissivity)
        ax.set(xlabel='Wavelength [Angstrom]', ylabel='Transmissivity')
        return ax

    @staticmethod
    def available_filters():
        return [i.split('_')[1].replace('.', '_')[:-4]
                for i in glob(os.path.join(filter_path, '*'))]

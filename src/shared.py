import numpy as np


""" ******************** Constantes ******************** """


π = np.pi


""" ******************** Formularios ******************** """


""" ******************** Modelos ******************** """


class Parameter:

    def __init__(self, label, value, unit, description=""):
        self.label = label
        self.value = value
        self.description = description
        self.unit = unit

    def is_value(self):
        return self.value * self.unit


class Spectrometer:

    def __init__(self, params):

        self.min_wavelength = params["min_wavelength"].is_value()
        self.λmin = self.min_wavelength

        self.max_wavelength = params["max_wavelength"].is_value()
        self.λmax = self.max_wavelength

        self.num_pixels = params["num_pixels"].is_value()
        self.N = self.num_pixels

        self.integration_time = params["integration_time"].is_value()
        self.T = self.integration_time

        self.OPDlen = self.N + params["zero_padding"].is_value()

        self.dt = self.T * 1e-3

        self.wavelength = np.linspace(self.λmin, self.λmax, self.N)
        self.λ = self.wavelength

        self.spectral_range = self.λmax - self.λmin
        self.Δλ = self.spectral_range

        self.pixel_resolution = (self.λmax - self.λmax) / self.N
        self.dλ = self.pixel_resolution

        self.wavenumber = np.flip(2*π / self.λ)
        self.k = self.wavenumber

        self.kmin = self.k[0]

        self.kmax = self.k[-1]

        self.Δk = self.kmax - self.kmin

        self.wavenumber_es = np.linspace(self.kmin, self.kmax, self.N)
        self.k_es = self.wavenumber_es

        self.dk = self.k_es[1] - self.k_es[0]

        self.OPDmin = 2*π / self. Δk

        self.OPDmax = π / self.dk

        self.OPD = np.linspace(self.OPDmin, self.OPDmax, self.OPDlen)

        self.ΔOPD = self.OPDmax - self.OPDmin

        self.dOPD = self.OPD[1] - self.OPD[0]


class Interface:

    def __init__(self):

        self.spectrometer_params = {
            "min_wavelength": Parameter("Longitud de onda mínima [nm]", 770, unit=1e-9),
            "max_wavelength": Parameter("Longitud de onda máxima [nm]", 930, unit=1e-9),
            "num_pixels": Parameter("Número de píxeles", 2048, unit=1),
            "integration_time": Parameter("Tiempo de integración [us]", 100, unit=1e-6),
            "zero_padding": Parameter("Agregar ceros", 0, unit=1)
        }

        self.spectrometer = Spectrometer(self.spectrometer_params)

    def set_spectrometer(self, key, value):
        self.spectrometer_params[key].value = value
        self.spectrometer = Spectrometer(self.spectrometer_params)
        return True

    def update_plot(self, t):
        pass

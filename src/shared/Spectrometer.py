import numpy as np
from .functions import ISU_value


class Spectrometer:

    def __init__(self):

        min_wavelength = {
            "args": {
                "label": "Min. wavelength [nm]",
                "min_value": 0,
                "default_value": 770,
            },
            "unit": 1e-9,
            "value": 770,
            "type": "input_int"
        }

        max_wavelength = {
            "args": {
                "label": "Max. wavelength [nm]",
                "min_value": 0,
                "default_value": 930,
            },
            "unit": 1e-9,
            "value": 930,
            "type": "input_int"
        }

        num_pixels = {
            "args": {
                "label": "Num. pixels",
                "min_value": 1,
                "default_value": 2048,
            },
            "value": 2048,
            "type": "input_int"
        }

        zero_padding = {
            "args": {
                "label": "0 padding",
                "min_value": 0,
                "default_value": 0,
            },
            "value": 0,
            "type": "input_int"
        }

        self.parameters = {
            "min_wavelength": min_wavelength,
            "max_wavelength": max_wavelength,
            "num_pixels": num_pixels,
            "zero_padding": zero_padding
        }

        self.min_wavelength = lambda: ISU_value(
            self.parameters["min_wavelength"])
        self.λmin = self.min_wavelength

        self.max_wavelength = lambda: ISU_value(
            self.parameters["max_wavelength"])
        self.λmax = self.max_wavelength

        self.num_pixels = lambda: ISU_value(self.parameters["num_pixels"])
        self.N = self.num_pixels

        self.OPDlen = lambda: self.N(
        ) + ISU_value(self.parameters["zero_padding"])

        self.wavelength = lambda: np.linspace(
            self.λmin(), self.λmax(), self.N())
        self.λ = self.wavelength

        self.spectral_range = lambda: self.λmax() - self.λmin()
        self.Δλ = self.spectral_range

        self.pixel_resolution = lambda: (self.λmax() - self.λmin()) / self.N()
        self.dλ = self.pixel_resolution

        self.wavenumber = lambda: np.flip(2*np.pi / self.λ())

        p = np.array(range(2048))
        C0 = 7.94223e2
        C1 = 4.62979e-2
        C2 = -2.60004e-6
        C3 = -1.48385e-11
        self.wavelength = C0 + C1 * p + C2 * p**2 + C3 * p**3
        self.k = lambda: 2*np.pi / wavelength

        self.kmin = lambda: self.k()[0]

        self.kmax = lambda: self.k()[-1]

        self.Δk = lambda: self.kmax() - self.kmin()

        self.wavenumber_es = lambda: np.linspace(
            self.kmin(), self.kmax(), self.N())
        self.k_es = self.wavenumber_es

        self.dk = lambda: self.k_es()[1] - self.k_es()[0]

        self.OPDmin = lambda: 2*np.pi / self.Δk()

        self.OPDmax = lambda: np.pi / self.dk()

        self.OPD = lambda: np.linspace(
            self.OPDmin(), self.OPDmax(), self.OPDlen())

        self.ΔOPD = lambda: self.OPDmax() - self.OPDmin()

        self.dOPD = lambda: self.OPD()[1] - self.OPD()[0]

    def set_parameter(self, key: str, value):
        self.parameters[key]["value"] = value

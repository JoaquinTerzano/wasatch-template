import numpy as np
from ..shared import ISU_value


class CoherentLightSource:

    def __init__(self):

        central_wavelength = {
            "args": {
                "label": "Central wavelength [nm]",
                "min_value": 0,
                "default_value": 850,
            },
            "unit": 1e-9,
            "value": 850,
            "type": "input_int"
        }

        spectral_bandwidth = {
            "args": {
                "label": "Spectral bandwidth [nm]",
                "min_value": 0,
                "default_value": 80,
            },
            "unit": 1e-9,
            "value": 80,
            "type": "input_int"
        }

        power = {
            "args": {
                "label": "Power",
                "min_value": 0,
                "default_value": 1000000000,
            },
            "unit": 1,
            "value": 1000000000,
            "type": "input_int"
        }

        self.parameters = {
            "central_wavelength": central_wavelength,
            "spectral_bandwidth": spectral_bandwidth,
            "power": power
        }

        self.central_wavelength = lambda: ISU_value(
            self.parameters["central_wavelength"])
        self.λc = self.central_wavelength

        self.spectral_bandwidth = lambda: ISU_value(
            self.parameters["spectral_bandwidth"])
        self.Δλ = self.spectral_bandwidth

        self.power = lambda: ISU_value(self.parameters["power"])
        self.P = self.power

    def set_parameter(self, key: str, value):
        self.parameters[key]["value"] = value

    def A(self, λ):
        # Usa la función de densidad de la distribución normal
        def G(μ, σ): return lambda x: 1 / np.sqrt(2*np.pi) * \
            np.exp(-(x - μ)**2 / (2*σ**2))
        μ = self.λc()
        σ = self.Δλ() / (2*np.sqrt(2*np.log(2)))
        return self.P() * G(μ, σ)(λ) * np.random.normal(μ, σ, len(λ))

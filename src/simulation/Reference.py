import numpy as np
from ..shared import ISU_value

optical_distance = {
    "args": {
        "label": "OD [um]",
        "min_value": 0,
        "default_value": 700,
    },
    "unit": 1e-6,
    "value": 700,
    "type": "input_int",
    "tooltip": "Optical distance"
}

intensity_factor = {
    "args": {
        "label": "Intensity [%]",
        "min_value": 0,
        "max_value": 100,
        "default_value": 33,
    },
    "unit": 1e-2,
    "value": 33,
    "type": "input_int"
}

vibration_frequency = {
    "args": {
        "label": "Freq. [Hz]",
        "min_value": 0,
        "default_value": 44000,
    },
    "unit": 1,
    "value": 44000,
    "type": "input_int",
    "tooltip": "Vibration frequency"
}

vibration_amplitude = {
    "args": {
        "label": "Amplitude [um]",
        "min_value": 0,
        "default_value": 20,
    },
    "unit": 1e-6,
    "value": 20,
    "type": "input_int",
    "tooltip": "Vibration amplitude"
}

reference_parameters = {
    "optical_distance": optical_distance,
    "intensity_factor": intensity_factor,
    "vibration_frequency": vibration_frequency,
    "vibration_amplitude": vibration_amplitude
}


class Reference:

    def __init__(self, parameters):

        self.parameters = parameters

        self.x = lambda: ISU_value(self.parameters["optical_distance"])

        self.intensity_factor = lambda: ISU_value(
            self.parameters["intensity_factor"])

        self.Ω = lambda: ISU_value(self.parameters["vibration_frequency"])

        self.β = lambda: ISU_value(self.parameters["vibration_amplitude"])

    def set_parameter(self, key: str, value):
        self.parameters[key]["value"] = value

    def α(self, t):
        return self.x() - self.β() * np.sin(self.Ω() * t)

    def A(self, source):
        return lambda λ: self.intensity_factor() * source.A(λ)

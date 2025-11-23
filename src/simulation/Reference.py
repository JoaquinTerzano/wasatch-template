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


def A(reference, source):
    return lambda λ: ISU_value(reference["intensity_factor"]) * source.A(λ)


def α(reference, t):
    Ω = ISU_value(reference["vibration_frequency"])
    β = ISU_value(reference["vibration_amplitude"])
    x = ISU_value(reference["optical_distance"])
    return x - β * np.sin(Ω * t)


class Reference:

    def __init__(self, parameters):
        self.parameters = parameters

    def set_parameter(self, key: str, value):
        self.parameters[key]["value"] = value

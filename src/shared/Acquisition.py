import numpy as np
from .functions import ISU_value


class Acquisition:

    def __init__(self):

        min_opd = {
            "args": {
                "label": "Min. OPD [um]",
                "min_value": 0,
                "default_value": 900,
            },
            "unit": 1e-6,
            "value": 900,
            "type": "input_int"
        }

        max_opd = {
            "args": {
                "label": "Max. OPD [um]",
                "min_value": 1,
                "default_value": 1100,
            },
            "unit": 1e-6,
            "value": 1100,
            "type": "input_int"
        }

        acq_time = {
            "args": {
                "label": "Acq. time [ms]",
                "min_value": 1,
                "default_value": 5000,
            },
            "unit": 1e-3,
            "value": 5000,
            "type": "input_int"
        }

        self.parameters = {
            "min_opd": min_opd,
            "max_opd": max_opd,
            "acq_time": acq_time
        }

        self.acq_name = "data"

        self.T = lambda: ISU_value(self.parameters["acq_time"])

        self.min_opd = lambda: ISU_value(
            self.parameters["min_opd"])

        self.max_opd = lambda: ISU_value(
            self.parameters["max_opd"])

    def set_parameter(self, key: str, value):
        self.parameters[key]["value"] = value

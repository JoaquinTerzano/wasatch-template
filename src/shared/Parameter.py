

def is_value(parameter):
    value = parameter["value"]
    if "unit" in parameter:
        value *= parameter["unit"]
    return value


class Parameter:

    def __init__(self, label, default_value, unit, min, max, tooltip="", type="input", pow=1):
        self.label = label
        self.value = default_value
        self.unit = unit
        self.tooltip = tooltip
        self.pow = pow

    def is_value(self):
        return self.value**self.pow * self.unit

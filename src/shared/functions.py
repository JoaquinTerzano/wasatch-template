
# International System Units
def ISU_value(parameter):
    value = parameter["value"]
    if "unit" in parameter:
        value *= parameter["unit"]
    return value

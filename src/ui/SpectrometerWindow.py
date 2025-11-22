import dearpygui.dearpygui as dpg
from .ParametersForm import ParametersForm


def SpectrometerWindow(interface):
    return ParametersForm(interface)

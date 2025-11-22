import dearpygui.dearpygui as dpg
from .Logs import log


def ParametersForm(interface):

    def parameter_callback(sender, app_data, user_data):
        log(interface.set_parameter(user_data, app_data))

    with dpg.group(width=100) as ParametersForm:

        for key, parameter in interface.parameters.items():

            args = {arg: val for arg, val in parameter["args"].items()}
            args |= {"user_data": key, "callback": parameter_callback}

            match parameter["type"]:
                case "input_int": dpg.add_input_int(**args)
                case "slider_int": dpg.add_slider_int(**args)

            if "tooltip" in parameter:
                with dpg.tooltip(dpg.last_item()):
                    dpg.add_text(parameter["tooltip"])

    return ParametersForm

import dearpygui.dearpygui as dpg
from .Logs import log


def AcquisitionWindow(cam_interface):

    with dpg.group(width=100) as AcquisitionWindow:

        dpg.add_text("Acquisition")

        def acqtime_callback(sender, app_data, user_data):
            log(cam_interface.set_acq_time(app_data))

        args = cam_interface.acq_time["args"]
        dpg.add_input_int(
            label=args["label"],  default_value=args["default_value"], callback=acqtime_callback)
        if "tooltip" in cam_interface.acq_time:
            with dpg.tooltip(dpg.last_item()):
                dpg.add_text(cam_interface.acq_time["tooltip"])

        def acqname_callback(sender, app_data, user_data):
            cam_interface.acq_name = app_data

        dpg.add_input_text(label="Acq. name",
                           default_value="data", callback=acqname_callback)

        def acquire_callback(sender, app_data, user_data):
            dpg.set_item_label(sender, "Acquiring...")
            log(cam_interface.acquire())
            dpg.set_item_label(sender, "Acquire")

        dpg.add_button(label="Acquire", callback=acquire_callback)

    return AcquisitionWindow

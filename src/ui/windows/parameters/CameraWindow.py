import dearpygui.dearpygui as dpg
from ..shared import ParametersForm, log


def CameraWindow(interface):

    with dpg.child_window(border=False) as CameraWindow:

        def list_cameras_callback(sender, app_data, user_data):
            cameras = interface.list_cameras()
            if cameras:
                dpg.configure_item(
                    "CameraListbox", items=cameras)
            else:
                log("no cameras detected\n")

        dpg.add_button(label="List cameras", callback=list_cameras_callback)

        dpg.add_listbox(tag="CameraListbox")

        dpg.add_separator()

        _ = ParametersForm(interface)

    return CameraWindow

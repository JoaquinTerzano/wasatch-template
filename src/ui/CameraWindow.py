import dearpygui.dearpygui as dpg
from .ParametersForm import ParametersForm
from .Logs import log


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

        def select_camera_callback(sender, app_data, user_data):
            log(interface.select_cam(app_data))

        dpg.add_listbox(tag="CameraListbox", callback=select_camera_callback)

        dpg.add_separator()

        _ = ParametersForm(interface)

    return CameraWindow

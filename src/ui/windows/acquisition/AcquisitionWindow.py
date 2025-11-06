import dearpygui.dearpygui as dpg


def AcquisitionWindow(cam_interface):

    dpg.add_text("Acquisition")

    def acqtime_callback(sender, app_data, user_data):
        cam_interface.acq_time = app_data

    dpg.add_input_int(width=100, label="acq_time",
                      default_value=100, callback=acqtime_callback)

    def acquire_callback(sender, app_data, user_data):
        dpg.set_item_label(sender, "Acquiring...")
        cam_interface.acquire()
        dpg.set_item_label(sender, "Acquire")

    dpg.add_button(label="Acquire", callback=acquire_callback)

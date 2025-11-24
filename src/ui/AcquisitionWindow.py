import dearpygui.dearpygui as dpg
from .Logs import log
from .ParametersForm import ParametersForm
from .Plots import plot_acquisition


def AcquisitionWindow(acq_interface, cam_interface, sim_interface, spectrometer):

    with dpg.group(width=100) as AcquisitionWindow:

        Acquisition_ = ParametersForm(acq_interface)

        def acqname_callback(sender, app_data, user_data):
            acq_interface.acq_name = app_data

        dpg.add_input_text(label="Acq. name",
                           default_value="data", callback=acqname_callback)

        def acquire_callback(sender, app_data, user_data):
            dpg.set_item_label(sender, "Acquiring...")
            log(cam_interface.acquire(acq_interface))
            log(sim_interface.acquire(acq_interface, cam_interface, spectrometer))
            plot_acquisition(spectrometer, cam_interface,
                             sim_interface, acq_interface)
            dpg.set_item_label(sender, "Acquire")

        dpg.add_button(label="Acquire", callback=acquire_callback)

    return AcquisitionWindow

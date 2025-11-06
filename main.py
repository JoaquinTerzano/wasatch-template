import dearpygui.dearpygui as dpg
from src.ui import *
from src.shared import *
from src.wasatch import *
from src.simulation import *


def main():

    viewport = {
        "title": "Wasatch",
        "width": 960,
        "height": 640,
        "height_upper": 480
    }

    dpg.create_context()
    dpg.create_viewport(title=viewport["title"],
                        width=viewport["width"],
                        height=viewport["height"])

    spectrometer, cam_interface, sim_interface = Spectrometer(
    ), WasatchCamera(), SimulationCamera()

    main_window = MainWindow(spectrometer, cam_interface, sim_interface)

    update(spectrometer, cam_interface, sim_interface, 0.)

    dpg.setup_dearpygui()

    dpg.set_primary_window(main_window, True)

    dpg.show_viewport()
    dpg.start_dearpygui()

    dpg.destroy_context()


if __name__ == "__main__":
    main()

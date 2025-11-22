import dearpygui.dearpygui as dpg
import src.ui as ui
import src.shared as shared
import src.wasatch as wasatch
import src.simulation as simulation


def main():

    viewport = {
        "title": "Wasatch",
        "width": 960,
        "height": 660,
        "height_upper": 480
    }

    dpg.create_context()
    dpg.create_viewport(title=viewport["title"],
                        width=viewport["width"],
                        height=viewport["height"])

    spectrometer, cam_interface, sim_interface = shared.Spectrometer(
    ), wasatch.WasatchCamera(), simulation.SimulationCamera()

    main_window = ui.MainWindow(spectrometer, cam_interface, sim_interface)

    ui.update(spectrometer, cam_interface, sim_interface, 0.)

    dpg.setup_dearpygui()

    dpg.set_primary_window(main_window, True)

    dpg.show_viewport()
    dpg.start_dearpygui()

    dpg.destroy_context()


if __name__ == "__main__":
    main()

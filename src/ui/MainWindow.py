import dearpygui.dearpygui as dpg
from .AcquisitionWindow import AcquisitionWindow
from .CameraWindow import CameraWindow
from .Logs import LogsWindow
from .Plots import PlotWindow
from .SimulationWindow import SimulationWindow
from .SpectrometerWindow import SpectrometerWindow


def MainWindow(spectrometer, cam_interface, sim_interface):

    with dpg.window() as MainWindow:

        with dpg.table(header_row=False, resizable=True):

            dpg.add_table_column(init_width_or_weight=0.3)
            dpg.add_table_column(init_width_or_weight=0.7)

            with dpg.table_row():

                """ ******************** 1ra columna ******************** """

                with dpg.child_window(border=False):

                    """ ******************** 2do cuadrante ******************** """

                    with dpg.child_window(height=480):
                        with dpg.tab_bar():

                            with dpg.tab(label="Camera"):
                                _ = CameraWindow(cam_interface)

                            with dpg.tab(label="Simulation"):
                                _ = SimulationWindow(sim_interface)

                            with dpg.tab(label="Spectrometer"):
                                _ = SpectrometerWindow(spectrometer)

                    """ ******************** 3er cuadrante ******************** """

                    with dpg.child_window():
                        _ = AcquisitionWindow(cam_interface)

                """ ******************** 2da columna ******************** """

                with dpg.child_window(border=False):

                    """ ******************** 1er cuadrante ******************** """

                    with dpg.child_window(height=480):
                        with dpg.tab_bar():

                            with dpg.tab(label="Wavenumber"):
                                _ = PlotWindow("WavenumberAcq",
                                               "Acquired", "Wavenumber [1/m]")
                                _ = PlotWindow("WavenumberSim",
                                               "Simulated", "Wavenumber [1/m]")

                            with dpg.tab(label="OPD"):
                                _ = PlotWindow("OPDAcq",
                                               "Acquired", "OPD [um]")
                                _ = PlotWindow("OPDSim",
                                               "Simulated", "OPD [um]")

                    """ ******************** 4to cuadrante ******************** """

                    with dpg.child_window():
                        _ = LogsWindow()

    return MainWindow

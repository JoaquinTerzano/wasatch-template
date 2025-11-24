import dearpygui.dearpygui as dpg
from .AcquisitionWindow import AcquisitionWindow
from .CameraWindow import CameraWindow
from .Logs import LogsWindow
from .Plots import PlotWindow
from .SimulationWindow import SimulationWindow
from .SpectrometerWindow import SpectrometerWindow


def MainWindow(spectrometer, cam_interface, sim_interface, acq_interface):

    with dpg.window() as MainWindow:

        with dpg.table(header_row=False, resizable=True):

            dpg.add_table_column(init_width_or_weight=0.3)
            dpg.add_table_column(init_width_or_weight=0.7)

            with dpg.table_row():

                """ ******************** 1ra columna ******************** """

                with dpg.child_window(border=False):

                    with dpg.child_window():
                        with dpg.tab_bar():

                            with dpg.tab(label="Camera"):
                                Camera = CameraWindow(cam_interface)

                            with dpg.tab(label="Simulation"):
                                Simulation = SimulationWindow(sim_interface)

                            with dpg.tab(label="Spectrometer"):
                                Spectrometer = SpectrometerWindow(spectrometer)

                            with dpg.tab(label="Acquisition"):
                                Acquisition = AcquisitionWindow(
                                    acq_interface, cam_interface, sim_interface, spectrometer)

                """ ******************** 2da columna ******************** """

                with dpg.child_window(border=False):

                    with dpg.child_window():
                        with dpg.tab_bar():

                            with dpg.tab(label="Wavenumber"):
                                WavenumberAcq = PlotWindow("WavenumberAcq",
                                                           "Acquired", "Wavenumber [1/m]")
                                WavenumberSim = PlotWindow("WavenumberSim",
                                                           "Simulated", "Wavenumber [1/m]")

                            with dpg.tab(label="OPD"):
                                OPDAcq = PlotWindow("OPDAcq",
                                                    "Acquired", "OPD [um]")
                                OPDSim = PlotWindow("OPDSim",
                                                    "Simulated", "OPD [um]")

                            with dpg.tab(label="OPD_time"):
                                OPD_time_Acq = PlotWindow(
                                    "OPD_time_Acq", "Acquired", "Time [s]")
                                OPD_time_Sim = PlotWindow(
                                    "OPD_time_Sim", "Simulated", "Time [s]")

    return MainWindow

import dearpygui.dearpygui as dpg
import numpy as np


def update(spectrometer, cam_interface, sim_interface, t):
    t += dpg.get_delta_time()

    update_plots(spectrometer, cam_interface, sim_interface, t)

    dpg.set_frame_callback(dpg.get_frame_count() + 60,
                           lambda: update(spectrometer, cam_interface, sim_interface, t))


def update_plots(spectrometer, cam_interface, sim_interface, t):
    k = spectrometer.k()
    OPD = spectrometer.OPD()

    dpg.set_value("WavenumberAcq", [k.tolist(), cam_interface.I().tolist()])
    dpg.set_value("WavenumberSim", [k.tolist(),
                  sim_interface.I(spectrometer, t).tolist()])

    def fft(I): return np.abs(np.fft.fft(I, spectrometer.OPDlen()))
    l, r = 5, len(k)//2
    dpg.set_value("OPDAcq", [(OPD[l:r]*1e6).tolist(),
                  fft(cam_interface.I())[l:r].tolist()])
    dpg.set_value("OPDSim", [(OPD[l:r]*1e6).tolist(),
                  fft(sim_interface.I(spectrometer, t))[l:r].tolist()])

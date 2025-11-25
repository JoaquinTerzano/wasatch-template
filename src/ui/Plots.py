import dearpygui.dearpygui as dpg
import numpy as np
from scipy.interpolate import interp1d
from scipy.signal import zoom_fft


def update(spectrometer, cam_interface, sim_interface, acq_interface, t):
    t_ = t
    t += dpg.get_delta_time()

    update_plots(spectrometer, cam_interface, sim_interface, acq_interface, t)

    dpg.set_frame_callback(dpg.get_frame_count() + 10,
                           lambda: update(spectrometer, cam_interface, sim_interface, acq_interface, t))


def update_plots(spectrometer, cam_interface, sim_interface, acq_interface, t):
    k = spectrometer.k()
    k_es = spectrometer.k_es()
    opd = spectrometer.OPD()
    zl = spectrometer.OPDmin()
    zr = spectrometer.OPDmax()
    n = spectrometer.OPDlen()
    opd = spectrometer.OPD()
    dopd = spectrometer.dOPD()
    l = int((zl - opd[0]) / dopd)
    r = int((zr - opd[0]) / dopd)

    def fft(irr):
        irr_es = interp1d(k, irr)(k_es)
        return np.abs(zoom_fft(irr_es, [l, r], n, fs=n))

    cam_irr = cam_interface.I()
    sim_irr = sim_interface.I(spectrometer, t)

    cam_opd = fft(cam_irr)
    sim_opd = fft(sim_irr)

    dpg.set_value("WavenumberAcq", [k.tolist(), cam_irr.tolist()])
    dpg.set_value("WavenumberSim", [k.tolist(), sim_irr.tolist()])

    dpg.set_value(
        "OPDAcq", [(opd*1e6)[l:r//2].tolist(), cam_opd[l:r//2].tolist()])
    dpg.set_value(
        "OPDSim", [(opd*1e6)[l:r//2].tolist(), sim_opd[l:r//2].tolist()])


def plot_acquisition(spectrometer, cam_interface, sim_interface, acq_interface):
    k = spectrometer.k()
    k_es = spectrometer.k_es()
    zl = acq_interface.min_opd()
    zr = acq_interface.max_opd()
    n = spectrometer.OPDlen()
    dopd = spectrometer.dOPD()
    l = int((zl - spectrometer.OPD()[0]) / dopd)
    r = int((zr - spectrometer.OPD()[0]) / dopd)
    opd = np.linspace(zl, zr, n)

    def get_opd(irr):
        irr_es = interp1d(k, irr)(k_es)
        fft = np.abs(zoom_fft(irr_es, [l, r], n, fs=n))
        return opd[np.argmax(fft)]

    cam_irr = cam_interface.data
    sim_irr = sim_interface.data

    cam_opd = np.apply_along_axis(get_opd, axis=1, arr=cam_irr)
    cam_t = np.linspace(0, acq_interface.T(), len(cam_opd))
    sim_opd = np.apply_along_axis(get_opd, axis=1, arr=sim_irr)
    sim_t = np.linspace(0, acq_interface.T(), len(sim_opd))

    dpg.set_value("OPD_time_Acq", [cam_t.tolist(), cam_opd.tolist()])
    dpg.set_axis_limits("OPD_time_Acq_", ymin=zl, ymax=zr)
    dpg.set_value("OPD_time_Sim", [sim_t.tolist(), sim_opd.tolist()])
    dpg.set_axis_limits("OPD_time_Sim_", ymin=zl, ymax=zr)

    cam_fft = np.abs(np.fft.fft(cam_opd))
    cam_freq = np.fft.fftfreq(len(cam_opd), acq_interface.T()/len(cam_opd))
    sim_fft = np.abs(np.fft.fft(sim_opd))
    cam_freq = np.fft.fftfreq(len(sim_opd), acq_interface.T()/len(sim_opd))

    dpg.set_value("Frequency_Acq", [
                  cam_freq[0:len(cam_opd)//2].tolist(), cam_fft[0:len(cam_opd)//2].tolist()])
    dpg.set_value("Frequency_Sim", [
                  cam_freq[0:len(sim_opd)//2].tolist(), sim_fft[0:len(sim_opd)//2].tolist()])


def PlotWindow(tag, label="", xlabel="", ylabel="", x=[], y=[]):
    with dpg.plot(label=label, height=215, width=-1) as PlotWindow:
        dpg.add_plot_axis(dpg.mvXAxis, label=xlabel, tag=f"{tag}_{xlabel}")
        dpg.add_plot_axis(dpg.mvYAxis, label=ylabel, tag=f"{tag}_{ylabel}")
        dpg.add_line_series(x, y, parent=dpg.last_item(), tag=tag)

    return PlotWindow

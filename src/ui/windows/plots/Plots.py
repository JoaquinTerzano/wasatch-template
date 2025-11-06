import dearpygui.dearpygui as dpg


def PlotWindow(tag, label="", xlabel="", ylabel="", x=[], y=[]):
    with dpg.plot(label=label, height=215, width=-1) as PlotWindow:
        dpg.add_plot_axis(dpg.mvXAxis, label=xlabel)
        dpg.add_plot_axis(dpg.mvYAxis, label=ylabel)
        dpg.add_line_series(x, y, parent=dpg.last_item(), tag=tag)

    return PlotWindow

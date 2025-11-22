import dearpygui.dearpygui as dpg


def log(msg):
    if msg:
        dpg.add_text(msg, parent="LogsWindow")
        dpg.set_y_scroll("LogsWindow", dpg.get_y_scroll_max("LogsWindow"))


def LogsWindow():
    return dpg.add_child_window(tag="LogsWindow")

import dearpygui.dearpygui as dpg
from .ParametersForm import ParametersForm
from ..simulation import Reference


def SimulationWindow(interface):

    with dpg.tab_bar() as SimulationWindow:

        """ ******************** Pestaña Fuente ******************** """

        with dpg.tab(label="Source"):
            _ = ParametersForm(interface.source)

        """ ******************** Pestaña Referencias ******************** """

        with dpg.tab(label="References"):
            _ = ParametersForm(
                interface.reference)

            def add_reference_callback(sender, app_data, user_data):
                interface.references.append(
                    Reference(interface.reference.parameters))
                with dpg.table_row(parent="ReferencesTable"):
                    for key, parameter in interface.reference.parameters.items():
                        dpg.add_text(str(parameter["value"]))

            dpg.add_button(label="Add", callback=add_reference_callback)

            dpg.add_table(tag="ReferencesTable", resizable=True)

            for key, parameter in interface.reference.parameters.items():
                dpg.add_table_column(
                    label=parameter["args"]["label"], parent="ReferencesTable")

    return SimulationWindow

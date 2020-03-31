import numpy as np

from bokeh.models import (Div, Tabs, Panel, Slider, Column, TextInput, PreText,
                          ColumnDataSource)
from bokeh.plotting import curdoc, figure
from bokeh.layouts import layout, row

from cliente_control import Cliente
import threading


''' ******************** Modo Automático ******************** '''
label1 = Div(text='<h1>Modo Automático</h1>')
refEst1 = Slider(title="Altura de Referencia Estanque 1", value=0.0, start=0.0,
             end=50.0, step=0.1)
refEst2 = Slider(title="Altura de Referencia Estanque 2", value=0.0, start=0.0,
             end=50.0, step=0.1)

Kp = TextInput(title="Constante Proporcional", value='0')
Ki = TextInput(title="Constante Integral", value='0')
Kd = TextInput(title="Constante Derivativa", value='0')


''' ******************** Modo Manual ******************** '''
label2 = Div(text='<h1>Modo Manual</h1>')
voltageV1 = Slider(title="Voltaje Válvula 1", value=0.0, start=-5.0, end=5.0,
                   step=0.01)
voltageV2 = Slider(title="Voltaje Válvula 2", value=0.0, start=-5.0, end=5.0,
                   step=0.01)
razonFlujoV1 = Slider(title="Razón de Flujo Válvula 1", value=0.0, start=0.0,
                      end=1.0, step=0.01)
razonFlujoV2 = Slider(title="Razón de Flujo Válvula 2", value=0.0, start=0.0,
                      end=1.0, step=0.01)


''' ******************** Added stuff ******************** '''

# DataSources
DataSource_tanque1 = ColumnDataSource(dict(time=[], ref=[], real=[]))
DataSource_tanque2 = ColumnDataSource(dict(time=[], ref=[], real=[]))
DataSource_tanque3 = ColumnDataSource(dict(time=[], real=[]))
DataSource_tanque4 = ColumnDataSource(dict(time=[], real=[]))

# Figuras
# Tanque 1
fig_tanque1 = figure(title='Tanque 1', plot_width=600, plot_height=300, y_axis_location="left", y_range=(0, 70))
fig_tanque1.line(x='time', y='ref', alpha=0.8, line_width=3, color='black', source=DataSource_tanque1, legend_label='Ref')
fig_tanque1.line(x='time', y='real', alpha=0.8, line_width=3, color='red', source=DataSource_tanque1, legend_label='Real')
fig_tanque1.xaxis.axis_label = 'Tiempo (S)'
fig_tanque1.yaxis.axis_label = 'Valores'
fig_tanque1.legend.location = "top_left"

# Tanque 2
fig_tanque2 = figure(title='Tanque 2', plot_width=600, plot_height=300, y_axis_location="left", y_range=(0, 70))
fig_tanque2.line(x='time', y='ref', alpha=0.8, line_width=3, color='black', source=DataSource_tanque2, legend_label='Ref')
fig_tanque2.line(x='time', y='real', alpha=0.8, line_width=3, color='red', source=DataSource_tanque2, legend_label='Real')
fig_tanque2.xaxis.axis_label = 'Tiempo (S)'
fig_tanque2.yaxis.axis_label = 'Valores'
fig_tanque2.legend.location = "top_left"

# Tanque 3
fig_tanque3 = figure(title='Tanque 3', plot_width=600, plot_height=300, y_axis_location="left", y_range=(0, 70))
fig_tanque3.line(x='time', y='real', alpha=0.8, line_width=3, color='red', source=DataSource_tanque3, legend_label='Real')
fig_tanque3.xaxis.axis_label = 'Tiempo (S)'
fig_tanque3.yaxis.axis_label = 'Valores'
fig_tanque3.legend.location = "top_left"

# Tanque 4
fig_tanque4 = figure(title='Tanque 4', plot_width=600, plot_height=300, y_axis_location="left", y_range=(0, 70))
fig_tanque4.line(x='time', y='real', alpha=0.8, line_width=3, color='red', source=DataSource_tanque4, legend_label='Real')
fig_tanque4.xaxis.axis_label = 'Tiempo (S)'
fig_tanque4.yaxis.axis_label = 'Valores'
fig_tanque4.legend.location = "top_left"


t = 0


# Funcion principal que se llama cada cierto tiempo para mostrar la informacion
def MainLoop():  # Funcion principal que se llama cada cierto tiempo para mostrar la informacion
    global t

    h1 = cliente.alturas['H1'].get_value()
    update = dict(time=[t], ref=[32], real=[h1])
    DataSource_tanque1.stream(new_data=update, rollover=50)  # Se ven los ultimos 50 datos

    h2 = cliente.alturas['H2'].get_value()
    update = dict(time=[t], ref=[32], real=[h2])
    DataSource_tanque2.stream(new_data=update, rollover=50)  # Se ven los ultimos 50 datos

    h3 = cliente.alturas['H3'].get_value()
    update = dict(time=[t], real=[h3])
    DataSource_tanque3.stream(new_data=update, rollover=50)  # Se ven los ultimos 50 datos

    h4 = cliente.alturas['H4'].get_value()
    update = dict(time=[t], real=[h4])
    DataSource_tanque4.stream(new_data=update, rollover=50)  # Se ven los ultimos 50 datos

    t += 1


layout = layout([
   [fig_tanque3, fig_tanque4],
   [fig_tanque1, fig_tanque2]
 ])


panel1 = Panel(child=row(Column(label1, refEst1, refEst2, Kp, Ki, Kd), layout,
               sizing_mode='fixed'), title='Modo Automático')
panel2 = Panel(child=row(Column(label2, voltageV1, voltageV2, razonFlujoV1,
               razonFlujoV2), layout, sizing_mode='fixed'), title='Modo Manual')

# Tabs
tabs = Tabs(tabs=[panel1, panel2])


''' ******************** Events functions ******************** '''

textInputs = [Kp, Ki, Kd]

sliderInputs = [refEst1, refEst2, voltageV1, voltageV2, razonFlujoV1,
                razonFlujoV2]


def textChanges(attr, old, new):
    '''
    Get excecuted when a text input changes
    '''
    print('attr', attr)
    print('old', old)
    print('new', new)


def sliderChanges(attr, old, new):
    '''
    Get excecuted when the slide value is changed
    '''
    print('attr', attr)
    print('old', old)
    print('new', new)


def panelActive(attr, old, new):
    '''
    Get excecuted when the other tab is selected
    Changes the operation mode if a tab is changed
    '''
    if tabs.active == 0:
        print('Modo automático activado')

    elif tabs.active == 1:
        print('Modo manual activado')


for text in textInputs:
    text.on_change('value', textChanges)

for slider in sliderInputs:
    slider.on_change('value', sliderChanges)

tabs.on_change('active', panelActive)


''' ******************** Client ******************** '''

def funcion_handler(node, val):
    key = node.get_parent().get_display_name().Text
    if key == 'Tanque1':
        lolito = val


class SubHandler(object):
    """
    Subscription Handler. To receive events from server for a subscription
    data_change and event methods are called directly from receiving thread.
    Do not do expensive, slow or network operation there. Create another
    thread if you need to do such a thing
    """

    def datachange_notification(self, node, val, data):
        thread_handler = threading.Thread(target=funcion_handler,
                                          args=(node, val))  # Se realiza la descarga por un thread
        thread_handler.start()

    def event_notification(self, event):
        print("Python: New event", event)


cliente = Cliente("opc.tcp://127.0.0.1:4840/freeopcua/server/", suscribir_eventos=True, SubHandler=SubHandler)
cliente.conectar()

# cliente.subscribir_mv() # Se subscribe a las variables manipuladas
# cliente.subscribir_cv() # Se subscribe a las variables controladas


curdoc().add_root(tabs)
curdoc().title = 'Experiencia 1: Control de Procesos'
curdoc().add_periodic_callback(MainLoop, 150)

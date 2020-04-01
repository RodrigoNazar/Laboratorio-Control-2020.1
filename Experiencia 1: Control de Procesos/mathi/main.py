import numpy as np

from bokeh.models import (Div, Tabs, Panel, Slider, Column, TextInput, PreText,
                          ColumnDataSource)
from bokeh.plotting import curdoc, figure
from bokeh.layouts import layout, row

from cliente_control import Cliente
import threading

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

'''************************ Valores iniciales ***************'''
ref1 = 40
ref2 = 40
vol1 = cliente.valvulas['valvula1'].get_value()
vol2 = cliente.valvulas['valvula2'].get_value()
gamma1 = cliente.razones['razon1'].get_value()
gamma2 = cliente.razones['razon2'].get_value()

''' ******************** Modo Automático ******************** '''
label1 = Div(text='<h1>Modo Automático</h1>')
refEst1 = Slider(title="Altura de Referencia Estanque 1", value=ref1, start=0.0,
                 end=50.0, step=0.1)
refEst2 = Slider(title="Altura de Referencia Estanque 2", value=ref2, start=0.0,
                 end=50.0, step=0.1)

Kp = TextInput(title="Constante Proporcional", value='0')
Ki = TextInput(title="Constante Integral", value='0')
Kd = TextInput(title="Constante Derivativa", value='0')

''' ******************** Modo Manual ******************** '''
label2 = Div(text='<h1>Modo Manual</h1>')
voltageV1 = Slider(title="Voltaje Válvula 1", value=vol1, start=-0.99, end=0.99,
                   step=0.01)
voltageV2 = Slider(title="Voltaje Válvula 2", value=vol2, start=-0.99, end=0.99,
                   step=0.01)
razonFlujoV1 = Slider(title="Razón de Flujo Válvula 1", value=gamma1, start=0.01,
                      end=0.99, step=0.01)
razonFlujoV2 = Slider(title="Razón de Flujo Válvula 2", value=gamma2, start=0.0,
                      end=0.99, step=0.01)

''' ******************** Figures ******************** '''

# DataSources
DataSource_tanques = ColumnDataSource(
    dict(time=[], ref1=[], real1=[], ref2=[], real2=[], real3=[], real4=[], vol1=[], vol2=[]))

# Figuras
# Tanque 1
fig_tanque1 = figure(title='Tanque 1', plot_width=600, plot_height=300, y_axis_location="left", y_range=(0, 52))
l1t1 = fig_tanque1.line(x='time', y='ref1', alpha=0.8, line_width=3, color='black', source=DataSource_tanques,
                        legend_label='Ref')
l2t1 = fig_tanque1.line(x='time', y='real1', alpha=0.8, line_width=3, color='red', source=DataSource_tanques,
                        legend_label='Real')
fig_tanque1.xaxis.axis_label = 'Tiempo (S)'
fig_tanque1.yaxis.axis_label = 'Valores'
fig_tanque1.legend.location = "top_left"

# Tanque 2
fig_tanque2 = figure(title='Tanque 2', plot_width=600, plot_height=300, y_axis_location="left", y_range=(0, 52))
l1t2 = fig_tanque2.line(x='time', y='ref2', alpha=0.8, line_width=3, color='black', source=DataSource_tanques,
                        legend_label='Ref')
l2t2 = fig_tanque2.line(x='time', y='real2', alpha=0.8, line_width=3, color='red', source=DataSource_tanques,
                        legend_label='Real')
fig_tanque2.xaxis.axis_label = 'Tiempo (S)'
fig_tanque2.yaxis.axis_label = 'Valores'
fig_tanque2.legend.location = "top_left"

# Tanque 3
fig_tanque3 = figure(title='Tanque 3', plot_width=600, plot_height=300, y_axis_location="left", y_range=(0, 52))
l1t3 = fig_tanque3.line(x='time', y='real3', alpha=0.8, line_width=3, color='red', source=DataSource_tanques,
                        legend_label='Real')
fig_tanque3.xaxis.axis_label = 'Tiempo (S)'
fig_tanque3.yaxis.axis_label = 'Valores'
fig_tanque3.legend.location = "top_left"

# Tanque 4
fig_tanque4 = figure(title='Tanque 4', plot_width=600, plot_height=300, y_axis_location="left", y_range=(0, 52))
l1t4 = fig_tanque4.line(x='time', y='real4', alpha=0.8, line_width=3, color='red', source=DataSource_tanques,
                        legend_label='Real')
fig_tanque4.xaxis.axis_label = 'Tiempo (S)'
fig_tanque4.yaxis.axis_label = 'Valores'
fig_tanque4.legend.location = "top_left"

# Voltaje1
fig_vol1 = figure(title='Voltaje 1', plot_width=600, plot_height=300, y_axis_location="left", y_range=(-1, 1))
fig_vol1.line(x='time', y='vol1', alpha=0.8, line_width=3, color='red', source=DataSource_tanques,
              legend_label='Vol1')
fig_vol1.xaxis.axis_label = 'Tiempo (S)'
fig_vol1.yaxis.axis_label = '[V]'
fig_vol1.legend.location = "top_left"

# Voltaje2
fig_vol2 = figure(title='Voltaje 2', plot_width=600, plot_height=300, y_axis_location="left", y_range=(-1, 1))
fig_vol2.line(x='time', y='vol2', alpha=0.8, line_width=3, color='red', source=DataSource_tanques,
              legend_label='Vol2')
fig_vol2.xaxis.axis_label = 'Tiempo (S)'
fig_vol2.yaxis.axis_label = '[V]'
fig_vol2.legend.location = "top_left"

t = 0


# Funcion principal que se llama cada cierto tiempo para mostrar la informacion
def MainLoop():  # Funcion principal que se llama cada cierto tiempo para mostrar la informacion
    global t

    h1 = cliente.alturas['H1'].get_value()
    h2 = cliente.alturas['H2'].get_value()
    h3 = cliente.alturas['H3'].get_value()
    h4 = cliente.alturas['H4'].get_value()

    v1 = cliente.valvulas['valvula1'].get_value()
    v2 = cliente.valvulas['valvula2'].get_value()

    update = dict(time=[t], ref1=[32], real1=[h1], ref2=[32], real2=[h2],
                  real3=[h3], real4=[h4], vol1=[v1], vol2=[v2])

    DataSource_tanques.stream(new_data=update, rollover=200)

    t += 1


layout = layout([
    [fig_tanque3, fig_tanque4],
    [fig_tanque1, fig_tanque2],
    [fig_vol1, fig_vol2]
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
    kp = Kp.value
    ki = Ki.value
    kd = Kd.value

    print(f'\nConstantes del pid:')
    print('kp:', kp)
    print('ki:', ki)
    print('kd:', kd)


def slider_changes_ref1(attr, old, new):
    global ref1
    ref1 = new
refEst1.on_change('value', slider_changes_ref1)


def slider_changes_ref2(attr, old, new):
    global ref2
    ref2 = new
refEst2.on_change('value', slider_changes_ref2)


def slider_changes_voltaje1(attr, old, new):
    cliente.valvulas['valvula1'].set_value(new)
    print('vol1 cambio')

voltageV1.on_change('value',slider_changes_voltaje1)


def slider_changes_voltaje2(attr, old, new):
    cliente.valvulas['valvula2'].set_value(new)
    print('vol2 cambio')

voltageV2.on_change('value', slider_changes_voltaje2)


def slider_changes_razon1(attr, old, new):
    cliente.razones['razon1'].set_value(new)
    print('razon1 cambio')

razonFlujoV1.on_change('value', slider_changes_razon1)


def slider_changes_razon2(attr, old, new):
    cliente.razones['razon2'].set_value(new)
    print('razon2 cambio')
razonFlujoV2.on_change('value', slider_changes_razon2)


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

tabs.on_change('active', panelActive)

curdoc().add_root(tabs)
curdoc().title = 'Experiencia 1: Control de Procesos'
curdoc().add_periodic_callback(MainLoop, 150)

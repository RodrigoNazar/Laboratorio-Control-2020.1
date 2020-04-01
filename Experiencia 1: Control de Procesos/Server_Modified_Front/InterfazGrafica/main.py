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

''' ******************** Alarmas ******************** '''

alarm = Div(text='<div class="container"><h2>¡ALARMA!</h2><img src="InterfazGrafica/static/alarm.png"></div>')
alarm.visible = False

''' ******************** Figures ******************** '''

# DataSources
DataSource_tanques = ColumnDataSource(dict(time=[], ref1=[], real1=[], ref2=[], real2=[], real3=[], real4=[], vol1=[], vol2=[]))

# Figuras
# Tanque 1
fig_tanque1 = figure(title='Tanque 1', plot_width=600, plot_height=300, y_axis_location="left", y_range=(0, 70))
l1t1 = fig_tanque1.line(x='time', y='ref1', alpha=0.8, line_width=3, color='black', source=DataSource_tanques,
                        legend_label='Ref')
l2t1 = fig_tanque1.line(x='time', y='real1', alpha=0.8, line_width=3, color='red', source=DataSource_tanques,
                        legend_label='Real')
fig_tanque1.xaxis.axis_label = 'Tiempo (S)'
fig_tanque1.yaxis.axis_label = 'Valores'
fig_tanque1.legend.location = "top_left"

# Tanque 2
fig_tanque2 = figure(title='Tanque 2', plot_width=600, plot_height=300, y_axis_location="left", y_range=(0, 70))
l1t2 = fig_tanque2.line(x='time', y='ref2', alpha=0.8, line_width=3, color='black', source=DataSource_tanques,
                        legend_label='Ref')
l2t2 = fig_tanque2.line(x='time', y='real2', alpha=0.8, line_width=3, color='red', source=DataSource_tanques,
                        legend_label='Real')
fig_tanque2.xaxis.axis_label = 'Tiempo (S)'
fig_tanque2.yaxis.axis_label = 'Valores'
fig_tanque2.legend.location = "top_left"

# Tanque 3
fig_tanque3 = figure(title='Tanque 3', plot_width=600, plot_height=300, y_axis_location="left", y_range=(0, 70))
l1t3 = fig_tanque3.line(x='time', y='real3', alpha=0.8, line_width=3, color='red', source=DataSource_tanques,
                        legend_label='Real')
fig_tanque3.xaxis.axis_label = 'Tiempo (S)'
fig_tanque3.yaxis.axis_label = 'Valores'
fig_tanque3.legend.location = "top_left"

# Tanque 4
fig_tanque4 = figure(title='Tanque 4', plot_width=600, plot_height=300, y_axis_location="left", y_range=(0, 70))
l1t4 = fig_tanque4.line(x='time', y='real4', alpha=0.8, line_width=3, color='red', source=DataSource_tanques,
                        legend_label='Real')
fig_tanque4.xaxis.axis_label = 'Tiempo (S)'
fig_tanque4.yaxis.axis_label = 'Valores'
fig_tanque4.legend.location = "top_left"

# Voltaje1
fig_vol1 = figure(title='Voltaje 1', plot_width=600, plot_height=300, y_axis_location="left", y_range=(-5, 5))
fig_vol1.line(x='time', y='vol1', alpha=0.8, line_width=3, color='red', source=DataSource_tanques,
                        legend_label='Vol1')
fig_vol1.xaxis.axis_label = 'Tiempo (S)'
fig_vol1.yaxis.axis_label = '[V]'
fig_vol1.legend.location = "top_left"

# Voltaje2
fig_vol2 = figure(title='Voltaje 2', plot_width=600, plot_height=300, y_axis_location="left", y_range=(-5, 5))
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


panel1 = Panel(child=row(Column(label1, refEst1, refEst2, Kp, Ki, Kd, alarm), layout), title='Modo Automático')
panel2 = Panel(child=row(Column(label2, voltageV1, voltageV2, razonFlujoV1,
               razonFlujoV2), layout), title='Modo Manual')

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


def sliderChanges(attr, old, new):
    '''
    Get excecuted when the slide value is changed
    '''
    ref_est1 = refEst1.value
    ref_est2 = refEst2.value
    volV1 = voltageV1.value
    volV2 = voltageV2.value
    rFlujoV1 = razonFlujoV1.value
    rFlujoV2 = razonFlujoV2.value

    alarm.visible = not alarm.visible

    print(f'\nSliders:')
    print('ref_est1:', ref_est1)
    print('ref_est2:', ref_est2)
    print('volV1:', volV1)
    print('volV2:', volV2)
    print('rFlujoV1:', rFlujoV1)
    print('rFlujoV2:', rFlujoV2)



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

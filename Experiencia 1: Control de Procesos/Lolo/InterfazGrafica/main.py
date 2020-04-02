import numpy as np

from bokeh.models import (Div, Tabs, Panel, Slider, Column, TextInput, PreText,
                          ColumnDataSource, Button, Select)
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

# cliente.subscribir_mv() # Se subscribe a las variables manipuladas
# cliente.subscribir_cv() # Se subscribe a las variables controladas


'''************************ Valores iniciales y variables globales ***************'''

ref1 = 40
ref2 = 40
vol1 = cliente.valvulas['valvula1'].get_value()
vol2 = cliente.valvulas['valvula2'].get_value()
gamma1 = cliente.razones['razon1'].get_value()
gamma2 = cliente.razones['razon2'].get_value()

t = 0
automatico = True


''' ******************** Alarmas y botones ******************** '''

alarm = Div(text='<div class="container"><h2>¡ALARMA!</h2><img src="InterfazGrafica/static/alarm.png"></div>')
alarm.visible = False

dataRecordingButton = Button(label="Comenzar a adquirir datos", button_type="success")
dataRecordingLabel = Div(text='<p>Adquiriendo datos...</p>')
dataRecordingLabel.visible = False

# saveDataButton = Button(label="Guardar datos", button_type="success")
extensionsSelect = Select(title="Guardar los datos con extensión:", options=['csv', 'txt', 'npy'])


''' ******************** Modo Automático ******************** '''

label1 = Div(text='<h1>Modo Automático &#9889;</h1><hr>')
refEst1 = Slider(title="Altura de Referencia Estanque 1", value=40, start=0.0,
             end=50.0, step=0.1)
refEst2 = Slider(title="Altura de Referencia Estanque 2", value=40, start=0.0,
             end=50.0, step=0.1)

valvula1Label = Div(text='<h3>Válvula 1</h3><hr>')
Kp1 = TextInput(title="Constante Proporcional", value='0')
Ki1 = TextInput(title="Constante Integral", value='0')
Kd1 = TextInput(title="Constante Derivativa", value='0')

valvula2Label = Div(text='<h3>Válvula 2</h3><hr>')
Kp2 = TextInput(title="Constante Proporcional", value='0')
Ki2 = TextInput(title="Constante Integral", value='0')
Kd2 = TextInput(title="Constante Derivativa", value='0')


''' ******************** Modo Manual ******************** '''

label2 = Div(text='<h1>Modo Manual &#9997;</h1><hr>')
voltageV1 = Slider(title="Voltaje Válvula 1", value=vol1, start=-5.0, end=5.0,
                   step=0.01)
voltageV2 = Slider(title="Voltaje Válvula 2", value=vol2, start=-5.0, end=5.0,
                   step=0.01)
razonFlujoV1 = Slider(title="Razón de Flujo Válvula 1", value=0.0, start=0.0,
                      end=0.99, step=0.01)
razonFlujoV2 = Slider(title="Razón de Flujo Válvula 2", value=0.0, start=0.0,
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


''' ******************** Main Loop ******************** '''

# Funcion principal que se llama cada cierto tiempo para mostrar la informacion
def MainLoop():  # Funcion principal que se llama cada cierto tiempo para mostrar la informacion
    global t, ref1, ref2, automatico

    h1 = cliente.alturas['H1'].get_value()
    h2 = cliente.alturas['H2'].get_value()
    h3 = cliente.alturas['H3'].get_value()
    h4 = cliente.alturas['H4'].get_value()

    v1 = cliente.valvulas['valvula1'].get_value()
    v2 = cliente.valvulas['valvula2'].get_value()

    if automatico:
        ref11 = ref1
        ref22 = ref2
    else:
        ref11 = -1
        ref22 = -1

    update = dict(time=[t], ref1=[ref11], real1=[h1], ref2=[ref22], real2=[h2],
                  real3=[h3], real4=[h4], vol1=[v1], vol2=[v2])

    DataSource_tanques.stream(new_data=update, rollover=200)

    t += 1


layout = layout([
    [fig_tanque3, fig_tanque4],
    [fig_tanque1, fig_tanque2],
    [fig_vol1, fig_vol2]
])


panel1 = Panel(child=row(Column(label1, row(Column(dataRecordingButton, dataRecordingLabel), Column(extensionsSelect)), refEst1, refEst2, row(Column(valvula1Label, Kp1,
                Ki1, Kd1), Column(valvula2Label, Kp2, Ki2, Kd2)), alarm),
                layout), title='Modo Automático')
panel2 = Panel(child=row(Column(label2, dataRecordingButton, dataRecordingLabel, row(Column(valvula1Label, voltageV1, razonFlujoV1),
               Column(valvula2Label, voltageV2, razonFlujoV2)), alarm), layout), title='Modo Manual')

# Tabs
tabs = Tabs(tabs=[panel1, panel2])


''' ******************** Events functions ******************** '''

textInputs = [Kp1, Ki1, Kd1, Kp2, Ki2, Kd2]

sliderInputs = [refEst1, refEst2, voltageV1, voltageV2, razonFlujoV1,
                razonFlujoV2]

# Texto
def textChanges(attr, old, new):
    '''
    Get excecuted when a text input changes
    '''
    kp1 = Kp1.value
    ki1 = Ki1.value
    kd1 = Kd1.value

    print(f'\nConstantes del pid:')
    print('kp:', kp1)
    print('ki:', ki1)
    print('kd:', kd1)


# Sliders
def slider_changes_ref1(attr, old, new):
    global ref1
    ref1 = new

refEst1.on_change('value', slider_changes_ref1)


def slider_changes_ref2(attr, old, new):
    global ref2
    ref2 = new
    alarm.visible = not alarm.visible

refEst2.on_change('value', slider_changes_ref2)


def slider_changes_voltaje1(attr, old, new):
    cliente.valvulas['valvula1'].set_value(new)
    alarm.visible = not alarm.visible

voltageV1.on_change('value', slider_changes_voltaje1)


def slider_changes_voltaje2(attr, old, new):
    cliente.valvulas['valvula2'].set_value(new)

voltageV2.on_change('value', slider_changes_voltaje2)


def slider_changes_razon1(attr, old, new):
    cliente.razones['razon1'].set_value(new)

razonFlujoV1.on_change('value', slider_changes_razon1)


def slider_changes_razon2(attr, old, new):
    cliente.razones['razon2'].set_value(new)

razonFlujoV2.on_change('value', slider_changes_razon2)


# Button
def recordingButtonClicked():
    # We were recording the data
    if dataRecordingLabel.visible:
        dataRecordingButton.button_type = 'success'
        dataRecordingButton.label = 'Comenzar a adquirir datos'

    else:
        dataRecordingButton.button_type = 'danger'
        dataRecordingButton.label = 'Dejar de adquirir datos'

    dataRecordingLabel.visible = not dataRecordingLabel.visible

dataRecordingButton.on_click(recordingButtonClicked)


# Dropdown
def extensionsSelectClicked(attrname, old, new):
    print(old, new)

extensionsSelect.on_change('value', extensionsSelect)


# Tabs
def panelActive(attr, old, new):
    '''
    Get excecuted when the other tab is selected
    Changes the operation mode if a tab is changed
    '''
    if tabs.active == 0:
        print('Modo automático activado')

    elif tabs.active == 1:
        print('Modo manual activado')

tabs.on_change('active', panelActive)


for text in textInputs:
    text.on_change('value', textChanges)


''' ******************** Curdoc ******************** '''

curdoc().add_root(tabs)
curdoc().title = 'Experiencia 1: Control de Procesos'
curdoc().add_periodic_callback(MainLoop, 150)

import numpy as np
import pandas as pd

from bokeh.models import (Div, Tabs, Panel, Slider, Column, TextInput, PreText,
                          ColumnDataSource, Button, Select, Dropdown)
from bokeh.events import MenuItemClick
from bokeh.plotting import curdoc, figure
from bokeh.layouts import layout, row

from cliente_control import Cliente
import threading
import json
from PID import PID

''' ******************** Client ******************** '''


def funcion_handler(node, val):
    key = node.get_parent().get_display_name().Text


def changeWarningList():
    global alarm_list, warning_devices

    text = alarm_list.text

    start = text.find("<ul>")
    end = text.find("</ul>") + len('</ul>')

    head = text[:start]
    tail = text[end:]

    middle = ''

    for device in warning_devices:
        dispositivo = device['dispositivo']
        dispositivo = f'<li>{dispositivo}<p>¡Revisar niveles!</p></li>'

        middle += dispositivo

    print('Cambiando la lista a:')
    print(head + '<ul>' + middle + '</ul>' + tail)

    alarm_list.text = head + '<ul>' + middle + '</ul>' + tail


def eventParser(event):
    '''
    Los objetos event vienen en una forma que se hace muy dificil de obtener los
    datos que trae.
    Esta función busca facilitar el método de adquisición de los datos.
    '''
    return {k: v for k, v in event.__dict__.items() if k not in event.internal_properties}


def eventMessageParser(message):
    '''
    Los mensajes de los eventos son un string de la forma:

    Alarma en: Tanque3-h valor: 8.034358101949158

    Este método busca mejorar la adquisición de los datos del mensaje
    '''
    message = message.split()

    return message[2][:-2], message[-1]


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
        global alarm, t, warning_devices

        print('\nAlarma', )

        alarm.visible = True
        alarm_list.visible = True
        event_dict = eventParser(event)

        nivel = event_dict['Nivel']
        dispositivo, valor = eventMessageParser(event_dict['Mensaje'])
        severidad = event_dict['Severity']

        existe = False
        indice = 0
        print('\nAlarma', warning_devices)

        # Buscamos si existe el dispositivo en la lista
        for indx, elem in enumerate(warning_devices):
            if dispositivo == elem['dispositivo']:
                existe = True
                indice = indx

        if existe:
            # Elevamos el cooldown
            elem = warning_devices[indx]
            elem['cooldown'] = 50

            # Sólo si hay info que actualizar, se actualiza la lista en el front
            if nivel != elem['nivel']:
                warning_devices[indx]['nivel'] = nivel
                changeWarningList()

        # Si el dispositivo no existe
        if not existe:
            # Insertamos el elemento en la lista de warning
            elem = {
                'dispositivo': dispositivo,
                'nivel': nivel,
                'severidad': severidad,
                'cooldown': 50
            }

            warning_devices.append(elem)

            # Actualizamos la lista en el front
            changeWarningList()


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
datos_a_guardar = None
extension = None
n_archivos = 0
cont = 0
warning_devices = []
primer_ciclo = True

'''************************************ Controladores PID ***************************'''
pid1 = PID()
pid2 = PID()

''' ******************** Alarmas y botones ******************** '''

alarm = Div(text='<div class="container"><h2>¡ALARMA!</h2><img src="InterfazGrafica/static/alarm.png"></div>')
alarm.visible = False
alarm_list = Div(text='<div class="container"><h3>Dispositivos que presentan problemas:</h3><ul></ul></div>')
alarm_list.visible = False

dataRecordingButton = Button(label="Comenzar a adquirir datos", button_type="success")
dataRecordingLabel = Div(text='<p>Adquiriendo datos...</p>')
dataRecordingLabel.visible = False

extensionsMenu = [("csv", "csv"), ("txt", "txt"), ("npy", "npy")]
extensionsDropdown = Dropdown(label="Guardar los datos con extensión:", button_type="success", menu=extensionsMenu)

''' ******************** Modo Automático ******************** '''

label1 = Div(text='<h1>Modo Automático &#9889;</h1><hr>')
refEst1 = Slider(title="Altura de Referencia Estanque 1", value=40, start=0.0,
                 end=50.0, step=0.1)
refEst2 = Slider(title="Altura de Referencia Estanque 2", value=40, start=0.0,
                 end=50.0, step=0.1)

valvula1Label = Div(text='<h3>Válvula 1</h3><hr>')
Kp1 = TextInput(title="Constante Proporcional", value='{}'.format(pid1.Kp))
Ki1 = TextInput(title="Constante Integral", value='{}'.format(pid1.Ki))
Kd1 = TextInput(title="Constante Derivativa", value='{}'.format(pid1.Kd))
Kw1 = TextInput(title="Constante Anti W-UP", value='{}'.format(pid1.Kw))

valvula2Label = Div(text='<h3>Válvula 2</h3><hr>')
Kp2 = TextInput(title="Constante Proporcional", value='{}'.format(pid2.Kp))
Ki2 = TextInput(title="Constante Integral", value='{}'.format(pid2.Ki))
Kd2 = TextInput(title="Constante Derivativa", value='{}'.format(pid2.Kd))
Kw2 = TextInput(title="Constante Anti W-UP", value='{}'.format(pid2.Kw))

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
fig_tanque1.xaxis.axis_label = 'Tiempo [S]'
fig_tanque1.yaxis.axis_label = 'Altura [m]'
fig_tanque1.legend.location = "top_left"

# Tanque 2
fig_tanque2 = figure(title='Tanque 2', plot_width=600, plot_height=300, y_axis_location="left", y_range=(0, 52))
l1t2 = fig_tanque2.line(x='time', y='ref2', alpha=0.8, line_width=3, color='black', source=DataSource_tanques,
                        legend_label='Ref')
l2t2 = fig_tanque2.line(x='time', y='real2', alpha=0.8, line_width=3, color='red', source=DataSource_tanques,
                        legend_label='Real')
fig_tanque2.xaxis.axis_label = 'Tiempo [S]'
fig_tanque2.yaxis.axis_label = 'Altura [m]'
fig_tanque2.legend.location = "top_left"

# Tanque 3
fig_tanque3 = figure(title='Tanque 3', plot_width=600, plot_height=300, y_axis_location="left", y_range=(0, 52))
l1t3 = fig_tanque3.line(x='time', y='real3', alpha=0.8, line_width=3, color='red', source=DataSource_tanques,
                        legend_label='Real')
fig_tanque3.xaxis.axis_label = 'Tiempo [S]'
fig_tanque3.yaxis.axis_label = 'Altura [m]'
fig_tanque3.legend.location = "top_left"

# Tanque 4
fig_tanque4 = figure(title='Tanque 4', plot_width=600, plot_height=300, y_axis_location="left", y_range=(0, 52))
l1t4 = fig_tanque4.line(x='time', y='real4', alpha=0.8, line_width=3, color='red', source=DataSource_tanques,
                        legend_label='Real')
fig_tanque4.xaxis.axis_label = 'Tiempo [S]'
fig_tanque4.yaxis.axis_label = 'Altura [m]'
fig_tanque4.legend.location = "top_left"

# Voltaje1
fig_vol1 = figure(title='Voltaje 1', plot_width=600, plot_height=300, y_axis_location="left", y_range=(-1, 1))
fig_vol1.line(x='time', y='vol1', alpha=0.8, line_width=3, color='red', source=DataSource_tanques,
              legend_label='Vol1')
fig_vol1.xaxis.axis_label = 'Tiempo [S]'
fig_vol1.yaxis.axis_label = 'Voltaje [V]'
fig_vol1.legend.location = "top_left"

# Voltaje2
fig_vol2 = figure(title='Voltaje 2', plot_width=600, plot_height=300, y_axis_location="left", y_range=(-1, 1))
fig_vol2.line(x='time', y='vol2', alpha=0.8, line_width=3, color='red', source=DataSource_tanques,
              legend_label='Vol2')
fig_vol2.xaxis.axis_label = 'Tiempo [S]'
fig_vol2.yaxis.axis_label = 'Voltaje [V]'
fig_vol2.legend.location = "top_left"

''' ******************** Main Loop ******************** '''


# Funcion principal que se llama cada cierto tiempo para mostrar la informacion
def MainLoop():  # Funcion principal que se llama cada cierto tiempo para mostrar la informacion
    global t, ref1, ref2, automatico, cont, primer_ciclo
    if primer_ciclo:
        pid1.reset()
        pid2.reset()
        primer_ciclo = False


    h1 = cliente.alturas['H1'].get_value()
    h2 = cliente.alturas['H2'].get_value()
    h3 = cliente.alturas['H3'].get_value()
    h4 = cliente.alturas['H4'].get_value()

    v1 = cliente.valvulas['valvula1'].get_value()
    v2 = cliente.valvulas['valvula2'].get_value()

    if automatico:
        ref11 = ref1
        ref22 = ref2
        u1 = pid1.update(h1)
        u2 = pid2.update(h2)
        cliente.valvulas['valvula1'].set_value(u1)
        cliente.valvulas['valvula2'].set_value(u2)
    else:
        ref11 = -1
        ref22 = -1

    update = dict(time=[t], ref1=[ref11], real1=[h1], ref2=[ref22], real2=[h2],
                  real3=[h3], real4=[h4], vol1=[v1], vol2=[v2])

    DataSource_tanques.stream(new_data=update, rollover=200)

    if datos_a_guardar is not None:
        g1 = cliente.razones['razon1'].get_value()
        g2 = cliente.razones['razon2'].get_value()
        datos_a_guardar.loc[cont] = [t, h1, h2, h3, h4, ref11, ref22, *pid1.ctes(), *pid2.ctes(), v1, v2, g1, g2]
        cont += 1

    t += 1


layout = layout([
    [fig_tanque3, fig_tanque4],
    [fig_tanque1, fig_tanque2],
    [fig_vol1, fig_vol2]
])

panel1 = Panel(child=row(
    Column(label1, row(Column(dataRecordingButton, dataRecordingLabel), Column(extensionsDropdown)), refEst1, refEst2,
           row(Column(valvula1Label, Kp1,
                      Ki1, Kd1, Kw1), Column(valvula2Label, Kp2, Ki2, Kd2, Kw2)), row(alarm, alarm_list)),
    layout), title='Modo Automático')
panel2 = Panel(child=row(
    Column(label2, row(Column(dataRecordingButton, dataRecordingLabel), Column(extensionsDropdown)),
           row(Column(valvula1Label, voltageV1, razonFlujoV1),
               Column(valvula2Label, voltageV2, razonFlujoV2)), row(alarm, alarm_list)), layout), title='Modo Manual')

# Tabs
tabs = Tabs(tabs=[panel1, panel2])

''' ******************** Events functions ******************** '''


sliderInputs = [refEst1, refEst2, voltageV1, voltageV2, razonFlujoV1,
                razonFlujoV2]


# Texto
def kp1_change(attr, old, new):
    pid1.Kp = float(new)
Kp1.on_change('value', kp1_change)

def ki1_change(attr, old, new):
    pid1.Ki = float(new)
Ki1.on_change('value', ki1_change)

def kd1_change(attr, old, new):
    pid1.Kd = float(new)
Kd1.on_change('value', kd1_change)

def kw1_change(attr, old, new):
    pid1.Kw = float(new)
Kw1.on_change('value', kw1_change)


def kp2_change(attr, old, new):
    pid2.Kp = float(new)
Kp2.on_change('value', kp2_change)

def ki2_change(attr, old, new):
    pid2.Ki = float(new)
Ki2.on_change('value', ki2_change)

def kd2_change(attr, old, new):
    pid2.Kd = float(new)
Kd2.on_change('value', kd2_change)

def kw2_change(attr, old, new):
    pid2.Kw = float(new)
Kw2.on_change('value', kw2_change)



# Sliders
def slider_changes_ref1(attr, old, new):
    global ref1
    ref1 = new
    pid1.ref = ref1


refEst1.on_change('value', slider_changes_ref1)


def slider_changes_ref2(attr, old, new):
    global ref2
    ref2 = new
    pid2.ref = ref2


refEst2.on_change('value', slider_changes_ref2)


def slider_changes_voltaje1(attr, old, new):
    cliente.valvulas['valvula1'].set_value(new)


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
    global datos_a_guardar, extension, n_archivos, cont
    # We were recording the data
    if dataRecordingLabel.visible:
        dataRecordingButton.button_type = 'success'
        dataRecordingButton.label = 'Comenzar a adquirir datos'
        if extension == 'csv':
            datos_a_guardar.to_csv('Datos_{}.csv'.format(n_archivos))
        elif extension == 'txt':
            tfile = open('Datos_{}.txt'.format(n_archivos), 'a')
            tfile.write(datos_a_guardar.to_string())
            tfile.close()
        elif extension == 'npy':
            aux = datos_a_guardar.to_numpy()
            np.save('Datos_{}.npy'.format(n_archivos), aux)
        datos_a_guardar = None
        n_archivos += 1
        cont = 0
    else:
        dataRecordingButton.button_type = 'danger'
        dataRecordingButton.label = 'Dejar de adquirir datos'
        datos_a_guardar = pd.DataFrame(columns=['Tiempo', 'Tanque1', 'Tanque2', 'Tanque3', 'Tanque4', 'Ref1', 'Ref2',
                                                'kp1', 'ki1', 'kd1', 'kw1', 'kp2', 'ki2', 'kd2', 'kw2', 'V1', 'V2',
                                                'Gamma1', 'Gamma2'])

    dataRecordingLabel.visible = not dataRecordingLabel.visible


dataRecordingButton.on_click(recordingButtonClicked)


# Dropdown
def extensionsDropdownChanged(event):
    global extension
    extension = event.item


extensionsDropdown.on_event(MenuItemClick, extensionsDropdownChanged)


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


''' ******************** Curdoc ******************** '''

curdoc().add_root(tabs)
curdoc().title = 'Experiencia 1: Control de Procesos'
curdoc().add_periodic_callback(MainLoop, 150)

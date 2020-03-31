import numpy as np
from bokeh.models import ColumnDataSource, PreText
from bokeh.layouts import layout
from bokeh.plotting import curdoc, figure
import threading
from cliente_control import Cliente

# DataSources
DataSource_tanque1 = ColumnDataSource(dict(time=[], ref=[], real=[]))
DataSource_tanque2 = ColumnDataSource(dict(time=[], ref=[], real=[]))
DataSource_tanque3 = ColumnDataSource(dict(time=[], real=[]))
DataSource_tanque4 = ColumnDataSource(dict(time=[], real=[]))

# Figuras
# Tanque 1
fig_tanque1 = figure(title='Tanque 1', plot_width=600, plot_height=300, y_axis_location="left", y_range=(0, 70))
fig_tanque1.line(x='time', y='ref', alpha=0.8, line_width=3, color='black', source=DataSource_tanque1, legend='Ref')
fig_tanque1.line(x='time', y='real', alpha=0.8, line_width=3, color='red', source=DataSource_tanque1, legend='Real')
fig_tanque1.xaxis.axis_label = 'Tiempo (S)'
fig_tanque1.yaxis.axis_label = 'Valores'
fig_tanque1.legend.location = "top_left"

# Tanque 2
fig_tanque2 = figure(title='Tanque 2', plot_width=600, plot_height=300, y_axis_location="left", y_range=(0, 70))
fig_tanque2.line(x='time', y='ref', alpha=0.8, line_width=3, color='black', source=DataSource_tanque2, legend='Ref')
fig_tanque2.line(x='time', y='real', alpha=0.8, line_width=3, color='red', source=DataSource_tanque2, legend='Real')
fig_tanque2.xaxis.axis_label = 'Tiempo (S)'
fig_tanque2.yaxis.axis_label = 'Valores'
fig_tanque2.legend.location = "top_left"

# Tanque 3
fig_tanque3 = figure(title='Tanque 2', plot_width=600, plot_height=300, y_axis_location="left", y_range=(0, 70))
fig_tanque3.line(x='time', y='real', alpha=0.8, line_width=3, color='red', source=DataSource_tanque3, legend='Real')
fig_tanque3.xaxis.axis_label = 'Tiempo (S)'
fig_tanque3.yaxis.axis_label = 'Valores'
fig_tanque3.legend.location = "top_left"

# Tanque 4
fig_tanque4 = figure(title='Tanque 2', plot_width=600, plot_height=300, y_axis_location="left", y_range=(0, 70))
fig_tanque4.line(x='time', y='real', alpha=0.8, line_width=3, color='red', source=DataSource_tanque4, legend='Real')
fig_tanque4.xaxis.axis_label = 'Tiempo (S)'
fig_tanque4.yaxis.axis_label = 'Valores'
fig_tanque4.legend.location = "top_left"

# Widgets para desplegar valores
estilo1 = {'color': 'white', 'font': '15px bold arial, sans-serif', 'background-color': 'black', 'text-align': 'center',
           'border-radius': '7px'}
estilo2 = {'color': 'white', 'font': '15px bold arial, sans-serif', 'background-color': 'red', 'text-align': 'center',
           'border-radius': '7px'}
# ref_tanque1 = PreText(text='Valor de referencia: 0.00 ', width=300, style=estilo1)
real_tanque1 = PreText(text='Valor real: 0.00', width=600, style=estilo2)

# ref_tanque2 = PreText(text='Valor de referencia: 0.00 ', width=300, style=estilo1)
real_tanque2 = PreText(text='Valor real: 0.00', width=600, style=estilo2)

real_tanque3 = PreText(text='Valor real: 0.00', width=600, style=estilo2)

real_tanque4 = PreText(text='Valor real: 0.00', width=600, style=estilo2)


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


cliente = Cliente("opc.tcp://localhost:4840/freeopcua/server/", suscribir_eventos=True, SubHandler=SubHandler)
cliente.conectar()

t = 0


def MainLoop():  # Funcion principal que se llama cada cierto tiempo para mostrar la informacion
    global t

    h1 = cliente.alturas['H1'].get_value()
    update = dict(time=[t], ref=[32], real=[h1])
    DataSource_tanque1.stream(new_data=update, rollover=50)  # Se ven los ultimos 100 datos
    real_tanque1.text = 'Valor real: {}'.format(round(h1, 2))

    h2 = cliente.alturas['H2'].get_value()
    update = dict(time=[t], ref=[32], real=[h2])
    DataSource_tanque2.stream(new_data=update, rollover=50)  # Se ven los ultimos 100 datos
    real_tanque2.text = 'Valor real: {}'.format(round(h2, 2))

    h3 = cliente.alturas['H3'].get_value()
    update = dict(time=[t], real=[h3])
    DataSource_tanque3.stream(new_data=update, rollover=50)  # Se ven los ultimos 100 datos
    real_tanque3.text = 'Valor real: {}'.format(round(h3, 2))

    h4 = cliente.alturas['H4'].get_value()
    update = dict(time=[t], real=[h4])
    DataSource_tanque4.stream(new_data=update, rollover=50)  # Se ven los ultimos 100 datos
    real_tanque4.text = 'Valor real: {}'.format(round(h4, 2))

    t += 1


l = layout([
    [fig_tanque3, fig_tanque4],
    [real_tanque3, real_tanque4],
    [fig_tanque1, fig_tanque2],
    [real_tanque1, real_tanque2]
])

curdoc().add_root(l)
curdoc().title = "Mile-Lolo-Mathi"
curdoc().add_periodic_callback(MainLoop, 100)  # Cada 100 milisegundos se llama a la funcion y se actualiza el grafico

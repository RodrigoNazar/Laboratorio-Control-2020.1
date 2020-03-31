import numpy as np
from bokeh.models import ColumnDataSource, PreText
from bokeh.layouts import layout
from bokeh.plotting import curdoc, figure
import threading
from cliente_control import Cliente
from collections import deque

# DataSources
DataSource_tanques = ColumnDataSource(dict(time=[], ref1=[], real1=[], ref2=[], real2=[], real3=[], real4=[], vol1=[], vol2=[]))

# Figuras
# Tanque 1
fig_tanque1 = figure(title='Tanque 1', plot_width=600, plot_height=300, y_axis_location="left", y_range=(0, 70))
l1t1 = fig_tanque1.line(x='time', y='ref1', alpha=0.8, line_width=3, color='black', source=DataSource_tanques,
                        legend='Ref')
l2t1 = fig_tanque1.line(x='time', y='real1', alpha=0.8, line_width=3, color='red', source=DataSource_tanques,
                        legend='Real')
fig_tanque1.xaxis.axis_label = 'Tiempo (S)'
fig_tanque1.yaxis.axis_label = 'Valores'
fig_tanque1.legend.location = "top_left"

# Tanque 2
fig_tanque2 = figure(title='Tanque 2', plot_width=600, plot_height=300, y_axis_location="left", y_range=(0, 70))
l1t2 = fig_tanque2.line(x='time', y='ref2', alpha=0.8, line_width=3, color='black', source=DataSource_tanques,
                        legend='Ref')
l2t2 = fig_tanque2.line(x='time', y='real2', alpha=0.8, line_width=3, color='red', source=DataSource_tanques,
                        legend='Real')
fig_tanque2.xaxis.axis_label = 'Tiempo (S)'
fig_tanque2.yaxis.axis_label = 'Valores'
fig_tanque2.legend.location = "top_left"

# Tanque 3
fig_tanque3 = figure(title='Tanque 3', plot_width=600, plot_height=300, y_axis_location="left", y_range=(0, 70))
l1t3 = fig_tanque3.line(x='time', y='real3', alpha=0.8, line_width=3, color='red', source=DataSource_tanques,
                        legend='Real')
fig_tanque3.xaxis.axis_label = 'Tiempo (S)'
fig_tanque3.yaxis.axis_label = 'Valores'
fig_tanque3.legend.location = "top_left"

# Tanque 4
fig_tanque4 = figure(title='Tanque 4', plot_width=600, plot_height=300, y_axis_location="left", y_range=(0, 70))
l1t4 = fig_tanque4.line(x='time', y='real4', alpha=0.8, line_width=3, color='red', source=DataSource_tanques,
                        legend='Real')
fig_tanque4.xaxis.axis_label = 'Tiempo (S)'
fig_tanque4.yaxis.axis_label = 'Valores'
fig_tanque4.legend.location = "top_left"

# Voltaje1
fig_vol1 = figure(title='Voltaje 1', plot_width=600, plot_height=300, y_axis_location="left", y_range=(-5, 5))
fig_vol1.line(x='time', y='vol1', alpha=0.8, line_width=3, color='red', source=DataSource_tanques,
                        legend='Vol1')
fig_vol1.xaxis.axis_label = 'Tiempo (S)'
fig_vol1.yaxis.axis_label = '[V]'
fig_vol1.legend.location = "top_left"

# Voltaje2
fig_vol2 = figure(title='Voltaje 2', plot_width=600, plot_height=300, y_axis_location="left", y_range=(-5, 5))
fig_vol2.line(x='time', y='vol2', alpha=0.8, line_width=3, color='red', source=DataSource_tanques,
                        legend='Vol2')
fig_vol2.xaxis.axis_label = 'Tiempo (S)'
fig_vol2.yaxis.axis_label = '[V]'
fig_vol2.legend.location = "top_left"



def funcion_handler(node, val):
    key = node.get_parent().get_display_name().Text
    if key == 'Tanque1':
        pass


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
    h2 = cliente.alturas['H2'].get_value()
    h3 = cliente.alturas['H3'].get_value()
    h4 = cliente.alturas['H4'].get_value()
    v1 = cliente.valvulas['valvula1'].get_value()
    v2 = cliente.valvulas['valvula2'].get_value()

    update = dict(time=[t], ref1=[50 * np.random.random()], real1=[h1],
                  ref2=[50 * np.random.random()], real2=[h2], real3=[h3], real4=[h4], vol1=[v1], vol2=[v2])
    DataSource_tanques.stream(new_data=update, rollover=200)  # Se ven los ultimos 200 datos
    t += 1


l = layout([
    [fig_tanque3, fig_tanque4],
    [fig_tanque1, fig_tanque2],
    [fig_vol1, fig_vol2]
])

curdoc().add_root(l)
curdoc().title = "Mile-Lolo-Mathi"
curdoc().add_periodic_callback(MainLoop, 100)  # Cada 100 milisegundos se llama a la funcion y se actualiza el grafico

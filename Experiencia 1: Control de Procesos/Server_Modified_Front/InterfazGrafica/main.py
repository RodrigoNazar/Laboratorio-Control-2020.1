import numpy as np

from bokeh.models import (Div, Tabs, Panel, Slider, Column, TextInput, PreText,
                          ColumnDataSource)
from bokeh.plotting import curdoc, figure
from bokeh.layouts import layout, row


''' Modo Automático '''
label1 = Div(text='<h1>Modo Automático</h1>')
ref = Slider(title="Altura de Referencia", value=0.0, start=0.0, end=50.0,
                   step=0.1)

Kp = TextInput(title="Constante Proporcional", value='0')
Ki = TextInput(title="Constante Integral", value='0')
Kd = TextInput(title="Constante Derivativa", value='0')


''' Modo Manual '''
label2 = Div(text='<h1>Modo Manual</h1>')
voltageV1 = Slider(title="Voltaje Válvula 1", value=0.0, start=-1.0, end=1.0,
                   step=0.01)
voltageV2 = Slider(title="Voltaje Válvula 2", value=0.0, start=-1.0, end=1.0,
                   step=0.01)


''' Added stuff '''

# Se crea un seno
T = np.linspace(0, 1000, 1001)
sin = np.sin(T)
cos = np.cos(T)

# Se crea el DataSource
DataSource = ColumnDataSource({'time': [], 'sin': [], 'cos': []})

# Figura
fig_sin = figure(title='Seno y Coseno', plot_width=600, plot_height=200,
                 tools="reset,xpan,xwheel_zoom,xbox_zoom",
                 y_axis_location="left")
fig_sin.line(x='time', y='sin', alpha=0.8, line_width=3, color='blue',
             source=DataSource, legend_label='Seno')
fig_sin.line(x='time', y='cos', alpha=0.8, line_width=3, color='red',
             source=DataSource, legend_label='Coseno')
fig_sin.xaxis.axis_label = 'Tiempo (S)'
fig_sin.yaxis.axis_label = 'Valores'

# Se crea un par de Widgets
estilo = {'color': 'white', 'font': '15px bold arial, sans-serif',
          'background-color': 'green', 'text-align': 'center',
          'border-radius': '7px'}
SinText = PreText(text='Valor del Seno: 0.00 ', width=300, style=estilo)
CosText = PreText(text='Valor del Coseno: 0.00', width=300, style=estilo)

t = 0


# Funcion principal que se llama cada cierto tiempo para mostrar la informacion
def MainLoop():
    global t, sin, cos
    update = dict(time=[t], sin=[sin[t]], cos=[cos[t]])
    # Se ven los ultimos 100 datos
    DataSource.stream(new_data=update, rollover=100)
    SinText.text = 'Valor del Seno: {}'.format(round(sin[t], 2))
    CosText.text = 'Valor del Coseno: {}'.format(round(cos[t], 2))
    t += 1


layout = layout([
   [fig_sin],
   [SinText, CosText]
   ])


panel1 = Panel(child=Column(label1, ref, Kp, Ki, Kd), title='Modo Automático')
panel2 = Panel(child=Column(label2, voltageV1, voltageV2), title='Modo Manual')

# Tabs
tabs = Tabs(tabs=[panel1, panel2])


''' Change functions '''


def panelActive(attr, old, new):
    '''
    Changes the operation mode if a tab is changed
    '''
    if tabs.active == 0:
        print('Modo automático activado')

    elif tabs.active == 1:
        print('Modo manual activado')


tabs.on_change('active', panelActive)

curdoc().add_root(tabs)
curdoc().title = 'Experiencia 1: Control de Procesos'
curdoc().add_periodic_callback(MainLoop, 100)

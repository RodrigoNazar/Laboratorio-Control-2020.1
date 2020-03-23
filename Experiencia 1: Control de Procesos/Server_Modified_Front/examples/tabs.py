from bokeh.layouts import widgetbox
from bokeh.models import Div, Tabs, Panel
from bokeh.plotting import curdoc

label1 = Div(text = 'Tab 1')
label2 = Div(text = 'Tab 2')
panel1 = Panel(child = widgetbox(label1), title = 'Tab 1')
panel2 = Panel(child = widgetbox(label2), title = 'Tab 2')
tabs = Tabs(tabs = [panel1, panel2])

def panelActive(attr, old, new):
    print("the active panel is " + str(tabs.active))

tabs.on_change('active', panelActive)

curdoc().add_root(tabs)

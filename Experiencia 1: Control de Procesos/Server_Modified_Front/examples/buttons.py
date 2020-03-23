from bokeh.models import Button, Div, RadioGroup
from bokeh.io import curdoc


bt = Button(label='Click me', button_type="success")
bt2 = Button(label='Dont click me', button_type="success")


def change_click():
    print('I was clicked')


bt.on_click(change_click)
bt2.on_click(change_click)

radio_group = RadioGroup(
        labels=["Option 1", "Option 2", "Option 3"], active=0)


div = Div(text="""Your <a href="https://en.wikipedia.org/wiki/HTML">HTML</a>-supported text is initialized with the <b>text</b> argument.  The
remaining div arguments are <b>width</b> and <b>height</b>. For this example, those values
are <i>200</i> and <i>100</i> respectively.""",
width=200, height=100)


curdoc().add_root(bt)
curdoc().add_root(bt2)
curdoc().add_root(radio_group)
curdoc().add_root(div)

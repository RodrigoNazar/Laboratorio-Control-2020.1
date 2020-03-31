import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from cliente_control import Cliente
import threading

t = np.arange(0, 3, .01)


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.modo = True
        self.place(relwidth=1, relheight=1)

    def create_widgets(self):
        self.titulo = tk.Label(self, text='Control de Procesos', font=("Times", 44))
        self.titulo.place(x=320, y=5)

        self.boton_automatico = tk.Button(self, text='Modo automatico', font=("Times", 24), command=self.mostrar)
        self.boton_automatico.place(x=320, y=60)

        self.boton_manual = tk.Button(self, text='Modo manual', font=("Times", 24), command=self.mostrar)
        self.boton_manual.place(x=505, y=60)

        # Figura Tanque 3
        self._fig_tq3 = plt.Figure(figsize=(6, 4), dpi=70)
        self._fig_tq3.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))
        self._fig_tq3.suptitle('Tanque3')
        self.fig_tq3 = FigureCanvasTkAgg(self._fig_tq3, self.master)
        self.fig_tq3.draw()
        self.fig_tq3.get_tk_widget().place(x=100, y=200)

        # Figura Tanque 4
        self._fig_tq4 = plt.Figure(figsize=(6, 4), dpi=70)
        self._fig_tq4.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))
        self._fig_tq4.suptitle('Tanque4')
        self.fig_tq4 = FigureCanvasTkAgg(self._fig_tq4, self.master)
        self.fig_tq4.draw()
        self.fig_tq4.get_tk_widget().place(x=500, y=200)

        # Figura Tanque 1
        self._fig_tq1 = plt.Figure(figsize=(6, 4), dpi=70)
        self._fig_tq1.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))
        self._fig_tq1.suptitle('Tanque1')
        self.fig_tq1 = FigureCanvasTkAgg(self._fig_tq1, self.master)
        self.fig_tq1.draw()
        self.fig_tq1.get_tk_widget().place(x=100, y=550)

        # Figura Tanque 2
        self._fig_tq2 = plt.Figure(figsize=(6, 4), dpi=70)
        self._fig_tq2.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))
        self._fig_tq2.suptitle('Tanque2')
        self.fig_tq2 = FigureCanvasTkAgg(self._fig_tq2, self.master)
        self.fig_tq2.draw()
        self.fig_tq2.get_tk_widget().place(x=500, y=550)

        #
        # self.quit = tk.Button(self, text="Mostrar", fg="red",
        #                       command=self.mostrar)
        # self.quit.pack(side="top")

    def mostrar(self):
        if self.modo:
            self.titulo.place_forget()
        else:
            self.titulo.place(x=320, y=5)
        self.modo = not self.modo


if '__main__' == __name__:
    t2 = []

    root = tk.Tk()
    root.geometry('1000x900')
    app = Application(master=root)
    app.master.title("Mile - Lolo - Mathi")


    def funcion_handler(node, val):
        key = node.get_parent().get_display_name().Text
        if key == 'Tanque1':
            t2.append(val)
            app._fig_tq2.add_subplot(111).plot(np.array(t2))


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


    # ki = threading.Thread(target=app.mainloop)
    # ki.start()

    # cliente = Cliente("opc.tcp://localhost:4840/freeopcua/server/", suscribir_eventos=True, SubHandler=SubHandler)
    # cliente.conectar()
    # cliente.subscribir_cv()  # Se subscribe a las variables controladas

    app.mainloop()

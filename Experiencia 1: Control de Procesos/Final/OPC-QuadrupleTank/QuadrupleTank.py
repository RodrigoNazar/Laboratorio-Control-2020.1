import numpy as np
from scipy.integrate import odeint
import scipy.integrate as integrator
import matplotlib.pyplot as plt
import pygame
import time
import sys
from cliente import Cliente  # cliente OPCUA
import random
import threading


class QuadrupleTank():
    def __init__(self, x0, Hmax, voltmax):
        self.x0 = x0
        self.t = 0

        # Parámetros
        self.A = [28, 32, 28, 32]  # cm^2
        self.a = [0.071, 0.057, 0.071, 0.057]  # cm^2
        self.g = 981  # cm/s^2
        self.rho = 1  # g/cm^3
        self.kout = 0.5
        self.kin = 3.33

        self.time_scaling = 1
        self.gamma = [0.7, 0.6]  # %
        self.volt = [0., 0.]  # %
        self.voltmax = voltmax
        self.x = self.x0
        self.ti = 0
        self.Ts = 0
        self.Hmax = Hmax
        self.Hmin = 0.0

    # Restricciones físicas de los tanques
    def Limites(self):
        for i in range(len(self.x)):
            if self.x[i] > self.Hmax:
                self.x[i] = self.Hmax
            elif self.x[i] < 1e-2:
                self.x[i] = 1e-2

        for i in range(2):
            if self.volt[i] > 1:
                self.volt[i] = 1
            elif self.volt[i] < -1:
                self.volt[i] = -1

    # Ecuaciones diferenciales de los tanques
    def xd_func(self, x, t):
        xd0 = -self.a[0] / self.A[0] * np.sqrt(2 * self.g * x[0]) + self.a[2] / self.A[0] * np.sqrt(2 * self.g * x[2]) + \
              self.gamma[0] * self.kin * self.volt[0] * self.voltmax / self.A[0]
        xd1 = -self.a[1] / self.A[1] * np.sqrt(2 * self.g * x[1]) + self.a[3] / self.A[1] * np.sqrt(2 * self.g * x[3]) + \
              self.gamma[1] * self.kin * self.volt[1] * self.voltmax / self.A[1]
        xd2 = -self.a[2] / self.A[2] * np.sqrt(2 * self.g * x[2]) + (1 - self.gamma[1]) * self.kin * self.volt[
            1] * self.voltmax / self.A[2]
        xd3 = -self.a[3] / self.A[3] * np.sqrt(2 * self.g * x[3]) + (1 - self.gamma[0]) * self.kin * self.volt[
            0] * self.voltmax / self.A[3]
        res = [xd0, xd1, xd2, xd3]
        for i in range(len(res)):

            if np.isnan(res[i]) or type(res[i]) != np.float64:
                res[i] = 0
        return np.multiply(self.time_scaling, res)

    # Integración en "tiempo real"
    def sim(self):
        self.x0 = np.array(self.x)  # Estado actual se vuelve condición inicial para el nuevo estado
        self.Ts = time.time() - self.ti
        # self.Ts = 0.01
        t = np.linspace(0, self.Ts, 2)
        x = odeint(self.xd_func, self.x0, t)  # Perform integration using Fortran's LSODA (Adams & BDF methods)
        self.x = [x[-1, 0], x[-1, 1], x[-1, 2], x[-1, 3]]
        self.Limites()
        # print(self.x)
        self.ti = time.time()
        return self.x


######################## Cliente opc ####################################

# Se declaran después cuando se haga el controlador
variables_manipuladas = {'Valvula1': 0, 'Valvula2': 0, 'Razon1': 0, 'Razon2': 0}


# Función que se suscribe
def funcion_handler(node, val):
    key = node.get_parent().get_display_name().Text
    variables_manipuladas[
        key] = val  # Se cambia globalmente el valor de las variables manipuladas cada vez que estas cambian
    print('key: {} | val: {}'.format(key, val))


class SubHandler(object):  # Clase debe estar en el script porque el thread que comienza debe mover variables globales
    def datachange_notification(self, node, val, data):
        thread_handler = threading.Thread(target=funcion_handler,
                                          args=(node, val))  # Se realiza la descarga por un thread
        thread_handler.start()

    def event_notification(self, event):
        # print("Python: New event", event)
        pass


def QuadrupleTankRoutine():

    cliente = Cliente("opc.tcp://localhost:4840/freeopcua/server/", suscribir_eventos=True, SubHandler=SubHandler)
    cliente.conectar()
    # cliente.subscribir_mv() # Se subscribe a las variables manipuladas


    ######################### Main loop #################################

    # Setup
    x0 = [40, 40, 40, 40]  # Condición inicial de los tanques
    # x0=[33.915, 35.224, 4.485, 3.914] #Condición inicial de los tanques (eq para u_eq = (0.5,0.5)) y gamma = (0.7,0.6)
    # x0=[28.029, 43.489, 10.091, 15.656] #Condic

    #
    # drh dfh dión inicial de los tanques (eq para u_eq = (0.5,0.5)) y gamma = (0.4,0.4)
    Hmax = 50
    voltmax = 10
    fps = 20
    sensibilidad = 0.01  # Cambio de las varibles manipuladas cada vez que se aprieta una tecla
    # clock = pygame.time.Clock()  # Limita la cantidad de FPS
    first_it = True

    sistema = QuadrupleTank(x0=x0, Hmax=Hmax, voltmax=voltmax)

    cliente.razones['razon1'].set_value(sistema.gamma[0])
    cliente.razones['razon2'].set_value(sistema.gamma[1])


    cliente.valvulas['valvula1'].set_value(0)
    cliente.valvulas['valvula2'].set_value(0)

    sistema.time_scaling = 1  # Para el tiempo
    # interfaz = Interfaz_grafica(Hmax=Hmax)
    # interfaz.paint()
    running = True
    manual = False  # Control Manual o automático de las variables
    t = 0
    alturasMatrix = []


    while running:

        # Actualización del sistema de forma manual
        if manual:
            running, u = interfaz.eventos(running, sensibilidad, sistema.volt[0], sistema.volt[1], sistema.gamma[0],
                                          sistema.gamma[1])
            sistema.volt[0] = u['valvula1']
            sistema.volt[1] = u['valvula2']
            sistema.gamma[0] = u['razon1']
            sistema.gamma[1] = u['razon2']

            # Envío de los valores por OPC cuando se está en forma manual
            # Obtención de los pumps
            cliente.valvulas['valvula1'].set_value(u['valvula1'])
            cliente.valvulas['valvula2'].set_value(u['valvula2'])

            # Obtención de los switches
            cliente.razones['razon1'].set_value(u['razon1'])
            cliente.razones['razon2'].set_value(u['razon2'])
        else:
            volt1 = cliente.valvulas['valvula1'].get_value()
            volt2 = cliente.valvulas['valvula2'].get_value()

            gamma1 = cliente.razones['razon1'].get_value()
            gamma2 = cliente.razones['razon2'].get_value()

            if volt1 > 1 or volt1 < -1 or volt2 > 1 or volt2 < -1 \
                    or gamma1 > 1 or gamma1 < 0 or gamma2 > 1 or gamma2 < 0:
                raise ValueError('Valores fuera del rango específicado')

            # interfaz.Automatico(volt1, volt2, gamma1, gamma2)

            sistema.volt[0] = volt1
            sistema.volt[1] = volt2
            sistema.gamma[0] = gamma1
            sistema.gamma[1] = gamma2

        # interfaz.screen.blit(interfaz.background, (0, 0))
        # interfaz.screen.blit(interfaz.textSurf, (0,0))

        ####### Simulación del sistema ######
        if first_it:
            sistema.ti = time.time()
            first_it = False

        alturas = sistema.sim()
        ####### Updates interfaz #################

        ##    # Tanque 1
        ##    interfaz.Tank_update(altura=alturas[0], posicion=interfaz.posTank1)
        ##
        ##    # Tanque 2
        ##    interfaz.Tank_update(altura=alturas[1], posicion=interfaz.posTank2)
        ##
        ##    # Tanque 3
        ##    interfaz.Tank_update(altura=alturas[2], posicion=interfaz.posTank3)
        ##
        ##    # Tanque 4
        ##    interfaz.Tank_update(altura=alturas[3], posicion=interfaz.posTank4)

        ############ UPDATE CLIENTE OPC ##################################
        cliente.alturas['H1'].set_value(alturas[0])
        cliente.alturas['H2'].set_value(alturas[1])
        cliente.alturas['H3'].set_value(alturas[2])
        cliente.alturas['H4'].set_value(alturas[3])

        cliente.temperaturas['T1'].set_value(22 + random.randrange(-7, 7, 1))
        cliente.temperaturas['T2'].set_value(22 + random.randrange(-7, 7, 1))
        cliente.temperaturas['T3'].set_value(22 + random.randrange(-7, 7, 1))
        cliente.temperaturas['T4'].set_value(22 + random.randrange(-7, 7, 1))

        # pygame.display.flip()
        # clock.tick(fps)

    # pygame.quit()

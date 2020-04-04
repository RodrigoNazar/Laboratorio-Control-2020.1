from opcua import ua
from time import time
from cliente import Cliente, SubHandler, funcion_handler
import matplotlib.pyplot as plt

class PID:
    def __init__(self, y, ref, T, tau, Kp, Ki, Kd, limitador, uk1, uk2, e1, e2, cliente):
        self.N = tau # Valor del polo del filtro pasabajos
        # Calculo de constantes del problema
        self.a0 = (1 + N*T)
        self.a1 = -(2 + N*T)
        self.a2 = 1
        self.b0 = Kp * (1 + N*T) + Ki*T*(1 + N*T) + Kd*N
        self.b1 = -(Kp*(2+N*T) + Ki*T + 2*Kd*N)
        self.b2 = Kp + Kd*N
        self.ku1 = a1/a0
        self.ku2 = a2/a0
        self.ke0 = b0/a0
        self.ke1 = b1/a0
        self.ke2 = b2/a0

        error = ref - y
        u0 = - (ku1*uk1) - (ku2*uk2) + (ke0*error) + (ke1*e1) + (ke2*e2)


def controlador_pid(y, ref, T, tau, Kp, Ki, Kd, limitador, uk1, uk2, e1, e2):
    N = tau # Valor del polo del filtro pasabajos
    # Calculo de constantes del problema
    a0 = (1 + N*T)
    a1 = -(2 + N*T)
    a2 = 1
    b0 = Kp * (1 + N*T) + Ki*T*(1 + N*T) + Kd*N
    b1 = -(Kp*(2+N*T) + Ki*T + 2*Kd*N)
    b2 = Kp + Kd*N
    ku1 = a1/a0
    ku2 = a2/a0
    ke0 = b0/a0
    ke1 = b1/a0
    ke2 = b2/a0

    error = ref - y
    u0 = - (ku1*uk1) - (ku2*uk2) + (ke0*error) + (ke1*e1) + (ke2*e2)

    if u0 > limitador:
        u0 = limitador
    elif u0 < -limitador:
        u0 = -limitador
    return u0, error


def alturas_get():
    h1 = cliente.alturas['H1'].get_value()
    h2 = cliente.alturas['H2'].get_value()
    h3 = cliente.alturas['H3'].get_value()
    h4 = cliente.alturas['H4'].get_value()
    return h1, h2, h3, h4

def voltajes_get():
    v1 = cliente.valvulas['valvula1'].get_value()
    v2 = cliente.valvulas['valvula2'].get_value()
    return v1, v2

def razones_get():
    r1 = cliente.razones['razon1']
    r2 = cliente.razones['razon2']
    return r1, r2

def voltajes_set(v1, v2):
    cliente.valvulas['valvula1'].set_value(v1)
    cliente.valvulas['valvula2'].set_value(v2)


if __name__ == "__main__":
    cliente = Cliente("opc.tcp://localhost:4840/freeopcua/server/", suscribir_eventos=True, SubHandler=SubHandler)
    cliente.conectar()

    h1_list = []
    h2_list = []
    h3_list = []
    h4_list = []
    v1_list = []
    v2_list = []
    #Intervalo discretizacion de Euler hacia adelante
    T = 0.5
    #constantes PID variable controlada 1
    kp1 = 1
    ki1 = 0.8
    kd1 = 0.5
    kw1 = 1
    #constantes PID variable controlada 2
    kp2 = kp1
    ki2 = ki1
    kd2 = kd1
    kw2 = kw1
    #Limitador variable manipulada
    limitador = 1
    #referencias
    ref1 = 20
    ref2 = 25
    #valor para filtro pasabajos
    N = 20
    error1 = 5
    error2 = 5
    voltajes_set(0, 0)
    t = 0

    # pid1 = PID(kp1, ki1, kd1, kw1)
    # pid2 = PID(kp2, ki2, kd2, kw2)
    # pid1.setPoint = ref1
    # pid2.setPoint = ref2
    while t <= 3000:
        #Obtener variables
        h1, h2, h3, h4 = alturas_get()
        v1, v2 = voltajes_get()
        r1, r2 = razones_get()
        h1_list.append(h1)
        h2_list.append(h2)
        h3_list.append(h3)
        h4_list.append(h4)
        v1_list.append(v1)
        v2_list.append(v2)

        if len(h1_list) == 1:
            v1_1 = v1
            v2_1 = v1
            e1_1 = 0
            e1_2 = 0
            e2_1 = 0
            e2_2 = 0
        else:
            v1_2 = v1_1
            v2_2 = v2_1
            v1_1 = v1
            v2_1 = v2

            e1_2 = e1_1
            e2_2 = e2_1
            e1_1 = error1
            e2_1 = error2


            u1, error1 = controlador_pid(h1, ref1, T, N, kp1, ki1, kd1, limitador, v1_1, v1_2, e1_1, e1_2)
            u2, error2 = controlador_pid(h2, ref2, T, N, kp2, ki2, kd2, limitador, v2_1, v2_2, e2_1, e2_2)
            # print("u1 = {}, u2  {}".format(u1, u2))
            voltajes_set(u1, u2)
        t += 1


    n = len(h1_list)
    x = [i for i in range(n)]
    r1 = [ref1]*n
    r2 = [ref2]*n
    plt.plot(x, h1_list, color='b', label="h1")
    plt.plot(x, h2_list, color='g', label="h2")

    plt.plot(x, r1, color='r', label="ref1")
    plt.plot(x, r2, color='m', label="ref2")
    plt.legend()
    plt.ylim(0,50)
    plt.show()
    plt.plot(x, v1_list, color='g', label="v1")
    plt.plot(x, v2_list, color='orange', label="v2")
    plt.ylim(-1.2,1.2)
    plt.legend()
    plt.show()

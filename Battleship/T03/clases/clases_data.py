from string import ascii_lowercase as abc
from tools import funciones_aux as f


ataques = ["Misil de Crucero BGM-109 Tomahawk", "Misil UGM-133 Trident II",
           "Kamikaze", "Misil Balistico Intercontinental Minuteman III",
           "Napalm", "GBU-43/B Massive Ordnance Air Blast Paralizer",
           "Kit de ingenierios"]


class BarcoStats:

    def __init__(self):
        self.dano_rec = 0
        self.mov = 0
        self.att = 0
        self.att_ex = 0


class AtaqueStats:

    def __init__(self):
        self.n_usado = 0
        self.d_causado = 0


class Estadistica:

    def __init__(self, p):
        self.player = p
        self.v = {i: BarcoStats() for i in p.vehiculos}
        self.a = {i: AtaqueStats() for i in ataques}
        self.cont_ataques = 0
        self.cont_ataques_ex = 0
        self.cont_turnos = 0
        self.cont_dano_r = 0
        self.cont_dano_c = 0

    def mover(self, vehiculo):
        # Recibe instancia vehiculo que se movera y actualiza las estadisticas
        # TESTEADA
        self.cont_turnos += 1
        self.v[vehiculo].mov += 1
        return vehiculo

    def atacar(self, vehiculo, ataque, resultado, dano):
        # Recibe un vehiculo propio que ataco, nombre del ataque, el resultado
        # [0,1] con 0 exitoso , el dano causado al enemigo
        # TESTEADA
        self.cont_turnos += 1
        self.cont_ataques += 1
        self.a[ataque].n_usado += 1
        self.v[vehiculo].att += 1
        if resultado == 0:
            self.cont_dano_c += dano
            self.a[ataque].d_causado += dano
            self.cont_ataques_ex += 1
            self.v[vehiculo].att_ex += 1
        return vehiculo

    def recibir_dano(self, vehiculo_atacado, dano):
        # Recibe un vehiculo propio que fue atacado y el dano que recibio
        # TESTEADA
        self.v[vehiculo_atacado].dano_rec += dano
        self.cont_dano_r += dano
        return vehiculo_atacado

    @property
    def porcentaje_exitosos(self):
        # Retorna el porcentaje de ataques exitosos
        # TESTEADA
        if self.cont_ataques == 0:
            return 0
        else:
            return (self.cont_ataques_ex * 100) / self.cont_ataques

    @property
    def att_mas_eficiente(self):
        # Retorna tupla el ataque mas eficiente (dano causado / veces usado)
        # NO TESTEADA
        atacaron = list(filter(lambda x: x[1].n_usado != 0, self.a.items()))
        if len(atacaron) != 0:
            item_max = max(
                atacaron, key=lambda x: x[1].d_causado / x[1].n_usado)
            return (item_max[0], item_max[1].d_causado / item_max[1].n_usado)
        else:
            return ("-", "-")

    @property
    def att_mas_utilizado(self):
        # Retorna tupla con el ataque mas utilizado y las veces usado
        # TESTEADA
        item_max = max(self.a.items(), key=lambda x: x[1].n_usado)
        return (item_max[0], item_max[1].n_usado)

    @property
    def barco_mas_movido(self):
        # Retorna tupla con el barco que mas se movio
        # TESTEADA
        item_max = max(self.v.items(), key=lambda x: x[1].mov)
        return (item_max[0].name, item_max[1].mov)

    def __repr__(self):
        estado = "PERDEDOR" if self.player.is_dead() else "GANADOR"
        info = (estado, self.player.id)
        string = "\n\nESTADISTICAS DEL JUGADOR {0} (Jugador {1})\n\n".format(
            *info)
        string += "Cantidad de turnos : {}\n".format(self.cont_turnos)
        string += "Barco mas movido : {0} con {1} movimientos\n".format(
            *self.barco_mas_movido)
        string += "\nATAQUES EXITOSOS\n\n"
        string += "{}% de ataques exitosos\n\n".format(
            self.porcentaje_exitosos)
        for veh in self.v:
            if self.v[veh].att == 0:
                string += "{0} : No tuvo ataques\n".format(veh.name)
            else:
                t = (veh.name, (self.v[veh].att_ex * 100) / self.v[veh].att)
                string += "{0} : {1}% de ataques exitosos\n".format(*t)
        string += "\nANALISIS DE DAÑO\n\n"
        string += "Daño total recibido : {}\n\n".format(self.cont_dano_r)
        barcos = [veh for veh in self.v if veh.tipo == "mar"]
        for bar in barcos:
            string += "{0} : recibio {1} de daño\n".format(
                bar.name, self.v[bar].dano_rec)
        string += "\nDaño total causado : {}\n".format(self.cont_dano_c)
        string += "\nANALISIS DE ATAQUES\n\n"
        string += "Ataque mas eficiente : {0} con eficiencia {1}\n".format(
            *self.att_mas_eficiente)
        string += "Ataque mas utilizado : {0} utilizado {1} veces\n".format(
            *self.att_mas_utilizado)
        return string


class Radar:

    def __init__(self):
        self.n = 1
        self.turnos = {}

    def agregar_anuncio(self, string):
        # Permite agregar anuncio a radar (exploracion)
        # TESTEADA
        if self.n != 1:
            self.turnos[self.n - 1] += "\n\nANUNCIO: {0}\n\n".format(string)
        return self

    def format_radar(self, exito, veh, ataque, coor=[]):
        # Retorna un string estilo radar con lo que sucedio en el turno
        # NO TESTEADA
        exito = " exitoso" if exito else " no exitoso"
        coord = " - "
        for i, j in coor:
            coord += " " + abc[i] + str(j)
        coord += " - "
        v = veh.name
        att = ataque.name
        if len(coor) != 0:
            s = "Ataque " + att + " desde " + v + exito
            s += " en coordenada" + coord
            return s
        return "Ataque " + att + " desde " + v + exito

    def agregar_turno(self, string):
        # Agrega un turno al radar
        # TESTEADA
        self.turnos[self.n] = string
        self.n += 1
        return string

    def radar_n(self, n):
        # Retorna string correspondiente a un turno
        # TESTEADA
        return "\nTURNO {}\n".format(n) + self.turnos[n]

    def __str__(self):
        # Imprime el historial completo
        string = ""
        for i in range(len(self.turnos)):
            string += "\nTURNO {}\n".format(i + 1) + self.turnos[i + 1]
        return string

    def menu(self):
        # Genera el menu del radar
        # NO TESTEADA
        radar_ok = False
        while not radar_ok:
            print(""" \n

        1. Mostrar historial de turno especifico

        2. Mostrar historial completo

        3. Salir del radar """)

            opcion = f.manejo_opcion(["1", "2", "3"])
            if opcion == "1":
                if self.n == 1:
                    print("\nUsted no tiene acciones registradas en el radar")
                else:
                    l_turnos = [str(i) for i in range(1, self.n)]
                    opcion_ = f.manejo_opcion(l_turnos, string="turno")
                    print(self.radar_n(int(opcion_)))
            elif opcion == "2":
                if self.n == 1:
                    print("\nUsted no tiene acciones registradas en el radar")
                else:
                    print(self)
            elif opcion == "3":
                radar_ok = True

        return radar_ok

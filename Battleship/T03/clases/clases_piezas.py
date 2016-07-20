import clases.clases_ataques as att
import random as r


class Vehiculo:

    def __init__(self, tipo, area, res, att, n, sym):
        self.tipo = tipo
        self.area = area
        self.res = res
        self.res_hist = res
        self.att = att
        self.name = n
        self.sym = sym
        self.movible = True

    def __repr__(self):
        basic = "{0} con area {1}x{2} y simbolo {3} \n".format(
            self.name, self.area[0], self.area[1], self.sym)
        ataque = self.print_ataques()
        res = "\nResistencia {}".format(self.res)
        return basic + ataque + res

    def is_horizontal(self):
        # Bool para determinar orientacion de vehiculo
        # TESTEADA
        return True if self.area[0] < self.area[1] else False

    def is_amorfo(self):
        # Bool para determinar si vehiculo es simetrico
        # TESTEADA
        return True if self.area[0] != self.area[1] else False

    def girar(self):
        # Permite cambiar orientacion de vehiculo
        # TESTEADA
        tupla = (self.area[1], self.area[0])
        self.area = tupla
        return self.area

    def print_ataques(self):
        # Retorna string con descripcion de los ataques del vehiculo
        # NO TESTEADA
        string = "Sus ataques son:"
        for atta in self.att:
            string += "\n{}".format(atta.__repr__())
        if len(self.att) == 0:
            string += " No tiene"
        return string

    def ataques_disp(self):
        # Lista con los ataques disponibles del vehiculo
        # TESTEADA
        return [ataq for ataq in self.att if ataq.disponible]

    def estado(self):
        # Determina el estado del barco, si es que puede atacar y moverse
        # Retorna tupla con string de opciones y dic que las relaciona
        # NO TESTEADA
        string = ""
        opciones = []
        dic = {}
        cont = 1
        if len(self.ataques_disp()) != 0:
            opciones.append("Atacar")
            dic[cont] = "a"
            cont += 1
        if self.movible:
            if self.sym == "Ⓔ":
                opciones.append("Explorar")
            else:
                opciones.append("Mover")
            dic[cont] = "m"
            cont += 1
        for i in range(len(opciones)):
            string += "\n{0}. {1}".format(i + 1, opciones[i])
        string += "\n{0}. Cambiar vehiculo".format(cont)
        dic[cont] = False
        if len(opciones) == 0:
            return ("\n Este vehiculo no tiene ataques ni movimientos \n", {})
        return (string, dic)

    def estado_actual(self):
        # Representacion del estado actual del barco
        # TESTEADA
        s = self.name + " " + str(self.res) + "/" + str(self.res_hist)
        return s


class Barco(Vehiculo):

    def __init__(self):
        ataques = [
            att.MisilTrident(), att.MisilIntercontinental(), att.Paralizer()]
        super().__init__("mar", (1, 3), 30, ataques, "Barco Pequeño", "Ⓑ")


class Buque(Vehiculo):

    def __init__(self):
        ataques = [att.MisilTrident(), att.MisilTomahawk(), att.Paralizer()]
        super().__init__("mar", (2, 3), 60, ataques, "Buque de Guerra", "Ⓖ")


class Lancha(Vehiculo):

    def __init__(self):
        ataques = []
        super().__init__("mar", (1, 2), 1, ataques, "Lancha", "Ⓛ")


class Puerto(Vehiculo):

    def __init__(self):
        ataques = [att.Kit(), att.MisilTrident(), att.Paralizer()]
        super().__init__("mar", (2, 4), 80, ataques, "Puerto", "Ⓟ")
        self.movible = False


class AvionExplorador(Vehiculo):

    def __init__(self):
        ataques = [att.MisilTrident(), att.Paralizer()]
        super().__init__(
            "aire", (3, 3), float("inf"), ataques, "Avion Explorador", "Ⓔ")

    def explorar(self, coor, mapa_enemigo):
        # Explora un area
        # Retorna tupla con numero de vehiculos en area explorada 
        # y si revela coordenadas
        # NO TESTEADA
        barcos = set()
        for i, j in coor:
            enemigo = mapa_enemigo.mar.grilla[i][j]
            if enemigo is not None:
                barcos.add(enemigo)
        random = r.randint(0, 1)
        if random == 0:
            return (len(barcos), True)
        else:
            return (len(barcos), False)

    def paralizar(self):
        # Paraliza al avion explorador
        # TESTEADA
        self.movible = False
        self.turnos = 0
        return self

    def pasar_turno(self):
        # Pasa un turno en el avion explorador
        # TESTEADA
        if not self.movible:
            self.turnos += 1
            if self.turnos == 5:
                self.movible = True
        return self


class Kamikaze(Vehiculo):

    def __init__(self):
        ataques = [att.MisilTrident(), att.Kamikaze(), att.Paralizer()]
        super().__init__(
            "aire", (1, 1), float("inf"), ataques, "Kamikaze IXXI", "Ⓚ")


class AvionCaza(Vehiculo):

    def __init__(self):
        ataques = [att.MisilTrident(), att.Napalm(), att.Paralizer()]
        super().__init__(
            "aire", (1, 1), float("inf"), ataques, "Avion Caza", "Ⓒ")

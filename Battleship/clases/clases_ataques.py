from tools import funciones_aux as f


class Ataque:

    def __init__(self, area, dano, n, d="siempre"):
        self.area = area
        self.dano = dano
        self.name = n
        self.disponible = True
        self.disp = d

    def __repr__(self):
        d = self.disp if isinstance(
            self.disp, str) else "cada " + str(self.disp) + " turnos"
        tupla = (self.name, self.area[0], self.area[1], self.dano, d)
        return "{0} en area {1}x{2} con {3} de daño - DISP {4} ".format(*tupla)

    def get_coor(self):
        # Permite obtener la coordenada donde se quiere atacar
        # NO TESTEADA
        return [f.get_coor(str="del sector Mar donde desea atacar")]

    def atacar(self, siempre=True):
        # Cambia estado a no disponible si es que es alternante
        # TESTEADA
        if not siempre:
            self.disponible = False
            self.turnos = -1
        return self

    def pasar_turno(self, *args):
        # Si no esta disponible, pasa los turnos
        # TESTEADA
        if not self.disponible:
            self.turnos += 1
            if self.turnos == args[0]:
                self.disponible = True
        return self


class MisilTrident(Ataque):

    def __init__(self):
        super().__init__((1, 1), 5, "Misil UGM-133 Trident II")

    def atacar(self, vehiculo):
        # Disminuye la resistencia del vehiculo atacado
        # Retorna lista con vehiculo
        # TESTEADA
        if vehiculo:
            vehiculo.res -= self.dano
            return [vehiculo]
        else:
            return self


class MisilTomahawk(Ataque):

    def __init__(self):
        super().__init__((1, 12), 5, "Misil de Crucero BGM-109 Tomahawk", d=3)

    def get_coor(self):
        # NO TESTEADA
        return f.get_coor_tomahawk()

    def atacar(self, vehiculos):
        # Recibe lista de vehiculos en fila atacada
        # Retorna set con vehiculos atacados y res disminuidas
        # TESTEADA
        super().atacar(siempre=False)
        if vehiculos:
            veh = set(vehiculos)
            for vehiculo in veh:
                vehiculo.res -= self.dano
            return veh
        return vehiculos

    def pasar_turno(self):
        # NO LA CONTE COMO TESTEABLE PUES YA SE TESTEO EL METODO SUPER
        super().pasar_turno(self.disp)


class Napalm(Ataque):

    def __init__(self):
        super().__init__((1, 1), 5, "Napalm", d=8)
        self.vehiculo = None

    def atacar(self, vehiculo):
        # TESTEADA
        super().atacar(siempre=False)
        if vehiculo:
            vehiculo.res -= self.dano
            self.vehiculo = vehiculo
            self.cont = 0
            return [vehiculo]
        else:
            return self

    def pasar_turno(self):
        # TESTEADA
        super().pasar_turno(self.disp)
        if self.vehiculo is not None:
            self.cont += 1
            if self.cont == 2:
                self.vehiculo.res -= self.dano
                self.vehiculo = None

    def __repr__(self):
        s = super().__repr__()
        s += " - Ataca objetivo por dos turnos seguidos"
        return s


class MisilIntercontinental(Ataque):

    def __init__(self):
        super().__init__(
            (1, 1), 15, "Misil Balistico Intercontinental Minuteman III", d=3)

    def atacar(self, vehiculo):
        # NO LA CONTE COMO TESTEABLE PUES YA SE TESTEO EL METODO SUPER Y
        # TRIDENT
        super().atacar(siempre=False)
        if vehiculo:
            vehiculo.res -= self.dano
            return [vehiculo]
        else:
            return False

    def pasar_turno(self):
        # NO LA CONTE COMO TESTEABLE PUES YA SE TESTEO EL METODO SUPER
        super().pasar_turno(self.disp)


class Kamikaze(Ataque):

    def __init__(self):
        super().__init__((1, 1), float("inf"), "Kamikaze", d="una vez")

    def atacar(self, vehiculo):
        # TESTEADA
        if vehiculo:
            vehiculo.res -= self.dano
            return [vehiculo]
        else:
            return self

    def __repr__(self):
        s = super().__repr__()
        s += " - Autodestruye avion post ataque"
        return s


class Kit(Ataque):

    def __init__(self):
        self.name = "Kit de ingenierios"
        self.disponible = True

    def atacar(self, vehiculo):
        # TESTEADA
        super().atacar(siempre=False)
        vehiculo.res += 1
        return [vehiculo]

    def pasar_turno(self):
        # NO LA CONTE COMO TESTEABLE PUES YA SE TESTEO EL METODO SUPER
        super().pasar_turno(2)

    def __repr__(self):
        s = "{0} +1 en resistencia de vehiculo propio - ".format(self.name)
        s += "DISP cada 8 turnos"
        return s


class Paralizer(Ataque):

    def __init__(self):
        self.name = "GBU-43/B Massive Ordnance Air Blast Paralizer"
        self.disponible = True
        self.area = (1, 2)

    def get_coor(self):
        # NO TESTEADA
        coor = f.get_coor(str="del sector Aire donde desea atacar")
        return [coor, f.get_coor_around(coor)]

    def atacar(self, vehiculo):
        # TESTEADA
        super().atacar(siempre=False)
        if vehiculo:
            vehiculo.paralizar()
            return [vehiculo]
        else:
            return self

    def pasar_turno(self):
        # NO LA CONTE COMO TESTEABLE PUES YA SE TESTEO EL METODO SUPER
        super().pasar_turno(5)

    def __repr__(self):
        s = "{0} paraliza explorador enemigo x5 turnos - ".format(
            self.name)
        s += "DISP siempre - Debe coincidir en ambas casillas con enemigo"
        return s

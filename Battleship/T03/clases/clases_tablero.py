from string import ascii_lowercase as abc
from tools import funciones_aux as f


class Sector:

    def __init__(self, tipo, mapa):
        self.grilla = [[None for i in range(12)] for i in range(12)]
        self.tipo = tipo
        self.mapa = mapa

    def revisar_around_coor(self, coor):
        # Retorna falso si coordenadas alrededor de coor estan ocupadas
        # Usado para el explorador
        # TESTEADA
        coordenadas = []
        f = coor[0] - 1
        c = coor[1] - 1
        for i in range(3):
            for j in range(3):
                coordenadas.append((f+i, c+j))
                if f+i > 11 or f+i < 0 or c+j > 11 or c+j < 0:
                    return "Alguna parte del exp se sale de los bordes"
                if not self.is_vacia((f+i, c+j)):
                    s = "Alguna parte del exp en cas ocupada por "
                    s += self.grilla[f+i][c+j].name
                    return s
        return coordenadas

    def is_vacia(self, coor):
        # Revisa si una coordenada esta vacia
        # TESTEADA
        return True if self.grilla[coor[0]][coor[1]] is None else False

    def mover_vehiculo(self, veh, vector):
        # Mueve vehiculo en grilla en direccion del vector
        # TESTEADA
        if vector == "Izquierda":
            coor_mueve = self.get_coor_izq(self.encontrar_coordenadas(veh))
            coor_sigue = self.get_coor_der(self.encontrar_coordenadas(veh))
            mov = [(0, -1)]
        elif vector == "Derecha":
            coor_mueve = self.get_coor_der(self.encontrar_coordenadas(veh))
            coor_sigue = self.get_coor_izq(self.encontrar_coordenadas(veh))
            mov = [(0, 1)]
        elif vector == "Arriba":
            coor_mueve = self.get_coor_arriba(self.encontrar_coordenadas(veh))
            coor_sigue = self.get_coor_abajo(self.encontrar_coordenadas(veh))
            mov = [(-1, 0)]
        elif vector == "Abajo":
            coor_mueve = self.get_coor_abajo(self.encontrar_coordenadas(veh))
            coor_sigue = self.get_coor_arriba(self.encontrar_coordenadas(veh))
            mov = [(1, 0)]
        self.eliminar_vehiculo(coor_sigue)
        for i, j in coor_mueve:
            for a, b in mov:
                self.grilla[i+a][j+b] = veh
        return veh

    def mov_disp(self, vehiculo):
        # Entrega lista con movimientos disponibles del vehiculo
        # TESTEADA
        coor = self.encontrar_coordenadas(vehiculo)
        disponibles = []
        if self.se_puede_mover(self.get_coor_arriba(coor), "Arriba"):
            disponibles.append("Arriba")
        if self.se_puede_mover(self.get_coor_abajo(coor), "Abajo"):
            disponibles.append("Abajo")
        if self.se_puede_mover(self.get_coor_izq(coor), "Izquierda"):
            disponibles.append("Izquierda")
        if self.se_puede_mover(self.get_coor_der(coor), "Derecha"):
            disponibles.append("Derecha")
        return disponibles

    def se_puede_mover(self, coor, vector):
        # Dada lista de coordenadas limite, determina si se puede mover
        # en direccion del vector
        # TESTEADA
        if vector == "Izquierda":
            for i, j in coor:
                if j - 1 < 0 or self.grilla[i][j - 1] is not None:
                    return False
            return True
        elif vector == "Derecha":
            for i, j in coor:
                if j + 1 > 11 or self.grilla[i][j + 1] is not None:
                    return False
            return True
        elif vector == "Abajo":
            for i, j in coor:
                if i + 1 > 11 or self.grilla[i + 1][j] is not None:
                    return False
            return True
        elif vector == "Arriba":
            for i, j in coor:
                if i - 1 < 0 or self.grilla[i - 1][j] is not None:
                    return False
            return True

    def get_coor_arriba(self, coor):
        # Dada lista de coordenadas entrega las que se moverian hacia arriba
        # TESTEADA
        return [t for t in coor if t[0] == min(coor, key=lambda x:x[0])[0]]

    def get_coor_abajo(self, coor):
        # Dada lista de coordenadas entrega las que se moverian hacia abajo
        # TESTEADA
        return [t for t in coor if t[0] == max(coor, key=lambda x:x[0])[0]]

    def get_coor_der(self, coor):
        # Dada lista de coordenadas entrega las que se moverian hacia la der
        # TESTEADA
        return [t for t in coor if t[1] == max(coor, key=lambda x:x[1])[1]]

    def get_coor_izq(self, coor):
        # Dada lista de coordenadas entrega las que se moverian hacia la izq
        # TESTEADA
        return [t for t in coor if t[1] == min(coor, key=lambda x:x[1])[1]]

    def encontrar_coordenadas(self, vehiculo):
        # Retorna lista con tuplas estilo (i,j), coor donde esta vehiculo
        # TESTEADA
        coor = []
        for i in range(12):
            for j in range(12):
                if self.grilla[i][j] is vehiculo:
                    coor.append((i, j))
        return coor

    def eliminar_vehiculo(self, coor):
        # Elimina vehiculo de la grilla dada lista de coordenadas
        # TESTEADA
        for i, j in coor:
            self.grilla[i][j] = None
        return self.grilla

    def evaluar_ataque(self, lista_coor):
        # Retorna lista con vehiculos atacados dada lista de coordenadas
        # TESTEADA
        atacados = []
        for coor in lista_coor:
            if self.grilla[coor[0]][coor[1]] is not None:
                atacados.append(self.grilla[coor[0]][coor[1]])
        return atacados

    def posicionar_vehiculo(self, vehiculo):
        # Posiciona un vehiculo en la grilla
        # NO TESTEADA
        print("\nVEHICULO A POSICIONAR\n")
        print(vehiculo)
        print(self.mapa)
        if vehiculo.is_amorfo():
            f.def_orientacion(vehiculo, s="vehiculo")
        coor_ok = False
        while not coor_ok:
            try:
                coor = f.get_coor(str="para posicionar la cabeza del vehiculo")
                coor_ = self.check_coordenadas(coor, vehiculo)
                coor_ok = True
            except(f.CasillaOcupada, IndexError) as err:
                print(err)
        self.insertar_vehiculo(coor_, vehiculo)
        print("\nVEHICULO POSICIONADO EXITOSAMENTE")
        return vehiculo

    def insertar_vehiculo(self, coor, vehiculo):
        # Inserta el vehiculo en la coordenada correspondiente
        # NO TESTEADA
        for i in range(vehiculo.area[0]):
            for j in range(vehiculo.area[1]):
                self.grilla[coor[0] + i][coor[1] + j] = vehiculo
        return self

    def check_coordenadas(self, coor, vehiculo):
        # Revisa si un vehiculo es insertable en una coordenada
        # NO TESTEADA
        for i in range(vehiculo.area[0]):
            for j in range(vehiculo.area[1]):
                fil = coor[0] + i
                col = coor[1] + j
                if fil > 11 or col > 11:
                    s = "\nEl vehiculo paso los bordes del tablero, try again!"
                    raise IndexError(s)
                cas = self.grilla[fil][col]
                if cas is not None:
                    c = "{0}{1}".format(abc[fil], col)
                    v = cas.name
                    raise f.CasillaOcupada(c, v)
        return coor


class Mapa:

    def __init__(self):
        self.mar = Sector("mar", self)
        self.aire = Sector("aire", self)

    def get_coor_muerto(self, vehiculo):
        # Dado un vehiculo que esta muerto, lo elimina y retorna sus coor
        # NO TESTEABLE/ NO TIENE SENTIDO YA QUE ESTA COMPUESTA DE FUNCIONES YA
        # TESTEADAS
        coor = self.mar.encontrar_coordenadas(vehiculo)
        self.mar.eliminar_vehiculo(coor)
        return coor

    def get_sector(self, sec):
        # TESTEADA
        return self.aire if sec == "a" else self.mar

    def get_sector_vehiculo(self, vehiculo):
        # TESTEADA
        return self.aire if vehiculo.tipo == "aire" else self.mar

    def posicionar_vehiculo(self, vehiculo, sec):
        # Permite posicionar un vehiculo en el sector adecuado
        # NO TESTEADA
        self.get_sector(sec).posicionar_vehiculo(vehiculo)
        return vehiculo

    def __str__(self):
        string = "\n" + " " * 20 + "SECTOR MAR" + " " * 45 + "SECTOR AIRE\n"
        string += (" " * 3 + "-" * 49 + " " * 3) * 2 + "\n"
        string += "   | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10| 11|   " * 2
        string += "\n"
        string += ("-" * 52 + " " * 3) * 2 + "\n"

        for i in range(12):
            fila = " {} |".format(abc[i])
            for e in self.mar.grilla[i]:
                if e is None:
                    valor = " "
                else:
                    valor = e.sym
                fila += " {} |".format(valor)
            fila += " " * 3 + " {} |".format(abc[i])
            for e in self.aire.grilla[i]:
                if e is None:
                    valor = " "
                else:
                    valor = e.sym
                fila += " {} |".format(valor)

            string += fila + "\n" + ("-" * 52 + " " * 3) * 2 + "\n"

        return string

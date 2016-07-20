import unittest
import random as r
from clases.clases_tablero import Sector, Mapa
from clases.clases_piezas import Barco, Lancha, AvionExplorador

# 14/18 funciones testeadas del modulo clases_tablero


class TestMapa(unittest.TestCase):

    def setUp(self):
        self.m = Mapa()

    def test_get_sector(self):
        sector = self.m.get_sector("a")
        assert sector is self.m.aire
        sector = self.m.get_sector("m")
        assert sector is self.m.mar

    def test_get_sector_vehiculo(self):
        sector = self.m.aire
        assert self.m.get_sector_vehiculo(AvionExplorador()) is sector
        sector = self.m.mar
        assert self.m.get_sector_vehiculo(Barco()) is sector


class TestSector(unittest.TestCase):

    def setUp(self):
        self.v = Barco()
        self.v1 = Lancha()
        self.m = Mapa()
        self.s = Sector("mar", self.m)
        self.coor = [(1, 2), (2, 2), (3, 2)]
        self.coor1 = [(1, 2), (1, 3), (1, 4)]
        self.coor2 = [(5, 5)]
        self.coor3 = [(1, 2), (1, 3), (2, 2), (2, 3)]

    def test_revisar_around_coor(self):
        lista = [(1,4),(1,5),(1,6),(2,4),(2,5),(2,6),(3,4),(3,5),(3,6)]
        assert self.s.revisar_around_coor((2,5)) == lista
        self.s.grilla[2][3] = Barco()
        assert self.s.revisar_around_coor((2,5)) == lista
        self.s.grilla[2][4] = Barco()
        string = "Alguna parte del exp en cas ocupada por Barco Pequeño"
        string1 = "Alguna parte del exp se sale de los bordes"
        assert self.s.revisar_around_coor((2,5)) == string
        assert self.s.revisar_around_coor((0,1)) == string1
        assert self.s.revisar_around_coor((1,0)) == string1
        assert self.s.revisar_around_coor((11,11)) == string1
        assert self.s.revisar_around_coor((7,11)) == string1
        assert self.s.revisar_around_coor((11,5)) == string1


    def test_is_vacia(self):
        assert self.s.is_vacia((2,4))
        self.s.grilla[2][4] = Barco()
        assert not self.s.is_vacia((2,4))

    def test_mover_vehiculo_simple(self):
        self.s.grilla[5][5] = self.v
        self.s.mover_vehiculo(self.v,"Arriba")
        assert self.s.grilla[5][5] == None
        assert self.s.grilla[4][5] == self.v
        self.s.mover_vehiculo(self.v,"Abajo")
        assert self.s.grilla[5][5] == self.v
        assert self.s.grilla[4][5] == None
        self.s.mover_vehiculo(self.v,"Derecha")
        assert self.s.grilla[5][6] == self.v
        assert self.s.grilla[5][5] == None
        self.s.mover_vehiculo(self.v,"Izquierda")
        assert self.s.grilla[5][5] == self.v
        assert self.s.grilla[5][6] == None

    def test_mover_vehiculo_complejo(self):
        for i in range(3):
            self.s.grilla[i+1][1] = self.v
            self.s.grilla[i+1][2] = self.v
        self.s.mover_vehiculo(self.v,"Arriba")
        for i in range(3):
            assert self.s.grilla[i][1] == self.v
            assert self.s.grilla[i][2] == self.v
        assert self.s.grilla[3][1] == None
        assert self.s.grilla[3][2] == None
        self.s.mover_vehiculo(self.v,"Abajo")
        for i in range(3):
            assert self.s.grilla[i+1][1] == self.v
            assert self.s.grilla[i+1][2] == self.v
        assert self.s.grilla[0][1] == None
        assert self.s.grilla[0][2] == None
        self.s.mover_vehiculo(self.v,"Derecha")
        for i in range(3):
            assert self.s.grilla[i+1][2] == self.v
            assert self.s.grilla[i+1][3] == self.v
            assert self.s.grilla[i+1][1] == None
        self.s.mover_vehiculo(self.v,"Izquierda")
        for i in range(3):
            assert self.s.grilla[i+1][1] == self.v
            assert self.s.grilla[i+1][2] == self.v
            assert self.s.grilla[i+1][3] == None


    def test_mov_disp(self):
        self.s.grilla[5][5] = self.v
        assert self.s.mov_disp(self.v) == ["Arriba","Abajo","Izquierda","Derecha"]
        self.s.grilla[11][1] = self.v1
        assert self.s.mov_disp(self.v1) == ["Arriba","Izquierda","Derecha"]
        self.s.grilla[5][6] = self.v1
        assert self.s.mov_disp(self.v) == ["Arriba","Abajo","Izquierda"]
        self.s.grilla[6][5] = self.v1
        assert self.s.mov_disp(self.v) == ["Arriba","Izquierda"]
        self.s.grilla[4][5] = self.v1
        assert self.s.mov_disp(self.v) == ["Izquierda"]
        self.s.grilla[5][4] = self.v1
        assert not self.s.mov_disp(self.v)

    def test_se_puede_mover(self):
        assert self.s.se_puede_mover(self.coor1, "Arriba")
        self.s.grilla[0][3] = Barco()
        assert not self.s.se_puede_mover(self.coor1, "Arriba")
        assert not self.s.se_puede_mover([(0, 3), (0, 4)], "Arriba")
        assert self.s.se_puede_mover(self.coor2, "Izquierda")
        assert not self.s.se_puede_mover([(0, 4)], "Izquierda")
        assert not self.s.se_puede_mover([(2, 0), (1, 0)], "Izquierda")
        assert not self.s.se_puede_mover([(2, 11)], "Derecha")
        assert self.s.se_puede_mover([(0, 4)], "Derecha")
        self.s.grilla[3][5] = Barco()
        self.s.grilla[3][7] = Barco()
        self.s.grilla[4][6] = Barco()
        self.s.grilla[2][6] = Barco()
        assert not self.s.se_puede_mover([(3, 6)], "Derecha")
        assert not self.s.se_puede_mover([(3, 6)], "Izquierda")
        assert not self.s.se_puede_mover([(3, 6)], "Abajo")
        assert not self.s.se_puede_mover([(3, 6)], "Arriba")
        self.s.grilla[4][6] = None
        assert self.s.se_puede_mover([(3, 6)], "Abajo")

    def test_get_coor_der(self):
        assert self.s.get_coor_der(self.coor) == self.coor
        assert self.s.get_coor_der(self.coor1) == [(1, 4)]
        assert self.s.get_coor_der(self.coor2) == self.coor2
        assert self.s.get_coor_der(self.coor3) == [(1, 3), (2, 3)]

    def test_get_coor_abajo(self):
        assert self.s.get_coor_abajo(self.coor) == [(3, 2)]
        assert self.s.get_coor_abajo(self.coor1) == self.coor1
        assert self.s.get_coor_abajo(self.coor2) == self.coor2
        assert self.s.get_coor_abajo(self.coor3) == [(2, 2), (2, 3)]

    def test_get_coor_arriba(self):
        assert self.s.get_coor_arriba(self.coor) == [(1, 2)]
        assert self.s.get_coor_arriba(self.coor1) == self.coor1
        assert self.s.get_coor_arriba(self.coor2) == self.coor2
        assert self.s.get_coor_arriba(self.coor3) == [(1, 2), (1, 3)]

    def test_get_coor_izq(self):
        assert self.s.get_coor_izq(self.coor) == self.coor
        assert self.s.get_coor_izq(self.coor1) == [(1, 2)]
        assert self.s.get_coor_izq(self.coor2) == self.coor2
        assert self.s.get_coor_izq(self.coor3) == [(1, 2), (2, 2)]

    def test_encontrar_coordenadas(self):
        lista = set()
        assert not self.s.encontrar_coordenadas(self.v)
        for i in range(20):
            a = r.randint(0, 11)
            b = r.randint(0, 11)
            lista.add((a, b))
            self.s.grilla[a][b] = self.v
        assert set(self.s.encontrar_coordenadas(self.v)) == lista

    def test_eliminar_vehiculo(self):
        lista = set()
        grilla = [[None for i in range(12)] for i in range(12)]
        self.s.eliminar_vehiculo([])
        assert grilla == self.s.grilla
        for i in range(20):
            a = r.randint(0, 11)
            b = r.randint(0, 11)
            lista.add((a, b))
            self.s.grilla[a][b] = self.v
        assert not grilla == self.s.grilla
        self.s.eliminar_vehiculo(list(lista))
        assert grilla == self.s.grilla

    def test_evaluar_ataque(self):
        assert not self.s.evaluar_ataque([])
        assert not self.s.evaluar_ataque([(1, 3), (5, 3), (2, 3)])
        lista = [(i, i + 1) for i in range(9)]
        lista1 = [(i + 2, i) for i in range(5)]
        for i, j in lista:
            self.s.grilla[i][j] = self.v
        for i, j in lista1:
            self.s.grilla[i][j] = self.v1
        assert self.s.evaluar_ataque([lista[0]]) == [self.v]
        lista_aux = [lista[1], lista1[4], (11, 11)]
        assert self.s.evaluar_ataque(lista_aux) == [self.v, self.v1]

import unittest
import clases.clases_piezas as c

# 7/10 funciones testeadas del modulo clases_piezas

class TestAvionExplorador(unittest.TestCase):

    def setUp(self):
        self.a = c.AvionExplorador()

    def test_paralizar(self):
        self.a.paralizar()
        assert not self.a.movible

    def test_pasar_turno(self):
        self.a.paralizar()
        for i in range(4):
            self.a.pasar_turno()
        assert not self.a.movible
        self.a.pasar_turno()
        assert self.a.movible

class TestVehiculoSuper(unittest.TestCase):

    def setUp(self):
        self.v = c.Barco()

    def test_is_horizontal(self):
        self.v.area = (10, 1)
        assert not self.v.is_horizontal()
        self.v.area = (1, 10)
        assert self.v.is_horizontal()
        self.v.area = (1, 1)
        assert not self.v.is_horizontal()

    def test_is_amorfo(self):
        self.v.area = (1, 1)
        assert not self.v.is_amorfo()
        self.v.area = (6, 7)
        assert self.v.is_amorfo()

    def test_girar(self):
        self.v.area = (1, 1)
        assert self.v.girar() == (1, 1)
        self.v.area = (1, 2)
        assert self.v.girar() == (2, 1)
        self.v.area = (2, 1)
        assert self.v.girar() == (1, 2)

    def test_ataques_disp(self):
        self.v.att = []
        assert not self.v.ataques_disp()

    def test_ataques_disp1(self):
        assert self.v.ataques_disp() == self.v.att

    def test_ataques_disp2(self):
        self.v.att[0].disponible = False
        assert self.v.ataques_disp() == [self.v.att[1], self.v.att[2]]

    def test_estado_actual(self):
        assert self.v.estado_actual() == "Barco Pequeño 30/30"
        self.v.res = 20
        assert self.v.estado_actual() == "Barco Pequeño 20/30"

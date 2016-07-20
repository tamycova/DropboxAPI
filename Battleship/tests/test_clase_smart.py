import unittest
from clases.clase_smart import Maquina
from string import ascii_lowercase as abc


# 2/9 funciones testeadas del modulo clase_smart


class TestMaquina(unittest.TestCase):
    def setUp(self):
        self.m = Maquina("1",None)

    def test_get_random_coor(self):
        for i in range (1000):
            c = self.m.get_random_coor()
            assert c[0] >= 0
            assert c[0] <= 11
            assert c[1] >= 0
            assert c[1] <= 11

    def test_understand_anuncio(self):
        lista = [(1, 2),(3, 5),(4, 6),(11, 11)]
        s1 = "En turno enemigo ud fue explorado en "
        s1 += " ".join([abc[i[0]]+str(i[1]) for i in lista])
        self.m.anuncio = s1
        for e in self.m.understand_anuncio():
            assert e in lista
        assert len(lista) == len(self.m.understand_anuncio())



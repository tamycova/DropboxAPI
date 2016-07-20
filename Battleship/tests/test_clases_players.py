import unittest
from clases.clase_juego import Juego
from clases.clases_piezas import Lancha, Puerto

# 4/18 funciones testeadas del modulo clases_players


class TestJugador(unittest.TestCase):

    def setUp(self):
        self.juego = Juego()
        self.p = self.juego.players[0]

    def test_vehiculos(self):
        self.p.vehiculos_mar = [1, 2, 3]
        self.p.vehiculos_aire = [4, 5]
        assert self.p.vehiculos == [4, 5, 1, 2, 3]

    def test_is_dead(self):
        for p in self.juego.players:
            assert not p.is_dead()
        self.p.vehiculos_mar = [Lancha(), Puerto()]
        assert not self.p.is_dead()
        self.p.vehiculos_mar = []
        assert self.p.is_dead()
        self.p.vehiculos_mar = [Lancha()]
        assert self.p.is_dead()

    def test_eliminar_vehiculo(self):
        assert len(self.p.vehiculos_mar) == 4
        barco = [
            v for v in self.p.vehiculos_mar if v.name == "Barco Pequeño"][0]
        assert barco in self.p.vehiculos_mar
        self.p.eliminar_vehiculo(barco)
        assert barco not in self.p.vehiculos_mar
        assert len(self.p.vehiculos_mar) == 3

    def test_get_explorador(self):
        assert self.p.get_explorador() is self.p.vehiculos_aire[0]

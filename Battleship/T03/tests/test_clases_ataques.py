import unittest
import clases.clases_ataques as c
from clases.clases_piezas import Puerto, Barco, AvionExplorador

# 9/12 funciones testeadas del modulo clases_ataques


class TestClasesAtaquesSub(unittest.TestCase):

    def setUp(self):
        self.trident = c.MisilTrident()
        self.tomahawk = c.MisilTomahawk()
        self.napalm = c.Napalm()
        self.kmkz = c.Kamikaze()
        self.vehiculo = Puerto()
        self.vehiculos = [self.vehiculo, self.vehiculo, self.vehiculo, Barco()]

    def test_atacar_trident(self):
        atacado = self.trident.atacar(self.vehiculo)
        assert self.vehiculo.res == 75
        assert isinstance(atacado, list)

    def test_atacar_tomahawk(self):
        atacados = self.tomahawk.atacar(self.vehiculos)
        assert len(atacados) == 2
        assert isinstance(atacados, set)
        for v in atacados:
            assert v.res in [75, 25]
        self.vehiculos = []
        atacados = self.tomahawk.atacar(self.vehiculos)
        assert atacados is self.vehiculos

    def test_atacar_napalm(self):
        assert self.napalm.vehiculo is None
        self.napalm.atacar(self.vehiculo)
        assert self.vehiculo.res == 75
        assert self.napalm.vehiculo is self.vehiculo

    def test_pasar_turno_napalm(self):
        self.napalm.atacar(self.vehiculo)
        self.napalm.pasar_turno()
        assert self.vehiculo.res == 75
        self.napalm.pasar_turno()
        assert self.vehiculo.res == 70
        self.napalm.pasar_turno()
        assert self.vehiculo.res == 70

    def test_atacar_kmkz(self):
        self.kmkz.atacar(self.vehiculo)
        assert self.vehiculo.res < 0

    def test_kit(self):
        kit = c.Kit()
        kit.atacar(self.vehiculo)
        assert self.vehiculo.res == 81

    def test_paralizar(self):
        par = c.Paralizer()
        avion = AvionExplorador()
        par.atacar(avion)
        assert not avion.movible


class TestClasesAtaquesSuper(unittest.TestCase):

    def setUp(self):
        self.ataque = c.Ataque((1, 1), 100, "ataque")

    def test_atacar_super_siempre(self):
        a = self.ataque.atacar()
        assert a.disponible

    def test_atacar_super_nosiempre(self):
        a = self.ataque.atacar(siempre=False)
        assert not a.disponible

    def test_pasar_turno_super(self):
        # ataca con ataque que se puede usar cada 3 turnos
        a = self.ataque.atacar(siempre=False)
        a.pasar_turno(3)
        # pasa el turno
        assert a.turnos == 0
        assert not a.disponible
        # entra al turno 1 desde ataque con 0 turnos y att no disponible
        a.pasar_turno(3)
        # pasa el turno
        assert a.turnos == 1
        assert not a.disponible
        # entra al turno 2 desde ataque con 1 turnos y att no disponible
        a.pasar_turno(3)
        # pasa el turno
        assert a.turnos == 2
        assert not a.disponible
        # entra al turno 3 desde ataque con 2 turnos y att no disponible
        a.pasar_turno(3)
        # pasa el turno
        assert a.turnos == 3
        assert a.disponible
        # entra al turno 4 desde ataque con 3 turnos y att disponible
        a.pasar_turno(3)
        # pasa el turno
        assert a.turnos == 3
        assert a.disponible
        # el contador ya no avanza al pasar turnos, y ataque sigue disponible
        a.atacar(siempre=False)
        # si ataca, turno vuelve a quedar no disponible
        assert a.turnos == -1
        assert not a.disponible

import unittest
from clases.clases_data import Radar, Estadistica
from clases.clases_players import Jugador
from clases.clases_ataques import MisilTrident, MisilIntercontinental

# 9/12 funciones testeadas del modulo clases_data


class TestRadar(unittest.TestCase):

    def setUp(self):
        self.r = Radar()

    def test_agregar_anuncio(self):
        self.r.agregar_turno("soy un turno")
        self.r.agregar_turno("soy otro turno")
        assert len(self.r.turnos) == 2
        assert self.r.turnos[2] == "soy otro turno"
        self.r.agregar_anuncio("1")
        assert len(self.r.turnos) == 2
        assert self.r.turnos[2] == "soy otro turno\n\nANUNCIO: 1\n\n"

    def test_agregar_turno(self):
        assert len(self.r.turnos) == 0
        assert self.r.n == 1
        self.r.agregar_turno("soy un turno")
        assert len(self.r.turnos) == 1
        assert self.r.turnos[1] == "soy un turno"
        self.r.agregar_turno("soy otro turno")
        assert len(self.r.turnos) == 2
        assert self.r.turnos[2] == "soy otro turno"

    def test_radar_n(self):
        self.r.agregar_turno("soy un turno")
        self.r.agregar_turno("soy otro turno")
        s = "\nTURNO 2\nsoy otro turno"
        assert s == self.r.radar_n(2)


class TestEstadistica(unittest.TestCase):

    def setUp(self):
        self.p = Jugador("1", None)
        self.barco = self.p.vehiculos_mar[0]
        self.barco1 = self.p.vehiculos_mar[1]
        self.e = Estadistica(self.p)
        self.name_att = MisilTrident().name
        self.name_att1 = MisilIntercontinental().name

    def test_mover(self):
        self.e.mover(self.barco)
        self.e.mover(self.barco)
        self.e.mover(self.barco)
        self.e.mover(self.barco1)
        assert self.e.cont_turnos == 4
        assert self.e.v[self.barco].mov == 3

    def test_atacar(self):
        self.e.atacar(self.barco1, self.name_att, 1, 10)
        self.e.atacar(self.barco1, self.name_att, 1, 20)
        self.e.atacar(self.barco1, self.name_att, 0, 5)
        self.e.atacar(self.barco1, self.name_att, 0, 3)
        self.e.atacar(self.barco, self.name_att1, 0, 100)
        self.e.atacar(self.barco, self.name_att1, 1, 6)
        assert self.e.cont_turnos == 6
        assert self.e.cont_ataques == 6
        assert self.e.a[self.name_att].n_usado == 4
        assert self.e.a[self.name_att1].n_usado == 2
        assert self.e.v[self.barco].att == 2
        assert self.e.v[self.barco1].att == 4
        assert self.e.cont_dano_c == 108
        assert self.e.a[self.name_att].d_causado == 8
        assert self.e.a[self.name_att1].d_causado == 100
        assert self.e.cont_ataques_ex == 3
        assert self.e.v[self.barco].att_ex == 1
        assert self.e.v[self.barco1].att_ex == 2

    def test_recibir_dano(self):
        self.e.recibir_dano(self.barco, 10)
        self.e.recibir_dano(self.barco, 20)
        assert self.e.cont_dano_r == 30
        assert self.e.v[self.barco1].dano_rec == 0
        assert self.e.v[self.barco].dano_rec == 30

    def test_porcentaje_exitosos(self):
        assert self.e.porcentaje_exitosos == 0
        for i in range(60):
            self.e.atacar(self.barco, self.name_att, 1, 10)
        for i in range(40):
            self.e.atacar(self.barco1, self.name_att, 0, 10)
        assert self.e.porcentaje_exitosos == 40

    def test_att_mas_utilizado(self):
        for i in range(41):
            self.e.atacar(self.barco, self.name_att1, 1, 10)
        for i in range(40):
            self.e.atacar(self.barco1, self.name_att, 0, 10)
        assert self.e.att_mas_utilizado == (self.name_att1, 41)
        for i in range(5):
            self.e.atacar(self.barco1, self.name_att, 0, 10)
        assert self.e.att_mas_utilizado == (self.name_att, 45)

    def test_barco_mas_movido(self):
        for i in range(39):
            self.e.mover(self.barco)
        for i in range(41):
            self.e.mover(self.barco1)
        assert self.e.barco_mas_movido == (self.barco1.name, 41)

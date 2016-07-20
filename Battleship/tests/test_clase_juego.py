import unittest
import clases.clase_juego as c

# 3/6 funciones testeadas del modulo clase_juego


class TestClaseJuego(unittest.TestCase):

    def setUp(self):
        self.juego = c.Juego()
        self.juego_ = c.Juego(maquina=True)
        self.lista_players = [c.Jugador("1", "0"), c.Jugador("2", "0")]

    def test_sorteo(self):
        empieza = self.juego.sorteo()
        empieza_ = self.juego_.sorteo()
        self.assertIn(empieza, self.juego.players)
        self.assertIn(empieza_, self.juego_.players)

    def test_aleatoriedad_sorteo(self):
        empiezan = {self.juego.sorteo() for i in range(1000)}
        self.assertEqual(len(empiezan), 2)

    def test_el_otro(self):
        self.juego.players = self.lista_players
        otro = self.juego.el_otro(self.lista_players[0])
        otro1 = self.juego.el_otro(self.lista_players[1])
        self.assertEqual(otro, self.lista_players[1])
        self.assertEqual(otro1, self.lista_players[0])

    def test_get_winner(self):
        self.juego.players[1].vehiculos_mar = []
        self.assertEqual(self.juego.get_winner(), self.juego.players[0])

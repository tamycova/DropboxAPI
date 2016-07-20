import random
from clases.clases_players import Jugador
from clases.clase_smart import Maquina


class Juego:

    def __init__(self, maquina=False):
        if not maquina:
            self.players = (Jugador("1", self), Jugador("2", self))
        else:
            self.players = (Jugador("1", self), Maquina("2 (M)", self))

    def sorteo(self):
        # Realiza el sorteo para ver quien comienza y retorna el jugador
        # TESTEADA
        empieza = random.choice(self.players)
        return empieza

    def el_otro(self, p):
        # Retorna un jugador dado el otro
        # TESTEADA
        return self.players[1] if self.players[0] is p else self.players[0]

    def posicionar_vehiculos(self):
        # Posicionamiento de vehiculos para los jugadores
        # NO TESTEADA
        for p in self.players:
            p.posicionar_vehiculos()
        return "Vehiculos posicionados exitosamente."

    def turno(self, p):
        # Genera un turno completo del juego, de los dos jugadores
        # NO TESTEADA
        p.turno()
        if not self.el_otro(p).is_dead():
            self.el_otro(p).turno()
        return p

    def get_winner(self):
        # Retorna el ganador del juego
        # TESTEADA
        win = self.players[0] if self.players[1].is_dead() else self.players[1]
        return win

    def run(self, p):
        # Inicia el juego una vez posicionados los vehiculos
        # Recibe el jugador que empieza el juego, retorna el ganador
        # NO TESTEADA
        while not self.players[0].is_dead() and not self.players[1].is_dead():
            self.turno(p)
        for p in self.players:
            print(p.stats)
        return self.get_winner()

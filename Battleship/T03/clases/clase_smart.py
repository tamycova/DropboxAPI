from clases.clases_players import Jugador
import random as r
from string import ascii_lowercase as abc


class Maquina(Jugador):

    def __init__(self, id, juego):
        super().__init__(id, juego)
        self.exploradas = []  # lista que almacena coor exploradas
        self.por_atacar = []  # stack que almacena coor por atacar
        self.atacando = None  # casilla actualmente atacada
        self.dano_atacando = 0  # dano en casilla actualmente atacada
        self.kmkz = False  # para saber si usara el kmkz

    def get_ataque_optimo(self):
        # Dada las preferencias de la estrategia, retorna el ataque y
        # el vehiculo que se deben usar para atacar
        # NO TESTEADA
        # print("BUSCANDO ATAQUE OPTIMO") # para revisar!
        m = "Misil Balistico Intercontinental Minuteman III"
        b = [v for v in self.vehiculos_mar if v.sym == "Ⓑ"]
        c = [v for v in self.vehiculos_aire if v.sym == "Ⓒ"][0]
        if self.kmkz:
            # print("KMKZ") # para revisar!
            k = [v for v in self.vehiculos_aire if v.sym == "Ⓚ"][0]
            kmkz = k.att[1]
            return(k, kmkz)
        elif b and [a for a in b[0].ataques_disp() if a.name == m]:
            # print("MINUTEMAN") # para revisar!
            minuteman = [a for a in b[0].ataques_disp() if a.name == m][0]
            return (b[0], minuteman)
        elif [a for a in c.ataques_disp() if a.name == "Napalm"]:
            # print("NAPALM") # para revisar!
            napalm = [a for a in c.ataques_disp() if a.name == "Napalm"][0]
            return (c, napalm)
        else:
            # print("TRIDENT") # para revisar!
            d = c.ataques_disp()
            trident = [a for a in d if a.name == "Misil UGM-133 Trident II"][0]
            return (c, trident)

    def get_random_coor(self):
        # Retorna coordenadas validas random
        # TESTEADA
        num = [i for i in range(12)]
        return (r.choice(num), r.choice(num))

    def get_unexplored_coords(self):
        # Retorna una coordenada inexplorada
        # NO TESTEADA
        coor_ok = False
        while not coor_ok:
            coor = self.get_random_coor()  # recibo coor aleatoria
            res = self.mapa.aire.revisar_around_coor(
                coor)  # reviso si puedo exp
            if isinstance(res, list):  # si puedo explorarla
                estan = [c for c in res if c in self.exploradas]
                if len(estan) == 0:  # exploro ese cuadrado pq no lo he hecho
                    coor_ok = True
                    self.exploradas.extend(res)  # agrego a exploradas
                    return res

    def posicionar_vehiculos(self):
        # Posiciona vehiculos aleatoriamente, es lo mas inteligente
        # en el caso de jugar repetidamente contra un jugador
        # NO TESTEADA
        num = [i for i in range(12)]
        mapa = [(self.vehiculos_mar, self.mapa.mar),
                (self.vehiculos_aire, self.mapa.aire)]
        for s in mapa:
            for v in s[0]:
                a = r.randint(0, 1)
                if a == 0:
                    v.girar()
                coor_ok = False
                while not coor_ok:
                    try:
                        coor = (r.choice(num), r.choice(num))
                        coor_ = s[1].check_coordenadas(coor, v)
                        coor_ok = True
                    except:
                        pass
                s[1].insertar_vehiculo(coor_, v)
        return self.mapa

    def explorar(self, exp):
        # Explora maquina style (todo sigue muy fair para el otro jugador)
        # NO TESTEADA
        res = self.get_unexplored_coords()
        self.mapa.aire.eliminar_vehiculo(
            self.mapa.aire.encontrar_coordenadas(exp))
        for i, j in res:
            self.mapa.aire.grilla[i][j] = exp
        exploracion = exp.explorar(res, self.juego.el_otro(self).mapa)
        self.stats.mover(exp)  # actualizo mis stats

        if exploracion[1]:
            # revelo mi posicion al jugador humano
            s1 = "En turno enemigo ud fue explorado en "
            s1 += " ".join([abc[i[0]] + str(i[1]) for i in res])
            self.juego.el_otro(self).radar.agregar_anuncio(s1)
            self.juego.el_otro(self).anuncio = s1

        # PARA REVISAR
        # s1 = "En turno enemigo ud fue explorado en "
        # s1 += " ".join([abc[i[0]]+str(i[1]) for i in res])
        # self.juego.el_otro(self).radar.agregar_anuncio(s1)
        # self.juego.el_otro(self).anuncio = s1

        return (exploracion[0], res)

    def understand_anuncio(self):
        # Retorna lista de coordenadas en que fui explorada, para paralizar
        # TESTEADA
        dic_board = dict(zip(abc[:12], [i for i in range(15)]))
        a = [(dic_board[i[0]], int(i[1:])) for i in self.anuncio.split()[7:]]
        return a

    def paralizar(self, c1, c2):
        # Paraliza
        # NO TESTEADA
        # la maquina no fallara en su eleccion de coordenadas,
        # aun asi para q sea justo chequeo
        coor = [c1, c2]
        vehiculo = [v for v in self.vehiculos_aire if v.sym == "Ⓒ"][0]
        ataque = vehiculo.att[2]
        atacados = self.juego.el_otro(self).mapa.aire.evaluar_ataque(coor)
        n = len(atacados)
        if n == 2 and atacados[0] is atacados[1] and atacados[0].movible:
            ataque.atacar(atacados[0])
            self.stats.atacar(vehiculo, ataque.name, 0, 0)
        return True

    def atacar(self, coor):
        # Recibe la coordenada donde atacara y luego hace la magia
        # NO TESTEADA
        # print("ATACANDO") # para revisar
        # print(abc[coor[0][0]]+str(coor[0][1])) # para revisar
        accion = self.get_ataque_optimo()  # obtengo ataque optimo
        vehiculo = accion[0]  # vehiculo que atacara
        ataque = accion[1]  # el ataque (minuteman, napalm,trident o kmkz)
        atacados = self.juego.el_otro(self).mapa.mar.evaluar_ataque(coor)
        if vehiculo.name == "Kamikaze IXXI":
            d = atacados[0].res_hist
        else:
            d = ataque.dano
        if len(atacados) == 0:  # se movio
            self.atacando = None  # dejo de atacar esa casilla
            self.dano_atacando = 0  # vuelvo el dano de casilla a 0
            ataque.atacar(False)
            self.stats.atacar(vehiculo, ataque.name, 1, d)
        else:  # si ataque
            muertos = self.juego.el_otro(self).actualizar_vehiculo(
                ataque.atacar(atacados[0]))
            self.stats.atacar(vehiculo, ataque.name, 0, d)
            self.juego.el_otro(self).stats.recibir_dano(atacados[0], d)
            self.dano_atacando += d  # sumo el dano a esa casilla
            if self.dano_atacando >= 30 and not muertos:
                if self.kmkz is not None:
                    # uso el kmkz porque es puerto o buque de guerra
                    self.kmkz = True
                # para optimizar ataque en prox turno
            if muertos:  # si mate el barco
                self.atacando = None  # para que no ataque de nuevo
                self.dano_atacando = 0  # vuelvo el dano de casilla a 0
            if vehiculo.name == "Kamikaze IXXI":
                self.vehiculos_aire.remove(vehiculo)
                self.mapa.get_coor_muerto(vehiculo)
                self.kmkz = None
        return self

    def turno(self):
        # Un turno mega inteligente de maquina (cada if es una opcion de turno)
        # NO TESTEADA

        # PRIMERO REVISO SI EN EL TURNO ANTERIOR FUI EXPLORADA, Y PARALIZO
        if self.anuncio != "":
            coords = self.understand_anuncio()
            # paralizo atacando esas dos coordenadas
            self.paralizar(coords[0], coords[1])
            # print("PARALIZE") # para revisar!
            self.anuncio = ""

        # LUEGO REVISO SI ES QUE TENGO UNA CASILLA DONDE SE QUE HAY BARCO
        elif self.atacando is not None:
            self.atacar([self.atacando])

        # DADO QUE DEJE DE REVISAR UNA CASILLA, VOY POR LA PROXIMA QUE HE
        # EXPLORADO
        elif len(self.por_atacar) != 0:
            self.atacando = self.por_atacar.pop()
            self.atacar([self.atacando])

        # SI NO TENGO MAS COORDENADAS POR ATACAR O ATACANDO, EXPLORO
        elif self.get_explorador().movible:
            # print("EXPLORE") # para revisar!
            exp = self.explorar(self.get_explorador())
            if exp[0] != 0:  # encontro un vehiculo
                # agrego todas las cordenadas a un stack
                self.por_atacar.extend(exp[1])

        # SI NO TENGO MAS PARA ATACAR Y NO PUEDO EXPLORAR, ATACO RANDOM
        else:
            # print("ATAQUE RANDOM") para revisar!
            # ataca y si encuentra algo sigue atacando
            self.atacando = self.get_random_coor()
            self.atacar([self.atacando])

        self.get_explorador().pasar_turno()
        self.turno_en_ataques()
        return False

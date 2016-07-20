import sys
from string import ascii_lowercase as abc
from tools import funciones_aux as f
from clases.clases_data import Estadistica, Radar
from clases.clases_piezas import (
    Barco, Buque, Lancha, Puerto, AvionExplorador, AvionCaza, Kamikaze)
from clases.clases_tablero import Mapa


class Jugador:

    def __init__(self, id, juego):
        self.id = id
        self.mapa = Mapa()
        self.radar = Radar()
        self.vehiculos_mar = [Barco(), Buque(), Lancha(), Puerto()]
        self.vehiculos_aire = [AvionExplorador(), AvionCaza(), Kamikaze()]
        self.stats = Estadistica(self)
        self.juego = juego
        self.anuncio = ""

    @property
    def vehiculos(self):
        # Retorna la lista de todos los vehiculos (aire y mar)
        # TESTEADA
        return self.vehiculos_aire + self.vehiculos_mar

    def turno_en_ataques(self):
        # Actualiza el paso de turno para restricciones de ataques
        # NO TESTEADA
        for v in self.vehiculos:
            for a in v.att:
                a.pasar_turno()
        return self

    def get_explorador(self):
        # Retorna el explorador, para pasarle su turno
        # TESTEADA
        return [e for e in self.vehiculos_aire if e.sym == "Ⓔ"][0]

    def is_dead(self):
        # Determina si un jugador perdio
        # TESTEADA
        quedan = [v for v in self.vehiculos_mar if v.name != "Lancha"]
        return True if len(quedan) == 0 else False

    def posicionar_vehiculos(self):
        # Permite posicionar los vehiculos en el mapa
        # NO TESTEADA
        print("\nINGRESAR VEHICULOS PARA JUGADOR {} ".format(self.id))
        print("\nSECTOR MAR")
        for vehiculo in self.vehiculos_mar:
            self.mapa.posicionar_vehiculo(vehiculo, "m")
        print("\n\n ASIGNACION DE SECTOR MAR FINALIZADA \n\n")
        print("\nSECTOR AIRE")
        for vehiculo in self.vehiculos_aire:
            self.mapa.posicionar_vehiculo(vehiculo, "a")
        print("\n\n ASIGNACION DE SECTOR AIRE FINALIZADA \n\n")
        print(self.mapa)
        print("\n" * 42)  # SACAR ESPACIOS
        return self.mapa

    def eliminar_vehiculo(self, vehiculo):
        # Elimina vehiculo marino
        # TESTEADA
        return self.vehiculos_mar.remove(vehiculo)

    def menu_ataque(self, vehiculo):
        # Menu ataques disponibles
        # NO TESTEADA
        in_menu_ataque = True
        while in_menu_ataque:
            ataque = f.get_opciones(
                "ATAQUES", vehiculo.ataques_disp(), "__repr__")
            if not ataque:
                return True
            else:
                in_menu_ataque = self.atacar_con_vehiculo(ataque, vehiculo)

    def menu_vehiculo(self, vehiculo):
        # Menu una vez que el vehiculo fue seleccionado
        # NO TESTEADA
        in_menu_vehiculo = True
        while in_menu_vehiculo:
            estado_vehiculo = vehiculo.estado()
            print(estado_vehiculo[0])
            n = len(estado_vehiculo[1])
            if n == 0:
                print("Vehiculo no tiene movimientos o ataques en este turno.")
                return True
            else:
                opcion = f.manejo_opcion([str(i + 1) for i in range(n)])
                accion = estado_vehiculo[1][int(opcion)]
                if not accion:
                    return True
                elif accion == "a":
                    in_menu_vehiculo = self.menu_ataque(vehiculo)
                elif accion == "m":
                    in_menu_vehiculo = self.menu_moverse(vehiculo)
        return in_menu_vehiculo

    def main_menu(self):
        # Menu principal
        # NO TESTEADA
        in_main = True
        while in_main:
            vehiculo = f.get_opciones(
                "VEHICULOS", self.vehiculos, "estado_actual")
            if not vehiculo:
                return True
            else:
                print("\n {} \n".format(vehiculo.name))
                in_main = self.menu_vehiculo(vehiculo)
        return in_main

    def turno(self):
        # Se ejecuta un turno del jugador
        # NO TESTEADA
        # print("\n" * 40)  # SACAR ESPACIOS
        print(self.mapa)
        print(self.anuncio)
        self.anuncio = ""
        in_turno = True
        while in_turno:
            print("""
            1. Seleccionar vehiculo (mover o atacar)

            2. Ingresar al radar

            3. Salir del juego """)

            opcion = f.manejo_opcion(["1", "2", "3"])

            if opcion == "1":
                in_turno = self.main_menu()
            elif opcion == "2":
                self.radar.menu()
            elif opcion == "3":
                sys.exit("Adios! Tu te lo pierdes ;) ")

        self.get_explorador().pasar_turno()
        self.turno_en_ataques()
        f.stop("ESTA LISTO CON SU TURNO, DEJE DE MIRAR PANTALLA")

    def actualizar_vehiculo(self, atacados):
        # Procesa vehiculos atacados si es que estan muertos
        # NO TESTEADA
        muertos = []
        for vehiculo in atacados:
            if vehiculo.res <= 0:
                coor = self.mapa.get_coor_muerto(vehiculo)
                coor_muerto = [(abc[i], j) for i, j in coor]
                muertos.append((vehiculo, coor_muerto))
                self.eliminar_vehiculo(vehiculo)
        return muertos

    def actualizar_string_con_muertos(self, string, muertos):
        # Retorna informacion con string de barco hundido
        # NO TESTEADA
        for muerto in muertos:
            coor = " ".join(str(i) + str(j) for i, j in muerto[1])
            string += "\nSe hundio: {0} en coordenadas - {1} -".format(
                muerto[0].name, coor)
        return string

    def atacar_con_vehiculo(self, ataque, vehiculo):
        # Gestiona el ataque, llamando a distintas funciones de el
        # NO TESTEADA

        if ataque.name == "Kit de ingenierios":
            string = self.atacar_con_kit(ataque)
            self.stats.atacar(vehiculo, ataque.name, 0, 0)
        else:
            coor = ataque.get_coor()
            tablero_oponente = self.juego.el_otro(self).mapa
            if ataque.name == "GBU-43/B Massive Ordnance Air Blast Paralizer":
                atacados = tablero_oponente.aire.evaluar_ataque(coor)
                string = self.atacar_con_paralizador(
                    ataque, vehiculo, atacados, coor)
            else:
                atacados = tablero_oponente.mar.evaluar_ataque(coor)
                if ataque.name == "Misil de Crucero BGM-109 Tomahawk":
                    string = self.atacar_con_misil(
                        ataque, vehiculo, atacados)
                else:
                    string = self.atacar_con_otros(
                        ataque, vehiculo, atacados, coor)
                    if vehiculo.name == "Kamikaze IXXI":
                        self.vehiculos_aire.remove(vehiculo)
                        self.mapa.get_coor_muerto(vehiculo)

        self.radar.agregar_turno(string)
        print("\n{}\n".format(string))
        return False

    def atacar_con_kit(self, ataque):
        # Ataca con kit de ingenieros
        # Retorna string con estado del ataque
        # NO TESTEADA
        atacados = f.get_opciones(
            "VEHICULOS", self.vehiculos, "estado_actual", salir=False)
        ataque.atacar(atacados)
        string = "Kit de ingenieros usado exitosamente en {}".format(
            atacados.name)
        return string

    def atacar_con_paralizador(self, ataque, vehiculo, at, coord):
        # Ataca con paralizador, si ambas casillas coinciden
        # y si el explorador no se encuentra ya paralizado
        # NO TESTEADA
        if len(at) == 2 and at[0] is at[1] and at[0].movible:
            string = self.radar.format_radar(
                True, vehiculo, ataque, coor=coord)
            ataque.atacar(at[0])
            self.stats.atacar(vehiculo, ataque.name, 0, 0)
        else:
            string = self.radar.format_radar(
                False, vehiculo, ataque, coor=coord)
            ataque.atacar(False)
            self.stats.atacar(vehiculo, ataque.name, 1, 0)
        return string

    def atacar_con_misil(self, ataque, vehiculo, atacados):
        # Ataca con misil, dada lista de atacados
        # NO TESTEADA
        if len(atacados) == 0:
            string = self.radar.format_radar(False, vehiculo, ataque)
            ataque.atacar(False)
            self.stats.atacar(vehiculo, ataque.name, 1, ataque.dano)
        else:
            string = self.radar.format_radar(True, vehiculo, ataque)
            muertos = self.juego.el_otro(
                self).actualizar_vehiculo(ataque.atacar(atacados))
            string = self.actualizar_string_con_muertos(string, muertos)
            self.stats.atacar(
                vehiculo, ataque.name, 0, ataque.dano * len(set(atacados)))
            for atacado in set(atacados):
                self.juego.el_otro(self).stats.recibir_dano(
                    atacado, ataque.dano)
        return string

    def atacar_con_otros(self, ataque, vehiculo, atacados, coord):
        # Ataca con ataques no especiales, dada coordenada singular
        # NO TESTEADA
        if len(atacados) == 0:
            string = self.radar.format_radar(
                False, vehiculo, ataque, coor=coord)
            ataque.atacar(False)
            self.stats.atacar(vehiculo, ataque.name, 1, ataque.dano)

        else:
            string = self.radar.format_radar(
                True, vehiculo, ataque, coor=coord)
            muertos = self.juego.el_otro(self).actualizar_vehiculo(
                ataque.atacar(atacados[0]))
            string = self.actualizar_string_con_muertos(string, muertos)
            if vehiculo.name == "Kamikaze IXXI":
                d = atacados[0].res_hist
            else:
                d = ataque.dano
            self.stats.atacar(vehiculo, ataque.name, 0, d)
            self.juego.el_otro(self).stats.recibir_dano(
                atacados[0], d)
        return string

    def menu_moverse(self, veh):
        # Menu moverse
        # NO TESTEADA
        in_menu_moverse = True
        while in_menu_moverse:
            sector = self.mapa.get_sector_vehiculo(veh)
            if veh.sym != "Ⓛ" and veh.sym != "Ⓔ":
                mov = f.get_opciones("MOVIMIENTOS", sector.mov_disp(veh), None)
                if not mov:
                    return True
                else:
                    sector.mover_vehiculo(veh, mov)
                    self.stats.mover(veh)
                    s = "{0} movido en direccion {1}".format(veh.name, mov)
                    self.radar.agregar_turno(s)
                    return False
            elif veh.sym == "Ⓛ":
                coor_ok = False
                while not coor_ok:
                    a = "donde desea ubicar cabeza de la lancha"
                    coor = f.get_coor(a, sector)
                    cf = coor[0]
                    cc = coor[1]
                    if veh.is_horizontal() and not cc+1 > 11:
                        if sector.grilla[cf][cc+1] is None:
                            a = sector.encontrar_coordenadas(veh)
                            sector.eliminar_vehiculo(a)
                            sector.grilla[cf][cc] = veh
                            sector.grilla[cf][cc+1] = veh
                            coor_ok = True
                        else:
                            a = "\nEl segundo componente queda en cas ocupada!"
                            print(a)
                    elif not veh.is_horizontal() and not cf+1 > 11:
                        if sector.grilla[cf+1][cc] is None:
                            a = sector.encontrar_coordenadas(veh)
                            sector.eliminar_vehiculo(a)
                            sector.grilla[cf][cc] = veh
                            sector.grilla[cf+1][cc] = veh
                            coor_ok = True
                        else:
                            a = "\nEl segundo componente queda en cas ocupada!"
                            print(a)
                    else:
                        a = "\nEl segundo componente traspasa el tablero!"
                        print(a)
                self.stats.mover(veh)
                self.radar.agregar_turno("Lancha movida exitosamente")
                return False
            elif veh.sym == "Ⓔ":
                coor_ok = False
                while not coor_ok:
                    coor = f.get_coor("donde desea ubicar el centro (es 3x3)",sector)
                    res = sector.revisar_around_coor(coor)
                    if isinstance(res,list):
                        coor_ok = True
                        sector.eliminar_vehiculo(sector.encontrar_coordenadas(veh))
                        for i,j in res:
                            sector.grilla[i][j] = veh
                        exploracion = veh.explorar(res, self.juego.el_otro(self).mapa)
                        self.stats.mover(veh)
                        s = "Explorador revelo {} vehiculos".format(exploracion[0])
                        if exploracion[1]:
                            s += " en sector maritimo enemigo y si revelo ubicacion"
                            s1 = "En turno enemigo ud fue explorado en "
                            s1 += " ".join([abc[i[0]]+str(i[1]) for i in res])
                            self.juego.el_otro(self).radar.agregar_anuncio(s1)
                            self.juego.el_otro(self).anuncio = s1
                        elif not exploracion[1]:
                            s += " en sector maritimo enemigo y no revelo ubicacion"
                        print("\n" + s)
                        self.radar.agregar_turno(s)
                    else:
                        print(res)
                return False
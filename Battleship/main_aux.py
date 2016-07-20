from clases.clase_juego import Juego
from tools import funciones_aux as f
import random as r


def cargar_tableros(juego):
    num = [i for i in range(12)]
    for p in juego.players:
        mapa = [(p.vehiculos_mar, p.mapa.mar), (p.vehiculos_aire, p.mapa.aire)]
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
        print(p.mapa)
    return juego

juego = Juego()  # aux
juego = cargar_tableros(juego)  # aux
emp = juego.sorteo()  # original
print("Empieza el Jugador {0} !".format(emp.id))  # original
f.stop("\n\n\n JUGADOR {} CIERRE LOS OJOS!".format(juego.el_otro(emp).id))
ter = juego.run(emp)  # original
print("\nGracias por jugar! Congrats again to P{0}".format(ter.id))  # original
print("\n  BATTLESHEEP, el ajedrez del futuro. \n")  # original

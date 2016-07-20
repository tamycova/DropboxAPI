import sys
from tools import funciones_aux as f
from clases.clase_juego import Juego


if __name__ == '__main__':

    print(""" \n
    Bienvenidos a BATTLESHEEP, ¡el juego preferido de los ingenieros!

    Elija un modo de juego:

    1. Jugador vs Jugador

    2. Jugador vs Maquina

    3. Salir del juego """)

    players = {}
    opcion = f.manejo_opcion(["1", "2", "3"])
    if opcion == "1":
        juego = Juego()
        opcion_ok = True
        players["1"] = input("\n Ingrese el nombre del Jugador 1: ")
        players["2"] = input("\n Ingrese el nombre del Jugador 2: ")
    elif opcion == "2":
        juego = Juego(maquina=True)
        players["1"] = input("\n Ingrese el nombre del Jugador 1: ")
        players["2 (M)"] = "SuperMachine"
    elif opcion == "3":
        sys.exit("Adios! Tu te lo pierdes ;) ")

    juego.posicionar_vehiculos()

    emp = juego.sorteo()
    print("\n" * 40)  # SACAR ESPACIOS
    print("Sorteo realizado exitosamente. ", end="")
    print("Empieza {0}, el Jugador {1} !".format(players[emp.id], emp.id))
    f.stop("\n\n\n JUGADOR {} CIERRE LOS OJOS!".format(juego.el_otro(emp).id))

    ter = juego.run(emp)

    print("\nGracias por jugar! Congrats again to {0}".format(players[ter.id]))

    print("\n  BATTLESHEEP, el ajedrez del futuro. \n")

from string import ascii_lowercase as abc

dic_board = dict(zip(abc[:12], [i for i in range(15)]))


def stop(mensaje):
    # Genera un stop en la consola, para que el siguiente jugador
    # no pueda ver el mapa del otro
    # TESTEADA
    input(mensaje + " press any key to continue     ")
    return True


class CasillaOcupada(Exception):
    # Excepcion unica para cuando una casilla esta ocupada

    def __init__(self, c, v):
        super().__init__("\nLa casilla {0} esta ocupada por {1}".format(c, v))


def def_orientacion(objeto, s):
    # Manejo de error para elegir orientacion de vehiculo
    # NO TESTEADA
    orientacion_def = False
    while not orientacion_def:
        try:
            opcion = input(
                "\n¿Desea su {} horizontal(h) o vertical(v)? h/v: ".format(s))
            if opcion == "h":
                orientacion_def = True
                print("\n-> La cabeza es el inicio de la pieza de izq a der")
            elif opcion == "v":
                orientacion_def = True
                objeto.girar()
                print("\n-> La cabeza es el inicio de la pieza de arr a abaj")
            else:
                if not opcion.isalpha():
                    raise TypeError("\nDebe ingresar una letra, h o v")
                elif not opcion.islower():
                    raise ValueError("\nLa letra debe estar en minusculas!")
                else:
                    raise ValueError("\nLa letra debe ser h o v")
        except(TypeError, ValueError) as err:
            print(err)

    return objeto


def get_coor_tomahawk():
    # Manejo de error para elegir coordenada del misil tomahwak
    # retorna lista con coordenadas de la fila o la columna
    # NO TESTEADA
    coordenada_def = False
    while not coordenada_def:
        try:
            coor = input(
                "\nLetra o numero de la fila/columna que desa atacar: ")
            if not coor.isalpha() and not coor.isnumeric():
                raise TypeError("\nDebe ser letra o numero!")
            if coor.isalpha() and coor not in dic_board:
                if not coor.islower():
                    raise ValueError("\nLa letra debe estar en minusculas!")
                else:
                    raise IndexError("\nLa letra debe ser entre la a y la l!")
            if coor.isnumeric() and (int(coor) > 11 or int(coor) < 0):
                raise IndexError("\nEl numero debe estar entre 0 y 11!")
            if coor.isalpha():
                return [(dic_board[coor], i) for i in range(12)]
            if coor.isnumeric():
                return [(i, int(coor)) for i in range(12)]
        except(ValueError, TypeError, IndexError) as err:
            print(err)


def get_coor(str="", sector = False):
    # Manejo de errores para recibir una coordenada validam si se entrega
    # sector ademas revisa que coordenada este vacia
    # NO TESTEADA
    coordenada_def = False
    while not coordenada_def:
        try:
            coor = input(
                "\nCoordenada LetraNumero {}: ".format(str))
            if len(coor) > 3 or len(coor) < 2:
                raise ValueError(
                    "\nDebe ser letra y numero max 2 digitos, nada mas/menos!")
            if not coor[0].isalpha():
                raise TypeError(
                    "\nPrimer valor de la coordenada debe ser una letra!")
            if coor[0] not in dic_board:
                if not coor[0].islower():
                    raise ValueError("\nLa letra debe estar en minusculas!")
                else:
                    raise IndexError("\nLa letra debe ser entre la a y la l!")
            if len(coor) == 2:
                if not coor[1].isnumeric():
                    raise TypeError(
                        "\nSegundo valor de la coordenada debe ser un numero!")
            if len(coor) == 3:
                if not coor[1].isnumeric() or not coor[2].isnumeric():
                    raise TypeError(
                        "\nSegundo valor de la coordenada debe ser un numero!")
                if int(coor[1:]) > 11 or int(coor[1:]) < 0:
                    raise IndexError("\nEl numero debe estar entre 0 y 11!")
            if sector and not sector.is_vacia((dic_board[coor[0]], int(coor[1:]))):
                    raise CasillaOcupada(coor,sector.grilla[dic_board[coor[0]]][int(coor[1:])].name)

            return (dic_board[coor[0]], int(coor[1:]))

        except(ValueError, TypeError, IndexError,CasillaOcupada) as err:
            print(err)


def manejo_opcion(validas, string="opcion"):
    # Dada una lista de opciones validas, maneja los errores de input asociados
    # NO TESTEADA
    opcion_ok = False
    while not opcion_ok:
        try:
            opcion = input("\n Ingresar {}:  ".format(string))
            if not opcion.isnumeric():
                raise TypeError("\nLa opcion debe ser un numero. Try again!")
            if opcion not in validas:
                raise ValueError(
                    "\nLa opcion debe ser entre {}-{}. Try again!".format(
                        validas[0], validas[-1]))
            else:
                opcion_ok = True
        except (ValueError, TypeError) as err:
            print(err)
    return opcion


def get_coor_around(coor):
    # Dada una coordenada, permite elegir otra coordenada alrededor
    # Usada para ataque paralizer
    # NO TESTEADA
    print("\nElija la segunda coordenada (ambas deben alcanzar al enemigo): ")
    num = coor[1]
    dic = {}
    n = 1
    if num - 1 >= 0:
        dic.update({str(n): (coor[0], num - 1)})
        print ("{0}. {1}{2}".format(n, abc[coor[0]], num - 1))
        n += 1
    if num + 1 <= 11:
        dic.update({str(n): (coor[0], num + 1)})
        print ("{0}. {1}{2}".format(n, abc[coor[0]], num + 1))
        n += 1
    if coor[0] + 1 <= 11:
        dic.update({str(n): (coor[0] + 1, num)})
        print ("{0}. {1}{2}".format(n, abc[coor[0] + 1], num))
        n += 1
    if coor[0] - 1 >= 0:
        dic.update({str(n): (coor[0] - 1, num)})
        print ("{0}. {1}{2}".format(n, abc[coor[0] - 1], num))
    opcion = manejo_opcion([str(i) for i in range(n)])
    return dic[opcion]


def get_opciones(tipo, iterable, at, salir=True):
    # Imprime opciones de un iterable, dado atributo, metodo o string
    # Retorna elemento seleccionado
    # NO TESTEADA
    print("\n SUS {} DISPONIBLES \n".format(tipo))
    dic = {i + 1: j for i, j in enumerate(iterable)}
    n = len(dic)
    for op in dic:
        if at is not None:
            imp = getattr(dic[op], at)
            if not hasattr(imp, "__call__"):
                print("{0}. {1}".format(op, imp))
            else:
                print("{0}. {1}".format(op, imp()))
        else:
            print("{0}. {1}".format(op, dic[op]))
    if salir:
        print("{0}. SALIR".format(n + 1))
        dic[n + 1] = False
    opcion = manejo_opcion([str(i + 1) for i in range(len(dic))])
    elemento = dic[int(opcion)]
    return elemento

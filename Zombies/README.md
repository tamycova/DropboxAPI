# Zombie Attack

A simple game, runs well in Ubuntu. Code and README in spanish. 

### ESTRUCTURA DEL REPO
```sh
/T05
|-- main.py                     
Se ejecuta para iniciar el juego
|-- load_ui_game.py
Carga la ui del juego
|-- load_ui_menus.py
Carga las uis de los menus
|-- ui_methods.py
Metodos de ui (centralizar la ventana)
-- /threads                     
Aqui se encuentran los threads usados (sniper no es un thread)
|   |-- balas.py
|   |-- helicoptero.py
|   |-- reloj.py
|   |-- sniper.py
|   |-- zombies.py
-- /uis  
|   |-- inicio.ui
|   |-- juego.ui
|   |-- pausa.ui
|   |-- over.ui 
-- /assets      
```

### Main.py

Al correr el main aparece la ventana inicio, el resto del desarrollo del juego es bastante intuitivo. Se pausa con la tecla espacio y los movimientos del jugador son con las flechas del teclado. Al perder aparece una ventana game over con el puntaje final.


### Acerca del sistema de colisiones

Las colisiones entre zombies se permiten a menos que soprelapen completamente, esto porque son imagenes png y controlar dichas colisiones le quita realismo y continuidad a su movimiento (el juego de referencia si pemite que se sobrelapen). Un zombie no puede entrar donde esta el jugador, pero el jugador si puede pasar donde hay zombies (eso le permite escapar si esta rodeado, sino no podría!) [aunque es un poco suicida]. Las municiones y vida aparecen a cierta distancia mínima del jugador. 

### Acerca de los tiempos

Se determinaron, bajo mi criterio, los mejores tiempos para el desarrollo del juego. El lambda de los zombies quizas pueda ser considerado un poco rapido pero sino hay largos periodos de tiempo (al ser aleatorio a veces 40 segundos) en los que no aparece algun zombie. Además, las velocidades tambien ayudan a que el computador no colapse (si emito muchas señales en los threads el mio se quedaba pegado), pero con estos tiempos me corre perfectamente:

- Rango de la bala: 300 pixeles, si no pega a nada una vez avanzada dicha trayectoria desaparece. 
- Aparicion de municiones y vida: cada 30 segundos (decidi que aparecieran juntos para que el jugador deba elegir cual escoger juju)
- Duracion municiones y vida: 15 segundos
- Municiones dan +30 de vida (necesario para el final porque aparecen muchos zombies) y vida dan +20 (equivalente a dos ataques de zombies) [**la representacion grafica y numerica de las vidas esta en la barra, donde se indica el porcentaje de vida y la barra de progreso**]
- Lambda zombies: parte en 1/4, y cada 30 segundos baja un punto (1/3, 1/2), es decir al minuto y medio la tasa es 1 (un zombie cada un segundo) y luego se queda ahi (sino seria satanico). 
- Cada a ataque de zombie baja en -10 la vida [**cuando ataca, un zombie queda dormido brevemente lo que permite que el jugador escape**] 
- El puntaje solo se agrega tras matar un zombie, y se suma el doble de lo que llevamos de tiemp0 (al segundo 10 matar un zombie te da +20, pero al minuto matar un zombie te da +120)

### Acerca de los threads

Los threads son almacenados en memoria, pero se elimina su referencia cada vez que terminan, fui muy rigurosa en que los threads no queden running cuando se supone que no deberian. 

El Helicoptero es un thread generador de municiones, el Zombie Generator es un thread generador de Zombies. El sniper no es un thread (ya que es unico y se mueve por eventos de mouse y teclado), pero genera Balas. El Reloj funciona por abajo, pero sirve para actualizar el puntaje.

### Acerca de notificaciones y movimientos

Cuando un zombie muere y cuando el jugador es atacado se notifica con una imagen en la esquina superior derecha (calavera y sangre respectivamente).

El jugador tiene tres estados de movimiento (pie derecho adelante, pies juntos, pie izquierdo adelante) y los zombies tienen 6. 

### Variables importantes (para la revisión)
- load_ui_game.py:
    - linea 40 hasta 43, variables de inicio (con cuantas municiones, vida, ptje parte el jugador)
    - linea 46, funcion puntaje
- balas.py:
    - linea 22, cada cuanto emite la bala la señal de moverse
    - linea 34, la distancia en pixeles a la que detecta el zombie
    - linea 41, el rango de la bala
- helicoptero.py:
    - linea 18 y 22, el tiempo entre cada conjunto de municiones y vida
    - linea 84, duracion de las municiones y las vidas
    - linea 85, distancia a la que detecta el jugador
    - linea 93 y 96, lo que suma obtener una municion o una vida
- sniper.py:
    - linea 72 y 73, el *25 determina cuantos pixeles avanza la bala en cada movimiento
    - linea 27 y 28, el *3 determina cuantos pixeles avanza el jugador en cada movimiento
- zombie.py:
    - linea 20: lambda de aparicion de los zombies 
    - linea 90: cada cuanto se mueve el zombie
    - linea 92: a que distancia del jugador se considera que ataca
    - linea 106: cuando de vida le quita al jugador
. 



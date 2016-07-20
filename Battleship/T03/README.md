# BATTLESHIP 2.0

A battleship game (1 vs 1 and 1 v machine) with additional funcionalities, it's console based (code and rest of README written in spanish). A week project.   

### ESTRUCTURA DEL REPO
```sh
/T03
|-- main.py                     
Debe ejecutarse para iniciar el programa
|-- main_aux.py
Main alternativo para probar el programa entre 2 jugadores sin cargar las piezas
|-- run_tests.py
Debe ejecutarse para ejecutar los tests de la tarea
|-- /clases                       
Aqui se encuentran los archivos de la modelacion del programa
|   |-- clase_juego.py
|   |-- clases_ataques.py
|   |-- clases_data.py
|   |-- clase_smart.py
|   |-- clases_piezas.py
|   |-- clases_players.py
|   |-- clases_tablero.py
|-- /tests
Aqui se encuentran los tests que se ejecutan con el modulo discover    
|   |-- test_clase_juego.py
|   |-- test_clases_ataques.py
|   |-- test_clases_data.py
|   |-- test_clase_smart.py
|   |-- test_clases_piezas.py
|   |-- test_clases_players.py
|   |-- test_clases_tablero.py
|   |-- test_funciones_aux.py
|-- /tools
Aqui se encuentran funciones auxiliares, especialmente las de manejo de error
|   |-- funciones_aux.py
```

### Directorio principal

En el directorio principal hay 3 archivos. El **run_tests.py** usa el modulo discover de unittest para ejecutar los tests de las funciones, **main.py** es el main oficial de la tarea y **main_aux.py** puede ejecutarse si no se desea jugar realmente (se salta la eterna fase de posicionamiento y no tiene la opcion de jugar vs maquina).  

### Decisiones de la modelacion

La mayoria de las interacciones entre clases usa **ducktyping**, esto porque hay vehiculos que hacen cosas especificas al atacar y otros no, ataques que hacen cosas especificas, etc. Desde la clase juego se maneja la dinamica entre ambos jugadores (haciendo llamadas a funcion turno por ejemplo o posicionar vehiculos, que es distinta para maquina y jugador pero tienen el mismo nombre). Ademas, cada jugador tiene una referencia al juego lo que le permite enviar anuncios y daño recibido al otro jugador (se que esto no es correcto, pero **tuve especial cuidado en que la inteligencia artifical no acceda a la informacion del otro jugador**).

##### Sobre el juego en general

- **Fije n como 12**, considero que es el tamaño optimo para que el juego no sea eterno, haya suficiente espacio entre vehiculos y los dos sectores puedan printearse en pantalla
- El sorteo no se hace por consola, el programa lo hace automaticamente con numeros **seudoaeatorios**.
- Los barcos estan representados por simbolos, **el unico momento en que declaro su simbolo es al posicionarlos** (considero que es suficiente porque son muy autoexplicativos) [por temas de espacio y comodidad para ver mapa en cada turno].
- La **orientacion de los vehiculos es fijada** al posicionar los vehiculos, luego estos se pueden mover paralelamente o en direccion de su orientacion pero no cambiarla (lo hice para que sea mas similar al juego original).
- **Fije el numero de vehiculos como 1 de cada tipo**, despues de mucho pensarlo considere que es lo mejor, porque si hay 3 barcos pequeños por ejemplo el ataque Tomahawk estaria disponible cada turno y no habria restriccion de "cada 3 turnos", ademas se requeriria un mapa mas grande y es incomodo para la interaccion con la consola. 
- **La restriccion de turnos considera los turnos intermedios**, por ejemplo si el ataque es cada 3 turnos: turno 1 use el ataque - turno 2 - turno 3 - turno 4 - turno 5 vuelve a estar disponible (similar para el paralizador).
- Los barcos hundidos desaparecen del mapa (literalmente se huden).
- Para hacer mas realistica la interaccion en consola se usaron **stops de input y prints de lineas en blanco**, de esta forma al terminar de un turno un jugador "le pasa el computador al otro" y ninguno puede ver el mapa o la accion realizada por el jugador. 

##### Sobre los vehiculos y ataques

- **Las restricciones de ataque se aplican aunque el ataque falle**, es decir el kamikaze solo puede ser usado una vez, y si falla igual muere (es como si chocara contra el mar).
- Para las estadisticas, **el daño del kamikaze es considerado como igual al de la resistencia historica del vehiculo que ataco**, porque sino al atacar con "infinito" las estadisticas no sirven de mucho.
- El **kit de ingenieros si permite aumentar la resistencia de un vehiculo** (dejar el puerto en 81 por ejemplo), esto porque considero que abre nuevas estrategias para engañar al rival y porque no es un cambio muy drastico, no se gastaran todos los turnos en aumentar la resistencia en +1 considerando las magnitudes de los ataques, y ademas tiene restriccion de 2 turnos. 
- **TODOS** los vehiculos menos la lancha tienen los ataques paralizer y trident, esto para evitar quedarse sin ataques y que el juego deje de tener sentido. 
- **El ataque paralizer solo surte efecto si el explorador enemigo esta movible**, es decir, no se puede dejar pegado al explorador enemigo eternamente (paralizarlo por 5 turnos mas cuando esta en su 4to turno de paralizacion, por ejemplo). 

##### Sobre el radar

- El radar entrega la informacion de lo hecho en cada turno y los anuncios del turno oponente (si es que su explorador delato posicion). No incluye si fuiste atacado o no, ya que **en el menu de vehiculos se muestra su resistencia parcial** y esto es suficiente para saber si te estan atacando.
- **No considere necesario mostrar mapas en el radar**, ya que puede ser hasta confuso por los movimientos del rival y ocupa demasiado espacio en la consola.  

### Sobre el Testing y la Modularizacion

**El testing fue hecho con unittest y su libreria mock para simular input del usuario.** 

| Modulo            | Testeadas |   
| ----------------- | --------- |   
| clase_juego.py    |   3/6     |
| clases_ataques.py |   9/12    |
| clases_data.py    |   9/12    |
| clase_smart.py    |   2/9     |
| clases_piezas.py  |   7/10    |
| clases_players.py |   4/18    |
| clases_tablero.py |   14/18   |
| funciones_aux.py  |   1/7     |
| TOTAL             | 49/92 (0.53%) | 
 
Pese a que intente modularizar lo más posible, hay funciones que estan en su mayoria compuestas de muchas otras funciones por lo que se ven muy grandes (funciones como atacar,mover, etc). Esas funciones son las que no testee, y estan en su mayoria concentradas en el modulo clases_players.py y clase_smart.py (menus, funciones de consola y funciones compuestas). Tampoco testee las funciones de manejo de error en funciones_aux.py ya que estan relacionadas a input del usuario y no fallan (issue #295) [obvio que todas las funciones para las que no hay test igual fueron probadas en consola].

**No considere como testeables los metodos __repr__ o __str__ o __init__** y tampoco los metodos que fueron ya testeados en la clase super y son heredados sin modificacion alguna a la subclase. 

Gracias al metodo setUp todos los test son independientes, pese a pertenecer al mismo objeto unittest. Hay tests con muchos asserts dentro, ya que **intento probar muchas situaciones posibles para la funcion que se desea testear** sin inflar el numero de tests. 

**TODAS LAS FUNCIONES ESTAN COMENTADAS**, indicando que hacen y si fueron testeadas o no. 

### Sobre el Manejo de errores

La principal forma de manejo de errores fue **quitarle la posibilidad al usuario de cometer errores**, esto se hizo a traves de booleanos que permitian saber cuando un vehiculo s
e podia mover o cuando un ataque estaba disponible y solo ofrecer las opciones disponibles (ver **get_opciones() y manejo_opcion()**).

Los errores muy exclusivos (como en modulo estadisticas) se hicieron con **sentencias if/else**, y lo que mas se controlo fueron los errores de interaccion con la consola. Revisar especialmente **modulo funciones_aux.py** aunque igual hay sentencias try/except en otras partes del programa (chequeo de coordenadas). 

### Sobre la Inteligencia

La inteligencia adopta una estrategia **agresiva** basada en la **priorizacion de acciones** y en la **informacion de la exploracion** (considero que el explorador es la mejor herramienta para esta estrategia, y por lo mismo el ataque de mayor prioridad es el paralizer si es que se me avisa que fui explorada).  

- get_ataque_optimo() : Le permite **elegir el mejor ataque** (segun lo que yo creo que es el mejor ataque **para su estrategia**) dada las circunstancias (si esta disponible o no). El orden de prioridad es: **Minuteman** (porque ataca 15), **Napalm** (porque puede atacar 10) y **Trident** (porque **siempre esta disponible**, lo llamo desde avion caza asi me aseguro que siempre estara esta opcion). Si es que la inteligencia se da cuenta que debe usar kamikaze en un barco (ataco al barco con +30 y este aun no muere, es puerto o buque de guerra), **la primera prioridad pasa al ataque kmkz**.

- **No inclui el ataque Tomahawk** porque considero que no le entrega suficiente informacion a la inteligencia (si me dice que fue exitoso tendria que revisar toda la fila, y basta con que el enemigo se mueva), **tampoco hago que mueva sus barcos** (personalmente considero que es un gasto de turno, la clave esta en atacar mas rapido que el rival) y **tampoco uso el kit de ingenieros** (porque da solo +1 considero que es mega inservible y es un gasto de turno). 

- **Stack** de coordenadas por atacar (entregada por el explorador si encontro un vehiculo) y variable **atacando** que almacena la coordenada actual que estoy atacando, donde se que hay un vehiculo. 

- **No explicare mas porque sino sera muy facil ganarle!** El codigo esta muy comentado ahi hay mas detalles.


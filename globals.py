from multiprocessing import Semaphore
from pickle import FALSE
from threading import Lock, Condition

#  A total alteração deste arquivo é permitida.
#  Lembre-se de que algumas variáveis globais são setadas no arquivo simulation.py
#  Portanto, ao alterá-las aqui, tenha cuidado de não modificá-las.
#  Você pode criar variáveis globais no código fora deste arquivo, contudo, agrupá-las em
#  um arquivo como este é considerado uma boa prática de programação. Frameworks como o Redux,
#  muito utilizado em frontend em libraries como o React, utilizam a filosofia de um store
#  global de estados da aplicação e está presente em sistemas robustos pelo mundo.

release_system = False
mutex_print = Lock()
planets = {}
bases = {}
mines = {}
simulation_time = None

# Sincronização de pedidos da lua
moon_ask_lion_launch = Semaphore(0) # Lua da release para solicitar foguete lion
alredy_asked = False # Impede lua de pedir foguetes caso já tenha pedido
lock_lion_launch = Lock() # TODO logica desse lock ainda incompleta
moon_wait = Condition(lock_lion_launch) # Lua aguarda recursos

# * Sincronização para as viagens
# Garante que apenas 2 foguetes estejam em rota para Marte
voyage_mars = Semaphore(2)
# Se lock estiver travado rota para o polo sul
mars_north_pole = Lock()

# Garante que apenas 2 foguetes estejam em rota para Io
voyage_io = Semaphore(2)
# Se lock estiver travado rota para o polo sul
io_north_pole = Lock()

# Garante que apenas 2 foguetes estejam em rota para Ganimedes
voyage_ganimedes = Semaphore(2)
# Se lock estiver travado rota para o polo sul
ganimedes_north_pole = Lock()

# Garante que apenas 2 foguetes estejam em rota para Europa
voyage_europa = Semaphore(2)
# Se lock estiver travado rota para o polo sul
europa_north_pole = Lock()

oil_units = 5       # Valor base para receber oil
uranium_units = 5   # Valor base para receber urânio

# * Sincronização para abastecimento das bases:

# Protege a região critica Pipeline.unities:
pipeline_units = Lock()
# Quantas unidades de óleo estão disponíveis?
oil_avaliable = Semaphore(0)
# Quantas unidades de urânio estão disponíveis?
uranium_avaliable = Semaphore(0)
# Faz dois consumidores não acessarem a região crítica
pipeline_consumidor = Lock()
# Condition para consumir oil
pipeline_itens = Condition(pipeline_units)


# Protege a região critica StoreHouse.unities:
store_house_units = Lock()
# Faz dois consumidores não acessarem a região crítica:
store_house_consumidor = Lock()
# Condition para consumir
store_house_itens = Condition(store_house_units)


def acquire_print():
    global mutex_print
    mutex_print.acquire()


def release_print():
    global mutex_print
    mutex_print.release()


def set_planets_ref(all_planets):
    global planets
    planets = all_planets


def get_planets_ref():
    global planets
    return planets


def set_bases_ref(all_bases):
    global bases
    bases = all_bases


def get_bases_ref():
    global bases
    return bases


def set_mines_ref(all_mines):
    global mines
    mines = all_mines


def get_mines_ref():
    global mines
    return mines


def set_release_system():
    global release_system
    release_system = True


def get_release_system():
    global release_system
    return release_system


def set_simulation_time(time):
    global simulation_time
    simulation_time = time


def get_simulation_time():
    global simulation_time
    return simulation_time

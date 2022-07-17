# from multiprocessing import Semaphore
from pickle import FALSE
from threading import Lock, Condition, Semaphore

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
# Lua da release para solicitar foguete lion
moon_ask_lion_launch = Semaphore(0)
alredy_asked = False  # Impede lua de pedir foguetes caso já tenha pedido
lock_lion_launch = Lock()  # Impede deadlock na lua
moon_wait = Condition(lock_lion_launch)  # Lua aguarda recursos
need_notify = Lock()  # Gerencia se lua precisa de notify quando recursos chegarem
moon_constraints = Lock()  # Protege região critica dos recurso da lua
send_next_to_moon = Lock()  # Garante que o foguete para lua será enviado

# * Sincronização para as viagens
# Garante que apenas 2 foguetes estejam em rota para Marte
voyage_mars = Semaphore(100)  # Sincronização para órbita
colision_course_mars = Semaphore(2)  # No máximo 2 em rota de colisão
# Se lock estiver travado rota para o polo sul
mars_north_pole = Lock()  # Bloqueia ao colidir com polo norte
# é liberado pela colisão com o polo sul

# Garante que apenas n foguetes estejam em rota para Io
voyage_io = Semaphore(100)  # Sincronização para órbita
colision_course_io = Semaphore(2)  # No máximo 2 em rota de colisão
# Se lock estiver travado rota para o polo sul
io_north_pole = Lock()  # Bloqueia ao colidir com polo norte
# é liberado pela colisão com o polo sul

# Garante que apenas n foguetes estejam em rota para Ganimedes
voyage_ganimedes = Semaphore(100)
colision_course_ganimedes = Semaphore(2)  # No máximo 2 em rota de colisão
# Se lock estiver travado rota para o polo sul
ganimedes_north_pole = Lock()  # Bloqueia ao colidir com polo norte
# é liberado pela colisão com o polo sul

# Garante que apenas n foguetes estejam em rota para Europa
voyage_europa = Semaphore(100)  # Sincronização para órbita
colision_course_europa = Semaphore(2)  # No máximo 2 em rota de colisão
# Se lock estiver travado rota para o polo sul
europa_north_pole = Lock()  # Bloqueia ao colidir com polo norte
# é liberado pela colisão com o polo sul

colision_course = {
    'MARS': colision_course_mars,
    'IO': colision_course_io,
    'GANIMEDES': colision_course_ganimedes,
    'EUROPA': colision_course_europa
}

pole = {
    'MARS': mars_north_pole,
    'IO': io_north_pole,
    'GANIMEDES': ganimedes_north_pole,
    'EUROPA': europa_north_pole
}

# * Sincronização para colisão


#! Variar para testar desempenho:
oil_units = 17       # Valor base para receber oil
uranium_units = 35  # Valor base de urânio para 1 foguete

# Deveria estar no construtor de cada mina:
#! Devem ser atualizados quando o recurso for decrementado da base
uranium_loads = 0   # Variável que diz para a mina quanto urânio tinha
oil_loads = 0       # Variável que diz para a mina quanto oil tinha

# * Sincronização para abastecimento das bases:

# Protege a região critica Pipeline.unities:
pipeline_units = Lock()
# Quantas unidades de óleo estão disponíveis?
available_oil = Semaphore(0)
# Faz dois consumidores não acessarem a região crítica
pipeline_consumidor = Lock()  # TODO verificar se usa em bases se não, REMOVER
# Condition para consumir oil
# TODO verificar se usa em bases se não, REMOVER
pipeline_itens = Condition(pipeline_units)

# Protege a região critica StoreHouse.unities:
store_house_units = Lock()
# Quantas unidades de urânio estão disponíveis?
available_uranium = Semaphore(0)
# Faz dois consumidores não acessarem a região crítica:
store_house_consumidor = Lock()  # TODO verificar se usa em bases se não, REMOVER
# Condition para consumir
# TODO verificar se usa em bases se não, REMOVER
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


# * Funções para as minas:

# Devia ser um método da classe minas
def delivery_control(unities, units_ready, global_material_loads, semaphore):
    '''Executa N° releases em semaphore, com base em N° envios possíveis de carga
    @param int unities: self.unities
    @param units_ready: Variável para armazenar int de n unidades prontas
    @param global_material_loads: Variável global para armazenar int de cargas de material
    @param semaphore: Semáforo global para controlar
    '''

    # Faz a divisão inteira, possuí "x" units_ready
    current_loads = unities // units_ready
    # Tenho um número de cargas igual ou maior que antes?
    if current_loads >= global_material_loads:
        n = current_loads - global_material_loads   # Diferença entre as cargas
        global_material_loads += n                  # incremento minhas cargas
        #! É nescessário decrementar esse valor a cada x_loads removidos
        # Tenho n cargas disponíveis!
        #!semaphore.release(n)
        # TypeError: SemLock.release() takes no arguments (1 given)
        for i in range(0, n):
            semaphore.release()

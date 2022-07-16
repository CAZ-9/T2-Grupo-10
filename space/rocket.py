from random import randrange, random
from time import sleep
from threading import Thread, current_thread, Semaphore
import globals


class Rocket:

    ################################################
    # O CONSTRUTOR DA CLASSE NÃO PODE SER ALTERADO #
    ################################################
    def __init__(self, type):
        self.id = randrange(1000)
        self.name = type
        if(self.name == 'LION'):
            self.fuel_cargo = 0
            self.uranium_cargo = 0

    def nuke(self, planet):  # Permitida a alteração

        self.damage()
        print(
            f"[EXPLOSION] - The {self.name} ROCKET reached the planet {planet.name} on North Pole")
        print(
            f"[EXPLOSION] - The {self.name} ROCKET reached the planet {planet.name} on South Pole")
        # TODO decrementar a vida do planeta respectivo
        pass

    def voyage(self, planet):  # Permitida a alteração (com ressalvas)
        # Thread da base cria a thread que faz launch

        # TODO lua deve estar em wait
        # TODO alterar lógica para dar notify pra lua se o foguete for lion
        if (planet == 'MOON'):
            # TODO abastecer a lua
            # semáforo para receber o lion e fazer o lançamento
            #! qual o tempo de viagem para a lua?
            #! self.simulation_time_voyage(planet)     # Rocket está viajando
            return

        # Essa chamada de código (do_we_have_a_problem e simulation_time_voyage) não pode ser retirada.
        # Você pode inserir código antes ou depois dela e deve
        # usar essa função.

        self.simulation_time_voyage(planet)     # Rocket está viajando
        failure = self.do_we_have_a_problem()   # Testa falha
        if failure == False:                    # Se não ouveuma falha
            #! mais de uma bomba não pode atingir o mesmo polo ao mesmo tempo
            #! Foguete pode orbitar
            self.nuke(planet)                   # Planeta é bombardeado

    # Retorna o planeta e o polo que o foguete deve viajar
    def planning_launch(self):
        if(self.name == 'LION'):
            planet = 'MOON'
            return planet

        # Semáforos n=2 para garantir que não serão 3 impactos simultâneos
        # Se >0 decrementa, mas não bloqueia
        elif globals.voyage_mars.acquire(blocking=False):
            planet = 'MARS'
            return planet

        elif globals.voyage_io.acquire(blocking=False):
            planet = 'IO'
            return planet

        elif globals.voyage_ganimedes.acquire(blocking=False):
            planet = 'GANIMEDES'
            return planet

        elif globals.voyage_europa.acquire(blocking=False):
            planet = 'EUROPA'
            return planet

        else:
            print(f'Lançamento não autorizado! Aguarde o fim de uma missão! 👩‍🚀')
            return False
        
    def lion_launch(self):
        sleep(0.01) # Quatro dias para o LION chega na lua
        lua = globals.get_mines_ref().get('MOON')
        with globals.moon_constraints: # Impede corrida na leitura e escrita dos recursos da lua
            lua.fuel += self.fuel_cargo # Recarrega combustível da lua
            lua.uranium += self.uranium_cargo # Recarrega urânio da lua
        
        globals.acquire_print()
        print(f"🚀🦁 - [LION] - Arrived in MOON base - refueling ⛽ {self.fuel_cargo} ☢🪨{ self.uranium_cargo}")
        globals.release_print()
        
        globals.lock_lion_launch.acquire()
        globals.alredy_asked = False # Seta false para lua poder pedir proximo LION quando necessário
        if globals.need_notify.locked():
            globals.moon_wait.notify()
        globals.lock_lion_launch.release()
        
        

        ####################################################
        #                   ATENÇÃO                        #
        #     AS FUNÇÕES ABAIXO NÃO PODEM SER ALTERADAS    #
        ####################################################

    def simulation_time_voyage(self, planet):
        if planet.name == 'MARS':
            # Marte tem uma distância aproximada de dois anos do planeta Terra.
            sleep(2)
        else:
            # IO, Europa e Ganimedes tem uma distância aproximada de cinco anos do planeta Terra.
            sleep(5)

    def do_we_have_a_problem(self):
        if(random() < 0.15):
            if(random() < 0.51):
                self.general_failure()
                return True
            else:
                self.meteor_collision()
                return True
        return False

    def general_failure(self):
        print(f"[GENERAL FAILURE] - {self.name} ROCKET id: {self.id}")

    def meteor_collision(self):
        print(f"[METEOR COLLISION] - {self.name} ROCKET id: {self.id}")

    def successfull_launch(self, base):
        if random() <= 0.1:
            print(
                f"[LAUNCH FAILED] - {self.name} ROCKET id:{self.id} on {base.name}")
            return False
        return True

    def damage(self):
        return random()

    def launch(self, base, planet):
        if(self.successfull_launch(base)):
            print(f"[{self.name} - {self.id}] launched.")
            self.voyage(planet)  # !

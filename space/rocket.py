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

    def orbit(self, planet):
        globals.colision_course.get(
            planet.name).acquire()    # em rota de colisão
        self.nuke(planet)

    def nuke(self, planet):  # Permitida a alteração

        if globals.pole.get(planet.name).acquire(blocking=False):
            print(
                f"🎇 - [EXPLOSION] - The {self.name} ROCKET / ID {self.id}, reached the planet {planet.name} on North Pole!")
        else:
            print(
                f"🎇 - [EXPLOSION] - The {self.name} ROCKET / ID {self.id}, reached the planet {planet.name} on South Pole!")
            globals.pole.get(planet.name).release()  # Intercalando a colisão

        # TODO decrementar a vida do planeta respectivo
        damage = self.damage()

        globals.colision_course.get(planet.name).release()    # colidiu

    def voyage(self, planet):  # Permitida a alteração (com ressalvas)

        # Essa chamada de código (do_we_have_a_problem e simulation_time_voyage) não pode ser retirada.
        # Você pode inserir código antes ou depois dela e deve
        # usar essa função.

        self.simulation_time_voyage(planet)     # Rocket está viajando
        failure = self.do_we_have_a_problem()   # Testa falha
        if failure == False:                    # Se não ouveuma falha
            self.orbit(planet)                  # fica em órbita
            # Planeta é bombardeado

    def planning_launch(self):
        '''Retorna o planeta que o foguete deve viajar, retorna falso se nenhum estiver disponível'''
        # Semáforos n=100, esses foguetes ficarão em órbita
        # Se < 0 decrementa, mas não bloqueia
        # TODO planetas que foram terraformados devem parar de ser opções
        if globals.voyage_mars.acquire(blocking=False):
            planet = globals.get_planets_ref().get('mars')
            return planet

        elif globals.voyage_io.acquire(blocking=False):
            planet = globals.get_planets_ref().get('io')
            return planet

        elif globals.voyage_ganimedes.acquire(blocking=False):
            planet = globals.get_planets_ref().get('ganimedes')
            return planet

        elif globals.voyage_europa.acquire(blocking=False):
            planet = globals.get_planets_ref().get('europa')
            return planet

        else:
            return False

    def lion_launch(self):

        sleep(0.01)  # Quatro dias para o foguete LION chegar na lua
        lua = globals.get_bases_ref().get('moon')

        lua.fuel += self.fuel_cargo  # Recarrega combustível da lua
        lua.uranium += self.uranium_cargo  # Recarrega urânio da lua

        globals.acquire_print()
        print(
            f"🚀🦁🚀🦁🚀🦁 - [LION] - Arrived in MOON base - refueling ⛽ {self.fuel_cargo} ☢🪨{ self.uranium_cargo}")
        globals.release_print()

        with globals.moon_wait:
            globals.moon_wait.notify()  # Da notify para base da lua voltar a trabalhar

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
        print(f"[GENERAL FAILURE] - {self.name} ROCKET, ID: {self.id}")

    def meteor_collision(self):
        print(f"[METEOR COLLISION] - {self.name} ROCKET, ID: {self.id}")

    def successfull_launch(self, base):
        if random() <= 0.1:
            print(
                f"[LAUNCH FAILED] - {self.name} ROCKET id:{self.id} on {base.name}")
            return False
        return True

    def damage(self):
        return random()

    def launch(self, base, planet):
        '''recebe objeto base e objeto planet'''
        if(self.successfull_launch(base)):
            print(f"[{self.name} - {self.id}] launched.")
            self.voyage(planet)

from pickle import FALSE, TRUE
import globals
from threading import Thread, Lock
from space.rocket import Rocket
from random import choice


class SpaceBase(Thread):

    ################################################
    # O CONSTRUTOR DA CLASSE NÃO PODE SER ALTERADO #
    ################################################
    def __init__(self, name, fuel, uranium, rockets):
        Thread.__init__(self)
        self.name = name
        self.uranium = 0
        self.fuel = 0
        self.rockets = 0
        self.constraints = [uranium, fuel, rockets]

    def print_space_base_info(self):
        print(f"🔭 - [{self.name}] → 🪨  {self.uranium}/{self.constraints[0]} URANIUM  ⛽ {self.fuel}/{self.constraints[1]}  🚀 {self.rockets}/{self.constraints[2]}")

    def base_rocket_resources(self, rocket_name):
        match rocket_name:
            case 'DRAGON':
                if self.uranium > 35 and self.fuel > 50:
                    self.uranium = self.uranium - 35
                    if self.name == 'ALCANTARA':
                        self.fuel = self.fuel - 70
                    elif self.name == 'MOON':
                        self.fuel = self.fuel - 50
                    else:
                        self.fuel = self.fuel - 100
                    rocket = Rocket('DRAGON')  # constrói foguete
            case 'FALCON':
                if self.uranium > 35 and self.fuel > 90:
                    self.uranium = self.uranium - 35
                    if self.name == 'ALCANTARA':
                        self.fuel = self.fuel - 100
                    elif self.name == 'MOON':
                        self.fuel = self.fuel - 90
                    else:
                        self.fuel = self.fuel - 120
                    rocket = Rocket('FALCON')  # constrói foguete
            case 'LION':
                if self.uranium > 35 and self.fuel > 100:
                    self.uranium = self.uranium - 35
                    if self.name == 'ALCANTARA':
                        self.fuel = self.fuel - 100
                    else:
                        self.fuel = self.fuel - 115
                    rocket = Rocket('LION')  # constrói foguete
            case _:
                print("Invalid rocket name")
                return

        # adiciona foguete ao armazenamento da base
        self.rockets.append(rocket)

    def refuel_oil():
        with globals.pipeline_consumidor:
            with globals.pipeline_units:

                globals.get_mines_ref()['oil_earth'].unities -= 5

            pass

    def refuel_uranium():
        pass

    def run(self):
        globals.acquire_print()
        self.print_space_base_info()
        globals.release_print()

        self.rockets = []
        random_rockets = ['DRAGON', 'FALCON']

        while(True):
            if (globals.get_release_system()):
                return

            # Se MOON, verificar se precisa de recursos
            if (self.name == 'MOON' and self.uranium < 35 and self.fuel < 50 and len(self.rockets) == 0):
                    globals.moon_wait.wait() # TODO incompleto

            if (self.name == 'MOON' and self.uranium <= 75 and self.fuel <= 70):
                globals.moon_ask_lion_launch.release() # Lua solicita recurso
                globals.acquire_print()
                print('Lua solicita lançamento de foguete LION')
                globals.release_print()

            # Se !MOON,coleta recurso das minas
            else:
                self.refuel_oil()
                self.refuel_uranium()

            # Constrói foguete se base não cheia
            if len(self.rockets <= self.constraints[2]):

                

                # TODO Construir lion se MOON precisa de recursos
                if (globals.moon_ask_lion_launch.acquire(blocking=False) and self.uranium >= 75 and self.fuel >= 235): # TODO mudar condicional para fuel 100
                    globals.acquire_print()
                    print(f'{self.name}: Construindo foguete LION')
                    globals.release_print()
                    self.base_rocket_resources('LION')

                # TODO Construir DRAGON ou FALCON
                else:
                    self.base_rocket_resources(choice(random_rockets))

            # TODO instanciar um foguete, colocar na lista da base
            # TODO: tentar lançar foguete chamando Rocket.launch

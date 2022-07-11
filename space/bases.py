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

    def build_rocket(self, rocket_name):
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
            
            case 'FALCON':
                if self.uranium > 35 and self.fuel > 90:
                    self.uranium = self.uranium - 35
                    if self.name == 'ALCANTARA':
                        self.fuel = self.fuel - 100
                    elif self.name == 'MOON':
                        self.fuel = self.fuel - 90
                    else:
                        self.fuel = self.fuel - 120
                 
            case 'LION':
                if self.uranium > 35 and self.fuel > 100:
                    self.uranium = self.uranium - 35
                    if self.name == 'ALCANTARA':
                        self.fuel = self.fuel - 100
                    else:
                        self.fuel = self.fuel - 115
                  
            case _:
                print("Invalid rocket name")
                return
        # Constrói foguete
        rocket = Rocket(rocket_name)
        # Adiciona foguete ao armazenamento da base
        self.rockets.append(rocket)
        globals.acquire_print()
        print(f'{self.name}: Construindo foguete {rocket}')
        globals.release_print()

    def refuel_oil():
        with globals.pipeline_consumidor:
            with globals.pipeline_units:

                globals.get_mines_ref()['oil_earth'].unities -= 5

            pass

    def refuel_uranium():
        pass

    def can_i_build_the_rocket(self,choiced):
        match self.name:
            case 'MOON':
                if choiced == 'DRAGON' and self.fuel < 50:
                    return
                elif choiced == 'FALCON' and self.fuel < 90:
                    return
                
            
            case 'ALCANTARA':
                if choiced == 'DRAGON' and self.fuel < 70:
                    return False
                elif choiced == 'FALCON' and self.fuel < 100:
                    return False
                
            
            case 'CANAVERAL CAPE':
                if choiced == 'DRAGON' and self.fuel < 100:
                    return False
                elif choiced == 'FALCON' and self.fuel < 120:
                    return False
                

            case 'MOSCOW':
                if choiced == 'DRAGON' and self.fuel < 100:
                    return False
                elif choiced == 'FALCON' and self.fuel < 120:
                    return False
                
        
        return TRUE


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

            if (self.name == 'MOON' and self.uranium <= 75 and self.fuel <= 70): # TODO determinar numero de fuel
                # TODO Lua pode pedir foguetes consecutivos !!ALTERAR                
                if globals.alredy_asked == True:
                    globals.moon_ask_lion_launch.release() # Lua solicita recurso
                    globals.acquire_print()
                    print('Lua solicita lançamento de foguete LION')
                    globals.release_print()
                if (len(self.rockets) == 0):
                    globals.moon_wait.wait()
                    globals.alredy_asked == False

            # Se !MOON,coleta recurso das minas
            else:
                self.refuel_oil()
                self.refuel_uranium()

            # Constrói foguete se base não cheia
            if len(self.rockets <= self.constraints[2]):

                # TODO Construir lion se MOON precisa de recursos
                if (globals.moon_ask_lion_launch.acquire(blocking=False) and self.uranium >= 75 and self.fuel >= 235): # TODO mudar condicional para fuel 100
                    self.build_rocket('LION')

                # TODO Construir DRAGON ou FALCON
                else:
                    if (self.uranium >= 35):
                        choiced = choice(random_rockets)
                        if (self.can_i_build_the_rocket(choiced)):
                            self.build_rocket(choiced)


                # TODO planing_launch
                    

            # TODO: tentar lançar foguete chamando Rocket.launch

            


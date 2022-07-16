from pickle import FALSE, TRUE
import globals
from threading import Thread, Lock, Semaphore
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
        print(f"🔭 - [{self.name}] - ☢ {self.uranium}/{self.constraints[0]} URANIUM  ⛽ {self.fuel}/{self.constraints[1]}  🚀 {len(self.rockets)}/{self.constraints[2]}")

    '''def build_rocket(self, rocket_name):
        match rocket_name:
            case 'DRAGON':
                #if self.uranium > 35 and self.fuel > 50:
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
        globals.release_print()'''  # TODO Depois eu vejo oq vou fazer com essa merda

    def refuel_oil(self):
        # Têm espaço para uma carga de oil?
        if self.fuel <= self.constraints[1] - globals.oil_units:
            # TODO, Será que fica mais eficiente?, Se tiver mais a disposição, pegue mais!
            # Existe oil disponível? Se não, tenho trabalho a fazer
            if globals.available_oil.acquire(blocking=False):
                # Existe oil disponível! Aguarda para receber
                with globals.pipeline_units:
                    # * Decrementa em oil_units self.unities
                    globals.get_mines_ref().get('oil_earth').unities -= globals.oil_units
                    globals.oil_loads - 1  # * Decrementa em 1 globals.oil_loads
                self.fuel += globals.oil_units
                globals.acquire_print()
                print(f'🔭 - [{self.name}] → refuel: {self.fuel} ⛽')
                globals.release_print()

    def refuel_uranium(self):
        # Têm espaço para uma carga de urânio?
        if self.uranium < self.constraints[0] - globals.uranium_units:
            # TODO, Será que fica mais eficiente?, Se tiver mais a disposição, pegue mais!
            # Existe urânio disponível? Se não, tenho trabalho a fazer
            if globals.available_uranium.acquire(blocking=False):
                # Existe urânio disponível! Aguarda para receber
                with globals.store_house_units:
                    # * Decrementa em uranium_units self.unities
                    globals.get_mines_ref().get(
                        'uranium_earth').unities -= globals.uranium_units
                    globals.uranium_loads - 1  # * Decrementa em 1 globals.uranium_loads
                self.uranium += globals.uranium_units
                globals.acquire_print()
                print(f'🔭 - [{self.name}] → refuel: {self.uranium} ☢')
                globals.release_print()

    def try_to_build_rocket(self, choiced_rocket):

        if self.name == 'MOON':
            if (choiced_rocket == 'DRAGON' and self.fuel >= 50) or (choiced_rocket == 'FALCON' and self.fuel >= 90):
                # Constrói foguete
                rocket = Rocket(choiced_rocket)
                with globals.moon_constraints: # Impede corrida na leitura e escrita dos recursos da lua
                    if choiced_rocket == 'DRAGON':
                        
                        self.fuel -= 50
                    else:
                        self.fuel -= 90
                    self.uranium -= 35

                # Adiciona foguete ao armazenamento da base
                self.rockets.append(rocket)
                globals.acquire_print()
                print(f'🔭 - [{self.name}]: Building {choiced_rocket} rocket')
                globals.release_print()

        elif self.name == 'ALCANTARA':
            if (choiced_rocket == 'DRAGON' and self.fuel >= 70) or (choiced_rocket == 'FALCON' and self.fuel >= 100) or (choiced_rocket == 'LION'):
                # Constrói foguete
                rocket = Rocket(choiced_rocket)

                if choiced_rocket == 'DRAGON':
                    self.fuel -= 70
                    self.uranium -= 35

                elif choiced_rocket == 'FALCON':
                    self.fuel -= 100
                    self.uranium -= 35

                else:
                    refuel = 30000 - globals.get_bases_ref().get['MOON'].fuel
                    if refuel >= 120:
                        refuel = 120
                    self.uranium -= 75
                    self.fuel -= refuel
                    rocket.uranium_cargo += 75
                    rocket.fuel_cargo += refuel

                # Adiciona foguete ao armazenamento da base
                self.rockets.append(rocket)
                globals.acquire_print()
                print(f'{self.name}: Building {choiced_rocket} rocket')
                globals.release_print()

        else:
            if (choiced_rocket == 'DRAGON' and self.fuel >= 100) or (choiced_rocket == 'FALCON' and self.fuel >= 120) or (choiced_rocket == 'LION'):
                # Constrói foguete
                rocket = Rocket(choiced_rocket)

                if choiced_rocket == 'DRAGON':
                    self.fuel -= 100
                    self.uranium -= 35

                elif choiced_rocket == 'FALCON':
                    self.fuel -= 120
                    self.uranium -= 35

                else:
                    refuel = 30000 - globals.get_bases_ref().get['MOON'].fuel
                    if refuel >= 120:
                        refuel = 120
                    self.uranium -= 75
                    self.fuel -= refuel
                    rocket.uranium_cargo += 75
                    rocket.fuel_cargo += refuel

                # Adiciona foguete ao armazenamento da base
                self.rockets.append(rocket)
                globals.acquire_print()
                print(f'{self.name}: Building {choiced_rocket} rocket')
                globals.release_print()

    def run(self):

        self.rockets = []
        random_rockets = ['DRAGON', 'FALCON']

        while(True):
            globals.acquire_print()
            self.print_space_base_info()
            globals.release_print()

            if (globals.get_release_system()):
                break  # finaliza a thread

            # Se MOON, verificar se precisa de recurso
            if (self.name == 'MOON' and self.uranium <= 75):

                if globals.alredy_asked == False:
                    globals.acquire_print()
                    print(f'🔭 - [MOON] → request LION rocket launch ')
                    globals.release_print()
                    globals.alredy_asked = True  # Seta true para não pedir foguetes caso já tenha pedido
                    globals.moon_ask_lion_launch.release()  # Lua solicita recurso

                # TODO usar lock_lion_launch em um # if (lock_lion_launch.locked) #  para determinar se lua precisa de notify do foguete
                globals.lock_lion_launch.acquire() # impede deadlock na lua e é condição para foguete dar notify para lua
                # Se não tem foguetes para lançar e recursos para construir mais, aguarda recursos chegarem
                if (len(self.rockets) == 0 and self.uranium < 35 and globals.alredy_asked == True):
                    with globals.need_notify:
                        globals.moon_wait.wait()
                    # TODO Foguete deve realizar # globals.alredy_asked == False # após chegar na lua

                globals.lock_lion_launch.release()

            # Se !MOON,coleta recurso das minas
            else:
                self.refuel_oil()
                self.refuel_uranium()

            # Constrói foguete se base não cheia e tem recursos para construir
            if len(self.rockets) < self.constraints[2]:

                # TODO Construir lion se MOON precisa de recursos
                if (globals.moon_ask_lion_launch.acquire(blocking=False) and self.uranium >= 75 and self.fuel >= 235):
                    self.try_to_build_rocket('LION')

                # Construir DRAGON ou FALCON
                if (self.uranium >= 35):
                    choiced_rocket = choice(random_rockets)
                    self.try_to_build_rocket(choiced_rocket)

            # TODO lógica de lançaento de foguetes incompleta
            # decidir qual foguete lançar
            if (len(self.rockets) > 0):
                # checa se tem foguete lion armazenado
                launch_lion = False
                for x in range(len(self.rockets)):
                    if self.rockets[x] == 'LION':
                        launch_lion = True
                        lion = self.rockets.pop(x)
                        break

                if (launch_lion == True):
                    
                    globals.acquire_print()
                    print(f'🔭 - [{self.name}] → launching LION rocket')
                    globals.release_print()
                    rocket = Thread(target=lion.launch_lion)
                    launch_lion = False
                    rocket.start()

                else:
                    choiced_to_launch = choice(self.rockets)
                    self.rockets.remove(choiced_to_launch)
                    globals.acquire_print()
                    print(
                        f'🔭 - [{self.name}] → launching {choiced_to_launch.name} rocket')
                    globals.release_print()
                    # TODO Chamar função de definição de destino
                    # TODO Criar thread do foguete em bases
                    # TODO Chamar função de lançamento

                # destination = choiced_to_launch.planning_launch()  # qual planeta
                # rocket_thread = Thread(name=self.id)
                # rocket_thread.start(target=self.launch)  # Inicializa a thread

                # TODO: tentar lançar foguete chamando Rocket.launch

        globals.acquire_print()
        print(f'Thread da base {self.name} finalizada')
        globals.release_print()

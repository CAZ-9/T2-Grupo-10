from threading import Thread, Condition, Semaphore, active_count
from time import sleep
import globals


class Planet(Thread):

    ################################################
    # O CONSTRUTOR DA CLASSE NÃO PODE SER ALTERADO #
    ################################################
    def __init__(self, terraform, name):
        Thread.__init__(self)
        self.terraform = terraform
        self.name = name

    def nuke_detected(self):
        planet_condition = globals.nuclear_event_condition.get(self.name)
        
        while(self.satellite_get_info() > 0):
            '''before_percentage = self.terraform
            while(before_percentage == self.terraform):
                pass'''
                #!
            with planet_condition:
                planet_condition.wait() # Impede busywaiting nos planetas
                 
            globals.acquire_print()
            print(f"🪐 - [NUKE DETECTION] - The planet {self.name} was bombed. {self.terraform}% UNHABITABLE")
            globals.release_print()

    def print_planet_info(self):
        print(f"🪐 - [{self.name}] → {self.terraform}% UNINHABITABLE")

    def satellite_get_info(self):  # * Limitação da tecnologia, um acesso por vez
        with globals.satellite_lock.get(self.name):
            info = self.terraform
        return info

    def planet_takes_damage(self, damage):
        '''Decrementa a vida do planeta'''
        # TODO proteger variável self.terraform
        #! self.terraform é uma região crítica? Se for deve ser protegido aqui e em satélite
        with globals.satellite_lock.get(self.name):
            self.terraform = self.terraform - damage

    def run(self):
        globals.acquire_print()
        self.print_planet_info()
        globals.release_print()
        #! Dar aquire nos locks antes
        # Quando iniciar a execução, da aquire no lock da condition
        # globals.nuclear_event.get(self.name).acquire()

        while(globals.get_release_system() == False):
            pass

        while(True):
            # TODO quando essa thread fica em wait, a velocidade dos prints aumenta muito!
            #! por ficar ociosa acho que está fazendo bases rodar em loop

            # * Aguarda o notify de rockets.nuke()
            # Por estar comentada recebemos o erro de cant notify an unaquired lock
            # TODO descomentar abaixo, e refletir se vale mesmo a pena acabar com o busy wait de todos os planetas
            # globals.nuclear_event_condition.get(self.name).wait()
            self.nuke_detected()       # Printa após atualizar satellite
            
            break 
        
        globals.colision_course.get(self.name).release(10)
        planets = globals.get_planets_ref()    
        
        time = globals.get_simulation_time().simulation_time()
        
        globals.acquire_print()
        print(f'🪐 - [{self.name}] - Terraform completed in {time} years')
        globals.release_print()
        
        if (planets.get('mars').satellite_get_info() < 0 and planets.get('io').satellite_get_info() < 0
            and planets.get('ganimedes').satellite_get_info() < 0 and planets.get('europa').satellite_get_info() < 0):
            globals.finalize_threads = True
            globals.no_more_busywating.release(4)
            with globals.moon_wait:
                globals.moon_wait.notify()
            globals.acquire_print()
            print(f'\033[1;31mAll planets terraformed in {time} years\033[m')
            globals.release_print()
            print('\033[1;31mFINALIZOU CARALHO\033[m🚀🎇🚀🎇🚀🎇🚀🎇🚀🎇🚀🎇🚀🎇')
        
                
            
            
                
            

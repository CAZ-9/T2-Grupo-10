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
        '''Aguarda detecção de nuke enquanto o planeta for inabitável. Quando há detecção, imprime self.terraform'''
        
        planet_condition = globals.nuclear_event_condition.get(self.name)
        
        # Verifica se self.terraform > 0
        while(self.satellite_get_info() > 0):
            
            with planet_condition:
                planet_condition.wait() # Impede busywaiting nos planetas
                 
            globals.acquire_print()
            print(f"🪐 - [NUKE DETECTION] - The planet {self.name} was bombed. {self.terraform}% UNHABITABLE")
            globals.release_print()

    def print_planet_info(self):
        print(f"🪐 - [{self.name}] → {self.terraform}% UNINHABITABLE")

    def satellite_get_info(self):
        
        '''Limitação da tecnologia, um acesso por vez'''
        
        with globals.satellite_lock.get(self.name):
            info = self.terraform
        return info

    def planet_takes_damage(self, damage):
        '''Decrementa a vida do planeta'''
      
        with globals.satellite_lock.get(self.name):
            self.terraform = self.terraform - damage

    def run(self):
        globals.acquire_print()
        self.print_planet_info()
        globals.release_print()

        while(globals.get_release_system() == False):
            pass

        while(True):
            
            self.nuke_detected() # Fica em laço até o planeta ser terraformado
            break 
        
        globals.colision_course.get(self.name).release(10) # Deixa threads de foguetes presos no semaforo finalizarem
        
        planets = globals.get_planets_ref()    
        time = globals.get_simulation_time().simulation_time()
        
        globals.acquire_print()
        print(f'\033[1;34m🪐 - [{self.name}] - Terraform completed in {time} years!\033[m')
        globals.release_print()
        
        # Verifica se todos planetas foram terraformados
        if (planets.get('mars').satellite_get_info() < 0 and planets.get('io').satellite_get_info() < 0
            and planets.get('ganimedes').satellite_get_info() < 0 and planets.get('europa').satellite_get_info() < 0):
            
            globals.finalize_threads = True # Seta True para finalizar bases, time e mines
                
            while active_count() > 2: # Se existem além de MainThread e a última thread planeta ativa
                with globals.stop_bases:
                    globals.stop_bases.notify_all() # Garante que bases vão finalizar
                with globals.moon_wait:
                    globals.moon_wait.notify() # Garante que lua vai finalizar
                sleep(1)
            
            globals.acquire_print()
            print(f'\n\033[1;32mAll planets terraformed in {time} years!!\033[m\n')
            globals.release_print()
            
        
                
            
            
                
            

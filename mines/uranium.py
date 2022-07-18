from threading import Thread
from random import randint
from time import sleep

import globals


######################################################################
#                                                                    #
#              Não é permitida a alteração deste arquivo!            #
#                                                                    #
######################################################################

class StoreHouse(Thread):

    def __init__(self, unities, location, constraint):
        Thread.__init__(self)
        self.unities = unities  # ! Região crítica, podemos ter valores errados
        self.location = location
        self.constraint = constraint

    def print_store_house(self):
        print(f"🔨 - [{self.location}] → {self.unities} uranium unities are produced ☢ .")

    def produce(self):
        with globals.store_house_units:  # Protege acesso a SoreHouse.units !! Região cŕitica !!
            if(self.unities < self.constraint):
                self.unities += 15
                self.print_store_house()
        globals.available_uranium.release() # Incrementa para bases saberem que podem pegar uma porção de urânio

        sleep(0.001)

    def run(self):

        while(globals.get_release_system() == False):
            pass
        
        while(True):
            self.produce()
            if globals.finalize_threads == True:
                break    

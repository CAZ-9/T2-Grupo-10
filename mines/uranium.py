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
        with globals.store_house_units:  # Acesso a store_house_units
            if(self.unities < self.constraint):
                self.unities += 15
                self.print_store_house()
        globals.available_uranium.release()

                #   Libera para as bases receberem recurso apenas quando o recurso está disponível
                #   globals.delivery_control(  # TODO: Testar delivery_control()
                #   self.unities, globals.uranium_units, globals.uranium_loads, globals.available_uranium)'''
        sleep(0.001)

        # TODO: apagar pós teste de delivery_control()
        # * # Faz a divisão inteira, "x" uranium_units
        # * cargas_atuais = self.unities // uranium_units
        # * # Tenho um número de cargas igual ou maior que antes?
        # * if cargas_atuais >= globals.uranium_loads:
        # *     n = cargas_atuais - globals.uranium_loads   # Diferença entre as cargas
        # *     globals.uranium_loads += n                  # incremento minhas cargas
        # *     #! É nescessário decrementar esse valor a cada x_loads removidos
        # *     globals.available_uranium.release(n)        # Tenho n cargas disponíveis!

    def run(self):

        while(globals.get_release_system() == False):
            pass
        
        while(True):

            self.produce()

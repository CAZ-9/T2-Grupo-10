from threading import Thread
from time import sleep

import globals


######################################################################
#                                                                    #
#              Não é permitida a alteração deste arquivo!            #
#                                                                    #
######################################################################

class Pipeline(Thread):

    def __init__(self, unities, location, constraint):
        Thread.__init__(self)
        self.unities = unities  # ! Região crítica, podemos ter valores errados
        self.location = location
        self.constraint = constraint

    def print_pipeline(self):
        print(f"🔨 - [{self.location}] → {self.unities} oil unities are produced ⛽ ")

    def produce(self):
        
        with globals.pipeline_units:  # Protege acesso a Pipeline.units !! Região crítica !!
            if(self.unities < self.constraint):
                self.unities += 17
                self.print_pipeline()
        globals.available_oil.release() # Incrementa para bases saberem que podem pegar uma porção de óleo

        sleep(0.001)

    def run(self):

        while(globals.get_release_system() == False):
            pass
        
        while(True):
            self.produce()
            if globals.finalize_threads == True:
                break    
        

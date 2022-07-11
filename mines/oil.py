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
        print(
            f"🔨 - [{self.location}] - {self.unities} oil unities are produced."
        )

    def produce(self):
        with globals.pipeline_units:  # Acesso a pipeline_units
            if(self.unities < self.constraint):
                self.unities += 17
                self.print_pipeline()
                # Faz a divisão inteira, para saber quantos poderão abastecer
                n = 17//globals.oil.units  # ! a cada 5 carregamentos +2 deverão acontecer
                globals.oil_avaliable.release(n)  # ! Espero um value error

        sleep(0.001)

    def run(self):
        globals.acquire_print()
        self.print_pipeline()
        globals.release_print()

        while(True):
            if (globals.get_release_system()):
                return  # finaliza a thread
            self.produce()

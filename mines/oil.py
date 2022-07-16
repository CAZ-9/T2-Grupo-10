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
            f"🔨 - [{self.location}] → {self.unities} oil unities are produced ⛽ ."
        )

    def produce(self):
        with globals.pipeline_units:  # Acesso a pipeline_units
            if(self.unities < self.constraint):
                self.unities += 17
                self.print_pipeline()

                # Libera para as bases receberem recurso apenas quando o recurso está disponível
                globals.delivery_control(
                    self.unities, globals.oil_units, globals.oil_loads, globals.available_oil)
        sleep(0.001)

    def run(self):
        globals.acquire_print()
        self.print_pipeline()
        globals.release_print()

        while(True):
            if (globals.get_release_system()):
                break  # finaliza a thread
            self.produce()

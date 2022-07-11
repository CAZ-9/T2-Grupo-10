from random import randrange, random
from time import sleep
from threading import Thread, current_thread


class Rocket:

    ################################################
    # O CONSTRUTOR DA CLASSE NÃO PODE SER ALTERADO #
    ################################################
    def __init__(self, type):
        self.id = randrange(1000)
        self.name = type
        if(self.name == 'LION'):
            self.fuel_cargo = 0
            self.uranium_cargo = 0

    def nuke(self, planet):  # Permitida a alteração

        self.damage()
        print(
            f"[EXPLOSION] - The {self.name} ROCKET reached the planet {planet.name} on North Pole")
        print(
            f"[EXPLOSION] - The {self.name} ROCKET reached the planet {planet.name} on South Pole")
        # TODO   decrementar a vida do planeta respectivo
        pass

    def voyage(self, planet):  # Permitida a alteração (com ressalvas)

        # Essa chamada de código (do_we_have_a_problem e simulation_time_voyage) não pode ser retirada.
        # Você pode inserir código antes ou depois dela e deve
        # usar essa função.
        # TODO alterar lógica para dar notify pra lua se o foguete for lion
        # TODO lua deve estar em wait
        self.simulation_time_voyage(planet)     # Planeta está viajando
        failure = self.do_we_have_a_problem()   # Testa falha
        if failure == False:                    # Se não ouveuma falha
            self.nuke(planet)                   # Planeta é bombardeado

    ####################################################
    #                   ATENÇÃO                        #
    #     AS FUNÇÕES ABAIXO NÃO PODEM SER ALTERADAS    #
    ###################################################

    def simulation_time_voyage(self, planet):
        if planet.name == 'MARS':
            # Marte tem uma distância aproximada de dois anos do planeta Terra.
            sleep(2)
        else:
            # IO, Europa e Ganimedes tem uma distância aproximada de cinco anos do planeta Terra.
            sleep(5)

    def do_we_have_a_problem(self):
        if(random() < 0.15):
            if(random() < 0.51):
                self.general_failure()
                return True
            else:
                self.meteor_collision()
                return True
        return False

    def general_failure(self):
        print(f"[GENERAL FAILURE] - {self.name} ROCKET id: {self.id}")

    def meteor_collision(self):
        print(f"[METEOR COLLISION] - {self.name} ROCKET id: {self.id}")

    def successfull_launch(self, base):
        if random() <= 0.1:
            print(
                f"[LAUNCH FAILED] - {self.name} ROCKET id:{self.id} on {base.name}")
            return False
        return True

    def damage(self):
        return random()

    def launch(self, base, planet):

        # match planet:
        #   case ''

        # TODO semáforo n=2 locking=false para garantir que não serão 3 nukes no mesmo planeta
        #! três bombas ou mais não podem chegassem ao mesmo tempo
        #! mais de uma bomba não pode atingir o mesmo polo ao mesmo tempo

        if(self.successfull_launch(base)):
            print(f"[{self.name} - {self.id}] launched.")

            # * Cria thread do foguete com a função voyage

            rocket_thread = Thread(name=self.id, target=self.voyage(planet))

            rocket_thread.start()  # Inicializa a thread

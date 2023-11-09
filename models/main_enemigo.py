# Importa la clase Jugador
from models.player.main_player import Jugador


# Clase derivada Enemig


class Enemigo(Jugador):
    def __init__(self, coord_x, coord_y, speed_fly=6, *args, **kwargs):
        super().__init__(coord_x, coord_y, *args, **kwargs)

        # Defino un nuevo atributo rect para la clase Enemigo

        self.__puede_volar = True
        self.__speed_fly = speed_fly
        self.__tiempo_vuelo = 1000
        self.__tiempo_vuelo_actual = 0
        self.__speed_fly = speed_fly

    def volar(self):
        if self.__puede_volar:
            # Mueve al enemigo hacia arriba en el eje y durante el tiempo de vuelo
            self.__rect.y -= self.__speed_fly
            self.__tiempo_vuelo_actual += self.__frame_rate
            if self.__tiempo_vuelo_actual >= self.__tiempo_vuelo:
                self.__tiempo_vuelo_actual = 0
                self.__puede_volar = False

    def atacar(self):
        print("Enemigo atacando")

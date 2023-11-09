import pygame as pg

from models.auxiliar import SurfaceManager as sf

from models.constantes import ANCHO_VENTANA, DEBUG


class Jugador:
    # nota: velocidad de animación (frame_rate)..,y altura de salto (jump).
    def __init__(
        self,
        coord_x,
        coord_y,
        frame_rate=100,
        speed_walk=6,
        speed_run=12,
        gravity=16,
        jump=32,
    ):
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>ATRIBUTOS <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        self.__iddle_r = sf.get_surface_from_spritesheet(
            "./assets/img/player/iddle/player_idle.png", 5, 1
        )
        self.__iddle_l = sf.get_surface_from_spritesheet(
            "./assets/img/player/iddle/player_idle.png", 5, 1, flip=True
        )
        self.__walk_r = sf.get_surface_from_spritesheet(
            "./assets/img/player/walk/player_walk.png", 6, 1
        )
        self.__walk_l = sf.get_surface_from_spritesheet(
            "./assets/img/player/walk/player_walk.png", 6, 1, flip=True
        )
        self.__run_r = sf.get_surface_from_spritesheet(
            "./assets/img/player/run/player_run.png", 2, 1
        )
        self.__run_l = sf.get_surface_from_spritesheet(
            "./assets/img/player/run/player_run.png", 2, 1, flip=True
        )
        self.__jump_r = sf.get_surface_from_spritesheet(
            "./assets/img/player/jump/player_jump.png", 6, 1
        )
        self.__jump_l = sf.get_surface_from_spritesheet(
            "./assets/img/player/jump/player_jump.png", 6, 1, flip=True
        )
        # Se establece el estado inicial del jugador

        # Se inicializan las variables de posición horizontal (__move_x)  del jugador con las coordenadas iniciales.
        self.__move_x = coord_x
        self.__move_y = coord_y

        self.__speed_walk = speed_walk
        self.__speed_run = speed_run
        self.__frame_rate = frame_rate
        self.__player_move_time = 0
        self.__player_animation_time = 0
        self.__gravity = gravity
        self.__jump = jump
        self.__is_jumping = False
        self.__initial_frame = 0  # comienza desde el primer fotograma.
        self.__actual_animation = self.__iddle_r

        # guarda la imagen actual que se muestra en la pantalla. En este punto, es la primera imagen de la animación actual.
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]

        # Se crea un rectángulo (pygame.Rect) que rodea la imagen actual.
        # Este rectángulo se utilizará para controlar la posición y la colisión del jugador en el juego.
        self.__rect = self.__actual_img_animation.get_rect()
        self.__is_looking_right = True

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>METODOS <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # para gestionar el movimiento y la animación del jugador, se encargan de controlar el comportamiento
    # del personaje en el juego, incluyendo cómo se mueve y cómo se muestra en la pantalla.
    def __set_x_animations_preset(
        self, move_x, animation_list: list[pg.surface.Surface], look_r: bool
    ):
        """Recibe tres parámetros: move_x (la velocidad de movimiento horizontal),
        animation_list (una lista de superficies de animación) y
        look_r (un booleano que indica si el jugador está mirando hacia la derecha)."""
        self.__move_x = move_x
        self.__actual_animation = animation_list
        self.__is_looking_right = look_r

    def __set_y_animations_preset(self):
        """Este método se utiliza para configurar las animaciones cuando el jugador salta.
        No toma parámetros explícitos; utiliza las propiedades actuales del jugador.
        Establece self.__move_y a la velocidad de salto negativa, self.__move_x a
        la velocidad de ejecución en la dirección correcta (según la dirección actual),
        self.__actual_animation a la animación de salto en la dirección correcta, reinicia
        el fotograma inicial (self.__initial_frame) y establece self.__is_jumping en True.
        Esto configura el jugador para realizar un salto."""
        self.__move_y = (
            -self.__jump
        )  # Establece self.__move_y a la velocidad de salto negativo
        self.__move_x = (
            self.__speed_run if self.__is_looking_right else -self.__speed_run
        )
        self.__actual_animation = (
            self.__jump_r if self.__is_looking_right else self.__jump_l
        )
        self.__initial_frame = 0
        self.__is_jumping = True

    def walk(self, direction: str = "Right"):
        """Llama a __set_x_animations_preset con la velocidad de caminar adecuada y las animaciones
        de caminar correspondientes."""
        match direction:
            case "Right":
                look_right = True
                self.__set_x_animations_preset(
                    self.__speed_walk, self.__walk_r, look_r=look_right
                )
            case "Left":
                look_right = False
                self.__set_x_animations_preset(
                    -self.__speed_walk, self.__walk_l, look_r=look_right
                )

    def run(self, direction: str = "Right"):
        self.__initial_frame = 0
        match direction:
            case "Right":
                look_right = True
                self.__set_x_animations_preset(
                    self.__speed_run, self.__run_r, look_r=look_right
                )
            case "Left":
                look_right = False
                self.__set_x_animations_preset(
                    -self.__speed_run, self.__run_l, look_r=look_right
                )

    def stay(self):
        if (
            self.__actual_animation != self.__iddle_l
            and self.__actual_animation != self.__iddle_r
        ):
            self.__actual_animation = (
                self.__iddle_r if self.__is_looking_right else self.__iddle_l
            )  # verifica si la animación actual no es la animación de reposo en ambas direcciones (izquierda y derecha).
            self.__initial_frame = 0
            self.__move_x = 0
            self.__move_y = 0

    def jump(self, jumping=True):
        """Si jumping es True y el jugador no está saltando actualmente, se configura para saltar
        llamando a __set_y_animations_preset. Si jumping es False, el jugador se configura para no
        saltar y entrar en el estado de reposo."""
        if jumping and not self.__is_jumping:
            self.__set_y_animations_preset()
        else:
            self.__is_jumping = False
            self.stay()

    def __set_borders_limits(self):
        """Este método se utiliza para evitar que el jugador se salga de los límites de la pantalla.
        Calcula cuántos píxeles puede moverse en la dirección actual sin exceder los límites de la pantalla.
        Retorna: la cantidad de píxeles que puede moverse."""
        pixels_move = 0
        if self.__move_x > 0:
            pixels_move = (
                self.__move_x
                if self.__rect.x
                < ANCHO_VENTANA - self.__actual_img_animation.get_width()
                else 0
            )
        elif self.__move_x < 0:
            pixels_move = self.__move_x if self.__rect.x > 0 else 0
        return pixels_move

    def do_movement(self, delta_ms):
        """Este método se encarga de actualizar la posición del jugador en función del tiempo
        y las animaciones.
        Controla el movimiento horizontal del jugador y aplica la gravedad cuando está en el aire.
        """
        self.__player_move_time += delta_ms
        if self.__player_move_time >= self.__frame_rate:
            self.__player_move_time = 0
            self.__rect.x += self.__set_borders_limits()
            self.__rect.y += self.__move_y

            # Parte relacionado a saltar.
            # esta parte controla la gravedad y el salto del jugador.
            # Si la posición vertical del jugador es menor que 300
            # (lo que significa que está en el aire), se le aplica la gravedad
            # sumando self.__gravity a su posición vertical. Esto hace que el jugador caiga hacia abajo.
            if self.__rect.y < 300:
                self.__rect.y += self.__gravity

    def do_animation(self, delta_ms):
        self.__player_animation_time += delta_ms
        if self.__player_animation_time >= self.__frame_rate:
            self.__player_animation_time = 0
            if self.__initial_frame < len(self.__actual_animation) - 1:
                self.__initial_frame += 1
            else:
                self.__initial_frame = 0
                # if self.__is_jumping:
                #     self.__is_jumping = False
                #     self.__move_y = 0

    def update(self, delta_ms):
        """Este método se utiliza para actualizar el estado del jugador.
        Llama a do_movement y do_animation con el tiempo transcurrido (delta_ms) para actualizar
        la posición y la animación."""
        self.do_movement(delta_ms)
        self.do_animation(delta_ms)

    def draw(self, screen: pg.surface.Surface):
        if DEBUG:
            """Este método se utiliza para dibujar al jugador en la pantalla.
            Si DEBUG es True, dibuja un rectángulo rojo alrededor del jugador.
            Establece la imagen de animación actual y la dibuja en la pantalla."""
            pg.draw.rect(screen, "red", self.__rect)
            # pg.draw.rect(screen, 'green', self.__rect.bottom)
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        screen.blit(self.__actual_img_animation, self.__rect)

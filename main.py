import pygame as pg
from models.main_enemigo import (
    Enemigo,
)  # Asegúrate de tener una clase Enemigo en el archivo models/enemigo.py

from models.constantes import ALTO_VENTANA, ANCHO_VENTANA, FPS
from models.player.main_player import Jugador

screen = pg.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pg.init()
clock = pg.time.Clock()

back_img = pg.image.load("./assets/img/background/goku_house.png")
back_img = pg.transform.scale(back_img, (ANCHO_VENTANA, ALTO_VENTANA))


juego_ejecutandose = True

vegeta = Jugador(0, 0, frame_rate=70, speed_walk=20, speed_run=40)
enemigo = Enemigo(
    0, 2, frame_rate=70, speed_fly=6
)  # Ajusta las coordenadas según tu diseño

# Resto de tu código...  # Ajusta las coordenadas iniciales según tu diseño

# FPS significa "Frames Per Second" (cuadros por segundo) y se refiere a la cantidad
# de imágenes individuales (cuadros) que se muestran en una pantalla en un segundo.

# velocidad de fotogramas (frame rate)
while juego_ejecutandose:
    # print(delta_ms)
    lista_eventos = pg.event.get()
    for event in lista_eventos:
        match event.type:
            case pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    vegeta.jump(True)
            # case pg.KEYUP:
            #     if event.key == pg.K_SPACE:
            #         print('Estoy SOLTANDO el espacio')

            #
            case pg.QUIT:
                print("Estoy CERRANDO el JUEGO")
                juego_ejecutandose = False
                break
    # pg.key.get_pressed() devuelve una lista de booleanos que repr el estado de todas las teclas del teclado.
    lista_teclas_presionadas = pg.key.get_pressed()

    # Esta línea verifica si la tecla de la flecha derecha (pg.K_RIGHT) está siendo presionada y
    # la tecla de la flecha izquierda (pg.K_LEFT) no lo está al mismo tiempo.
    # Esto significa que el jugador está presionando la tecla de flecha derecha.
    if lista_teclas_presionadas[pg.K_RIGHT] and not lista_teclas_presionadas[pg.K_LEFT]:
        vegeta.walk("Right")
    if lista_teclas_presionadas[pg.K_LEFT] and not lista_teclas_presionadas[pg.K_RIGHT]:
        vegeta.walk("Left")
    if (
        not lista_teclas_presionadas[pg.K_RIGHT]
        and not lista_teclas_presionadas[pg.K_LEFT]
    ):
        vegeta.stay()
    # (pg.K_LSHIFT):tecla de mayúsculas izquierda  está siendo presionada.
    if (
        lista_teclas_presionadas[pg.K_RIGHT]
        and lista_teclas_presionadas[pg.K_LSHIFT]
        and not lista_teclas_presionadas[pg.K_LEFT]
    ):
        vegeta.run("Right")
    if (
        lista_teclas_presionadas[pg.K_LEFT]
        and lista_teclas_presionadas[pg.K_LSHIFT]
        and not lista_teclas_presionadas[pg.K_RIGHT]
    ):
        vegeta.run("Left")

    if lista_teclas_presionadas[pg.K_LSHIFT]:
        enemigo.volar()
    # En el bucle principal del juego:

    screen.blit(back_img, back_img.get_rect())
    delta_ms = clock.tick(FPS)
    vegeta.update(delta_ms)
    vegeta.draw(screen)
    # Enemigo
    enemigo.update(delta_ms)
    enemigo.draw(screen)

    pg.display.update()

pg.quit()

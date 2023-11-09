import pygame as pg


# modulo auxiliar.py
class SurfaceManager:
    """Se define una clase llamada SurfaceManager, que contendrá métodos
    para administrar superficies y cargar sprites desde hojas de sprites."""

    @staticmethod
    # obtener surface desde hoja de sprites
    def get_surface_from_spritesheet(
        img_path: str, cols: int, rows: int, step=1, flip: bool = False
    ) -> list[pg.surface.Surface]:
        # se crea la lista para almacenar las superficies individuales.
        sprites_list = list()

        # Se carga la hoja de sprites desde el archivo especificado en img_path
        surface_img = pg.image.load(img_path)

        # Se calcula el ancho y el alto de cada cuadro individual en la hoja de sprites
        # dividiendo el ancho y el alto totales de la hoja por el número de columnas y filas,
        # respectivamente.
        frame_width = int(surface_img.get_width() / cols)
        frame_height = int(surface_img.get_height() / rows)

        for row in range(rows):
            for column in range(0, cols, step):
                x_axis = column * frame_width
                y_axis = row * frame_height

                # Se recorta una superficie individual del cuadro actual utilizando surface_img.subsurface().
                frame_surface = surface_img.subsurface(
                    x_axis, y_axis, frame_width, frame_height
                )

                if flip:
                    # Si el parámetro flip es True, la superficie se voltea horizontalmente utilizando pg.transform.flip()
                    frame_surface = pg.transform.flip(frame_surface, True, False)
                    # La superficie recién creada se agrega a la lista sprites_list.
                sprites_list.append(frame_surface)
        return sprites_list

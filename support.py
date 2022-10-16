from os import walk
import os
import pygame

def import_folder(path):
    surface_list = []
    for _, _, img_files in walk(path):
        for image in sorted(img_files):
            full_path = path + "/" + image
            # print(full_path)
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list

def lerp(a: float, b: float, t: float) -> float:
    """Linear interpolate on the scale given by a to b, using t as the point on that scale.
    Examples
    --------
        50 == lerp(0, 100, 0.5)
        4.2 == lerp(1, 5, 0.8)
    """
    return (1 - t) * a + t * b


def inv_lerp(a: float, b: float, v: float) -> float:
    """Inverse Linar Interpolation, get the fraction between a and b on which v resides.
    Examples
    --------
        0.5 == inv_lerp(0, 100, 50)
        0.8 == inv_lerp(1, 5, 4.2)
    """
    return (v - a) / (b - a)

def move_towards(a: float, b:float, step:float, margin:float):
    """_summary_
        increment first vaue toward second value by given step
    Args:
        a (float): move from this value
        b (float): toward this value
        step (float): by this step
    """
    if abs(a-b) < margin:
        return b
    if a < b:
        a += step
    elif a > b:
        a -= step
    else:
        return a

    return a
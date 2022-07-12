
from multiprocessing.connection import wait
import pygame as pg
from pygame.locals import *
import os
from time import sleep

main_dir = os.path.split(os.path.abspath(__file__))[0]
main_dir = os.path.abspath(os.path.join(main_dir, '..'))


def load_image(file):
    """loads an image, prepares it for play"""
    file = os.path.join(main_dir, "data", file)
    try:
        surface = pg.image.load(file)
        surface = scale(surface, 0.8)
        pg.Surface.set_colorkey(surface, [0,0,0])
    except pg.error:
        raise SystemExit('Could not load image "%s" %s' % (file, pg.get_error()))
    return surface.convert()

def load_character(img1, num):
    nv=[]
    base=str(os.path.basename(img1))
    file=base.split('.')
    width=[]
    height=[]

    for i in range(1,num+1):
        file_name = os.path.join(main_dir, "data", file[0][:-1]+str(i)+'.'+file[1])
        nv.append(load_image(file_name))
        pg.Surface.set_colorkey (nv[-1], [0,0,0])
    return nv

def scale(surface,scale_in):
    x=surface.get_width()
    y=surface.get_height()
    surface = pg.transform.scale(surface, (x*scale_in, y*scale_in))
    return surface


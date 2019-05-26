import pygame as pg
from numpy import complex, array
import colorsys
from numpy import interp

width = 400
zoomSpeed = 1
height = int(width/2)
zoom = 1
xMove = width
yMove = height
iterations = 10
def rgb_conv(i):
    color = 255 * array(colorsys.hsv_to_rgb(i / 255.0, 1.0, 1.0))
    return tuple(color.astype(int))
def mandelbrot(x,y):
    c0 = complex((x-width+xMove), (y-height+yMove)) / zoom
    c = 0
    for i in range(170, 170 + iterations):
        if abs(c) > 2:
            return rgb_conv(i)
        c = c * c + c0
    return (0, 0, 0)

pg.init()
canvas = pg.display.set_mode((width, height))

def reRender():
    #print('zoom: ', zoom)
    for y in range(height):
        for x in range(width):
            color = mandelbrot((x - (0.75 * width)) / (width / 4), (y - (width / 4)) / (width / 4))
            canvas.set_at((x, y), color)
reRender()
while True:
    ev = pg.event.poll()
    if ev.type == pg.QUIT:
        break
    if pg.mouse.get_pressed()[0]:
        endPos = pg.mouse.get_pos()
        startPos = [width/2,height/2]
        xToMid = (endPos[0] - startPos[0])
        xMove += interp(xToMid, [-width/2,width/2], [-2,2])

        yToMid = (endPos[1] - startPos[1])
        yMove += interp(yToMid, [-height/2,height/2], [-1,1])
        reRender()
    elif ev.type == pg.MOUSEBUTTONDOWN:
        if ev.button == 4:
            zoom += zoomSpeed
            reRender()
        elif ev.button == 5:
            if zoom <= 1:
                zoom -= zoomSpeed / 5
            else:
                zoom -= zoomSpeed
            reRender()
    pg.draw.rect(canvas, (0,255,0), (width/2,1,1,height))
    pg.draw.rect(canvas, (0,255,0), (1,height/2,width,1))
    pg.display.flip()
pg.quit()

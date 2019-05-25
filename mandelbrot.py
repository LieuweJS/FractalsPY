import pygame as pg
import colorsys

from numpy import complex, array, interp


width = 400
height = int(width/2)
zoom = 1
xMove = width
yMove = height
prevPressed = 0
pressStarted = 0
iterations = 60

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
update = 1

while True:
    ev = pg.event.poll()
    if ev.type == pg.QUIT:
        break
    if update == 1:
        for x in range(width):
            for y in range(height):
                color = mandelbrot((x - (0.75 * width)) / (width / 4), (y - (width / 4)) / (width / 4))
                canvas.set_at((x, y), color)
        update = 0
    if pg.mouse.get_pressed()[0]:
        if not pressStarted == 1:
            pressStarted = 1
            startPos = pg.mouse.get_pos()
    elif not pg.mouse.get_pressed()[0] and pressStarted == 1:
        prevPressed = 0
        pressStarted = 0
        endPos = pg.mouse.get_pos()
        zoom = 1#height/(abs(startPos[1] - endPos[1]))
        xTemp = (endPos[0] - startPos[0])/2
        xToMid = (endPos[0] - xTemp) - (width/2)
        xMove += interp(xToMid, [-width/2,width/2], [-2,2])

        yTemp = (endPos[1] - startPos[1])/2
        yToMid = (endPos[1] - yTemp) - (height/2)
        yMove += interp(yToMid, [-height/2,height/2], [-1,1])
        update = 1
    pg.draw.rect(canvas, (0,255,0), (width/2,1,1,height))
    pg.draw.rect(canvas, (0,255,0), (1,height/2,width,1))
    pg.display.flip()
pg.quit()

import pygame as pg
from numpy import complex, array
import colorsys
from numpy import interp

width = 500
height = 250
zoom = 1
xMove = width
yMove = height
prevPressed = 0
pressStarted = 0

def rgb_conv(i):
    color = 255 * array(colorsys.hsv_to_rgb(i / 255.0, 1.0, 1.0))
    return tuple(color.astype(int))
def mandelbrot(x,y):
    c0 = complex((x-width+xMove), (y-height+yMove)) / zoom
    c = 0
    for i in range(170, 210):
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
        if endPos[0] > startPos[0]:
            #from left to right
            #works
            xTemp = (endPos[0] - startPos[0])/2
            xToMid = (endPos[0] - xTemp) - (width/2)
            xMove += interp(xToMid, [0,width], [0,4])
        else:
            #from right to left
            xTemp = (endPos[0] - startPos[0])/2
            #xToMid = ((width/2) - xTemp)
            xMove -= interp(xToMid, [0,width], [0,4])
        if endPos[1] > startPos[1]:
            #2
            yTemp = (endPos[1] - startPos[1])/2
            yMove += interp(yTemp, [0,height], [0,2])
        else:
            yTemp = (startPos[1] - endPos[1])/2
            yMove -= interp(yTemp,[0,height],[0,2])
        print(startPos[0])
        print(endPos[0])
        print(xTemp)
        print(xToMid)
        update = 1
    if False:
        if pressed[pg.K_UP]:
            yMove -= 0.5
            update = 1
        elif pressed[pg.K_DOWN]:
            yMove += 0.5
            update = 1
        elif pressed[pg.K_LEFT]:
            xMove -= 0.5
            update = 1
        elif pressed[pg.K_RIGHT]:
            xMove += 0.5
            update = 1
        elif pressed[pg.K_EQUALS]:
            zoom += 1
            update = 1
        elif pressed[pg.K_MINUS]:
            if zoom > 1:
                zoom -= 1
                update = 1
    pg.draw.rect(canvas, (0,255,0), (width/2,1,1,height))
    pg.display.flip()
pg.quit()

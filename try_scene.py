from matvec import *
import tkinter
from math import pi
from random import randint,choice
from itertools import chain,product


def fix_system_zoom():
    import sys
    if sys.platform == 'win32':
        try:
            import ctypes
            PROCESS_SYSTEM_DPI_AWARE = 1  # Int required.
            ctypes.OleDLL('shcore').SetProcessDpiAwareness(PROCESS_SYSTEM_DPI_AWARE)
        except (ImportError, AttributeError, OSError):
            pass


def init_tk():
    fix_system_zoom()
    root = tkinter.Tk()
    canvas = tkinter.Canvas(root,bg='black')
    canvas.pack(fill='both', expand=True)
    root.state('zoomed')
    return root,canvas

root,canvas = init_tk()

def randc(): return (randint(1000,1000000)-500000)*1e3
stars = [ (randc(),randc(),randc(),1) for i in range(10000) ]
lstars = [ choice((2,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0)) for s in stars]

points = [
    (0,0,0,1),
    (0,0,1,1),
    (0,1,0,1),
    (0,1,1,1),
    (1,0,0,1),
    (1,0,1,1),
    (1,1,0,1),
    (1,1,1,1),
]
points = [mul_mv(
            mul_mn(
                scale(200,200,200),
                move(-0.5,-0.5,-0.5),
            ),
            point )
            for point in points]

plane =[
    (0,0,0,1),
    (1,0,0,1),
    (1,1,0,1),
    (0,1,0,1),
]
plane = [mul_mv(
            mul_mn(
                scale(150,200,100),
                move(-0.5,-0.5,0),
            ),
            point )
            for point in plane]

D6 = 100
R6 = D6/sqrt(3)

def plane6(i,j):
    xc = D6*i + D6*j/2
    yc = j*R6*1.5
    return [ (xc+sin(k*pi/3)*R6,yc+cos(k*pi/3)*R6,0,1)   for k in range(6)]

planes6 = [ plane6(i,j) for i,j in product(range(-10,10),range(-7,7)) if i*i+j*j<64]
planes6 = [ 
            [mul_mv(
                mul_mn(
                    move(200,300,1000),
                    rotx(-pi/3),
                ),
                point)
                for point in plane]
            for plane in planes6
            ]


M = mul_mn(rotx(pi/180),rotz(pi/180))
M1 = mul_mn(mul_mn(rotx(pi/18000/3),roty(3*pi/18000/3)),rotz(pi/180000/3))
M2 = mul_mn(mul_mn(rotx(-pi/180/3),roty(-pi/180/4)),rotz(pi/180/5))

CAM = move(0,0,300)
F = 1700

CX,CY = (1000,500)

CNT = 1

def inscreen(p):
    x,y,zb=p
    return zb and abs(x)<1000 and abs(y)<1000

def drawplane(points,fill,color,tag):
    dpoints = [project_zf(mul_mv(CAM,point),F) for point in points]
    cpoints = [(x+CX,y+CY) for x,y,_ in dpoints]
    canvas.create_polygon(
        *chain(cpoints),
        fill=fill,
        outline=color,
        tags=tag
        )


def draw():
    global CNT
    CNT1 = CNT+1
    canvas.delete('all')

    dpoints = [project_zf(mul_mv(CAM,point),F) for point in points]
    for x,y,_ in dpoints:
        x+=CX
        y+=CY
        canvas.create_rectangle(x-2,y-2,x+2,y+2,tags=f'r{CNT1}',fill='yellow')

    dstars = [project_zf(mul_mv(CAM,star),F) for star in stars]
    for p,l in zip(dstars,lstars):
        if inscreen(p):
            x,y = p[0]+CX,p[1]+CY
            canvas.create_rectangle(x-l,y-l,x+l,y+l,tags=f'r{CNT1}',fill='white')
    
    #drawplane(plane,'darkgrey','green',CNT1)
    for plane in planes6: drawplane(plane,'darkgrey','green',CNT1)
    CNT = CNT1

def step():
    global points,stars,plane
    points = [mul_mv(M,point) for point in points]
    stars = [mul_mv(M1,star) for star in stars]
    plane = [mul_mv(M2,point) for point in plane]
    draw()
    root.after(10,step)

step()

root.mainloop()





import tkinter
import time
from tktools import *
import itertools

root,canvas = init_tk()

W = 1000
H = 500

colors = itertools.cycle(['red','green','blue','cyan','grey','yellow'])


def line(i,j):
    canvas.create_line(i*10,j,i*10+10,j,fill = next(colors))

def draw():
    t1 = time.time_ns()
    print('start',t1)

    for i in range(W//10):
        for j in range(H):
            line(i,j)


    t2 = time.time_ns()
    print('stop',t2,(t2-t1)/1e6,'ms')

draw()

root.mainloop()
import tkinter
import time
from random import randint
from itertools import pairwise,chain


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


N = [1000,5000,10000]

def draw():
    n = N.pop(0)
    t1 = time.time_ns()
    print('start',n,t1)

    points = [0,0,10,0,10,20]

    canvas.delete('all')
    for i in range(n):
        dx,dy = randint(-2000,2000),randint(-2000,2000)
        dpoints = list(chain([(x+dx,y+dy) for x,y in pairwise(points)]))
        canvas.create_polygon(dpoints,fill='grey',outline='blue')

    t2 = time.time_ns()
    print('stop',n,t2,(t2-t1)/1e6,'ms')
    if N: root.after(1000,draw)

draw()

root.mainloop()
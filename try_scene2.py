from matvec2 import *
from tktools import *
import random
import math
import itertools
import time

root,canvas = init_tk()



# init polygonas - random square fields+walls on height map

planes = []
D = 100000
R6 = D/math.sqrt(3)


def plane(x,y,z):
    xx = x*D
    yy = y*D
    return ((xx,yy,z),(xx+D,yy,z),(xx+D,yy+D,z),(xx,yy+D,z))

def hexp(x,y,z):
    return(D*x + D*y/2,y*R6*1.5,z*R6)

def hexagone(i,j,z):
    xc,yc,_ = hexp(i,j,0)
    return tuple(( xc+sin(k*pi/3)*R6, yc+cos(k*pi/3)*R6, z ) for k in range(6))

def cube(x,y,z):
    xx=x*D
    yy=y*D
    zz=z*D
    return [
        ((xx,yy,zz),(xx+D,yy,zz),(xx+D,yy+D,zz),(xx,yy+D,zz)),
        ((xx,yy,zz+D),(xx,yy+D,zz+D),(xx+D,yy+D,zz+D),(xx+D,yy,zz+D)),
        ((xx+D,yy,zz),(xx+D,yy,zz+D),(xx+D,yy+D,zz+D),(xx+D,yy+D,zz)),
        ((xx+D,yy+D,zz),(xx+D,yy+D,zz+D),(xx,yy+D,zz+D),(xx,yy+D,zz)),
        ((xx,yy+D,zz),(xx,yy+D,zz+D),(xx,yy,zz+D),(xx,yy,zz)),
        ((xx,yy,zz),(xx,yy,zz+D),(xx+D,yy,zz+D),(xx+D,yy,zz))
    ]

def hexel(x,y,z):
    h = hexagone(x,y,z*R6)
    w = [
        ( p1, (p1[0],p1[1],p1[2]+R6), (p2[0],p2[1],p2[2]+R6), p2 )   
        for p1,p2 in zip(h,[*h[1:],h[0]])
        ]
    h2 = hexagone(x,y,z*R6+R6)
    return [h,*w,h2]

def pillar(x,y,z,h):
    return itertools.chain(*[cube(x,y,z+zz) for zz in range(h)])

def pillarx(x,y,z,h):
    return itertools.chain(*[hexel(x,y,z+zz) for zz in range(h)])


N = 100

for i in range(N):
    for j in range(N):
        #planes.append(plane(i,j,0))
        planes.append(hexagone(i,j,0))


planes += pillarx(0,0,0,2)
planes += pillarx(10,0,0,5)
planes += pillarx(0,10,0,8)
for i in range(N**2//5): planes += pillarx(random.randint(0,N-1),random.randint(0,N-1),0,random.choice([0,0,0,0,0,1,1,1,2,2,3]))


##DEBUG
#planes = [
#    [(0,0,0),
#    (200,0,0),
#    (0,300,0)]
#]


CAM_P = hexp(-10,-10,23) #(20*D,-2000,4000)
CAM_VEC = sub_vec(hexp(N//2,N//2,0),CAM_P)
CAM_HOR= (-1,0,0.2)
F = 1700

LIGHT = (0,0,-5)
LIGHT = mul_vs(LIGHT,1/len_vec(LIGHT))

def m2cam():
    m_cam = m_1()
    cx,cy,cz = CAM_VEC
    try:
        alpha = math.asin( cx/sqrt(cx*cx+cz*cz) )
        if cz < 0: alpha = math.pi - alpha
        m_cam = m_roty(alpha)
        cx,cy,cz = mul_mv(m_cam,(cx,cy,cz))
    except ZeroDivisionError:
        pass
    try:
        beta = math.asin( cy/sqrt(cy*cy+cz*cz) )
        if cz < 0: beta = math.pi - beta
        m_cam = mul_mn(m_rotx(beta),m_cam)
    except ZeroDivisionError:
        pass

    cx,cy,cz = mul_mv(m_cam,CAM_HOR)
    if not math.isclose(cy, 0):
        gamma = math.asin( cy/sqrt(cx*cx+cy*cy) )
        if cx < 0: gamma = math.pi - gamma
        m_cam = mul_mn(m_rotz(-gamma),m_cam)

    return mul_mn(m_cam, m_move(neg_vec(CAM_P)))




def planes2cam(planes,m_cam):
    return [ 
        [ mul_mv(m_cam,point) for point in plane]
        for plane in planes
    ]

def color(plane):
    v = vector_mul(sub_vec(plane[1],plane[0]),sub_vec(plane[2],plane[1]))
    c = abs(scalar_mul(v,LIGHT)/len_vec(v))
    #rrggbb
    d = plane[0][2]/20000
    if d>1: d=1
    i = int(60+100*c*(1-d)**4)
    return f"#{i:02x}{i:02x}{i:02x}"


def planes2d(planes):
    p = [ 
        [[ project_zf(point,F) for point in plane ],color(plane)]
        for plane in planes
        ]
    return [[plane,c] for plane,c in p if all(plane)]

def center(pl2d,xc,yc):
    return [
        [[ (xc-x,yc-y) for x,y in points ],col]
        for points,col in pl2d
        ]

def clip(pl2d,xc,yc):
    return [
        [points,col] for points,col in pl2d 
        if any(0<=x<xc and 0<=y<=yc for x,y in points)
        ]

def wireplanes(pl2d):
    for plane,c in pl2d:
        p = [*plane,plane[0]]
        canvas.create_line(*itertools.chain(p),fill = 'white')

def polygons(pl2d):
    for plane,c in pl2d:
        canvas.create_polygon(*itertools.chain(plane),fill = c,
        outline='grey',
        activefill = 'yellow'
        )


def farpoint(plane): return min(p[2] for p in plane)

def draw():
    t1 = time.time_ns()
    # convert to camera choords
    m = m2cam()
    cplanes = planes2cam(planes,m)
    t2 = time.time_ns()
    
    cplanes.sort(reverse=True,key=farpoint )
    t3 = time.time_ns()
    
    #print(cplanes)
    # project to 2d
    # clip z<0
    # clip out of pyramid
    dplanes = clip(center(planes2d(cplanes),1000,500),2000,1200)
    t4 = time.time_ns()
    

    #TEST DRAW
    #    wireplanes(dplanes)
    polygons(dplanes)
    t5 = time.time_ns()

    canvas.create_rectangle(1000-10,500-10,1000+10,500+10,outline='red')
    
    print("planes",len(planes),"tocam", (t2-t1)/1e6, "sort", (t3-t2)/1e6,"project,center,clip", (t4-t3)/1e6, "tk draw",(t5-t4)/1e6)

# sort by distance

# draw 2d polygonas


M_STEP = mul_mn(m_rotx(math.pi/180/300), m_move(neg_vec(hexp(N//2,N//2,0))))
M_STEP = mul_mn(m_roty(math.pi/180/200), M_STEP)
M_STEP = mul_mn(m_rotz(math.pi/180), M_STEP)
M_STEP = mul_mn(m_move(hexp(N//2,N//2,0)), M_STEP)


def step():
    canvas.delete('all')
    draw()
    global planes
    planes = planes2cam(planes,M_STEP)

    root.after(10,step)
    
step()
#draw()

root.mainloop()





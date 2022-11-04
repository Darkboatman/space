
from math import sin,cos,pi,sqrt

def mul_mv(m,v):
    (
        m11,m12,m13,m14,
        m21,m22,m23,m24,
        m31,m32,m33,m34,
        m41,m42,m43,m44,
    ) = m
    v1,v2,v3 = v
    v4 =1
    return (
        m11*v1 + m12*v2 + m13*v3 + m14*v4,
        m21*v1 + m22*v2 + m23*v3 + m24*v4,
        m31*v1 + m32*v2 + m33*v3 + m34*v4,
    )

def mul_mn(m,n):
    (
        m11,m12,m13,m14,
        m21,m22,m23,m24,
        m31,m32,m33,m34,
        m41,m42,m43,m44,
    ) = m
    (
        n11,n12,n13,n14,
        n21,n22,n23,n24,
        n31,n32,n33,n34,
        n41,n42,n43,n44,
    ) = n
    return (
        m11*n11 + m12*n21 + m13*n31 + m14*n41,
        m11*n12 + m12*n22 + m13*n32 + m14*n42,
        m11*n13 + m12*n23 + m13*n33 + m14*n43,
        m11*n14 + m12*n24 + m13*n34 + m14*n44,
        m21*n11 + m22*n21 + m23*n31 + m24*n41,
        m21*n12 + m22*n22 + m23*n32 + m24*n42,
        m21*n13 + m22*n23 + m23*n33 + m24*n43,
        m21*n14 + m22*n24 + m23*n34 + m24*n44,
        m31*n11 + m32*n21 + m33*n31 + m34*n41,
        m31*n12 + m32*n22 + m33*n32 + m34*n42,
        m31*n13 + m32*n23 + m33*n33 + m34*n43,
        m31*n14 + m32*n24 + m33*n34 + m34*n44,
        m41*n11 + m42*n21 + m43*n31 + m44*n41,
        m41*n12 + m42*n22 + m43*n32 + m44*n42,
        m41*n13 + m42*n23 + m43*n33 + m44*n43,
        m41*n14 + m42*n24 + m43*n34 + m44*n44,
    )


def m_scale(kx,ky,kz):
    return (
        kx,0,0,0,
        0,ky,0,0,
        0,0,kz,0,
        0,0,0,1,
    )


def m_move(v):
    dx,dy,dz=v
    return (
        1,0,0,dx,
        0,1,0,dy,
        0,0,1,dz,
        0,0,0,1,
    )

def m_1():
    return (
        1,0,0,0,
        0,1,0,0,
        0,0,1,0,
        0,0,0,1,
    )

def m_rotx(a):
    return (
        1,0,0,0,
        0,cos(a),-sin(a),0,
        0,sin(a),cos(a),0,
        0,0,0,1,
    )

def m_roty(a):
    return (
        cos(a),0,-sin(a),0,
        0,1,0,0,
        sin(a),0,cos(a),0,
        0,0,0,1,
    )

def m_rotz(a):
    return (
        cos(a),-sin(a),0,0,
        sin(a),cos(a),0,0,
        0,0,1,0,
        0,0,0,1,
    )

def m_transpose(m):
    (
        m11,m12,m13,m14,
        m21,m22,m23,m24,
        m31,m32,m33,m34,
        m41,m42,m43,m44,
    ) = m
    return (
        m11,m21,m31,m41,
        m12,m22,m32,m42,
        m13,m23,m33,m43,
        m14,m24,m34,m44,
    )


def scalar_mul(a,b):
    (a1,a2,a3) = a
    (b1,b2,b3) = b
    return a1*b1+a2*b2+a3*b3

def vector_mul(a,b):
    (a1,a2,a3) = a
    (b1,b2,b3) = b
    return (
        a2*b3-a3*b2,
        a1*b3-a3*b1,
        a1*b2-a2*b1
    )

def mul_vs(v,k):
    (v1,v2,v3) = v
    return v1*k,v2*k,v3*k

def len_vec(v):
    v1,v2,v3 = v
    return sqrt(v1*v1+v2*v2+v3*v3)

def neg_vec(v):
    v1,v2,v3 = v
    return (-v1,-v2,-v3)


def add_vec(a,b):
    (a1,a2,a3) = a
    (b1,b2,b3) = b
    return a1+b1,a2+b2,a3+b3

def sub_vec(a,b):
    (a1,a2,a3) = a
    (b1,b2,b3) = b
    return a1-b1,a2-b2,a3-b3


def project_zf(v,f):
    x,y,z = v
    if z>=0: return f*x/(z+f),f*y/(z+f)
    else: return None

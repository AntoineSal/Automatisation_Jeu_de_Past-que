import numpy as np

def f(U,t): #U est un vecteur de R3 contenant x',y',z'
    m=2.7 * (10**-3)
    h=3*(10**-4)
    alpha = 9 / (10**4)
    omega = 40
    g = 9.81
    a = U[0]
    b = U[1]
    c = U[2]
    return [(1/m)*(-h*np.sqrt(a**2+b**2+c**2)*a + alpha*omega*c), (1/m)*(-h*np.sqrt(a**2+b**2+c**2)*b -m*g), (1/m)*(-h*np.sqrt(a**2+b**2+c**2)* - alpha*omega*a)]


def Euler (f, x0, t):
    tabx0, tabx1, tabx2=[x0[0]], [x0[1]], [x0[2]]
    x0cop=x0. copy ()
    for k in range (1, len(t)):
        delta = t[k]-t[k-1] #calcul du pas
        tabx0.append (0)
        tabx1.append (0)
        tabx2.append (0)
        tabx0[k]=tabx0[k-1]+ delta*(f(x0cop, t [k-1]) [0])
        tabx1[k]=tabx1[k-1]+ delta*(f(x0cop, t [k-1]) [1])
        tabx2[k]=tabx2[k-1]+ delta*(f(x0cop, t [k-1]) [2])
        x0cop=[tabx0 [k], tabx1[k], tabx2 [k]]
    return tabx0, tabx1, tabx2

def x_rectangle(xp, t) :
    tab_x = [0 for i in range(len(t))]
    res = 0
    for i in range(len(t) - 1) :
        res += (t[i+1] - t[i]) * xp[i] 
        tab_x[i] = res 
    return tab_x

def x_euler(xp, t, x0) :
    tab_x = [0 for i in range(len(t))] 
    tab_x[0] = x0
    for i in range(1, len(t)) :
        tab_x[i] = tab_x[i-1] + (t[i] - t[i-1]) * xp[i-1]
    return tab_x

def y_euler(yp, t, y0) :
    tab_y = [0 for i in range(len(t))] 
    tab_y[0] = y0
    for i in range(1, len(t)) :
        tab_y[i] = tab_y[i-1] + (t[i] - t[i-1]) * yp[i-1]
    return tab_y

t = np.linspace(0, 0.7, 10)
xp, yp, zp = Euler(f, [8, 0, 0], t)
print(x_euler(xp, t, 0))
print(y_euler(yp, t, 0.02))
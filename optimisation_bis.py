import math
from copy import copy

r = [0, 20, 40, 50, 70]
a, b = 1116, 900
n = int((math.pi * r[0]) / (a * b) + 1)

dmin = (math.pi * r[1] * r[1]) / (a * b)

def e(m) :
    return math.sqrt(a*a + b*b) / m        # deplacement maximal des centres pour les placer sur la grille

def rho(m) :
    min = (r[1]/(r[1] + e(m)))      # On détèrmine le coefficient pour s'assurer que les sphères deplacées restent dans les spheres de la configuration supposée optimale
    for k in range (1, len(r)) :
        if ((r[k]/(r[k] + e(m))) < min) :
            min = (r[k]/(r[k] + e(m)))
    return min

def p(m) :
    res = 0
    for k in range(1, len(r)) :
        res += r[k] * r[k] * (1/(rho(m)*rho(m)) - 1)   # Différence des aires après diminution du rayon
    return n * math.pi * res

def majoration_perte(m) :
    return (1 - rho(m) * rho(m)) * (1 - dmin) + (p(m) / (a * b))

def taille_grille_pour_seuil(epsilon) :
    m = 1
    while (majoration_perte(m) > epsilon) :
        m += 1
    return m


epsilon = 0.5
m = taille_grille_pour_seuil(epsilon)
print(m)

def init_grille(m) :
    return [[0 for i in range(0, m)] for j in range(0, m)]

def densite(g) : 
    res = 0
    for i in range(len(g)) :
        for j in range(len(g)) :
            res += math.pi * r[g[i][j]] * r[g[i][j]]
    return res /(a * b)

def distance(i, j, k, l) :
    return math.sqrt((i-k)*(i-k) * (b/m) * (b/m) + (j-l)*(j-l) * (a/(m) * (a/(m))))

def incrementer_grille(g) :
    i, j = 0, 0
    while g[i][j] == 4 :
        g[i][j] = 0
        if i < len(g) and j < len(g[i]) :
            j += 1
        if i < len(g) - 1 and j == len(g[i]) :
            i += 1
            j = 0
    g[i][j] = g[i][j] + 1

def grille_max(g) :
    for i in range(len(g)) :
        for j in range(len(g[i])) :
            if g[i][j] != 4 :
                return False 
    return True

def est_valide(g) :
    for i in range(len(g)) :
        for j in range(len(g[i])) :
            if g[i][j] > 0 :
                for k in range(len(g)) :
                    for l in range(len(g[k])) :
                        if distance(i, j, k, l) < r[g[i][j]] + r[g[k][l]] :
                            return False
    return True

#def ajouter_sphere(g, i, j) :


def configuration_optimale(m) :
    densite_max = 0
    g = init_grille(m)
    g_max = copy(g)
    while not(grille_max(g)) :
        if est_valide(g) :
            d = densite(g)
            if d > densite_max :
                densite_max = d
                g_max = copy(g)
        incrementer_grille(g)
    return g_max

print(configuration_optimale(3))
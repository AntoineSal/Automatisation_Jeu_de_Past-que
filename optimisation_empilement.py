import math

rayons = [20, 40, 50, 70]
a, b = 1116, 900
n = int((math.pi * r[0]) / (a * b) + 1)

dmin = (math.pi * rayons[0] * rayons[0]) / (a * b)

def e(m) :
    return math.sqrt(a*a + b*b) / (2**m)        # deplacement maximal des centres pour les placer sur la grille

def rho(m) :
    min = (rayons[1]/(rayons[1] + e(m)))      # On détèrmine le coefficient pour s'assurer que les sphères deplacées restent dans les spheres de la configuration supposée optimale
    for k in range (len(rayons)) :
        if ((rayons[k]/(rayons[k] + e(m))) < min) :
            min = (rayons[k]/(rayons[k] + e(m)))
    return min

def p(m) :
    res = 0
    for k in range(len(rayons)) :
        res += rayons[k] * rayons[k] * (1/(rho(m)*rho(m)) - 1)   # Différence des aires après diminution du rayon
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
    return [[-1 for i in range(0, 2**m)] for j in range(0, 2**m)]

def densite(g) : 
    res = 0
    for i in range(len(g)) :
        for j in range(len(g)) :
            res += math.pi * rayons[g[i][j]] * rayons[g[i][j]]
    return res /(a * b)

def distance(i, j, k, l) :
    return math.sqrt((i-k)*(i-k) * (b/(m)) + (j-l)*(j-l) * (a/(m)))

def ajouter_sphere(g, k, i, j) :
    if i * (b/(2**m)) >= r[k] and i * (b/(2**m)) <= (b - rayons[k]) and j * (a/(2**m)) >= rayons[k] and j * (a/(2**m)) <= (a - rayons[k]) :
        for ip in range(len(g)) :
            for jp in range(len(g)) :
                if g[ip][jp] > 0 and distance(ip, jp, i, j) < rayons[g[ip][jp]] + rayons[k] :
                    return False 
        g[i][j] = k
        return True 
    else :
        return False
                    

def configuration_optimisee_aux(c_max, g, i0, j0, densite_max) :
    if i0 >= 2**m - 1 and j0 >= 2**m - 1 :
        for k in range(0, 5) :
            if ajouter_sphere(g, k, i0, j0):
                new_d = densite(g)
                if new_d > densite_max :
                    densite_max = new_d
                    c_max = g
    else :
        for k in range(0, 5) :
            if ajouter_sphere(g, k, i0, j0) :
                while i0 < len(g) - 1 and j0 <= len(g[i0]) - 1 and g[i0][j0] != -1:
                    if j0 < 2**m - 1 :
                        j0 += 1
                    if j0 == 2**m - 1 :
                        i0 += 1
                        j0 = 0
                configuration_optimisee_aux(c_max, g, i0, j0, densite_max)

def configuration_optimisee(m) :
    c_max = init_grille(m)
    densite_max = 0
    configuration_optimisee_aux(c_max, c_max, 0, 0, densite_max)
    return c_max

c_max = configuration_optimisee(4)
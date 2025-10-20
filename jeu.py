#from importlib.metadata import packages_distributions
#from operator import attrgetter
import sys

import random
from turtle import shape
import numpy as np
import pygame
import pymunk
import math

pygame.init()
rng = np.random.default_rng()

# Constantes

taille = (largeur, hauteur) = (1116, 900)
pad = (40, 160)
bg = (pad[0], pad[1])
hg = (pad[0], hauteur - pad[1])
bd = (largeur - pad[0], pad[1])
hd = (largeur - pad[0], hauteur - pad[1])

couleurs_sphere = (84,84,84)
couleur_fond = (201, 201, 201)
couleur_mur = (0, 0, 0)
epaisseur_mur = 10 
 
fps = 60
next_delay = fps 
next_steps = 20
bias = 0.1

rayons = [20, 40, 50, 70]

density = 0.01
elasticite = 0
impulse = 10
gravite = 24000
damping = 0 # Capacite à etre mis en mouvement

shape_to_sphere = dict()

class Sphere :
    def __init__(self, pos, n, space, mapper) :
        self.n = n % 4
        self.rayon = rayons[self.n]
        self.body = pymunk.Body(body_type = pymunk.Body.DYNAMIC)
        self.body.position = tuple(pos)
        self.shape = pymunk.Circle(body = self.body, radius = self.rayon)
        self.shape.density = density
        self.shape.elasticity = elasticite
        self.shape.collision_type = 1
        self.shape.friction = 0.2
        self.has_collided = False
        mapper[self.shape] = self
        space.add(self.body, self.shape)
        self.alive = True

    def draw(self, screen) : 
        if self.alive :
            c = couleurs_sphere
            c_centre = (0,0,0)
            pygame.draw.circle(screen, tuple(c), self.body.position, self.rayon)
            pygame.draw.circle(screen, tuple(c_centre), self.body.position, self.rayon/100)

    
    @property
    def pos(self) :
        return np.array(self.body.position)

class preSphere :
    def __init__(self, x, n) : 
        self.n = n % 4
        self.rayon = rayons[self.n]
        self.x = x 
    
    def draw(self, screen) :
        pygame.draw.circle(screen, couleurs_sphere, (self.x , pad[1] // 2), self.rayon)

    def set_x(self, x) :
        lim = pad[0] + self.rayon + epaisseur_mur // 2
        self.x = np.clip(x, lim, largeur - lim)
    
    def relacher(self, space, mapper) :
        return Sphere((self.x, pad[0]//2), self.n, space, mapper)

class Mur :
    epaisseur = epaisseur_mur
    def __init__(self, a, b, space) :
        self.body = pymunk.Body(body_type = pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, a, b, self.epaisseur // 2)
        self.shape.friction = 10
        space.add(self.body, self.shape)
    def draw(self, screen) :
        pygame.draw.line(screen, couleur_mur, self.shape.a, self.shape.b, self.epaisseur)


# Creation de la fenetre Pygame

screen = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Jeu de Pastèque")
clock = pygame.time.Clock()
pygame.font.init()
police_score = pygame.font.SysFont("Arial", 32)
overfont = pygame.font.SysFont("Arial", 72)

space = pymunk.Space()
space.gravity = (0, gravite)
space.damping = damping 
space.collision_bias = bias


# Murs

Pad = 20
mur_gauche = Mur(hg, bg, space)
mur_droit = Mur(hd, bd, space)
mur_bas = Mur(hd, hg, space)
murs = [mur_gauche, mur_bas, mur_droit]

# Memorisation des Spheres

rayon_init = random.randint(0, 3)
attendre_prochain = 0
prochaine_sphere = preSphere(largeur//2, rayon_init)
spheres = []

fin_partie = False

# Gestion des Collisions

def resolve_collision(p1, p2, space, spheres, mapper) :
    return None

handler = space.add_collision_handler(1,1)

def collision(arbiter, space, data) :
    shape1, shape2 = arbiter.shapes
    _mapper = data["mapper"]
    sphere1 = _mapper[shape1]
    sphere2 = _mapper[shape2]
    sphere1.has_collided = True
    sphere2.has_collided = True 
    return True

handler.begin = collision 
handler.data["mapper"] = shape_to_sphere
handler.data["spheres"] = spheres 
handler.data["score"] = 0



# Boucle principale du jeu, 
def lancer_partie_manuelle() :
    rayon_init = random.randint(0, 3)
    attendre_prochain = 0
    prochaine_sphere = preSphere(largeur//2, rayon_init)
    spheres = []
    fin_partie = False
    while not fin_partie : 
        attendre_prochain = 0
        for event in pygame.event.get() :
            if event.type == pygame.QUIT : 
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and attendre_prochain == 0 :
                spheres.append(prochaine_sphere.relacher(space, shape_to_sphere))
                attendre_prochain = 1
                print(pygame.mouse.get_pos())
        prochaine_sphere.set_x(pygame.mouse.get_pos()[0])
        if attendre_prochain == 1 :
            prochaine_sphere = preSphere(pygame.mouse.get_pos()[0], random.randint(0, 3))
            attendre_prochain -= 1
    
        screen.fill(couleur_fond)
        prochaine_sphere.draw(screen)
        for m in murs :
            m.draw(screen)
        score = 0
        for s in spheres :
            s.draw(screen)
            score += s.rayon * s.rayon * np.pi
            if s.pos[1] < pad[1] and s.has_collided :
                fin_partie = True 
        score = score / ((bd[0] - bg[0]) * (hd[1] - bd[1]))
        score = int(score * 100) / 100
        handler.data['score'] = score
        label = police_score.render(f" score stratégie optimisée: {handler.data['score']}", 1, (0, 0, 0))
        screen.blit(label, (10, 10))
    
        space.step(1/fps)
        pygame.display.update()
        clock.tick(fps)

    print(handler.data['score'])


# STRATEGIE ALEATOIRE

def jouer_coup_aleatoire() : 
    x = random.uniform(18, 1035)
    print(x)
    pygame.mouse.set_pos([x, 400])
    pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN))

def lancer_partie_aleatoire() :
    rayon_init = random.randint(0, 3)
    attendre_prochain = 0
    prochaine_sphere = preSphere(largeur//2, rayon_init)
    spheres = []
    fin_partie = False
    tour = 0
    while not fin_partie : 
        tour = (tour + 1) % 30
        attendre_prochain = 0
        for event in pygame.event.get() :
            if event.type == pygame.QUIT : 
                pygame.quit()
                sys.exit()
        if tour == 0 and attendre_prochain == 0 :
            prochaine_sphere.set_x(random.uniform(18, 1035))
            spheres.append(prochaine_sphere.relacher(space, shape_to_sphere))
            attendre_prochain = 1
        if attendre_prochain == 1 :
            prochaine_sphere = preSphere(pygame.mouse.get_pos()[0], random.randint(0, 3))
            attendre_prochain -= 1
    
        screen.fill(couleur_fond)
        prochaine_sphere.draw(screen)
        for m in murs :
            m.draw(screen)
        score = 0
        for s in spheres :
            s.draw(screen)
            score += s.rayon * s.rayon * np.pi
            if s.pos[1] < pad[1] and s.has_collided :
                fin_partie = True 
        score = score / ((bd[0] - bg[0]) * (hd[1] - bd[1]))
        score = int(score * 100) / 100
        handler.data['score'] = score
        label = police_score.render(f" score stratégie aléatoire: {handler.data['score']}", 1, (0, 0, 0))
        screen.blit(label, (10, 10))
    
        space.step(1/fps)
        pygame.display.update()
        clock.tick(fps)

    print(handler.data['score'])

# STRATEGIE GLOUTONNE

def ind_rayon(rayons, r) :
    for i in range(len(rayons)) :
        if rayons[i] == r :
            return i + 1

def grille_etat_partie(m, sph) :
    g = [[0 for i in range(0, m)] for j in range(0, m)]
    pas_h = largeur / m
    pas_v = hauteur / m
    for s in sph :
        i, j = 0, 0
        while s.pos[0] > (j + 1) * pas_h:
            j += 1
        while s.pos[1] > (i + 1) * pas_v:
            i += 1
        g[i][j] = - ind_rayon(rayons, s.rayon)
    return g


def jouer_coup_glouton(n, sph) :
    pas = (1035 - 18) / n
    g = grille_etat_partie(n, sph)
    hauteur_colonnes = [0 for i in range(n)]
    for j in range(n) :
        for i in range(n) :
            if g[i][j] != 0 :
                hauteur_colonnes[j] += rayons[-1-g[i][j]]
    ind_min = 0
    print(hauteur_colonnes)
    for i in range(len(hauteur_colonnes)) :
        if hauteur_colonnes[i] < hauteur_colonnes[ind_min] :
            ind_min = i
    print(ind_min)
    return pas * ind_min

def lancer_partie_gloutonne(n) :
    rayon_init = random.randint(0, 3)
    rayon_actuel = rayon_init
    attendre_prochain = 0
    prochaine_sphere = preSphere(largeur//2, rayon_init)
    spheres = []
    fin_partie = False
    tour = 0
    while not fin_partie : 
        tour = (tour + 1) % 34
        attendre_prochain = 0
        for event in pygame.event.get() :
            if event.type == pygame.QUIT : 
                pygame.quit()
                sys.exit()
        if tour == 0 and attendre_prochain == 0 :
            prochaine_sphere.set_x(jouer_coup_glouton(n, spheres))
            spheres.append(prochaine_sphere.relacher(space, shape_to_sphere))
            attendre_prochain = 1
        if attendre_prochain == 1 :
            rayon_actuel = random.randint(0, 3)
            prochaine_sphere = preSphere(pygame.mouse.get_pos()[0], rayon_actuel)
            attendre_prochain -= 1
    
        screen.fill(couleur_fond)
        prochaine_sphere.draw(screen)
        for m in murs :
            m.draw(screen)
        score = 0
        for s in spheres :
            s.draw(screen)
            score += s.rayon * s.rayon * np.pi
            if s.pos[1] < pad[1] and s.has_collided :
                fin_partie = True 
        score = score / ((bd[0] - bg[0]) * (hd[1] - bd[1]))
        score = int(score * 1000) / 1000
        handler.data['score'] = score
        label = police_score.render(f" score stratégie gloutonne: {handler.data['score']}", 1, (0, 0, 0))
        screen.blit(label, (10, 10))
    
        space.step(1/fps)
        pygame.display.update()
        clock.tick(fps)

    print(handler.data['score'])





# STRATEGIE EMPILEMENT OPTIMISE

a, b = 1116, 900
n = int((math.pi * rayons[0]) / (a * b) + 1)

dmin = (math.pi * rayons[0] * rayons[0]) / (a * b)

def e(m) :
    return math.sqrt(a*a + b*b) / (m)        # deplacement maximal des centres pour les placer sur la grille

def rho(m) :
    min = (rayons[0]/(rayons[0] + e(m)))      # On détèrmine le coefficient pour s'assurer que les sphères deplacées restent dans les spheres de la configuration supposée optimale
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

def distance(p, i, j, k, l) :
    return math.sqrt((i-k)*(i-k) * (b/(p)) + (j-l)*(j-l) * (a/(p)))

def densite(g) : 
    res = 0
    for i in range(len(g)) :
        for j in range(len(g)) :
            res += math.pi * rayons[abs(g[i][j]) - 1] * rayons[abs(g[i][j]) - 1]
    return res /(a * b)

def est_valide(g) :
    for i in range(len(g)) :
        for j in range(len(g[i])) :
            if g[i][j] != 0 :
                for k in range(len(g)) :
                    for l in range(len(g[k])) :
                        if g[k][l] != 0 :
                            if distance(len(g), i, j, k, l) < rayons[abs(g[i][j]) - 1] + rayons[abs(g[k][l]) - 1] :
                                return False
    return True

def heuristique(g, i_actuel, j_actuel) :
    pas = (1035 - 18) / n
    largeur_actuelle = j_actuel * pas 
    hauteur_actuelle = i_actuel * pas 
    return (densite(g) - 1) * largeur_actuelle * hauteur_actuelle + a * b

def incr_indice(i, j, g) :
    if j < len(g) - 1 :
        j += 1
    else :
        j = 0
        i += 1

def configuration_optimisee(g, i_actuel, j_actuel, densite_opt, grille_opt) :
    if i_actuel == len(g) and j_actuel == len(g) and densite(g) > densite_opt:
        grille_opt = g
        densite_opt = densite(g)
    if g[i_actuel][j_actuel] >= 0 :
        for r in range(0, 4) :
            new_i, new_j = i_actuel, j_actuel
            incr_indice(new_i, new_j, g)
            g[i_actuel][j_actuel] = r
            if est_valide(g) and heuristique(g, i_actuel, j_actuel) > densite_opt :
                configuration_optimisee(g, new_i, new_j, densite_opt, grille_opt)
    else :
        incr_indice(i_actuel, j_actuel, g) 
        configuration_optimisee(g, i_actuel, j_actuel, densite_opt, grille_opt)
    return grille_opt


def jouer_coup_optimise(p, rayon_actuel, sph) :
    g = grille_etat_partie(p, sph)
    cible = configuration_optimisee(g, 0, 0, dmin, g)
    for i in range(len(cible)) :
        for j in range(len(cible)) :
            if cible[i][j] == rayon_actuel :
                return j * largeur / len(cible)
    return random.uniform(18, 1035)

def lancer_partie_optimise(epsilon) :
    rayon_init = random.randint(0, 3)
    rayon_actuel = rayon_init
    attendre_prochain = 0
    prochaine_sphere = preSphere(largeur//2, rayon_init)
    spheres = []
    fin_partie = False
    tour = 0
    p = taille_grille_pour_seuil(epsilon)
    p = 10
    while not fin_partie : 
        tour = (tour + 1) % 44
        attendre_prochain = 0
        for event in pygame.event.get() :
            if event.type == pygame.QUIT : 
                pygame.quit()
                sys.exit()
        if tour == 0 and attendre_prochain == 0 :
            prochaine_sphere.set_x(jouer_coup_optimise(p, rayon_actuel, spheres))
            spheres.append(prochaine_sphere.relacher(space, shape_to_sphere))
            attendre_prochain = 1
        if attendre_prochain == 1 :
            rayon_actuel = random.randint(0, 3)
            prochaine_sphere = preSphere(pygame.mouse.get_pos()[0], rayon_actuel)
            attendre_prochain -= 1
    
        screen.fill(couleur_fond)
        prochaine_sphere.draw(screen)
        for m in murs :
            m.draw(screen)
        score = 0
        for s in spheres :
            s.draw(screen)
            score += s.rayon * s.rayon * np.pi
            if s.pos[1] < pad[1] and s.has_collided :
                fin_partie = True 
        score = score / ((bd[0] - bg[0]) * (hd[1] - bd[1]))
        score = int(score * 1000) / 1000
        handler.data['score'] = score
        label = police_score.render(f" score stratégie optimisée : {handler.data['score']}", 1, (0, 0, 0))
        screen.blit(label, (10, 10))
    
        space.step(1/fps)
        pygame.display.update()
        clock.tick(fps)

    print(handler.data['score'])


# lancer_partie_manuelle()
# lancer_partie_aleatoire()
# lancer_partie_gloutonne(7)
# lancer_partie_optimise(0.1)
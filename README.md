# Automatisation Jeu de Pastèque
Automatisation du jeu de Pastèque (ou Suika Game), basée sur une recherche de la configuration de densité minimale pour un empilement de sphères.

Dans le cadre de mon TIPE, j'ai fait un travail de recherche sur la question d'empilement de sphères, notamment sur une minimisation de la densité d'empilement de sphères aléatoires.

Dans le jeu de pastèque, on empile des sphères de rayon aléatoire de manière séquentielle.

J'ai démontré que, en discrétisant le panier où l'on dépose les sphères, on peut s'approcher autant qu'on veut de la densité minimale en centrant nos sphères sur la grille créée.
Pour tout epsilon > 0, il existe n un entier tel qu'en découpant le panier en une grille de taille n, on obtient une configuration centrée sur la grille dont la densité d <= dmin + epsilon.
La démonstration est la partie la plus intéressante du projet à mon sens.

Une fois que j'ai montré ça, à chaque sphère à déposer dans le panier, je calcul une configuration dont la densité s'approche à epsilon près de l'optimal avec un algorithme séparer et évaluer, et je place ma  sphère de sorte à me rapprocher de la configuration obtenue.

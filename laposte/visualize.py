#!/usr/bin/env python3
# université pierre et marie curie - c. dürr - 2016

"""
Usage:
    ./visualize.py gpsfile < SCIP_output  > visualize.js

Lit un texte avec des données géographiques et la sortie du solveur SCIP et
produit du code javascript pour la visualisation. L'entrée contient trois
types de lignes.  Une ligne du fichier de la forme

    v identifiant longitude latitude

décrit un sommet, où *identifiant* est un identifiant unique du sommet et
*longitude, latitude* sont des nombres flottants qui représentent les degrés
des coordonnées GPS. Une ligne de l'entrée de la forme

    open#i          v ...

représente un sommet sélectionné si v > 0.5. Alors qu'une ligne de la forme

    objective value:                     13915.2817350018

décrit la valeur objectif de la solution.
"""

from math import sin, cos, sqrt, radians, asin
import sys


# --- from tryalgo.convex_hull import andrew

def left_turn(a, b, c):
    return (a[0] - c[0]) * (b[1] - c[1]) - (a[1] - c[1]) * (b[0] - c[0]) > 0


def andrew(S):
    """Convex hull by Andrew

    :param S: list of points as coordinate pairs
    :requires: S has at least 2 points
    :returns: list of points of the convex hull
    :complexity: `O(n log n)`
    """
    S.sort()
    top = []
    bot = []
    for p in S:
        while len(top) >= 2 and not left_turn(p, top[-1], top[-2]):
            top.pop()
        top.append(p)
        while len(bot) >= 2 and not left_turn(bot[-2], bot[-1], p):
            bot.pop()
        bot.append(p)
    return bot[:-1] + top[:0:-1]

# --- données globales

GPS = {}           # associe identifiant à un point (latitude, longitude)
selected = []      # liste de centres
objvalue = 0.0     # valeur objectif obtenue par la liste des centres
cell = {}

"""lit de l'entrée standard une solution dont les lignes sont dans un des formats
v [identificateur] [latitude] [longitude]
s [latitude] [longitude]
o [valeur objectif]
"""
for line in open(sys.argv[1],  'r'):
    if line[0] == "v":
        tab = line.split()
        identficateur = int(tab[1])
        latitude  = float(tab[2])
        longitude = float(tab[3])
        GPS[identficateur] = (latitude, longitude)

for line in sys.stdin:
    if line[0:4] == "open":
        tab = line.split()
        tab = tab[0].split('#')
        selected.append(GPS[int(tab[1])])
    if line[0:6] == "client":
        tab = line.split()
        tab = tab[0].split('#')
        c = GPS[int(tab[1])]
        p = GPS[int(tab[2])]
        if p not in cell:
            cell[p] = [c]
        else:
            cell[p].append(c)
    if line[0:9] == "objective":
        tab = line.split()
        objvalue = float(tab[2])


# restrict to convex hull
for j in selected:
    cell[j] = andrew(cell[j])

# --- print javascript for visualization

print ("var markers = [")
for p in selected:
    print(" [%.6f, %.6f]," % p)
print("];")


print("var polygons = [")
for j in selected:
    print("[")
    for point in cell[j]:
        print("[%.6f, %.6f], " % point )
    print("[%.6f, %.6f] " % cell[j][0] )   # to close the polygon
    print("],")
print("];")

print("var objvalue = %.10f;" % objvalue)

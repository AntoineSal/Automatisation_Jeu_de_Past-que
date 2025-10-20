import sys

import random
from turtle import shape
import numpy as np
import pygame
import pymunk
import time

fin_partie = False 

def placer_prochain_coup() :
    x = random.uniform(0, 1116)
    pygame.set_mouse(x)

def jouer_coup() : 
    pygame.event.post(pygame.MOUSEBUTTONDOWN)

while not fin_partie :
    placer_prochain_coup()
    time.sleep(0.5)
    jouer_coup()

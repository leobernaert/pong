import pygame
import random

import random
import pygame, sys
from pygame.locals import *

pygame.init()
fps = pygame.time.Clock()

#colors #couleurs
WHITE = (225,225,225)
RED = (0,0,0)
""" on a changé la couleur de la balle en noir a la place du rouge"""
GREEN = (0,0,0)
""" on  a changé la couleur des raquettes en noir la place du vert"""
BLACK = (0,250,100)
""" on a changé la couleur du fond en ver fluo a la place du noir"""

#globals #global
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH // 2
HALF_PAD_HEIGHT = PAD_HEIGHT // 2
ball_pos = [0,0]
ball_vel = [0,0]
paddle1_vel = 0
paddle2_vel = 0
l_score = 0
r_score = 0

#canvas declaration #déclaration de toile
window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('Hello World')

# helper function that spawns a ball, returns a position vector and a velocity vector
# if right is True, spawn to the right, else spawn to the left
def ball_init(right):
    """
    fonction utilitaire qui lance la balle, modifie globalement le 
    vecteur position et le vecteur vitesse 
    @param right s'il est vrai, la balle se lance a droite sinon a gauche 
    """
    global ball_pos, ball_vel # these are vectors stored as lists
    """
    Ce sont des vecteurs stockés sous formes de listes
    """
    ball_pos = [WIDTH//2,HEIGHT//2]
    horz = random.randrange(2,4)
    vert = random.randrange(1,3)
    
    if right == False:
        horz = - horz
        
    ball_vel = [horz,-vert]

# define event handlers
"""
Définir les gestionnaires d'événements
"""
def init():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel,l_score,r_score  # these are floats
    global score1, score2  # these are ints
    paddle1_pos = [HALF_PAD_WIDTH - 1,HEIGHT//2]
    paddle2_pos = [WIDTH +1 - HALF_PAD_WIDTH,HEIGHT//2]
    l_score = 0
    r_score = 0
    if random.randrange(0,2) == 0:
        ball_init(True)
    else:
        ball_init(False)

#keydown handler 
"""
touche bas gestionnaire
"""
def keydown(event):
    global paddle1_vel, paddle2_vel
    
    if event.key == K_UP:
        paddle2_vel = -8
    elif event.key == K_DOWN:
        paddle2_vel = 8
        """ changement de la touche w initiale par la touche z afin de permettre a la raquette 1 d'être dirigée par les touches z et s"""
    elif event.key == K_z:
        paddle1_vel = -8
    elif event.key == K_s:
        paddle1_vel = 8

#keyup handler
"""
touche haute gestionnaire
"""
def keyup(event):
    global paddle1_vel, paddle2_vel
    
    if event.key in (K_z, K_s):
        paddle1_vel = 0
    elif event.key in (K_UP, K_DOWN):
        paddle2_vel = 0

init()

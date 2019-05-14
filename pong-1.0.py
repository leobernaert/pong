#PONG pygame
"""
Copyright: 2013 vinothpandian
téléchargé depuis https://gist.github.com/vinothpandian/4337527

Débogué le 8 mars 2019, par G. Khaznadar, pour
l'adapter à Python3. Les seules adaptations faites
ont consisté à replacer les divisions par défaut (/)
par des divisions entières (//), sachant que Python3
fait la distinction. Si les variables ne sont pas entières,
ça crée des exceptions pour l'appel à range, ainsi que pour
le tracé des objets géométriques.

L'autre débogage a été de placer la dernière instruction, 
qui était inaccessible, dans la boucle principale du jeu.
"""

import random
import pygame, sys
from pygame.locals import *

pygame.init()
fps = pygame.time.Clock()

#colors #couleurs
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,225,0)
BLACK= (0,0,0)

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


#draw function of canvas
"""
dessine la fonction de la toile
"""
def draw(canvas):
    global paddle1_pos, paddle2_pos, ball_pos, ball_vel, l_score, r_score
           
    canvas.fill(BLACK)
    pygame.draw.line(canvas, WHITE, [WIDTH // 2, 0],[WIDTH // 2, HEIGHT], 1)
    pygame.draw.line(canvas, WHITE, [PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1)
    pygame.draw.line(canvas, WHITE, [WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1)
    pygame.draw.circle(canvas, WHITE, [WIDTH//2, HEIGHT//2], 70, 1)

    # update paddle's vertical position, keep paddle on the screen
    """
    mise à jour de la position verticale de la raquette, garder la palette à l'écran
    """
    if paddle1_pos[1] > HALF_PAD_HEIGHT and paddle1_pos[1] < HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos[1] += int(paddle1_vel)
    elif paddle1_pos[1] == HALF_PAD_HEIGHT and paddle1_vel > 0:
        paddle1_pos[1] += int(paddle1_vel)
    elif paddle1_pos[1] == HEIGHT - HALF_PAD_HEIGHT and paddle1_vel < 0:
        paddle1_pos[1] += int(paddle1_vel)
    
    if paddle2_pos[1] > HALF_PAD_HEIGHT and paddle2_pos[1] < HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos[1] += int(paddle2_vel)
    elif paddle2_pos[1] == HALF_PAD_HEIGHT and paddle2_vel > 0:
        paddle2_pos[1] += int(paddle2_vel)
    elif paddle2_pos[1] == HEIGHT - HALF_PAD_HEIGHT and paddle2_vel < 0:
        paddle2_pos[1] += int(paddle2_vel)

    #update ball
    """
    mise a jour de la balle
    """
    ball_pos[0] += int(ball_vel[0])
    ball_pos[1] += int(ball_vel[1])

    #draw paddles and ball
    """
    dessiner une raquette et une balle
    """
    pygame.draw.circle(canvas, RED, ball_pos, 20, 0)
    pygame.draw.polygon(canvas, GREEN, [[paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT], [paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT], [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT], [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT]], 0)
    pygame.draw.polygon(canvas, GREEN, [[paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT], [paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT], [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT], [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT]], 0)

    #ball collision check on top and bottom walls
    """
    contrôle de collision de billes sur les murs supérieurs et inférieurs
    """
    if int(ball_pos[1]) <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    if int(ball_pos[1]) >= HEIGHT + 1 - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
    
    #ball collison check on gutters or paddles
    """
    contrôle de collision de balle dans les gouttières ou les raquettes
    """
    if int(ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH and int(ball_pos[1]) in range(paddle1_pos[1] - HALF_PAD_HEIGHT,paddle1_pos[1] + HALF_PAD_HEIGHT,1):
        ball_vel[0] = -ball_vel[0]
        ball_vel[0] *= 1.1
        ball_vel[1] *= 1.1
    elif int(ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH:
        r_score += 1
        ball_init(True)
        
    if int(ball_pos[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH and int(ball_pos[1]) in range(paddle2_pos[1] - HALF_PAD_HEIGHT,paddle2_pos[1] + HALF_PAD_HEIGHT,1):
        ball_vel[0] = -ball_vel[0]
        ball_vel[0] *= 1.1
        ball_vel[1] *= 1.1
    elif int(ball_pos[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH:
        l_score += 1
        ball_init(False)

    #update scores
    """
    mise a jour des scores
    """
    myfont1 = pygame.font.SysFont("Comic Sans MS", 20)
    label1 = myfont1.render("Score "+str(l_score), 1, (255,255,0))
    canvas.blit(label1, (50,20))

    myfont2 = pygame.font.SysFont("Comic Sans MS", 20)
    label2 = myfont2.render("Score "+str(r_score), 1, (255,255,0))
    canvas.blit(label2, (470, 20))  
    
    
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


#game loop
"""
boucle de jeu
"""
while True:

    draw(window)

    for event in pygame.event.get():

        if event.type == KEYDOWN:
            keydown(event)
        elif event.type == KEYUP:
            keyup(event)
        elif event.type == QUIT:
            pygame.quit()
            sys.exit()
            
    pygame.display.update()
    fps.tick(60)

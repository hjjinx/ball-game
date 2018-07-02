import time
import random
import pygame
pygame.init()

#colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
DARKVIOLET = (148,0,211)
BGCOLOR = BLACK
BALL_COLOR = RED
PROJECTILE_COLOR = DARKVIOLET

#display
displayWidth = 1024
displayHeight = 600
display = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption('PHY')
heart = pygame.image.load('heart.png')
myfont = pygame.font.SysFont('Terminal', 18)
clock = pygame.time.Clock()
endTime = time.time()

#physics
x, y = displayWidth/2, displayHeight/1.1
ux, uy, ax, ay = 0, 0, 0, 0 # u means velocity, a  means acceleration
uc, ac = 10, 2 # c stands for the amount of change on key press
moveUp, moveDown, moveRight, moveLeft = False, False, False, False
xp1, yp1, up1, ap = [], 0, 50, 50 #projectile variables. xp1 list coz multiple projectiles
xl, yl, ul, al = random.randint(0, displayWidth - 50), 0, 50, 50
score = 0
lives = 3
touching = False
lifeFalling = False

#misc
projectile = pygame.Surface((10,20))
projectile.fill(PROJECTILE_COLOR)
numOfProjectiles = 15
inc_numOfProjectiles = 3 

#adding random locations for projectiles to spawn in
for _ in range(numOfProjectiles):
    xp1.append(random.randint(0,displayWidth))

playing = True
while playing:
    #taking dt to be a small value which will depend on the processing power
    startTime = time.time()
    t = startTime - endTime

    #changing the postions and velocities with time
    ux += ax * t
    uy += ay * t
    x += ux * t
    y += uy * t
    up1 += ap * t
    yp1 += up1 * t
    if lives <= 5: #spawning extra lives
        ran=random.random()
    if ran<0.01:
       lifeFalling = True
    if lifeFalling == True:
        ul += al * t
        yl += ul * t
        if yl > displayHeight:
            xl, yl, ul, al = random.randint(0, displayWidth - 50), 0, 50, 50
            lifeFaling = False

    endTime = time.time()
    
    #checking for collision of ball with boundaries
    if x < 0:
        x = 0
        ux = -ux / 3
    if x > displayWidth:
        x = displayWidth
        ux = -ux / 3
    if y < 0:
        y = 0
        uy = -uy / 3
    if y > displayHeight:
        y = displayHeight
        uy = -uy / 3

    #Checking for key press
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            playing = False
        elif ev.type == pygame.KEYDOWN: #acts on pressing and not on holding key
            if ev.key == pygame.K_UP:
                moveUp = True
            if ev.key == pygame.K_DOWN:
                moveDown = True
            if ev.key == pygame.K_LEFT:
                moveLeft = True
            if ev.key == pygame.K_RIGHT:
                moveRight = True
        elif ev.type == pygame.KEYUP:
##            if ev.key == pygame.K_UP or ev.key == pygame.K_DOWN:
##                moveUp, moveDown = False, False
##            if ev.key == pygame.K_LEFT or ev.key == pygame.K_RIGHT:
##                moveLeft, moveRight = False, False
            if ev.key == pygame.K_UP:
                moveUp = False
            if ev.key == pygame.K_DOWN:
                moveDown = False
            if ev.key == pygame.K_LEFT:
                moveLeft = False
            if ev.key == pygame.K_RIGHT:
                moveRight = False
    if moveUp == True:
        ay -= ac
        uy -= uc
##        moveUp = False
    if moveDown == True:
        ay += ac
        uy += uc
##        moveDown = False
    if moveLeft == True:
        ax -= ac
        ux -= uc
##        moveLeft = False
    if moveRight == True:
        ax += ac
        ux += uc
##        moveRight = False

    #condition for when the projectile crosses the screen
    if yp1 > displayHeight:
        yp1 = 0
        up1 = 4 * up1 / 5
        ap += 5
        xp1 = []
        score += 1
        if score % 5 == 0:
            numOfProjectiles += inc_numOfProjectiles 
        for _ in range(numOfProjectiles):
            xp1.append(random.randint(0,displayWidth))

    #checking for collision between ball and project
    if y > yp1 and y < yp1 + 30:
        g = 0
        while g < numOfProjectiles:
            if x > xp1[g] - 10 and x < xp1[g] + 20:
                touching = True
                del xp1[g]
                numOfProjectiles -= 1
            g += 1
    if touching:
        if lives > 1:
            lives -= 1
            touching = False
        else:
            playing = False

    #checking for collision between ball and live
    if x > xl and x < xl + 20 and y < yl + 20 and y > yl:
        lives += 1
        xl, yl, ul, al = random.randint(0, displayWidth - 50), 0, 50, 50
        lifeFalling = False
        
    #displaying
    display.fill(BGCOLOR)
    for g in range(lives): #displaying the lives as hearts
        display.blit(heart, (1000 - g * 25,25))
    for g in range(numOfProjectiles): #displaying the same projectile at 20 places
        display.blit(projectile, (xp1[g], yp1))
    if lifeFalling == True:
        display.blit(heart, (xl, yl))
    pygame.draw.circle(display, BALL_COLOR, (int(x),int(y)), 10, 0) #displaying the ball
    textDisp = myfont.render('SCORE: %s'%(score),False,WHITE)
    display.blit(textDisp,(960, 50)) #displaying the score
    pygame.display.update()
    clock.tick(60)

pygame.quit()
print("You lost :(. Your score was " + str(score))

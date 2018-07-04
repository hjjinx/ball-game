import time
import random
import pygame
pygame.init()

#colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0 ,255)
DARKVIOLET = (148, 0, 211)
FLAME = (226, 88, 34)
BGCOLOR = BLACK
BALL_COLOR = RED
PROJECTILE_COLOR = DARKVIOLET
WS_COLOR = FLAME

#display
displayWidth = 1024
displayHeight = 600
display = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption('PHY')
heart = pygame.image.load('heart.png')
myfont = pygame.font.SysFont('Terminal', 18)
clock = pygame.time.Clock()
endTime = time.time()
FPS = 120 #Don't change. It has a lot of effect on game and speeds
    
#physics
x, y, ux, uy, ax, ay, uc, ac = displayWidth/2, displayHeight/1.1, 0, 0, 0, 0, 5, 5 # Ball variables. u means velocity, a  means acceleration. uc and ac is the amount of change on key press
moveUp, moveDown, moveRight, moveLeft = False, False, False, False
xp1, yp1, up1, ap = [], 0, 50, 50 #projectile variables. xp1 list coz multiple projectiles
xws, yws, uws, xwsDicrease = random.randint(50, displayWidth - 50), 0, 100, 0 #wallSpace variables. xws is the x coordinate of the space in the wall
xl, yl, ul, al = random.randint(0, displayWidth - 50), 0, 50, 50 #life variables
score = 0
lives = 3
lifeFalling = False
textDisp = myfont.render('SCORE: %s'%(score),False,WHITE)

#stages is the word I gave to various levels of game
stageTimes = 0 # This is the number of times the same stage has occured
stages = [] # 0 - projectileFalling, 1 - wallSpace
stageActive = True
projectileFalling = True # True because I want the first stage of the game to be projectileFalling
wallSpace = False
#add new stages here
stages.append(projectileFalling) # stages[0] is projectileFalling
stages.append(wallSpace) # stages[1] is wallSpace
projectile = pygame.Surface((10,20))
projectile.fill(PROJECTILE_COLOR)
numOfProjectiles = 15
inc_numOfProjectiles = 3

#adding random locations for projectiles to spawn in
for _ in range(numOfProjectiles):
    xp1.append(random.randint(0,displayWidth))

playing = True
while playing:
    if stageActive == False:
        stages[random.randint(0,len(stages) - 1)] = True #selecting a random stage to start
        stageActive = True
    
    #filling the bgcolor first because other objects will overlap it
    display.fill(BGCOLOR)

    #taking dt to be a small value which will depend on the processing power
    startTime = time.time()
    t = startTime - endTime

    #ball
    ux += ax * t
    uy += ay * t
    x += ux * t
    y += uy * t

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

    #projectileFalling
    if stages[0] == True:
        up1 += ap * t
        yp1 += up1 * t
        
        #condition for when the projectile crosses the screen
        if yp1 > displayHeight:
            stageTimes += 1
            
            if stageTimes == 5:
                #setting this stage to False so 'probably' a new stage can start
                stageTimes = 0
                stages[0] = False
                stageActive = False
                
            yp1 = 0
            up1 = 3 * up1 / 5
            ap += 5
            uws += 10 #wall space vars increment
            if score != 0:
                xwsDicrease += 10/score #wall space vars increment
            else:
                xwsDicrease += 15 #wall space vars increment
            xp1 = []
            score += 1
            textDisp = myfont.render('SCORE: %s'%(score),False,WHITE)
            if score % 5 == 0:
                numOfProjectiles += inc_numOfProjectiles 
            for _ in range(numOfProjectiles):
                xp1.append(random.randint(0,displayWidth))
                
        #checking for collision between ball and projectile
        if y > yp1 and y < yp1 + 30:
            g = 0
            while g < numOfProjectiles:
                if x > xp1[g] - 10 and x < xp1[g] + 20:
                    if lives > 1:
                        lives -= 1
                    else:
                        playing = Fals
                    del xp1[g]
                    numOfProjectiles -= 1
                g += 1

                
        #displaying the same projectile at 20 places
        for g in range(numOfProjectiles):
            display.blit(projectile, (xp1[g], yp1))


    #wallSpace
    if stages[1] == True:
        yws += uws * t
        if yws > displayHeight:
            xws, yws = random.randint(50, displayWidth - 50), 0
            uws += 10
            if score != 0:
                xwsDicrease += 10/score
            else:
                xwsDicrease += 15
            up1 = 3 * up1 / 5 #projectile vars increment
            ap += 5 #projectile vars increment
            stageTimes += 1
            score += 1
            textDisp = myfont.render('SCORE: %s'%(score),False,WHITE)
            if score % 5 == 0:
                numOfProjectiles += inc_numOfProjectiles #projectile vars increment
            for _ in range(numOfProjectiles):
                xp1.append(random.randint(0,displayWidth))
            if stageTimes >= 5:
                stageTimes = 0
                stages[1] = False
                stageActive = False

        else:
            wsLeftSurf = pygame.Surface((xws, 50))
            wsLeftSurf.fill(WS_COLOR)
            display.blit(wsLeftSurf,(0, yws))
            wsRightSurf = pygame.Surface(((displayWidth - xws - 100 + xwsDicrease), 50))
            wsRightSurf.fill(WS_COLOR)
            display.blit(wsRightSurf, ((xws + 100 - xwsDicrease), yws))
        
        if (x < (xws) and y > (yws) and y < (yws + 50)) or (x > (xws + 100 - xwsDicrease) and y > yws and y < (yws + 50)):
            if lives > 1:
                lives -= 1
            else:
                playing = False
                
            xws, yws = random.randint(50, displayWidth - 50), 0
            uws += 5

        


    #extra life falling
    if lives <= 4: #max no. of lives is 5. If lives less than max, extra life may fall.
        ran=random.random()
        if ran<0.01:
           lifeFalling = True
    if lifeFalling == True:
        ul += al * t
        yl += ul * t
        if yl > displayHeight:
            xl, yl, ul, al = random.randint(0, displayWidth - 50), 0, 50, 50
            lifeFaling = False
        #checking for collision between ball and live
        elif x > xl and x < xl + 20 and y < yl + 20 and y > yl:
            lives += 1
            xl, yl, ul, al = random.randint(0, displayWidth - 50), 0, 50, 50
            lifeFalling = False


    #Checking for key press
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            playing = False
        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_UP:
                moveUp = True
            if ev.key == pygame.K_DOWN:
                moveDown = True
            if ev.key == pygame.K_LEFT:
                moveLeft = True
            if ev.key == pygame.K_RIGHT:
                moveRight = True
        elif ev.type == pygame.KEYUP:
            if ev.key == pygame.K_UP:
                moveUp = False
                ay = 0
            if ev.key == pygame.K_DOWN:
                moveDown = False
                ay = 0
            if ev.key == pygame.K_LEFT:
                moveLeft = False
                ax = 0
            if ev.key == pygame.K_RIGHT:
                moveRight = False
                ax = 0
    #actions on key press. If the velocity is in opposite direction of what user presses the button of, ball will turn around faster.
    if moveUp == True:
        if uy > 0:
            ay -= ac * 2
            uy -= uc * 2
        else:
            ay -= ac
            uy -= uc
    if moveDown == True:
        if uy < 0:
            ay += ac * 2
            uy += uc * 2
        else:
            ay += ac
            uy += uc
    if moveLeft == True:
        if ux > 0:
            ax -= ac * 2
            ux -= uc * 2
        else:
            ax -= ac
            ux -= uc
    if moveRight == True:
        if ux < 0:
            ax += ac * 2
            ux += uc * 2
        else:
            ax += ac
            ux += uc
        
    #displaying
    for g in range(lives): #displaying the current no. of lives as hearts
        display.blit(heart, (displayWidth - 50 - g * 25,25))
    if lifeFalling == True:
        display.blit(heart, [xl, yl])
    pygame.draw.circle(display, BALL_COLOR, (int(x),int(y)), 10, 0) #displaying the ball
    display.blit(textDisp,(displayWidth - 100, 50)) #displaying the score
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
print("Thanks for playing. Your score was " + str(score))

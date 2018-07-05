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
myfontScore = pygame.font.SysFont('Terminal', 18)
clock = pygame.time.Clock()
FPS = 60 #Don't change. It has a lot of effect on game and speeds
pygame.mouse.set_pos([displayWidth/2, displayHeight/2])
moveUp, moveDown, moveRight, moveLeft = False, False, False, False
score = 0
lifeFalling = False
playing = False
scoreDisp = myfontScore.render('SCORE: %s'%(score),False,WHITE)
pygame.event.set_grab(True) #Disabling mouse to move out of screen

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
numOfProjectiles = 20
inc_numOfProjectiles = 5

#Welcome Screen
welcomeDisp = (pygame.font.SysFont('Terminal', 52)).render("WELCOME TO BALL GAME", False, FLAME)
diffSay = (pygame.font.SysFont('Terminal', 28)).render("SELECT YOUR DIFFICULTY", False, FLAME)
myfontDiff = (pygame.font.SysFont('Terminal', 25))
diffPleb = myfontDiff.render('PLEB (FOR ULTIMATE NOOBS)', False, (255,255,0)) #http://www.color-hex.com/color-palette/62287
diffEasy = myfontDiff.render('EASY (FOR NOOBS)', False, (173,255,47))
diffMedium = myfontDiff.render('MEDIUM (FOR INTERMEDIATES)', False, (0,255,127))
diffHard = myfontDiff.render('HARD (FOR THOSE WHO LIKE A CHALLENGE)', False, (255,99,71))
diffExtreme = myfontDiff.render('EXTREME (FOR HARDCORE REBELS)', False, RED)

diffPlebCoord = (displayWidth / 2 - 126, displayHeight / 3)
diffEasyCoord = (displayWidth / 2 - 82, displayHeight / 2.7)
diffMediumCoord = (displayWidth / 2 - 132, displayHeight / 2.45)
diffHardCoord = (displayWidth / 2 - 192, displayHeight / 2.25)
diffExtremeCoord = (displayWidth / 2 - 154, displayHeight / 2.08)
#459

askingDifficulty = True
while askingDifficulty:
    pos = pygame.mouse.get_pos()
    #Plec
    if pos[0] > diffPlebCoord[0] and pos[0] < diffPlebCoord[0] + 252 and pos[1] > diffPlebCoord[1] and pos[1] < diffPlebCoord[1] + 25 and pygame.mouse.get_pressed()[0] == 1:
        xp1, yp1, up1, ap = [], 0, 30, 30 #projectile variables. xp1 list coz multiple projectiles
        xws, yws, uws, xwsDicrease = random.randint(50, displayWidth - 50), 0, 50, 0 #wallSpace variables. xws is the x coordinate of the space in the wall
        xl, yl, ul, al = random.randint(0, displayWidth - 50), 0, 30, 30 #life variables
        upc, apc, uwsc, xwsDc = 0.5, 4, 5, 5 
        lives = 5
        maxLives = 5
        liveSpawnChance = 0.01
        askingDifficulty = False
        playing = True
        numOfProjectiles = 15
        inc_numOfProjectiles = 2
        #adding random locations for projectiles to spawn in
        for _ in range(numOfProjectiles):
            xp1.append(random.randint(0,displayWidth)) 

    #Easy
    if pos[0] > diffEasyCoord[0] and pos[0] < diffEasyCoord[0] + 164 and pos[1] > diffEasyCoord[1] and pos[1] < diffEasyCoord[1] + 25 and pygame.mouse.get_pressed()[0] == 1:
        xp1, yp1, up1, ap = [], 0, 50, 50 #projectile variables. xp1 list coz multiple projectiles
        xws, yws, uws, xwsDicrease = random.randint(50, displayWidth - 50), 0, 70, 0 #wallSpace variables. xws is the x coordinate of the space in the wall
        xl, yl, ul, al = random.randint(0, displayWidth - 50), 0, 50, 50 #life variables
        upc, apc, uwsc, xwsDc = 0.55, 5, 7, 7 
        lives = 5
        maxLives = 5
        liveSpawnChance = 0.005
        askingDifficulty = False
        playing = True
        numOfProjectiles = 20
        inc_numOfProjectiles = 3
        #adding random locations for projectiles to spawn in
        for _ in range(numOfProjectiles):
            xp1.append(random.randint(0,displayWidth)) 

    #Medium
    if pos[0] > diffMediumCoord[0] and pos[0] < diffMediumCoord[0] + 264 and pos[1] > diffMediumCoord[1] and pos[1] < diffMediumCoord[1] + 25 and pygame.mouse.get_pressed()[0] == 1:
        xp1, yp1, up1, ap = [], 0, 70, 70 #projectile variables. xp1 list coz multiple projectiles
        xws, yws, uws, xwsDicrease = random.randint(50, displayWidth - 50), 0, 100, 0 #wallSpace variables. xws is the x coordinate of the space in the wall
        xl, yl, ul, al = random.randint(0, displayWidth - 50), 0, 60, 50 #life variables
        upc, apc, uwsc, xwsDc = 0.6, 7, 9, 9
        lives = 3
        maxLives = 5
        liveSpawnChance = 0.001
        askingDifficulty = False
        playing = True
        numOfProjectiles = 20
        inc_numOfProjectiles = 5
        #adding random locations for projectiles to spawn in
        for _ in range(numOfProjectiles):
            xp1.append(random.randint(0,displayWidth)) 

    #Hard. Only 1 life. Extra lives spawn rarely
    if pos[0] > diffHardCoord[0] and pos[0] < diffHardCoord[0] + 383 and pos[1] > diffHardCoord[1] and pos[1] < diffHardCoord[1] + 25 and pygame.mouse.get_pressed()[0] == 1:
        xp1, yp1, up1, ap = [], 0, 90, 90 #projectile variables. xp1 list coz multiple projectiles
        xws, yws, uws, xwsDicrease = random.randint(50, displayWidth - 50), 0, 150, 0 #wallSpace variables. xws is the x coordinate of the space in the wall
        xl, yl, ul, al = random.randint(0, displayWidth - 50), 0, 80, 50 #life variables
        upc, apc, uwsc, xwsDc = 0.65, 8, 10, 10 
        lives = 1
        maxLives = 3
        liveSpawnChance = 0.0008
        askingDifficulty = False
        playing = True
        numOfProjectiles = 20
        inc_numOfProjectiles = 5
        #adding random locations for projectiles to spawn in
        for _ in range(numOfProjectiles):
            xp1.append(random.randint(0,displayWidth)) 

    #Extreme. No extra lives spawn and start with only 1 life
    if pos[0] > diffExtremeCoord[1] and pos[0] < diffExtremeCoord[1] + 309 and pos[1] > diffExtremeCoord[1] and pos[1] < diffExtremeCoord[1] + 25 and pygame.mouse.get_pressed()[0] == 1:
        xp1, yp1, up1, ap = [], 0, 50, 50 #projectile variables. xp1 list coz multiple projectiles
        xws, yws, uws, xwsDicrease = random.randint(50, displayWidth - 50), 0, 200, 0 #wallSpace variables. xws is the x coordinate of the space in the wall
        xl, yl, ul, al = random.randint(0, displayWidth - 50), 0, 100, 50 #life variables
        upc, apc, uwsc, xwsDc = 0.8, 10, 12, 12
        lives = 1
        maxLives = 1
        liveSpawnChance = 0
        askingDifficulty = False
        playing = True
        numOfProjectiles = 25
        inc_numOfProjectiles = 6
        #adding random locations for projectiles to spawn in
        for _ in range(numOfProjectiles):
            xp1.append(random.randint(0,displayWidth))  
        
    display.fill(BLACK)
    display.blit(welcomeDisp, (displayWidth/2 - 230, displayHeight/8))
    display.blit(diffSay, (displayWidth/2 - 128, displayHeight/3.8))
    display.blit(diffPleb, diffPlebCoord)
    display.blit(diffEasy, diffEasyCoord)
    display.blit(diffMedium, diffMediumCoord)
    display.blit(diffHard, diffHardCoord)
    display.blit(diffExtreme, diffExtremeCoord)
    
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            askingDifficulty = False
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_ESCAPE:
                askingDifficulty = False
    
    pygame.display.update()
    clock.tick(FPS)
      

pygame.mouse.set_pos([displayWidth/2, displayHeight/1.1])
pygame.mouse.set_visible(False) #set cursor invisible
endTime = time.time()
#Main game loop
while playing:
    if stageActive == False:
        stages[random.randint(0,len(stages) - 1)] = True #selecting a random stage to start
        stageActive = True
    
    #filling the bgcolor first because other objects will overlap it
    display.fill(BGCOLOR)

    #taking dt to be a small value which will depend on the processing power
    startTime = time.time()
    t = startTime - endTime

    #ball coordinates = mouse coordinates
    (x, y) = pygame.mouse.get_pos()

    endTime = time.time()
    
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
            up1 = upc * up1
            ap += apc
            uws += uwsc #wall space vars increment
            if score != 0:
                xwsDicrease += xwsDc/score #wall space vars increment
            else:
                xwsDicrease += xwsDc #wall space vars increment the first time
            xp1 = []
            score += 1
            scoreDisp = myfontScore.render('SCORE: %s'%(score),False,WHITE)
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
                        playing = False
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
            uws += uwsc + 5
            if score != 0:
                xwsDicrease += (xwsDc + 2) / score
            else:
                xwsDicrease += (uwswDc + 5)
            up1 = upc * up1 #projectile vars increment
            ap += apc #projectile vars increment
            stageTimes += 1
            score += 1
            scoreDisp = myfontScore.render('SCORE: %s'%(score),False,WHITE)
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
            try:
                wsRightSurf = pygame.Surface(((displayWidth - xws - 100 + xwsDicrease), 50))
                wsRightSurf.fill(WS_COLOR)
                display.blit(wsRightSurf, ((xws + 100 - xwsDicrease), yws))
            except:
                pass
        
        if (x < (xws) and y > (yws) and y < (yws + 50)) or (x > (xws + 100 - xwsDicrease) and y > yws and y < (yws + 50)):
            if lives > 1:
                lives -= 1
            else:
                playing = False
                
            xws, yws = random.randint(50, displayWidth - 50), 0
            uws += 5

    #extra life falling
    if lives <= maxLives: #max no. of lives is 5. If lives less than max, extra life may fall.
        ran = random.random()
        if ran < liveSpawnChance:
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
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_ESCAPE:
                playing = False
        
    #displaying
    for g in range(lives): #displaying the current no. of lives as hearts
        display.blit(heart, (displayWidth - 50 - g * 25,25))
    if lifeFalling == True:
        display.blit(heart, [xl, yl])
    pygame.draw.circle(display, BALL_COLOR, (int(x),int(y)), 10, 0) #displaying the ball
    display.blit(scoreDisp,(displayWidth - 100, 50)) #displaying the score
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
print("Thanks for playing. Your score was " + str(score))

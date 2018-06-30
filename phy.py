import time
import random
import pygame
pygame.init()

#colors
black=(0,0,0)
white=(255,255,255)
red=(255,0,0)
green=(0,255,0)
blue=(0,0,255)
darkViolet=(148,0,211)

#display
displayWidth=1024
displayHeight=600
display=pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption('PHY')
heart=pygame.image.load('heart.png')
myfont=pygame.font.SysFont('Terminal', 18)
clock=pygame.time.Clock()
endTime=time.time()

#physics
x,y=displayWidth/2,displayHeight/2
ux, uy, ax, ay= 0, 0, 0, 0 # u means velocity, a  means acceleration
yp1, up1, ap = 0, 50, 50 #p for projectile
xp1,yp1,up1,ap1=[],0,50,50 #projectile variables. xp1 list coz multiple projectiles
uc, ac = 20, 5 # c stands for the amount of change on key press
score, lives=0,3
touching=False
running=True

#misc
projectile=pygame.Surface((10,20))
projectile.fill(darkViolet)

#adding random locations for projectiles to spawn in
for _ in range(20):
    xp1.append(random.randint(0,displayWidth))


while running:
    #taking dt to be a small value which will depend on the processing power
    startTime=time.time()
    t=startTime-endTime

    #changing the postions and velocities with time
    ux+=ax*t
    uy+=ay*t
    x+=ux*t
    y+=uy*t
    up1+=ap*t
    yp1+=up1*t

    endTime=time.time()
    
    #checking for collision of ball with boundaries
    if x<0:
        x=0
        ux=-ux/3
    if x>displayWidth:
        x=displayWidth
        ux=-ux/3
    if y<0:
        y=0
        uy=-uy/3
    if y>displayHeight:
        y=displayHeight
        uy=-uy/3
    
    
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running=False
        elif ev.type == pygame.KEYDOWN: #acts on pressing and not on holding key
            if ev.key == pygame.K_UP:
                ay-=ac
                uy-=uc
            if ev.key == pygame.K_DOWN:
                ay+=ac
                uy+=uc
            if ev.key == pygame.K_LEFT:
                ax-=ac
                ux-=uc
            if ev.key == pygame.K_RIGHT:
                ax+=ac
                ux+=uc
        elif ev.type == pygame.KEYUP:
            if ev.key == pygame.K_UP:
                ay=0
            if ev.key == pygame.K_DOWN:
                ay=0
            if ev.key == pygame.K_LEFT:
                ax=0
            if ev.key == pygame.K_RIGHT:
                ax=0

    #condition for when the projectile crosses the screen
    if yp1>displayHeight:
        yp1=0
        up1=3*up1/5
        ap+=5
        xp1=[]
        score+=1
        for _ in range(20):
            xp1.append(random.randint(0,displayWidth))

    #checking for collision between ball and projectile
    for g in range(20):
        if x>xp1[g]-10 and x<10+xp1[g] and y>yp1-15 and y<yp1+15:
            touching=True
            xp1[g]=1050
    if touching:
        if lives>1:
            lives-=1
            touching=False
        else:
            running=False

    #displaying
    display.fill(black)
    for g in range(lives): #displaying the lives as hearts
        display.blit(heart, (950+g*25,25))
    for g in range(20): #displaying the same projectile at 20 places
        display.blit(projectile, (xp1[g], yp1))
    textDisp=myfont.render('SCORE: %s'%(score),False,white)
    pygame.draw.circle(display, red, (int(x),int(y)), 10, 0) #displaying the ball
    display.blit(textDisp,(950,50)) #displaying the score
    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()

  

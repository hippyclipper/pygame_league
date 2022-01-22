import pygame
import random
import math 
import sys

#hippyclipper

#==================================================

def overLap(x1, y1, r1, x2, y2, r2):
    distSq = (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)
    radSumSq = (r1 + r2) * (r1 + r2)
    if (distSq == radSumSq):
        return True
    elif (distSq > radSumSq):
        return False
    return True

#==================================================
class minionTimer:
    def __init__(self, period):
        self.period = period
        self.tickNum = 1
        self.trigger = False
        
    def checkTimer(self):
        if self.tickNum % self.period == 0:
            self.tickNum = 1
            self.trigger = True
        else:
            self.trigger = False

        
    def getFrameTimer(self):
        self.tickNum += 1
        self.checkTimer()
        return self.trigger
    
class Ship:
    
    def __init__(self,x, y):
        self.w = int(.03 * width)
        self.h = int(.03 * height)
        self.x = x
        self.y = y
        self.speed = int(.002 * width) + 1
        self.destX = x
        self.destY = y
        self.xv = 0
        self.yv = 0
        self.drawDest = True
        self.color = (0,0,255)
        
    def setLocation(self, newX, newY):
        self.destX = newX
        self.destY = newY
                
        distX = self.x - newX 
        distY = self.y - newY 
        
        distTotal = math.sqrt(distX**2 + distY**2)
        
        precentX = distX / distTotal
        precentY = distY / distTotal
        
        newXV = precentX * -1
        newYV = precentY * -1 
        
        self.xv = newXV
        self.yv = newYV
        
    def drawMarker(self):
        pygame.draw.circle(screen, (255, 100, 251), (int(self.destX), int(self.destY)), int(self.w/5)+1)
        
    def checkLocation(self):
        if(overLap(self.x, self.y, int(self.w/3)+1, self.destX, self.destY, int(self.w/5)+1)):
            self.xv = 0
            self.yv = 0
            return
        
        if self.drawDest:
            self.drawMarker()
            
        self.x += self.xv * self.speed
        self.y += self.yv * self.speed
        
    def drawShip(self):
        self.checkLocation()
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.w))
    
    def draw(self):
        self.drawShip()
        
#==================================================

class Bullet(Ship):
    
    def __init__(self, x, y, destX, destY):
            super().__init__(x, y)   
            self.drawDest = False
            self.w /= 3
            self.h /= 3
            self.speed *= 3
            self.setLocation(destX, destY)
            self.damage = 30
            
    def checkLocation(self):
        if(self.x > width or self.x < 0 or self.y > height or self.y < 0):
            self.xv = 0
            self.yv = 0
            return
        
        if self.drawDest:
            self.drawMarker()
            
        self.x += self.xv * self.speed
        self.y += self.yv * self.speed
            
#==================================================

class Turret(Ship):
    
    def __init__(self, x, y):
        super().__init__(x, y)   
        self.drawDest = False
        self.w *= 3
        self.h *= 3
        self.speed = 0
        self.maxHealth = 1000
        self.health = self.maxHealth
        self.range = 100
            
    def drawHealth(self):
        if self.health < 0:
            return
        x = int(self.x - self.w)
        y = int(self.y - self.w - self.w/10)
        w = int(self.w*2) * self.health / self.maxHealth
        h = int(self.w/10)
        healthBar = pygame.Rect(x, y, w, h)
        pygame.draw.rect(screen, RED, healthBar)
        
    def hitTurret(self, damage):
        self.health -= damage
               
    def draw(self):
        self.drawHealth()
        self.drawShip()
           
class Minion(Turret):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.w /= 5
        self.speed = int((.003 * width)/2) + 1
        self.maxHealth = 100
        self.health = self.maxHealth
        self.color = (255,0,0)
                        
#==================================================
            
#constants
screenScale = 8
width = int(100 * screenScale)
height = width
UP = -1
DOWN = 1
RED = (255,0,0)
BLUE = (0,0,255)
LEFT_MOUSE = 1
RIGHT_MOUSE = 3

#init code
pygame.init()
pygame.mixer.init()
pygame.font.init()
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()

#game states
last = None
start = False
end = False
win = False
done = False

#game objects
projectiles = []
player = Ship(width - int(width/20), int(height/20))
turrets = [Turret(0, height), Turret(0, height/2), Turret(width/2, height), Turret(width - math.sqrt((2*(width/2)**2)), math.sqrt(2*(height/2)**2))]
for turret in turrets:
    turret.x += turret.w
    turret.y -= turret.w
minions = [Minion(0, height)]
x, y = 0, 0
spawnTimer = minionTimer(75)
spawn = False
#==================================================

while not done:
    
    pressed = pygame.key.get_pressed()
    spawn = spawnTimer.getFrameTimer()
    if len(turrets) == 0:
        sys.exit(0)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            pass
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            pass
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            pass
        if event.type == pygame.MOUSEBUTTONDOWN and event.button ==  RIGHT_MOUSE:           
            x, y = pygame.mouse.get_pos()
            player.setLocation(x,y)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT_MOUSE:
            x, y = pygame.mouse.get_pos()
            projectiles.append(Bullet(player.x, player.y, x, y))
            
#==================================================
#some logic
            
    if spawn:
        turretNum = random.randint(0,len(turrets)-1)
        minions.append(Minion(turrets[turretNum].x, turrets[turretNum].y))
        if spawnTimer.period - 30 > 0:
            spawnTimer.period -= 0
                      
#==================================================
#draw section
            
    for projectile in projectiles:
        if projectile.xv == 0 and projectile.yv == 0:
            projectiles.remove(projectile)
        projectile.draw()

    for minion in minions:
        if minion.health <= 0:
            minions.remove(minion)
        else:
            minion.setLocation(player.x, player.y)
                
    for turret in turrets:
        if turret.health <= 0:
            turrets.remove(turret)
        else:
            turret.setLocation(player.x, player.y)
        
    for turret in turrets+minions:
        for projectile in projectiles:
            if overLap(projectile.x, projectile.y, projectile.w, turret.x, turret.y, turret.w):
                turret.hitTurret(projectile.damage)
                projectiles.remove(projectile)
        turret.draw()
        
    for minion in minions:
        if overLap(player.x, player.y, player.w, minion.x, minion.y, minion.w):
            sys.exit(0)
        
    player.draw()
       
#==================================================
#frame end
    
    pygame.display.flip()
    clock.tick(60)
    screen.fill((0, 0, 0))

#==================================================
#shutdown

pygame.display.quit()
pygame.quit()

#==================================================

#if pressed[pygame.K_LEFT]:
#x, y = pygame.mouse.get_pos()
#print(x, y)


        
        
        
        
        

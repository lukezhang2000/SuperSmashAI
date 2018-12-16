import pygame
from Surface import *
import math
import random
class Character(pygame.sprite.Sprite):
    def __init__(self, screen):
        self.width = 600
        self.height = 400
        self.health = 100
        self.speed = 5
        self.jumpSpeed = 13
        self.attackSpeed = 20
        self.closeDamage = 40
        self.rangeDamage = 20
        self.closeDamageInit = self.closeDamage
        self.rangeDamageInit = self.rangeDamage
        self.fallSpeed = self.jumpSpeed/30
        self.state = 0
        self.characterX = int(self.width/15)
        self.characterY = int(self.height/8)
        self.sphereRad = int(self.width/40)
        self.charHandX = self.width/20
        self.charHandY = self.height/40
        self.posX = self.width/6
        self.posY = 230 * self.height/400
        self.resetX = self.width/2-self.characterX/2
        self.resetY = 100
        self.time = 0
        self.bullets = []
        self.screen = screen
        self.surface = Surface(self.screen)
        self.lives = 3
        self.health = 0
        self.jumpCount = 0
        self.jumpLimit = 2
        self.attackTime = 0
        self.attackTimeDelay = 2
        self.attackVelX = self.width/100
        self.attackVelY = self.height/40
        self.rangeReloadTime = 24
        self.closeReloadTime = 4
        self.rangeSwitchTime = 8
        self.closeSwitchTime = 8
        self.onSurface = True
        self.onLeftPlatform = False
        self.onRightPlatform = False
        self.onTopPlatform = False
        self.onBottomPlatform = True
        self.airTime = 0
        #self.charAngles = [-20, 0, 20, 40, 60]
        self.angles = [0, -20, 20, 40, 60]
        self.angleIndex = 1
        self.isStunned = False
        self.stunTime = 0
        self.stunLimit = 40
        self.choices = [True, False]
        self.gravity = 9.8/10
        self.aiDelay = 1.4
        self.rangeKnockbackConstant = .08
        self.closeKnockbackConstant = .1
        self.weightConstant = 1
        self.coolDownTime = 0
        #self.jump
        self.jumpReloadTime = 6
        self.isJumping = False
        self.xVelocity = 0
        self.yVelocity = 0
        self.knockbackSpeed = 10
        self.knockbackAngle = 20
        self.isLucario = False
        self.isBowser = False
        self.isPikachu = False
        self.isPit = False
        self.closeLoadTime = 0
        self.closeLoadLimit = 24
        self.triedToAttack = False
        self.dealtDamage = False
        self.isBoosted = False
        self.boostTime = 0
        self.boostLimit = 60
        
        #self.stand = True
        #self.hitBox = pygame.Rect(self.posX,self.posY,self.characterX,self.characterY)
        #self.hitBox2 = pygame.Rect(self.posX,self.posY,self.characterX,self.characterY)
        #self.hitBoxes = [self.hitBox, self.hitBox2]
        
        self.standingSprite = None
        self.jumpingSprite = None
        self.runSpriteSheet = None
        self.meleeSpriteSheet = None
        self.rangeSpriteSheet = None
        self.runSpriteIndex = 0
        
        self.bulletImage = None
        self.runImages = []
        self.jumpImage = None
        self.punchImage = None
        self.rangeImage = None
        self.loadedRunImages = []
        
    '''def getImage(self, x, y, width, height):
        
        image = pygame.Surface([width, height]).convert()
        
        image.blit(self.)'''
        
        
    #moves the sprite by its speed, and moves based on x direction  
    def draw(self):
        '''if self.state != 0 and self.state != 3 and self.state != 6 and self.state != 7:
            for image in self.images:
                self.loadedImages.append(pygame.transform.scale(pygame.image.load(image),(self.characterX,self.characterY)))
            image = self.loadedImages[self.state]'''
        #self.screen.blit(pygame.transform.scale(pygame.image.load(self.runImages[0]),(self.characterX,self.characterY)), (2*self.posX, self.posY))
        
        if self.state == 0:
            if self.isJumping:
                image = pygame.transform.scale(pygame.image.load(self.jumpImage),(self.characterX,self.characterY))
            else:
                for image in self.runImages:
                    self.loadedRunImages.append(pygame.transform.scale(pygame.image.load(image),(self.characterX,self.characterY)))
                image = self.loadedRunImages[self.runSpriteIndex%len(self.loadedRunImages)]
        if self.state == 1:
            image = image = pygame.transform.scale(pygame.image.load(self.rangeImage),(self.characterX,self.characterY))
        if self.state == 2:
            image = pygame.transform.scale(pygame.image.load(self.punchImage),(self.characterX,self.characterY))
        if self.state == 3:
            if self.isJumping:
                image = pygame.transform.flip(pygame.transform.scale(pygame.image.load(self.jumpImage),(self.characterX,self.characterY)), True, False)
            else:
                for image in self.runImages:
                    self.loadedRunImages.append(pygame.transform.scale(pygame.image.load(image),(self.characterX,self.characterY)))
                image = pygame.transform.flip(self.loadedRunImages[self.runSpriteIndex%len(self.loadedRunImages)], True, False)
        if self.state == 4:
            image = pygame.transform.flip(pygame.transform.scale(pygame.image.load(self.rangeImage),(self.characterX,self.characterY)), True, False)     
        if self.state == 5:
            image = pygame.transform.flip(pygame.transform.scale(pygame.image.load(self.punchImage),(self.characterX,self.characterY)), True, False)
        self.screen.blit(image, (self.posX, self.posY))
        for bullet in self.bullets:
            if bullet[2] == True:
                self.screen.blit(self.bulletImage, (bullet[0]-self.sphereRad/2,bullet[1]-self.sphereRad/2))
            else:
                self.screen.blit(pygame.transform.flip(self.bulletImage, True, False), (bullet[0]-self.sphereRad/2,bullet[1]-self.sphereRad/2))
            
    def move(self, right):
        if self.isStunned == False:
            self.runSpriteIndex += 1
            if right == True:
                self.state = 0
                self.posX += self.speed
                #print(self.posX)
            else: 
                self.state = 3
                self.posX -= self.speed
                
    #makes sprite jump by adjusting velocity
    def jump(self):
        if self.isStunned == False and self.triedToAttack == False:
            #if self.onSurface == True:
            if self.jumpCount <= self.jumpLimit:
                self.airTime = 0
                self.yVelocity = self.jumpSpeed
                self.isJumping = True
                self.jumpCount += 1
                if self.isPit:
                    self.runSpriteIndex += 1
                #self.posX -= self.jumpSpeed
                if self.state == 0 or self.state == 1 or self.state == 2:
                    self.state = 0
                elif self.state == 3 or self.state == 4 or self.state == 5:
                    self.state = 3
                    
    #shoots a ranged attack, default angle is 0 but Pit can change angles
    def rangeAttack(self, angle=0):
        if self.isStunned == False and self.triedToAttack == False:
            if self.state == 0 or self.state == 1 or self.state == 2:
                self.state = 1
                self.bullets.append([self.posX+self.charHandX/2 + self.sphereRad/2, self.posY+self.charHandY + self.sphereRad/2, True, 0, self.angles[self.angleIndex]])
            elif self.state == 3 or self.state == 4 or self.state == 5:
                self.state = 4
                self.bullets.append([self.posX+self.charHandX/2 - self.sphereRad/2, self.posY+self.charHandY + self.sphereRad/2, False, 0, self.angles[self.angleIndex]])
            self.attackTime = 0
            self.coolDownTime = 0
            #self.stand = False
            
    #launches a close, melee attack 
    def closeAttack(self):
        if self.isStunned == False:
            if self.state == 0 or self.state == 1 or self.state == 2:
                #if self.closeLoadTime >= self.closeLoadLimit:
                self.state = 2
            elif self.state == 3 or self.state == 4 or self.state == 5:
                #if self.closeLoadTime >= self.closeLoadLimit:
                self.state = 5
            self.attackTime = 0
            self.coolDownTime = 0
    # helper function for AI, dodges bullets that are near by jumping
    def dodgeBullets(self, other):
        for bullet in other.bullets:
            if abs(bullet[0]-self.posX)<=4*other.attackSpeed and abs(bullet[1]-self.posY) <= self.characterY:
                #self.posY -= 40
                if self.isStunned == False:
                    self.yVelocity = 14
                #self.jump()
                
                return
                
    #checks to see if sprite is stunned and runs the duration of the stun
    def checkStun(self):
        if self.isStunned:
            self.stunTime += 1
            if self.stunTime >= self.stunLimit:
                self.isStunned = False
                self.stunTime = 0
    def checkBoost(self):
        if self.isBoosted:
            self.rangeDamage = int(1.5 * self.rangeDamageInit)
            self.closeDamage = int(1.5 * self.closeDamageInit)
            self.boostTime += 1
            if self.boostTime >= self.boostLimit:
                self.isBoosted = False
                self.stunTime = 0
                self.rangeDamage = self.rangeDamageInit
                self.closeDamage = self.closeDamageInit
                
    #changes y velocity based on time and gravity if sprite is in air
    def fallGravity(self):
        if self.isJumping or self.onSurface == False:
            self.yVelocity -=.5*self.gravity * self.airTime
            
    #checks to see what platform the sprite is currently on
    def checkSurface(self):
        leftPlatformRect = pygame.Rect(self.surface.leftBox[0],self.surface.leftBox[1],self.surface.leftBox[2],self.surface.leftBox[3])
        rightPlatformRect = pygame.Rect(self.surface.rightBox[0],self.surface.rightBox[1],self.surface.rightBox[2],self.surface.rightBox[3])
        topPlatformRect = pygame.Rect(self.surface.topBox[0],self.surface.topBox[1],self.surface.topBox[2],self.surface.topBox[3])
        bottomPlatformRect = pygame.Rect(self.surface.bottomBox[0],self.surface.bottomBox[1],self.surface.bottomBox[2],self.surface.bottomBox[3])
        charRect = pygame.Rect(self.posX,self.posY,self.characterX,self.characterY)
        if charRect.colliderect(leftPlatformRect) and abs(self.posY-self.surface.leftBox[1]) <= self.height/80:
            self.onLeftPlatform = True
            self.onRightPlatform, self.onTopPlatform, self.onBottomPlatform = False, False, False
        elif charRect.colliderect(rightPlatformRect) and abs(self.posY-self.surface.rightBox[1]) <= self.height/80:
            self.onRightPlatform = True
            self.onLeftPlatform, self.onTopPlatform, self.onBottomPlatform = False, False, False
        elif charRect.colliderect(topPlatformRect) and abs(self.posY-self.surface.topBox[1]) <= self.height/80:
            self.onTopPlatform = True
            self.onLeftPlatform, self.onBottomPlatform, self.onRightPlatform = False, False, False
        elif charRect.colliderect(bottomPlatformRect) and abs(self.posY-self.surface.bottomBox[1]) <= self.height/80:
            self.onLeftPlatform, self.onRightPlatform, self.onTopPlatform = False, False, False
            self.onBottomPlatform = True
        else:
            self.onLeftPlatform, self.onRightPlatform, self.onTopPlatform, self.onBottomPlatform = False, False, False, False
            
    #checks to see if sprite is on surface and resets airTime to 0 if so
    def ifOnSurface(self):
        if self.onBottomPlatform or self.onTopPlatform or self.onLeftPlatform or self.onRightPlatform:
            self.onSurface = True
            #self.stand = True
            self.airTime = 0
        else:
            self.onSurface = False
    #switches sprite back to original position after performing an attack
    def switchBack(self):
        if self.attackTime > self.closeSwitchTime and (self.state == 2):
            self.state = 0
            self.attackTime = 0
            self.dealtDamage = False
            #self.stand = True
        elif self.attackTime > self.closeSwitchTime and (self.state == 5):
            self.state = 3
            self.attackTime = 0
            self.dealtDamage = False
            #self.stand = True
        if self.attackTime > self.rangeSwitchTime and (self.state == 1):
            self.state = 0
            self.attackTime = 0
            
            #self.stand = True
        elif self.attackTime > self.rangeSwitchTime and (self.state == 4):
            self.state = 3
            self.attackTime = 0
            #self.stand = True
    #adjusts the lives and health of a sprite if knocked off screen
    def checkBounds(self):
        if self.posX + self.characterX <= 0 or self.posX >= self.width + self.characterX or self.posY <= -4*self.characterY or self.posY >= self.height:
            self.lives -= 1
            self.health = 0
            self.posY = self.resetY
            self.posX = self.resetX
            self.onBottomPlatform = True
            self.yVelocity = 0
            self.xVelocity = 0
            self.airTime = 0
    
    
    '''def checkValidFall(self):
        if self.posY <= self.surface.leftBox[1]:
            if self.posY - self.yVelocity >= self.surface.leftBox[1]:
                if self.surface.leftBox[0] - self.characterX <= self.posX <= self.surface.leftBox[0] + self.surface.leftBox[2] or self.surface.rightBox[0] - self.characterX <= self.posX <= self.surface.rightBox[0] + self.surface.rightBox[2]:
                    self.posY = self.surface.leftBox[1]'''
                    
    #checks for collisions of bullets to other sprites and platforms
    #also updates positions of bullets                
    def checkBullets(self, other):
        angleChar = self.angles[self.angleIndex]*math.pi/180
        knockbackAngle = other.knockbackAngle * math.pi/180
        otherRect = pygame.Rect(other.posX,other.posY,other.characterX,other.characterY)
        for bullet in self.bullets:
            bullet[3] += 1
            angleChar = bullet[4]*math.pi/180
            #uses projectile motion if opponent is Pit
            if self.isPit:
                #print(bullet[4],(self.attackSpeed * math.sin(angleChar) - bullet[3]*self.gravity))
                bullet[1] -= (self.attackSpeed * math.sin(angleChar) - bullet[3]*self.gravity)
            
            #changes the x positions of the bullets
            if bullet[2] == True:
                bullet[0] += self.attackSpeed * math.cos(angleChar)
                bulletRect = pygame.Rect(bullet[0]-self.sphereRad/2,bullet[1] - self.sphereRad/2 ,self.sphereRad,self.sphereRad)
            elif bullet[2] == False:
                bullet[0] -= self.attackSpeed * math.cos(angleChar)
                bulletRect = pygame.Rect(bullet[0]+self.sphereRad/2,bullet[1] - self.sphereRad/2 ,self.sphereRad,self.sphereRad)
            #if other.hitBoxes[0].colliderect(bulletRect) or other.hitBoxes[1].colliderect(bulletRect):
            if bullet[0] > self.width or bullet[0] < -self.sphereRad/2:
                self.bullets.remove(bullet)
            #causes damage and knockback if bullet hits sprite, removes bullet after
            if otherRect.colliderect(bulletRect):
                if bullet[3] >= 2:
                    damage = int(self.rangeDamage * 5/(bullet[3]+1))
                else: 
                    damage = int(self.rangeDamage * 5/3)
                other.health += damage
                if self.posX < other.posX:
                    other.xVelocity = other.health * self.rangeKnockbackConstant * other.weightConstant * math.cos(knockbackAngle)
                    #other.posX+=other.health * self.rangeKnockbackConstant * other.weightConstant
                else:
                    other.xVelocity = -other.health * self.rangeKnockbackConstant * other.weightConstant * math.cos(knockbackAngle)
                    #other.posX-=other.health * self.rangeKnockbackConstant * other.weightConstant
                
                other.yVelocity = other.health * self.rangeKnockbackConstant * other.weightConstant * math.sin(knockbackAngle) - other.airTime * other.gravity
                other.onLeftPlatform, other.onRightPlatform, other.onTopPlatform, other.onBottomPlatform = False, False, False, False
                if self.isPikachu:
                    if other.isStunned == False:
                        other.isStunned = random.choice(self.choices)
                try:
                    self.bullets.remove(bullet)
                except:
                    return
            #removes bullets if they collide with surface
            for ground in self.surface.surfaces2:
                groundRect = pygame.Rect(ground[0],ground[1],ground[2],ground[3])
                if groundRect.colliderect(bulletRect):
                    try:
                        self.bullets.remove(bullet)
                    except:
                        return
    #helper for the charge-up time for melee attacks
    def closeAttackDelay(self):
        if self.triedToAttack and self.closeLoadTime >= self.closeLoadLimit:
            self.closeAttack()
            self.closeLoadTime = 0
            self.triedToAttack = False
    def checkMelee(self, other):
        knockbackAngle = other.knockbackAngle * math.pi/180
        otherRect = pygame.Rect(other.posX,other.posY,other.characterX,other.characterY)
        playerRect = pygame.Rect(self.posX,self.posY,self.characterX,self.characterY)
        if otherRect.colliderect(playerRect) == True:
            if self.state == 2 and other.posX - other.characterX<=self.posX <= other.posX + other.characterX:
                if self.dealtDamage == False:
                    other.health += self.closeDamage
                    self.dealtDamage = True
                other.xVelocity = other.health * self.closeKnockbackConstant * other.weightConstant * math.cos(knockbackAngle)
                other.yVelocity = other.health * self.closeKnockbackConstant * other.weightConstant * math.sin(knockbackAngle) - other.airTime * other.gravity
            if self.state == 5 and other.posX - other.characterX <= self.posX <= other.posX + other.characterX:
                if self.dealtDamage == False:
                    other.health += self.closeDamage
                    self.dealtDamage = True
                other.xVelocity = -other.health * self.closeKnockbackConstant * other.weightConstant * math.cos(knockbackAngle)
                other.yVelocity = other.health * self.closeKnockbackConstant * other.weightConstant * math.sin(knockbackAngle) - other.airTime * other.gravity
            '''if other.state == 2 and self.posX - self.characterX<=other.posX <= self.posX + self.characterX:
                self.health += other.closeDamage
                self.posX += self.health * other.closeKnockbackConstant * self.weightConstant
            if other.state == 5 and self.posX - self.characterX <= other.posX <= self.posX + self.characterX:
                self.health += other.closeDamage
                self.posX-=self.health * other.closeKnockbackConstant * self.weightConstant'''
        
        
    def makeMove(self):
        return
import pygame
from Character import *
from Surface import *
from supersmash import *
import math
class Pit(Character):
    def __init__(self, screen):
        super().__init__(screen)
        self.images = ["images/pitrun.png","images/pitrange.png","images/pitclose.png","images/pitrunleft.png","images/pitrangeleft.png","images/pitcloseleft.png"]
        self.bulletImage = pygame.transform.scale(pygame.image.load("images/arrow.png"),(self.sphereRad,self.sphereRad))
        #self.runImages = ["images/pipR1.png", "images/pipR2.png", "images/pipR3.png", "images/pipR4.png"]
        self.runImages = ["images/PW1.png", "images/PW2.png", "images/PW3.png", "images/PW4.png", "images/PW5.png", "images/PW6.png"]
        self.jumpImage = "images/pitjump.png"
        self.punchImage = "images/pitpunch.png"
        self.rangeImage = "images/pitrange0.png"
        self.loadedRunImages = []
        self.closeDamage = 28
        self.rangeDamage = 31
        self.closeDamageInit = self.closeDamage
        self.rangeDamageInit = self.rangeDamage
        self.speed = 3
        self.weightConstant = .9
        self.isValidAttack = True
        self.closeLoadLimit = 8
        self.closeReloadTime = 20
        self.rangeReloadTime = 20
        
        

            
    #checks to see if bullet will go underneath platform using projectile motion
    def checkUnderCollision(self, surface, angle):
        distY = abs((self.posY+self.charHandY)- (surface[1] + surface[3]) + self.sphereRad/2)
        angleRad = angle * math.pi/180
        maxHeight = ((self.attackSpeed * math.sin(angleRad))**2)/(2*self.gravity)
        if maxHeight >= distY:
            return True
        else:
            return False
    #checks collisions (against left side of surfaces) for bullets that shoot right and upwards using projectile motion
    def checkUpLeftCollision(self, surface, angle):
        distX, distY = abs(self.posX+self.charHandX/2-surface[0]+self.sphereRad), (self.posY+self.charHandY)- surface[1] + self.sphereRad
        angleRad = angle * math.pi/180
        time = distX/(self.attackSpeed * math.cos(angleRad))
        print(angle,distX,abs(-.5*self.gravity*(time**2) + self.attackSpeed*math.sin(angleRad)*time), distY)
        if abs(-.5*self.gravity*(time**2) + self.attackSpeed*math.sin(angleRad)*time) < distY + .5:
            return True
        else:
            return False
    #checks collisions (against right side of surfaces) for bullets that shoot left and upwards using projectile motion
    def checkUpRightCollision(self, surface, angle):
        distX, distY = abs(self.posX+self.charHandX/2-(surface[0]+surface[2])), abs((self.posY+self.charHandY)- surface[1] + self.sphereRad)
        
        angleRad = angle * math.pi/180
        time = distX/(self.attackSpeed * math.cos(angleRad))
        print(angle,distX,abs(-.5*self.gravity*(time**2) + self.attackSpeed*math.sin(angleRad)*time), distY)
        if abs(-.5*self.gravity*(time**2) + self.attackSpeed*math.sin(angleRad)*time) < distY + .5:
            return True
        else:
            return False
    #checks collisions (against left side of surfaces) for bullets that shoot right and downwards using projectile motion
    def checkDownLeftCollision(self, surface, angle):
        distX, distY = abs(self.posX+self.charHandX/2-surface[0]), abs(surface[1] + surface[3] - (self.posY+self.charHandY))
        angleRad = angle * math.pi/180
        time = distX/(self.attackSpeed * math.cos(angleRad))
        if abs(-.5*self.gravity*(time**2) + self.attackSpeed*math.sin(angleRad)*time) < distY + .5:
            return True
        else:
            return False
    #checks collisions (against right side of surfaces) for bullets that shoot left and downwards using projectile motion
    def checkDownRightCollision(self, surface, angle):
        distX, distY = abs(self.posX+self.charHandX/2-(surface[0]+surface[2])), abs(surface[1] + surface[3] - (self.posY+self.charHandY))
        angleRad = angle * math.pi/180
        time = distX/(self.attackSpeed * math.cos(angleRad))
        if abs(-.5*self.gravity*(time**2) + self.attackSpeed*math.sin(angleRad)*time) < distY + .5:
            return True
        else:
            return False
    '''def canMove(self, other):
        distX1, distY1 = abs(other.posX + other.characterX - self.posX - self.charHandX/2), -(other.posY + other.characterY - self.charHandY - self.posY)
        #distX2, distY2 = abs(other.posX - self.posX - self.charHandX/2), -(other.posY - self.charHandY - self.posY)
        for i in range(len(self.angles)):
            angleRad = self.angles[i] * math.pi/180
            time1 = distX1/(self.attackSpeed * math.cos(angleRad))
            #time2 = distX2/(self.attackSpeed * math.cos(angleRad))
            if distY1+2*self.characterY>-.5*self.gravity*(time1**2) + self.attackSpeed*math.sin(angleRad)*time1 > distY1:
                return [i, True]
                #self.isValidAttack = True'''
        #return [None, False]
        
#returns the lowest possible angle in absolute value
#The reasoning for returning the lowest possible angle is because ranged attacks 
#lose damage over time, the lower the angle, the less time traveled for the 
#bullet in the air (since time is inversely proportional to cosine)
    def canMove(self, other):
        distX, distY = abs(other.posX-self.posX), (self.posY - other.posY)
        for i in range(len(self.angles)):
            angleRad = self.angles[i] * math.pi/180
            time = distX/(self.attackSpeed * math.cos(angleRad))
            if distY-self.characterY*2/3 <= -.5*self.gravity*(time**2) + self.attackSpeed*math.sin(angleRad)*time <= distY + self.characterY *2/3:
                return [i, True]
                #self.isValidAttack = True
        return [None, False]
        
    #AI system for Pit
    def makeMove(self,other):
        self.dodgeBullets(other)
        if abs(self.posY - other.posY) <= self.height/40:
            #cases when opponent and player have same y coordinate

            if self.onRightPlatform:
                self.state = 3
                #shoots if move is valid and does not collide with surface
                if self.canMove(other)[1]==True and self.checkUpRightCollision(self.surface.topBox2, self.angles[self.canMove(other)[0]])==False:
                    #attack cycles for the range reload time, and AI has a delay
                    if self.attackTime >= self.rangeReloadTime*self.aiDelay:
                        self.angleIndex = self.canMove(other)[0]
                        self.rangeAttack(self.angles[self.angleIndex])
                else:
                    #otherwise sprite moves back
                    if self.posX >= self.surface.leftBox[0] + 1.5*self.speed:
                        self.move(False)
                        #self.state = 1
            elif self.onLeftPlatform:
                self.state = 0
                if self.canMove(other)[1]==True and self.checkUpLeftCollision(self.surface.topBox2, self.angles[self.canMove(other)[0]])==False:
                    if self.attackTime >= self.rangeReloadTime*self.aiDelay:
                        self.angleIndex = self.canMove(other)[0]
                        self.rangeAttack(self.angles[self.angleIndex])
                else:
                    if self.posX >= self.surface.leftBox[0] + 1.5*self.speed:
                        self.move(False)
                        #self.state = 1
            #case where player and opponent are very close (melee attacks)
            if abs(self.posX-other.posX) < self.characterX/2:
                if self.posX < other.posX:
                    if other.triedToAttack == False:
                        self.move(True)
                    self.state = 0
                    #AI senses when player tries to attack and moves away
                    if other.triedToAttack and int(other.closeLoadLimit/4) <= other.closeLoadTime < other.closeLoadLimit:
                        if self.posX >= self.surface.bottomBox[0]+self.characterX+self.speed:
                            self.move(False)
                        if other.closeLoadTime == other.closeLoadLimit:
                            self.state = 0
                    elif self.attackTime >= self.closeReloadTime*self.aiDelay:
                        #self.triedToAttack = True
                        self.closeAttack()
                else:
                    if other.triedToAttack == False:
                        self.move(False)
                    self.state = 3
                    if other.triedToAttack and int(other.closeLoadLimit/4) <= other.closeLoadTime < other.closeLoadLimit:
                        if self.posX <= self.surface.bottomBox[0] + self.surface.bottomBox[2] - self.characterX+self.speed:
                            self.move(True)
                        if other.closeLoadTime == other.closeLoadLimit:
                            self.state = 3
                    if self.coolDownTime >= self.closeReloadTime*self.aiDelay:
                        #self.triedToAttack = True
                        self.closeAttack()
            else:
                if self.posX > other.posX:
                    self.state = 3
                else:
                    self.state = 0
                if self.coolDownTime >= self.rangeReloadTime*self.aiDelay:
                    #if self.onBottomPlatform and self.posX > other.posX
                    if self.canMove(other)[1] == True and self.checkUnderCollision(self.surface.leftBox2, self.angles[self.canMove(other)[0]])==False:
                        self.angleIndex = self.canMove(other)[0]
                        self.rangeAttack(self.angles[self.angleIndex])
                    else:
                        if self.posX > other.posX:
                            self.move(False)
                        else:
                            self.move(True)
        #case where player is above AI        
        elif self.posY > other.posY + self.height/40:
            #case with player on top platform
            if other.onTopPlatform:
                #if on bottom platform, the AI will move to the left/right platform
                if self.onBottomPlatform:
                    if self.posX <= self.surface.leftBox[0] - self.characterX + 1.5*self.speed:
                        self.move(True)
                    elif self.surface.leftBox[0]+self.surface.leftBox[2] - 1.5*self.speed <= self.posX < self.width/2:
                        self.move(True)
                    elif self.width/2 <= self.posX <= self.surface.rightBox[0] - self.characterX + 1.5*self.speed:
                        self.move(True)
                    elif self.posX >= self.surface.rightBox[0]+self.surface.rightBox[2] - 1.5*self.speed:
                        self.move(False)
                    else:
                        self.jump()
                elif self.onSurface == False:
                    if self.airTime > self.jumpReloadTime:
                        self.jump()
                else:
                    #if on left platform, the AI will repeatedly calculate if a move is possible, and if not, it will move further away from opponent
                    if self.onLeftPlatform:
                        self.state = 0
                        if self.canMove(other)[1]==True and self.checkUpLeftCollision(self.surface.topBox2, self.angles[self.canMove(other)[0]])==False:
                            if self.attackTime >= self.rangeReloadTime*self.aiDelay:
                                self.angleIndex = self.canMove(other)[0]
                                self.rangeAttack(self.angles[self.angleIndex])
                        else:
                            if self.posX >= self.surface.leftBox[0] + self.speed:
                                self.move(False)
                                #self.state = 1
                                
                    #if on right platform, the AI will repeatedly calculate if a move is possible and will move further from opponent if not
                    if self.onRightPlatform:
                        self.state = 3
                        if self.canMove(other)[1]==True and self.checkUpRightCollision(self.surface.topBox2, self.angles[self.canMove(other)[0]])==False:
                        #if self.isValidAttack:
                            if self.attackTime >= self.rangeReloadTime*self.aiDelay:
                                self.angleIndex = self.canMove(other)[0]
                                self.rangeAttack(self.angles[self.angleIndex])
                        else:
                            if self.posX <= self.surface.rightBox[0] + self.surface.rightBox[2] - 1.5*self.speed:
                                self.move(True)
                                #self.state = 1
                                
            #case where player is on the left platform
            elif other.onLeftPlatform: 
                #opponent will calculate if move is possible and adjust position if not
                if self.onBottomPlatform:
                    #will attempt to shoot if AI is in a reasonable position (not under platforms, etc)
                    if self.width/2 <= self.posX <= self.surface.rightBox[0] - self.characterX + 1.5*self.speed:
                        self.state = 3
                        if self.canMove(other)[1]==True and self.checkUpRightCollision(self.surface.leftBox2, self.angles[self.canMove(other)[0]])==False:
                            if self.attackTime >= self.rangeReloadTime*self.aiDelay:
                                self.angleIndex = self.canMove(other)[0]
                                self.rangeAttack(self.angles[self.angleIndex])
                        else:
                            self.move(True)
                    #otherwise, will move to a platform above or will move to good shooting position
                    elif self.posX >= self.surface.rightBox[0] + self.surface.rightBox[2] - 1.5*self.speed:
                        self.move(False)
                    elif self.surface.leftBox[0]+self.surface.leftBox[2]-1.5*self.speed < self.posX < self.width/2:
                        self.move(True)
                    elif self.posX <= self.surface.leftBox[0] - self.characterX + 1.5*self.speed:
                        self.move(True)
                    else:
                        self.jump()
                elif self.onSurface == False:
                    if self.airTime > self.jumpReloadTime:
                        self.jump()
                        
            #case where player is on right platform (similar to left platform)
            elif other.onRightPlatform:
                #opponent will calculate if move is possible and adjust position if not
                if self.onBottomPlatform:            
                    if self.surface.leftBox[0]+self.surface.leftBox[2]-1.5*self.speed < self.posX < self.width/2:
                        self.state = 0
                        if self.canMove(other)[1]==True and self.checkUpLeftCollision(self.surface.rightBox2, self.angles[self.canMove(other)[0]])==False:
                            if self.attackTime >= self.rangeReloadTime*self.aiDelay:
                                self.angleIndex = self.canMove(other)[0]
                                self.rangeAttack(self.angles[self.angleIndex])
                        else:
                            self.move(False)
                    elif self.posX <= self.surface.leftBox[0] - self.characterX + 1.5*self.speed:
                        self.move(True)
                    elif self.width/2 <= self.posX <= self.surface.rightBox[0] - self.characterX + 1.5*self.speed:
                        self.move(False)
                    elif self.posX >= self.surface.rightBox[0] + self.surface.rightBox[2] - 1.5*self.speed:
                        self.move(False)
                    else:
                        self.jump()
                elif self.onSurface == False:
                    if self.airTime > self.jumpReloadTime:
                        self.jump()
        else:
            if other.onBottomPlatform:
                if self.onLeftPlatform:
                    if self.posX < other.posX:
                        self.state = 0
                        if self.canMove(other)[1]==True and self.checkDownLeftCollision(self.surface.rightBox2, self.angles[self.canMove(other)[0]])==False:
                            if self.posX >= self.surface.leftBox2[0] + self.surface.leftBox2[2]/2:
                                if self.attackTime >= self.rangeReloadTime*self.aiDelay:
                                    self.angleIndex = self.canMove(other)[0]
                                    self.rangeAttack(self.angles[self.angleIndex])
                            else:
                                self.move(True)
                        else:
                            if self.posX <= self.surface.leftBox[0] + self.surface.leftBox[2]:
                                self.move(True)

                    else:
                        self.state = 3
                        self.move(True)
                elif self.onRightPlatform:
                    if self.posX > other.posX:
                        self.state = 3
                        if self.canMove(other)[1]==True and self.checkDownRightCollision(self.surface.leftBox2, self.angles[self.canMove(other)[0]])==False:
                            if self.posX <= self.surface.rightBox2[0] + self.surface.rightBox2[2]/2 - self.characterY:
                                
                                if self.attackTime >= self.rangeReloadTime*self.aiDelay:
                                    self.angleIndex = self.canMove(other)[0]
                                    self.rangeAttack(self.angles[self.angleIndex])
                            else:
                                self.move(False)
                        else:
                            if self.posX >= self.surface.rightBox[0] - self.characterX + self.speed:
                                self.move(False)
                            elif self.posX < self.surface.rightBox[0] - self.characterX + self.speed:
                                self.move(False)
                    else:
                        self.state = 0
                        self.move(False)
        '''if other.triedToAttack == False:
            if self.posX <= self.width/6:
                self.move(True)
            elif self.posX >= 5*self.width/6:
                self.move(False)'''
        '''if abs(self.posY-other.posY)<=self.height/40:
            if self.posX < other.posX:
                if abs(self.posX-other.posX) <= self.characterX:
                    if self.attackTime >= 20:
                        self.move(True)
                        self.state = 2
                        self.closeAttack()
                else:
                    if self.attackTime >= 20:
                        self.state = 1
                        self.rangeAttack()
            else:
                if abs(self.posX-other.posX) <= self.characterX:
                    if self.attackTime >= 20:
                        self.move(False)
                        self.state = 5
                        self.closeAttack()
                else:
                    if self.attackTime >= 20:
                        self.state = 4
                        self.rangeAttack()
        else:
            if self.posY > other.posY + self.height/40:
                if other.onTopPlatform:
                    if self.onLeftPlatform:
                        if self.posX >= self.surface.leftBox[0] + self.surface.leftBox[2] - self.speed:
                            if self.time % 12 == 0:
                                self.jump()
                                self.move(True)
                        else:
                            self.move(True)
                    elif self.onRightPlatform:
                        if self.posX <= self.surface.rightBox[0] - self.characterX + self.speed:
                            if self.time % 12 == 0:
                                self.jump()
                                self.move(False)
                        else:
                            self.move(False)
                        
                    elif self.onBottomPlatform:
                        if self.posX <= self.surface.leftBox[0] - self.characterX + self.speed:
                            self.move(True)
                        elif self.surface.leftBox[0]+self.surface.leftBox[2] - self.speed <= self.posX < self.width/2:
                            self.move(False)
                        elif self.width/2 <= self.posX <= self.surface.rightBox[0] - self.characterX + self.speed:
                            self.move(True)
                        elif self.posX >= self.surface.rightBox[0]+self.surface.rightBox[2] - self.speed:
                            self.move(False)

                        else:
                            if self.time % 12 == 0:
                                self.jump()

                elif other.onLeftPlatform or other.onRightPlatform:
                    if self.onBottomPlatform:
                        if self.posX <= self.surface.leftBox[0] - self.characterX + self.speed:
                            self.move(True)
                        elif self.surface.leftBox[0]+self.surface.leftBox[2] - self.speed <= self.posX < self.width/2:
                            self.move(False)
                        elif self.width/2 <= self.posX <= self.surface.rightBox[0] - self.characterX + self.speed:
                            self.move(True)
                        elif self.posX >= self.surface.rightBox[0]+self.surface.rightBox[2] - self.speed:
                            self.move(False)

                        else:
                            if self.time % 12 == 0:
                                self.jump()
                else:
                    return
                    


            elif self.posY <= other.posY - self.height/40:
                if other.onLeftPlatform:
                    if self.onTopPlatform:
                        if self.posX >= self.surface.topBox2[0] - self.characterX:
                            self.move(False)
                elif other.onRightPlatform:
                    if self.onTopPlatform:
                        if self.posX <= self.surface.topBox[0] + self.surface.topBox[2]:
                            self.move(True)
                elif other.onBottomPlatform:
                    if self.onLeftPlatform:
                        if self.posX <= self.surface.leftBox[0] + self.surface.leftBox[2]:
                            self.move(True)
                    elif self.onRightPlatform:
                        if self.posX >= self.surface.rightBox[0] - self.characterX:
                            self.move(False)
                    elif self.onTopPlatform:
                        if self.posX + self.characterX/2 <= self.width/2:
                            if self.posX >= self.surface.topBox[0] - self.characterX:
                                self.move(False)
                        else:
                            if self.posX <= self.surface.topBox[0] + self.surface.topBox[2]:
                                self.move(True)'''
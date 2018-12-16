import pygame
from Character import *
from Surface import *
import random
class Pikachu(Character):
    def __init__(self, screen):
        super().__init__(screen)
        #self.images = ["pikachurun.png", "pikachurange.png", "pikachuclose.png", "pikachurunleft.png", "pikachucloseleft.png", "pikachurangeleft.png"]
        #self.pikachuRunSheet = "pikachurunspritesheet.png"
        #self.loadedImages = []
        self.bulletImage = pygame.transform.scale(pygame.image.load("images/thunder.png"),(self.sphereRad,self.sphereRad))
        self.runImages = ["images/PR1.png", "images/PR2.png", "images/PR3.png", "images/PR4.png"]
        self.jumpImage = "images/pikachujump.png"
        self.punchImage = "images/pikachupunch.png"
        self.rangeImage = "images/pikachurange.png"
        self.loadedRunImages = []
        self.closeDamage = 28
        self.rangeDamage = 14
        self.closeDamageInit = self.closeDamage
        self.rangeDamageInit = self.rangeDamage
        self.speed = 5
        self.rangeReloadTime = 32
        self.closeReloadTime = 16
        self.weightConstant = 1.3
    def closeAttack(self):
        if self.isStunned == False:
            if self.state == 0 or self.state == 1 or self.state == 2:
                self.move(True)
                self.state = 2
            elif self.state == 3 or self.state == 4 or self.state == 5:
                self.move(False)
                self.state = 5
            self.attackTime = 0

    def makeMove(self,other):
        self.dodgeBullets(other)
        if abs(self.posX-other.posX) >= self.width/3 and self.onBottomPlatform and other.onBottomPlatform:
            if self.posX < other.posX:
                self.move(True)
            else:
                self.move(False)
                
        if abs(self.posY-other.posY)<=self.height/40:
            if self.posX < other.posX:
                if self.characterX/3 <= abs(self.posX-other.posX) <= self.characterX:
                    if self.attackTime >= self.closeReloadTime*self.aiDelay:
                        if other.triedToAttack == False:
                            self.move(True)
                        self.state = 0
                        #self.closeLoadTime = 0
                        #if self.closeLoadTime >= self.closeLoadLimit:
                        self.closeAttack()
                    if other.triedToAttack and int(other.closeLoadLimit/4) <= other.closeLoadTime < other.closeLoadLimit:
                        if self.posX >= self.surface.bottomBox[0]-self.characterX+self.speed:
                            self.move(False)
                        if other.closeLoadTime == other.closeLoadLimit:
                            self.state = 0

                elif abs(self.posX-other.posX) < self.characterX/3:
                    self.state = 0
                    self.closeAttack()
                    if other.triedToAttack and int(other.closeLoadLimit/4) <= other.closeLoadTime < other.closeLoadLimit:
                        if self.posX >= self.surface.bottomBox[0]-self.characterX+self.speed:
                            self.move(False)
                        if other.closeLoadTime == other.closeLoadLimit:
                            self.state = 0
                else:
                    if other.isStunned:
                        self.move(True)
                    elif self.attackTime >= self.rangeReloadTime*self.aiDelay:
                        self.state = 1
                        self.rangeAttack()
            else:
                if self.characterX/3 <= abs(self.posX-other.posX) <= self.characterX:
                    if self.attackTime >= self.closeReloadTime*self.aiDelay:
                        if other.triedToAttack == False:
                            self.move(False)
                        self.state = 3
                        #self.closeLoadTime = 0
                        #if self.closeLoadTime >= self.closeLoadLimit:
                        #self.closeAttack()
                        self.triedToAttack = True
                    if other.triedToAttack and int(other.closeLoadLimit*1/4) <= other.closeLoadTime < other.closeLoadLimit:
                        if self.posX <= self.surface.bottomBox[0] + self.surface.bottomBox[2]-self.speed:
                            self.move(True)
                        if other.closeLoadTime == other.closeLoadLimit:
                            self.state = 3
                elif abs(self.posX-other.posX) < self.characterX/3:
                    self.state = 3
                    self.triedToAttack = True
                    if other.triedToAttack and int(other.closeLoadLimit*1/4) <= other.closeLoadTime < other.closeLoadLimit:
                        if self.posX <= self.surface.bottomBox[0] + self.surface.bottomBox[2]-self.speed:
                            self.move(True)
                        if other.closeLoadTime == other.closeLoadLimit:
                            self.state = 3
                else:
                    if other.isStunned:
                        self.move(False)
                    elif self.attackTime >= self.rangeReloadTime*self.aiDelay:
                        self.state = 4
                        self.rangeAttack()
                            
                            
        else:
            if self.posY > other.posY + self.height/40:
                if other.onTopPlatform:
                    if self.onLeftPlatform:
                        if self.posX >= self.surface.leftBox[0] + self.surface.leftBox[2] - self.speed:
                            self.jump()
                            self.move(True)
                        else:
                            self.move(True)
                    elif self.onRightPlatform:
                        if self.posX <= self.surface.rightBox[0] - self.characterX + self.speed:
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
                            self.jump()
                    elif self.onSurface == False:
                        if self.airTime > self.jumpReloadTime:
                            if self.posX <= self.surface.rightBox[0] - self.characterX + self.speed and self.posY >= self.surface.topBox[1] + self.characterY:
                                self.jump()
                                self.move(False)
                            elif self.posX >= self.surface.leftBox[0] + self.surface.leftBox[2] - self.speed and self.posY >= self.surface.topBox[1] + self.characterY:
                                self.jump()
                                self.move(True)
                            else:
                                self.jump()

                elif other.onLeftPlatform or other.onRightPlatform:
                    if other.isStunned:
                        if other.onLeftPlatform:
                            if self.onBottomPlatform:
                                if self.posX <= self.surface.leftBox[0] - self.characterX + self.speed:
                                    self.move(True)
                                elif self.surface.leftBox[0]+self.surface.leftBox[2] - self.speed <= self.posX:
                                    self.move(False)
                                else:
                                    self.jump()
                        if other.onRightPlatform:
                            if self.onBottomPlatform:
                                if self.posX <= self.surface.rightBox[0] - self.characterX + self.speed:
                                    self.move(True)
                                elif self.surface.rightBox[0]+self.surface.rightBox[2] - self.speed <= self.posX:
                                    self.move(False)
                                else:
                                    self.jump()
                        elif self.onSurface == False:
                            if self.airTime > self.jumpReloadTime:
                                self.jump()
                    else:
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
                                self.jump()
                        elif self.onSurface == False:
                            if self.airTime > self.jumpReloadTime:
                                self.jump()
                else:
                    return
                    


            elif self.posY <= other.posY - self.height/40:
                if other.onLeftPlatform:
                    if self.onTopPlatform:
                        if self.posX >= self.surface.topBox[0] - self.characterX:
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
                                self.move(True)
        '''if self.posX <= self.width/6:
            self.move(True)
        elif self.posX >= 5*self.width/6:
            self.move(False)'''
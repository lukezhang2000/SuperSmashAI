import pygame
from Character import *
from Surface import *
class Lucario(Character):
    def __init__(self, screen):
        super().__init__(screen)
        #self.images = ["lucarioblock.png","lucariorange.png","lucariopunch.png","lucarioblockleft.png","lucariorangeleft.png","lucariopunchleft.png"]
        #self.loadedImages = []
        #self.blockHitBox = [self.posX, self.posY, self.posX + self.characterX, self.posY + self.characterY]
        self.bulletImage = pygame.transform.scale(pygame.image.load("images/aurasphere.png"),(self.sphereRad,self.sphereRad))
        self.runImages = ["images/LR1.png", "images/LR2.png"]
        self.jumpImage = "images/lucariojump.png"
        self.punchImage = "images/lucariopunch.png"
        self.rangeImage = "images/lrange2.png"
        self.standImage = "images/lucariostand.png"
        self.loadedRunImages = []
        self.closeDamage = 34
        self.rangeDamage = 34
        self.closeDamageInit = self.closeDamage
        self.rangeDamageInit = self.rangeDamage
        self.speed = 3
        self.weightConstant = 1
    
            
            
    '''def defineHitboxes(self):
        if self.state == 0:
            self.hitBox = pygame.Rect(self.posX + 3,self.posY + 5,27,38)
            self.hitBox2 = pygame.Rect(self.posX + 3,self.posY + 5,27,38)
        if self.state == 1:
            self.hitBox = pygame.Rect(self.posX + 3,self.posY + 5,27,38)
            self.hitBox2 = pygame.Rect(self.posX+30,self.posY + 15,5,5)
        if self.state == 2:
            self.hitBox = pygame.Rect(self.posX + 3,self.posY + 5,27,38)
            self.hitBox2 = pygame.Rect(self.posX+30,self.posY + 15,5,5)
        if self.state == 3:
            self.hitBox = pygame.Rect(self.posX + 10,self.posY + 7,27,38)
            self.hitBox2 = pygame.Rect(self.posX + 3,self.posY + 5,27,38)
        if self.state == 4:
            self.hitBox = pygame.Rect(self.posX + 3,self.posY + 5,27,38)
            self.hitBox2 = pygame.Rect(self.posX-2,self.posY+15,5,5)
        if self.state == 5:
            self.hitBox = pygame.Rect(self.posX + 3,self.posY + 5,27,38)
            self.hitBox2 = pygame.Rect(self.posX-2,self.posY+15,5,5)'''
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
                         #   self.closeAttack()
                         
                        self.triedToAttack = True
                    if other.triedToAttack and int(other.closeLoadLimit/4) <= other.closeLoadTime < other.closeLoadLimit:
                        if self.posX >= self.surface.bottomBox[0]+self.characterX+self.speed:
                            self.move(False)
                        if other.closeLoadTime == other.closeLoadLimit:
                            self.state = 0

                elif abs(self.posX-other.posX) < self.characterX/3:
                    self.state = 0
                    self.triedToAttack = True
                    if other.triedToAttack and int(other.closeLoadLimit/4) <= other.closeLoadTime < other.closeLoadLimit:
                        if self.posX >= self.surface.bottomBox[0]+self.characterX+self.speed:
                            self.move(False)
                        if other.closeLoadTime == other.closeLoadLimit:
                            self.state = 0
                else:
                    if self.attackTime >= self.rangeReloadTime*self.aiDelay:
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
                    if self.attackTime >= 20:
                        self.state = 4
                        self.rangeAttack()
        else:
            if self.posY > other.posY + self.height/40:
                if other.onTopPlatform:
                    if self.onLeftPlatform:
                        if self.posX >= self.surface.leftBox[0] + self.surface.leftBox[2] - self.speed:
                            self.jump()
                            self.move(True)
                            print("jump : other Top self Left")
                        else:
                            self.move(True)
                    elif self.onRightPlatform:
                        if self.posX <= self.surface.rightBox[0] - self.characterX + self.speed:
                            self.jump()
                            self.move(False)
                            print("jump : other Top self Right")
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
                            print("jump: other Top self Bottom")
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
                            print("jump: other L/R self Bottom")
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
                                
        '''if other.triedToAttack == False:
            if self.posX <= self.width/6:
                self.move(True)
            elif self.posX >= 5*self.width/6:
                self.move(False)'''
        
   #def ai(self, player, opponent):
        
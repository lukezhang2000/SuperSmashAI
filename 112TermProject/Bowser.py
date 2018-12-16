import pygame
from Character import *
from Surface import *
class Bowser(Character):
    def __init__(self, screen):
        super().__init__(screen)
        #self.images = ["bowserrun.png","bowserrange.png","bowserpunch.png","bowserrunleft.png","bowserrangeleft.png","bowserpunchleft.png"]
        #self.loadedImages = []
        self.bulletImage = pygame.transform.scale(pygame.image.load("images/firebreath.png"),(self.sphereRad,self.sphereRad))
        self.runImages = ["images/BR1.png", "images/BR2.png", "images/BR3.png", "images/BR4.png", "images/BR5.png", "images/BR6.png"]
        self.jumpImage = "images/bowserjump.png"
        self.punchImage = "images/bowserpunch.png"
        self.rangeImage = "images/bowserrange.png"
        self.loadedRunImages = []
        self.closeDamage = 53
        self.rangeDamage = 20
        self.closeDamageInit = self.closeDamage
        self.rangeDamageInit = self.rangeDamage
        self.speed = 2
        self.closeReloadTime = 12
        self.rangeReloadTime = 32
        self.weightConstant = .6

    def draw(self):
        '''if self.state != 0 and self.state != 3 and self.state != 6 and self.state != 7:
            for image in self.images:
                self.loadedImages.append(pygame.transform.scale(pygame.image.load(image),(self.characterX,self.characterY)))
            image = self.loadedImages[self.state]'''
        #self.screen.blit(pygame.transform.scale(pygame.image.load(self.runImages[0]),(self.characterX,self.characterY)), (2*self.posX, self.posY))
        
        if self.state == 3:
            if self.isJumping:
                image = pygame.transform.scale(pygame.image.load(self.jumpImage),(self.characterX,self.characterY))
            else:
                for image in self.runImages:
                    self.loadedRunImages.append(pygame.transform.scale(pygame.image.load(image),(self.characterX,self.characterY)))
                image = self.loadedRunImages[self.runSpriteIndex%len(self.loadedRunImages)]
        if self.state == 4:
            image = image = pygame.transform.scale(pygame.image.load(self.rangeImage),(self.characterX,self.characterY))
        if self.state == 5:
            image = pygame.transform.scale(pygame.image.load(self.punchImage),(self.characterX,self.characterY))
        if self.state == 0:
            if self.isJumping:
                image = pygame.transform.flip(pygame.transform.scale(pygame.image.load(self.jumpImage),(self.characterX,self.characterY)), True, False)
            else:
                for image in self.runImages:
                    self.loadedRunImages.append(pygame.transform.scale(pygame.image.load(image),(self.characterX,self.characterY)))
                image = pygame.transform.flip(self.loadedRunImages[self.runSpriteIndex%len(self.loadedRunImages)], True, False)
        if self.state == 1:
            image = pygame.transform.flip(pygame.transform.scale(pygame.image.load(self.rangeImage),(self.characterX,self.characterY)), True, False)     
        if self.state == 2:
            image = pygame.transform.flip(pygame.transform.scale(pygame.image.load(self.punchImage),(self.characterX,self.characterY)), True, False)
        self.screen.blit(image, (self.posX, self.posY))
        for bullet in self.bullets:
            self.screen.blit(self.bulletImage,(bullet[0],bullet[1]))
    def makeMove(self,other):
        self.dodgeBullets(other)
        if abs(self.posX-other.posX) >= self.width/3 and self.onBottomPlatform and other.onBottomPlatform:
            if self.posX < other.posX:
                self.move(True)
            else:
                self.move(False)
        if abs(self.posY-other.posY)<=self.height/40:
            if self.posX < other.posX:
                if abs(self.posX-other.posX) <= self.characterX:
                    if self.attackTime >= self.closeReloadTime*self.aiDelay:
                        self.move(True)
                        self.state = 2
                        self.closeAttack()
                else:
                    if self.attackTime >= self.rangeReloadTime*self.aiDelay:
                        self.state = 1
                        if self.onBottomPlatform:
                            self.move(True)
                        self.rangeAttack()
            else:
                if abs(self.posX-other.posX) <= self.characterX:
                    if self.attackTime >= self.closeReloadTime*self.aiDelay:
                        self.move(False)
                        self.state = 5
                        self.closeAttack()
                else:
                    if self.attackTime >= self.rangeReloadTime*self.aiDelay:
                        self.state = 4
                        if self.onBottomPlatform:
                            self.move(False)
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
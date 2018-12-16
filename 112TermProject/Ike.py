import pygame
from Character import *
from Surface import *
class Ike(Character):
    def __init__(self, screen):
        super().__init__(screen)
        self.ikerange = pygame.image.load("ikesword.png")
        self.ikerange = pygame.transform.scale(self.ikerange,(3*self.characterX,self.characterY))
        self.ikepunch = pygame.image.load("ikepunch.png")
        self.ikepunch = pygame.transform.scale(self.ikepunch,(self.characterX,self.characterY))
        self.ikeblock = pygame.image.load("ike.png")
        self.ikeblock = pygame.transform.scale(self.ikeblock,(self.characterX,self.characterY))
        self.ikepunchleft = pygame.image.load("ikepunchleft.png")
        self.ikepunchleft = pygame.transform.scale(self.ikepunchleft,(self.characterX,self.characterY))
        self.ikerangeleft = pygame.image.load("ikeswordleft.png")
        self.ikerangeleft = pygame.transform.scale(self.ikerange,(int(self.characterX *2),self.characterY))
        self.ikeblockleft = pygame.image.load("ikeleft.png")
        self.ikeblockleft = pygame.transform.scale(self.ikeblockleft,(self.characterX,self.characterY))
        self.sword = pygame.image.load("sword.png")
        self.sword = pygame.transform.scale(self.sword,(self.sphereRad,self.sphereRad))
        self.bullets = []
        self.closeDamage = 48
        self.rangeDamage = 32
        self.speed = 8
    def rangeAttack(self):
        '''try:
            if self.bullets[0][0] != 0:
                self.bullets[0] = [self.posX, self.posY, True]
        except:
            return'''
        if self.state == 0 or self.state == 1 or self.state == 2:
            self.state = 1
        elif self.state == 3 or self.state == 4 or self.state == 5:
            self.state = 4
    def draw(self):
        if self.state == 0:
            image = self.ikeblock
        elif self.state == 1:
            image = self.ikerange
        elif self.state == 2:
            image = self.ikepunch
        elif self.state == 3:
            image = self.ikeblockleft
        elif self.state == 4:
            image = self.ikerangeleft
        elif self.state == 5:
            image = self.ikepunchleft
        image = pygame.transform.scale(image, (self.characterX, self.characterY))
        self.screen.blit(image, (self.posX, self.posY))
        for bullet in self.bullets:
            self.screen.blit(self.sword,(bullet[0],bullet[1]))
        
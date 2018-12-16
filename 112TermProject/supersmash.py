
###Used pygamegame template by Lukas Peraza
import pygame
import random
import math

import pygame as pg
import sys
from pygame.locals import *
from Character import *
from Surface import *
from Ike import *
from lucario import *
from Bowser import *
from Pikachu import *
from Pit import *



class PygameGame(object):

    def init(self):
        self.state = 0
        self.auraSpheres = pygame.sprite.Group()
        self.width = 600
        self.height = 400
        self.homeScreen=pygame.transform.scale(pygame.image.load("images/homescreen.png"),(self.width,self.height))
        self.charScreen=pygame.transform.scale(pygame.image.load("images/charScreen.png"),(self.width,self.height))
        self.images = ["images/lucario.png", "images/bowser.png" , "images/pikachu.png", "images/pit.png"]
        #self.images = ["p1lucario.png", "p1bowser.png", "p1pikachu.png", "p1pit.png", "lucariolucario.png", "lucariobowser.png", "lucariopikachu.png", "lucariopit.png", "bowserlucario.png", "bowserbowser.png", "bowserpikachu.png", "bowserpit.png", "pikachulucario.png", "pikachubowser.png", "pikachupikachu.png", "pikachupit.png", "pitlucario.png", "pitbowser.png", "pitpikachu.png", "pitpit.png"]
        self.time = 0
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.singlePlayerBox = (228 * self.width/600, 265 * self.height/400, 373 * self.width/600, 297 * self.height/400)
        self.multiPlayerBox = (228 * self.width/600, 297 * self.height/400, 373 * self.width/600, 331 * self.height/400)
        self.field1 = pygame.image.load("images/field1.jpg")
        self.field1=pygame.transform.scale(self.field1,(self.width,self.height))
        self.player = None
        self.opponent = None
        self.surface = Surface(self.screen)
        self.white = (255,255,255)
        self.black = (0,0,0)
        self.lucarioBox = [26 * self.width/600,61 * self.height/400,150 * self.width/600,230 * self.height/400]
        self.bowserBox = [158 * self.width/600,61 * self.height/400,289 * self.width/600,230 * self.height/400]
        self.pikachuBox = [297 * self.width/600,61 * self.height/400,434 * self.width/600,230 * self.height/400]
        self.pitBox = [440 * self.width/600,61 * self.height/400,576 * self.width/600,230 * self.height/400]
        self.pressedKeys = {"left": False, "right": False}
        self.gameOver = False
        self.mode = None
        self.items = ["apple", "ice", "heart"]
        self.droppedItems = []
        self.itemRadius = 20
        self.choices = [True, False]
        self.apple=pygame.transform.scale(pygame.image.load("images/apple.png"),(self.itemRadius,self.itemRadius))
        self.ice=pygame.transform.scale(pygame.image.load("images/ice.png"),(self.itemRadius,self.itemRadius))
        self.heart=pygame.transform.scale(pygame.image.load("images/heart.png"),(self.itemRadius,self.itemRadius))
        self.itemsUsed = False

    def mousePressed(self, x, y):
        X, Y = pygame.mouse.get_pos()
        print(X,Y)
        if self.state == 0:
            if (self.singlePlayerBox[0] < X < self.singlePlayerBox[2]) and (self.singlePlayerBox[1] < Y <self.singlePlayerBox[3]):
                self.mode="single"
                self.state = 1
            if (self.multiPlayerBox[0] < X < self.multiPlayerBox[2]) and (self.multiPlayerBox[1] < Y <self.multiPlayerBox[3]):
                self.mode="multi"
                self.state = 23
        elif self.state == 1:
            if (self.lucarioBox[0] < X < self.lucarioBox[2]) and (self.lucarioBox[1] < Y <self.lucarioBox[3]):
                self.state = 2
                self.player = Lucario(self.screen)
                self.player.isLucario = True
            elif (self.bowserBox[0] < X < self.bowserBox[2]) and (self.bowserBox[1] < Y <self.bowserBox[3]):
                self.state = 3
                self.player = Bowser(self.screen)
                self.player.isBowser = True
            elif (self.pikachuBox[0] < X < self.pikachuBox[2]) and (self.pikachuBox[1] < Y <self.pikachuBox[3]):
                self.state = 4
                self.player = Pikachu(self.screen)
                self.player.isPikachu = True
            elif (self.pitBox[0] < X < self.pitBox[2]) and (self.pitBox[1] < Y <self.pitBox[3]):
                self.state = 5
                self.player = Pit(self.screen)
                self.player.isPit = True
                    
        elif self.state == 2:
            if (self.lucarioBox[0] < X < self.lucarioBox[2]) and (self.lucarioBox[1] < Y <self.lucarioBox[3]):
                self.state = 6
                self.opponent = Lucario(self.screen)
                self.opponent.isLucario = True
            elif (self.bowserBox[0] < X < self.bowserBox[2]) and (self.bowserBox[1] < Y <self.bowserBox[3]):
                self.state = 7
                self.opponent = Bowser(self.screen)
                self.opponent.isBowser = True
            elif (self.pikachuBox[0] < X < self.pikachuBox[2]) and (self.pikachuBox[1] < Y <self.pikachuBox[3]):
                self.state = 8
                self.opponent =  Pikachu(self.screen)
                self.opponent.isPikachu = True
            elif (self.pitBox[0] < X < self.pitBox[2]) and (self.pitBox[1] < Y <self.pitBox[3]):
                self.state = 9
                self.opponent = Pit(self.screen)
                self.opponent.isPit = True
            if self.opponent != None:
                self.opponent.state = 3
                self.opponent.posX = 450 * self.width/600
                self.opponent.closeLoadTime = self.opponent.aiDelay * self.opponent.closeLoadTime
        elif self.state == 3:
            if (self.lucarioBox[0] < X < self.lucarioBox[2]) and (self.lucarioBox[1] < Y <self.lucarioBox[3]):
                self.state = 10
                self.opponent = Lucario(self.screen)
                self.opponent.isLucario = True
            elif (self.bowserBox[0] < X < self.bowserBox[2]) and (self.bowserBox[1] < Y <self.bowserBox[3]):
                self.state = 11
                self.opponent = Bowser(self.screen)
                self.opponent.isBowser = True
            elif (self.pikachuBox[0] < X < self.pikachuBox[2]) and (self.pikachuBox[1] < Y <self.pikachuBox[3]):
                self.state = 12
                self.opponent = Pikachu(self.screen)
                self.opponent.isPikachu = True
            elif (self.pitBox[0] < X < self.pitBox[2]) and (self.pitBox[1] < Y <self.pitBox[3]):
                self.state = 13
                self.opponent = Pit(self.screen)
                self.opponent.isPit = True
            if self.opponent != None:
                self.opponent.state = 3
                self.opponent.posX = 450 * self.width/600
                self.opponent.closeLoadTime = self.opponent.aiDelay * self.opponent.closeLoadTime
        elif self.state == 4:
            if (self.lucarioBox[0] < X < self.lucarioBox[2]) and (self.lucarioBox[1] < Y <self.lucarioBox[3]):
                self.state = 14
                self.opponent = Lucario(self.screen)
                self.opponent.isLucario = True
            elif (self.bowserBox[0] < X < self.bowserBox[2]) and (self.bowserBox[1] < Y <self.bowserBox[3]):
                self.state = 15
                self.opponent =  Bowser(self.screen)
                self.opponent.isBowser = True
            elif (self.pikachuBox[0] < X < self.pikachuBox[2]) and (self.pikachuBox[1] < Y <self.pikachuBox[3]):
                self.state = 16
                self.opponent = Pikachu(self.screen)
                self.opponent.isPikachu = True
            elif (self.pitBox[0] < X < self.pitBox[2]) and (self.pitBox[1] < Y <self.pitBox[3]):
                self.state = 17
                self.opponent = Pit(self.screen)
                self.opponent.isPit = True
            if self.opponent != None:
                self.opponent.state = 3
                self.opponent.posX = 450 * self.width/600
                self.opponent.closeLoadTime = self.opponent.aiDelay * self.opponent.closeLoadTime
        elif self.state == 5:
            if (self.lucarioBox[0] < X < self.lucarioBox[2]) and (self.lucarioBox[1] < Y <self.lucarioBox[3]):
                self.state = 18
                self.opponent = Lucario(self.screen)
                self.opponent.isLucario = True
            elif (self.bowserBox[0] < X < self.bowserBox[2]) and (self.bowserBox[1] < Y <self.bowserBox[3]):
                self.state = 19
                self.opponent = Bowser(self.screen)
                self.opponent.isBowser = True
            elif (self.pikachuBox[0] < X < self.pikachuBox[2]) and (self.pikachuBox[1] < Y <self.pikachuBox[3]):
                self.state = 20
                self.opponent =  Pikachu(self.screen)
                self.opponent.isPikachu = True
            elif (self.pitBox[0] < X < self.pitBox[2]) and (self.pitBox[1] < Y <self.pitBox[3]):
                self.state = 21
                self.opponent = Pit(self.screen)
                self.opponent.isPit = True
            if self.opponent != None:
                self.opponent.state = 3
                self.opponent.posX = 450 * self.width/600
                #self.opponent.posY = 205 * self.width/600
                self.opponent.closeLoadTime = self.opponent.aiDelay * self.opponent.closeLoadTime
        elif self.state == 22:
            if self.gameOver == False:
                X, Y = pygame.mouse.get_pos()
                print(X,Y)
               
    def mouseReleased(self, x, y):
        pass

    def mouseMotion(self, x, y):
        pass

    def mouseDrag(self, x, y):
        pass

    def keyPressed(self, keyCode, modifier):
        if 6 <= self.state <= 21:
            if keyCode == pygame.K_RETURN:
                self.state = 22
        if self.state == 22:
            if keyCode == pygame.K_SPACE:
                if self.player.isStunned == False:
                    #if self.player.jumpCount < self.player.jumpLimit:
                    self.player.jump()
                    #self.player.jumpCount += 1
            if keyCode == pygame.K_a:
                if self.player.isStunned == False:
                    if self.player.attackTime > self.player.rangeReloadTime:
                        self.player.rangeAttack()
                        self.player.attackTime = 0

            if keyCode == pygame.K_s:
                if self.player.isStunned == False:
                    if self.player.attackTime > self.player.rangeReloadTime:
                        self.player.closeLoadTime = 0
                        self.player.triedToAttack = True
                        #self.player.closeAttack()
                        self.player.attackTime = 0
            if keyCode == pygame.K_DOWN:
                if self.player.isStunned == False:
                    if self.player.isPit:
                        if self.player.angleIndex >= 1:
                            self.player.angleIndex -= 1
            if keyCode == pygame.K_UP:
                if self.player.isStunned == False:
                    if self.player.isPit:
                        if self.player.angleIndex <= len(self.player.angles) - 2:
                            self.player.angleIndex += 1
                            
            if self.mode == "multi":
                if keyCode == pygame.K_RETURN:
                    if self.opponent.isStunned == False:
                        self.opponent.jump()
                if keyCode == pygame.K_n:
                    if self.opponent.isStunned == False:
                        if self.opponent.attackTime > self.opponent.rangeReloadTime:
                            self.opponent.rangeAttack()
                            self.opponent.attackTime = 0
    
                if keyCode == pygame.K_m:
                    if self.opponent.isStunned == False:
                        if self.opponent.attackTime > self.opponent.rangeReloadTime:
                            self.opponent.closeLoadTime = 0
                            self.opponent.triedToAttack = True
                            self.opponent.attackTime = 0
                if keyCode == pygame.K_k:
                    if self.opponent.isStunned == False:
                        if self.opponent.isPit:
                            if self.opponent.angleIndex >= 1:
                                self.opponent.angleIndex -= 1
                if keyCode == pygame.K_i:
                    if self.opponent.isStunned == False:
                        if self.opponent.isPit:
                            if self.opponent.angleIndex <= len(self.opponent.angles) - 2:
                                self.opponent.angleIndex += 1
        if self.state == 23:
            if keyCode == pygame.K_y:
                self.itemsUsed = True
                self.state = 1
            if keyCode == pygame.K_n:
                self.itemsUsed = False
                self.state = 1

    def keyReleased(self, keyCode, modifier):
        pass
        
    def dropItem(self):
        if random.choice(self.choices) == True:
            self.droppedItems.append([random.choice(self.items), random.randrange(self.surface.bottomBox2[0],            self.surface.bottomBox2[0]+self.surface.bottomBox2[2]), random.randrange(self.surface.leftBox2[1] + self.surface.leftBox2[3], self.surface.bottomBox2[1]- self.itemRadius),0, False])
        else:
            self.droppedItems.append([random.choice(self.items), random.randrange(self.surface.bottomBox2[0], self.surface.bottomBox2[0]+self.surface.bottomBox2[2]), random.randrange(0, self.surface.leftBox[1]-self.itemRadius), 0, False])


    def timerFired(self):
        if self.gameOver == False and self.player != None and self.opponent != None and self.state == 22:
            #print(self.player.closeLoadTime)
            #print(self.opponent.posY)
            self.player.time += 1
            self.opponent.time += 1
            self.player.attackTime += 1
            self.opponent.attackTime += 1
            self.opponent.airTime += 1
            self.player.airTime += 1
            self.player.closeLoadTime += 1
            self.opponent.closeLoadTime += 1
            self.opponent.coolDownTime += 1
            self.player.closeAttackDelay()
            self.opponent.closeAttackDelay()

            if self.isKeyPressed(pygame.K_RIGHT):
                self.player.move(True)
            if self.isKeyPressed(pygame.K_LEFT):
                self.player.move(False)
            if self.mode == "multi":
                if self.isKeyPressed(pygame.K_l):
                    self.opponent.move(True)
                if self.isKeyPressed(pygame.K_j):
                    self.opponent.move(False)
                if self.itemsUsed == True:
                    if self.opponent.time % 500 == 0 and self.opponent.time != 0:
                        self.dropItem()
            if self.opponent.time % 3 == 0:
                opponentRect = pygame.Rect(self.opponent.posX,self.opponent.posY,self.opponent.characterX,self.opponent.characterY)
                playerRect = pygame.Rect(self.player.posX,self.player.posY,self.player.characterX,self.player.characterY)
                self.player.checkStun()
                self.opponent.checkStun()
                self.opponent.checkSurface()
                self.player.checkSurface()
                self.opponent.ifOnSurface()
                self.player.ifOnSurface()
                self.player.checkBoost()
                self.opponent.checkBoost()
                #print(self.player.onSurface)
                self.player.posY -= self.player.yVelocity
                self.opponent.posY -= self.opponent.yVelocity
                self.player.posX += self.player.xVelocity
                self.opponent.posX += self.opponent.xVelocity
                for i in range(len(self.surface.surfaces)):
                    surfaceRect = pygame.Rect(self.surface.surfaces[i][0],self.surface.surfaces[i][1],self.surface.surfaces[i][2],self.surface.surfaces[i][3])
                    if playerRect.colliderect(surfaceRect) and self.player.posY > self.surface.surfaces[i][1]:
                        self.player.posY = self.surface.surfaces[i][1]
                        self.player.jumpCount = 0
                        self.player.airTime = 0
                        self.player.isJumping = False
                        self.player.yVelocity = 0
                        self.player.xVelocity = 0
                    if (opponentRect.colliderect(surfaceRect) and self.opponent.posY > self.surface.surfaces[i][1]):
                        self.opponent.posY = self.surface.surfaces[i][1]
                        self.opponent.jumpCount = 0
                        self.opponent.airTime = 0
                        self.opponent.isJumping = False
                        self.opponent.yVelocity = 0
                        self.opponent.xVelocity = 0
                if self.mode == "multi" and self.itemsUsed == True:
                    for item in self.droppedItems:
                        if item[4] == False:
                            item[2] += self.player.gravity * item[3]
                            item[3] += 1
                    for i in range(len(self.surface.surfaces2)):
                        surfaceRect = pygame.Rect(self.surface.surfaces[i][0],self.surface.surfaces[i][1],self.surface.surfaces[i][2],self.surface.surfaces[i][3])
                        for item in self.droppedItems:
                            itemRect = pygame.Rect(item[1],item[2],self.itemRadius, self.itemRadius)
                            if (itemRect.colliderect(surfaceRect) and item[2] >= self.surface.surfaces[i][1]-self.itemRadius/2):
                                item[2] = self.surface.surfaces[i][1] + self.itemRadius
                                item[3] = 0
                                item[4] = True
                            if (itemRect.colliderect(playerRect)):
                                if item[0] == "heart":
                                    self.player.lives += 1
                                if item[0] == "ice":
                                    self.opponent.isStunned = True
                                if item[0] == "apple":
                                    self.player.isBoosted = True
                                try:
                                    self.droppedItems.remove(item)
                                except:
                                    return
                            if (itemRect.colliderect(opponentRect)):
                                if item[0] == "heart":
                                    self.opponent.lives += 1
                                if item[0] == "ice":
                                    self.player.isStunned = True
                                if item[0] == "apple":
                                    self.opponent.isBoosted = True
                                try:
                                    self.droppedItems.remove(item)
                                except:
                                    return
                self.player.fallGravity()
                self.opponent.fallGravity()
                #self.player.checkValidFall()
                #self.player.posY -= self.player.yVelocity
                #self.opponent.posY -= self.opponent.yVelocity
                
                #AI Opponent Below
                #if self.mode == "multi":
                #    self.opponent.dodgeBullets(self.player)
                if self.mode == "single":
                    self.opponent.makeMove(self.player)
                
                
                #self.player.makeMove(self.opponent)
                #AI Above
                
                self.player.switchBack()
                self.opponent.switchBack()
                
                self.player.checkMelee(self.opponent)
                self.opponent.checkMelee(self.player)
                
                '''if opponentRect.colliderect(playerRect) == True:
                    if self.player.state == 2 and self.opponent.posX - self.opponent.character<=self.player.posX <= self.opponent.posX + self.opponent.characterX:
                        self.opponent.health += self.player.closeDamage
                        self.opponent.posX+=self.opponent.health * self.player.closeKnockbackConstant * self.opponent.weightConstant
                    if self.player.state == 5 and self.opponent.posX - self.opponent.characterX <= self.player.posX <= self.opponent.posX + self.opponent.characterX:
                        self.opponent.health += self.player.closeDamage
                        self.opponent.posX-=self.opponent.health * self.player.closeKnockbackConstant * self.opponent.weightConstant
                    if self.opponent.state == 2 and self.player.posX - self.player.characterX<=self.opponent.posX <= self.player.posX + self.player.characterX:
                        self.player.health += self.opponent.closeDamage
                        self.player.posX += self.player.health * self.opponent.closeKnockbackConstant * self.player.weightConstant
                    if self.opponent.state == 5 and self.player.posX - self.player.characterX <= self.opponent.posX <= self.player.posX + self.player.characterX:
                        self.player.health += self.opponent.closeDamage
                        self.player.posX-=self.player.health * self.opponent.closeKnockbackConstant * self.player.weightConstant'''
                        
                self.player.checkBounds()
                self.opponent.checkBounds()
                #game is over when one sprite's lives is 0
                if self.player.lives == 0 or self.opponent.lives == 0:
                    self.gameOver = True
                #checks for collisions of bullets between sprites
                for playerBullet in self.player.bullets:
                    playerBulletRect = pygame.Rect(playerBullet[0]-self.player.sphereRad/2,playerBullet[1]-self.player.sphereRad/2,self.player.sphereRad,self.player.sphereRad)
                    for oppBullet in self.opponent.bullets:
                        oppBulletRect = pygame.Rect(oppBullet[0] - self.opponent.sphereRad/2,oppBullet[1]-self.opponent.sphereRad/2,self.player.sphereRad,self.player.sphereRad)
                        if playerBulletRect.colliderect(oppBulletRect):
                            self.player.bullets.remove(playerBullet)
                            self.opponent.bullets.remove(oppBullet)
                #angleOpponent = self.opponent.angles[self.opponent.angleIndex]*math.pi/180     
                self.player.checkBullets(self.opponent)
                self.opponent.checkBullets(self.player)
                    
            
    def redrawAll(self, screen):
        if self.state == 0:
            screen.blit(self.homeScreen,(0,0))
            #self.startBox = (300 * self.width/600, 265 * self.height/400, 350 * self.width/600, 282 * self.height/400)
            #pygame.draw.rect(screen, self.white, [self.startBox[0], self.startBox[1],self.startBox[2]-self.startBox[0], self.startBox[3]-self.startBox[1]], 3)
        elif self.state == 1:
            screen.blit(self.charScreen,(0,0))
        elif 2 <= self.state <= 5:
            screen.blit(self.charScreen,(0,0))
            image = pygame.transform.scale(pygame.image.load(self.images[self.state-2]),(100,130))
            screen.blit(image,(23, 264))
            #image = pygame.transform.scale(pygame.image.load(self.images[self.state-2]),(self.width,self.height))
            #screen.blit(image,(0,0))
        if  22>self.state >= 6:
            screen.blit(self.charScreen,(0,0))
            image1 = pygame.transform.scale(pygame.image.load(self.images[self.state%4-2]),(100,130))
            image2 = pygame.transform.scale(pygame.image.load(self.images[(self.state+2)//4-2]),(100,130))
            screen.blit(image2,(23,264))
            screen.blit(image1,(310,264))
            pygame.init()
            basicfont = pygame.font.SysFont(None, 30)
            text = basicfont.render("Press ENTER to begin!", True, self.white)
            textrect = text.get_rect()
            textrect.center = ((self.width/2,self.height*3/5))
            screen.blit(text, textrect)
            
            '''if self.mode == "multi":
                pygame.init()
                basicfont = pygame.font.SysFont(None, 30)
                text = basicfont.render("Click Y for items to drop and N otherwise", True, self.white)
                textrect = text.get_rect()
                textrect.center = ((self.width/2,self.height*3/5 + 10))
                screen.blit(text, textrect)'''
        
        elif self.state == 22:
            screen.blit(self.field1,(0,0))
            pygame.init()
            basicfont = pygame.font.SysFont(None, 30)
            text = basicfont.render('Player Lives:' + str(self.player.lives) + " " + str(self.player.health) + "%", True, self.white)
            textrect = text.get_rect()
            textrect.center = ((self.width/4,self.height*4/5))
            screen.blit(text, textrect)
            pygame.init()
            basicfont = pygame.font.SysFont(None, 30)
            text = basicfont.render('Opponent Lives:' + str(self.opponent.lives) + " " + str(self.opponent.health) + "%", True, self.white)
            textrect = text.get_rect()
            textrect.center = ((self.width*3/4,self.height*4/5))
            screen.blit(text, textrect)
            if self.gameOver == True:
                pygame.init()
                basicfont = pygame.font.SysFont(None, 30)
                if self.opponent.lives == 0:
                    text = basicfont.render("Game Over! The player wins!", True, self.white)
                elif self.player.lives == 0:
                    text = basicfont.render("Game Over! The opponent wins!", True, self.white)
                textrect = text.get_rect()
                textrect.center = ((self.width/2,self.height/2))
                screen.blit(text, textrect)
            for item in self.droppedItems:
                if item[0] == "apple":
                    screen.blit(self.apple, (item[1], item[2]))
                elif item[0] == "ice":
                    screen.blit(self.ice, (item[1], item[2]))
                elif item[0] == "heart":
                    screen.blit(self.heart, (item[1], item[2]))
            #pygame.draw.rect(screen, self.white, [self.player.posX, self.player.posY,self.player.characterX, self.player.characterY], 3)
            if self.player.lives != 0:
                self.player.draw()
            if self.opponent.lives != 0:
                self.opponent.draw() 
            pygame.display.update()
        elif self.state == 23:
            screen.blit(self.homeScreen,(0,0))
            if self.mode == "multi":
                pygame.init()
                basicfont = pygame.font.SysFont(None, 30)
                text = basicfont.render("Click Y for items to drop and N otherwise", True, self.white)
                textrect = text.get_rect()
                textrect.center = ((self.width/2,self.height*3/5))
                screen.blit(text, textrect)
    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)

    def __init__(self, width=600, height=400, fps=50, title="112 Pygame Game"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.bgColor = (255, 255, 255)
        pygame.init()

    def run(self):

        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)

        # stores all the keys currently being held down
        self._keys = dict()

        # call game-specific initialization
        self.init()
        playing = True
        while playing:
            #time = clock.tick(self.fps)
            self.timerFired()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons == (0, 0, 0)):
                    self.mouseMotion(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons[0] == 1):
                    self.mouseDrag(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                elif event.type == pygame.QUIT:
                    playing = False
            screen.fill(self.bgColor)
            self.redrawAll(screen)
            pygame.display.flip()

        pygame.quit()


def main():
    game = PygameGame()
    game.run()

if __name__ == '__main__':
    main()


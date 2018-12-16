import pygame
class Surface(pygame.sprite.Sprite):
    def __init__(self, screen):
        self.width = 600
        self.height = 400
        self.leftBox = [105 * self.width/600,115 * self.height/400,118 * self.width/600,15 * self.height/400]
        self.rightBox = [375 * self.width/600,115 * self.height/400,118 * self.width/600,15 * self.height/400]
        self.topBox = [245 * self.width/600,25 * self.height/400,115 * self.width/600,10 * self.height/400]
        self.bottomBox = [43 * self.width/600,205 * self.height/400,509 * self.width/600,70 * self.height/400]
        self.surfaces = [self.leftBox, self.rightBox, self.topBox, self.bottomBox]
        self.leftBox2 = [110 * self.width/600,165 * self.height/400,110 * self.width/600,10 * self.height/400]
        self.rightBox2 = [383 * self.width/600,165 * self.height/400,107 * self.width/600,10 * self.height/400]
        self.topBox2 = [245 * self.width/600,75 * self.height/400,115 * self.width/600,10 * self.height/400]
        self.bottomBox2 = [43 * self.width/600,255 * self.height/400,509 * self.width/600,70 * self.height/400]
        self.surfaces2 = [self.leftBox2, self.rightBox2, self.topBox2, self.bottomBox2]
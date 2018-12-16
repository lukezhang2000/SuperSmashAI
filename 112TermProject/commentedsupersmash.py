    '''def init(self):
       self.next = 'game'
       self.state = 0
       self.homeScreen = pygame.image.load("homescreen.png")
       self.width = 600
       self.height = 400
       self.homeScreen=pygame.transform.scale(self.homeScreen,(self.width,self.height))
       self.field1 = pygame.image.load("field1.jpg")
       self.field1=pygame.transform.scale(self.field1,(self.width,self.height))
       #self.field2 = pygame.image.load("field2.jpg")

    def mousePressed(self, x, y):
        pass

    def mouseReleased(self, x, y):
        pass

    def mouseMotion(self, x, y):
        pass

    def mouseDrag(self, x, y):
        pass

    def keyPressed(self, keyCode, modifier):
        pass

    def keyReleased(self, keyCode, modifier):
        pass

    def timerFired(self, dt):
        pass

    def redrawAll(self, screen):
        pass

    def isKeyPressed(self, key):
        pass

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
            time = clock.tick(self.fps)
            self.timerFired(time)
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
    main()'''

'''class PygameGame(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.field1 = pygame.image.load("field1.jpg")
    def redrawAll(self, screen):
        self.win.blit(field1,(0,0))
import pygame'''

'''# initialize game engine
pygame.init()
# set screen width/height and caption
size = [640, 480]
screen = pygame.display.set_mode(size)
pygame.display.set_caption('My Game')
# initialize clock. used later in the loop.
clock = pygame.time.Clock()

# Loop until the user clicks close button
done = False
while done == False:
    # write event handlers here
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    # write game logic here

    # clear the screen before drawing
    screen.fill((255, 255, 255)) 
    # write draw code here

    # display what’s drawn. this might change.
    pygame.display.update()
    # run at 20 fps
    clock.tick(20)

# close the window and quit
pygame.quit()'''
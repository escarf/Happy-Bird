import pygame
import random
import math
pygame.init()

game_display = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Happy Bird")

clock = pygame.time.Clock()

image = pygame.image.load("happyBird.png")
background = pygame.image.load("backgroundnight.png")
gameoverImage = pygame.image.load("gameover.png")
startImage = pygame.image.load("startButton.png")

playerScore = 0

WHITE = (255, 255, 255)

crashed = False
started = False
gameover = False
blue = (153, 217, 234) #background
pipecolor = (50, 230, 150) #pipes
gap = 170 #distance between top and bottom pipes
pipeDistance = 190 #horizontal distance between pipes

font = pygame.font.SysFont("comicsansma",28)
scoreText = font.render("press button to start: ", True, (50, 230, 10)) #text for score
startText = font.render("press button to start: ", True, (254, 177, 204)) #text for start

#for the bird    
class player(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([49, 49])
        self.image.fill(color)

        self.rect = self.image.get_rect()

        self.image = pygame.image.load("happyBird.png").convert()
        self.image.set_colorkey(WHITE)         
 


#each topPipe sprite has its own bottom pipe
class topPipe(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        self.rect = self.image.get_rect()
        
        self.image = pygame.image.load("pipegreendown.png").convert()
        self.image.set_colorkey(WHITE)
        self.passed = False #used for score keeping
        self.bot = bottomPipe(pipecolor, 52, 320)
        self.bot.rect.y = self.rect.y + 320 + gap #set values of bottom pipe
        self.bot.rect.x = self.rect.x
    def update(self):
        self.bot.update()#update bottom pipe
        self.rect.x += 1 #move right

        #if this top pipe goes out of range, deletes itself and its bottom pipe
        if self.rect.x > 500:
            self.bot.kill() #remove bottom pipe from any groups it's in
            del self.bot #deletes bottom pipe
            self.kill() #remove from whatever sprite list(s) it's in
            del self #deletes itself

#similar to topPipe
class bottomPipe(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        self.rect = self.image.get_rect()

        self.image = pygame.image.load("pipegreenup.png").convert()
        self.image.set_colorkey(WHITE)
 
    def update(self):
        self.rect.x += 1

            
birdw = 49 #width of bird image
birdh = 49 #height of bird image
bird = player(blue, birdw, birdh)
bird.rect.x = 400 #setting location of bird
bird.rect.y = 80
v = 0.0 #velocity
dy = -6 #change in y
flap = 0.0 #pressing up increases flap, which accelerates bird upwards


toppipelist = pygame.sprite.Group() #group of all the top pipes
bottompipelist = pygame.sprite.Group() #group of all the bottom pipes


pipeCount = 4 #number of pipes that exist at a time
i = 0 #creating the first pipes here
while i < pipeCount:
    #b = bottomPipe(pipecolor, 52, 320)
    t = topPipe(pipecolor, 52, 320)
    t.rect.x = 0 - (pipeDistance * i) #each set of pipes generated is pipeDistance away from the next
    t.bot.rect.x = t.rect.x #top and bottom pipes have same x           
    t.rect.y = random.randrange(-250, 0) #random height for top pipe
    t.bot.rect.y = t.rect.y + 320 + gap #bottom pipe is a constant distance away from top pipe

    toppipelist.add(t)
    i+=1

#add pipe whenever one is deleted    
def addPipe():
    t = topPipe(pipecolor, 52, 320)
    t.rect.x = 0 - 2*pipeDistance - 50 #this works out to be a good distance
    t.bot.rect.x = t.rect.x        
       
    t.rect.y = random.randrange(-250, 0)
    t.bot.rect.y = t.rect.y + 320 + gap

    toppipelist.add(t)


while not started:
    game_display.blit(background, (0, 0))
    imagex = 50 #x coordinate of image
    imagey = 250       
    
    game_display.blit(startImage, (imagex, imagey))

    game_display.blit(startText, (20, 90))
    pygame.display.update()
    width = 195 #width and height are the size of the image
    height = 105


    #check if player clicked on the start box
    for event in pygame.event.get():
        if(event.type == pygame.MOUSEBUTTONDOWN):
            mx, my = pygame.mouse.get_pos()
            if((imagex <= mx < imagex + width )and(imagey <= my < imagey + height)):
                started = True

                
while not crashed:  

    #hit the bottom  
    if (bird.rect.y > 480):
        gameover = True
    while(gameover):
        game_display.blit(gameoverImage, (230, 250))
        game_display.blit(scoreText, (20, 20))
        pygame.display.update()
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
                crashed = True
        if(event.type == pygame.KEYDOWN):
                if(event.key == pygame.K_UP):                      
                        flap = 0.54

        elif(event.type == pygame.MOUSEBUTTONDOWN):
            flap = 0.54

        elif(event.type == pygame.KEYUP):
            if(event.key == pygame.K_UP):
                flap = 0

        elif(event.type == pygame.MOUSEBUTTONUP):
            flap = 0
        
    v -= 0.24 #constant downward accel
    v += flap #flapping moves you up
    bird.rect.y -= math.ceil(v)
    #   we have to subtract velocity since 
    #   y values increase as you go down the screen
    #   math.ceil rounds up to nearest int


    game_display.blit(background, (0, 0))
    game_display.blit(bird.image, (bird.rect.x, bird.rect.y))


    for t in toppipelist:
        game_display.blit(t.image, (t.rect.x, t.rect.y))
        game_display.blit(t.bot.image, (t.bot.rect.x, t.bot.rect.y))
        
        
        #if bird hits a pipe
        if (pygame.sprite.collide_rect(bird, t) or pygame.sprite.collide_rect(bird, t.bot)):
            gameover = True

        #if bird passes a top pipe, increase score (and mark that pipe as passed)
        #(top and bottom pipes have same x)
        if(t.passed == False and t.rect.x > bird.rect.x):
            playerScore += 1
            t.passed = True
        t.update()
   
    pipeCounter = len(toppipelist.sprites())#how many pipes are left
    if(pipeCounter < pipeCount):
        addPipe()#add one if one goes off screen 

    s = "score: " + str(playerScore)
    scoreText = font.render(s, True, (50, 230, 10))
    game_display.blit(scoreText, (20, 20))#display score
    pygame.display.update()
    
    clock.tick(60)
pygame.quit()
quit()

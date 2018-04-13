# block raiders
# a dirt-simple game framework
# arrow keys move / esc exits
# mouse aims/fires
# each time you clear the board, it respawns the same amount + 50 more
# each time you die, you lost 10 "frags" * level
# each time you kill, you gain 1 "frags" * level
# 1000 frags wins, -1000 frags loses
import pygame
import random
import math

# define some stuff
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255,255,0)
pygame.font.init()
firing = False
winlose_message = pygame.font.SysFont('Sans',48)
scoreboard = pygame.font.SysFont('Sans',30)
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
PLAY_AREA_X = SCREEN_WIDTH - 20
PLAY_AREA_Y = SCREEN_HEIGHT - 20
# Classes


class Block(pygame.sprite.Sprite):
    """ This class represents the block. """
    def __init__(self, color):
        super(Block,self).__init__()
        self.image = pygame.Surface([15, 15])
        self.image.fill(color)
        self.speed = 1
        self.rect = self.image.get_rect()
    def move_towards_player(self,player):
        if self.rect.x > player.rect.x:
            self.rect.x -= self.speed
        elif self.rect.x < player.rect.x:
            self.rect.x += self.speed
        # movement along x/y
        if self.rect.y < player.rect.y:
            self.rect.y += self.speed
        elif self.rect.y > player.rect.y:
            self.rect.y -= self.speed
    def update(self):
        if self.rect.x < 10:
            self.rect.x = 10
        if self.rect.x > PLAY_AREA_X:
            self.rect.x = PLAY_AREA_X
        if self.rect.y < 10:
            self.rect.y = 10
        if self.rect.y > PLAY_AREA_Y:
            self.rect.y = PLAY_AREA_Y
    def die (self):
        block_list.remove(self)
        all_sprites_list.remove(self)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player,self).__init__()
        self.ammo = 10
        self.frags = 0
        self.image = pygame.Surface([20, 20])
        self.image.fill(RED)
        self.level = 1
        self.rect = self.image.get_rect()
        self.speed = 2
        self.vel_x = 0
        self.vel_y = 0
    def die (self):
        self.rect.x = random.randrange(PLAY_AREA_X)
        self.rect.y = random.randrange(PLAY_AREA_Y)

def wait():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                done = True
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                for block in block_list:
                    block.die()
                for bullet in bullet_list:
                    bullet_list.remove(bullet)
                    all_sprites_list.remove(bullet)
                firing = False
                player.level = 0
                player.frags = 0
                return

                
class Bullet(pygame.sprite.Sprite):
    """ This class represents the bullet. """

    def __init__(self, start_x, start_y, dest_x, dest_y):
        super(Bullet,self).__init__()
        #drawing geometries and some other goodies
        self.image = pygame.Surface([4, 4])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y

        # because rect.x and rect.y are automatically converted to integers, we need to create different variables that
        # store the location as floating point numbers. int is not accurate enough for aiming.
        self.floating_point_x = start_x
        self.floating_point_y = start_y
        # calculating the angle in radians between the start points and end points.
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff);
        # taking into account the angle, calculate our change_x and change_y. velocity is how fast the bullet travels.
        velocity = 5
        self.change_x = math.cos(angle) * velocity
        self.change_y = math.sin(angle) * velocity
    def update(self):
        # floating point x and y hold our more accurate location.
        self.floating_point_y += self.change_y
        self.floating_point_x += self.change_x
        # rect.x and rect.y are converted to integers.
        self.rect.y = int(self.floating_point_y)
        self.rect.x = int(self.floating_point_x)

        # if bullet flies of the screen, get rid of it.
        if self.rect.x < 0 or self.rect.x > SCREEN_WIDTH or self.rect.y < 0 or self.rect.y > SCREEN_HEIGHT:
            self.kill()

pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("block raiders")
pygame.mouse.set_visible(False)

# list of every sprite. blocks, bullets, player, etc
all_sprites_list = pygame.sprite.Group()

# list of each block in the game
block_list = pygame.sprite.Group()

# list of each bullet
bullet_list = pygame.sprite.Group()

for i in range(50):
    # create an object, represents a block
    block = Block(BLUE)

    # random spawn coords
    block.rect.x = random.randrange(PLAY_AREA_X)
    block.rect.y = random.randrange(PLAY_AREA_Y)
    #add to list
    block_list.add(block)
    all_sprites_list.add(block)

# red player block
player = Player()
all_sprites_list.add(player)

# loop until true
done = False

# manage how fast the screen updates
clock = pygame.time.Clock()

score = 0

player.rect.x = SCREEN_WIDTH / 2
player.rect.y = SCREEN_HEIGHT / 2

# main loop 
while not done:
    # catch pygame.events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # this part is a total hack job to do rapid-fire bursts of x bullets
            # it saves some of the spamming of mouse1
            # get the mouse position
            pos = pygame.mouse.get_pos()
            mouse_x = pos[0]
            mouse_y = pos[1]
            #don't fire if out of ammo
            #if player.ammo > 0:
            firing = True
            #fire if has ammo
            #if player.ammo <= 0:
            #    firing = False
            #    player.ammo = 0
            #stop firing when mouse is released    
        elif event.type == pygame.MOUSEBUTTONUP:
            firing = False
            #if player.ammo <= 0:
            #    player.ammo = player.ammo + 10
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                done = True
            if event.key == pygame.K_DOWN:
                player.vel_y = player.vel_y + player.speed
            if event.key == pygame.K_UP:
                player.vel_y = player.vel_y - player.speed
            if event.key == pygame.K_LEFT:
                player.vel_x = player.vel_x - player.speed
            if event.key == pygame.K_RIGHT:
                player.vel_x = player.vel_x + player.speed
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player.vel_y = 0
            if event.key == pygame.K_UP:
                player.vel_y = 0
            if event.key == pygame.K_RIGHT:
                player.vel_x = 0
            if event.key == pygame.K_LEFT:
                player.vel_x = 0
                
    # --- Game logic

    #move the player by velocity
    player.rect.x = player.rect.x + player.vel_x
    player.rect.y = player.rect.y + player.vel_y
    if player.rect.x > (SCREEN_WIDTH - 20):
        #player.rect.x = (SCREEN_WIDTH - 10)
        player.vel_x = 0
    if player.rect.x < 0:
        #player.rect.x = 0
        player.vel_x = 0
    if player.rect.y > (SCREEN_HEIGHT -20):
        #player.rect.y = (SCREEN_HEIGHT-10)
        player.vel_y = 0
    if player.rect.y < 0:
        #player.rect.y = 10
        player.vel_y = 0
    #count the bad guys
    blockcount = 0
    for block in block_list:
        blockcount += 1
    if blockcount < 1:
        player.level += 1
        while blockcount < (50 * player.level):
            block = Block(BLUE)
    # Set a random location for the block
            block.rect.x = random.randrange(SCREEN_WIDTH)
            block.rect.y = random.randrange(SCREEN_HEIGHT - 50)
    # Add the block to the list of objects
            block_list.add(block)
            all_sprites_list.add(block)
            blockcount += 1

    #move the bad guys
    for block in block_list:
        block.move_towards_player(player)
        block.rect.x = block.rect.x + (random.randrange(-1,2))
        block.rect.y = block.rect.y + (random.randrange(-1,2))
        #did we get the player?
        block_hit_list = pygame.sprite.spritecollide(player, block_list, True)
        for block in block_hit_list:
            player.frags = player.frags - (10 * player.level)
            player.die()

    # update() method all sprites
    all_sprites_list.update()
    
    # mechanics for each bullet
    # for each in list, check hits and out-of-bounds
    
    for bullet in bullet_list:

        # if it hit a block
        block_hit_list = pygame.sprite.spritecollide(bullet, block_list, True)

        # is block hit, remove the bullet and add to the score
        for block in block_hit_list:
            bullet_list.remove(bullet)
            block.die()
            all_sprites_list.remove(bullet)
            player.frags += (1 * player.level)
            print(player.frags)

        # remove the bullet if it flies up off the screen
        if bullet.rect.y < -10:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)

    #check if firing?
    if firing == True:
        #if player.ammo <= 0:
        #        firing = False
        #        player.ammo = 0
        bullet = Bullet((player.rect.x+10), (player.rect.y+10), mouse_x, mouse_y)
            # Add the bullet to the lists
        #player.ammo = player.ammo - 1
        all_sprites_list.add(bullet)
        bullet_list.add(bullet)
            
    # --- Begin new frame
    # --- below here is basically the renderer and win/fail rules
    # --- in order from top to bottom is how it's drawn
    # --- it helps to think of it in layers
             
                                 
    # clear screen
    screen.fill(BLACK)
    
    # draw all spites
    all_sprites_list.draw(screen)
    # win/lose
    if player.frags <= -1000:
        losetext = winlose_message.render("you suck! [esc] to end [space] to restart",0,(WHITE))
        screen.blit(losetext,(5,SCREEN_HEIGHT/2))
        pygame.display.flip()
        wait()
    if player.frags >= 1000:
        wintext = winlose_message.render("you win!  [esc] to end [space] to restart",0,(WHITE))
        screen.blit(wintext,(5,SCREEN_HEIGHT/2))
        pygame.display.flip()
        wait()
        
    #draw the scoreboard
    scores = "frags: " + str(player.frags) + " level: " + str(player.level) + " blocks " + str(blockcount) + " ammo " + str(player.ammo)
    scoretext = scoreboard.render(scores,0,(WHITE))
    instructiontext = scoreboard.render("arrows/mouse - esc to exit",0,(WHITE))
    screen.blit(instructiontext,(SCREEN_WIDTH/2,SCREEN_HEIGHT-35))
    screen.blit(scoretext,(SCREEN_WIDTH/2,0))
    
    #draw the reticule
    pos = pygame.mouse.get_pos()
    mouse_x = pos[0]
    mouse_y = pos[1]
    pygame.draw.circle(screen,YELLOW,[mouse_x,mouse_y],3,2)
    
    # flip framebuffer
    pygame.display.flip()

    # --- Limit frames per second
    clock.tick(60)


pygame.quit()

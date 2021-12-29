from pygame import rect                                # TODO: Separate object and people/mob/creature/plant classes into modules 
from settings import *
import pygame as pg

vec = pg.math.Vector2
class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game    # to be able to acess all_sprites
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites  # adding player to all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)    # hard to use super() on classes from imported modules
        self.image = pg.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.vel = vec(0, 0)                # velocity vector instead of vx and vy 
        self.pos = vec(x, y) * TILESIZE     # position vector instead of x and y

        self.in_portal = False                 # player status
        self.jumping = False


    def move(self):
        boost = 0
        self.vel = vec(0, 0)                # velocity doesn't accumulate, preventing unwanted movement 

        keys = pg.key.get_pressed()
        if keys[pg.K_LSHIFT]:
            boost = RUNNING_SPEED
        if keys[pg.K_LEFT]:
            self.vel.x = -(PLAYER_SPEED + boost)
        if keys[pg.K_RIGHT]:
            self.vel.x = (PLAYER_SPEED + boost)
        if keys[pg.K_UP]:
            self.vel.y = -(PLAYER_SPEED + boost)
        if keys[pg.K_DOWN]:
            self.vel.y= (PLAYER_SPEED + boost)
        if self.vel.x != 0 and self.vel.y != 0:  # prevents faster diagonals
            self.vel.x *= .7071
            self.vel.y *= .7071


    def collision(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.vel.x > 0: # sprite moving to the right
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0: # sprite moving to the left
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0                         #stop moving
                self.rect.x = self.pos.x

            enter = pg.sprite.spritecollide(self, self.game.portals, False)
            if enter:
                self.rect.x = enter[0].rect.left
                self.rect.y = enter[0].rect.top
                self.in_portal = True

            
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.vel.y > 0: # sprite moving down
                    self.pos.y = hits[0].rect.top - self.rect.width
                if self.vel.y < 0: # sprite moving up
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0                         #stop moving
                self.rect.y = self.pos.y

            enter = pg.sprite.spritecollide(self, self.game.portals, False)
            if enter:
                self.rect.x = enter[0].rect.left
                self.rect.y = enter[0].rect.top
                self.in_portal = True

    
    def jump(self):
        if self.jumping:
            self.image.fill(BLUE)
        else:
            self.image.fill(YELLOW)
        

    def update(self):
        self.jump()
        self.move()
        self.pos += self.vel * self.game.dt # the speed
        self.rect.x = self.pos.x
        self.collision('x')
        self.rect.y = self.pos.y
        self.collision('y')

#================================================================================================================================
class Block(pg.sprite.Sprite):                      # default block is a wall
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.blocks # game.blocks for blocks objects
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Ledge(Block):
    def __init__(self, game, x, y, facing):
        super().__init__(game, x, y)
        self.face = facing
        
    def jump_over(self):
        if self.game.player.jumping == True:
            self.image.fill(BLACK)
            self.image = pg.draw.circle(self.image, GREEN, (TILESIZE, TILESIZE), 5)
        else:
            self.image = pg.Surface((TILESIZE, TILESIZE))
            self.image.fill(GREEN)

        
    def update(self):
        self.jump_over()
        
#================================================================================================================================
class Portal(pg.sprite.Sprite):
    portals = []

    def __init__(self, game, x, y, mode):
        self.game = game
        self.groups = game.all_sprites, game.portals
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()

        self.portals.append(self)

        self.mode = mode
        if self.mode == "entrance": self.image.fill(WHITE)
        else: self.image.fill(RED) 
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def activated(self, player):
        if player.rect.x == self.rect.x and player.rect.y == self.rect.y:
            return True

    def transport(self, status, player):
        
        if self.mode == "entrance" and status and self.activated(player):
            return 1
        elif self.mode == "exit" and status and self.activated(player):
            return -1
        else: 
            pass
    
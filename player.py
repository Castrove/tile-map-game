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
        self.game.portal.collision('x')
        self.game.block.collision('x')

        self.rect.y = self.pos.y
        self.game.portal.collision('y')
        self.game.block.collision('y')


    
from pygame.draw import rect
from settings import *
import pygame as pg


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game    # to be able to acess all_sprites
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites  # adding player to all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)    # hard to use super() on classes from imported modules
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x * TILESIZE
        self.y = y * TILESIZE

        self.vx, self.vy = 0, 0

    def move(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.vx = -PLAYER_SPEED
        if keys[pg.K_RIGHT]:
            self.vx = PLAYER_SPEED
        if keys[pg.K_UP]:
            self.vy = -PLAYER_SPEED
        if keys[pg.K_DOWN]:
            self.vy= PLAYER_SPEED
        if self.vx != 0 and self.vy != 0:  # prevents faster diagonals
            self.vx *= .7071
            self.vy *= .7071

    # def move(self, dx=0, dy=0):             - for simple movement
         # if not self.collision(dx, dy):
     #     self.x += dx
        #    self.y += dy

    def collision(self, dir):
        # for wall in self.game.walls:
        #     if wall.x == self.x + dx and wall.y == self.y + dy:
        #         return True
        # return False

        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0: # sprite moving to the right
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0: # sprite moving to the left
                    self.x = hits[0].rect.right
                self.vx = 0                         #stop moving
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0: # sprite moving down
                    self.y = hits[0].rect.top - self.rect.width
                if self.vy < 0: # sprite moving up
                    self.y = hits[0].rect.bottom
                self.vy = 0                         #stop moving
                self.rect.y = self.y
        

    def update(self):
        # self.rect.x = self.x * TILESIZE              - for simple by tile movement
        # self.rect.y = self.y * TILESIZE

        self.move()
        self.x += self.vx * self.game.dt    # the speed
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collision('x')
        self.rect.y = self.y
        self.collision('y')


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls # game.walls for wall objects
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
from pygame import rect
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

        # self.vx, self.vy = 0, 0
        self.in_portal = False
        self.jumping = False

    def move(self):
        boost = 0
        # self.vx, self.vy = 0, 0
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
                if self.vel.x > 0: # sprite moving to the right
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0: # sprite moving to the left
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0                         #stop moving
                self.rect.x = self.pos.x

            enter = pg.sprite.spritecollide(self, self.game.entrances, False)
            if enter:
                self.rect.x = enter[0].rect.left
                self.rect.y = enter[0].rect.top
                self.in_portal = True

            
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.y > 0: # sprite moving down
                    self.pos.y = hits[0].rect.top - self.rect.width
                if self.vel.y < 0: # sprite moving up
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0                         #stop moving
                self.rect.y = self.pos.y

            enter = pg.sprite.spritecollide(self, self.game.entrances, False)
            if enter:
                self.rect.x = enter[0].rect.left
                self.rect.y = enter[0].rect.top
                self.in_portal = True

    
    # def jump(self):

        

    #     if self.jumping:
    #         pg.time.set_timer(timer, delay)

            
    #         self.image.fill(BLUE)
    #         self.jumping == False
    #         self.image.fill(YELLOW)


        

    def update(self):
        # self.rect.x = self.x * TILESIZE              - for simple by tile movement
        # self.rect.y = self.y * TILESIZE
        
        # self.jump()
        self.move()
        self.pos += self.vel * self.game.dt # the speed
        self.rect.x = self.pos.x
        self.collision('x')
        self.rect.y = self.pos.y
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

class Door(pg.sprite.Sprite):
    portals = []

    def __init__(self, game, x, y, mode):
        self.game = game
        self.groups = game.all_sprites, game.entrances
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

    def __repr__(self):
        rep = self.mode
        return rep

    def activated(self, player):
        if player.rect.x == self.rect.x and player.rect.y == self.rect.y:
            return True

    def transport(self, status, player):
        
        # if self.mode == "entrance" and status:
        if self.mode == "entrance" and status and self.activated(player):
            return 1
        elif self.mode == "exit" and status and self.activated(player):
            return -1
        else: 
            pass
    
    
        

    # def detect_player(self, status):
    #     if status:
    #         return True
    
    # def update(self):
    #     # self.detect_player(Player.in_portal)
    #     print(Player.in_portal)

    # def player_collide(self, player):
    #     enter = pg.sprite.spritecollide(player, self.game.entrances, False)
    #     if enter:
    #         player.rect.x = self.x
    #         player.rect.y = self.y
    #         print("enter")

    # def update(self):
    #     player_collide()
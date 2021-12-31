import pygame as pg
from settings import *

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

    def collision(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self.game.player, self.game.blocks, False)
            if hits:
                if self.game.player.vel.x > 0: # sprite moving to the right
                    self.game.player.pos.x = hits[0].rect.left - self.game.player.rect.width
                if self.game.player.vel.x < 0: # sprite moving to the left
                    self.game.player.pos.x = hits[0].rect.right
                self.game.player.vel.x = 0                         #stop moving
                self.game.player.rect.x = self.game.player.pos.x


        if dir == 'y':
            hits = pg.sprite.spritecollide(self.game.player, self.game.blocks, False)
            if hits:
                if self.game.player.vel.y > 0: # sprite moving down
                    self.game.player.pos.y = hits[0].rect.top - self.game.player.rect.width
                if self.game.player.vel.y < 0: # sprite moving up
                    self.game.player.pos.y = hits[0].rect.bottom
                self.game.player.vel.y = 0                         #stop moving
                self.game.player.rect.y = self.game.player.pos.y
        
#================================================================================================================================
class Portal(pg.sprite.Sprite):
    portals = []

    def __init__(self, game, x, y, mode):
        self.game = game
        self.groups = game.all_sprites, game.portals
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()

        self.mode = mode
        if self.mode == "entrance": self.image.fill(WHITE)
        else: self.image.fill(RED) 
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

        if self.mode == 'entrance' or self.mode == 'exit':
            self.portals.append(self)

    
    def collision(self, dir):
        if dir == 'x':

            enter = pg.sprite.spritecollide(self.game.player, self.game.portals, False)
            if enter and (enter[0].mode == 'entrance' or enter[0].mode == 'entrance'):
                self.game.player.rect.x = enter[0].rect.left
                self.game.player.rect.y = enter[0].rect.top
                self.game.player.in_portal = True
            if enter and enter[0].mode == 'right':
                if self.game.player.vel.x < 0: # sprite moving to the left
                    self.game.player.pos.x = enter[0].rect.right
                    self.game.player.vel.x = 0                         #stop moving
                    self.game.player.rect.x = self.game.player.pos.x

                else:
                    self.game.player.rect.x = enter[0].rect.left
                    self.game.player.rect.y = enter[0].rect.top
                    self.game.player.in_portal = True
            
            if enter and enter[0].mode == 'left':
                if self.game.player.vel.x > 0: # sprite moving to the right
                    self.game.player.pos.x = enter[0].rect.left - self.game.player.rect.width
                    self.game.player.vel.x = 0                         #stop moving
                    self.game.player.rect.x = self.game.player.pos.x
                else:
                    self.game.player.rect.x = enter[0].rect.left
                    self.game.player.rect.y = enter[0].rect.top
                    self.game.player.in_portal = True

            if enter and (enter[0].mode == 'up' or enter[0].mode == 'down'):
                if self.game.player.vel.x > 0: # sprite moving to the right
                    self.game.player.pos.x = enter[0].rect.left - self.game.player.rect.width
                    self.game.player.vel.x = 0                         #stop moving
                    self.game.player.rect.x = self.game.player.pos.x

                elif self.game.player.vel.x < 0: # sprite moving to the left
                    self.game.player.pos.x = enter[0].rect.right
                    self.game.player.vel.x = 0                         #stop moving
                    self.game.player.rect.x = self.game.player.pos.x
            
        if dir == 'y':

            enter = pg.sprite.spritecollide(self.game.player, self.game.portals, False)
            if enter: 
                self.game.player.rect.x = enter[0].rect.left
                self.game.player.rect.y = enter[0].rect.top
                self.game.player.in_portal = True


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


class Ledge(Portal):
    def __init__(self, game, x, y, mode):
        super().__init__(game, x, y, mode)


    # def jump_over(self):
    #     if self.game.player.jumping == True:
    #         self.image.fill(BLACK)
            
    #     else:
    #         self.image = pg.Surface((TILESIZE, TILESIZE))
    #         self.image.fill(GREEN)

    
    def activated(self, player):
        if player.rect.x == self.rect.x and player.rect.y == self.rect.y:
            return True

    def transport(self, status, player):
        
        if self.mode == "left" and status and self.activated(player):
            self.game.player.pos.x = self.rect.left - TILESIZE
            self.game.player.rect.x = self.game.player.pos.x 

        elif self.mode == "right" and status and self.activated(player):
            self.game.player.pos.x = self.rect.right
            self.game.player.rect.x = self.game.player.pos.x 

        elif self.mode == "up" and status and self.activated(player):
            self.game.player.pos.y = self.rect.top - TILESIZE
            self.game.player.rect.y = self.game.player.pos.y 

        elif self.mode == "down" and status and self.activated(player):
            self.game.player.pos.y = self.rect.bottom
            self.game.player.rect.y = self.game.player.pos.y 
            
        else: 
            pass

        
    def update(self):
        # self.jump_over()
        self.transport(self.game.player.in_portal, self.game.player)
import pygame as pg
from settings import *
from player import *

# def player_input(key):
#     if key.type == pg.QUIT:           # for the close button in window
#         return "exit"
        
#     if key.type == pg.KEYDOWN:          # change number for choppy effect
#         button = key.key                # change ifs to elifs to prevent diagonal movement
#         if button == pg.K_ESCAPE:
#             return "exit"
#     #     if button == pg.K_LEFT:
#     #         return {"move": (-1, 0)}
#     #     if button == pg.K_RIGHT:
#     #         return {"move": (1, 0)}
#     #     if button == pg.K_UP:
#     #         return {"move": (0, -1)}
#     #     if button == pg.K_DOWN:
#     #         return {"move": (0, 1)}
#         if button == pg.K_SPACE:
#             return "jump"
            

#     else:
#         return "stay"


class Inputs():

    actions = []

    def __init__(self, game, key):
        self.game = game
        self.key = key

        self.actions.append(self)
        

    def events(self):

        if self.key.type == pg.QUIT:         
            self.game.playing = False
            self.game.running = False  

        if self.key.type == JUMP_TIMER:
            print("landed") 
            pg.time.set_timer(JUMP_TIMER, 0)
            self.game.player.jumping = False
            
        if self.key.type == pg.KEYDOWN:          
            button = self.key.key   

            if button == pg.K_ESCAPE:
                self.game.playing = False
                self.game.running = False

            if button == pg.K_r:
                self.game.playing = False

            if button == pg.K_SPACE:
                pg.time.set_timer(JUMP_TIMER, JUMP_DELAY)
                print("jumped")
                self.game.player.jumping = True  
                    

        else:
            pass

        self.actions.clear()
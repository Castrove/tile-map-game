import sys, random
from os import path
from typing import ClassVar
import pygame as pg
from input import player_input
from settings import *
from contents import *


class Game:
    def __init__(self):
        # initialize game window, etc.
        pg.init()
        self.win = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True

        pg.key.set_repeat(300,100) # by millisecond; repeats the key pressed every interval


    def load_data(self):    # load map
        game_folder = path.dirname(__file__)
        self.map_data = []
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line)


    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.LayeredUpdates()
        self.enemies = pg.sprite.LayeredUpdates()
        self.attacks = pg.sprite.LayeredUpdates()

        #spawn wall
        self.load_data()
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                elif tile == 'P':
                    self.player = Player(self, col, row)


        self.run()

    def run(self):
        # Starts game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
        # insert confirmation option to quit before closing program
        # insert self.running = False here

    def quit(self):
        pass

    def events(self):
        # Game loop - catch all events here
        for event in pg.event.get():
            self.action = player_input(event)

            if self.action == "exit":
                self.playing = False      # stops game; starts new game
                self.running = False   # stops program
            if self.action == "stay":
                pass
            
            # if "move" in self.action:
            #     x, y = self.action["move"]
            
            #     self.player.move(dx=x, dy=y)
            
    def update(self):
        # Game loop - update portion of the game loop
        self.all_sprites.update()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.win, LIGHTGREY, (x,0), (x,HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.win, LIGHTGREY, (0,y), (WIDTH,y))


    def draw(self):
        # Game loop - draw
        self.win.fill(BLACK)
        self.draw_grid()
        self.all_sprites.draw(self.win) # prepares drawing

        pg.display.update()     # presents drawing


    def start_win(self):
        pass

    def game_over(self):
        pass

# create the game object
g = Game()
while g.running:
    g.start_win()
    g.new()             # run instead when loading save can be done
    g.game_over()

pg.quit()

# TODO: GAME CONCEPT: theme, gimmick, goal
            # dungeon crawler but wilderness/explorer theme, with platformer bits, maybe catching?

# TODO: enemy class
# TODO: entity attack
# TODO: entity health

# TODO: ability to save/load/reset progress: thru .sav file or database? | must have account

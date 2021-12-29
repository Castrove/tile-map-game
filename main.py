import sys, random
from os import path
import pygame as pg
from input import *
from settings import *
from contents import *
from tilemap import *


class Game:
    def __init__(self):
        # initialize game window, etc.
        pg.init()
        self.win = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True

        self.level = 1
        self.prev_level = self.level


    def load_data(self):    # load map
        # game_folder = path.dirname(__file__)
        map_file = f"map{self.level}.txt"
        game_folder = [path.dirname(__file__),"assets","map",map_file]  


        print("prev:", self.prev_level)
        if not path.isfile(path.join(*game_folder)):

            self.level = self.prev_level
            map_file = f"map{self.level}.txt"
            game_folder = [path.dirname(__file__),"assets","map",map_file]  

            
        self.map = Map(path.join(*game_folder))     # stores the info in map object
    

    def new(self):
        #spawn wall
        self.load_data()            # prepares the map
        Portal.portals.clear()      # resets the active portals

        self.map.render(self)       # creates the map
        self.camera = Camera(self.map.width, self.map.height)   # spawns camera   

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
            input = Inputs(self, event)
            self.action = input.events()

        for portal in Portal.portals:    
            increment = portal.transport(self.player.in_portal, self.player)
            
            if increment == None:
                continue

            self.prev_level = self.level
            self.level += increment
            self.new()


    def update(self):
        # Game loop - update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)


    def draw_grid(self):
        for x in range(self.camera.x, WIDTH, TILESIZE):
            pg.draw.line(self.win, LIGHTGREY, (x,0), (x,HEIGHT))
        for y in range(self.camera.y, HEIGHT, TILESIZE):
            pg.draw.line(self.win, LIGHTGREY, (0,y), (WIDTH,y))


    def draw(self):
        # Game loop - draw
        self.win.fill(BLACK)
        self.draw_grid()
        # self.all_sprites.draw(self.win) # prepares drawing
        for sprite in self.all_sprites:
            self.win.blit(sprite.image, self.camera.apply(sprite))

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

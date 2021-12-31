import pygame as pg

from contents import *
from settings import *

class Map:
    
    def __init__(self, filename):
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())
    
        self.tilewidth = len(self.data[0])          # width of map by tile
        self.tileheight = len(self.data)            # height of map by tile
        self.width = self.tilewidth * TILESIZE      # by pixel
        self.height = self.tileheight * TILESIZE    # by pixel

    def render(self, game):                 # renders the map for the main program
        # initialize all variables and do all the setup for a new game
        game.all_sprites = pg.sprite.LayeredUpdates()
        game.blocks = pg.sprite.LayeredUpdates()
        game.portals = pg.sprite.LayeredUpdates()
        game.enemies = pg.sprite.LayeredUpdates()
        game.attacks = pg.sprite.LayeredUpdates()

        for row, tiles in enumerate(self.data):     # Make sure tile map has no blank line at the start to prevent issues ! ! ! !
            for col, tile in enumerate(tiles):
                if tile == '#':
                    game.block = Block(game, col, row)
                elif tile == 'P':
                    game.player = Player(game, col, row)
                elif tile == '0':
                    game.portal = Portal(game, col, row, "entrance")
                elif tile == "X":
                    game.portal = Portal(game, col, row, "exit")  
                elif tile == "/":
                    game.edge = Ledge(game, col, row, "left")
                elif tile == "\\":
                    game.edge = Ledge(game, col, row, "right")
                elif tile == "=":
                    game.edge = Ledge(game, col, row, "up")
                elif tile == "_":
                    game.edge = Ledge(game, col, row, "down")
    
class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height
    
    # shift the rectangle
    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)    

    # update itself to where the player is
    def update(self, target):
        self.x = -target.rect.x + (WIDTH // 2) 
        self.y = -target.rect.y + (HEIGHT // 2)

        # limit scrolling to map size
        self.x = min( 3*TILESIZE , self.x ) # min(offset, x coordinate) LEFT
        self.y = min( 3*TILESIZE , self.y ) # TOP
        self.x = max( -(self.width - WIDTH) - (3*TILESIZE) , self.x )    # RIGHT
        self.y = max( -(self.height - HEIGHT) - (3*TILESIZE) , self.y )  # BOTTOM
        self.camera = pg.Rect(self.x, self.y, self.width, self.height)

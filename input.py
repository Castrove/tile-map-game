import pygame as pg

def player_input(key):
    if key.type == pg.QUIT:           # for the close button in window
        return "exit"
        
    if key.type == pg.KEYDOWN:          # change number for choppy effect
        button = key.key                # change ifs to elifs to prevent diagonal movement
        if button == pg.K_ESCAPE:
            return "exit"
    #     if button == pg.K_LEFT:
    #         return {"move": (-1, 0)}
    #     if button == pg.K_RIGHT:
    #         return {"move": (1, 0)}
    #     if button == pg.K_UP:
    #         return {"move": (0, -1)}
    #     if button == pg.K_DOWN:
    #         return {"move": (0, 1)}

    else:
        return "stay"
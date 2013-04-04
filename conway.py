import sys, pygame
import numpy as np
import time, sys
from rle_read import rle_read
pygame.init()

# (width, height) in actual pixels
screenres = (600, 600)

# these must divide evenly into screenres width and height
zoom = [1, 2, 3, 6, 8, 10]

# zoom 6 (100x100 cells)
zoom_lvl = 3

max_zlvl = len(zoom) - 1

shiftspeed = 4 # number of spaces to shift when pressing arrow keys
fps = 30 # frames per second

livecells = set()

if len(sys.argv) == 2:
    rle_fname = sys.argv[1]
    shape = rle_read(rle_fname)
    for xx in range(shape.shape[0]):
        for yy in range(shape.shape[1]):
            if shape[xx,yy]:
                livecells.add((xx,yy))

def board2pygame(x, y):
    return x*zoom[zoom_lvl]+screenres[0]/2, y*zoom[zoom_lvl]+screenres[1]/2

def pygame2board(x, y):
    return (x-screenres[0]/2)/zoom[zoom_lvl], (y-screenres[1]/2)/zoom[zoom_lvl]

def update(cells):
    checkcells = set()
    new_cells = set()
    for cell in cells:
        for xx in range(cell[0]-1, cell[0]+2):
            for yy in range(cell[1]-1, cell[1]+2):
                checkcells.add((xx,yy))
    for cell in checkcells:
        count = 0
        for xx in range(cell[0]-1, cell[0]+2):
            for yy in range(cell[1]-1, cell[1]+2):
                if (xx,yy) != cell and (xx,yy) in cells:
                    count += 1
        if cell in cells:
            if count > 1 and count < 4:
                new_cells.add(cell)
        else:
            if count == 3:
                new_cells.add(cell)
    return new_cells

def shift(cells, dx, dy):
    new_cells = set()
    for cell in cells:
        new_cells.add((cell[0]+dx, cell[1]+dy))
    return new_cells

black = 0, 0, 0
white = 255, 255, 255
grey = 50, 50, 50

screen = pygame.display.set_mode(screenres)

background = pygame.Surface(screenres)
background.fill(black)

running = False
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_ESCAPE or event.key == pygame.K_q):
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_SPACE:
                if running:
                    running = False
                    print "Stopped."
                else:
                    running = True
                    print "Running."
            elif event.key == pygame.K_c:
                livecells = set()
            elif event.key == pygame.K_LEFT:
                livecells = shift(livecells, shiftspeed, 0)
            elif event.key == pygame.K_RIGHT:
                livecells = shift(livecells, -shiftspeed, 0)
            elif event.key == pygame.K_UP:
                livecells = shift(livecells, 0, shiftspeed)
            elif event.key == pygame.K_DOWN:
                livecells = shift(livecells, 0, -shiftspeed)
            elif event.key == pygame.K_EQUALS:
                if zoom_lvl < max_zlvl:
                    zoom_lvl += 1
            elif event.key == pygame.K_MINUS:
                if zoom_lvl > 0:
                    zoom_lvl -= 1

    #pygame.event.get()
    b1, b2, b3 = pygame.mouse.get_pressed()
    mousepos = pygame.mouse.get_pos()
    xpos = mousepos[0]
    ypos = mousepos[1]
    if b1:
        livecells.add(pygame2board(xpos, ypos))
    elif b3 and pygame2board(xpos, ypos) in livecells:
        livecells.remove(pygame2board(xpos, ypos))
    
    screen.blit(background, (0,0))

    if zoom_lvl == max_zlvl:
        lines_x = range(zoom[zoom_lvl], screenres[0], zoom[zoom_lvl])
        lines_y = range(zoom[zoom_lvl], screenres[1], zoom[zoom_lvl])
        for line_x in lines_x:
            pygame.draw.line(screen, grey, (line_x,0), (line_x,screenres[1]), 1)
        for line_y in lines_y:
            pygame.draw.line(screen, grey, (0,line_y), (screenres[0],line_y), 1)
    
    for cell in livecells:
        c_x, c_y = board2pygame(cell[0], cell[1])
        if zoom[zoom_lvl] > 1:
            pygame.draw.rect(screen, white,\
                [c_x,c_y,zoom[zoom_lvl],zoom[zoom_lvl]], 0)
        else:
            screen.set_at((c_x, c_y), white)

    if running:
        livecells = update(livecells)
    
    time.sleep(1./fps)
    pygame.display.flip()

import pygame
import random

# creating the data structure for pieces
# setting up global vars
# functions
# - create_grid
# - draw_grid
# - draw_window
# - rotating shape in main
# - setting up the main

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""

pygame.font.init()

# GLOBALS VARS
s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height


# SHAPE FORMATS
S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape


class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y 
        self.shape = shape 
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


def create_grid(locked_positions = {}):
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                color = locked_positions[(j, i)]
                grid[i][j] = color
    return grid

def convert_shape_format(piece):
    positions = []
    format = piece.shape[piece.rotation % len(piece.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column  == '0':
                positions.append((piece.x + j, piece.y + i))
    
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)
    
    return positions

def valid_space(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted_shape = convert_shape_format(shape)

    for pos in formatted_shape: 
        if pos not in accepted_pos:
            if pos[1] > -1: 
                return False 
    return True 
    

def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1: 
            return True 
    
    return False 

def get_shape():
    return Piece(5, 0, random.choice(shapes))

def draw_text_middle(win, text, size, color):  
    font = pygame.font.SysFont("impact", size)
    label = font.render(text, 1, color)

    win.blit(label, (top_left_x + play_width/2 - (label.get_width()/2), top_left_y + play_height/2 - (label.get_height()/2)))
    
   
def draw_grid(win, grid):
    start_x = top_left_x
    start_y = top_left_y

    for i in range(len(grid)):
        pygame.draw.line(win, (128, 128, 128), (start_x, start_y + i*block_size), (start_x + play_width, start_y + i*block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(win, (128, 128, 128), (start_x + j*block_size, start_y), (start_x + j*block_size, start_y + play_height))
    
def clear_rows(grid, locked):
    inc = 0
    for i in range(len(grid) -1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1 
            ind = i 
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    
    # Remove the line from the grid and shift all lines above it down by one
    if inc > 0: 
        for key in sorted(list(locked), key = lambda x: x[1])[::-1]:
            x, y = key 
            if y < ind: 
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
    
    return inc 


def draw_next_shape(piece, win):
    font = pygame.font.SysFont('impact', 30)
    label = font.render('Next shape', 1, (255, 255, 255))

    start_x = top_left_x + play_width + 50
    start_y = top_left_y + play_height/2 - 100
    format = piece.shape[piece.rotation % len(piece.shape)]
    
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(win, piece.color, (start_x + j*block_size, start_y + i*block_size, block_size, block_size), 0)

    win.blit(label, (start_x + 10, start_y - 30))

def update_score(newScore): 
    score = max_score()
    
    with open('scores.txt', 'w') as file:
        if newScore > int(score): 
            file.write(str(newScore))
        else: 
            file.write(str(score))

def max_score():
    with open('scores.txt', 'r') as file:
        lines = file.readlines() 
        score = lines[0].strip()
    
    return score

def draw_window(win, grid, score=0, high_score=0):
    win.fill((0, 0, 0))

    pygame.font.init()
    font = pygame.font.SysFont('impact', 60)
    label = font.render('Tetris', 1, (255, 255, 255))

    win.blit(label, (top_left_x + play_width/2 - label.get_width()/2, 30))

    font = pygame.font.SysFont('impact', 30)
    label = font.render('Score: ' + str(score), 1, (255, 255, 255))

    start_x = top_left_x + play_width + 50
    start_y = top_left_y + play_height/2 - 100

    win.blit(label, (start_x + 20, start_y + 200))

    label = font.render('High Score: ' + str(high_score), 1, (255, 255, 255))

    start_x = top_left_x - 220
    start_y = top_left_y + play_height/2 - 100

    win.blit(label, (start_x + 10, start_y - 200))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(win, grid[i][j], (top_left_x + j*block_size, top_left_y + i*block_size, block_size, block_size), 0)

    pygame.draw.rect(win, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 4)

    draw_grid(win, grid)

def main(win):
    high_score = max_score()
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False 
    run = True 
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    level_time = 0 

    score = 0


    while run: 
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time/1000 > 5: 
            level_time = 0 
            if fall_speed > 0.12: 
                fall_speed -= 0.005

        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not(valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False 
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.rotation -= 1

        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color
        
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10

         
        draw_window(win, grid, score, high_score)
        draw_next_shape(next_piece, win)  

        pygame.display.update()

        if check_lost(locked_positions):
            draw_text_middle(win, "YOU LOST!", 120, (255, 255, 255))
            pygame.display.update()
            pygame.time.delay(2500)
            run = False 
            update_score(score)

def main_menu(win):
    run = True 
    while run: 
        win.fill((0, 0, 0))
        draw_text_middle(win, 'Press Any Key To Play', 60, (255, 255, 255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False 
            if event.type == pygame.KEYDOWN:
                main(win)

    pygame.display.quit()


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')
main_menu(win)  # start game
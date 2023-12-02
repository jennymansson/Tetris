from shapes import *
import pygame 

# global variables
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
PLAY_WIDTH = 300  # meaning 300 // 10 = 30 width per block
PLAY_HEIGHT = 600  # meaning 600 // 20 = 20 height per block
BLOCK_SIZE = 30

TOP_LEFT_X = (SCREEN_WIDTH - PLAY_WIDTH) // 2
TOP_LEFT_Y = SCREEN_HEIGHT - PLAY_HEIGHT

def create_grid(locked_positions = {}):
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                color = locked_positions[(j, i)]
                grid[i][j] = color
    return grid

def draw_grid(win, grid):
    start_x = TOP_LEFT_X
    start_y = TOP_LEFT_Y

    for i in range(len(grid)):
        pygame.draw.line(win, (128, 128, 128), (start_x, start_y + i*BLOCK_SIZE), (start_x + PLAY_WIDTH, start_y + i*BLOCK_SIZE))
        for j in range(len(grid[i])):
            pygame.draw.line(win, (128, 128, 128), (start_x + j*BLOCK_SIZE, start_y), (start_x + j*BLOCK_SIZE, start_y + PLAY_HEIGHT))

def draw_text_middle(win, text, size, color):  
    font = pygame.font.SysFont("impact", size)
    label = font.render(text, 1, color)

    win.blit(label, (TOP_LEFT_X + PLAY_WIDTH/2 - (label.get_width()/2), TOP_LEFT_Y + PLAY_HEIGHT/2 - (label.get_height()/2)))


def draw_window(win, grid, score=0, high_score=0):
    win.fill((0, 0, 0))

    pygame.font.init()
    font = pygame.font.SysFont('impact', 60)
    label = font.render('Tetris', 1, (255, 255, 255))

    win.blit(label, (TOP_LEFT_X + PLAY_WIDTH/2 - label.get_width()/2, 30))

    font = pygame.font.SysFont('impact', 30)
    label = font.render('Score: ' + str(score), 1, (255, 255, 255))

    start_x = TOP_LEFT_X + PLAY_WIDTH + 50
    start_y = TOP_LEFT_Y + PLAY_HEIGHT/2 - 100

    win.blit(label, (start_x + 20, start_y + 200))

    label = font.render('High Score: ' + str(high_score), 1, (255, 255, 255))

    start_x = TOP_LEFT_X - 220
    start_y = TOP_LEFT_Y + PLAY_HEIGHT/2 - 100

    win.blit(label, (start_x + 10, start_y - 200))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(win, grid[i][j], (TOP_LEFT_X + j*BLOCK_SIZE, TOP_LEFT_Y + i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    pygame.draw.rect(win, (255, 0, 0), (TOP_LEFT_X, TOP_LEFT_Y, PLAY_WIDTH, PLAY_HEIGHT), 4)

    draw_grid(win, grid)

def draw_next_shape(piece, win):
    font = pygame.font.SysFont('impact', 30)
    label = font.render('Next shape', 1, (255, 255, 255))

    start_x = TOP_LEFT_X + PLAY_WIDTH + 50
    start_y = TOP_LEFT_Y + PLAY_HEIGHT/2 - 100
    format = piece.shape[piece.rotation % len(piece.shape)]
    
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(win, piece.color, (start_x + j*BLOCK_SIZE, start_y + i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    win.blit(label, (start_x + 10, start_y - 30))
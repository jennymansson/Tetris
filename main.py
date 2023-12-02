from shapes import *
from display import *
from game_logic import * 

import pygame
pygame.font.init()

"""

This module contains the main game loop and menu for the Tetris game. It initializes the game window,
handles user input, updates the game state, and displays the game elements.
"""

def main(win):
    """
    Main game loop for Tetris.

    Parameters:
    - win: The game window created using the pygame module.
    """
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

        # Level up the game by decreasing the fall speed to make it more difficult 
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

        # Control of the game piece, as well as quit the game (keyboard listeners) 
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

        # Color the piece to the grid 
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color
        
        # If the current piece has hit the bottom, lock the piece to the grid, load next shape 
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

        # Check if player has lost the game 
        if check_lost(locked_positions):
            draw_text_middle(win, "YOU LOST!", 120, (255, 255, 255))
            pygame.display.update()
            pygame.time.delay(2500)
            run = False 
            update_score(score)

def main_menu(win):
    """
    Main menu loop for Tetris.

    Parameters:
    - win: The game window created using the pygame module.
    """
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


win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tetris')
main_menu(win)  # start game
from shapes import *
from display import * 
import random 

"""
This module contains functions related to the game logic of Tetris. It includes functions for
converting the shape format, checking the validity of a space for a shape in the grid,
checking if the player has lost, obtaining a new random shape, clearing completed rows, and
updating and retrieving the player's score.
"""

def convert_shape_format(piece):
    """
    Converts the shape format based on the rotation of the piece.

    Parameters:
    - piece: An instance of the Piece class representing the current game piece.

    Returns:
    - positions: A list of (x, y) positions occupied by the piece.
    """
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
    """
    Checks if the space for the shape in the grid is valid.

    Parameters:
    - shape: An instance of the Piece class representing the current game piece.
    - grid: A 2D list representing the game grid.

    Returns:
    - True if the space is valid, False otherwise.
    """
    accepted_pos = [(j, i) for j in range(10) for i in range(20) if grid[i][j] == (0, 0, 0)]

    formatted_shape = convert_shape_format(shape)

    for pos in formatted_shape: 
        if pos not in accepted_pos:
            if pos[1] > -1: 
                return False 
    return True

def check_lost(positions):
    """
    Checks if the player has lost.

    Parameters:
    - positions: A list of (x, y) positions occupied by the locked game pieces.

    Returns:
    - True if the player has lost, False otherwise.
    """
    for pos in positions:
        x, y = pos
        if y < 1: 
            return True 
    
    return False 

def get_shape():
    """
    Obtains a new random shape for the game piece.

    Returns:
    - An instance of the Piece class representing the new game piece.
    """
    return Piece(5, 0, random.choice(SHAPES))

def clear_rows(grid, locked):
    """
    Clears completed rows in the grid and updates locked positions.

    Parameters:
    - grid: A 2D list representing the game grid.
    - locked: A dictionary representing the locked positions of game pieces.

    Returns:
    - The number of rows cleared.
    """
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

def update_score(newScore): 
    """
    Updates the high score in scores.txt file.

    Parameters:
    - new_score: The new score achieved by the player.
    """
    score = max_score()
    
    with open('scores.txt', 'w') as file:
        if newScore > int(score): 
            file.write(str(newScore))
        else: 
            file.write(str(score))

def max_score():
    """
    Retrieves the highest score from the scores.txt file.

    Returns:
    - The highest score as a string.
    """
    with open('scores.txt', 'r') as file:
        lines = file.readlines() 
        score = lines[0].strip()
    
    return score

from shapes import *
from display import * 
import random 

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
    # Accepted positions
    accepted_pos = [(j, i) for j in range(10) for i in range(20) if grid[i][j] == (0, 0, 0)]

    # Formatted shape positions
    formatted_shape = convert_shape_format(shape)

    # Check if any position of the shape is outside the accepted positions
    for pos in formatted_shape: 
        if pos not in accepted_pos:
            # Check if the shape position is inside the grid boundaries
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
    return Piece(5, 0, random.choice(SHAPES))

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

import tkinter as tk
import random

#constants 
GAME_WIDTH = 1000
GAME_HEIGHT = 700
DELAY_MS = 100
SPACE_SIZE = 20
BODY_PARTS = 3
SNAKE_COLOR = "#167A16"
FOOD_COLOR = "#E91E63" 
BACKGROUND_COLOR = "#000000"
INITIAL_DIRECTION = "Right"

COLS = GAME_WIDTH // SPACE_SIZE
ROWS = GAME_HEIGHT // SPACE_SIZE
TOTAL_CELLS = COLS * ROWS

OPPOSITES = {"left": "right", "right": "left", "up": "down", "down": "up"}

#game state (start_game / restart_game)
window = None
canvas = None
label = None
snake = None
food = None
score = 0
direction = INITIAL_DIRECTION
next_direction = INITIAL_DIRECTION
game_running = False


#classes
class Snake:
    def __init__(self):
        self.coordinates = []
        self.squares = []

        start_x = (COLS // 2) * SPACE_SIZE
        start_y = (ROWS // 2) * SPACE_SIZE

        #create the initial snake body head and body trailing to the left snake moves to right
        for i in range(BODY_PARTS):
        self.coordinates.append([start_x - i * SPACE_SIZE, start_y])

        for x, y in self.coordinates:
        square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
        self.squares.append(square)



class food:
    def __init__(self, x, y):
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

#FUNCTIONS
def create_food(snake):
    """Place food on random free cell. returnes None if the board is full. """
    occupied={tuple(c) for c in snake.coordinates}
    free_cells = [(col * SPACE_SIZE, row * SPACE_SIZE) for col in range(COLS) for row in range(ROWS) 
                  if (col * SPACE_SIZE, row * SPACE_SIZE) not in occupied]
    if not free_cells:
        return None

    x, y = random.choice(free_cells)
    return Food(x, y)

def next_turn(snake, food):
    global direction, score

    #apply the requested direction once per tick
    direction = next_direction
    x,y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE
snake.coordinates.insert(0, (x, y))

def change_direction(new_direction):

def check_collision():

def game_over():

def reset_state():

def restart_game():

def start_game():

        

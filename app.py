import tkinter as tk
import random

# constants
GAME_WIDTH = 1000
GAME_HEIGHT = 500
DELAY_MS = 100
SPACE_SIZE = 20
BODY_PARTS = 3
SNAKE_COLOR = "#167A16"
FOOD_COLOR = "#E91E63"
BACKGROUND_COLOR = "#000000"
INITIAL_DIRECTION = "right"

COLS = GAME_WIDTH // SPACE_SIZE
ROWS = GAME_HEIGHT // SPACE_SIZE
TOTAL_CELLS = COLS * ROWS

OPPOSITES = {"left": "right", "right": "left", "up": "down", "down": "up"}

# game state (start_game / restart_game)
window = None
canvas = None
label = None
snake = None
food = None
score = 0
direction = INITIAL_DIRECTION
next_direction = INITIAL_DIRECTION
game_running = False


# classes
class Snake:
    def __init__(self):
        self.coordinates = []
        self.squares = []

        start_x = (COLS // 2) * SPACE_SIZE
        start_y = (ROWS // 2) * SPACE_SIZE

        # The body trails to the left so the snake can start moving right.
        for i in range(BODY_PARTS):
            self.coordinates.append([start_x - i * SPACE_SIZE, start_y])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(
                x,
                y,
                x + SPACE_SIZE,
                y + SPACE_SIZE,
                fill=SNAKE_COLOR,
                tag="snake",
            )
            self.squares.append(square)


class Food:
    def __init__(self, x, y):
        self.coordinates = [x, y]
        canvas.create_oval(
            x,
            y,
            x + SPACE_SIZE,
            y + SPACE_SIZE,
            fill=FOOD_COLOR,
            tag="food",
        )


# Functions
def create_food(snake):
    """Place food on a free cell, or return None if the board is full."""
    occupied = {tuple(coordinate) for coordinate in snake.coordinates}
    free_cells = [
        (col * SPACE_SIZE, row * SPACE_SIZE)
        for col in range(COLS)
        for row in range(ROWS)
        if (col * SPACE_SIZE, row * SPACE_SIZE) not in occupied
    ]
    if not free_cells:
        return None

    x, y = random.choice(free_cells)
    return Food(x, y)


def next_turn(snake, current_food):
    global direction, score

    if current_food is None:
        game_over(won=True)
        return

    # Apply the requested direction once per tick.
    direction = next_direction
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE
    snake.coordinates.insert(0, [x, y])

    square = canvas.create_rectangle(
        x,
        y,
        x + SPACE_SIZE,
        y + SPACE_SIZE,
        fill=SNAKE_COLOR,
        tag="snake",
    )
    snake.squares.insert(0, square)

    if x == current_food.coordinates[0] and y == current_food.coordinates[1]:
        score += 1
        label.config(text=f"Score: {score}")
        canvas.delete("food")
        current_food = create_food(snake)
    else:
        # Remove the tail first so moving into its old cell remains legal.
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collision(snake):
        game_over()
    elif current_food is None:
        game_over(won=True)
    else:
        window.after(DELAY_MS, next_turn, snake, current_food)


def change_direction(new_direction):
    global next_direction
    if OPPOSITES[new_direction] != direction:
        next_direction = new_direction


def check_collision(snake):
    x, y = snake.coordinates[0]
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True

    return [x, y] in snake.coordinates[1:]


def game_over(won=False):
    global game_running
    game_running = False
    canvas.delete(tk.ALL)

    title = "You won!" if won else "Game Over!"
    canvas.create_text(
        canvas.winfo_width() / 2,
        canvas.winfo_height() / 2,
        font=("consolas", 36, "bold"),
        text=f"{title}\nPress R or Space to restart",
        fill="gold" if won else "red",
        tag="game_over",
    )


def reset_state():
    global snake, food, score, direction, next_direction
    canvas.delete(tk.ALL)
    snake = Snake()
    food = create_food(snake)
    score = 0
    direction = INITIAL_DIRECTION
    next_direction = INITIAL_DIRECTION
    label.config(text=f"Score: {score}")


def restart_game(event):
    global game_running
    if game_running:
        return
    reset_state()
    game_running = True
    next_turn(snake, food)


def start_game():
    global window, canvas, label, game_running
    window = tk.Tk()
    window.title("Snake Game")
    window.resizable(False, False)

    label = tk.Label(window, text="Score: 0 ", font=("consolas", 40))
    label.pack()

    canvas = tk.Canvas(
        window,
        bg=BACKGROUND_COLOR,
        height=GAME_HEIGHT,
        width=GAME_WIDTH,
    )
    canvas.pack()

    window.update()

    window_width = window.winfo_width()
    window_height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))

    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    window.bind("<Left>", lambda event: change_direction("left"))
    window.bind("<Right>", lambda event: change_direction("right"))
    window.bind("<Up>", lambda event: change_direction("up"))
    window.bind("<Down>", lambda event: change_direction("down"))
    window.bind("<R>", restart_game)
    window.bind("<r>", restart_game)
    window.bind("<space>", restart_game)

    reset_state()
    game_running = True
    next_turn(snake, food)
    window.mainloop()


if __name__ == "__main__":
    start_game()

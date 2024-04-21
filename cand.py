import tkinter as tk
import random

# Constants
ROWS = 8
COLS = 8
CELL_SIZE = 50
WINDOW_WIDTH = COLS * CELL_SIZE
WINDOW_HEIGHT = ROWS * CELL_SIZE

# Candy colors
COLORS = ["red", "green", "blue", "yellow", "orange"]

# Game board
board = [[random.choice(COLORS) for _ in range(COLS)] for _ in range(ROWS)]

# Stack for storing selected candies
selected_candies = []

def select_candy(row, col):
    candy_color = board[row][col]
    selected_candies.append((row, col))

    if len(selected_candies) >= 2:
        # Check if candies are adjacent
        if abs(selected_candies[-1][0] - selected_candies[-2][0]) + abs(selected_candies[-1][1] - selected_candies[-2][1]) == 1:
            swap_candies()
        else:
            selected_candies.pop(0)

    draw_board()

def swap_candies():
    row1, col1 = selected_candies[-2]
    row2, col2 = selected_candies[-1]
    board[row1][col1], board[row2][col2] = board[row2][col2], board[row1][col1]
    selected_candies.clear()

    # Check for matches
    matched_candies = find_matches()
    if matched_candies:
        remove_matches(matched_candies)
        refill_board()

def find_matches():
    matched_candies = []
    for row in range(ROWS):
        for col in range(COLS):
            candy = board[row][col]
            if candy == "":
                continue

            # Check horizontal matches
            if col + 2 < COLS and board[row][col + 1] == candy and board[row][col + 2] == candy:
                matched_candies.extend([(row, col), (row, col + 1), (row, col + 2)])

            # Check vertical matches
            if row + 2 < ROWS and board[row + 1][col] == candy and board[row + 2][col] == candy:
                matched_candies.extend([(row, col), (row + 1, col), (row + 2, col)])

    return matched_candies

def remove_matches(matched_candies):
    for row, col in matched_candies:
        board[row][col] = ""

def refill_board():
    for col in range(COLS):
        empty_cells = [row for row in range(ROWS) if board[row][col] == ""]
        num_empty_cells = len(empty_cells)
        for row in range(ROWS - 1, -1, -1):
            if row < ROWS - num_empty_cells:
                board[row][col] = board[empty_cells[row]][col]
            else:
                board[row][col] = random.choice(COLORS)

def draw_board():
    canvas.delete("all")

    for row in range(ROWS):
        for col in range(COLS):
            x1, y1 = col * CELL_SIZE, row * CELL_SIZE
            x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
            color = board[row][col]
            canvas.create_rectangle(x1, y1, x2, y2, fill=color)

    for row, col in selected_candies:
        x1, y1 = col * CELL_SIZE, row * CELL_SIZE
        x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
        canvas.create_rectangle(x1, y1, x2, y2, outline="black", width=2)

def click(event):
    col = event.x // CELL_SIZE
    row = event.y // CELL_SIZE
    select_candy(row, col)

# Initialize the GUI
root = tk.Tk()
root.title("Candy Crush")
canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
canvas.pack()

draw_board()
canvas.bind("<Button-1>", click)

# Start the GUI main loop
root.mainloop()

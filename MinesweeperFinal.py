import numpy as np
import tkinter as tk

# Constants
EMPTY = 0
MINE = 1
UNKNOWN = -1

# Create the main window
window = tk.Tk()
window.title("Minesweeper")

# Grid number (grd x grd)
grd = 9
# Generate random mines
mines_count = 12  # Number of mines (in 9x9 games, can place mines with 10 - 12 mines)
mines_indices = np.random.choice((grd*grd), mines_count, replace=False)

# Create the grid
grid = np.zeros((grd, grd), dtype=int)
grid.flat[mines_indices] = MINE

player_grid = np.full((grd, grd), UNKNOWN)

# Count the number of bombs surrounding the selected cell
def count(row, col):
    offsets = ((-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1))
    count = 0
    for offset in offsets:
        offset_row = row + offset[0]
        offset_col = col + offset[1]

        # Check for boundaries
        if 0 <= offset_row <= grd-1 and 0 <= offset_col <= grd-1:
            if grid[offset_row][offset_col] == MINE:
                count += 1
    return count

# Create game over message label
label_gameover = None

# Create win message label
label_win = None

# Create retry button
retry_button = None

# Selecting the cell
def click(row, col):
    # Check if it is a bomb
    if grid[row][col] == MINE:
        labels[row][col]["text"] = "X"  # Display the clicked mine
        global label_gameover
        label_gameover = tk.Label(window, text="LOL!, Better Luck Next Time :D")
        label_gameover.grid(row=grd+1, columnspan=grd)
        global retry_button
        retry_button = tk.Button(window, text="Retry", command=reset_game)
        retry_button.grid(row=grd+2, columnspan=grd)
        disable_grid()  # Disable the grid after game over
    elif player_grid[row][col] == UNKNOWN:
        reveal_neighbors(row, col)
        check_win()

# Function to disable the grid
def disable_grid():
    for row in range(grd):
        for col in range(grd):
            labels[row][col]["state"] = tk.DISABLED

# Reveal the cell and its neighbors recursively if empty
def reveal_neighbors(row, col):
    offsets = ((-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1))
    player_grid[row][col] = count(row, col)
    labels[row][col]["text"] = str(player_grid[row][col])
    if player_grid[row][col] == EMPTY:
        for offset in offsets:
            new_row = row + offset[0]
            new_col = col + offset[1]
            if 0 <= new_row <= grd-1 and 0 <= new_col <= grd-1:
                if player_grid[new_row][new_col] == UNKNOWN:
                    reveal_neighbors(new_row, new_col)

# Create labels for the grid cells
labels = []
for row in range(grd):
    row_labels = []
    for col in range(grd):
        label = tk.Label(window, text="", width=2, height=1, relief="raised")
        label.grid(row=row, column=col, padx=1, pady=1)
        row_labels.append(label)
    labels.append(row_labels)

# Update the labels with initial values
for row in range(grd):
    for col in range(grd):
        if player_grid[row][col] != UNKNOWN:
            labels[row][col]["text"] = str(player_grid[row][col])

# Click handler function
def on_click(row, col):
    if not game_over:
        click(row, col)

# Check if the player has won
def check_win():
    global game_over
    for row in range(grd):
        for col in range(grd):
            if player_grid[row][col] == UNKNOWN and grid[row][col] != MINE:
                return
    game_over = True
    global label_win
    label_win = tk.Label(window, text="Congratulations! You won XD!")
    label_win.grid(row=grd+1, columnspan=grd)
    global retry_button
    retry_button.grid(row=grd+2, columnspan=grd)

# Function to reset the game
def reset_game():
    global grid, player_grid, game_over, mines_indices, label_gameover, label_win, retry_button
    np.random.seed()  # Reset the random seed
    mines_indices = np.random.choice((grd*grd), mines_count, replace=False)  # Regenerate random mine indices
    grid = np.zeros((grd, grd), dtype=int)
    grid.flat[mines_indices] = MINE
    player_grid = np.full((grd, grd), UNKNOWN)
    game_over = False
    for row in range(grd):
        for col in range(grd):
            labels[row][col]["text"] = ""
            labels[row][col]["state"] = tk.NORMAL
    if label_gameover is not None:
        label_gameover.grid_remove()
        label_gameover = None
    if label_win is not None:
        label_win.grid_remove()
        label_win = None
    if retry_button is not None:
        retry_button.grid_remove()
        retry_button = None

# Add game over flag
game_over = False

# Bind click event to the labels
for row in range(grd):
    for col in range(grd):
        labels[row][col].bind("<Button-1>", lambda event, row=row, col=col: on_click(row, col))

# Create retry button
retry_button = tk.Button(window, text="Retry", command=reset_game)

# Run the main loop
window.mainloop()

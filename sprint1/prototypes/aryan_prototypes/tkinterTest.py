import tkinter as tk

board = [[None]*5 for _ in range(5)]
building_levels = [[0]*5 for _ in range(5)]

root = tk.Tk()

def on_click(i, j, event):
    if building_levels[i][j] < 4:
        building_levels[i][j] += 1
        update_cell(i, j)

def update_cell(i, j):
    level = building_levels[i][j]
    if level == 1:
        color = "lightblue"
    elif level == 2:
        color = "blue"
    elif level == 3:
        color = "darkblue"
    elif level == 4:
        color = "white"  # Dome
    else:
        color = "grey"
    board[i][j].config(bg=color)

for i in range(5):
    for j in range(5):
        L = tk.Label(root, text='    ', bg='grey', relief='raised', borderwidth=2)
        L.grid(row=i, column=j, padx=5, pady=5)
        L.bind('<Button-1>', lambda e, i=i, j=j: on_click(i, j, e))
        board[i][j] = L

root.mainloop()
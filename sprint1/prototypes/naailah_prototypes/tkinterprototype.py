#PROTOTYPE: A simple chessboard with its pieces, currently only white pawns can be moved (in any direction)

import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Chessboard")
root.geometry("600x500")  # Width x Height
root.configure(bg="gray")

size = 50
canvas = tk.Canvas(root, width=8*size, height=8*size)
canvas.place(relx=0.5, rely=0.5, anchor="center") 


for row in range(8):
    for col in range(8):
        color = "white" if (row + col) % 2 == 0 else "grey"
        x0, y0 = col * size, row * size
        x1, y1 = x0 + size, y0 + size
        canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="gray")

#white pieces coordinates
white_king_x = 4 * size + size // 2  # Centering horizontally in the 4th column
white_king_y = 7 * size + size // 2  # Centering vertically in the 8th row
white_queen_x = 3 * size + size // 2
white_queen_y = 7 * size + size // 2
white_bishop_left_x = 2 * size + size // 2
white_bishop_left_y = 7 * size + size // 2
white_bishop_right_x = 5 * size + size // 2
white_bishop_right_y = 7 * size + size // 2
white_knight_left_x = 1 * size + size // 2
white_knight_left_y = 7 * size + size // 2
white_knight_right_x = 6 * size + size // 2
white_knight_right_y = 7 * size + size // 2
white_rook_left_x = 0 * size + size // 2
white_rook_left_y = 7 * size + size // 2
white_rook_right_x = 7 * size + size // 2
white_rook_right_y = 7 * size + size // 2

#creating the pieces
canvas.create_text(white_king_x, white_king_y, text="♔", font=("Arial", 24), fill="black")
canvas.create_text(white_queen_x, white_queen_y, text="♕", font=("Arial", 24), fill="black")
canvas.create_text(white_bishop_left_x, white_bishop_left_y, text="♗", font=("Arial", 24), fill="black")
canvas.create_text(white_bishop_right_x, white_bishop_right_y, text="♗", font=("Arial", 24), fill="black")
canvas.create_text(white_knight_left_x, white_knight_left_y, text="♘", font=("Arial", 24), fill="black")
canvas.create_text(white_knight_right_x, white_knight_right_y, text="♘", font=("Arial", 24), fill="black")
canvas.create_text(white_rook_left_x, white_rook_left_y, text="♖", font=("Arial", 24), fill="black")
canvas.create_text(white_rook_right_x, white_rook_right_y, text="♖", font=("Arial", 24), fill="black")

# Add White Pawns
white_pawn_coords = [] #recording the pawns coordinates so that they can be moved 
pawn_ids = []  # To keep track of pawn IDs for deletion
for col in range(8):
    pawn_x = col * size + size // 2
    pawn_y = 6 * size + size // 2  # Centering vertically in the 7th row
    pawn_id = canvas.create_text(pawn_x, pawn_y, text="♙", font=("Arial", 24), fill="black")
    white_pawn_coords.append((pawn_x, pawn_y))
    pawn_ids.append(pawn_id)

# Function to move the white pawn
selected_pawn = None

def on_click(event):
    global selected_pawn

    # Check if a white pawn is selected
    if selected_pawn is None:
        for i, (x, y) in enumerate(white_pawn_coords):
            if abs(event.x - x) < size // 2 and abs(event.y - y) < size // 2:
                selected_pawn = i  # Store the index of the selected pawn
                canvas.create_oval(x - size // 4, y - size // 4, x + size // 4, y + size // 4, outline="yellow", width=3, tags="selected")
                break
    else:
        # Remove the pawn from its old location
        canvas.delete(pawn_ids[selected_pawn])  # Delete the pawn using the stored ID

        # Move the selected pawn to the new position
        x = (event.x // size) * size + size // 2
        y = (event.y // size) * size + size // 2
        white_pawn_coords[selected_pawn] = (x, y)  # Update the position in the list
        pawn_id = canvas.create_text(x, y, text="♙", font=("Arial", 24), fill="black")  # Place pawn
        pawn_ids[selected_pawn] = pawn_id  # Store the new ID

        canvas.delete("selected")  # Remove the selection highlight
        selected_pawn = None  # Deselect pawn

# Bind mouse click to the canvas
canvas.bind("<Button-1>", on_click)

# Black pieces coordinates (mirrored across the board)
black_king_x = 4 * size + size // 2  # Same horizontal position as white king
black_king_y = 0 * size + size // 2  # Placed at the top (row 0)
black_queen_x = 3 * size + size // 2
black_queen_y = 0 * size + size // 2
black_bishop_left_x = 2 * size + size // 2
black_bishop_left_y = 0 * size + size // 2
black_bishop_right_x = 5 * size + size // 2
black_bishop_right_y = 0 * size + size // 2
black_knight_left_x = 1 * size + size // 2
black_knight_left_y = 0 * size + size // 2
black_knight_right_x = 6 * size + size // 2
black_knight_right_y = 0 * size + size // 2
black_rook_left_x = 0 * size + size // 2
black_rook_left_y = 0 * size + size // 2
black_rook_right_x = 7 * size + size // 2
black_rook_right_y = 0 * size + size // 2

# Create Black pieces
canvas.create_text(black_king_x, black_king_y, text="♚", font=("Arial", 24), fill="black")
canvas.create_text(black_queen_x, black_queen_y, text="♛", font=("Arial", 24), fill="black")
canvas.create_text(black_bishop_left_x, black_bishop_left_y, text="♝", font=("Arial", 24), fill="black")
canvas.create_text(black_bishop_right_x, black_bishop_right_y, text="♝", font=("Arial", 24), fill="black")
canvas.create_text(black_knight_left_x, black_knight_left_y, text="♞", font=("Arial", 24), fill="black")
canvas.create_text(black_knight_right_x, black_knight_right_y, text="♞", font=("Arial", 24), fill="black")
canvas.create_text(black_rook_left_x, black_rook_left_y, text="♜", font=("Arial", 24), fill="black")
canvas.create_text(black_rook_right_x, black_rook_right_y, text="♜", font=("Arial", 24), fill="black")

# Add Pawns for Black
for col in range(8):
    pawn_x = col * size + size // 2
    pawn_y = 1 * size + size // 2  # Placed at the second row (row 1)
    canvas.create_text(pawn_x, pawn_y, text="♟", font=("Arial", 24), fill="black")


# Run the app
root.mainloop()
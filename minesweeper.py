import tkinter as tk
from tkinter import messagebox
import random

class Minesweeper:
    def __init__(self, master):
        self.master = master
        self.master.title("Minesweeper")
        self.master.resizable(False, False)

        # Game Settings
        self.ROWS = 10
        self.COLS = 10
        self.MINES = 15

        # Colors for numbers
        self.colors = {
            1: "blue", 2: "green", 3: "red", 4: "purple",
            5: "maroon", 6: "turquoise", 7: "black", 8: "gray"
        }

        # Game State
        self.game_over = False
        self.buttons = {}  # Dictionary to store button widgets: (r, c) -> Button
        self.mines = set() # Set to store mine locations: (r, c)
        self.revealed = 0  # Count of revealed tiles
        self.flags = set() # Set to store flagged locations
        self.first_click = True

        # Initialize GUI
        self.create_widgets()
        self.update_status()

    def create_widgets(self):
        # Top Frame for Status
        self.top_frame = tk.Frame(self.master)
        self.top_frame.pack(fill=tk.X)

        self.lbl_status = tk.Label(self.top_frame, text="Mines: " + str(self.MINES), font=("Arial", 12, "bold"))
        self.lbl_status.pack(side=tk.LEFT, padx=10, pady=5)

        self.btn_restart = tk.Button(self.top_frame, text="Restart", command=self.restart_game)
        self.btn_restart.pack(side=tk.RIGHT, padx=10, pady=5)

        # Grid Frame
        self.grid_frame = tk.Frame(self.master)
        self.grid_frame.pack()

        for r in range(self.ROWS):
            for c in range(self.COLS):
                btn = tk.Button(
                    self.grid_frame,
                    width=3,
                    height=1,
                    font=("Arial", 10, "bold"),
                    bg="#dddddd",
                    relief=tk.RAISED
                )
                # Bind left click (reveal) and right click (flag)
                btn.bind('<Button-1>', lambda event, row=r, col=c: self.on_left_click(row, col))
                btn.bind('<Button-3>', lambda event, row=r, col=c: self.on_right_click(row, col))
                
                # Mac users might need Button-2 for right click, uncomment below if needed:
                # btn.bind('<Button-2>', lambda event, row=r, col=c: self.on_right_click(row, col))
                
                btn.grid(row=r, column=c)
                self.buttons[(r, c)] = btn

    def restart_game(self):
        self.game_over = False
        self.mines.clear()
        self.revealed = 0
        self.flags.clear()
        self.first_click = True
        self.lbl_status.config(text="Mines: " + str(self.MINES))

        for r in range(self.ROWS):
            for c in range(self.COLS):
                btn = self.buttons[(r, c)]
                btn.config(text="", bg="#dddddd", state=tk.NORMAL, relief=tk.RAISED)

    def place_mines(self, safe_r, safe_c):
        # Place mines randomly, avoiding the first clicked tile (safe_r, safe_c)
        available_positions = [(r, c) for r in range(self.ROWS) for c in range(self.COLS) if (r, c) != (safe_r, safe_c)]
        self.mines = set(random.sample(available_positions, self.MINES))

    def on_left_click(self, r, c):
        if self.game_over or (r, c) in self.flags:
            return

        if self.first_click:
            self.place_mines(r, c)
            self.first_click = False

        if (r, c) in self.mines:
            self.game_over = True
            self.show_mines()
            self.buttons[(r, c)].config(bg="red")
            messagebox.showinfo("Game Over", "BOOM! You hit a mine.")
            return

        self.reveal_tile(r, c)
        self.check_win()

    def on_right_click(self, r, c):
        if self.game_over or self.buttons[(r, c)]['state'] == 'disabled':
            return

        btn = self.buttons[(r, c)]
        if (r, c) in self.flags:
            self.flags.remove((r, c))
            btn.config(text="")
        else:
            self.flags.add((r, c))
            btn.config(text="🚩", fg="red")
        
        self.update_status()

    def reveal_tile(self, r, c):
        if (r, c) not in self.buttons or self.buttons[(r, c)]['state'] == 'disabled':
            return

        btn = self.buttons[(r, c)]
        
        # Count adjacent mines
        count = self.count_adjacent_mines(r, c)
        
        btn.config(relief=tk.SUNKEN, bg="#eeeeee", state=tk.DISABLED)
        self.revealed += 1

        if count > 0:
            btn.config(text=str(count), disabledforeground=self.colors[count])
        else:
            # If 0, recursively reveal neighbors (flood fill)
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0: continue
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.ROWS and 0 <= nc < self.COLS:
                        self.reveal_tile(nr, nc)

    def count_adjacent_mines(self, r, c):
        count = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0: continue
                nr, nc = r + dr, c + dc
                if (nr, nc) in self.mines:
                    count += 1
        return count

    def show_mines(self):
        for r, c in self.mines:
            self.buttons[(r, c)].config(text="💣", bg="#ffcccc")

    def check_win(self):
        if self.revealed == (self.ROWS * self.COLS) - self.MINES:
            self.game_over = True
            messagebox.showinfo("Minesweeper", "Congratulations! You won!")

    def update_status(self):
        self.lbl_status.config(text=f"Mines: {self.MINES - len(self.flags)}")

if __name__ == "__main__":
    root = tk.Tk()
    game = Minesweeper(root)
    root.mainloop()
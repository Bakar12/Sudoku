import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import json
import os


class SudokuGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Sudoku Game")
        self.difficulty = None
        self.puzzle = None
        self.notes_mode = False
        self.board = [[0] * 9 for _ in range(9)]
        self.cells = [[None] * 9 for _ in range(9)]
        self.history = []
        self.create_widgets()
        self.solution = [[0] * 9 for _ in range(9)]
        self.generate_solution()

    def create_widgets(self):
        # Create main menu frame
        self.main_menu = tk.Frame(self.master)
        self.main_menu.pack()
        tk.Label(self.main_menu, text="Sudoku Game", font=("Arial", 24)).pack(pady=20)
        tk.Button(self.main_menu, text="New Game", command=self.start_new_game).pack(pady=5)
        tk.Button(self.main_menu, text="Continue", command=self.continue_game).pack(pady=5)
        tk.Button(self.main_menu, text="Settings", command=self.open_settings).pack(pady=5)
        tk.Button(self.main_menu, text="Leaderboard", command=self.show_leaderboard).pack(pady=5)
        tk.Button(self.main_menu, text="Help", command=self.show_help).pack(pady=5)
        tk.Button(self.main_menu, text="Exit", command=self.exit_game).pack(pady=5)

        # Create game board frame
        self.game_board = tk.Frame(self.master)
        for i in range(9):
            for j in range(9):
                self.cells[i][j] = tk.Entry(self.game_board, width=2, font=("Arial", 18), justify="center")
                self.cells[i][j].grid(row=i, column=j, padx=5, pady=5)
                self.cells[i][j].bind("<KeyRelease>", self.validate_input)

        # Create controls frame
        self.controls = tk.Frame(self.master)
        tk.Button(self.controls, text="Hint", command=self.request_hint).pack(side="left", padx=5)
        tk.Button(self.controls, text="Undo", command=self.undo_move).pack(side="left", padx=5)
        tk.Button(self.controls, text="Notes", command=self.toggle_note_mode).pack(side="left", padx=5)
        tk.Button(self.controls, text="Check Progress", command=self.check_progress).pack(side="left", padx=5)
        tk.Button(self.controls, text="Save", command=self.save_game).pack(side="left", padx=5)

    def start_new_game(self):
        self.difficulty = simpledialog.askstring("Difficulty", "Choose difficulty: Easy, Medium, Hard, Expert")
        self.generate_puzzle(self.difficulty)
        self.show_game_board()

    def continue_game(self):
        self.load_saved_game()
        self.show_game_board()

    def open_settings(self):
        messagebox.showinfo("Settings", "Settings menu not implemented yet.")

    def show_leaderboard(self):
        messagebox.showinfo("Leaderboard", "Leaderboard not implemented yet.")

    def show_help(self):
        messagebox.showinfo("Help", "Help menu not implemented yet.")

    def exit_game(self):
        self.master.quit()

    def show_game_board(self):
        self.main_menu.pack_forget()
        self.game_board.pack(pady=20)
        self.controls.pack(pady=10)
        self.update_board()

    def generate_puzzle(self, difficulty):
        self.board = [[self.solution[i][j] for j in range(9)] for i in range(9)]
        cells_to_clear = {
            "Easy": 20,
            "Medium": 40,
            "Hard": 50,
            "Expert": 60
        }.get(difficulty, 40)
        for _ in range(cells_to_clear):
            i = random.randint(0, 8)
            j = random.randint(0, 8)
            self.board[i][j] = 0

    def load_saved_game(self):
        if os.path.exists("saved_game.json"):
            with open("saved_game.json", "r") as file:
                data = json.load(file)
                self.board = data["board"]
                self.notes_mode = data["notes_mode"]

    def save_game(self):
        data = {
            "board": self.board,
            "notes_mode": self.notes_mode
        }
        with open("saved_game.json", "w") as file:
            json.dump(data, file)
        messagebox.showinfo("Save", "Game saved successfully.")

    def update_board(self):
        for i in range(9):
            for j in range(9):
                self.cells[i][j].delete(0, tk.END)
                if self.board[i][j] != 0:
                    self.cells[i][j].insert(0, str(self.board[i][j]))

    def request_hint(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    self.board[i][j] = self.solution[i][j]
                    self.update_board()
                    return

    def undo_move(self):
        if self.history:
            i, j, value = self.history.pop()
            self.board[i][j] = value
            self.update_board()
        else:
            messagebox.showinfo("Undo", "No moves to undo.")

    def toggle_note_mode(self):
        self.notes_mode = not self.notes_mode
        messagebox.showinfo("Notes", f"Notes mode {'enabled' if self.notes_mode else 'disabled'}.")

    def check_progress(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != 0 and self.board[i][j] != self.solution[i][j]:
                    messagebox.showinfo("Progress", "There are errors in your solution.")
                    return
        messagebox.showinfo("Progress", "No errors found.")

    def validate_input(self, event):
        row, col = None, None
        for i in range(9):
            for j in range(9):
                if self.cells[i][j] == event.widget:
                    row, col = i, j
                    break
        value = self.cells[row][col].get()
        if value.isdigit() and 1 <= int(value) <= 9:
            self.history.append((row, col, self.board[row][col]))
            self.board[row][col] = int(value)
            self.check_completion()
        else:
            self.cells[row][col].delete(0, tk.END)

    def check_completion(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return
        if self.board == self.solution:
            messagebox.showinfo("Congratulations", "You have completed the puzzle!")
        else:
            messagebox.showinfo("Incomplete", "The puzzle is not yet complete or contains errors.")

    def generate_solution(self):
        def is_valid(board, row, col, num):
            for i in range(9):
                if board[row][i] == num or board[i][col] == num:
                    return False
            start_row, start_col = 3 * (row // 3), 3 * (col // 3)
            for i in range(start_row, start_row + 3):
                for j in range(start_col, start_col + 3):
                    if board[i][j] == num:
                        return False
            return True

        def solve_sudoku(board):
            for i in range(9):
                for j in range(9):
                    if board[i][j] == 0:
                        for num in range(1, 10):
                            if is_valid(board, i, j, num):
                                board[i][j] = num
                                if solve_sudoku(board):
                                    return True
                                board[i][j] = 0
                        return False
            return True

        board = [[0] * 9 for _ in range(9)]
        solve_sudoku(board)
        self.solution = board


if __name__ == "__main__":
    root = tk.Tk()
    game = SudokuGame(root)
    root.mainloop()

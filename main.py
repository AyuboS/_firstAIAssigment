import tkinter as tk
from tkinter import messagebox
from random import randint, choice


class NumStringGameApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("20th Group AI Game")
        self.geometry("800x600")
        self.resizable(False, False)

        self.player_score = 100
        self.computer_score = 100
        self.current_turn = choice(["Player", "Computer"])
        self.num_string = ""

        self.create_widgets()

    def create_widgets(self):
        length_frame = tk.Frame(self)
        length_frame.pack(pady=20)

        self.length_label = tk.Label(length_frame, text="String Length (15-25):")
        self.length_label.pack(side=tk.LEFT)

        self.length_entry = tk.Entry(length_frame, width=5)
        self.length_entry.pack(side=tk.LEFT)

        self.start_button = tk.Button(length_frame, text="Start Game", command=self.start_game)
        self.start_button.pack(side=tk.LEFT)

        self.reset_button = tk.Button(length_frame, text="Reset Game", command=self.reset_game, state='disabled')
        self.reset_button.pack(side=tk.LEFT)

        self.game_area_frame = tk.Frame(self)
        self.game_area_frame.pack(pady=10, expand=True)

        self.move_entry = tk.Entry(self.game_area_frame, width=5, state=tk.DISABLED)
        self.move_entry.pack(side=tk.LEFT)

        self.move_button = tk.Button(self.game_area_frame, text="Make Move", command=self.make_move, state=tk.DISABLED)
        self.move_button.pack(side=tk.LEFT)

        self.score_label = tk.Label(self, text="Player Score: 100 | Computer Score: 100")
        self.score_label.pack(pady=(5, 0))
        self.turn_label = tk.Label(self, text="")
        self.turn_label.pack(pady=(5, 10))

    def start_game(self):
        try:
            length = int(self.length_entry.get())
            assert 15 <= length <= 25
        except (ValueError, AssertionError):
            messagebox.showerror("Error", "Invalid length. Please enter a number between 15 and 25.")
            return

        self.num_string = ''.join(str(randint(1, 4)) for _ in range(length))
        self.update_game_area()
        self.reset_button.config(state='normal')

    def update_game_area(self, clear=False):
        if clear:
            self.num_string_label.config(text="")
            self.score_label.config(text="Player Score: 100 | Computer Score: 100")
            self.turn_label.config(text="")
            return

        if hasattr(self, 'num_string_label'):
            self.num_string_label.config(text=self.num_string)
        else:
            self.num_string_label = tk.Label(self, text=self.num_string)
            self.num_string_label.pack(pady=(10, 0))

        self.score_label.config(text=f"Player Score: {self.player_score} | Computer Score: {self.computer_score}")
        self.turn_label.config(text=f"{self.current_turn}'s Turn")

        if self.current_turn == "Player":
            self.move_entry.config(state=tk.NORMAL)
            self.move_button.config(state=tk.NORMAL)
        else:
            self.move_entry.config(state=tk.DISABLED)
            self.move_button.config(state=tk.DISABLED)

    def make_move(self):
        if self.current_turn != "Player":
            messagebox.showinfo("Wait", "It's not your turn yet!")
            return

        move_position = self.move_entry.get()
        if not move_position.isdigit() or int(move_position) < 1 or int(move_position) > len(self.num_string):
            messagebox.showerror("Invalid Move", "Please enter a valid position.")
            return

        move_position = int(move_position) - 1
        removed_number = int(self.num_string[move_position])
        self.num_string = self.num_string[:move_position] + self.num_string[move_position + 1:]

        if removed_number % 2 == 0:
            self.player_score -= removed_number * 2
        else:
            self.computer_score += removed_number

        self.update_game_area()
        self.move_entry.delete(0, tk.END)

        if not self.num_string:
            self.end_game()
            return

        self.current_turn = "Computer"
        self.after(500, self.computer_move)

    def computer_move(self):
        if not self.num_string:
            self.end_game()
            return

        # Select strategy based on a condition or user input. For now, it's random selection for illustration.
        strategy = choice(['first', 'random'])
        if strategy == 'first':
            best_move = 0  # Always picks the first number
        elif strategy == 'random':
            best_move = randint(0, len(self.num_string) - 1)  # Picks a random number

        # Apply the move
        removed_number = int(self.num_string[best_move])
        self.num_string = self.num_string[:best_move] + self.num_string[best_move + 1:]

        if removed_number % 2 == 0:
            self.computer_score -= removed_number * 2
        else:
            self.player_score += removed_number

        self.update_game_area()

        if not self.num_string:
            self.end_game()
            return

        self.current_turn = "Player"
        self.move_entry.config(state=tk.NORMAL)  # Re-enable the move entry for the player
        self.move_button.config(state=tk.NORMAL)

    def end_game(self):
        # Determine the winner based on the scores
        if self.player_score < self.computer_score:
            result_text = "Player wins!"
        elif self.computer_score < self.player_score:
            result_text = "Computer wins!"
        else:
            result_text = "It's a draw!"

        # Show the game over message
        messagebox.showinfo("Game Over",
                            f"{result_text}\nFinal Scores:\nPlayer: {self.player_score}\nComputer: {self.computer_score}")

        # Enable the reset button after the game ends
        self.reset_button.config(state='normal')

    def reset_game(self):
        # Reset the game to its initial state
        self.player_score = 100
        self.computer_score = 100
        self.current_turn = choice(["Player", "Computer"])
        self.num_string = ""

        # Clear UI elements
        self.length_entry.config(state=tk.NORMAL)
        self.length_entry.delete(0, tk.END)
        self.start_button.config(state=tk.NORMAL)
        self.move_entry.delete(0, tk.END)
        self.move_entry.config(state=tk.DISABLED)
        self.move_button.config(state=tk.DISABLED)
        self.reset_button.config(state='disabled')  # Disable the reset button until the game starts again

        # Clear the game area
        if hasattr(self, 'num_string_label'):
            self.num_string_label.config(text="")
        self.score_label.config(text="Player Score: 100 | Computer Score: 100")
        self.turn_label.config(text="")


if __name__ == "__main__":
    app = NumStringGameApp()
    app.mainloop()

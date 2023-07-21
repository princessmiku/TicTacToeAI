import json
import os
import random
import sys
import time
import tkinter as tk
import webbrowser
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap import SUCCESS, WARNING, DANGER

# self-written for showing the icon in the taskbar
import ctypes

myappid = 'miku.ai.tictactoe.1.0'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
# self-written end

PLAYER_MARKER = 'X'
AI_MARKER = 'O'
EMPTY_MARKER = ' '
WIN_CONDITIONS = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))

if getattr(sys, 'frozen', False):
    base_dir = sys._MEIPASS
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

logo_png_path = os.path.join(base_dir, 'img', 'logo.png')
logo_ico_path = os.path.join(base_dir, 'img', 'logo.ico')


class TicTacToe:
    """
     A class representing the Tic Tac Toe game.

     Attributes:
     - root: The Tkinter root window
     - data_file: The filename of the JSON file to store game statistics
     - difficulty: The difficulty level of the AI player ('Easy', 'Medium', or 'Hard')
     - board: A list representing the Tic Tac Toe board
     - statistics: A dictionary containing game statistics

     Methods:
     - __init__(self): Initializes the TicTacToe class, creates the game window, and sets up the menu
     - initialize_menu(self): Initializes the menu options for the game
     - show_info(self): Displays information about the game
     - reset_statistics(self): Resets the game statistics to default
     - load_data(self): Loads the game statistics from a JSON file
     - save_data(self): Saves the game statistics to a JSON file
    """

    def __init__(self):
        """
        Initializes the TicTacToe game by setting up the GUI, loading game data, and setting default game settings.

        Parameters:
            None

        Returns:
            None
        """
        self.root = tk.Tk()
        self.root.iconbitmap(logo_ico_path)
        self.data_file = "tttdata.json"
        self.difficulty = "Easy"
        self.board = [' ' for _ in range(9)]
        self.statistics = self.load_data()

        self.style = ttk.Style("superhero")
        self.canvas = tk.Canvas(self.root, width=300, height=300)
        self.root.title(f"Tic Tac Toe - {self.difficulty}")

        self.initialize_menu()

        self.canvas.pack()
        self.canvas.bind('<Button-1>', self.click)

        self.draw_board()
        self.center_window()

    def initialize_menu(self):
        """
        Initialize the menu for the TicTacToe game.

        :return: None
        """
        menubar = tk.Menu(self.root)

        game_menu = tk.Menu(menubar, tearoff=0)
        game_menu.add_command(label="Modify Difficulty Level", command=self.show_difficulty_selection)
        game_menu.add_command(label="Reset Game", command=self.reset_game)
        menubar.add_cascade(label="Game", menu=game_menu)

        stats_menu = tk.Menu(menubar, tearoff=0)
        stats_menu.add_command(label="See Statistics", command=self.show_statistics)
        stats_menu.add_command(label="Reset Statistics", command=self.reset_statistics)
        menubar.add_cascade(label="Statistics", menu=stats_menu)

        info_menu = tk.Menu(menubar, tearoff=0)
        info_menu.add_command(label="About", command=self.show_info)
        menubar.add_cascade(label="Info", menu=info_menu)

        self.root.config(menu=menubar)

    def show_info(self):
        """
        Opens a window displaying information about the Tic Tac Toe game.

        :return: None
        """
        info_window = tk.Toplevel(self.root, bg='white')
        info_window.resizable(False, False)

        root_x = self.root.winfo_rootx()
        root_y = self.root.winfo_rooty()
        root_width = self.root.winfo_width()
        root_height = self.root.winfo_height()

        info_width = 500
        info_height = 250

        pos_x = root_x + root_width // 2 - info_width // 2
        pos_y = root_y + root_height // 2 - info_height // 2

        info_window.geometry(f"{info_width}x{info_height}+{pos_x}+{pos_y}")

        info_window.title("About this project")
        info_window.iconbitmap(logo_ico_path)

        img = tk.PhotoImage(file=logo_png_path)
        img = img.subsample(3)

        panel = tk.Label(info_window, image=img)
        panel.image = img
        panel.grid(row=0, column=0, padx=(20, 20), pady=(50, 20), sticky='nsew')

        message = ("Welcome to the Tic Tac Toe game.\n\nThis game was developed exclusively using JetBrains "
                   "AI.\n\nFind the source code at:")
        text = tk.Label(info_window, text=message, justify='left')
        link = "https://github.com/princessmiku/TicTacToeAI"
        link_label = tk.Label(info_window, text=link, fg="blue", cursor="hand2")
        link_label.bind("<Button-1>", lambda e: webbrowser.open_new(link))
        text.grid(row=0, column=1, sticky='w')
        link_label.grid(row=1, column=1, sticky='w')

    def reset_statistics(self):
        """
        Resets the statistics for the TicTacToe game.

        :return: None
        """
        if messagebox.askyesno('Confirm Reset', 'Are you sure you want to reset the statistics?'):
            self.statistics = {
                "Easy": {"Wins": 0, "Losses": 0, "Draws": 0},
                "Medium": {"Wins": 0, "Losses": 0, "Draws": 0},
                "Hard": {"Wins": 0, "Losses": 0, "Draws": 0}
            }
            self.save_data()

    def load_data(self):
        """
        Loads the game statistics from a JSON file.

        :return: A dictionary containing the game statistics.
        """
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                return data["statistics"]
        except FileNotFoundError:
            return {
                "Easy": {"Wins": 0, "Losses": 0, "Draws": 0},
                "Medium": {"Wins": 0, "Losses": 0, "Draws": 0},
                "Hard": {"Wins": 0, "Losses": 0, "Draws": 0}
            }

    def save_data(self):
        """
        Save the data of TicTacToe game.

        :return: None
        """
        data = {"statistics": self.statistics}
        with open(self.data_file, 'w') as f:
            json.dump(data, f)

    def set_difficulty(self, value):
        """
        :param value: The difficulty level to set for the Tic Tac Toe game.
        :return: None

        This method sets the difficulty level for the Tic Tac Toe game. The difficulty level is used to determine the
        AI's level of play. The value parameter should be one of the following: 'easy', 'medium', or 'hard'.

        Upon setting the difficulty level, the method updates the title of the game window to include the difficulty
        level. It also calls the reset_game() method to reset the game board and prepare for the next game.

        Example usage:
            game = TicTacToe()
            game.set_difficulty('easy')
        """
        self.difficulty = value
        self.root.title(f"Tic Tac Toe - {self.difficulty}")
        self.reset_game()

    def draw_board(self):
        """
        Draws the Tic-Tac-Toe board on the canvas.

        :return: None
        """
        for i in range(3):
            for j in range(3):
                self.canvas.create_rectangle(j * 100, i * 100, j * 100 + 100, i * 100 + 100, outline='black')
                if self.board[i * 3 + j] == 'X':
                    self.canvas.create_text(j * 100 + 50, i * 100 + 50, text=self.board[i * 3 + j], font=('Arial', 50),
                                            fill='blue')
                elif self.board[i * 3 + j] == 'O':
                    self.canvas.create_text(j * 100 + 50, i * 100 + 50, text=self.board[i * 3 + j], font=('Arial', 50),
                                            fill='red')

    def check_for_win(self):
        """
        Checks if there is a winner or a tie in the Tic Tac Toe game.

        :return: Returns the marker of the winner if there is a winner, 'Tie' if the game is tied, or False if there
        is no winner yet.
        """
        for each in WIN_CONDITIONS:
            if self.board[each[0]] == self.board[each[1]] == self.board[each[2]] != EMPTY_MARKER:
                return self.board[each[0]]
        if EMPTY_MARKER not in self.board:
            return 'Tie'
        return False

    def evaluate_game(self):
        """
        Evaluate the current state of the Tic Tac Toe game and determine if there is a winner.

        :return: Returns True if there is a winner and the game should be reset, False otherwise.
        """
        winner = self.check_for_win()
        if winner:
            if winner == PLAYER_MARKER:
                outcome_msg = "Congratulations! You won the game."
                self.statistics[self.difficulty]["Wins"] += 1
            elif winner == AI_MARKER:
                outcome_msg = "You lost the game. Better luck next time!"
                self.statistics[self.difficulty]["Losses"] += 1
            else:
                outcome_msg = "It's a draw!"
                self.statistics[self.difficulty]["Draws"] += 1

            self.save_data()
            messagebox.showinfo("End of Game", outcome_msg)
            self.reset_game()
            return True
        return False

    def click(self, event):
        """
        :param event: The event object that triggered the click event.
        :return: None

        Handles click events on game board. Updates game state considering click position, and executes necessary
        actions - the player's and the AI's moves. Evaluates the game after each move.

        The 'event' object includes information on mouse click position. The system calculates both the index of the
        game board cell corresponding to the clicked position, along with its row and column.

        If the clicked cell is empty, it sets the cell's value to 'X' and redraws the board. If game is ongoing,
        'ai_move' method is called after half a second delay to have AI move next. The board is updated and redrawn
        accordingly.

        The game is further evaluated after each move. If it finds the game over, it retreats back.

        Example usage:
        ```python
        game = TicTacToe()
        game.click(event)
        ```
        """
        x = event.x // 100
        y = event.y // 100
        i = y * 3 + x
        if self.board[i] == ' ':
            self.board[i] = 'X'
            self.draw_board()
            if self.evaluate_game():
                return
            self.canvas.update()
            time.sleep(0.5)
            self.ai_move('O')
            self.draw_board()
            if self.evaluate_game():
                return

    def reset_game(self):
        """
        Resets the Tic Tac Toe game.

        This method resets the game by clearing the game board and redrawing the empty game board.

        :return: None
        """
        self.board = [' ' for _ in range(9)]
        self.canvas.delete('all')
        self.draw_board()

    def ai_move_easy(self, ch):
        """
        Makes a random move for the AI player in an easy difficulty level.

        :param ch: The character representing the AI player's move.
        :return: This method returns nothing.
        """
        while True:
            i = random.randint(0, 8)
            if self.board[i] == ' ':
                self.board[i] = ch
                return

    def ai_move_medium(self, ch):
        """
        Represents the medium level AI move in the Tic Tac Toe game.

        :param ch: The player symbol ('X' or 'O') for which the AI will make a move.
        :type ch: str
        :return: None

        This method represents the medium level AI move in the Tic Tac Toe game. It takes a parameter 'ch' which
        represents the player symbol ('X' or 'O') for which the AI will make a move. The method tries to win the game
        for the given player by checking if making a move will result in a win for the player. If a winning move is
        found, the method returns. If there is no winning move, the method randomly selects an empty cell on the
        board and marks it with the player symbol.

        Example usage:
        ```
        game = TicTacToe()
        game.ai_move_medium('X')
        ```
        """
        for i in range(9):
            if self.board[i] == ' ':
                self.board[i] = ch
                if self.check_for_win() == 'O':
                    return
                self.board[i] = ' '

        for i in range(9):
            if self.board[i] == ' ':
                self.board[i] = 'X'
                if self.check_for_win() == 'X':
                    self.board[i] = 'O'
                    return
                self.board[i] = ' '

        while True:
            i = random.randint(0, 8)
            if self.board[i] == ' ':
                self.board[i] = ch
                return

    def ai_move_hard(self, ch):
        """
            Make a move for the AI player in hard mode.

            This method uses the minimax algorithm to determine the best move to make.

            :param ch: The character representing the current player's piece ('X' or 'O')
            :return: None
        """
        bestScore = float('-inf')
        move = 0
        for i in range(len(self.board)):
            if self.board[i] == ' ':
                self.board[i] = ch
                score = self.minimax(self.board, 0, False)
                self.board[i] = ' '
                if score > bestScore:
                    bestScore = score
                    move = i
        self.board[move] = ch

    def ai_move(self, ch):
        """
        :param ch: The character representing the player ('X' or 'O')
        :return: None

        This method determines the AI's move based on the difficulty level selected.
        If the difficulty is set to 'Easy', the AI makes a random move.
        If the difficulty is set to 'Medium', the AI uses a medium-level algorithm to determine its move.
        If the difficulty is set to 'Hard', the AI uses a hard-level algorithm to determine its move.
        """
        if self.difficulty == 'Easy':
            self.ai_move_easy(ch)
        elif self.difficulty == 'Medium':
            self.ai_move_medium(ch)
        elif self.difficulty == 'Hard':
            self.ai_move_hard(ch)

    def minimax(self, board, depth, isMaximizing):
        """
        Returns the optimal score for the current state of the tic-tac-toe board using the minimax algorithm.

        :param board: The current state of the tic-tac-toe board represented as a list.
        :param depth: The current depth of the minimax algorithm.
        :param isMaximizing: A boolean flag indicating whether it is the maximizing player's turn or not.
        :return: The optimal score for the current board state.
        """
        winner = self.check_for_win()
        if winner == 'O':
            return 1
        elif winner == 'X':
            return -1
        elif winner == 'Tie':
            return 0

        if isMaximizing:
            best_score = float('-inf')
            for i in range(len(board)):
                if board[i] == ' ':
                    board[i] = 'O'
                    score = self.minimax(board, depth + 1, False)
                    board[i] = ' '
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(len(board)):
                if board[i] == ' ':
                    board[i] = 'X'
                    score = self.minimax(board, depth + 1, True)
                    board[i] = ' '
                    best_score = min(score, best_score)
            return best_score

    def show_difficulty_selection(self):
        """
        Shows a difficulty selection window and updates the difficulty value based on user selection.

        :return: None
        """
        def update_difficulty(value):
            self.set_difficulty(value)
            difficulty_window.destroy()

        difficulty_window = ttk.Toplevel(self.root)
        difficulty_window.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))

        difficulty_window.title('Select Difficulty')
        difficulty_window.iconbitmap(logo_ico_path)

        difficulty_window.update_idletasks()

        width = 300
        height = 300
        x = (difficulty_window.winfo_screenwidth() // 2) - (width // 2)
        y = (difficulty_window.winfo_screenheight() // 2) - (height // 2)
        difficulty_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

        button_frame = ttk.Frame(difficulty_window)
        button_frame.place(relx=0.5, rely=0.5, anchor='center')

        ttk.Button(button_frame, text="Easy", bootstyle=SUCCESS,
                   command=lambda: update_difficulty("Easy")).pack(pady=10)
        ttk.Button(button_frame, text="Medium", bootstyle=WARNING,
                   command=lambda: update_difficulty("Medium")).pack(pady=10)
        ttk.Button(button_frame, text="Hard", bootstyle=DANGER,
                   command=lambda: update_difficulty("Hard")).pack(pady=10)

        difficulty_window.grab_set()
        difficulty_window.wait_window()

    def show_statistics(self):
        """
        Display the statistics of the game.

        :return: None
        """
        difficulties = list(self.statistics.keys())
        width = len(difficulties) * 150
        height = 200

        root_x = self.root.winfo_rootx()
        root_y = self.root.winfo_rooty()
        root_width = self.root.winfo_width()
        root_height = self.root.winfo_height()

        pos_x = root_x + root_width // 2 - width // 2
        pos_y = root_y + root_height // 2 - height // 2

        stats_window = tk.Toplevel(self.root, bg='white')
        stats_window.iconbitmap(logo_ico_path)
        stats_window.geometry(f"{width}x{height}+{pos_x}+{pos_y}")
        stats_window.grab_set()

        stats_window.pack_propagate(False)

        frame = tk.Frame(stats_window, bg='white')
        frame.pack(fill='both', expand=True)

        title = tk.Label(frame, text="Statistiken", font=('Helvetica', 20, 'bold'), bg='white')
        title.pack()

        for column, difficulty in enumerate(difficulties):
            stats_frame = tk.Frame(frame, bg='white')
            stats_frame.pack(side='left', expand=True, fill='both')

            stats = self.statistics[difficulty]
            difficulty_label = tk.Label(stats_frame, text=f"{difficulty}", font=('Helvetica', 16, 'bold'), bg='white')
            difficulty_label.pack()

            wins_label = tk.Label(stats_frame, text="Wins: " + str(stats["Wins"]), font=('Helvetica', 14), bg='white')
            wins_label.pack()

            losses_label = tk.Label(stats_frame, text="Losses: " + str(stats["Losses"]), font=('Helvetica', 14),
                                    bg='white')
            losses_label.pack()

            draws_label = tk.Label(stats_frame, text="Draws: " + str(stats["Draws"]), font=('Helvetica', 14),
                                   bg='white')
            draws_label.pack()

    def center_window(self):
        """
        Centers the Tkinter window on the screen.

        This method calculates the x and y coordinates needed to center the Tkinter window on the screen. It uses the
        `winfo_screenwidth()` and `winfo_screenheight()` methods of the `Tk` object to get the screen width and
        height, and then calculates the x and y coordinates by subtracting half of the window width and height
        respectively.

        :return: None
        """
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def start_game(self):
        """
        Starts the Tic Tac Toe game.

        :return: None
        """
        self.show_difficulty_selection()
        self.root.mainloop()


if __name__ == "__main__":
    game = TicTacToe()
    game.start_game()

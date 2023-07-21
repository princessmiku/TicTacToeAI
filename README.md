# Tic Tac Toe AI

This is a Tic Tac Toe game where you play against an artificial intelligence (AI). The AI has been meticulously created
to provide you with three levels of difficulty: Easy, Medium or Hard. The AI which powers this game was developed by
JetBrains AI Assistant.

<img src="https://github.com/princessmiku/TicTacToeAI/blob/master/img/game.png" alt="drawing" height="250"/>

## Dependencies

This project makes use of the following Python libraries:

1. `tkinter`: Required for creating the Graphic User Interface (GUI).
2. `ttkbootstrap`: For enhancing the visual elements of the GUI.
3. `json`: Used for storing and retrieving game statistics.
4. `ctypes`: Allows the display of a custom game icon on Windows taskbar.
5. `random` and `time`: These are utilized for computer moves (Easy level only).

Ensure that you have Python 3.11.1 installed, along with the mentioned libraries. Most of them come prepackaged with
Python. Other necessary libraries can be installed using the `pip install <package-name>` command.

## Features

- **Different AI Levels**: Three difficulty levels - Easy, Medium, and Hard.
- **Persistent Statistics**: The game keeps track of your wins, losses, and draws for each difficulty level. The stats
  persist across sessions, thanks to json data storage.
- **Modern Interface**: The GUI of the game is powered by tkinter and ttkbootstrap, thereby providing a modern and
  minimalistic visual experience.

## Running the Game

To run the game, make sure all dependencies are properly installed. Additionally, for the game icon to be displayed
correctly, have the `logo.ico` file in the same directory as the Python script. In the absence of the icon file, the
game will continue to operate, albeit without displaying an icon.

Navigate to the project directory in your terminal, and run the game using:

```bash
python tictactoe.py
```

Replace `tictactoe.py` with the name you have used for the game script.

## Credits

This game was 99% developed by the JetBrains AI Assistant. The only user input involved minor modifications like
adapting file paths to make the game locally operational.

If you encounter any issues, feel free to open an issue.

The game is open-source and free to use. You can view the complete source code
on [GitHub](https://github.com/princessmiku/TicTacToeAI).

```python
# The AI assistant was responsible for 99% of the code
# Only minor user adjustments were necessary to make the game operational on the local system
```

## License

The game is licensed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html). This
license allows the game to remain open-source and free for use, but disallows its use for commercial purposes.

## Graphics Creation and Implementation

The project's graphical resources, including logo and other related images, were created with guidance and input from
the JetBrains AI Assistant. The AI Assistant also contributed to the code for the logos in the `logo.py` script. The
collaborative efforts of the AI Assistant have played a pivotal role in the design and aesthetic presentation of this
game.

## Preparation of Documentation

The entirety of this README documentation was generated with valuable assistance of the JetBrains AI Assistant. This
includes all sections from introduction to the final remarks of the document, contributing significantly to the
thorough, comprehensive description and effective presentation of the project.
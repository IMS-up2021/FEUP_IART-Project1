# DROP OF LIGHT

## Description

The game "Drop of Light" involves arranging and combining photons and pigments to create specific color patterns. The player's objective is to match the specified color pattern by strategically arranging and combining photons on a web, as it is shown in the corner of the game screen.

## Setup

The application was designed to run using Python versions ranging from 3.8 to 3.10, with Python 3.10.10 being the version used during testing. Pygame was utilized for displaying the application. You can install it manually with the following command:

``` bash
pip install pygame
```

## Usage

To execute the application, either open and run the "menu.py" file located within the "src" folder using your preferred IDE, or execute the following command in your terminal:

``` bash
python src/menu.py
```

## Files

The application is organized into multiple files for improved readability and maintainability.

### drop.py

1. **LEVELS:** A dictionary containing different levels of the game, each defined by the initial state of the game board, selected pieces, the number of remaining moves, and the goal state.

2. **piece:** A dictionary containing information about different types of pieces on the game board. Each piece has attributes such as color, whether it can be moved, how it interacts with other pieces, and its associated cost.

3. **nodes:** A dictionary representing the nodes of the game board graph. Each node has connections to neighboring nodes and their positions.

4. Functions:
    - **check_can_piece_split:** Checks if a piece can be split into smaller pieces.
    - **check_empty:** Checks if a position on the board is empty.
    - **check_can_merge:** Checks if two pieces can be merged.
    - **check_can_move:** Checks if a piece can be moved to a certain position.
    - **check_win:** Checks if the current game state matches the goal state.
    - **split:** Splits a piece into smaller pieces.
    - **move:** Moves a piece to a specified position.
    - **photon_in_place:** Checks if a photon is in a specified place.
    - **filter_photon:** Filters available actions for a photon.
    - **dist:** Calculates the Euclidean distance between two nodes.
    - **dist_to_goal:** Calculates the distances from each node to the goal node.

### menu.py

1. **Initialization:** Pygame is initialized, and the screen dimensions are set.

2. **Constants:** Lists of coordinates (coords and coords_goal) are defined for drawing the game board and the goal area.

3. **Classes:**
    - **Button:** Represents clickable buttons on the game menu and level select screens.
    - **Piece:** Represents game pieces (photons) on the game board.

4. **Functions:**
    - **initialize_screen():** Initializes the Pygame screen.
    - **get_font():** Returns a Pygame font object.
    - **display_text():** Displays text on the screen.
    - **create_button():** Creates a Button object.
    - **create_piece():** Creates a Piece object.
    - **dist_points():** Computes the distance between two points.
    - **make_board():** Initializes the game board.
    - **make_goal():** Initializes the goal state.
    - **draw_board():** Draws the game board on the screen.
    - **draw_goal():** Draws the goal state on the screen.
    - **in_piece():** Checks if the mouse click is on a game piece.
    - **main_menu():** Displays the main menu.
    - **choose_level():** Displays the level select screen.
    - **algo_choose():** Displays the algorithm select screen.
    - **play_loop():** Main loop for playing a level.
    - **state_screen():** Displays the game state (win/lose) screen.
    - **play():** Main gameplay loop.
    - **algo_play():** Main gameplay loop for algorithm-assisted play.
    - **options():** Displays the instructions screen.

5. **Main Execution:**
    - The **main_menu()** function is called to start the game.

### search_alg.py

1. **DFS Algorithm** (dfs() function):
    - This function performs Depth-First Search recursively to find a solution to the game.
    - It iterates over all possible moves on the game board and recursively calls itself with the new state after each move.
    - The search is limited by a depth limit parameter to avoid infinite recursion.
    - If a solution is found (winning state reached), it returns the sequence of moves required to reach that state.

2. **Game Solver Function** (solve_game() function):
    - This function serves as the interface to call the DFS algorithm.
    - It takes the initial state, goal state, and maximum depth as input parameters.
    - It calls the dfs() function with the specified parameters and returns the result.

3. **Informed Search Initialization** (init_informed() function):
    - This function initializes the informed search algorithms (greedy and A*).
    - It determines the heuristic values for each game piece based on their distance to the goal positions.
    - If the algorithm flag is set to True, it calls the greedy search function, otherwise, it calls the A* search function.
    - It returns a dictionary containing the moves for each game piece.

4. **Greedy Search Algorithm** (greedy() function):
    - This function implements the greedy search algorithm.
    - It selects the next move by choosing the position with the minimum distance to the goal.
    - It recursively calls itself until reaching the goal position.
    - It returns the sequence of moves required to reach the goal.
  

This project was made by:

| Student                 | number      | email                     |
|-------------------------|-------------|---------------------------|
| André Dantas Rogrigues  | 202108721   | up202108721@edu.fe.up.pt  |
| Inês Martin Soares      | 202108852   | up202108852@edu.fe.up.pt  |

5. **A Search Algorithm\*** (a_star() function):
    - This function implements the A* search algorithm.
    - It maintains a priority queue of nodes to explore, prioritized based on the sum of the distance traveled and the heuristic value.
    - It explores nodes until reaching the goal position.
    - It returns the sequence of moves required to reach the goal.

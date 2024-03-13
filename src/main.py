import menu
from levels import LEVELS



if __name__ == "__main__":
    for level in LEVELS:
        # Create the game for the current level
        game = draw.Game(level)
        
        # Run the game
        if game.run():
            break
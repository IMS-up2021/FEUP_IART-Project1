from levels import levels

if __name__ == "main":
    for level in levels:
        # Create the game for the current level
        game = draw.Game(level)
        
        # Run the game
        if game.run():
            break
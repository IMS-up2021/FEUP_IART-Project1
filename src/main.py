from levels import levels

if name == "main":
    for level in LEVELS:
        # Create the game for the current level
        game = draw.Game(level)
        
        # Run the game
        if game.run():
            break
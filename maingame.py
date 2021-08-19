from Classes import classes
import time

# Function that allows for creation of players, including player number and player names
def createPlayers(no_of_players, board = classes.Board()):
    all_players = []
    for i in range(no_of_players):
        print(f'\nPlayer {i+1}\n--------')
        player_name = input('Name: ')
        player_class = classes.Player(name = player_name, player_no = i + 1, tile = board.root)
        all_players.append(player_class)
    return all_players

# Creates a board based on tile_list from classes
def createBoard(board = classes.Board()):
    tile_list = board.createBoard_List()
    for tile in tile_list:
        board.add(tile)
    return board

# If only one player is left in the all_players list, return True (Used to end the game)
def checkWinner(all_players):
    if len(all_players) == 1:
        return True
    else:
        return False

print('MONOPOLY SIMULATION v1.0\n------------------------')
# Get number of players
try:
    no_of_players = int(input('No. of Players: '))
except ValueError:
    print('You did not enter a number!')
except Exception:
    print('Something went wrong, please re-run the program!')
else:
    board = createBoard()
    all_players = createPlayers(no_of_players, board)

    # Turn-based component of the game until the last player standing
    while True:
        for player in all_players:
            print(f'\n{player.name}\'s Turn!')
            print('---------')

            # Player who's having their turn rolls dice
            dice = player.roll_dice()

            # Move across the board according to dice, checking their tile positions for special effects
            board.Move(player, dice)

            # Checks if player has passed Go
            board.Go(player)

            # Checks if player needs to pay rent
            board.rent_pay(player)

            # Checks if player is eligible to buy current tile
            board.buy(player)
            print(f'--------------------------------\n{player.name} has ${player.money}! ')
            time.sleep(0.5)
            # Checks if player has been bankrupt and remove player from all_players list
            if player.WinOrLose() == True:
                # Removes all tile ownership
                board.remove_Owner(player)
                all_players.remove(player)
        # Check if there's only one player left and if so, end the game
        if checkWinner(all_players) == True:
            break

finally:
    time.sleep(0.5)
    print(all_players[0].name +' won!')
    exit = input('Press ENTER to exit the game...')

















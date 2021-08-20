from Classes import classes
import time

# If only one player is left in the all_players list, return True (Used to end the game)
def checkWinner(all_players):
    if len(all_players) == 1:
        return True
    else:
        return False

print('MONOPOLY SIMULATION v1.0\n------------------------')
# Get number of players, looping until an integer has been input
while True:
    try:
        no_of_players = int(input('No. of Players: '))
        break
    except ValueError:
        print('You did not enter a number!')


board = classes.Board()
board.createBoard()
all_players = board.createPlayers(no_of_players)

# Turn-based component of the game until the last player standing
while not checkWinner(all_players):
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
        if player.HasLost():
            # Removes all tile ownership
            board.remove_Owner(player)
            all_players.remove(player)
# Check if there's only one player left and if so, end the game
time.sleep(0.5)
print(all_players[0].name, 'won!')
exit = input('Press ENTER to exit the game...')

















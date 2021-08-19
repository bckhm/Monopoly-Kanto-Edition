import random
import re
import time

# Tile class containing data of each tile on the gameboard
class Tile:
    def __init__(self, name = None, position = None, cost = 0, owner = None, next = None):
        self.name = name
        self.position = position
        self.cost = cost
        self.rent = cost // 10
        self.owner = owner
        self.next = next

    # Function that prints out details of a specific tile
    def show_Details(self, special_tiles = [3, 5, 8, 11, 18, 21, 23, 31, 34, 37, 39]):
        # Check if tile is a special tile(unbuyable e.g. Jail)
        if self.position in special_tiles:
            return False
        else:
            if self.owner != None:
                print(f'{self.name}\nTile Number: {self.position}\nCost: ${self.cost}\nRent: ${self.rent}\nOwned by: {self.owner.name}')
            else:
                print(
                    f'{self.name}\nTile Number: {self.position}\nCost: ${self.cost}\nRent: ${self.rent}\nOwned by: {self.owner}')

    def __str__(self):
        return str(f'({self.name})')

# Player class
class Player:
    def __init__(self, name, player_no, money = 1500, tile = Tile(), status = None):
        self.name = name
        self.player_no = player_no
        self.money = money
        self.tile = tile
        self.status = status
        self.steps = 0

    # Function that gives a random output between 1-6, acting as a dice
    def roll_dice(self):
        confirm = input('Press ENTER to roll the dice')
        time.sleep(0.5)
        dice_no = random.choice([1, 2, 3, 4, 5, 6])
        print(f'{self.name} rolled {dice_no}!\n--------------------------------')
        return dice_no

    # Function that checks if a player is on a special tile and changes player status accordingly
    def StatusChange(self, special_tiles = [3, 5, 8, 11, 18, 21, 23, 31, 34, 37, 39]):
        if self.tile.position in special_tiles:
            # If in Jail
            if self.tile.position in [11, 31]:
                self.status = 'is Jailed'
            # If in Income Tax or Super Tax
            elif self.tile.position in [5, 39]:
                self.status = 'is Taxed'
            # If in Chance
            elif self.tile.position in [37, 23, 8]:
                self.status = 'got a Chance Card!'
            # If in Community Chest
            elif self.tile.position in [34, 18, 3]:
                self.status = 'got a Community Chest!'
            # If in Pokemon Center
            elif self.tile.position == 21:
                self.status = 'is healing up...'
            print(f'{self.name} {self.status}')
            return True
        else:
            self.status = None
            return False

    # Function that apply effects to player based on the special tile they are on, except for Jail
    def StatusEffects(self):
        if self.status is not None:
            # Effects if under Tax status
            if self.status == 'is Taxed':
                # If under Income Tax, deduct $200
                if self.tile.position == 5:
                    self.deduct_money(200)
                    print(f'$200 has been deducted {self.name}\'s bank account as income tax!')
                # If under Super Tax, deduct 100
                if self.tile.position == 39:
                    self.deduct_money(100)
                    print(f'$100 has been deducted from {self.name}\'s bank account as super tax!')
                # Check if bank account is negative, and if so game over
                self.WinOrLose()
            elif self.status == 'got a Chance Card!':
                # Add chance function
                pass
            elif self.status == 'got a Community Chest!':
                #Add Chest function
                pass
            # Nothing happens if player is in Pokemon Center
            elif self.status == 'is healing up...':
                return False
        else:
            return False

    # Function that checks if player is in Jail, and deducts $50 if so
    def CheckJail(self):
        if self.status == 'is Jailed':
            decision = input('You are current in Jail\nPress ENTER to pay $50')
            self.deduct_money(50)
            print('$50 has been deducted from your bank account. You are now PRISON-FREE!')
            # Check if player is bankrupt
            self.WinOrLose()
            return True
        else:
            return False

    def __str__(self):
        return f'{self.name}'

    # Function that checks if player is bankrupt, and if so game ends
    def WinOrLose(self):
        if self.money < 0:
            print(f'{self.name} is bankrupt and has lost!')
            return True
        else:
            return False

    # Function that adds input amount to bank balance
    def add_money(self, amount):
        self.money += amount

    # Function that deducts input amount from bank balance
    def deduct_money(self, amount):
        self.money -= amount

# Circular Linked List that stores the board
class Board:
    def __init__(self, r = None):
        self.root = r
        self.size = 0

    # Function to add tiles
    def add(self, tile):
        # Check if Board is empty, and if so, the new tile will be the root tile
        if self.size == 0:
            self.root = tile
            self.root.next = self.root
        # If board is not empty, new tile will be added right after root tile
        else:
            tile.next = self.root.next
            self.root.next = tile
        self.size += 1

    # Function that moves player and acts depending on their position
    def Move(self, player, dice):
        # Check if player is in Jail, and act accordingly
        player.CheckJail()
        # Based on number rolled by dice, move the player by the same number of tiles
        start = player.tile
        player.steps += dice
        for i in range(dice):
            start = start.next
        player.tile = start
        time.sleep(0.5)
        print(f'{player.name} is now at {player.tile.name}\n--------------------------------')
        time.sleep(0.2)
        # Change player status if they are on a special tile and apply its effects accordingly
        player.StatusChange()
        player.StatusEffects()
        time.sleep(0.5)
        player.tile.show_Details()
        time.sleep(0.5)
        return player.tile.name

    # Function that removes ownership of tiles (used when a player has lost)
    def remove_Owner(self, player):
        current = self.root
        while True:
            if current.next is not self.root:
                if current.owner == player:
                    current.owner = None
                    current = current.next

    # Checks if player has passed Go, and rewards $200 if so
    def Go(self, player):
        if player.steps >= 40:
            player.add_money(200)
            print(f'--------------------------------\n{player.name} has has received $200 for passing by GO!')
            player.steps -= 40

    # Function that allows players to own a tile if eligible
    def buy(self, player, special_tiles = [3, 5, 8, 11, 18, 21, 23, 31, 34, 37, 39]):
        # No option to buy if on a special tile
            if player.tile.position in special_tiles:
                return False
            # If tile is a normal tile, give option to buy
            else:
                if player.tile.owner == None:
                    player_buy_option = input(f"--------------------------------\nWould you like to buy {player.tile}? Y/N ")
                    # If player chooses to buy, deduct cost of tile from their bank balance and add them to tile's ownership
                    if re.search('y', player_buy_option, re.I):
                        player.deduct_money(player.tile.cost)
                        player.tile.owner = player
                        print(f'--------------------------------\n{player.name} now owns {player.tile.name}')
                        time.sleep(0.5)
                        return True
                    time.sleep(0.5)
                    return False

    # Checks if player is owner of the current tile their own, transfers rent amount from their bank to owner's bank
    def rent_pay(self, player):
        if player.tile.owner != None and player.tile.owner != player:
            player.deduct_money(player.tile.rent)
            player.tile.owner.add_money(player.tile.rent)
            print(f'--------------------------------\nOops! You paid ${player.tile.rent} to {player.tile.owner.name} as rent ')

    # Create a list of instances of Tiles, whereby tile_data contains tile information. Made to edit Tile information more easily in the future
    def createBoard_List(self, tile_data = [['GO', 0, 0], ['ISLAND OF THE GIANT POKEMON', 400, 39], ['SUPER TAX', 0, 38], ['PARKLANE', 350, 37], ['CHANCE 3', 0, 36], ['CERULEAN CAVE', 200, 35], ['POWER PLANT', 320, 34], ['COMMUNITY CHEST 3', 0, 33], ['INDIGO PLATEAU', 300, 32], ['VICTORY ROAD', 300, 31], ['OFFICER JENNY CAUGHT YOU', 0, 30], ['CINNABAR LAB', 280, 29], ['POKEMON MANSION', 150, 28], ['CINNABAR ISLAND', 260, 27], ['SEAFOAM ISLANDS', 260, 26], ['MAGNET TRAIN STATION', 200, 25], ['SILPH CO.', 240, 24], ['SAFFRON CITY', 220, 23], ['CHANCE 2', 0, 22], ['SAFARI ZONE', 220, 21], ['POKEMON CENTRE', 0, 20], ['FUCHSIA CITY', 200, 19], ['BICYCLE ROAD', 180, 18], ['COMMUNITY CHEST 2', 0, 17], ['CELADON SUPERMART', 180, 16], ['CELADON CITY', 200, 15], ['CEMETRY@LAVENDER', 160, 14], ['LAVENDER TOWN', 140, 13], ['VERMILLION CITY', 150, 12], ['S.S. ANNE', 140, 11], ['JAIL', 0, 10], ['DAYCARE@ROUTE 5', 120, 9], ['CERULEAN CITY', 100, 8], ['CHANCE 1', 0, 7], ['MT. MOON', 100, 6], ['PEWTER CITY', 200, 5], ['INCOME TAX', 0, 4], ['VIRIDIAN CITY', 60, 3], ['COMMUNITY CHEST 1', 0, 2], ['PALLET TOWN', 60, 1]]):
        tile_list = []
        for tile in tile_data:
            gameTile = Tile(name = tile[0], position = tile[2] + 1, cost = tile[1])
            tile_list.append(gameTile)
        return tile_list





















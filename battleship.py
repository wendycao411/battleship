#to-do list
#Battleship board - 10x10 board, should label board columns and rows so users can input exact locations
#print board each time a new game is started
#computer will choose where to put the boats on its board, which will not be displayed to the user but will be updated as the player inputs values
#player chooses location to reveal
#if there is a ship, show an X, if there is no ship, show an ~
#if all ships found, end game and display winner
#if runs out of attempts, end game
#program must reject bad input - cannot reveal a space that was already revealed, or a space out of range
#keep track of how many games the player won
#limit number of bullets

#Citing random module from https://docs.python.org/3/library/random.html
import random
alphabet = "ABCDEFGHIJKLMNOPXRSTUVWXYZ"
#this will keep track of how many games you win in total
player_wins = 0

#Citing instructions from https://www.hasbro.com/common/instruct/battleship.pdf
def print_instructions():
	#if the user chooses to see the instructions, these will be displayed.
	print("\nWelcome to Battleship! The objective of this game is to sink all 5 of your opponent's (the computer's) ships before you run out of your 50 attempts.")
	print("\nTo input where you'd like to place a ship or what space you'd like to reveal, type the column number first then the row letter; for example, E6 is a valid response, but 5A is not.")
	print("\nThe ships are marked with X's while empty spaces are marked with ~'s.")
	print("\nGood luck!")

def reset_computer_board(size):
	#when a new game is started, the computer will reset its board and clear any previous data.
	global computer_board
	global ship_sunk
	global ships_needed
	global ship_pos
	global attempt
	#this is a list that will print out a . for each space in a board that has a size of size x size.
	computer_board = [["." for i in range(size)]for j in range(size)]
	ship_sunk = 0
	ships_needed = 5
	ship_pos = []
	attempt = 50
	
def reset_user_board(size):
	#we will have a separate user board that will be displayed to the user so the computer's board is "hidden". This will also be reset in the beginning
	global user_board
	user_board = [["." for i in range(size)]for j in range(size)]

def arrange_user_board(size):
	#this function will add labels to the board
	global labels
	labels = "ABCDEFGHIJ"
	col_label = [i for i in range(size)]
	print("\n")
	print("   ", end = " ")
	for i in col_label:
		print(i, end = " ")
	print("\n   ____________________")
	row_num = 0
	for row in user_board:
		print(labels[row_num], end = " | ")
		for i in row:
			print(i, end = " ")
		row_num += 1
		print()

def place_ship_on_board(row_init, row_end, col_init, col_end):
	#this is a function that will take parameters to check if the spaces are empty so the computer can place a ship. Then the computer will add the ships to its board
	valid = True
	for row in range(row_init, row_end):
		for col in range(col_init, col_end):
			if computer_board[row][col] != ".":
				valid = False
				break
	if valid:
		#this will run if we can place the ship
		for row in range(row_init, row_end):
			for col in range(col_init, col_end):
				#this will add a ship to the board, putting a % for each space between the start and end coordinates
				computer_board[row][col] = "%"
				#the % will represent a ship that was not hit on the computer's board
		ship_pos.append([row_init, row_end, col_init, col_end])
		#we will add the row numbers and column numbers of the start and end of the ship to a list we made previously, and this will be used later to check if the user hit a ship
	return valid
	#if everything works, the function will return True to indicate that it was carried out
	#it will return False if the space is occupied

#Citing place_ship_valid from https://pythondex.com/python-battleship-game
def place_ship_valid(row, col, dir, length, size):
	#this function will be taking in parameters to check if the ship that will potentially be placed is out of range
	row_init = row
	row_end = row + 1
	col_init = col
	col_end = col + 1
	
	if dir == "right":
		if col + length >= size:
			return False
		col_end = col + length
			#if the ship goes out of range, the function will return False and the ship will not be placed
		#this will create the end coordinate of the ship
	
	elif dir == "left":
		if col - length < 0:
			return False
		col_init = col - length + 1
	
	elif dir == "down":
		if row + length >= size:
			return False
		row_end = row + length
	
	elif dir == "up":
		if row - length < 0:
			return False
		row_init = row - length + 1

	#this function will return true if this function and place_ship_on_board returns true, indicating that the placement is valid
	return place_ship_on_board(row_init, row_end, col_init, col_end)

def random_ship():
	#this generates the random coordinates for the ships to be placed at and the random directions they will face
	global ships_placed
	ships_needed = 5
	ships_placed = 0
	#we will place 5 randomly generated ships
	while ships_placed < ships_needed:
		rand_row = random.randint(0, 9)
		rand_col = random.randint(0, 9)
		dir = random.choice(["up", "down", "left", "right"])
		#the ship will have a random size between 2 and 5
		ship_size = random.randint(2,5)
		if place_ship_valid(rand_row, rand_col, dir, ship_size, 10):
			#if the code was able to place a ship, we add one to the number of ships_placed
			ships_placed += 1

def valid_row_col(row, col, size):
	#this function will check to see if the row and columns inputted are within the boundaries and have not been used before
	while row <= -1 or row > size or col <= -1 or col > size:
		print("That is not a valid input. Please try again.")
		playerInput()
	if computer_board[row][col] == "~" or computer_board[row][col] == "X":
		print("You have shot here before, please input another coordinate.")
		return False
	elif computer_board[row][col] == "." or computer_board[row][col] == "%":
		return True
	

def playerInput():
	#this function will check to see if the player's input is valid
	#it is valid if it follows the format (a row label with a column label WITHOUT a space between) and if the player hadn't shot there before
	valid_move = False
	row = -1
	col = -1
	#the function will keep asking the user for input until it gets a valid response
	while valid_move == False:
		move = input("Enter coordinates, e.g. D4: ")
		#changing the input to uppercase will allow the code to take in lower and uppercase characters
		move = move.upper()
		#if they did not input a letter and a single digit, the string would have a length greater than 2 and must be incorrect
		#since our board uses all the single digit numbers and no two-digit numbers, we can just use this to see if they inputted a valid column coordinate
		if len(move) != 2:
			print("That is not a valid input. Please try again.")
			continue
		row = move[0]
		col = move[1]
		#if the first character they input is not a letter or if the second character is not a number, it is also not valid input
		if row.isalpha() == False or col.isnumeric() == False:
			print("That is not a valid input. Please try again.")
			continue
		#this will convert the coordinates the player inputted into integers the code can use to find the location on its own board
		#we will find the row number by finding its location in the original string of letters, which matches its row number
		row = int(alphabet.find(row))
		col = int(col)
		if valid_row_col (row, col, 10):
			valid_move = True
		else:
			continue
	#the function will return the integer values of the player's inputs
	return row, col

def checkShip(row, col):
	completed_ship = True

	#for each positioned ship
	for i in ship_pos:

		#we find the x-coordinate for its "head", which is at index 0 in the list ship_pos
		row_init = i[0]
		#we find the x-coordinate for its "tail" at index 1
		row_end = i[1]
		#we find the y-coordinate for its head at index 2
		col_init = i[2]
		#we find the y-coordinate for its tail at index 3
		col_end = i[3]

		#if the row and column that the user inputs is between the coordinates of a ship
		if row_init <= row <= row_end and col_init <= col <= col_end:
			#the program will check at each space between the ship's coordinates to see if there is a ship
			for r in range(row_init, row_end):
				for c in range(col_init, col_end):
					if computer_board[r][c] != "X":
						#if any space between the start and end coordinates have not been revealed, the ship has not been entirely sunken yet. Thus the function will return False.
						completed_ship = False
						break
	return completed_ship

def shoot():
	#this function will use the results from the function playerInput and place a piece on the board based on the coordinates the player inputted.
	global ship_sunk, attempt
	row, col = playerInput()
	print()

	#if the computer's board has a ., it means there was no ship there so the player missed. We must change the user_board's piece to a ~ to represent that that space had been hit.
	if computer_board[row][col] == ".":
		print("You missed!")
		computer_board[row][col] = "~"
		#We will also change the computer_board's piece so it can stay updated along with the user_board
		user_board[row][col] = "~"
	#the % means that there was a boat that had not been hit yet on the computer's board, so if the user hits that spot they will have hit a ship.
	#we must change the piece on both boards to X
	elif computer_board[row][col] == "%":
		print("You hit!", end=" ")
		computer_board[row][col] = "X"
		user_board[row][col] = "X"
		#if the user sinks the whole ship
		if checkShip(row, col):
			print("A ship was completely sunk!")
			ship_sunk += 1
		else:
			print("A ship was shot!")
	attempt -= 1

def game_over():
	#this function will check to see if the game is over 
	#the game is over when the player sinks all the ships or runs out of bullets.
	global end_game, player_wins, attempt
	end_game = False
	if ships_needed == ship_sunk:
		print("\n----------------------------")
		print("\nCongratulations, you won!")
		player_wins += 1
		print("\nYour current score is: " + str(player_wins))
		print("----------------------------")
		print()
		end_game = True
	elif attempt <= 0:
		end_game = True
		print("\n----------------------------")
		print("\nYou lost!")
		print("\nYour current score is: " + str(player_wins))
		print("----------------------------")
		print()
	return end_game

#this is the game loop
start = True
while start == True:
	start_game = str(input("Would you like to play a game of Battleship? Enter Y/N: "))
	if start_game == "y" or start_game == "Y":
		ask_instructions = True
		end_game = False
		#if the user wants to start the game, they will input a Y. if they don't, they will input an N and the code will proceed to the elif block.
		while ask_instructions == True:
			instructions = "N"
			instructions = input("\nWould you like to see the instructions? Enter Y/N: ")
			if instructions == "Y" or instructions == "y":
				#the instructions print if the user inputs a y but skips this section if the user inputs an n
				print_instructions()
				ask_instructions = False
			elif instructions == "N" or instructions == "n":
				print("\nGood luck!")
				ask_instructions = False
			else:
				print("That is not a valid input. Please try again.")
				continue
		#here we reset the boards every time a new game is played and randomly place ships on them
		reset_computer_board(10)
		reset_user_board(10)
		random_ship()
		#this loop runs until the user wins or loses
		while end_game == False:
			#it will print out the updated user_board, how many ships are left, how many tries the player has left, and continue asking for player inputs until the game is over.
			arrange_user_board(10)
			print("\nNumber of ships remaining: " + str(ships_needed - ship_sunk))
			print("\nNumber of attempts remaining: " + str(attempt))
			print("----------------------------")
			print("")
			shoot()
			game_over()
		
	elif start_game == "N" or start_game == "n":
		print("Goodbye!")
		start = False
	else:
		print("That is not a valid input. Please try again.")
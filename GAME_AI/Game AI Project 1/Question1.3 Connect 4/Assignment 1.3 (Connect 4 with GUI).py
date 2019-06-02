import numpy as np
import pygame
import sys
import math
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


ROW_COUNT = 6
COLUMN_COUNT = 7


##function to retrieve and empty row for the user specified column
def retrieve_empty_row(S, c):
    for row in range(6):
        if S[row][c] == 0:
            return row



##create the board
def create_board():
	S = np.zeros((ROW_COUNT,COLUMN_COUNT))
	return S

##change the orientation of the board cos the pieces get filled up from he top otherwise and print it
def print_board(board):
	print(np.flip(board, 0))




def check_winner(board, piece):
	##check vertical locations for winning first  
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True
   ##check horizontal locations for winning first 
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True



  ##check positively sloped diagnols
    ## if we start from down and 4th row and 4th column is the max we can go upto to make a diagnol hence we check with condition rowcount-3 and column count -3	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	##check negative sloped diagnols
    ##same logic as the positively sloped diagnol but in the other direction
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True

def draw_connect4_board(board):
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			##draw rectangle
            ## the column value is modified with r *SQUARESIZE+SQUARESIZE because we want one row empty at the top to see the coins dropping and here the axis starts from below..
			pygame.draw.rect(screen, (34,139,34), (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			  ##the above one was postioned at the top left so this should be that plus some  offset cos it has to be placed below that inside the rectangle space.
            ##the offset will be half the rectangle as we are considering radius.
            ##the last parameter is the radius.
			pygame.draw.circle(screen, (165,42,42), (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
	
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):		
			if board[r][c] == 1:
				pygame.draw.circle(screen, (0,0,255), (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == 2: 
				pygame.draw.circle(screen, (255,255,0), (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	pygame.display.update()

#creating the board confiuration
board = create_board()
##print the current board statuss
print_board(board)
##setting the flag to false which is basically no winner yet 
game_over = False
turn = 0
#initialising pygame
pygame.init()
##the squares inside which the circles are present are 100 pixels each.here measurement is taken in pixels
SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
draw_connect4_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("Arial", 75)
counter=0
label = myfont.render("CONNECT 4", 1, (255,0,0))
screen.blit(label, (40,10)) 
while not game_over:
  
##pygame considers everything like a mouse motion a click etc as an event.
	for event in pygame.event.get():
		 #to make sure the game is exited properly on the click of 'x'.
		if event.type == pygame.QUIT:
			sys.exit()
##this event is triggered when a mouse event occurs,say for example one      of the event  being user clicks on the screen for the coin to be dropped.
		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen, (0,0,0), (0,0, width, SQUARESIZE))
			posx = event.pos[0]
			if turn == 0:
				pygame.draw.circle(screen, (0,0,255), (posx, int(SQUARESIZE/2)), RADIUS)
			else: 
				pygame.draw.circle(screen, (255,255,0), (posx, int(SQUARESIZE/2)), RADIUS)
		pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(screen, (0,0,0), (0,0, width, SQUARESIZE))
			
			#player one chance 
			if turn == 0:
				posx = event.pos[0]
				## the board is of width 700 so dividing by 100 so as to scale to 7 instead of 700
				col = math.floor(posx/SQUARESIZE)
				col=int(col)

				if board[5][col]==0:
					row = retrieve_empty_row(board, col)
					board[row][col]=1
					

					if check_winner(board, 1):
						winner_label = myfont.render("Yayy Player 1 wins ", 1, (255,192,203))
						screen.blit(winner_label, (40,10))
						
						game_over = True


			# player two chance
			else:				
				posx = event.pos[0]
				col = math.floor(posx/SQUARESIZE)
				col=int(col)
				if board[5][col]==0:
					row = retrieve_empty_row(board, col)
					board[row][col]=2
					

					if check_winner(board, 2):
						winner_label = myfont.render("Yayy Player 2 wins!!", 1, (255,192,203))
						screen.blit(winner_label, (40,10))
						game_over = True

			print_board(board)
			##calling the function which draws the connect 4 board
			draw_connect4_board(board)
			#incrementing counter to check when the board is completely filled.this variable is used to check draw condition
			counter=counter+1
			turn += 1
			turn = turn % 2

			if game_over == True :
				print('game over true')
				pygame.time.wait(3000)
			print counter
			##checking draw condition	
			if counter>=42 and game_over==False:
				print counter
				winner_label = myfont.render("draw game", 1, (255,192,203))
				screen.blit(winner_label, (40,10))
				break
		
			
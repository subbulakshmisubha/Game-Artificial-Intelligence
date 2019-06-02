
import numpy as np, itertools
import time

Board_width = 7
Board_height = 6

class NextMove(object):
    def __init__(self, score=0, x_coord = -1, y_coord = -1):
        self.score = score
        self.x_coord = x_coord
        self.y_coord = y_coord

#Calculate the final score of a board based on the evaluation function
def calc_board_score(S , player):
    
    score = 0
    moves_x, moves_y = get_board_moves(S)
    #For each move (i,j) that is already on board, run the evaluation function for each 4-neighbourhood starting from (i,j) in all 8 directions
    for i in range(len(moves_x)) :
        score += evaluation_func(top_elements(S, moves_x[i], moves_y[i]), player)
        score += evaluation_func(bottom_elements(S, moves_x[i], moves_y[i]), player)
        score += evaluation_func(left_elements(S, moves_x[i], moves_y[i]), player)
        score += evaluation_func(right_elements(S, moves_x[i], moves_y[i]), player)
        score += evaluation_func(topL_diag_elements(S, moves_x[i], moves_y[i]), player)
        score += evaluation_func(topR_diag_elements(S, moves_x[i], moves_y[i]), player)
        score += evaluation_func(bottomL_diag_elements(S, moves_x[i], moves_y[i]), player)
        score += evaluation_func(bottomR_diag_elements(S, moves_x[i], moves_y[i]), player)
    
    return score


#Get indices of all moves currently on board
def get_board_moves(S):
    
    x,y = np.where(S != 0)
    return x,y

#Get the top 4-neighbourhood for cell (i,j)
def top_elements(S,i,j):
    if (i-3 >= 0):
        return(S[i-3:i+1,j])
    else:
        return []

#Get the bottom 4-neighbourhood for cell (i,j)
def bottom_elements(S,i,j):
    if (i+4 <= Board_height):
        return(S[i:i+4,j])
    else:
        return []

#Get the right 4-neighbourhood for cell (i,j)
def right_elements(S,i,j):
    if (j+4 <= Board_width):
        return(S[i,j:j+4])
    else:
        return []

#Get the left 4-neighbourhood for cell (i,j)
def left_elements(S,i,j):
    if (j-3 >= 0):
        return(S[i,j-3:j+1])
    else:
        return []

#Get the top-right diagonal 4-neighbourhood for cell (i,j)
def topR_diag_elements(S,i,j):
    elements = []
    if (j+4 <= Board_width or i-3 >= 0):
        elements = np.diag(np.fliplr(S[i-3:i+1,j:j+4]))    
    if (len(elements) == 4):
        return elements
    else:
        return []

#Get the top-left diagonal 4-neighbourhood for cell (i,j)
def topL_diag_elements(S,i,j):
    elements = []
    if (j-3 >= 0 or i-3 >= 0):
        elements = np.diag(S[i-3:i+1,j-3:j+1])    
    if (len(elements) == 4):
        return elements
    else:
        return []

#Get the bottom-right diagonal 4-neighbourhood for cell (i,j)
def bottomR_diag_elements(S,i,j):
    elements = []
    if (j+4 <= Board_width or i+4 <= Board_height):
        elements = np.diag(S[i:i+4,j:j+4])   
    if (len(elements) == 4):
        return elements
    else:
        return []

#Get the bottom-left diagonal 4-neighbourhood for cell (i,j)
def bottomL_diag_elements(S,i,j):
    elements = []
    if (j-3 >= 0 or i+4 <= Board_height):
        elements = np.diag(np.fliplr(S[i:i+4,j-3:j+1]))    
    if (len(elements) == 4):
        return elements
    else:
        return []
    
    
#Get indices of available board cells
def get_available_cells(S):
    
    x = []
    y = []
    for i in range(Board_width):
        for j in range(Board_height - 1, -1, -1):
            if (S[j][i] == 0):
                x.append(j)
                y.append(i)
                break;
    return x,y


#Function to evaluate score of a 4-neighbourhood on the board
def evaluation_func(elements, player):
    
    opponent = (-1)*player
    
    #Player's 4 in a row
    if(set(elements) == {player}):
        return 150000     
    
    #Player's 3 in a row (including empty spaces in between)
    if((set(elements) == {player,0}) and (np.count_nonzero(elements == player) == 3)):
        return 15000    
    
    #Player's 2 in a row (including empty spaces in between)
    if((set(elements) == {player,0}) and (np.count_nonzero(elements == player) == 2)):
        return 10    
    
    #Player's 1 in a row (including empty spaces in between)
    if((set(elements) == {player,0}) and (np.count_nonzero(elements == player) == 1)):
        return 1
    

    #Opponent's 4 in a row
    if(set(elements) == {opponent}):
        return -100000
    
    #Opponent's 3 in a row (including empty spaces in between)
    if((set(elements) == {opponent,0}) and (np.count_nonzero(elements == opponent) == 3)):
        return -10000
    
    #Opponent's 2 in a row (including empty spaces in between)
    if((set(elements) == {opponent,0}) and (np.count_nonzero(elements == opponent) == 2)):
        return -10
    
    #Opponent's 1 in a row (including empty spaces in between)
    if((set(elements) == {opponent,0}) and (np.count_nonzero(elements == opponent) == 1)):
        return -1
    
    else:
        return 0


# Function move_still_possible: game runs until the entire matrix is filled
def move_still_possible(S):
    return not (S[S==0].size == 0)


# Function move_at_random: Next random move of a player
def move_at_random(S, p):
    xs, ys = np.where(S==0)
    i = np.random.permutation(np.arange(xs.size))[0]
    
    #Condition check to add symbol to the bottom most available slot in a particular column
    
    for k in range(Board_height,0,-1):
        if(S[k-1,ys[i]])==0:
            
            S[k-1,ys[i]]=p
            break
            
    return S

   
# Function is_sequence_formed : Checking if the sequence has formed 
def is_sequence_formed(player, target_list, sequence):

    if player in target_list:
        longest_segment = max(sum(1 for i in l) for marker, l in itertools.groupby(target_list) if marker == player)
        if longest_segment >= sequence:
            return True

        return False

    
# Function find_winner: Finding the winner and storing the gameStats according to row, column, left diagonal  
#                       or right diagonal win

def find_winner(S, player):

    # Checking horizontal 
    j=0
    for row in S.tolist():
        j+=1
        if is_sequence_formed(player , target_list = row, sequence = 4):
            #modify_gameStats(S,player,j-1,row=True)
            return True

    # Checking vertical
    j=0
    for column in S.transpose().tolist():
        j+=1
        if is_sequence_formed(player , target_list = column, sequence = 4):
            #modify_gameStats(S,player,j-1,row=False,col=True)
            return True

    # Checking Diagonal
    for offset in range(S.shape[1] * -1, S.shape[1]):

        # Getting the diagonal 
        left_to_right = S.diagonal(offset, 1, 0).tolist()
        right_to_left = S[::-1].diagonal(offset, 1, 0).tolist()

        if len(right_to_left) < 4 and len(left_to_right) < 4:
            continue

        if is_sequence_formed(player, target_list = left_to_right, sequence = 4):
     
            #modify_gameStats(S,player,offset,row=False,col=False,left_diag=True)
            return True

        if is_sequence_formed(player, target_list = right_to_left, sequence = 4):
          
            #modify_gameStats(S,player,offset,row=False,col=False,left_diag=False,right_diag=True)
            return True

    # No winner
    return False
    

# relate numbers (1, -1, 0) to symbols ('x', 'o', ' ')
symbols = {1:'x', -1:'o', 0:' '}

# Function print_game_state : print game state matrix 
def print_game_state(S):
    B = np.copy(S).astype(object)
    for n in [-1, 0, 1]:
        B[B==n] = symbols[n]
    print B



def minimax(player, gameState, threshold_depth, is_max_turn=True, depth=0):
    
    #depth += 1
    
    new_gameState = np.copy(gameState)
    xs, ys = get_available_cells(gameState)
    if is_max_turn:
        max_sign = player
        min_sign = player*(-1)
    else:
        max_sign = player*(-1)
        min_sign = player

    # Check for return cases
    if(depth == threshold_depth):
        if(depth%2 == 0):
            return NextMove(calc_board_score(new_gameState, player),None,None)
        elif(depth%2 != 0):
            return NextMove(calc_board_score(new_gameState, player*(-1)),None,None)
    
    
    elif len(xs) == 0:
        return NextMove(0, None, None)

    moves = []
    for i in range(len(xs)):
        move = NextMove(None, xs[i], ys[i])
        new_gameState[xs[i],ys[i]] = player
        
        if find_winner(new_gameState,max_sign):
            return NextMove(100000, xs[i], ys[i])
    
        elif find_winner(gameState,min_sign):
            return NextMove(-100000, xs[i], ys[i])
        
        if is_max_turn:
            result = minimax(min_sign, new_gameState, threshold_depth, False, depth+1)
        else:
            result = minimax(max_sign, new_gameState, threshold_depth, True, depth+1)
        move.score = result.score
        new_gameState[xs[i],ys[i]] = 0   # Revert changes made to board
        moves.append(move)

    if is_max_turn:        
        m = max(i.score for i in moves)
        best_move = np.random.choice([i for i, j in enumerate(k.score for k in moves) if j == m])

    else:
        m = min(i.score for i in moves)
        best_move = np.random.choice([i for i, j in enumerate(k.score for k in moves) if j == m])

    return moves[best_move]


# Main 
if __name__ == '__main__':
    
    # Counters for the number of wins of player1, player2, draws, no. of moves and time taken for each minimax() call
    player1wins =0
    player2wins =0
    gameDraw = 0
    no_of_moves = []
    time_taken_for_minimax = []
    
    # Total number of random games to be run for taking Statistics
    noOfGames = 100

    
    
    for i in range (0,noOfGames):
        
        # initialize flag that indicates win
        noWinnerYet = True
        
        # initialize 6x7 connect 4 board
        gameState = np.zeros((Board_height,Board_width), dtype=int)

        # initialize player number, move counter
        player = 1
        mvcntr = 1
        
        
        
        while move_still_possible(gameState) and noWinnerYet:
            # get player symbol
            name = symbols[player]
            print '%s moves' % name

            if(player==1):
                start_time = time.time()
                best_move = minimax(player, gameState, 3)
                time_taken_for_minimax.append(time.time() - start_time)
                gameState[best_move.x_coord,best_move.y_coord] = player 
            else:
                gameState = move_at_random(gameState, player)

            # print current game state
            print_game_state(gameState)
        
            # evaluate game state
            if find_winner(gameState, player):
                print 'player %s wins after %d moves' % (name, mvcntr)
                no_of_moves.append(mvcntr)
                noWinnerYet = False
                
                if player==1:
                    player1wins+=1
                else:
                    player2wins+=1

            # switch player and increase move counter
            player *= -1
            mvcntr +=  1



        if noWinnerYet:
            gameDraw+= 1
            print 'game ended in a draw' 

    
    print "\n\nGAME STATS:\n "
    print "\n No. of times player 1 wins: %d" %player1wins
    print "\n No. of times player 2 wins: %d" %player2wins
    print "\n No. of times there was a draw: %d" %gameDraw
    print "\n Average no. of moves: %d" %(sum(no_of_moves)/len(no_of_moves))
    print "\n Average Time taken by player using Minimax:",(sum(time_taken_for_minimax)/len(time_taken_for_minimax))


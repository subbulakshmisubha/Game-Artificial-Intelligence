
# coding: utf-8

# In[4]:


import numpy as np, itertools

#the default matrix required for connect4
gameStats = np.zeros((6,7), dtype=int)

# Function move_still_possible: game runs until the entire matrix is filled
def move_still_possible(S):
    return not (S[S==0].size == 0)

# Function move_at_random: Next random move of a player
def move_at_random(S, p):
    xs, ys = np.where(S==0)
    i = np.random.permutation(np.arange(xs.size))[0]
    
    #Condition check to add symbol to the bottom most available slot in a particular column
    
    for k in range(6,0,-1):
        if(S[k-1,ys[i]])==0:
            
            S[k-1,ys[i]]=p
            break
            
    return S

# Function findSubstring : Returns the position of the sequence in the diagonal
def findSubstring(string, substring):
    len_substring = len(substring)
    for i in range(len(string)):  
        if (np.array_equal(string[i:i+len_substring],substring)):
             return i  

# Function modify_gameStats : GameStats consists of the Statistics of the likely good moves            
def modify_gameStats(S,player,position,row=False,col=False,left_diag=False,right_diag=False):
    
    # the substring to be checked in the matrix
    substring=np.array([player]*4)
    
    # Storing the win position in gameStats if the game is won with horizontal sequence
    if(row):
        i=findSubstring(S[position],substring)
        #print i
        gameStats[position,i:i+len(substring)]+=1
    
    # Storing the win position in gameStats if the game is won with vertical sequence
    elif(col):
        i=findSubstring(S[:,position],substring)
        #print i
        gameStats[i:i+len(substring),position]+=1
    
    # Storing the win position in gameStats if the game is won with left_to_right diagonal sequence
    elif(left_diag):
        i=findSubstring(S.diagonal(position,1,0),substring)
        starts = [0,0+((-1)*position)] if position<0 else [0+position,0]
        starts = [starts[0]+i,starts[1]+i]
        for X in range(0,4):
            gameStats[starts[0]+X, starts[1]+X]+=1
    
    # Storing the win position in gameStats if the game is won with right_to_left diagonal sequence
    elif(right_diag):
        i=findSubstring(S[::-1].diagonal(position, 1, 0),substring)
        starts = [S.shape[0]-1,0+((-1)*position)] if position<0 else [S.shape[0]-1-position,0]
        starts = [starts[0]-i,starts[1]+i]
        for X in range(0,4):
            gameStats[starts[0]-X, starts[1]+X]+=1
        
    
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
            modify_gameStats(S,player,j-1,row=True)
            return True

    # Checking vertical
    j=0
    for column in S.transpose().tolist():
        j+=1
        if is_sequence_formed(player , target_list = column, sequence = 4):
            modify_gameStats(S,player,j-1,row=False,col=True)
            return True

    # Checking Diagonal
    for offset in range(S.shape[1] * -1, S.shape[1]):

        # Getting the diagonal 
        left_to_right = S.diagonal(offset, 1, 0).tolist()
        right_to_left = S[::-1].diagonal(offset, 1, 0).tolist()

        if len(right_to_left) < 4 and len(left_to_right) < 4:
            continue

        if is_sequence_formed(player, target_list = left_to_right, sequence = 4):
     
            modify_gameStats(S,player,offset,row=False,col=False,left_diag=True)
            return True

        if is_sequence_formed(player, target_list = right_to_left, sequence = 4):
          
            modify_gameStats(S,player,offset,row=False,col=False,left_diag=False,right_diag=True)
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

# Main 
if __name__ == '__main__':
    
    # Counters for the number of wins of player1, player2 and draw consition
    player1wins =0
    player2wins =0
    gameDraw = 0
    
    # Total number of random games to be run for taking Statistics
    noOfGames = 10000
    
    for i in range (0,noOfGames):
        
        # initialize flag that indicates win
        noWinnerYet = True
        
        # initialize 6x7 connect 4 board
        gameState = np.zeros((6,7), dtype=int)

        # initialize player number, move counter
        player = 1
        mvcntr = 1
        
        while move_still_possible(gameState) and noWinnerYet:
            # get player symbol
            name = symbols[player]
            print '%s moves' % name

            # let player move at random
            gameState = move_at_random(gameState, player)

            # print current game state
            print_game_state(gameState)
        
            # evaluate game state
            if find_winner(gameState, player):
                print 'player %s wins after %d moves' % (name, mvcntr)
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
    print gameStats
    print "\n No. of times player 1 wins: %d" %player1wins
    print "\n No. of times player 2 wins: %d" %player2wins
    print "\n No. of times there was a draw: %d" %gameDraw



# coding: utf-8

# In[4]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def move_still_possible(S):
    return not (S[S==0].size == 0)


def move_at_random(S, p):
    xs, ys = np.where(S==0)

    i = np.random.permutation(np.arange(xs.size))[0]
    
    S[xs[i],ys[i]] = p

    return S


#Defines the heuristic values for each line (row/column/diagonal) of the game board
def get_heuristic(S,p):
    
    #for an empty line return +1
    if(all([ i == 0 for i in S ])):
        return 1
    
    #for a line with only one of player's symbols return +10
    elif(((np.sum(S)==1) and (p==1)) or ((np.sum(S)==(-1)) and (p==(-1)))):
        return 10
    
    
    #for a line with only one of opponent's symbols return -10
    elif(((np.sum(S)==1) and (p==(-1))) or ((np.sum(S)==(-1)) and (p==1))):
        return (-10)
    
    
    #for a line with two of player's symbols return +150
    elif(((np.sum(S)==2) and (p==1)) or ((np.sum(S)==(-2)) and (p==(-1)))):
        return 150
    
    
    #for a line with two of opponent's symbols return +100
    elif(((np.sum(S)==2) and (p==(-1))) or ((np.sum(S)==(-2)) and (p==1))):
        return 100
    
    
    #for a line with one player's and one opponent's symbol return 0
    elif(np.sum(S)==0):
        return 0
    
    
#calculate heuristics for each line on the 3x3 board that cell (x,y) appears in.
#The final heuristic for cell (x,y) is the sum of heuristics from each line.
def calc_heuristic_of_cell(x,y,S,p):
    heuristic=0
    
    #calculate heuristic of row
    heuristic+=get_heuristic(S[x],p)
    
    #calculate heuristic of column
    heuristic+=get_heuristic(S[:,y],p)
    
    #calculate heuristic for right diagonal (0,2) (1,1) (2,0)
    if((x+y)==2):
        heuristic+=get_heuristic(np.diag(np.rot90(S)),p)
    
    #calculate heuristic for left diagonal (0,0) (1,1) (2,2)
    if(x==y):
        heuristic+=get_heuristic(np.diag(S),p)
        
    return heuristic    



#function to evaluate heuristic of each free cell position on board
def move_with_heuristic(S, p):
    
    xs, ys = np.where(S==0)

    storeHeuristic=[0]*len(xs)
    
    for i in range(0,len(xs)):
        storeHeuristic[i]=calc_heuristic_of_cell(xs[i],ys[i],S,p)
        
    #choose the index of the maximum heuristic. For multiple such indices, choose one at random
    index=np.random.choice(np.argwhere([ i == np.max(storeHeuristic) for i in storeHeuristic ]).flatten())
    
    S[xs[index],ys[index]] = p

    return S


def move_was_winning_move(S, p):
    if np.max((np.sum(S, axis=0)) * p) == 3:
        return True

    if np.max((np.sum(S, axis=1)) * p) == 3:
        return True

    if (np.sum(np.diag(S)) * p) == 3:
        return True

    if (np.sum(np.diag(np.rot90(S))) * p) == 3:
        return True

    return False


  
# relate numbers (1, -1, 0) to symbols ('x', 'o', ' ')
symbols = {1:'x', -1:'o', 0:' '}

# print game state matrix using symbols
def print_game_state(S):
    B = np.copy(S).astype(object)
    for n in [-1, 0, 1]:
        B[B==n] = symbols[n]
    print B



#Visualising the results as a bar chart
def plot_wins_and_draws(x,y):
    get_ipython().magic(u'matplotlib inline')
    plt.title('HISTOGRAM OF WINS AND DRAWS (Player X moves with heuristic)\n')
    plt.ylabel('Number of Matches')
    plt.grid(color='gray', linestyle='dashed',zorder=0)
    plt.bar(x,y,zorder=3,width=0.5)
    plt.savefig('1.3 Histogram (Player X heuristic, Player O random).png')
    plt.show()    
    

if __name__ == '__main__':
    
    #counters for wins of player 1, player 2 and draws
    winsPlayer1=0
    winsPlayer2=0
    draws=0        
    
    #number of matches in the tournament
    numberOfGames = 10000

    for i in range(0,numberOfGames):
        
        # initialize 3x3 tic tac toe board
        gameState = np.zeros((3,3), dtype=int)
                
        # initialize player number, move counter
        player = 1
        mvcntr = 1
        
        # initialize flag that indicates win
        noWinnerYet = True
        
        while move_still_possible(gameState) and noWinnerYet:
           
            # get player symbol
            name = symbols[player]
            #print '%s moves' % name

            # let player 1 move with probability and player 2 move at random
            if(player==1):
                gameState = move_with_heuristic(gameState,player)
                
            else:
                gameState = move_at_random(gameState, player)
                

            # print current game state
            #print_game_state(gameState)
        
            # evaluate game state
            if move_was_winning_move(gameState, player):
                #print 'player %s wins after %d moves' % (name, mvcntr)
                
                #if player X wins, increment counter winsPlayer1
                if name == 'x':
                    winsPlayer1=winsPlayer1+1
                
                #if player O wins, increment counter winsPlayer2
                else:
                    winsPlayer2=winsPlayer2+1
                noWinnerYet=False    
                

            # switch player and increase move counter
            player *= -1
            mvcntr +=  1

        if noWinnerYet:
            #print 'game ended in a draw' 
            #if match ends in a draw, increment counter draws
            draws=draws+1
    
    #x stores the labels and y stores the frequencies of wins and draws
    x=['Wins by Player 1','Wins by Player 2','Draws'] 
    y=[winsPlayer1,winsPlayer2,draws]           
    
    #plotting the frequencies in a bar chart
    plot_wins_and_draws(x,y)


# In[1]:


python version


# In[2]:


python -version


# In[3]:


python --version


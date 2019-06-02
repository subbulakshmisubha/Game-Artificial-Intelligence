
# coding: utf-8

# In[1]:


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


#function to decide player's next move as per the probabilityMatrix values
def move_with_probability(S, p, pm):
    
    xs, ys = np.where(S==0)
    
    #select the index of the cell position with the highest probability value as the players next move
    max=0
    index=0
    for i in range(0,len(xs)):
        if(pm[xs[i],ys[i]] > max):
            max=pm[xs[i],ys[i]]
            index=i
    
    
    S[xs[index],ys[index]] = p

    return S

  
# relate numbers (1, -1, 0) to symbols ('x', 'o', ' ')
symbols = {1:'x', -1:'o', 0:' '}


# print game state matrix using symbols
def print_game_state(S):
    B = np.copy(S).astype(object)
    for n in [-1, 0, 1]:
        B[B==n] = symbols[n]
    print B

    
#Read the probability values of each cell position from Game Stats.xlsx file
def readFromGameStatsFile():
    df = pd.read_excel('Game Stats.xlsx')
    probabilityMatrix = np.reshape(np.array(df.loc['Probability','(0,0)':'(2,2)'].tolist()),(-1,3))
    
    return probabilityMatrix
    

#Visualising the results as a bar chart
def plot_wins_and_draws(x,y):
    get_ipython().magic(u'matplotlib inline')
    plt.title('HISTOGRAM OF WINS AND DRAWS (Player X probabilistic)\n')
    plt.ylabel('Number of Matches')
    plt.grid(color='gray', linestyle='dashed',zorder=0)
    plt.bar(x,y,zorder=3,width=0.5)
    plt.savefig('1.1.2 Histogram (Player X probabilistic, Player O random).png')
    plt.show()    
    

if __name__ == '__main__':
    
    #counters for wins of player 1, player 2 and draws
    winsPlayer1=0
    winsPlayer2=0
    draws=0
    
    #number of matches in the tournament
    numberOfGames = 10000
   
    probabilityMatrix = readFromGameStatsFile()
    
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
                gameState = move_with_probability(gameState,player,probabilityMatrix)
                
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
                noWinnerYet = False
            

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


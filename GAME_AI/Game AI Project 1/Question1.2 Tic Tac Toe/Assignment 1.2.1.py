
# coding: utf-8

# In[2]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def move_still_possible(S):
    #print S[S==0]
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


# relate numbers (1, -1, 0) to symbols ('x', 'o', ' ')
symbols = {1:'x', -1:'o', 0:' '}

# print game state matrix using symbols
def print_game_state(S):
    B = np.copy(S).astype(object)
    for n in [-1, 0, 1]:
        B[B==n] = symbols[n]
    return B


#function to find out the cell positions that resulted in a win from the entire game board.
#returns only the winning 3  cell positions as 1 and the rest of the board as 0
def populate_game_stats(S):
    
    found=False
    
    for row in range(3):
        if((len(set(S[row]))==1) and (np.sum(S[row])!=0)):
            S[row]=2
            found = True
    
    if(found == False):
        for col in range(3):
            if((len(set(S[:,col]))==1) and (np.sum(S[:,col])!=0)):
                S[:,col]=2
                found = True
    
    if(found == False):
        if(len(set(np.diag(S)))==1):
            np.fill_diagonal(S,2)   
            found = True
    
    if(found == False):
        if(len(set(np.diag(np.rot90(S))))==1):
            np.fill_diagonal(np.rot90(S),2)
    
    S[S<2]=0
    S[S==2]=1
    return S


#function to collect game stats as an element in a list
def analysis_of_game_data(S,p,X):
    currGame=[p,X]
    if p==1:
        currGame.extend(populate_game_stats(S).flatten().tolist())
    else:
        S = (-1)*S
        currGame.extend(populate_game_stats(S).flatten().tolist())
        
    return currGame


#calculate probabilities for each cell from the game stats collected over all matches
def calculate_probabilities(S):
    
    #Initializing dataframe to capture game stats
    df = pd.DataFrame(S,columns=['Game Won By Player','Game Board','(0,0)','(0,1)','(0,2)','(1,0)','(1,1)','(1,2)','(2,0)','(2,1)','(2,2)'])
    
    #number of games in the tournament that resulted in a win for either player
    noOfWinningGames=df.shape[0]
    
    #sum of counts of all cell positions in each game that resulted in a win
    sumOfCounts=(df.loc[:, '(0,0)':'(2,2)'].sum())
    
    #probability of occurence of each cell in a winning configuration
    # = (total count in all winning configurations)/(total number of cells in all games of the tournament that resulted in a win)
    probabilityOfPosition=(df.loc[:,'(0,0)':'(2,2)'].sum())/(3*noOfWinningGames)
    
    #add total and probability as rows to the dataframe to be stored in an excel file
    df.loc['Total']= sumOfCounts
    df.loc['Probability']= probabilityOfPosition
    
    write_to_excel(df)
    
    #extracting the probabilities (auspiciousness) of each cell from the dataframe
    probabilityMatrix = np.reshape(np.array(df.loc['Probability','(0,0)':'(2,2)'].tolist()),(-1,3))
    
    return (probabilityMatrix)



#writing the game stats to Game Stats.xlsx file    
def write_to_excel(S):
    
    writer = pd.ExcelWriter('Game Stats.xlsx')
    S.to_excel(writer,'Sheet1')
    writer.save()

    

#Visualising the results in a bar chart
def plot_wins_and_draws(x,y):
    get_ipython().magic(u'matplotlib inline')
    plt.title('HISTOGRAM OF WINS AND DRAWS (Both Players move randomly)\n')
    plt.ylabel('Number of Matches')
    plt.grid(color='gray', linestyle='dashed',zorder=0)
    plt.bar(x,y,zorder=3,width=0.5)
    plt.savefig('1.1.1 Histogram (Players move randomly).png')
    plt.show()
    
    
if __name__ == '__main__':
    
    #counters for wins of player 1, player 2 and draws
    winsPlayer1=0
    winsPlayer2=0
    draws=0
    
    #gameData stores stats of each match in the tournament
    gameData = list()          
    
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

            # let player move at random
            gameState = move_at_random(gameState, player)
            

            # print current game state
            print_game_state(gameState)
        
            # evaluate game state
            if move_was_winning_move(gameState, player):
                #print 'player %s wins after %d moves' % (name, mvcntr)
                noWinnerYet = False
                
                #if player X wins, increment counter winsPlayer1
                if name == 'x':
                    winsPlayer1=winsPlayer1+1
                
                #if player O wins, increment counter winsPlayer2
                else:
                    winsPlayer2=winsPlayer2+1
                
                gameData.append(analysis_of_game_data(gameState,player,print_game_state(gameState)))
                

            # switch player and increase move counter
            player *= -1
            mvcntr +=  1

        if noWinnerYet:
            #print 'game ended in a draw'
            #if match ends in a draw, increment counter draws
            draws=draws+1
    
    
    #Call function to use tournament statistics to calculate cell probabilities returned as a 2D array
    probabilityMatrix = calculate_probabilities(gameData)
    
    #print the probabilities for each cell of tic-tac-toe board
    print 'The auspiciousness of each tic-tac-toe board cell is as follows:\n'
    print probabilityMatrix
    
    #x stores the labels and y stores the frequencies of wins and draws
    x=['Wins by Player 1','Wins by Player 2','Draws'] 
    y=[winsPlayer1,winsPlayer2,draws]           
    
    #plotting the frequencies in a bar chart
    plot_wins_and_draws(x,y)



import copy as cp
import numpy as np

#Class to collect game Statistics
class Count:
    def __init__(self):
        self.noOfPlayer1Wins = 0
        self.noOfPlayer2Wins = 0
        self.noOfDraws = 0
        self.noOfNodesTraversed = 1
        self.noOfBranches = []

count = Count();

#Prints the game board
def print_game_state(S):
    B = np.copy(S).astype(object)
    for n in [-1, 0, 1]:
        B[B==n] = symbols[n]
    print B


#Variable to store already seen board configurations and their symmetrical variants (through reflection and rotation)
configs = []

#Adding seen board configurations and their symmetrical variants into configs list
def add_symmetries(gameState):
    configs.append(gameState)
    configs.append(np.rot90(gameState))
    configs.append(np.rot90(np.rot90(gameState)))
    configs.append(np.rot90(np.rot90(np.rot90(gameState))))
    configs.append(np.flip(gameState,0))
    configs.append(np.flip(gameState,1))
    configs.append(np.flip(np.rot90(gameState),0))
    configs.append(np.flip(np.rot90(gameState),1))
    

#Checks if there are any empty cells remaining on board        
def move_still_possible(S):
    return not (S[S==0].size == 0)

#Places player p's move randomly on the board at a free cell
def move_at_random(S, p):
    xs, ys = np.where(S==0)

    i = np.random.permutation(np.arange(xs.size))[0]
    
    S[xs[i],ys[i]] = p

    return S

#Checks whether p's last move resulted in a win or not
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



#Generates the entire game tree
def generate_game_tree(player, board, depth=0):
    
    depth += 1
    new_board = np.copy(board)
    xs, ys = np.where(board==0)
    
    #If a winning move is found, add 1 to the respective player's wins and return
    
    if move_was_winning_move(board,player*(-1)):    
        #(count.noOfBranches).append(0)
        if(player*(-1) == 1):
            count.noOfPlayer1Wins += 1
        else:
            count.noOfPlayer2Wins += 1
        return
    
    #If there are no more empty spaces on board, add 1 to the count of games drawn
    
    elif len(xs) == 0:
        count.noOfDraws += 1
        return
    (count.noOfBranches).append(len(xs))

    
    #Expand each node only if it (or it's symmetric variants) has not been previously expanded  
    
    for i in range(len(xs)):        
        new_board[xs[i],ys[i]] = player
        if (not any(np.array_equal(new_board, j) for j in configs)):
            count.noOfNodesTraversed += 1
            add_symmetries(cp.deepcopy(new_board))
            generate_game_tree(player*(-1), new_board, depth)
        new_board[xs[i],ys[i]] = 0        
       
    


if __name__ == '__main__':
    
    # initialize 3x3 tic tac toe board
    gameState = np.zeros((3,3), dtype=int)
    
    # initialize player number, move counter
    player = 1
    
    generate_game_tree(player,gameState)

print "No. of player 1 wins: ",count.noOfPlayer1Wins
print "No. of player 2 wins: ",count.noOfPlayer2Wins
print "No. of draws: ",count.noOfDraws
print "No. of nodes traversed: ",count.noOfNodesTraversed
print "Average branching factor: ",sum(count.noOfBranches)/len(count.noOfBranches)


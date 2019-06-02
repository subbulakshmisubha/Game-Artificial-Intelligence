import numpy as np


class Tree(object):
    def __init__(self, name, value, children=None, lookahead=None):
        self.name = name
        self.value = value
        self.children = children or []
        self.lookahead = lookahead
        for child in self.children:
            child.parent = self

#Function to check if multiple child nodes have the same minimax value         
def is_duplicate_value(minimax_values, m):
    return len([i for i,x in enumerate(minimax_values) if x==m])>1


#Function for calculating mmv of root nodes for user defined trees. The next best move is stored in the variable next_move.
#If lookahead argument is true, function also keeps track of the worst value amongst child nodes from current node's perspective (This value is the best value from the opponent's perspective). 
def minimax_for_tree(gameState, is_max_turn=True, lookahead = False, depth=0):
    
    global next_move
    depth += 1
    tree=gameState
    if(tree.children == []):
        return tree.value
    else:
        minimax_values = []
        for child in tree.children:
            
            minimax_values.append(minimax_for_tree(child , not is_max_turn))
            
            if(is_max_turn):
                tree.value=max(minimax_values)
                
                if(lookahead):
                    tree.lookahead = min(minimax_values)
                    if (is_duplicate_value(minimax_values, max(minimax_values))):
                        duplicate_pos=[i for i,x in enumerate(minimax_values) if x==max(minimax_values)]
                        lookahead_values = []
                        for i in duplicate_pos:
                            lookahead_values.append(tree.children[i].lookahead)
                        next_move = tree.children[np.argmax(lookahead_values)].name
                        return tree.value
                next_move = tree.children[np.argmax(minimax_values)].name   
            
            else:
                tree.value=min(minimax_values)                
                
                if(lookahead):
                    tree.lookahead = max(minimax_values)
                    if (is_duplicate_value(minimax_values, max(minimax_values))):
                        duplicate_pos=[i for i,x in enumerate(minimax_values) if x==min(minimax_values)]
                        lookahead_values = []
                        for i in duplicate_pos:
                            lookahead_values.append(tree.children[i].lookahead)
                        next_move = tree.children[np.argmin(lookahead_values)].name
                        return tree.value
                next_move = tree.children[np.argmin(minimax_values)].name
        
    return tree.value
    

if __name__ == '__main__':
    
    
    tree1 = Tree("node0",None,[
    Tree("node1",None,[Tree("node6",15),Tree("node7",20),Tree("node8",1),Tree("node9",3)]),
    Tree("node2",None,[Tree("node10",3),Tree("node11",4)]),
    Tree("node3",None,[Tree("node12",15),Tree("node13",10)]),
    Tree("node4",None,[Tree("node14",16),Tree("node15",4),Tree("node16",12)]),
    Tree("node5",None,[Tree("node17",15),Tree("node18",12),Tree("node19",8)])
    ])

    value = minimax_for_tree(tree1)
    print "The mmv value for node0 of Tree 1 is : ",value," and the next move is ",next_move 
    
    tree2 = Tree("node0",None,[
    Tree("node1",None,[Tree("node5",18),Tree("node6",6),Tree("node7",16),Tree("node8",6),Tree("node9",5)]),
    Tree("node2",None,[Tree("node10",7),Tree("node11",1)]),
    Tree("node3",None,[Tree("node12",16),Tree("node13",16),Tree("node14",5)]),
    Tree("node4",None,[Tree("node15",10),Tree("node16",2)]),
    ])
        
    value = minimax_for_tree(tree2)
    print "The mmv value for node0 of Tree 2 is : ",value," and the next move is ",next_move


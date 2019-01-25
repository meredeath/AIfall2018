import random

''' Layout positions:
0 1 2
3 4 5
6 7 8
'''
# Best future states according to the player viewing this board
ST_X = 1  # X wins
ST_O = 2  # O wins
ST_D = 3  # Draw

Wins = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]

AllBoards = {}   # This is primarily for debugging: key = layout, value = BoardNode

class BoardNode:
    
    def __init__(self, layout):
        self.layout = layout
        self.mover = 'x' if layout.count('x') == layout.count('o') else 'o'
        
        self.state = BoardNode.this_state(layout) # if final board, then ST_X, ST_O or ST_D, else None
        if self.state is None:
            self.best_final_state = None           # best achievable future state: ST_X, ST_O or ST_D
            self.best_move = None                  # 0-9 to achieve best state
            self.num_moves_to_final_state = None   # number of moves to best state
        else:
            self.best_final_state = self.state
            self.best_move = -1
            self.num_moves_to_final_state = 0
        
        self.children = list()
        
    def print_me(self):
        print('layout:',self.layout)
        print('mover:',self.mover)
        print('state:',BoardNode.str_state(self.state))
        print('best_final_state:',BoardNode.str_state(self.best_final_state))
        print('best_move:',self.best_move,BoardNode.str_move(self.best_move))
        print('num_moves_to_final_state:',self.num_moves_to_final_state)
        print('children:',self.children)
    
    def print_layout(self):
        print('%s\n%s\n%s' % (' '.join(self.layout[0:3]),' '.join(self.layout[3:6]),' '.join(self.layout[6:9])))
        
    # =================== class methods  =======================
    def str_state(state):
        # human description of a state
        return 'None' if state is None else ['x wins','o wins','draw'][state-1]
        
    def str_move(move):
        # human description of a move
        moves = ('top-left','top-center','top-right',\
                 'middle-left','middle-center','middle-right',\
                 'bottom-left','bottom-center','bottom-right')
        if move == -1:
            return 'done'
        elif move == None:
            return "None"
        else:
            return moves[move]
        
    def this_state(layout):
        # classifies this layout as None if not final, otherwise ST_X or ST_O or ST_D
        for awin in Wins:
            if layout[awin[0]] != '_' and layout[awin[0]] == layout[awin[1]] == layout[awin[2]]:
                return ST_X if layout[awin[0]] == 'x' else ST_O
        if layout.count('_') == 0:
            return ST_D
        return None

def CreateAllBoards(layout):
    # Populate AllBoards with finally calculated BoardNodes
    if layout in AllBoards:
        return
    
    anode = BoardNode(layout)
    # if this is an end board, then all of its properties have already been calculated by __init__()
    if anode.state is not None:
        AllBoards[layout] = anode
        return
    
    # expand children if this is not a final state
    if layout.count('x') == layout.count('o'):
        move = 'x'
    else:
        move = 'o'
    for pos in range(9):
        if layout[pos] != '_':
            anode.children.append(None)
        else:
            new_layout = layout[:pos] + move + layout[pos+1:]
            if new_layout not in AllBoards:
                CreateAllBoards(new_layout)
            anode.children.append(new_layout)

    # ==============================================================================
    # Your excellent code here to calculate the BoardNode properties below for this node
    print("==========\n\ncurrent node info, before calculating stuff: ")
    anode.print_me()
    
    anode.num_moves_to_final_state = 0
    #keeping track of which index move you are in to calculate best move
    counter = 0 
    #look through all 9 possible children
    while counter < 9:
        cur = anode.children[counter]
        '''
        print("parent: " + layout)
        if cur != None:
            print("child of parent (input): " + cur)
        else:
            print("None")
        '''
        #has to be a position that you can place your move in
        if cur != None:  
            
            #if the child is an end state
            if AllBoards[cur].state is not None:
                #print("child is an end state! " + cur)
                #print("child's state: " + str(AllBoards[cur].state))
                anode.best_final_state = AllBoards[cur].state #set best final state of current node to state of winning child node
                anode.best_move = counter #best move is the child you are on right now
                anode.num_moves_to_final_state += 1
                #print("num moves to final: " + str(anode.num_moves_to_final_state))
                #break bc we don't need to check other children
                print("\nnode info after calculating things, if immediate child turns out to be an end state: ")
                anode.print_me()
                break
            
            #if no immediate children lead to your mover winning or a draw, check the children of the children until you run into a win
            else:
                #print("num_moves now: " + str(anode.num_moves_to_final_state))
                #anode.num_moves_to_final_state += 1

                #set your best move to your child's best move because you'd prevent the other side from winning, if you're not one move away from winning yourself.
                anode.best_move = AllBoards[cur].best_move
                if move == 'x':
                    win = 1
                else:
                    win = 2
                #check children of children for win state match or draw
                winfound = False
                c2 = 0
                while c2 < 9 and winfound == False:
                    childnode = AllBoards[cur]
                    #cur2 is a layout once again
                    cur2 = childnode.children[c2]
                    if cur2 != None:
                        
                        #if cur2 node's state matches with the win state we are looking for or is a draw
                        if AllBoards[cur2].state == win or AllBoards[cur2].state == ST_D:
                            anode.best_final_state = AllBoards[cur2].state
                            winfound == True
                            
                        #we can't win
                        else:
                            anode.best_final_state = AllBoards[cur2].best_final_state
                            #print("num_moves now: " + str(anode.num_moves_to_final_state))
                            #anode.num_moves_to_final_state += 1
                    c2 += 1
                #print("num_moves now: " + str(anode.num_moves_to_final_state))
                anode.num_moves_to_final_state += 1
                #print("num_moves now after adding 1: " + str(anode.num_moves_to_final_state))
                
                print("\nthat node's info after calculating the things if there was no end state in the immediate children: ")
                anode.print_me()
        counter += 1
    # ===============================================================================
    
    
    AllBoards[layout] = anode
    
#  Test me here...

AllBoards = {}
print('x should win this one in 3 moves')
b='x_o_o___x'
CreateAllBoards(b)
AllBoards[b].print_me()
AllBoards[b].print_layout()

'''
AllBoards = {}
b='x__xoxo__'
print('\no should win this one in 1 move')
CreateAllBoards(b)
AllBoards[b].print_me()
AllBoards[b].print_layout()


AllBoards = {}
b='_________'
print('\nthis should be a draw in 9 moves')
CreateAllBoards(b)
AllBoards[b].print_me()
AllBoards[b].print_layout()
'''

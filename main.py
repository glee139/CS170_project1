import time
import copy
# https://www.programiz.com/python-programming/time
# https://docs.python.org/3/library/time.html
# https://docs.python.org/3/tutorial/classes.html
# https://www.geeksforgeeks.org/copy-python-deep-copy-shallow-copy/

class Node:
    def __init__(self, state):
        self.child0 = None # blank moves up
        self.child1 = None #blank moves down
        self.child2 = None #blank moves left
        self.child3 = None #blank moves right
        self.depth = 0
        self.cost = 0
        self.state = state

goal = [['1','2','3'],['4','5','6'],['7','8','0']]
coord = [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]] # coordinates of the goal state

nodesExp = 0 #everytime we append to queue add 1
qSize = 0 #len of queue
max = 0 #compare with max to track biggest queue size

def main():
    problem = chooseBoard()
    search = chooseSearch(problem)
    UniformSearch(problem, search)


#which board does the user want to solve
def chooseBoard():
    boardNumber = input("Choose the board that you would like to solve(0-7) or choose '8' to create your own: ")
    while boardNumber != '0' and boardNumber != '1' and boardNumber != '2' and boardNumber != '3' and boardNumber != '4' and boardNumber != '5' and boardNumber != '6' and boardNumber != '7' and boardNumber != '8':
        print("Try again")
        boardNumber = input("Choose the board that you would like to solve(0-7) or choose '8' to create your own: ")

    if boardNumber == '0':
        board = [['1','2','3'],['4','5','6'],['7','8','0']] #depth 0
    elif boardNumber == '1':
        board = [['1','2','3'],['4','5','6'],['0','7','8']] #depth 2
    elif boardNumber == '2':
        board = [['1','2','3'],['5','8','6'],['4','7','0']] #depth 4
    elif boardNumber == '3':
        board = [['1','3','6'],['5','8','2'],['4','7','0']] #depth 8
    elif boardNumber == '4':
        board = [['1','3','6'],['5','0','7'],['4','8','2']] #depth 12
    elif boardNumber == '5':
        board = [['1','6','7'],['5','0','3'],['4','8','2']] #depth 16
    elif boardNumber == '6':
        board = [['7','1','2'],['4','8','5'],['6','3','0']] #depth 20
    elif boardNumber == '7':
        board = [['0','7','2'],['4','6','1'],['3','5','8']] #depth 24
    elif boardNumber == '8':
        customRow1 = input("Enter row 1 with spaces in between each number: ")
        customRow2 = input("Enter row 2 with spaces in between each number: ")
        customRow3 = input("Enter row 3 with spaces in between each number: ")

        customRow1 = (customRow1.split())
        customRow2 = (customRow2.split())
        customRow3 = (customRow3.split())

        board = [customRow1, customRow2, customRow3]
    printBoard(board)
    return board


#user chooses which search to do
# 1 - Uniform, 2 - Manhatten, 3 - Misplaced
def chooseSearch(board):
    search = input('Which search would you like to implement?\n1: Uniform Search\n2: Manhattan Search\n3: Tile Search\nInput: ')
    while search != '1' and search != '2' and search != '3':
        print('Try again')
        search = input('Which search would you like to implement?\n1: Uniform Search\n2: Manhattan Search\n3: Tile Search\nInput: ')
    return search

#print baord
def printBoard(board):
    for i in range(0,3):
        for y in range(0,3):
            print(board[i][y], end = ' ')
        print('')
    print('')


#gets the different ways that the blank can move
def getChildren(node):
    children = []
    board = node.state
    r = 0
    c = 0
    #find the indices for '0'
    for i in range(0,3):
        for j in range(0,3):
            if board[i][j] == '0':
                r = i
                c = j
    
    #0 move right
    if c !=2:
        #create new Node
        rightChild =  Node(board)
        rightChild.depth = node.depth + 1
        rightChild.cost = node.cost +1

        child = copy.deepcopy(node.state) # make copy of parent node
        #swap
        temp = child[r][c]
        child[r][c] = child[r][c+1]
        child[r][c+1] = temp

        #assign the new Node updated board
        rightChild.state = child
        #assign child
        node.child3 = rightChild
        children.append(rightChild)
    
    #0 move left
    if c !=0:
        leftChild =  Node(board)
        leftChild.depth = node.depth + 1

        child = copy.deepcopy(node.state) # make copy of parent node
        #swap
        temp = child[r][c]
        child[r][c] = child[r][c-1]
        child[r][c-1] = temp

        #assign the new Node updated board
        leftChild.state = child
        #assign child
        node.child2 = child
        children.append(leftChild)
    
    #0 move up
    if r !=0:
        upChild = Node(node)
        upChild.depth = node.depth + 1

        child = copy.deepcopy(node.state) # make copy of parent node
        #swap
        temp = child[r][c]
        child[r][c] = child[r-1][c]
        child[r-1][c] = temp

        #assign the new Node updated board
        upChild.state = child
        #assign child
        node.child0 = child
        children.append(upChild)

    #0 move down
    if r !=2:
        downChild = Node(node)
        downChild.depth = node.depth + 1

        child = copy.deepcopy(node.state) # make copy of parent node
        #swap
        temp = child[r][c]
        child[r][c] = child[r+1][c]
        child[r+1][c] = temp

        #assign the new Node updated board
        downChild.state = child
        #assign child
        node.child1 = child
        children.append(downChild)

    return children


#Breadth First Search - A* g(n) + h(n) where h(n) = 0
def UniformSearch(board,search):
    timestart = time.time()
    #initialize variables
    start = Node(board)
    start.cost = 1
    queue = []
    done = []
    min = 100

    #root node
    queue.append(start)
    while len(queue) > 0:
        node = queue.pop(0)
        done.append(node)
        
        if node.state == goal:
            print('Goal State!')
            print('Solution Depth was ' + str(node.depth))
            print('Number of nodes expanded: ' + str(nodesExp))
            print('Max queue size: ' + str(qSize))
            print('Time taken is ' + str(f'{(time.time() - timestart):.2f}') + ' secs')
            return node
        else:
            printBoard(node.state)
            children = getChildren(node)
            children[:] = [x for x in children if x not in done]
            if search == '1':
                for i in children:
                    queue.append(i)
            elif search == '2': 
                for i in children:
                    heuristic = ManhattanSearch(i)
                    i.cost = heuristic
            elif search == '3':
                for i in children:
                    heuristic = TileSearch(i)
                    i.cost = heuristic

            #find index of min heurestic
            if search != '1':
                for i in children:
                    if int(i.cost) < min:
                        minchild = i
                        min = i.cost
                print('The best state to expand with a g(n) = ' + str(minchild.depth) + ' and h(n) = ' + str(minchild.cost) + ' is: ')
                queue.append(minchild)
    

def ManhattanSearch(node):
    #calculate the h(n)
    board = node.state
    manhattan = 0
    for i in range(0,3):
        for j in range(0,3):
            if board[i][j] != goal[i][j] and board[i][j] != '0':
                value = int(board[i][j])
                manhattan += (abs(i-coord[value-1][0]) + abs(j-coord[value-1][1]))
    return manhattan
    

def TileSearch(node):
    #calculate h(n)
    board = node.state
    misplaced = 0
    for i in range(0,3):
        for j in range(0,3):
            if board[i][j] != goal[i][j]:
                misplaced +=1
    if(board[2][2] != '0'):
        misplaced -=1
    return misplaced

if __name__ == "__main__":
    main()

import pygame
import random
import time
import math
import sys

sys.setrecursionlimit(20000)

pygame.init()

width = 640
height = 660
display = pygame.display.set_mode((width, height))

green = (0, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

gameOn = True
userMove = True

count = 400

whiteScore = 2
blackScore = 2

board = [["*", "*", "*", "*", "*", "*", "*", "*"], ["*", "*", "*", "*", "*", "*", "*", "*"], ["*", "*", "*", "*", "*", "*", "*", "*"], ["*", "*", "*", "W", "B", "*", "*", "*"], ["*", "*", "*", "B", "W", "*", "*", "*"], ["*", "*", "*", "*", "*", "*", "*", "*"], ["*", "*", "*", "*", "*", "*", "*", "*"], ["*", "*", "*", "*", "*", "*", "*", "*"]]
weights = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 120, -20, 20, 20, -20, 120, 0], [0, -20, -40, -5, -5, -40, -20, 0], [0, 20, -5, 3, 3, -5, 20, 0], [0, 20, -5, 3, 3, -5, 20, 0], [0, -20, -40, -5, -5, -40, -20, 0], [0, 120, -20, 20, 20, -20, 120, 0], [0, 0, 0, 0, 0, 0, 0, 0],]

weights1D = []
for l in weights:
    for num in l:
        weights1D.append(num)

maxValue = sum(map(abs, weights1D))
minValue = -maxValue

def final(board, player):
    diff = calculateScore(board, player)
    if diff < 0:
        return minValue
    elif diff > 0:
        return maxValue
    return diff

def showText(msg, x, y, color):
    font = pygame.font.SysFont(None, 25)
    text = font.render(msg, False, color)
    display.blit(text, [x, y])

def calculateScore(board, player):
    score = 0
    for i in board:
        for j in i:
            if j == player:
                score = score+1
    return score   

def weightedScore(board, player):
        opponent = "*"
        if player == "B":
            opponent = "W"
        else:
            opponent = "B"
        
        total = 0
        for i in range(0, 7):
            for j in range(0, 7):
                if j == player:
                    total += weights[i][j]
                if j == opponent:
                    total -= weights[i][j]
        return total     

def checkValid(row, col, board, player):
    directions = ["N", "E", "S", "W"]
    
    if board[row][col] == "B" or board[row][col] == "W":
        return False

    opponent = "*"
    if player == "B":
        opponent = "W"
    else:
        opponent = "B"

    for dir in directions:
        if dir == "N":
            end = row-1
            while end > 0 and board[end][col] == opponent:
                end = end-1
            if end != row-1 and end >= 0 and board[end][col] == player:
                return True
        if dir == "S":
            end = row+1
            while end < 7 and board[end][col] == opponent:
                end = end+1
            if end != row+1 and end < 8 and board[end][col] == player:
                return True
        if dir == "E":
            end = col+1
            while end < 7 and board[row][end] == opponent:
                end = end+1
            if end != col+1 and end < 8 and board[row][end] == player:
                return True
        if dir == "W":
            end = col-1
            while end > 0 and board[row][end] == opponent:
                end = end-1
            if end != col-1 and end >= 0 and board[row][end] == player:
                return True
    return False  

def flip(row, col, board, player):
    directions = ["N", "E", "S", "W"]
    
    opponent = "*"
    if player == "B":
        opponent = "W"
    else:
        opponent = "B"

    for dir in directions:

        if dir == "W":
            end = row-1
            while end > 0 and board[end][col] == opponent:
                end = end-1
            if end > 0 and board[end][col] == player:
                for i in range(end, row):
                    board[i][col] = player

        if dir == "E": 
            end = row+1
            while end < 7 and board[end][col] == opponent:
                end = end+1
            if  end < 7 and board[end][col] == player:
                for i in range(row, end):
                    board[i][col] = player

        if dir == "S":
            end = col+1
            while end < 7 and board[row][end] == opponent:
                end = end+1
            if end < 7 and board[row][end] == player:
                for i in range(col, end+1):
                    board[row][i] = player
        
        if dir == "N":
            end = col-1
            while end > 0 and board[row][end] == opponent:
                end = end-1
            if end > 0  and board[row][end] == player:
                for i in range(end, col):
                    board[row][i] = player

    return board

def movePossible(userMove, board):
    player = "*"
    if userMove:
        player = "W"
    else:
        player = "B"
    
    for i in range(0, 7):
        for j in range(0, 7):
            if board[i][j] == "*" and checkValid(i, j, board, player):
                return True
    
    return False

def randomMove(board, player):

    row = random.randrange(0, 7)
    col = random.randrange(0, 7)

    while not checkValid(row, col, board, player):
        row = random.randrange(0, 7)
        col = random.randrange(0, 7)

    return (row, col)

def maximizeMove(board, player):
    newB = []
    for x in range(0, 7):
        newB.append([])
        for y in range(0, 7):
            newB[x].append(board[x][y])

    potentialBoards = []
    potentialCoords = []
    for i in range(0, 7):
        for j in range(0, 7):
            if checkValid(i, j, board, player):
                potentialBoards.append(flip(i, j, newB, player))
                potentialCoords.append((i, j))

    maxIndex = 0
    for i in range(0, len(potentialBoards)-1):
        maxScore = calculateScore(potentialBoards[maxIndex], player)
        score = calculateScore(potentialBoards[i], player)
        
        if score > maxScore:
            maxIndex = i

    if len(potentialBoards) == 0:
        return (-1, -1)
    return potentialCoords[maxIndex]

def maximizeWithWeights(board, player):
    newB = []
    for i in range(0, 7):
        newB.append([])
        for j in range(0, 7):
            newB[i].append(board[i][j])

    potentialBoards = []
    potentialCoords = []
    for i in range(0, 7):
        for j in range(0, 7):
            if checkValid(i, j, board, player):
                potentialBoards.append(flip(i, j, newB, player))
                potentialCoords.append((i, j))

    maxIndex = 0
    for i in range(0, len(potentialBoards)-1):
        maxScore = weightedScore(potentialBoards[maxIndex], player)
        score = weightedScore(potentialBoards[i], player)
        
        if score > maxScore:
            maxIndex = i

    if len(potentialBoards) == 0:
        return (-1, -1)
    return potentialCoords[maxIndex]

def minimaxMove(board, player):
    newB = []
    for i in range(0, 7):
        newB.append([])
        for j in range(0, 7):
            newB[i].append(board[i][j])

    def minimax(player, board, depth, evaluate):
        opponent = "*"
        if player == "B":
            opponent = "W"
        else:
            opponent = "W"
        
        def value(board):
            return -minimax(opponent, board, depth-1, evaluate)[0]

        if depth == 0:
            return (evaluate(board, player), None)

        moves = []
        for i in range(0, 7):
            for j in range(0, 7):
                if checkValid(i, j, board, player):
                    moves.append((i, j))

        if not moves:
            return (final(player, board), None)

        return max((value(flip(m[0], m[1], newB, player)), m) for m in moves)

    depth = 3

    return minimax(player, board, depth, weightedScore)[1]

def alphaBetaMove(board, player):
    newB = []
    for i in range(0, 7):
        newB.append([])
        for j in range(0, 7):
            newB[i].append(board[i][j])

    def alphaBeta(board, player, alpha, beta, depth, evaluate):
        opponent = "*"
        if player == "B":
            opponent = "W"
        else:
            opponent = "W"

        def value(board, alpha, beta):
            return -alphaBeta(board, player, alpha, beta, depth, evaluate)[0]

        if depth == 0:
            return (evaluate(newB, player), None)

        moves = []
        for i in range(0, 7):
            for j in range(0, 7):
                if checkValid(i, j, board, player):
                    moves.append((i, j))

        if not moves:
            return (final(player, board), None)

        bestMove = moves[0]
        for m in moves:
            if alpha >= beta:
                break

            val = value(flip(m[0], m[1], newB, player), alpha, beta)

            if val < alpha:
                alpha = val
                bestMove = m

        return (alpha, bestMove)

    depth = 4
    return alphaBeta(board, player, minValue, maxValue, depth, weightedScore)[1]
        
while gameOn:
    pygame.event.get()
    display.fill(black)

    pygame.draw.rect(display, green, [0, 640, 640, 20])
    showText("Score: " + str(whiteScore), 5, 645, white)
    showText("Score: " + str(blackScore), 560, 645, black)


    for i in range(0, width, 80):
        for j in range(0, height-20, 80):
            pygame.draw.rect(display, green, [i+2, j+2, 76, 76])

    for i in range(0, 8):
        for j in range(0, 8):
            if board[i][j] == "B":
                pygame.draw.circle(display, black, (i*80+40, j*80+40), 30)
            if board[i][j] == "W":
                pygame.draw.circle(display, white, (i*80+40, j*80+40), 30)
    
    gameOn = movePossible(userMove, board)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOn = False
        if event.type == pygame.MOUSEBUTTONUP and userMove and gameOn:
            loc = pygame.mouse.get_pos()
            row = int(loc[0]/80)
            col = int(loc[1]/80)
            valid = checkValid(row, col, board, "W")

            if valid:
                board[row][col] = "W"
                pygame.draw.circle(display, white, (row*80+40, col*80+40), 30)
                board = flip(row, col, board, "W")
                whiteScore = calculateScore(board, "W")
                blackScore = calculateScore(board, "B")
                count = 400
                userMove = False
    
    gameOn = movePossible(userMove, board)
    
    if not userMove:
        count = count - 1

    if not userMove and gameOn and count < 0:
        #random
        """
        coord = randomMove(board, "B")
        if coord != None:  
            row = coord[0]
            col = coord[1]
            board[row][col] = "B"
            pygame.draw.circle(display, black, (row*80+40, col*80+40), 30)
            board = flip(row, col, board, "B")
            whiteScore = calculateScore(board, "W")
            blackScore = calculateScore(board, "B")
            userMove = True
        """

        #local maximization
        
        coord = maximizeMove(board, "B")
        #coord = maximizeWithWeights(board, "B")
        if coord != None:  
            row = coord[0]
            col = coord[1]
            board[row][col] = "B"
            pygame.draw.circle(display, black, (row*80+40, col*80+40), 30)
            board = flip(row, col, board, "B")
            whiteScore = calculateScore(board, "W")
            blackScore = calculateScore(board, "B")
            userMove = True
        

        #minimax search
        """
        coord = minimaxMove(board, "B")
        if coord != None:  
            row = coord[0]
            col = coord[1]
            board[row][col] = "B"
            pygame.draw.circle(display, black, (row*80+40, col*80+40), 30)
            board = flip(row, col, board, "B")
            whiteScore = calculateScore(board, "W")
            blackScore = calculateScore(board, "B")
            userMove = True
        

        #alpha beta pruning
        
        coord = alphaBetaMove(board, "B")
        if coord != None:  
            row = coord[0]
            col = coord[1]
            board[row][col] = "B"
            pygame.draw.circle(display, black, (row*80+40, col*80+40), 30)
            board = flip(row, col, board, "B")
            whiteScore = calculateScore(board, "W")
            blackScore = calculateScore(board, "B")
            userMove = True
        """
    
    pygame.display.update()

while not gameOn:
    if whiteScore > blackScore:
        showText("White wins!", 20, 200, red)
    elif blackScore > whiteScore:
        showText("Black wins!", 20, 200, red)
    else:
        showText("Tie!", 20, 200, red)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOn = True

pygame.quit()
quit()

import pygame
pygame.init()

class Spot(object):
    """
    value is an integer 0,9
    location is a tuple that represents the upper border
    """
    def __init__(self, value, x, y, selected=False):
        self.value = value
        self.x = x
        self.y = y
        self.selected = selected
        self.color = (255,255,255)
        self.filled = False
        self.correct = 2

    def pickTextColor(self):
        if(self.filled):
            return (0,0,0)
        else:
            return (255,0,255)

    def pickColor(self):
        if(self.selected):
            return (230,230,255)
        elif(not self.filled and self.correct == 1):
            return (220,255,220)
        elif(not self.filled and self.correct == 0):
            return (255,220,220)
        else:
            return (255,255,255)

    def setSelected(self, bool):
        self.selected = bool

    def setFilled(self, bool):
        self.filled = bool

    def setValue(self, inte):
        self.value = inte

    def setCorrect(self, bool):
        self.correct = True

    def draw(self, win):
        pygame.draw.rect(win, self.pickColor(), (self.x,self.y,WIDTH,WIDTH), 0)
        if (self.value > 0):
            doText(win, str(self.value), self.pickTextColor(), (self.x + 37.5 - (font.size(str(self.value)))[0]), self.y)

    def __str__(self):
        return str(self.value) + "AT (" + str(self.x) + ", " + str(self.y) + ")"


# Draws the entire board when passed a puzzle board
def drawBoard(board,win):
    for row in range(9):
        for col in range(9):
            curSpot = board[row][col]
            curSpot.draw(win)

def doText(win,msg,color, x, y):
    screen_text = font.render(msg, True, color)
    win.blit(screen_text,(x,y))

# This is an empty board
def initBoard():
    board = []
    x = SIDE_MARGIN
    y = TOP_MARGIN
    for i in range(9):
        if (i % 3 == 0 and i != 0):
            y += MARGIN
        arr = []
        for j in range(9):
            if (j % 3 == 0 and j != 0):
                x += MARGIN
            new = Spot(0,x,y)
            arr.append(new)

            x += WIDTH + MARGIN

        board.append(arr)
        y += WIDTH + MARGIN
        x = SIDE_MARGIN

    return board

def generateSpots(board):
    fillSpots = []
    for row in range(9):
        for col in range(9):
            cur = board[row][col].value
            if(cur == 0):
                fillSpots.append((row,col))
    return fillSpots

def printBoard(board):
    for i in range(9):
        if (i % 3 == 0 and i != 0):
            print("-------------------------------")
        for j in range(9):
            if (j % 3 == 0 and j != 0):
                print("|", end=" ")
            print(str(board[i][j]) + " ", end=" ")
        print()

def determineNum(board, row, col, start):
    for i in range(start + 1, 10):
        if (checkValidity(board, i, row, col)):
            return i
    return -1

def gridCalc(loc):

    x = loc[0]
    y = loc[1]
    if(x < 9 or x > 455 or y < 100 or y > 550):
        return (-1,-1)
    else:
        x -= SIDE_MARGIN
        gridX = x // (MARGIN + WIDTH)

        y -= TOP_MARGIN
        gridY = y // (MARGIN + WIDTH)
        return (gridY, gridX)

def checkValidity(board, num, row, col):
    return validRow(board,row,num) and validCol(board, col, num) and validGrid(board, row, col, num)

def validRow(board,row,num):
    for i in range(9):
        if(board[row][i].value == num):
            return False
    return True

def validCol(board, col, num):
    for i in range(9):
        if (board[i][col].value == num):
            return False
    return True

def validGrid(board,row, col, num):
    adjRow = (row // 3) * 3
    adjCol = (col // 3) * 3

    for i in range(adjRow, adjRow + 3):
        for j in range(adjCol, adjCol + 3):
            if (board[i][j].value == num):
                return False

    return True

def solve(puzzle):
    fillSpots = generateSpots(puzzle)

    i = 0
    while i < len(fillSpots):
        c = 0
        status = determineNum(puzzle, fillSpots[i - c][0], fillSpots[i - c][1], puzzle[fillSpots[i - c][0]][fillSpots[i - c][1]].value)

        while(status == -1):
            puzzle[fillSpots[i - c][0]][fillSpots[i - c][1]].value = 0
            puzzle[fillSpots[i - c][0]][fillSpots[i - c][1]].correct = 0
            c += 1
            status = determineNum(puzzle, fillSpots[i - c][0], fillSpots[i - c][1], puzzle[fillSpots[i - c][0]][fillSpots[i - c][1]].value)


        puzzle[fillSpots[i - c][0]][fillSpots[i - c][1]].value = status
        puzzle[fillSpots[i - c][0]][fillSpots[i - c][1]].correct = 1
        drawBoard(board, WIN)

        # pygame.time.delay(100)
        pygame.display.update()

        i = i - c
        i = i + 1

def determineType(event):
    k = event.key
    if(k == pygame.K_1):
        return 1
    elif(k == pygame.K_2):
        return 2
    elif (k == pygame.K_3):
        return 3
    elif (k == pygame.K_4):
        return 4
    elif (k == pygame.K_5):
        return 5
    elif (k == pygame.K_6):
        return 6
    elif (k == pygame.K_7):
        return 7
    elif (k == pygame.K_8):
        return 8
    elif (k == pygame.K_9):
        return 9
    else:
        return -1

#Global Constants
SCREEN_LTH = 610
WIN = pygame.display.set_mode((SCREEN_LTH - 135, SCREEN_LTH))
WIDTH = 45
MARGIN = 5
TOP_MARGIN = 100
SIDE_MARGIN = 10


running = True
board = initBoard()
WIN.fill((169,169,169))

drawBoard(board,WIN)
hasSelected = False
selected = (-1,-1)
font = pygame.font.SysFont(None, 75)
pygame.draw.rect(WIN, (0,255,0), (SCREEN_LTH - 335 - MARGIN, MARGIN, 195,90), 0)
transX = (SCREEN_LTH - 335 - MARGIN) + (195 // 2) - (font.size("Solve")[0] // 2)
transY = (MARGIN) + (90 // 2) - (font.size("Solve")[1] // 2)
doText(WIN, "Solve",(255,255,255), transX, transY)


while running:
    drawBoard(board, WIN)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if(not hasSelected):
            if event.type == pygame.MOUSEBUTTONDOWN:
                loc = event.pos
                if(SCREEN_LTH - 335 - MARGIN < loc[0] < SCREEN_LTH - 145 - MARGIN and MARGIN + 90 > loc[1] > MARGIN):
                    solve(board)
                else:
                    loc = gridCalc(loc)
                    if(loc[0] > -1):
                        board[loc[0]][loc[1]].setSelected(True)
                        hasSelected = True
                        selected = loc
        else:
            if event.type == pygame.KEYDOWN:
                if(event.key == pygame.K_BACKSPACE or determineType(event) == -1):
                    board[selected[0]][selected[1]].setValue(0)
                    board[selected[0]][selected[1]].setSelected(False)
                    hasSelected = False
                    selected = (-1, -1)
                else:
                    board[selected[0]][selected[1]].setValue(determineType(event))
                    board[selected[0]][selected[1]].setFilled(True)
                    board[selected[0]][selected[1]].setSelected(False)
                    hasSelected = False
                    selected = (-1,-1)



pygame.quit()


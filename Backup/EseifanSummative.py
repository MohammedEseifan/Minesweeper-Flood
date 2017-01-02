                            # # # # # # # # # # # # # # #
                            # #      Minesweeper      # # 
                            # #  By: Mohammed Eseifan # # 
                            # # # # # # # # # # # # # # # 
from pygame import *
import random,math,os
init()

# Decalring fonts (must be before functions )
TEXTFONT  = font.Font("SLANT.TTF",30)
WARNINGFONT= font.Font("SLANT.TTF",20)
TITLEFONT= font.Font("GODOFWAR.TTF",50)
STATSFONT = font.Font("GODOFWAR.TTF",30)


###############Functions###############

# Returns if the number if positive or negative
def copysign(string,inverse = False):
    
    string = str(string)

    # If the number is negative then return -1
    if '-' in string:
        if inverse:
            return 1
        else:
            return -1
    else:
        if inverse:
            return -1
        else:
            return 1
    
# Returns the plural form of the text if the number is more than 1
def checkPlural(text,number):
    if number >0 and number <= 1:
        return text
    elif number > 1 or number ==0:
        return text+'s'
        
# Moves between Screens
def moveScreens(targetScreen):
    # Declaring all of the global varibles
    global endScreen,gameScreen,currentBgColour,boardRect,currentScreen,gameInProgress,buttonOrder
    
    endScreen.fill(ENDSCREENBG)

    if targetScreen == 'gameScreen':
        
        while gameScreenCoords[0] != 20:
            
            # Moving all of the screens to thier positions
            gameScreenCoords[0] += copysign(gameScreenCoords[0]-20,True)*screenSlideSpeed
            endScreenCoords[0]+= copysign(gameScreenCoords[0]-40,True)*screenSlideSpeed
            menuScreenCoords[0]+= copysign(gameScreenCoords[0]-20,True)*screenSlideSpeed
            optionScreenCoords[0]+= copysign(gameScreenCoords[0]-20,True)*screenSlideSpeed
           
            # Updating Screen
            mainScreen.fill(WHITE)
            gameScreen.fill(WHITE)
            updateScreens()
            
        # Updating Global varibles
        boardRect = Rect(addLists(boardCoords,gameScreenCoords),(boardSize*(tileSize + tileBuffer) ,boardSize*(tileSize + tileBuffer)))
        currentScreen = gameScreen
        gameInProgress = True
        timer = 0
        currentBgColour = WHITE
        
    elif targetScreen == 'endScreen':
        
        while endScreenCoords[0] != 0:
            
            # Moving all of the screens to thier positions
            gameScreenCoords[0] += copysign(endScreenCoords[0],True)*screenSlideSpeed
            endScreenCoords[0]+= copysign(endScreenCoords[0],True)*screenSlideSpeed
            menuScreenCoords[0]+= copysign(endScreenCoords[0],True)*screenSlideSpeed
            optionScreenCoords[0]+= copysign(endScreenCoords[0],True)*screenSlideSpeed
            
            # Updating Screen
            mainScreen.fill(WHITE)
            updateScreens()
            
        # Updating Global varibles
        currentScreen  = endScreen
        gameInProgress= False
        currentBgColour = ENDSCREENBG    
        
# Resets all the varibles to default

def updateScreens():
    gameScreen.blit(board,boardCoords)
    mainScreen.blit(gameScreen,gameScreenCoords)
    mainScreen.blit(endScreen,endScreenCoords)
    mainScreen.blit(menuScreen,menuScreenCoords)
    display.flip()
def resetGame():
    global gameOver, boardList, flagList, placedFlags, timer,win,clicks, buttons,buttonAnimations
    
    buttons = {}
    buttonAnimations = []
    flagList = []
    placedFlags = 0
    timer = 0  
    clicks = 0
    win = False
    gameOver = False
    boardList = setupBoard(boardSize,numMines)
    drawBoard(board, boardList, boardSize, tileSize, tileBuffer)
    moveScreens('gameScreen')
    
    
    

# Checks if the player has won
def checkWin():
    # Exit function is the game is over
    if gameOver:
        return 
    
    global win, gameOver,ENDSCREENBG
    win = True
    
    # Loops through every flag position
    for flagPos in flagList:
        # If there is no mine at the flag position then player has not won
        if boardList[flagPos[0]][flagPos[1]] != 'X':
            win = False
            
    # If player has won then show end screen       
    if win:
        ENDSCREENBG = BLUE
        showMines()
        gameOver = True
        moveScreens('endScreen')
        
        stats = ["It Took You "+timeToText(timer),"You Clicked "+str(clicks)+" " +checkPlural('Time',clicks)]
        drawEndScreen(endScreen,ENDSCREENBG,'YOU WIN',stats)      
        
# Makes explosion at given coordinates
def makeExplosion(x,y,speed):
    xSpeed = int(speed*1.5)
    # Makes 20 pieces of shrapnel
    for i in range(20):
        acelX = random.randint(xSpeed*-1,xSpeed)
        acelY = random.randint(speed*-1,speed)
        # Add the starting x,y and x,y aceleation to list
        explosions.append([[x,y],[acelX,acelY]])
        
        
    
# Returns the time in 00:00.00 format
def timeToString(frames):
    # Converting input into useful varibles
    rawTime = float(frames)/FPS
    minutes = int(rawTime/60)
    seconds = round(rawTime-minutes*60,1)
    
    # If the seconds is 1 digit then add a 0 to the beginning
    if len(str(int(seconds)))<2:
        seconds = '0'+str(seconds)
    # If the minutes is 1 digit then add a 0 to the beginning
    if len(str(minutes))<2:
        minutes = '0'+str(minutes)
        
    return str(minutes)+':'+str(seconds)


# Returns the time as Text (ex. 10 Minutes and 5.5 seconds)
def timeToText(frames):
    # Converting input into useful varibles
    rawTime = float(frames)/FPS
    minutes = int(rawTime/60)
    seconds = round(rawTime-minutes*60,1)
    returnString = ""
    
    # Adding text to final string
    if minutes >0:        
        returnString += str(minutes)+checkPlural(" Minute",minutes)+','
    if seconds>0:
        returnString += str(seconds)+checkPlural(" Second",seconds)+'.'

    
    return returnString


# Returns the number of unopen Tiles
def numberOfUnopendTiles():
    counter = 0
    # Loops through every tile
    for column in range(boardSize):
        for row in range(boardSize):
            # if tile is not open then add 1 to the counter
            if boardList[column][row]== []: 
                counter +=1
                
    return counter
    

# Checks if any of the buttons are clicked
def checkButtons():
    
    # Loops through all of the buttons
    for buttonName in buttons: 
        
        # If the mouse is colliding with the button (AKA clicking on it)
        if buttons[buttonName].collidepoint(mouse.get_pos()): 
            
            # Checks the name of the button and does the appropiate action
            if buttonName == 'retry':
                resetGame()
                return removeButtons()
            elif buttonName == 'minesweeper':
                moveScreens('gameScreen')
                removeButtons()
                return addButton(gameScreen,"Options",BLACK,300,STATSFONT,0)
            elif buttonName == 'continue':
                loadGame()
                moveScreens('gameScreen')
                return removeButtons()
            elif buttonName == 'quit':
                global running
                running = False
            elif buttonName == 'flood':
                os.startfile('Flood.exe')
        
    
# Draws the end screen            
def drawEndScreen(surface,bgColour,titleText,stats,animate = True):
    global buttons,width,height
    # Declaring all of the varibles
    width = SIZE[0]
    height = SIZE[1]
    surface.fill(bgColour)
    startingY = height/4

    # Drawings and centers the title
    title = TITLEFONT.render(titleText,True,WHITE)
    titleWidth = title.get_width()
    titleX = (width-titleWidth)/2
    titleY = 10
    surface.blit(title,(titleX,titleY))

    # Loops through every statistic that need to be displayed
    for stat in stats:
        # Drawing and positioning text on screen
        text = STATSFONT.render(stat,True,WHITE)
        textWidth = text.get_width()
        textHeight = text.get_height()
        x = (width-textWidth)/2
        y = startingY+ textHeight*stats.index(stat)
        surface.blit(text,(x, y))
        # Updating screens
        mainScreen.blit(gameScreen,gameScreenCoords)
        mainScreen.blit(endScreen,endScreenCoords)
        display.flip()
        # Waits a bit to make it look cooler
        if animate:
            if win:
                time.wait(1000)
            else:
                time.wait(500)
                
    # Adding return button
    if animate:    
        addButton(endScreen,'RETRY?',WHITE)
    
# Displays a warning
def displayWarning(surface):
    remove = []
    # For every warning
    for index in range(len(warnings)):
        # If the warning should still be showing draw the text
        if warningTimes[index] !=0:
            text = WARNINGFONT.render(warnings[index],True,RED)
            spacing = text.get_height()
            x = 10
            y = spacing*2 + spacing *(index+1)
            surface.blit(text,(x, y))
                         
            warningTimes[index] -=1
        else:
            # If time is over then add it to the remove array
            remove.append(index)
    
    # For every index to remove
    for index in remove:
        # Remove index from both lists
        del warningTimes[index]
        del warnings[index]

# Adds the elements of 2 lists together
def addLists(list1,list2):
    return [list1[0]+list2[0],list1[1]+list2[1]]

# sets up the board
def setupBoard(boardSize,numMines):
    
    plantedMines = 0
    boardList = [[[] for x in range(boardSize)] for x in range(boardSize)]# creating empty 2D list
    
    # Filling list with mines
    while plantedMines < numMines:
        # Creates random spot to place mine
        randomCol = random.randint(0,boardSize-1)
        randomRow = random.randint(0,boardSize-1)
        # If there is no mine there already then place the mine 
        if boardList[randomCol][randomRow] !='X':
            boardList[randomCol][randomRow] = 'X'
            plantedMines +=1
            
    return boardList


# Draws the board

def drawBoard(surface,boardList,boardSize,tileSize,tileBuffer):
    if gameOver :
        return
    mouseCol = int((mouse.get_pos()[0]-(boardCoords[0]+gameScreenCoords[0]))/(tileSize+tileBuffer))
    mouseRow = int((mouse.get_pos()[1]-(boardCoords[1]+gameScreenCoords[1]))/(tileSize+tileBuffer))
            
    # Loops through every tile
    for column in range(boardSize):
        for row in range(boardSize):
            # Coordinates of the Tile
            tileX = column*tileSize + column*tileBuffer
            tileY = row*tileSize + row*tileBuffer
            
            # If there is a mine in the tile then draw a mine under the Tile
            if boardList[column][row] == 'X':
                # Drawing the Mine and the background
                draw.rect(surface, LIGHTGRAY, Rect(tileX, tileY, tileSize, tileSize))
                surface.blit(MINE_IMG, (tileX, tileY))
                
                # Draws the Tiles
                if mouseCol == column or mouseRow == row:
                    surface.blit(LIGHTTILE_IMG, (tileX, tileY))
                else:
                    surface.blit(TILE_IMG, (tileX, tileY))
                if mouseCol == column and mouseRow == row:
                    surface.blit(DARKTILE_IMG, (tileX, tileY))
                    
                draw.rect(surface, RED, Rect(tileX, tileY, tileSize, tileSize))
                
            # If the tile is unopened then draw the empty Tile
            elif boardList[column][row] == []:
                
                # Draws the Tiles
                if mouseCol == column or mouseRow == row:
                    surface.blit(LIGHTTILE_IMG, (tileX, tileY))
                else:
                    surface.blit(TILE_IMG, (tileX, tileY))
                if mouseCol == column and mouseRow == row:
                    surface.blit(DARKTILE_IMG, (tileX, tileY))
                    
            # If the tile is open and empty
            elif boardList[column][row] ==0:
                draw.rect(surface, (170,170,245), Rect(tileX, tileY, tileSize, tileSize))
            
            # If tile has a number in it
            elif boardList[column][row] >0:
                # Creating varibles to change the shading of the tile 
                multiplier = 30
                shading = boardList[column][row] * multiplier
                
                # If the shading is too much then tone it down
                while shading >150:
                    multiplier -=1
                    shading = boardList[column][row] * multiplier
                    
                # Draws the rectangle with shading
                draw.rect(surface, (150-shading , 200 ,150-shading), Rect(tileX, tileY, tileSize, tileSize))
                text = NUMBERFONT.render(str(boardList[column][row]) ,True, BLACK)
                surface.blit(text,(tileX + (tileSize-text.get_width())/2,tileY + (tileSize-text.get_height())/2))


# Draws the flags
def drawFlags(surface, flagList):
    
    if gameOver:
        return
    
    # Loops through every flag position
    for flagPos in flagList:
        
        # Calculating x,y of flag
        column = flagPos[0]
        row = flagPos[1]
        flagX = column*tileSize + column*tileBuffer
        flagY = row*tileSize + row*tileBuffer
        
        # Draw flag
        surface.blit(FLAG_IMG, (flagX, flagY))
        
# Displays the text showing how many flags are left 
def drawFlagsLeft(surface, x, y, flagsLeft):
    
    text = TEXTFONT.render("Flags Left: "+str(flagsLeft),True,BLACK)
    surface.blit(text, (x,y))


# Checks the tile at a given location
def checkTile(surface, column ,row): 
    if gameOver:
        return
    
    if boardList[column][row] != []:
        if boardList[column][row] != 'X':
            return
    
    if boardList[column][row] == 'X':
        
        gameOverFunc()
            
        return 
    else:
        mineCount =0
        surroundings = [[column-1,row],[column-1,row-1],[column,row-1],[column+1,row-1],[column+1,row],[column+1,row+1],[column,row+1],[column-1,row+1]]
    
        for tile in surroundings:
            checkColumn = int(tile[0])
            checkRow = int(tile[1])

            if checkColumn >=0 and checkRow >=0 and checkColumn <= boardSize-1 and checkRow <= boardSize-1:
            
                if boardList[checkColumn][checkRow] == 'X':
                    
                    mineCount +=1
                   
        if [column,row] in flagList:
            return "FLAG"
        
        if mineCount ==0:
            boardList[column][row] = 0
            blankTile(surface, column, row)
            return 0
        else:
            boardList[column][row] = mineCount
            return mineCount
        
        
        
# Recursive function to open all blank tiles
def blankTile(surface, column ,row): 

    surroundings = [[column-1,row],[column-1,row-1],[column,row-1],[column+1,row-1],[column+1,row],[column+1,row+1],[column,row+1],[column-1,row+1]]
    
    for tile in surroundings:
            checkColumn = int(tile[0])
            checkRow = int(tile[1])

            if checkColumn >=0 and checkRow >=0 and checkColumn <= boardSize-1 and checkRow <= boardSize-1:
                
                if checkTile(surface, checkColumn, checkRow) == 0:
                    boardList[checkColumn][checkRow]=0
                    
                    blankTile(surface, checkColumn, checkRow)
                    drawBoard(board, boardList, boardSize, tileSize, tileBuffer)
                    updateScreens()
    return 
    

def showMines():
    for column in range(boardSize):
        for row in range(boardSize):
            
            if boardList[column][row] == 'X':
                tileX = column*tileSize + column*tileBuffer
                tileY = row*tileSize + row*tileBuffer
                
                
                if [column,row] in flagList:
                    draw.rect(board, GREEN, Rect(tileX,tileY,tileSize,tileSize))
                    board.blit(FLAG_IMG, (tileX, tileY))
                else:
                    expX = gameScreenCoords[0]+boardCoords[0]+tileX+tileSize/2
                    expY = gameScreenCoords[1]+boardCoords[1]+tileY+tileSize/2
                    makeExplosion(expX,expY,explosionSpeed)
                    
                    draw.rect(board, RED, Rect(tileX,tileY,tileSize,tileSize))
                    board.blit(MINE_IMG, (tileX, tileY))
                
            if [column,row] in flagList and boardList[column][row] != 'X':
                tileX = column*tileSize + column*tileBuffer
                tileY = row*tileSize + row*tileBuffer
                
                board.blit(BROKENFLAG_IMG, (tileX, tileY))

    display.flip()

def gameOverFunc():
    global ENDSCREENBG,gameOver
    
    ENDSCREENBG = DARKRED
    
    drawBoard(board, boardList, boardSize, tileSize, tileBuffer)
    gameScreen.blit(board,boardCoords)
    mainScreen.blit(gameScreen,gameScreenCoords)
    display.update()
    gameOver = True
    
    showMines()
    
    
    
    if os.path.exists('Saved Game.txt'):
        os.remove('Saved Game.txt')
    
def checkCorrectFlags():
    flaggedMines = 0
    for flagPos in flagList:
        if boardList[flagPos[0]][flagPos[1]] == 'X':
            flaggedMines +=1
            
    return flaggedMines
        
    
def displayTime(frame):
    
    timeString = "Time: "+ timeToString(frame)
    text = TEXTFONT.render(timeString,True,BLACK)
    y = text.get_height()
    
    gameScreen.blit(text,(0,y))
    

# Function to add buttons
    
def addButton(surface,name,colour,y=9999,textFont = TITLEFONT,x=9999):
    
    # Creating the text and getting its dimensions
    text = textFont.render(name,True,colour)
    textWidth = text.get_width()
    textHeight = text.get_height()
    
    # If no x or y was given then use these default values
    if x ==9999: x = (width-textWidth)/2
    if y ==9999: y = (height/3)*2
         
    # Display text
    surface.blit(text,(x, y))
        
    # Adding button to button lists to be used for collsion and animations
    buttonText.append([surface,name,[x,y],colour,textFont])
    name = name.lower()
    name = name.replace("?","")
    buttons[name]=Rect(x, y, textWidth, textHeight)
    buttonAnimations.append(Rect(x, y+textHeight,0,10))
    buttonOrder.append(name)
          
    
# Function to draw 3D text

def animateText(surface,surfaceCoords,x,y,size,text):
    
    # Setting up varibles for loop
    colourMultipler = 255.0/size
    textColour = WHITE
    currentSize = 0
    
    while True:
        
        # Declaring font,rendering text and getting width of text
        FONT= font.Font("GODOFWAR.TTF",currentSize)
        textRender = FONT.render(text,True,textColour)
        textWidth = textRender.get_width()
        
        # Drawing text and updating screen
        surface.blit(textRender,(x-textWidth/2,y))
        mainScreen.blit(surface,surfaceCoords)
        display.update()
        
        # Chainging varibles for next iteration of the loop
        y -=1
        currentSize +=1
        textColour = (textColour[0]-colourMultipler,textColour[1]-colourMultipler,textColour[2]-colourMultipler)
        
        time.wait(10) # wait to make animation cooler
        
        if size ==currentSize: #  If text has reached desired size then break
            break
        
    # Make on last layer of text to make it easier to read 
    textRender = FONT.render(text,True,RED)
    textWidth = textRender.get_width()
    surface.blit(textRender,(x-textWidth/2,y))
    mainScreen.blit(surface,surfaceCoords)
    display.update()


# Draws main menu
def drawMenu():
    
    # Draws the Title
    animateText(menuScreen,menuScreenCoords, width/2,100,50,'MEGA ARCADE')
    # Draws the first button
    addButton(menuScreen,'Minesweeper',BLACK,height/3)
    # Updates the screen
    mainScreen.blit(menuScreen,menuScreenCoords)
    display.update()
    time.wait(500)

    # Draws the continue button if there is a saved game 
    floodY = height/2
    if os.path.exists('Saved Game.txt'):
        addButton(menuScreen,'Continue',BLACK,(height/2))
        mainScreen.blit(menuScreen,menuScreenCoords)
        display.update()
        floodY = (2*height/3)
        time.wait(500)
        
    # Draws the Flood button and updates the screen
    addButton(menuScreen,'Flood',BLACK,floodY)
    mainScreen.blit(menuScreen,menuScreenCoords)
    display.update()
    time.wait(500)
    # Draws the quit button
    quitY = floodY + TITLEFONT.size("Flood")[1]+20
    addButton(menuScreen,'Quit',BLACK,quitY)
    mainScreen.blit(menuScreen,menuScreenCoords)
    display.update()
    
# Removes all of the buttons
def removeButtons():
    global buttons,buttonAnimations ,buttonOrder    
    # Sets all the button varibles to nothing
    buttons = {}
    buttonAnimations = []
    buttonOrder = []
    
    
# Saves the current game
def saveGame():
    # Saves the time
    finalText = str(timer)+'\n'
    
    # Loops through every item in the list
    for column in boardList:
        for item in column:
            # Gives the current tile a symbol
            if item ==[]:
                symbol = 'E'+':'#If the tile has not been opened yet use E as the symbol
            else:
                symbol = str(item)+':'# Add the number with a colon after it (colon is used to seperate the items)
                
            finalText +=symbol
            
        finalText+='\n'
    
    #Saves the Flags
    for pos in flagList:
        finalText+=str(pos[0])+':'+str(pos[1])+'\n'
        
    #Write the text to the file
    saveFile = open('Saved Game.txt','w')
    saveFile.write(finalText)
    saveFile.close()
    
def loadGame():
    #Declaring all of the varibles and reading the save file
    global boardList,timer
    boardList = []
    inputFile = open('Saved Game.txt','r')
    rawLines = inputFile.readlines()
    inputFile.close
    timer = int(rawLines[0])
    del rawLines[0]
    
    #Loops through every line in the file
    for index in range(boardSize):
        #Decodes the symbols
        boardList.append([])
        for item in rawLines[index].split(":"):
            if item == 'E':
                boardList[-1].append([])
            elif item == 'X':
                boardList[-1].append('X')
                
            elif item =='\n':
                pass
            else:
                boardList[-1].append(int(item))
            
    #Loads the flags
    for index in range(len(rawLines)-(boardSize)):
        flagPos = rawLines[len(boardList)+index]
        flagList.append([int(x) for x in flagPos.split(':')])
        
    #Draws the board
    drawBoard(board, boardList, boardSize, tileSize, tileBuffer)
    drawFlags(board, flagList)
                
    
def highlightTile(column,row):
    if [column,row] in highlightCenters:
        return
    surroundings = [[column-1,row],[column-1,row-1],[column,row-1],[column+1,row-1],[column+1,row],[column+1,row+1],[column,row+1],[column-1,row+1]]
    tempList = []
    for tile in surroundings:
        tileX = tile[0]*tileSize + tile[0]*tileBuffer
        tileY = tile[1]*tileSize + tile[1]*tileBuffer
        tempList.append([tileX,tileY])
        board.blit(highlight,(tileX,tileY))
        
    highlights.append(tempList)
    highlightTimes.append(timer+FPS*3)
    highlightCenters.append([column,row])
    
#######################Main Varibles#######################

# Declaring Colours
RED=(254,0,0)
DARKRED= (155,0,0)
GREEN=(0,254,0)
BLUE=(1,170,230)
BLACK=(0,0,0)
GRAY=(100,100,100)
LIGHTGRAY = (180,180,180)
WHITE = (254,254,254)
ORANGE = (255,70,0)
ENDSCREENBG = BLUE


# Declaring all Surfaces
SIZE = width,height = 650,450
FPS = 24
mainScreen = display.set_mode(SIZE)
menuScreen = Surface(SIZE)
gameScreen = Surface(SIZE)
endScreen = Surface(SIZE)
optionScreen = Surface(SIZE)
currentScreen = menuScreen

# Filling all of the Surfaces
mainScreen.fill(WHITE)
menuScreen.fill(WHITE)
gameScreen.set_colorkey(WHITE)
endScreen.fill(BLUE)
optionScreen.fill(WHITE)
currentBgColour = WHITE

# Coordiantes for all of the Surfaces
boardCoords= [200,0]
gameScreenCoords = [width+20,20]
endScreenCoords = [width*2,0]
menuScreenCoords = [0,0]
optionScreenCoords = [width,height]
screenSlideSpeed = 5

# Declaring board varibles
boardSize = 20 # in tiles
tileSize = (width-250)/boardSize
numMines = 3
tileBuffer = int(round(tileSize/20,0))
board = Surface((boardSize*tileSize + tileSize*tileBuffer ,boardSize*tileSize + tileSize*tileBuffer))
boardRect = Rect(addLists(boardCoords,gameScreenCoords),(boardSize*(tileSize + tileBuffer) ,boardSize*(tileSize + tileBuffer)))
board.fill(WHITE)
board.set_colorkey(WHITE)
boardList = setupBoard(boardSize,numMines)
NUMBERFONT = font.SysFont("Times New Roman", tileSize-5)

# Declaring varibles for flags
flagList = []
numFlags = numMines
placedFlags = 0

# Decalring varibles for buttons
buttons = {}
buttonText = []
buttonAnimations = []
buttonAnimationSpeed = 20
buttonOrder = []

# Declaring varibles for warnings
warnings = []
warningTimes=[]

# Decalring explosion varibles
explosionSpeed = 7
explosions = []

#Declaring highlight Varibles
highlights = []
highlightTimes = []
highlightCenters = []
highlight = Surface((tileSize,tileSize)) 
highlight.set_alpha(128)             
highlight.fill((255,0,0))

# General game varibles
gameOver = False
gameInProgress = False
win = False
timer = 0
clock = time.Clock()
running = True
clicks = 0

# Importing images
FLAG_IMG = image.load('Flag.png')
MINE_IMG = image.load('Mine.png')
TILE_IMG = image.load('Tile.png')
BROKENFLAG_IMG = image.load('Broken Flag.png')
LIGHTTILE_IMG = image.load('Light Tile.png')
DARKTILE_IMG = image.load('Dark Tile.png')

# Resizing images
FLAG_IMG = transform.scale(FLAG_IMG, (tileSize, tileSize))
MINE_IMG.set_colorkey(WHITE)
MINE_IMG = transform.scale(MINE_IMG, (tileSize, tileSize))
TILE_IMG = transform.scale(TILE_IMG, (tileSize, tileSize))
LIGHTTILE_IMG = transform.scale(LIGHTTILE_IMG, (tileSize, tileSize))
DARKTILE_IMG = transform.scale(DARKTILE_IMG, (tileSize, tileSize))
BROKENFLAG_IMG = transform.scale(BROKENFLAG_IMG, (tileSize, tileSize))

# Setting up the window
display.set_caption("MineSweeper")
display.set_icon(MINE_IMG)
drawBoard(board, boardList, boardSize, tileSize, tileBuffer)# Initializing starting board
drawMenu()
mainScreen.blit(menuScreen,menuScreenCoords)
display.update()


while running:
    mousePos = mouse.get_pos()
    clock.tick(FPS)
    mainScreen.fill(WHITE)
    gameScreen.fill(WHITE)
    
    # Add to time if the game is going on
    if gameOver == False:
        timer +=1
    
    for evnt in event.get():
        
        if evnt.type == QUIT:
            # If there is a game in progress then save it
            if gameInProgress:                
                saveGame()
            running = False
            
        if evnt.type == MOUSEBUTTONDOWN and mouse.get_pressed()[0]: # clicking on a tile
            clicks+=1
            
            col = int((mousePos[0]-(boardCoords[0]+gameScreenCoords[0]))/(tileSize+tileBuffer))
            row = int((mousePos[1]-(boardCoords[1]+gameScreenCoords[1]))/(tileSize+tileBuffer))

           
            
            if boardRect.collidepoint(mousePos):
                
                if [col,row] not in flagList:
                    
                    checkTile(board, col, row)
                    drawBoard(board, boardList, boardSize, tileSize, tileBuffer)
                    drawFlags(board, flagList)
            else:
                print "Invalid Tile"
                
            checkButtons()
            
        if evnt.type == MOUSEBUTTONDOWN and mouse.get_pressed()[1]:
            col = int((mousePos[0]-(boardCoords[0]+gameScreenCoords[0]))/(tileSize+tileBuffer))
            row = int((mousePos[1]-(boardCoords[1]+gameScreenCoords[1]))/(tileSize+tileBuffer))
            
            if boardList[col][row] != [] or boardList[col][row] != 'X' :
                if boardList[col][row] >0:
                    highlightTile(col,row)
            
        if evnt.type == MOUSEBUTTONDOWN and mouse.get_pressed()[2]: # placing a flag
            clicks+=1
            
            col = int((mousePos[0]-(boardCoords[0]+gameScreenCoords[0]))/(tileSize+tileBuffer))
            row = int((mousePos[1]-(boardCoords[1]+gameScreenCoords[1]))/(tileSize+tileBuffer))
                
           
            if boardRect.collidepoint(mousePos):
                
                if [col,row] in flagList:
                    flagList.remove([col,row])
                    
                else:
                    if placedFlags < numMines:
                        
                        if boardList[col][row] == [] or boardList[col][row] == 'X' :
                            flagList.append([col,row])
                    
                            drawBoard(board, boardList, boardSize, tileSize, tileBuffer)
                            drawFlags(board, flagList)

                    else:
                        warnings.append('No Flags Left')
                        warningTimes.append(2*FPS)
        
                
        if evnt.type == KEYDOWN and evnt.key ==K_r:
            resetGame()
   
   
    placedFlags = len(flagList)
    drawBoard(board, boardList, boardSize, tileSize, tileBuffer)
    drawFlags(board, flagList)
            
    
    if placedFlags ==numMines and numberOfUnopendTiles() == 0:
        checkWin()       
            
    # Calculating the widths for the rectangles that animate under the buttons
    buttonIndex = -1
    for buttonName in buttonOrder:
        buttonIndex +=1
        collisionRect = buttons[buttonName]
        
        # If the mouse is on the button then make the rectangle wider
        if collisionRect.collidepoint(mouse.get_pos()): 
            animationRect = buttonAnimations[buttonIndex]
            x = animationRect.x
            y = animationRect.y
            width = animationRect.width
            height = animationRect.height
            # if the rectangle is smaller than button then update the width      
            if width < collisionRect.width:           
                buttonAnimations[buttonIndex] = Rect(x,y,width+buttonAnimationSpeed,height)
        else:

            # Making rectangle smaller if the mouse is not on the button
            animationRect = buttonAnimations[buttonIndex]
            x = animationRect.x
            y = animationRect.y
            width = animationRect.width
            height = animationRect.height
            # If the rectangle's width is greater than 0 then update the width  
            if width >0:
                buttonAnimations[buttonIndex] = Rect(x,y,width-buttonAnimationSpeed,height)
            
                
        ##### The rectangles that animate under the buttons#####
            
        # Calculating the multipliers for the colours to make the bar fade in and out
        redMulti = float((255-currentBgColour[0])-currentBgColour[0])/(buttons[buttonName].width + buttonAnimationSpeed)
        greenMulti = float((255-currentBgColour[1])-currentBgColour[1])/(buttons[buttonName].width + buttonAnimationSpeed)
        blueMulti = float((255-currentBgColour[2])-currentBgColour[2])/(buttons[buttonName].width + buttonAnimationSpeed)
        
        # Making the new colour based on the width of the rectangle
        barColour = (currentBgColour[0]+animationRect.width*redMulti,currentBgColour[1]+animationRect.width*greenMulti,currentBgColour[2]+animationRect.width*blueMulti)

        # Drawing the rectangles        
        draw.rect(currentScreen,currentBgColour, Rect(animationRect.x,animationRect.y,buttons[buttonName].width + buttonAnimationSpeed,animationRect.height))
        draw.rect(currentScreen, barColour ,animationRect)       
            
    #Drawing button text
    for rawData in buttonText:
        blitter = rawData[4].render(rawData[1],True,rawData[3])
        draw.rect(rawData[0],currentBgColour,Rect(rawData[2],(blitter.get_width(),blitter.get_height())))
        rawData[0].blit(blitter,rawData[2])
    
    
    ########## Explosion animation #########
    removeExplosion = []
    
    # Updating "shrapnel" positions
    for index in range(len(explosions)):
        
        rawData = explosions[index]
        #Updating shrapnel positions
        explosions[index][0][0] += rawData[1][0]
        explosions[index][0][1] += rawData[1][1]
        explosions[index][1][0] *= 0.98
        explosions[index][1][1] *= 0.98
        if math.fabs(explosions[index][1][0]) <explosionSpeed*.3:
            removeExplosion.append(index)
            
    removed = 0
    
    # Removing slow shrapnel
    for removeIndex in removeExplosion:
        del explosions[removeIndex-removed]
        #if all of the shrapnel is gone then show the end screen
        if len(explosions) ==0 and gameOver:
            moveScreens('endScreen')
            stats = ["It Took You "+timeToText(timer),"You Clicked "+str(clicks)+checkPlural(' Time',clicks), "You Placed "+str(placedFlags) + checkPlural(' Flag',placedFlags), "You Flagged "+str(checkCorrectFlags()) + checkPlural(' Mine',checkCorrectFlags())]
            drawEndScreen(endScreen,ENDSCREENBG,'YOU LOSE',stats)
            
        removed +=1
        
    ############Drawing Highlights############
        
    for square in highlights:
        for coord in square:
            board.blit(highlight,coord)
            
    if len(highlights) >0:
        if  timer>=highlightTimes[0]:
            del highlights[0],highlightTimes[0],highlightCenters[0]
        
    # Functions that need to run every iteration of the loop
    drawFlagsLeft(gameScreen,0 ,0 ,numFlags-placedFlags)
    displayTime(timer)
    displayWarning(gameScreen)
    
        
        
     # Drawing all surfaces to the main screen
    if not win:
        draw.rect(mainScreen,GRAY, boardRect)
    gameScreen.blit(board,boardCoords)
    mainScreen.blit(gameScreen,gameScreenCoords)
    mainScreen.blit(menuScreen,menuScreenCoords)
    mainScreen.blit(endScreen,endScreenCoords)
    
    # Drawing shrapnel
    for rawCoords in explosions:
        draw.circle(mainScreen, ORANGE, rawCoords[0], 3)

    # Updating the Screen
    display.flip()
        


                            # # # # # # # # # # # # # # #
                            # #      Minesweeper      # # 
                            # #  By: Mohammed Eseifan # # 
                            # # # # # # # # # # # # # # # 
from pygame import *
import random,math,os
import inputbox # by Timothy Downs
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
        startY = highscoreScreenCoords[1]
        while gameScreenCoords[0] != 20 or gameScreenCoords[1] !=20:
            if gameScreenCoords[0] != 20:
                # Moving all of the screens to thier positions
                gameScreenCoords[0] += copysign(gameScreenCoords[0]-20,True)*screenSlideSpeed
                endScreenCoords[0]+= copysign(gameScreenCoords[0]-40,True)*screenSlideSpeed
                menuScreenCoords[0]+= copysign(gameScreenCoords[0]-20,True)*screenSlideSpeed
                optionScreenCoords[0]+= copysign(gameScreenCoords[0]-20,True)*screenSlideSpeed
                highscoreScreenCoords[0]+= copysign(gameScreenCoords[0]-20,True)*screenSlideSpeed
           
            if gameScreenCoords[1] !=20:
                
                gameScreenCoords[1] += copysign(startY,True)*screenSlideSpeed
                endScreenCoords[1]+= copysign(startY,True)*screenSlideSpeed
                menuScreenCoords[1]+= copysign(startY,True)*screenSlideSpeed
                optionScreenCoords[1]+= copysign(startY,True)*screenSlideSpeed
                highscoreScreenCoords[1]+= copysign(startY,True)*screenSlideSpeed
            
            # Updating Screen
            mainScreen.fill(WHITE)
            gameScreen.fill(WHITE)
            updateScreens()
            
        # Updating Global varibles
    
        boardRect = Rect(addLists(boardCoords,gameScreenCoords),(boardSize*(tileSize + tileBuffer) ,boardSize*(tileSize + tileBuffer)))
        boardRect.normalize()
        currentScreen = gameScreen
        gameInProgress = True
        timer = 0
        currentBgColour = WHITE
        
        
        textHeight = TEXTFONT.size('Main Menu')[1]
        menuCoords = height -(textHeight+gameScreenCoords[1]+10)
        addButton(gameScreen,gameScreenCoords,"Main Menu",BLACK,menuCoords-(textHeight+10),STATSFONT,0) 
        
        addButton(gameScreen,gameScreenCoords,"Options",BLACK,menuCoords,STATSFONT,0)

    elif targetScreen == 'endScreen':
        
        while endScreenCoords[0] != 0:
            
            # Moving all of the screens to thier positions
            gameScreenCoords[0] += copysign(endScreenCoords[0],True)*screenSlideSpeed
            endScreenCoords[0]+= copysign(endScreenCoords[0],True)*screenSlideSpeed
            menuScreenCoords[0]+= copysign(endScreenCoords[0],True)*screenSlideSpeed
            optionScreenCoords[0]+= copysign(endScreenCoords[0],True)*screenSlideSpeed
            highscoreScreenCoords[0]+= copysign(endScreenCoords[0],True)*screenSlideSpeed
            
            # Updating Screen
            mainScreen.fill(WHITE)
            updateScreens()
            
        # Updating Global varibles
        currentScreen  = endScreen
        gameInProgress= False
        currentBgColour = ENDSCREENBG    
        
    elif targetScreen == 'optionScreen':
        
        optionScreen.fill(BLUE)
        if optionScreenCoords[0]!=0:
            moveScreens('gameScreen')
            optionScreenCoords[0] = 0
            
        while optionScreenCoords[1] > 0:
            
            # Moving all of the screens to thier positions
            gameScreenCoords[1] += copysign(optionScreenCoords[1],True)*screenSlideSpeed
            endScreenCoords[1]+= copysign(optionScreenCoords[1],True)*screenSlideSpeed
            menuScreenCoords[1]+= copysign(optionScreenCoords[1],True)*screenSlideSpeed
            optionScreenCoords[1]+= copysign(optionScreenCoords[1],True)*screenSlideSpeed
            highscoreScreenCoords[1]+= copysign(optionScreenCoords[1],True)*screenSlideSpeed
            
            # Updating Screen
            mainScreen.fill(WHITE)
            updateScreens()
            
        # Updating Global varibles
        currentScreen  = optionScreen
        currentBgColour = BLUE
        drawOptions()
        
    elif targetScreen == 'highscoreScreen':
        
        highscoreScreen.fill(BLUE)
        if highscoreScreenCoords[0]>0:
                moveScreens('gameScreen')
                highscoreScreenCoords[0] = 0
        while highscoreScreenCoords[1] < 0:
            
                
         # Moving all of the screens to thier positions
            gameScreenCoords[1] += copysign(highscoreScreenCoords[1],True)*screenSlideSpeed
            endScreenCoords[1]+= copysign(highscoreScreenCoords[1],True)*screenSlideSpeed
            menuScreenCoords[1]+= copysign(highscoreScreenCoords[1],True)*screenSlideSpeed
            optionScreenCoords[1]+= copysign(highscoreScreenCoords[1],True)*screenSlideSpeed
            highscoreScreenCoords[1]+= copysign(highscoreScreenCoords[1],True)*screenSlideSpeed
            
            # Updating Screen
            mainScreen.fill(WHITE)
            updateScreens()
            
        # Updating Global varibles
        currentScreen  = highscoreScreen
        currentBgColour = BLUE
        
    elif targetScreen == 'menuScreen':
        
        menuScreen.fill(WHITE)
        if menuScreenCoords[1] !=0:
            moveScreens('gameScreen')
            
        while menuScreenCoords[0] !=0:
            # Moving all of the screens to thier positions
            gameScreenCoords[0] += copysign(menuScreenCoords[0],True)*screenSlideSpeed
            endScreenCoords[0]+= copysign(menuScreenCoords[0],True)*screenSlideSpeed
            menuScreenCoords[0]+= copysign(menuScreenCoords[0],True)*screenSlideSpeed
            optionScreenCoords[0]+= copysign(menuScreenCoords[0],True)*screenSlideSpeed
            highscoreScreenCoords[0]+= copysign(menuScreenCoords[0],True)*screenSlideSpeed
            
            # Updating Screen
            mainScreen.fill(WHITE)
            updateScreens()
        
        currentScreen  = menuScreen
        currentBgColour = WHITE
                                     
#Updates all of the screens
def updateScreens(refresh =True):
    gameScreen.blit(board,boardCoords)
    mainScreen.blit(gameScreen,gameScreenCoords)
    mainScreen.blit(endScreen,endScreenCoords)
    mainScreen.blit(menuScreen,menuScreenCoords)
    mainScreen.blit(optionScreen,optionScreenCoords)
    mainScreen.blit(highscoreScreen,highscoreScreenCoords)
    
    if refresh:
        display.flip()
        
# Resets all the varibles to default        
def resetGame():
    global gameOver, boardList, flagList, placedFlags, timer,win,clicks, buttons,buttonAnimations,board,highlights,highlightTimes,highlightCenters,lasers,laserAcels,laserTimers,laserDeadList,laserBallCoords,laserCoords
    checkDifficulty()
    
    #Resets all varibles
    lasers = []
    laserAcels = []
    laserTimers = []
    laserDeadList = []
    laserBallCoords = laserBallX,laserBallY = [width/2,height/2]
    laserCoords = [[width/2,height/2]]
    flagList = []
    placedFlags = 0
    timer = 0  
    clicks = 0
    win = False
    gameOver = False
    highlights = []
    highlightTimes = []
    highlightCenters = []
    
    #Setting up board again
    boardList = setupBoard()
    board = Surface((boardSize*tileSize + tileSize*tileBuffer ,boardSize*tileSize + tileSize*tileBuffer))
    board.fill(WHITE)
    board.set_colorkey(WHITE)
    drawBoard(board, boardList, boardSize, tileSize, tileBuffer)
    removeButtons()
    moveScreens('gameScreen')
    updateScreens()
    
    
    

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
        
        #If the player has set a new highscore then show the screen
        if timer<highscores[-1] or len(highscores) <8 or highscores[-1] == None:
            addHighscore(timer)
            
        
        drawEndScreen(endScreen,ENDSCREENBG,'YOU WIN',stats)      
        
# Makes explosion at given coordinates
def makeExplosion(x,y,speed):
    xSpeed = int(speed*1.5)
    
    # Makes pieces of shrapnel
    shrapnelCount =250/numMines
    for i in range(20):
        acelX = random.randint(-xSpeed,xSpeed)
        acelY = random.randint(-speed,speed)
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
        returnString += str(minutes)+checkPlural(" Minute",minutes)+', '
    if seconds>0:
        returnString += str(seconds)+checkPlural(" Second",seconds)+'.'

    
    return returnString


# Returns the number of unopen Tiles
def numberOfUnopendTiles(includeMines = False):
    counter = 0
    # Loops through every tile
    for column in range(boardSize):
        for row in range(boardSize):
            # if tile is not open then add 1 to the counter
            if boardList[column][row]== []: 
                counter +=1
            elif boardList[column][row] == 'X' and includeMines == True:
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
                removeButtons()
                return resetGame() 
            
            elif buttonName == 'minesweeper':
                removeButtons()
                return moveScreens('gameScreen')
            
            elif buttonName == 'continue':
                loadGame()
                removeButtons()
                return moveScreens('gameScreen')
            
            elif buttonName == 'quit':
                global running
                running = False
                return removeButtons()
            
            elif buttonName == 'bonus game':
                os.startfile('Flood.exe')
                
            elif buttonName == 'options':
                removeButtons()
                return moveScreens('optionScreen')
            
            elif buttonName == 'easy':
                global difficulty
                difficulty = 'easy'
                return resetGame()
            
            elif buttonName == 'normal':
                global difficulty
                difficulty = 'normal'
                return resetGame()
            
            elif buttonName == 'hard':
                global difficulty
                difficulty = 'hard'
                return resetGame()    
            
            elif buttonName == 'highscores':
                moveScreens('highscoreScreen')
                removeButtons()
                return drawHighscoreScreen()
            
            elif buttonName == 'main menu':
                moveScreens('menuScreen')
                removeButtons()
                return drawMenu()
            
            elif buttonName == 'game screen':
                removeButtons()
                return moveScreens('gameScreen')
            
            elif buttonName == 'help':
                removeButtons()
                menuScreen.fill(WHITE)
                return showHelp()
 

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
        if '$' in stat:
            animate = False
            newStat =stat.replace('$','')
        else:
            newStat = stat
            animate = True
        # Drawing and positioning text on screen
        text = STATSFONT.render(newStat,True,WHITE)
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
        addButton(endScreen,endScreenCoords,'RETRY?',WHITE)
    
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
            y = spacing*3 + spacing *(index+1)
            surface.blit(text,(x, y))
                         
            warningTimes[index] -=1
        else:
            # If time is over then add it to the remove array
            remove.append(index)
    removed = 0
    # For every index to remove
    for index in remove:
        # Remove index from both lists
        del warningTimes[index-removed]
        del warnings[index-removed]
        removed +=1
        
# Adds the elements of 2 lists together
def addLists(list1,list2):
    return [list1[0]+list2[0],list1[1]+list2[1]]

#Changes the board according to the difficulty
def checkDifficulty():
    global boardSize,tileSize,numMines,numFlags,placedFlags,NUMBERFONT,highscores
    width = SIZE[0]
    #If the difficulty is easy then make the board 15x15 with 10 mines
    if difficulty == 'easy':
        boardSize =15
        numMines = 10
    #If the difficulty is easy then make the board 20x20 with 30 mines
    elif difficulty == 'normal':
        boardSize = 20
        numMines = 30
    #If the difficulty is hard then make the board 20x20 with 70 mines
    elif difficulty == 'hard':
        boardSize = 20
        numMines = 70
        
    #Resetting the varibles that depend on board size and number of mines
    tileSize = (width-250)/boardSize
    NUMBERFONT = font.SysFont("Times New Roman", tileSize-5)
    numFlags = numMines
    placedFlags = 0
    highscores = getHighscores()
    loadImages()

# sets up the board
def setupBoard():
    
        
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
                    
                #draw.rect(surface, RED, Rect(tileX, tileY, tileSize, tileSize))#Shows all of the mines(used for debugging)
                
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
    #If the game is over then exit
    if gameOver:
        return
    
    #if the function has been called on this tile before then exit
    if boardList[column][row] != []:
        if boardList[column][row] != 'X':
            return
    #If it is a mine then end the game
    if boardList[column][row] == 'X':
        tileX = gameScreenCoords[0]+boardCoords[0]+column*tileSize + column*tileBuffer+tileSize/2
        tileY = gameScreenCoords[1]+boardCoords[1]+row*tileSize + row*tileBuffer+tileSize/2
        makeBurst(tileX,tileY,20)
        gameOverFunc()
        return 
    #If it is not a mine then display a number
    else:
        #Declaring varibles needed to cound mines
        mineCount =0
        surroundings = [[column-1,row],[column-1,row-1],[column,row-1],[column+1,row-1],[column+1,row],[column+1,row+1],[column,row+1],[column-1,row+1]]
        
        #For every surrounding tile
        for tile in surroundings:
            checkColumn = int(tile[0])
            checkRow = int(tile[1])
            #If the tile is on the board
            if checkColumn >=0 and checkRow >=0 and checkColumn <= boardSize-1 and checkRow <= boardSize-1:
                #If there is a mine under the surrounding tile then add to the mine count
                if boardList[checkColumn][checkRow] == 'X':
                    mineCount +=1
                    
        #If there is a flag then return FLAG 
        if [column,row] in flagList:
            return "FLAG"
        
        #if there are no mines in the surrounding tiles
        if mineCount ==0:
            boardList[column][row] = 0
            blankTile(surface, column, row) #Calls the recursive function to open all the blank tiles
            return 0
        #if there are 1 or more mines
        else:
            #returns the number of mines
            boardList[column][row] = mineCount
            return mineCount
        
        
        
# Recursive function to open all blank tiles
def blankTile(surface, column ,row): 
    #list of surrounding tiles
    surroundings = [[column-1,row],[column-1,row-1],[column,row-1],[column+1,row-1],[column+1,row],[column+1,row+1],[column,row+1],[column-1,row+1]]
    
    #For every surrounding tile
    for tile in surroundings:
            checkColumn = int(tile[0])
            checkRow = int(tile[1])
            #if the tile in on the board
            if checkColumn >=0 and checkRow >=0 and checkColumn <= boardSize-1 and checkRow <= boardSize-1:
                
                #Checks the tile, if it is empty then call the recursive function on it again
                if checkTile(surface, checkColumn, checkRow) == 0:
                    boardList[checkColumn][checkRow]=0
                    blankTile(surface, checkColumn, checkRow)
            
    return 
    

#Shows all of the mines at the end of the game
def showMines():
    #For every tile
    for column in range(boardSize):
        for row in range(boardSize):
            #If the tile is is mine then show it
            if boardList[column][row] == 'X':
                tileX = column*tileSize + column*tileBuffer
                tileY = row*tileSize + row*tileBuffer
                #If the mine was flagged 
                if [column,row] in flagList:
                    #Show a green tile with a flag over it 
                    draw.rect(board, GREEN, Rect(tileX,tileY,tileSize,tileSize))
                    board.blit(FLAG_IMG, (tileX, tileY))
                #If the mine wasn't flagged
                else:
                    #Make an explosion
                    expX = gameScreenCoords[0]+boardCoords[0]+tileX+tileSize/2
                    expY = gameScreenCoords[1]+boardCoords[1]+tileY+tileSize/2
                    makeExplosion(expX,expY,explosionSpeed)
                    explosionSound.play()
                    #Show a red tile with a mine on it
                    draw.rect(board, RED, Rect(tileX,tileY,tileSize,tileSize))
                    board.blit(MINE_IMG, (tileX, tileY))
                    
            #If the tile was flagged but there wasnèt a mine there
            if [column,row] in flagList and boardList[column][row] != 'X':
                #Show a broken flag
                tileX = column*tileSize + column*tileBuffer
                tileY = row*tileSize + row*tileBuffer
                board.blit(BROKENFLAG_IMG, (tileX, tileY))

    display.flip()

#Ends the game
def gameOverFunc():
    global ENDSCREENBG,gameOver
    ENDSCREENBG = DARKRED
    #Removes all of the buttons and draws the board one more time. Then updates the screen
    removeButtons()
    drawBoard(board, boardList, boardSize, tileSize, tileBuffer)
    gameScreen.blit(board,boardCoords)
    mainScreen.blit(gameScreen,gameScreenCoords)  
    display.update()
    
    #Shows the mines and offically ends the game
    gameOver = True
    showMines()
    #Deletes the save file, if there is one
    if os.path.exists('Saved Game.txt'):
        os.remove('Saved Game.txt')
    
#Checks the number of correctly flagged flags
def checkCorrectFlags():
    flaggedMines = 0
    #for every flag
    for flagPos in flagList:
        #if there is a mine then add 1 to the count
        if boardList[flagPos[0]][flagPos[1]] == 'X':
            flaggedMines +=1
    #Return the count
    return flaggedMines
        

#Displays the time and the current Highscore
def displayStats(frame):
    #Formats the display time
    timeString = "Time: "+ timeToString(frame)
    text = TEXTFONT.render(timeString,True,BLACK)
    y = text.get_height()
    gameScreen.blit(text,(0,y))
    
    #If there is no highscore then display "No highscore"
    if highscores[0] ==None:
        text = 'No Highscores.'
    #If there is a highscore then display it
    else:
        #If the current time is greater than the highscore then show the next highscore
        if timer > highscores[0] and len(highscores)>1:
            index = 1
            #Loops though the highscores until it find the next best one
            while timer>highscores[index]:
                index +=1
                #If there is no next highscore then just use the last one
                if index >= len(highscores):
                    index = -1
                    break
                
            #Set the text
            text = "Next Highscore: "+timeToString(highscores[index])
        #If the current time is less than the highscore then display that
        else:
            text = "Current Highscore: "+timeToString(highscores[0])
    
    width = NUMBERFONT.size(text)[0]
    #If the text is too long then make a second line
    if width>=200:
        #Spliting the text into two lines
        firstLine = NUMBERFONT.render('Current HighScore:',True,BLACK)
        secondLine = NUMBERFONT.render(timeToString(highscores[0]),True,BLACK)
        gameScreen.blit(firstLine,(0,y*2))
        gameScreen.blit(secondLine,(0,y*3))
    else:
        currentHS= NUMBERFONT.render(text,True,BLACK)
        gameScreen.blit(currentHS,(0,y*2))
        

# Function to add buttons
    
def addButton(surface,surfaceCoords,name,colour,y=9999,textFont = TITLEFONT,x=9999):
    width,height = SIZE
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
    x2 =x+surfaceCoords[0]
    y2 = y+surfaceCoords[1]
    name = name.lower()
    name = name.replace("?","")
    buttons[name]=Rect(x2, y2, textWidth, textHeight)
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
    animateText(menuScreen,menuScreenCoords, width/2,50,50,'MEGA ARCADE')

    #Declaring vairbles to evenly space text
    startY = height/5
    buttons = ['Minesweeper','Continue','Bonus Game','Highscores','Options','Help']
    if os.path.exists('Saved Game.txt') == False:buttons.remove('Continue')#If there is no save file then dont show the continue option        
    totalTextHeight = sum([TITLEFONT.size(text)[1] for text in buttons])#Calculates the total height of the buttons text
    vertSpacing = (height-startY-totalTextHeight)/len(buttons)
    
    #Loops through every button
    for button in buttons:
        #Adds button then updates the screen and the Y varible
        addButton(menuScreen,menuScreenCoords,button,BLACK,startY)
        mainScreen.blit(menuScreen,menuScreenCoords)
        display.update()
        time.wait(250)
        startY+=vertSpacing+TITLEFONT.size(button)[1]
    
    
#Shows help menu
def showHelp():
    fileNames = os.listdir('Instructions\Minesweeper')
    listOfImages = [image.load('Instructions\Minesweeper\\'+filename) for filename in fileNames]
    currentImage = 0
    
    display.set_caption(fileNames[currentImage].split('.')[0])
    mainScreen.blit(listOfImages[currentImage],(0,0))
    display.update()
    
    while currentImage <= len(listOfImages)-1:
        clock.tick(10)
        for evnt in event.get():
            #If they quit then exit
            if evnt.type == QUIT:
                global running 
                running = False
                return  
            
            #Checks for a mouse clicked event
            if evnt.type == MOUSEBUTTONDOWN and mouse.get_pressed()[0]:
                currentImage+=1
            elif evnt.type == MOUSEBUTTONDOWN and mouse.get_pressed()[2]:
                if currentImage!=0:
                    currentImage-=1
            elif evnt.type == KEYDOWN and evnt.key ==K_ESCAPE:
                display.set_caption('Minesweeper')
                return drawMenu()
        
        if currentImage >= len(listOfImages):
            display.set_caption('Minesweeper')
            return drawMenu()
        
        display.set_caption(fileNames[currentImage].split('.')[0])
        mainScreen.blit(listOfImages[currentImage],(0,0))
        display.update()
    
    display.set_caption('Flood')
    drawMenu()
    
#Draws the option screen    
def drawOptions():
    optionScreen.fill(BLUE)
    height = SIZE[1]
    
    #Draws the title
    title = TITLEFONT.render('Difficulty',True,WHITE)
    titleWidth = title.get_width()
    titleCoords = [(width-titleWidth)/2,height/16]
    optionScreen.blit(title,titleCoords)
    
    #Declaring varibles for spacing buttons
    startY = height/3
    endY = 3*height/4
    buttons = ['Easy','Normal','Hard']
    totalTextHeight = sum([TITLEFONT.size(text)[1] for text in buttons])#Calculates the total height of the buttons text
    vertSpacing = (endY-startY-totalTextHeight)/len(buttons)
    
    #Loops through every button
    for button in buttons:
        #Adds button then updates the screen and the Y varible
        addButton(optionScreen,optionScreenCoords,button,WHITE,startY)
        mainScreen.blit(optionScreen,optionScreenCoords)
        display.update()
        time.wait(250)
        startY+=vertSpacing+TITLEFONT.size(button)[1]
        
    #Addinng main menu button
    addButton(optionScreen,optionScreenCoords,'Main Menu',WHITE,0,TEXTFONT,0)
    #Adding game screen button
    textWidth = TEXTFONT.size('Game Screen')[0]
    addButton(optionScreen,optionScreenCoords,'Game Screen', WHITE,0,TEXTFONT,width-10-textWidth)
    
    updateScreens()
    
# Removes all of the buttons
def removeButtons():
    global buttons,buttonAnimations ,buttonOrder,buttonText
    # Sets all the button varibles to nothing
    buttons = {}
    buttonText = []
    buttonAnimations = []
    buttonOrder = []
    
    
# Saves the current game
def saveGame():
    # Saves the time
    finalText = str(timer)+'\n'+difficulty+'\n'
    
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
    difficulty = rawLines[0]
    del rawLines[0]
    checkDifficulty()
    
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
    #If the tile doesnt have a number on it
    if [column,row] in highlightCenters or boardList[column][row] == [] or boardList[column][row] == 'X':
        #Display a warning and then exit the function
        warnings.append("Can't Highlight Here")
        warningTimes.append(FPS)
        return
    
    #Varibles for surrounding tiles
    surroundings = [[column-1,row],[column-1,row-1],[column,row-1],[column+1,row-1],[column+1,row],[column+1,row+1],[column,row+1],[column-1,row+1]]
    tempList = []
    #Loops throught every surrounding tile
    for tile in surroundings:
        #If the tile is on the board
        if tile[0]>=0 and tile[0]<boardSize and tile[1]>=0 and tile[1]<boardSize:
            #Adds the tile to a temporary list
            tileX = tile[0]*tileSize + tile[0]*tileBuffer
            tileY = tile[1]*tileSize + tile[1]*tileBuffer
            tempList.append([tileX,tileY])
            board.blit(highlight,(tileX,tileY))
            
    #Adds the temporary list to the main lists
    highlights.append(tempList)
    highlightTimes.append(timer+FPS*2)
    highlightCenters.append([column,row])
    
    
    
def loadImages():
    global FLAG_IMG,MINE_IMG,TILE_IMG,BROKENFLAG_IMG,LIGHTTILE_IMG,DARKTILE_IMG,highlight
    # Importing images
    FLAG_IMG = image.load('Images\Flag.png')
    MINE_IMG = image.load('Images\Mine.png')
    TILE_IMG = image.load('Images\Tile.png')
    BROKENFLAG_IMG = image.load('Images\Broken Flag.png')
    LIGHTTILE_IMG = image.load('Images\Light Tile.png')
    DARKTILE_IMG = image.load('Images\Dark Tile.png')
    
    # Resizing images
    FLAG_IMG = transform.scale(FLAG_IMG, (tileSize, tileSize))
    MINE_IMG.set_colorkey(WHITE)
    MINE_IMG = transform.scale(MINE_IMG, (tileSize, tileSize))
    TILE_IMG = transform.scale(TILE_IMG, (tileSize, tileSize))
    LIGHTTILE_IMG = transform.scale(LIGHTTILE_IMG, (tileSize, tileSize))
    DARKTILE_IMG = transform.scale(DARKTILE_IMG, (tileSize, tileSize))
    BROKENFLAG_IMG = transform.scale(BROKENFLAG_IMG, (tileSize, tileSize))
    
    highlight = Surface((tileSize,tileSize)) 
    highlight.set_alpha(128)             
    highlight.fill((255,0,0))
    
#Draws the highscore screen
def drawHighscoreScreen():
    highscoreScreen.fill(BLUE)
    #Draws title
    animateText(highscoreScreen,highscoreScreenCoords,width/2,35,30,"Highscores")
    
    #Adds main menu button
    textHeight = TEXTFONT.size('Main Menu')[1]+10
    addButton(highscoreScreen,highscoreScreenCoords,"Main Menu",WHITE,height-textHeight,TEXTFONT,0) 
    
    #Adds game screen Button
    textWidth,textHeight = TEXTFONT.size('Game Screen')
    addButton(highscoreScreen,highscoreScreenCoords,"Game Screen",WHITE,height-(textHeight+10),TEXTFONT,width-textWidth) 
    
    #Adds the current difficulty in the top left corner 
    highscoreScreen.blit(TEXTFONT.render(difficulty.upper(),True,WHITE),(5,5))
    
    #Draws the highscore then updates the screen
    drawHighscores()
    updateScreens()
    
#Draws the highscore chart
def drawHighscores():
    global cellWidth
    #Reading scores from files
    filename = 'Highscores/'+difficulty+'_scores.score'
    inputFile = open(filename,'r')
    rawData = inputFile.readlines()
    inputFile.close()
    names = [line.split(':')[0] for line in rawData]
    scores = [int(line.split(':')[1]) for line in rawData]
    if len(names) >8: del names[8:],scores[8:]#If there are too many highscores then delete the old ones
    #Getting coords for headers
    centerX = width/2
    textHeight = TEXTFONT.size('L')[1]+textBuffer
    y = (height-textHeight*(len(names)+1))/2
   
    #Determining the width of the cell based on the width of the text
    for name in names:
        if TEXTFONT.size(name)[0]+textMargin >cellWidth:
            cellWidth = TEXTFONT.size(name)[0]+textMargin
    
    #Drawing Headers
    draw.rect(highscoreScreen,GREEN,Rect(centerX-1-cellWidth,y,cellWidth,textHeight))
    draw.rect(highscoreScreen,GREEN,Rect(centerX+1,y,cellWidth,textHeight))
    draw.rect(highscoreScreen,BLACK,Rect(centerX-1-cellWidth,y,cellWidth*2+2,textHeight),2)
    draw.rect(highscoreScreen,BLACK,Rect(centerX-1,y,2,textHeight*(len(names)+1)),3)
    
    header1 = TEXTFONT.render('Names',True,WHITE)
    header1Width = header1.get_width()
    header2 = TEXTFONT.render('Times',True,WHITE)
    header2Width = header2.get_width()
    
    highscoreScreen.blit(header1,((centerX-cellWidth)+(cellWidth-header1Width)/2,y+textBuffer+2))
    highscoreScreen.blit(header2,(centerX+1+(cellWidth-header2Width)/2,y+textBuffer+2))
    
    #Drawing scores 
    for index in range(len(names)):
        col1X = centerX-1-cellWidth
        col2X = centerX+1
        y += textHeight
        draw.rect(highscoreScreen,BLACK,Rect(col1X,y,cellWidth,textHeight),2)
        draw.rect(highscoreScreen,BLACK,Rect(col2X,y,cellWidth,textHeight),2)
        
        nameText = TEXTFONT.render(names[index],True,WHITE)
        timeText = TEXTFONT.render(timeToString(scores[index]),True,WHITE)
        
        nameWidth = nameText.get_width()
        timeWidth = timeText.get_width()
    
        highscoreScreen.blit(nameText,(col1X+(cellWidth-nameWidth)/2,y+textBuffer/2))
        highscoreScreen.blit(timeText,(col2X+(cellWidth-timeWidth)/2,y+textBuffer/2))    
        
    #If there are no highscores then display "no highscores"
    if len(names) ==0:
        draw.rect(highscoreScreen, BLACK, Rect(centerX-1-cellWidth,y+textHeight,cellWidth*2+2,textHeight),2)
        
        col1X = centerX-1-cellWidth
        emptyText = TEXTFONT.render('No Highscores',True,BLACK)
        emptyTextWidth = emptyText.get_width()
        highscoreScreen.blit(emptyText,(col1X+(cellWidth*2-emptyTextWidth)/2,y+textHeight+textBuffer/2))
    
#Returns the current highscores 
def getHighscores():
    #reads the highscore file for the current difficulty
    filename = 'Highscores/'+difficulty+'_scores.score'
    inputFile = open(filename,'r')
    rawLines = inputFile.readlines()
    rawLines = [line.replace('\n','') for line in rawLines]#Cleans up the raw data
    scores = [int(line.split(':')[1]) for line in rawLines]#Extracts the scores and places them in a list
    
    #If there are no scores then add None to the list
    if len(scores) == 0:
        scores.append(None)
    return scores

def addHighscore(time):
    global highscores,stats
    moveScreens('endScreen')
    
    #If it is the highest score then show the new highsccore text
    if time<highscores[0] or highscores[0] == None:
        animateText(endScreen,endScreenCoords,width/2,150,50,"New Highscore")
        #If there was a new highscore set then change the stats that get displayed at the end screen
        if highscores[0] != None:
            stats = ["It Took You "+timeToText(timer),"You Clicked "+str(clicks)+checkPlural(' Time',clicks)+'.',"You beat the last highscore$ " ,"by "+ timeToText(highscores[0]-time)]
        else:
            stats = ["It Took You "+timeToText(timer),"You Clicked "+str(clicks)+checkPlural(' Time',clicks)+'.', "You set a new highscore."]
    else:
        stats = ["It Took You "+timeToText(timer),"You Clicked "+str(clicks)+checkPlural(' Time',clicks)+'.']
        
        
    #Getting the name of the player
    playerName = ""
    while playerName == "":
        playerName = inputbox.ask(mainScreen,endScreen, "Enter Your Name")
    
    #Reading highscore file
    filename = 'Highscores/'+difficulty+'_scores.score'
    inputFile = open(filename,'r')
    rawData = inputFile.readlines()
    inputFile.close()
    #Getting data from raw data
    names = [line.split(':')[0] for line in rawData]
    scores = [int(line.split(':')[1]) for line in rawData]
    
    #Adding the highscore to a string in the correct place (in order from fastest to slowest)
    saveString = ""
    added = False
    #loops through the old highscores
    for index in range(len(scores)):
        #Adds the new highscore in the correct spot 
        if time<scores[index] and added ==False:
            saveString += playerName+':'+str(time)+'\n'
            added=True
            
        saveString +=names[index]+':'+str(scores[index])+'\n'
        
        #Adds the highscore if it is the last iteration
        if index == len(scores)-1 and added == False:
            saveString += playerName+':'+str(time)+'\n'
            added=True
            
    #If there is no highscores then just add it
    if len(names) ==0:
        saveString += playerName+':'+str(time)+'\n'
    
    #Write the new scores to the file
    outfile = open(filename,'w')
    outfile.write(saveString)
    outfile.close()
    
    highscores = getHighscores()
    
    #Makes the 'fireworks' at random positions
    makeBurst(random.randint(10,width-10),random.randint(10,height-10),20)
    makeBurst(random.randint(10,width-10),random.randint(10,height-10),20)
    makeBurst(random.randint(10,width-10),random.randint(10,height-10),20)

    
#Automatically wins the game (used for debugging)
def autoWin():
    removeButtons()
    #Loops through every tile
    for column in range(boardSize):
        for row in range(boardSize):
            #If the tile is a mine the flag it
            if boardList[column][row] == 'X':
                flagList.append([column,row])
            #if it isn't a mine the open it
            else:
                checkTile(board, column, row)
                
    #Update the screen and check for the win
    drawBoard(board, boardList, boardSize, tileSize, tileBuffer)
    updateScreens()
    checkWin()
                
#Makes circle of lasers
def makeBurst(x,y,degrees):
    global laserBallCoords,laserBallX,laserBallY,laser,laserDead
    
    #Loops through 360 degrees and increments by passed amount
    for angle in range(0,360,degrees):
        #Declaring the needed local vairbles
        a = math.radians(angle)
        acelX = (laserMaxSpeed * math.cos(a))
        acelY = (laserMaxSpeed * math.sin(a))
        
        #Adding lobal varibles to global lists
        laserBallCoords = laserBallX,laserBallY = x,y
        laserCoords = [[[x,y]]]
        lasers.append(laserCoords[:])
        laserTimers.append(0)
        laserAcels.append([acelX,acelY])
        laser = True
        laserDead = False
    
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
highscoreScreen = Surface(SIZE)
currentScreen = menuScreen

# Filling all of the Surfaces
mainScreen.fill(WHITE)
menuScreen.fill(WHITE)
gameScreen.fill(WHITE)
highscoreScreen.fill(BLUE)
gameScreen.set_colorkey(WHITE)
endScreen.fill(BLUE)
optionScreen.fill(BLUE)
currentBgColour = WHITE

# Coordiantes for all of the Surfaces
boardCoords= [200,0]
gameScreenCoords = [width+20,20]
endScreenCoords = [width*2,0]
menuScreenCoords = [0,0]
optionScreenCoords = [width,height]
highscoreScreenCoords = [width,-height]
screenSlideSpeed = 5

# Declaring board varibles
difficulty = 'normal'
checkDifficulty()
tileBuffer = int(round(tileSize/20,0))
board = Surface((boardSize*tileSize + tileSize*tileBuffer ,boardSize*tileSize + tileSize*tileBuffer))
boardRect = Rect(addLists(boardCoords,gameScreenCoords),(boardSize*(tileSize + tileBuffer) ,boardSize*(tileSize + tileBuffer)))
board.fill(WHITE)
board.set_colorkey(WHITE)
NUMBERFONT = font.SysFont("Times New Roman", tileSize-5)
boardList = setupBoard()

# Declaring varibles for flags
flagList = []
numFlags = numMines
placedFlags = 0

#Declaring varibles for lasers
laserRadius = 10
lasers = []
laserAcels = []
laserTimers = []
laserDeadList = []
laserBallCoords = laserBallX,laserBallY = [width/2,height/2]
laserCoords = [[width/2,height/2]]
laserTrailLength = 25
laser = False
laserMaxSpeed =15
laserTimer = 0
laserLife = 2
laserDead = False


# Decalaring varibles for buttons
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
explosionSound = mixer.Sound('Sounds\Explosion.wav')

#Declaring highlight Varibles
highlights = []
highlightTimes = []
highlightCenters = []
highlight = Surface((tileSize,tileSize)) 
highlight.set_alpha(128)             
highlight.fill((255,0,0))

#Declaring highscore varibles
highscores = getHighscores()
cellWidth = width/4
textBuffer = 10
textMargin = 10

# General game varibles
gameOver = False
gameInProgress = False
win = False
timer = 0
clock = time.Clock()
running = True
clicks = 0
loadImages()


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
    if gameOver == False and currentScreen == gameScreen:
        timer +=1
    
    for evnt in event.get():
        
        if evnt.type == QUIT:
            # If there is a game in progress then save it
            if gameInProgress and numberOfUnopendTiles(True) < boardSize**2:                
                saveGame()
            running = False
            
        #If the left mouse button was clicked
        if evnt.type == MOUSEBUTTONDOWN and mouse.get_pressed()[0]: 
            clicks+=1
            #Determine which tile the mouse is on
            col = int((mousePos[0]-(boardCoords[0]+gameScreenCoords[0]))/(tileSize+tileBuffer))
            row = int((mousePos[1]-(boardCoords[1]+gameScreenCoords[1]))/(tileSize+tileBuffer))
            
            #If the mouse is on the board and the player is on the game screen
            if boardRect.collidepoint(mousePos) and currentScreen == gameScreen:
                #If the tile is not flagged
                if [col,row] not in flagList:
                    #Checks the tile then draws the board and flags
                    checkTile(board, col, row)
                    drawBoard(board, boardList, boardSize, tileSize, tileBuffer)
                    drawFlags(board, flagList)
                    
            #Checks the buttons incase they were clicked
            checkButtons()
            
        #If the middle mouse button is clicked
        if evnt.type == MOUSEBUTTONDOWN and mouse.get_pressed()[1]:
            #Determine which tile the mouse is on
            col = int((mousePos[0]-(boardCoords[0]+gameScreenCoords[0]))/(tileSize+tileBuffer))
            row = int((mousePos[1]-(boardCoords[1]+gameScreenCoords[1]))/(tileSize+tileBuffer))
            
            #If the tile is number then highlight the tile
            if boardList[col][row] != [] or boardList[col][row] != 'X' :
                if boardList[col][row] >0:
                    highlightTile(col,row)
            
        #The right mouse button was pressed
        if evnt.type == MOUSEBUTTONDOWN and mouse.get_pressed()[2]:
            clicks+=1
            #Determine which tile the mouse is on
            col = int((mousePos[0]-(boardCoords[0]+gameScreenCoords[0]))/(tileSize+tileBuffer))
            row = int((mousePos[1]-(boardCoords[1]+gameScreenCoords[1]))/(tileSize+tileBuffer))
                
           #If the mouse is on the board
            if boardRect.collidepoint(mousePos):
                #If there is a flag on the tile then remove it
                if [col,row] in flagList:
                    flagList.remove([col,row])
                #If there isn't a flag  
                else:
                    #If there are flags left
                    if placedFlags < numMines:
                        #If the tile is unopened
                        if boardList[col][row] == [] or boardList[col][row] == 'X' :
                            #Add the flag to the list and then update the board
                            flagList.append([col,row])
                            drawBoard(board, boardList, boardSize, tileSize, tileBuffer)
                            drawFlags(board, flagList)
                    #If there are no flags left
                    else:
                        #Display the No flags warning
                        warnings.append('No Flags Left')
                        warningTimes.append(2*FPS)
        
        #Used for debugging purposes to win instantly  
        if evnt.type == KEYDOWN and evnt.key ==K_r:
            autoWin()
   
    #Updating the board and the flags
    placedFlags = len(flagList)
    drawBoard(board, boardList, boardSize, tileSize, tileBuffer)
    drawFlags(board, flagList)
            
    #If there are no flags left and there are no unopened tiles left then check if the game is over
    if placedFlags ==numMines and numberOfUnopendTiles() == 0:
        checkWin()       
            
    #Drawing button text
    for rawData in buttonText:
        blitter = rawData[4].render(rawData[1],True,rawData[3])
        draw.rect(rawData[0],currentBgColour,Rect(rawData[2],(blitter.get_width(),blitter.get_height())))
        rawData[0].blit(blitter,rawData[2])
        
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
            rectWidth = animationRect.width
            rectHeight = animationRect.height
            # if the rectangle is smaller than button then update the width      
            if rectWidth < collisionRect.width:           
                buttonAnimations[buttonIndex] = Rect(x,y,rectWidth+buttonAnimationSpeed,rectHeight)
        else:

            # Making rectangle smaller if the mouse is not on the button
            animationRect = buttonAnimations[buttonIndex]
            x = animationRect.x
            y = animationRect.y
            rectWidth = animationRect.width
            rectHeight = animationRect.height
            # If the rectangle's width is greater than 0 then update the width  
            if rectWidth >0:
                buttonAnimations[buttonIndex] = Rect(x,y,rectWidth-buttonAnimationSpeed,rectHeight)
            
                
        ##### The rectangles that animate under the buttons#####
        
        
        textColour = buttonText[buttonIndex][3]
        # Calculating the multipliers for the colours to make the bar fade in and out
        redMulti = float((textColour[0])-currentBgColour[0])/(buttons[buttonName].width + buttonAnimationSpeed)
        greenMulti = float((textColour[1])-currentBgColour[1])/(buttons[buttonName].width + buttonAnimationSpeed)
        blueMulti = float((textColour[2])-currentBgColour[2])/(buttons[buttonName].width + buttonAnimationSpeed)
        
        # Making the new colour based on the width of the rectangle
        barColour = (currentBgColour[0]+animationRect.width*redMulti,currentBgColour[1]+animationRect.width*greenMulti,currentBgColour[2]+animationRect.width*blueMulti)

        # Drawing the rectangles        
        draw.rect(currentScreen,currentBgColour, Rect(animationRect.x,animationRect.y,buttons[buttonName].width + buttonAnimationSpeed,animationRect.height))
        draw.rect(currentScreen, barColour ,animationRect)       
        
    
    
    
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
            stats = ["It Took You "+timeToText(timer),"You Clicked "+str(clicks)+checkPlural(' Time',clicks)+'.', "You Flagged "+str(checkCorrectFlags()) + checkPlural(' Mine',checkCorrectFlags()) + ' out of '+str(numMines)+' mines.']
            drawEndScreen(endScreen,ENDSCREENBG,'YOU LOSE',stats)
            
        removed +=1
        
    ############Drawing Highlights############
        
    for square in highlights:
        for coord in square:
            col = coord[0]/(tileSize+tileBuffer)
            row = coord[1]/(tileSize+tileBuffer)
            if boardList[col][row] ==[] or boardList[col][row] =='X':
                board.blit(highlight,coord)
            
    if len(highlights) >0:
        if  timer>=highlightTimes[0]:
            del highlights[0],highlightTimes[0],highlightCenters[0]
        
    # Functions that need to run every iteration of the loop
    drawFlagsLeft(gameScreen,0 ,0 ,numFlags-placedFlags)
    displayStats(timer)
    displayWarning(gameScreen)
    width,height  =SIZE
    
        
        
     # Drawing all surfaces to the main screen
    if not win:
        draw.rect(mainScreen,GRAY, boardRect)
    updateScreens(False)    
    
    # Drawing shrapnel
    for rawCoords in explosions:
        draw.circle(mainScreen, ORANGE, rawCoords[0], 3)
        
    #######################Lasers###########################
    if laser:
        #Loops though every lasaer    
        for index in range(len(lasers)):
            laserDead = False
            #If the laser is not 'dead'
            if lasers[index] != 'X':
                #Declaring the varibles that will be changed
                laserCoords = lasers[index]
                acelX = laserAcels[index][0]
                acelY = laserAcels[index][1]
                laserTimer = laserTimers[index]
                if len(laserCoords)>0:
                    laserBallCoords = laserBallX,laserBallY = laserCoords[-1][0]
                    
                #Checks if the laser should be laserDead
                if laserTimer/FPS >=laserLife:
                    laserDead = True
                    
                #Increments laserTimer
                laserTimer +=1
                
                #Checks collision on X
                if laserBallX + laserRadius >=width:
                    acelX*=-1
                     
                elif laserBallX - laserRadius <=0:
                    acelX*=-1
    
                #Checks colliosion on Y
                if laserBallY + laserRadius >=height:
                     
                    acelY*=-1
                    
                elif laserBallY - laserRadius <=0:
                    acelY*=-1
                     
                #If the laser is not dead
                if not laserDead:
                    #Update the coordinates
                    laserBallCoords = laserBallX,laserBallY = [laserBallCoords[0]+acelX,laserBallCoords[1]+acelY]
                    #If the laser is too short then make it longer else make it shorter
                    if len(laserCoords)<laserTrailLength:
                        laserCoords[-1].append([laserBallCoords[0],laserBallCoords[1]])
                        laserCoords.append([[laserBallCoords[0],laserBallCoords[1]]])
                        
                    else:
                        #Making the laser shorter
                        del laserCoords[0]
                        laserCoords[-1].append([laserBallCoords[0],laserBallCoords[1]])
                        laserCoords.append([[laserBallCoords[0],laserBallCoords[1]]])
                        
                    #Draws the laser
                    for colourIndex in range(len(laserCoords)-1):
                            coords = laserCoords[colourIndex]
                            #Calculates colour
                            colour = math.fabs(random.randint(0,255)-(255/len(laserCoords))*laserCoords.index(coords))
                            colour = [255,colour,0]
                            draw.line(mainScreen,colour,coords[0],coords[1],3)
                            
                #If the laser is laserDead        
                else:
                    #Update coords
                    laserBallCoords = laserBallX,laserBallY = [laserBallCoords[0]+acelX,laserBallCoords[1]+acelY]
                    
                    #If the laser is not fully gone
                    if len(laserCoords)>0:
                        #Make the laser shorter
                        laserCoords[-1].append([(laserBallCoords[0]),(laserBallCoords[1])])
                        laserCoords.append([[(laserBallCoords[0]),(laserBallCoords[1])]])
                        laserBallCoords = laserBallX,laserBallY = [laserBallCoords[0]+acelX,laserBallCoords[1]+acelY]
                        del laserCoords[:2]
                      
                        #Draws the laser
                        for colourIndex in range(len(laserCoords)-1):
                            coords = laserCoords[colourIndex]
                            #Calculates colour
                            colour = math.fabs(random.randint(0,255)-(255/laserTrailLength)*laserCoords.index(coords))
                            colour = [255,colour,0]
                            draw.line(mainScreen,colour,coords[0],coords[1],3)
                            
                    #If there is nothing left of the laser
                    else:
                        #Updates varibles to show that laser is laserDead
                        laserTimer = 0
                        lasers[index] = 'X'
                        laserDead = False
                        #Some extra error proofing
                        if len(lasers) == 0:
                            lasers = []
                            laser = False
                            break
                #Updates all of the varibles
                laserAcels[index][0]=acelX  
                laserAcels[index][1]=acelY  
                laserTimers[index] = laserTimer
                
    
    # Updating the Screen
    display.flip()
        


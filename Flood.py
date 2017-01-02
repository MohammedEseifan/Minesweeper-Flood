                            # # # # # # # # # # # # # # #
                            # #         Flood         # # 
                            # #  By: Mohammed Eseifan # # 
                            # # # # # # # # # # # # # # # 
from pygame import *
import random,sys,os
init()

#Setups up the symmetrical board
def setupBoard(boardSize):
    global fullList,playerSpots    
 
    #Makes half of the list to be reflected
    halfList = [[[] for x in range(boardSize/2)] for y in range(boardSize)]#creating empty 2D list
    #List that contains the position that each player owns
    playerSpots = [[[] for x in range(boardSize)] for y in range(boardSize)]
    
    #Fills half of the list with random colours
    for column in range(len(halfList)):
        for row in range(len(halfList)/2):
            randIndex = random.randint(0,len(boardColours)-1)
            halfList[column][row] = boardColours[randIndex]
           
    #Makes a full list
    halfList[-1][0] = WHITE
    fullList = []
    
    #Flipping the board along the X-Axis
    for column in range(len(halfList)):
        tempRow = []
        for row in halfList[column]:
            tempRow.append(row)
        fullList.append(tempRow)
        
    #Flipping the board along the Y-Axis
    for column in range(len(fullList)):
        temp = halfList[-1-column][::-1]
        for item in temp:
            fullList[column].append(item)
            

#Draws the board
def drawBoard(x,y,player):
    
    lines = []
    colours = []
    #Loops through every tile and draws it
    for column in range(len(fullList)):
        for row in range(len(fullList[0])):
            #Calculating the X and Y for each tile and draws the tile
            tileX = x + (tileSize+tileSpacing)*column
            tileY = y + (tileSize+tileSpacing)*row
            colour = fullList[column][row]
            draw.rect(mainScreen,colour,Rect(tileX,tileY,tileSize,tileSize))
            
            #Declares varibles to make it easier to outline the blocks
            topLeft = (tileX,tileY)
            topRight = (tileX+tileSize,tileY)
            bottomLeft = (tileX,tileY+tileSize)
            bottomRight = (tileX+tileSize,tileY+tileSize)
            
            if playerSpots[column][row] == player:
                mainScreen.blit(highlight,(tileX,tileY))
            elif playerSpots[column][row] !=[]:
                mainScreen.blit(shadow,(tileX,tileY))
            
            #Draws the outline around the blocks (hard to explain in comments, the comments would be as long as the program)
            for i in range(2):
                playerTurn = (player +i)%2
                edgeRow = False
                edgeCol = False
                
                #Draws the top and bottom outline on the border tiles
                if row ==0:
                    edgeRow = True
                    #Draws top line
                    if playerSpots[column][row] == playerTurn:
                        lines.append([topLeft,topRight])
                        #Adds what colour the line should be 
                        if playerTurn != player:
                            colours.append(LIGHTGRAY)
                        else:
                            colours.append(WHITE)
                    #Draws bottom line    
                    if playerSpots[column][row+1] != playerTurn and playerSpots[column][row] == playerTurn:
                        lines.append([bottomLeft,bottomRight])
                        if playerTurn != player:
                            colours.append(LIGHTGRAY)
                        else:
                            colours.append(WHITE)
                       
                if row == boardSize-1:
                    edgeRow = True
                    if playerSpots[column][row] == playerTurn:                
                        lines.append([bottomLeft,bottomRight])
                        if playerTurn != player:
                            colours.append(LIGHTGRAY)
                        else:
                            colours.append(WHITE)
                        
                    if playerSpots[column][row-1] != playerTurn and playerSpots[column][row] == playerTurn:
                        lines.append([topLeft,topRight])
                        if playerTurn != player:
                            colours.append(LIGHTGRAY)
                        else:
                            colours.append(WHITE)
                #Draws the lines around the outer 
                if column ==0:
                    edgeCol= True
                    if playerSpots[column][row] == playerTurn:
                        lines.append([topLeft,bottomLeft])
                        if playerTurn != player:
                            colours.append(LIGHTGRAY)
                        else:
                            colours.append(WHITE)
                        
                    if playerSpots[column+1][row] != playerTurn and playerSpots[column][row] == playerTurn:
                        lines.append([topRight,bottomRight])
                        if playerTurn != player:
                            colours.append(LIGHTGRAY)
                        else:
                            colours.append(WHITE)
                    
                if column ==boardSize-1: 
                    edgeCol = True
                    if playerSpots[column][row] == playerTurn:
                        lines.append([topRight,bottomRight])
                        if playerTurn != player:
                            colours.append(LIGHTGRAY)
                        else:
                            colours.append(WHITE)
                        
                    if playerSpots[column-1][row] != playerTurn and playerSpots[column][row] == playerTurn:
                        lines.append([topLeft,bottomLeft])
                        if playerTurn != player:
                            colours.append(LIGHTGRAY)
                        else:
                            colours.append(WHITE)
                    
                
                if edgeCol == False:
                    if playerSpots[column-1][row] != playerTurn and playerSpots[column][row] == playerTurn:
                        lines.append([topLeft,bottomLeft])
                        if playerTurn != player:
                            colours.append(LIGHTGRAY)
                        else:
                            colours.append(WHITE)
                        
                    if playerSpots[column+1][row] != playerTurn and playerSpots[column][row] == playerTurn:
                        lines.append([topRight,bottomRight])
                        if playerTurn != player:
                            colours.append(LIGHTGRAY)
                        else:
                            colours.append(WHITE)
                    
                if edgeRow == False:
                    if playerSpots[column][row-1] != playerTurn and playerSpots[column][row] == playerTurn:
                        lines.append([topLeft,topRight])
                        if playerTurn != player:
                            colours.append(LIGHTGRAY)
                        else:
                            colours.append(WHITE)
                        
                    if playerSpots[column][row+1] != playerTurn and playerSpots[column][row] == playerTurn:
                        lines.append([bottomLeft,bottomRight])
                        if playerTurn != player:
                            colours.append(LIGHTGRAY)
                        else:
                            colours.append(WHITE)
                
                    
        for coords in lines:
            draw.line(mainScreen,colours[lines.index(coords)],coords[0],coords[1],2)
                    
#Draws the current score          
def drawStats():
    #Renders the text then places it on the screen
    p1Text = TEXTFONT.render("P1: "+str(countSquares(0)),True,WHITE)
    p2Text = TEXTFONT.render("P2: "+str(countSquares(1)),True,WHITE)
    p2TextWidth = p2Text.get_width()
    p2TextHeight = p2Text.get_height()
    p1TextHeight = p1Text.get_height()
    
    moveText= TEXTFONT.render("Moves: "+str(moves), True, WHITE)
    turnText = TEXTFONT.render("P"+str(playerTurn+1)+"'s Turn", True, WHITE)
    turnTextWidth = turnText.get_width()
    
    mainScreen.blit(p1Text,(0,height-p1TextHeight))
    mainScreen.blit(p2Text,(width-p2TextWidth,height-p2TextHeight))
    mainScreen.blit(turnText, (width-(turnTextWidth+5),0))
    mainScreen.blit(moveText, (0,0))
   
    
    
    
    
#Expands the tiles around the current tile
def  expandTile(player,inputCoords,oldColour,newColour):
    global playerSpots
    #Gets the column and row from the passed arguments
    col = inputCoords[0]
    row = inputCoords [1]
    if col>=0 and row>=0 and col<=boardSize-1 and row <=boardSize-1:
        
        #If the current tile is the old colour then make it the new colour
        otherPlayer = (player+1)%2
        if fullList[col][row] == newColour:
            #If the tile is not owned by the other player then change the colour
            if playerSpots[col][row] !=otherPlayer:
                playerSpots[col][row] = player
                fullList[col][row] = newColour
                        
                #Checks the surrounding tiles (recursive part of the function)
                surroundings = [[col,row-1],[col+1,row],[col,row+1],[col-1,row]]
                for coords in surroundings:
                    #If the tile is in the board
                    if coords[0]>=0 and coords[1]>=0 and coords[1]<=boardSize-1 and coords[0] <=boardSize-1:
                        #If the tile is not owned by other player and it is the colour that needs to be absorbed then call the function again
                        if playerSpots[coords[0]][coords[1]] == [] and fullList[col][row] == newColour:
                            expandTile(player,coords,newColour,newColour) 
                        
        #If the colour has already been absorbed or it is the starting spot then absorb it 
        elif fullList[col][row] == oldColour or fullList[col][row]== WHITE:
            #If the tile is not owned by the other player
            if playerSpots[col][row] !=otherPlayer:
                fullList[col][row] = newColour
               
                playerSpots[col][row] = player
                surroundings = [[col,row-1],[col+1,row],[col,row+1],[col-1,row]]
                #Calls the function on all the surrounding tiles
                for coords in surroundings:
                    expandTile(player,coords,oldColour,newColour)
                    
        
#Checks to see if a player has won                
def checkWin(player):
    #Loops through every tile 
    for col in range(len(fullList)):
        for row in range(len(fullList)):
            #Checks the surrounding tiles
            surroundings = [[col,row-1],[col+1,row],[col,row+1],[col-1,row]]
            for coords in surroundings:
                #if the tile is on the board
                if coords[0]>=0 and coords[1]>=0 and coords[1]<=boardSize-1 and coords[0] <=boardSize-1:
                    #Makes a list of 2 adjacent tiles
                    pair= [playerSpots[col][row],playerSpots[coords[0]][coords[1]]]
                    #If there is another move avalible then no one has won yet
                    if player in pair and [] in pair:
                        return False
                    
    #If the function has not exited yet then someone has won                
    return True
            
#Displays the winner
def displayWinner():
    #Declaring counter varibles
    p1 = 0
    p2 = 0
    differnce = 0
    #Loops through every tile
    for col in range(len(fullList)):
        for row in range(len(fullList)):
            #Increments the respective counter
            if playerSpots[col][row] ==0:
                p1 +=1
            elif playerSpots[col][row] ==1:
                p2 +=1
                
    #Determines the winner and the differnce
    if p1 >p2 :
        differnce = p1-p2
        text = "Player 1 Has Won!"
    elif p2>p1:
        differnce = p2-p1
        text = "Player 2 Has Won!"
    elif p1==p2:
        text = "It Is A Tie!"
        
    #Draws the text to the screen
    BIGFONT  = font.Font("GODOFWAR.TTF",50)
    textRender = BIGFONT.render(text, True, WHITE)
    textWidth = textRender.get_width()
    textHeight = textRender.get_height()
    x = (width-textWidth)/2
    y = (height-textHeight)/2
    
    differnceText = TEXTFONT.render("Difference: "+str(differnce),True,WHITE)
    difWidth = differnceText.get_width()
    difHeight = differnceText.get_height()
    mainScreen.blit(differnceText,((width-difWidth)/2,height-difHeight))
    
    
    mainScreen.blit(textRender, (x,y))
    display.update()
    time.wait(5000)
    
    
#Countes the number of spots owned by a player
def countSquares(player):
    #Counter varible
    count = 0
    
    #Loops though every tile
    for col in range(len(fullList)):
        for row in range(len(fullList)):
            #If it is owned by the specified player then increment the counter
            if playerSpots[col][row] ==player:
                count +=1
    #Return the counter
    return count

#Resets the board
def resetGame():
    global moves,playerScore,playerList,playerTurn,frames,playerSpots
   
    #Resets all of the varibles to thier defaults
    moves = 0
    playerScore = [0,0]
    playerList = [[0,boardSize-1],[boardSize-1,0]]
    playerTurn = -1
    frames = 0
    setupBoard(boardSize)
    randomize()
    
    
def showHelp():
    fileNames = os.listdir('Instructions\Flood')
    listOfImages = [image.load('Instructions\Flood\\'+filename) for filename in fileNames]
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
                display.set_caption('Flood')
                return randomize()
                
        if currentImage >= len(listOfImages):
            display.set_caption('Flood')
            return randomize()
        
        display.set_caption(fileNames[currentImage].split('.')[0])
        mainScreen.blit(listOfImages[currentImage],(0,0))
        display.update()
    
    display.set_caption('Flood')
    randomize()
    
#Randomizes who goes first
def randomize():
    #Displays instructions
    mainScreen.fill(BLACK)
    textBlit =TEXTFONT.render("Pick Heads or Tails. Click to flip",True,WHITE)
    x,y = (width-textBlit.get_width())/2,10
    mainScreen.blit(textBlit,(x,y))
    
    helpText = TEXTFONT.render('Help',True,WHITE)
    textHeight = helpText.get_height()
    mainScreen.blit(helpText,(5,height-textHeight))
    
    helpRect = Rect(0,height-textHeight,helpText.get_width(),textHeight)
    display.update()
    clicked = False
    
    #Loops until mouse is clicked
    while clicked==False:
        clock.tick(10)
        for evnt in event.get():
            #If they quit then exit
            if evnt.type == QUIT:
                global running 
                running = False
                mainScreen.fill(BLACK)
                return
            
            #Checks for a mouse clicked event
            if evnt.type == MOUSEBUTTONDOWN and mouse.get_pressed()[0]:
                if helpRect.collidepoint(mouse.get_pos()):
                    return showHelp()
                    
                else:
                    #Stop looping
                    clicked = True
                    break
                
    #Shows count down
    for number in range(3,0,-1):
        #Printing text to screen
        mainScreen.fill(BLACK)
        textBlit =TEXTFONT.render(str(number),True,WHITE)
        x,y = (width-textBlit.get_width())/2,(height-textBlit.get_height())/2
        mainScreen.blit(textBlit,(x,y))
        display.update()
        time.wait(500)
    
    #Makes random number for heads or tails
    mainScreen.fill(BLACK)
    rand = random.randint(0,100)
    
    #Displays heads or tails based on the random number
    if rand <50:
        textBlit =TEXTFONT.render("HEADS",True,WHITE)
    elif rand>=50:
        textBlit =TEXTFONT.render("TAILS",True,WHITE)
    #Draws text to screen
    x,y = (width-textBlit.get_width())/2,(height-textBlit.get_height())/2
    mainScreen.blit(textBlit,(x,y))
    display.update()
    time.wait(2000)
    
                
          #######################Main Varibles#######################    
    
#Declaring all of the colours     
RED=(255,0,0)
PINK=(255,125,255)
DARKRED= (155,0,0)
GREEN=(0,255,0)
BLUE=(0,170,230)
BLACK=(0,0,0)
GRAY=(100,100,100)
LIGHTGRAY = PINK
WHITE = (255,255,255)
YELLOW = (255,255,0)
PURPLE = (138,43,226)
SIZE = width,height = (600, 600)
mainScreen = display.set_mode(SIZE)
mainScreen.fill(BLACK)
FPS = 24
clock = time.Clock()


#Board varibles
tileSpacing =0 
boardSize = 40
boardColours = [RED,BLUE,GREEN,PURPLE]
tileSize = (width-100)/boardSize

#Button varibles
buttonSize = 40
buttonSpacing = 10
buttons = []

#Highlight vairbles
highlight = Surface((tileSize,tileSize)) 
highlight.set_alpha(64)             
highlight.fill((255,255,255))
shadow = Surface((tileSize,tileSize)) 
shadow.set_alpha(64)             
shadow.fill((0,0,0))

#Varibles to keep track of players
playerList = [[0,boardSize-1],[boardSize-1,0]]
playerTurn = 0
playerScore = [0,0]
moves = 0

#General game varibles
frames = 0
boardx, boardy = (width-boardSize*(tileSize+tileSpacing))/2,(height-boardSize*(tileSize+tileSpacing))/2 -buttonSize*.3
boardBottom = boardy+boardSize*(tileSize+tileSpacing)
running  = True

#Importing requirements
TEXTFONT  = font.Font("SLANT.TTF",30)
icon = image.load('Images\Flood Icon.jpg')

#Initializing board and screen
display.set_icon(icon)
display.set_caption('Flood')
setupBoard(boardSize)
randomize()

#Laying out the butttons
for index in range(len(boardColours)):
        x = (width-(buttonSize+buttonSpacing)*len(boardColours))/2 + buttonSize*index + buttonSpacing*index
        y = (boardBottom +((height-boardBottom)/2))- buttonSize/2
        buttons.append(Rect(x,y,buttonSize, buttonSize))
        

while running:
    frames+=1
    clock.tick(FPS)
    mainScreen.fill(BLACK)
    
    #Loops through every ecent
    for evnt in event.get():
        #If they quit then exit
        if evnt.type == QUIT:
            running = False
            
        #if they click    
        if evnt.type == MOUSEBUTTONDOWN and mouse.get_pressed()[0]:
            #Loops though every button
            for button in buttons:
                #If they clicked on a button
                if button.collidepoint(mouse.get_pos()):
                    
                    colour = fullList[playerList[playerTurn][0]][playerList[playerTurn][1]]#Gets the current colour of the player
                    #If they're picking a new colour
                    if boardColours[buttons.index(button)] != colour:
                        #Expand the tile 
                        moves+=1
                        expandTile(playerTurn,playerList[playerTurn],colour,boardColours[buttons.index(button)])
                        
                        #Checks if anyone has won
                        if checkWin((playerTurn+1)%2) and moves >2:
                            #Draws the results if anyone has won
                            drawBoard(boardx, boardy,playerTurn)
                            drawStats()
                            displayWinner()
                            resetGame()
                        #Increments the player counter
                        playerTurn +=1
                        playerTurn = playerTurn%2
                        

        elif evnt.type == KEYDOWN:
            if evnt.key ==K_1:
                print "TT"
                        
    #Draws the buttons
    for rect in buttons:
        draw.rect(mainScreen,boardColours[buttons.index(rect)],rect)

    #Draws the board and statistics
    drawBoard(boardx, boardy,playerTurn)
    drawStats()
    
    #Updates the screen    
    display.update()

    
    

from Tkinter import *
import tkMessageBox
import tkSimpleDialog
import random

class Domino:

    def __init__(self, value = "00", size = 35):
        self.value = str(value)

        self.size = size
        self.radius = self.size / 5
        self.gap = self.radius / 2
        #custom property used for scaling (relative size)
        self.relSize = (4 * self.gap) + (6 * self.radius)
        self.inHand = False
        self.isSelected = False

    def __str__(self):
        return self.value

    def initDie(self):
        self.die1 = Die()
        self.die1.value = int(self.value[0])
        self.die2 = Die()
        self.die2.value = int(self.value[1])        
    
    def displayValue(self, canvas, vertical = True, faceUp = True, x = 20, y = 20, swapped = False):
        valueDie1 = int(self.value[0])
        valueDie2 = int(self.value[1])
        if faceUp:
            if swapped:
                valueDie1, valueDie2 = valueDie2, valueDie1
        else: # face down, dont show values
            valueDie1 = 0
            valueDie2 = 0
        self.drawDie(canvas, x, y, valueDie1)
        if vertical:                        
            self.drawDie(canvas, x, y + self.relSize, valueDie2)
        else:
            self.drawDie(canvas, x + self.relSize, y, valueDie2)
            
    def setValue(self):
        print ""
        
    #Author:    Abdul Wahab Derh
    #Date:      April 30th, 2013
    #Purpose:   Draws the die when given the canvas, and the x and y coordinates of the top corner
    #Inputs     canvas - The canvas object to draw to, x - the x-coordinate of the top left of the containing rectangle, y - the y-coordinate of the top left of the containing rectangle
    #Output     None   -     But the canvas will have a die drawn onto it
    def drawDie(self, canvas, x = 20, y = 20, value = 0):        
        ID = canvas.create_rectangle(x, y, x + self.relSize, y + self.relSize, fill="white", width=3);
        if self.isSelected:
            canvas.itemconfig(ID, outline="yellow")
        if self.inHand:
            canvas.tag_bind(ID,'<ButtonPress-1>', lambda x: handClicked(x, self.value))
        if value > 0:            
            if (value == 1 or value == 3 or value == 5): # middle dot
                self.drawDieDot(canvas, x, y, 2, 2);
            if (value == 2 or value == 3 or value == 4 or value == 5 or value == 6): # top left and bottom right dots
                self.drawDieDot(canvas, x, y, 1,1);
                self.drawDieDot(canvas, x, y, 3,3);            
            if (value == 5 or value == 6 or value == 4):  # bottom left and top right dots
                self.drawDieDot(canvas, x, y, 1,3);
                self.drawDieDot(canvas, x, y, 3,1);   
                if (value == 6): #middle left and middle right dots
                    self.drawDieDot(canvas, x, y, 1,2);
                    self.drawDieDot(canvas, x, y, 3,2);   

    #Author:    Abdul Wahab Derh
    #Date:      April 30th, 2013
    #Purpose:   a dot on a die based on the convential 3 by 3 grid of dice
    #Inputs:    canvas - The canvas object to draw to, startX - the top-left coordinate of the containing square,
    #           startY - the top-left coordinate of the containing rectangle, gridX - the x coordinate of a virtual die grid
    #           gridY - the y coordinate of a vritual die grid.
    #Concept:   Mr.Smith - Thanks alot :D
    #Credits
    # Die Grid:
    #               ------------------------
    #               |       |       |       |           JUST LIKE THE COMPUTER COORDINATE SYSTEM, START ON THE TOP-LEFT BUT WITH (1,1)...(3,3)
    #               | (1,1) | (1,2) | (1,3) |
    #               |       |       |       |    
    #               |-------|-------|-------|
    #               |       |       |       |    
    #               | (2,1) | (2,2) | (2,3) |
    #               |       |       |       |    
    #               |-------|-------|-------|
    #               |       |       |       |    
    #               | (3,1) | (3,2) | (3,3) |
    #               |       |       |       |    
    #               ------------------------
    def drawDieDot(self, canvas, startX = 20, startY = 20, gridX = 1, gridY = 1):
        xPos = startX + (self.gap * float(gridX)) + (self.radius * 2.0 * float(gridX - 1)) # add gaps and the number of dies in between
        yPos = startY + (self.gap * float(gridY)) + (self.radius * 2.0 * float(gridY - 1))
        # create oval within the virtual die grid
        #               start: top-left
        ID = canvas.create_oval(xPos, yPos, xPos + 2 * self.radius, yPos + 2 * self.radius, fill = "black")
        if self.inHand:
            canvas.tag_bind(ID,'<ButtonPress-1>', lambda x: handClicked(x, self.value))
        

class Hand:

    def __init__(self, hand = None, size = 0):
        if hand == None:
            # create a NEW list reference each time, this way extra calls does not result in hand objects using the same array
            # that is why this is not in the hand default parameter. Maybe there is a workaround? Not one we could find
            hand = [] 
        self.hand = hand
        self.size = size

        self.selected = None
        self.selectedIndex = -1

    def __str__(self):
        string = "Hand: "
        for domino in self.hand:
            string += str(domino) + " "
        string += " size: " + str(self.size)
        return string

    def clearHand(self):
        self.hand = []
        self.size = 0

    def getDominoByValue(self, value = "00"):
        for index in range(0, self.size):
            if self.hand[index].value == value:
                return index

    def getDomino(self, index = 0):
        if index > -1 and index < self.size:
            return self.hand[index]    


    def addDomino(self, domino):
        # check if object being added is a Domino object
        if isinstance(domino, Domino):
            # we will insert in order
            # add to end, which can be kept if req'd
            self.hand.append(domino)
            domino.inHand = True            
            if self.size > 0: # if there where values before this
                index = 0
                while index < self.size: # loop until end of list (before added value)
                    #check if there is a value in between that list that has a lower value
                    if domino.value < self.hand[index].value:
                        # if it does, add it to where it belongs
                        del self.hand[self.size]
                        self.hand.insert(index, domino)                        
                        index = self.size
                    else:
                        index += 1        
            self.size += 1
            self.updateSelected(-1)            

    def removeDomino(self, index = 0):
        domino = self.hand[index]
        domino.inHand = False
        self.size -= 1
        del self.hand[index]
        self.updateSelected(-1)        

    def updateSelected(self, selectedIndex = 0):
        # set current selected value to unselected
        if self.selected != None:
            self.selected.isSelected = False # this is letting the domino know that it is not selected
        selected = None 
        # determine new selected value
        if self.size > 0:
            if selectedIndex < 0:
                selectedIndex = self.size - 1
            if selectedIndex >= self.size: # if it's greater than size, set it to the first value
                selectedIndex = 0
            selected = self.hand[selectedIndex]
        # set new domino to selected               
        self.selected = selected
        if self.selected != None:
            self.selectedIndex = selectedIndex
            self.selected.isSelected = True

    def selectNext(self):
        self.updateSelected(self.selectedIndex + 1) # validation will be done by updateSelected

    def selectPrevious(self):
        self.updateSelected(self.selectedIndex - 1)
        
        
    def displayHand(self, canvas, vertical = True, faceUp = True, x = 10, y = 10, start = 0, end = -1):
        if end == -1:
            end = self.size
        if DEBUG:
            print "[hand]drawing from: ", start, " to ", end
        realStart = 0
        for index in range(start, end):            
            domino = self.hand[index]
            spacing = ((domino.relSize + 10) * realStart)
            if vertical:
                spacing = spacing + x
                domino.displayValue(canvas, vertical, faceUp, spacing, y)              
            else:
                spacing = spacing + y
                domino.displayValue(canvas, vertical, faceUp, x, spacing)
            realStart += 1
            
    def isAnythingSelected(self):
        isSelected = True
        if self.selected == None:
            isSelected = False
        return isSelected

    def removeSelected(self):
        if self.isAnythingSelected():
            self.removeDomino(self.selectedIndex) # this resets the selected value in the domino as well

class Table:

    def __init__(self, domino = None):
        self.table = []
        self.order = []
        self.size = 0        
        if domino != None:
            self.insertRight(domino)
            
    def __str__(self):
        string = "Size: " + str(self.size) + "|"
        for domino in self.table:
           string += str(domino.value) + " "
        return string

    def insert(self, domino, right = True):
        # first domino check
        if self.size == 0:
            self.first = domino
            ##### USED STRICTLY FOR DISPLAY #########                
            self.relSize = domino.relSize
            self.fullSize = self.relSize * 2
            if right:
                self.firstIndex = 0
        # standard insert right or left
        if right:
            if self.size > 0:
                rightMost = self.table[-1].value[1]
                if rightMost == domino.value[1]:
                    domino.value = domino.value[1] + domino.value[0]            
            self.table.append(domino)            
        else:
            if self.size > 0:
                leftMost = self.table[0].value[0]
                if leftMost == domino.value[0]: # reverse the order
                    domino.value = domino.value[1] + domino.value[0]              
            self.table.insert(0, domino)
            self.firstIndex += 1 # if its the 66, it will also go to 0          
        self.size += 1
            
    def insertRight(self, domino):
        self.insert(domino, True)

    def insertLeft(self, domino):
        self.insert(domino, False)

    def tryInsert(self, domino, right = True):
        success = True # give it a reason not to 
        if self.size > 0:
            if right:
                rightMost = self.table[-1].value[1]
                if rightMost != domino.value[0] and rightMost != domino.value[1]:
                    success = False                    
            else:                    
                leftMost = self.table[0].value[0]          
                if leftMost != domino.value[0] and leftMost != domino.value[1]:
                    success = False
                        
        return success

    def canInsert(self, domino):
        canInsert = False
        if self.canInsertRight(domino):
            canInsert = True
        if not canInsert and self.canInsertLeft(domino):
            canInsert = True
        return canInsert

    def canInsertRight(self, domino):
        return self.tryInsert(domino, True)

    def canInsertLeft(self, domino):
        return self.tryInsert(domino, False)                

    def clearTable(self):
        self.table = []
        self.size = 0
        
    def displayTable(self, canvas, faceUp = True, yOffset = 0):
        if DEBUG:
            print "[displayTable] Displaying a table with ", self.size, " number of dominoes"
        if self.size > 0:
            relSize = self.relSize
            fullSize = self.fullSize

            centerX = (WIDTH / 2) - relSize
            centerY = (HEIGHT / 2) - 150

            if self.size > 1:
                numLeft = self.firstIndex
                numRight = self.size - self.firstIndex - 1
            else:
                numLeft = 0
                numRight = 0

            centerY += yOffset

            self.first.displayValue(canvas, x = centerX, y = centerY, vertical = False)

            allDrawn = False
            isRightSide = False
            goingRight = False
            drawRange = reversed(range(0, self.firstIndex))
            while not allDrawn:
                curX = centerX # top left of the domino, always
                curY = centerY
                vertical = False                
                for index in drawRange:
                    dominoToDraw = self.table[index]
                    # calcaulate before draw
                    calculatedResult = self.calculateCoords(curX, curY, goingRight, isRightSide)
                    curX = calculatedResult[0]
                    curY = calculatedResult[1]
                    vertical = calculatedResult[2]
                    stillGoingRight = calculatedResult[3]
                    swapped = False
                    if not vertical:
                        swapped = goingRight != isRightSide # in the same direction as table structure
                    # draw the calculated values
                    dominoToDraw.displayValue(canvas, x = curX, y = curY, vertical = vertical, faceUp = faceUp, swapped = swapped)
                    # determine if the next is going to be in the opposite direction.
                    if self.directionChanged(goingRight, stillGoingRight):
                        # if so, make the necessery or desired changes
                        newCoords = self.desiredCoords(curX, curY,  stillGoingRight, isRightSide)
                        curX = newCoords[0]
                        curY = newCoords[1]
                        goingRight = stillGoingRight
                # now switch sides or end the draw table loop
                if not isRightSide:
                    drawRange = range(self.firstIndex + 1, self.size)
                    isRightSide = True
                    goingRight = True
                else:
                    allDrawn = True
                    

    def calculateCoords(self, curX = 0, curY = 0, goingRight = True, isRightSide = True):
        relSize = self.relSize
        fullSize = self.fullSize
        if DEBUG:
            print "[calculateCoords] before - X: ", curX, " Y: ", curY, " going right: ", goingRight, 
        # To calculate the coordinates, start at x and y, and determine if
        # the current direction is possible to traverse on
        # if so, calculate X and Y change for that direction (knowing that domino is always drawn from top left)
        canFit = True
        vertical = False
        stillGoingRight = goingRight
        if goingRight:
            if WIDTH - curX > fullSize * 2 + relSize:
                # there is enough space to print a domino on the right of the current position
                curX += fullSize
            else:
                # there is not enough space...
                canFit = False                
        else: # direction of draw is towarsd the left
            if curX - fullSize - relSize > 0:
                # there is enough space to print a domino on the left of the current position
                curX -= fullSize
            else:
                # there is not enough space, draw a domino up or down depending on side of the change
                canFit = False
        if not canFit: # the domino was unable to go to its direction
            vertical = True
            if isRightSide: 
                # draw Down
                if goingRight: #right switching to left
                    curX += fullSize
                else: #left -> right
                    curX -= relSize
            else:
                # draw Up
                curY -= relSize #positions it to the top in both cases
                if goingRight:
                    curX += fullSize
                else:
                    curX -= relSize
            if stillGoingRight: #since it couldn't fit, return a different direction (opposite to current)
                stillGoingRight = False
            else:
                stillGoingRight = True
        if DEBUG:
            print "Domino fit? ", canFit, " X: ", curX, " Y: ", curY, " vertical? ", vertical, " still going right? ", stillGoingRight
        return (curX, curY, vertical, stillGoingRight) # the new coordinates + whether or not there is a direction change
                
    def desiredCoords(self, curX = 0, curY = 0, goingRight = False, isRightSide = True):
        #assume canFit = false, so it wasn't able to fit and now we want to prepare for
        # the next draw.
        if not goingRight:
            # going Right was initially true, but they had to go left due to no space          
            if isRightSide:
                curX += self.relSize
                curY += self.fullSize
            else:
                curX += self.relSize
                curY -= self.relSize
        else:
            if isRightSide:
                curX -= self.fullSize
                curY += self.fullSize
            else:
                curY -= self.relSize
                curX -= self.fullSize
        return (curX, curY)
                
    def directionChanged(self, goingRight = True, stillGoingRight = True):
        return goingRight != stillGoingRight


class DominoGameStartupDialog(tkSimpleDialog.Dialog):
    # sub class, inheritance
    # see http://www.pythonware.com/library/tkinter/introduction/dialog-windows.htm

    def body(self, master):
        self.players = None
        # player names, if applicable
        self.player1Name = StringVar()
        self.player1Name.set("")
        self.player1Type = StringVar()
        self.player1Type.set("Player")

        self.player2Name = StringVar()
        self.player2Name.set("")
        self.player2Type = StringVar()
        self.player2Type.set("Computer")

        self.player3Name = StringVar()
        self.player3Name.set("")
        self.player3Type = StringVar()
        self.player3Type.set("None")

        self.player4Name = StringVar()
        self.player4Name.set("")
        self.player4Type = StringVar()
        self.player4Type.set("None")
        
        Label(master, text="Player 1:").grid(row = 0)
        OptionMenu(master, self.player1Type, "Player").grid(row = 1)        
        Entry(master, textvariable = self.player1Name).grid(row = 1, column = 1)        
        
        Label(master, text="Player 2:").grid(row = 2)
        OptionMenu(master, self.player2Type, "Computer", "Player").grid(row = 3)
        Entry(master, textvariable = self.player2Name).grid(row = 3, column = 1)
        
        Label(master, text="Player 3:").grid(row = 4)
        OptionMenu(master, self.player3Type, "None", "Computer", "Player").grid(row = 5)
        Entry(master, textvariable =self.player3Name).grid(row = 5, column = 1)
        
        Label(master, text="Player 4:").grid(row = 6)
        OptionMenu(master, self.player4Type, "None", "Computer", "Player").grid(row = 7)
        Entry(master, textvariable = self.player4Name).grid(row = 7, column = 1)

    def validate(self):
        valid = True
        chosenNames = []
        msg = ""
        
        if self.player1Name.get() == "":
            valid = False
            msg += "Player 1 has no name!\n"
        else:
            chosenNames.append(self.player1Name.get())
            
        if self.player2Name.get() == "" and self.player2Type.get() == "Player":
            valid = False
            msg += "Player 2 has no name!\n"
        elif self.player2Type.get() == "Player" and self.player2Name.get() in chosenNames:
            valid = False
            msg += "Player 2 needs a unique name!\n"
        else:
            chosenNames.append(self.player2Name.get())
            
        if self.player3Name.get() == "" and self.player3Type.get() == "Player":
            valid = False
            msg += "Player 3 has no name!\n"            
        elif self.player3Type.get() == "Player" and self.player3Name.get() in chosenNames:
            valid = False
            msg += "Player 3 needs a unique name!\n"            
        else:
            chosenNames.append(self.player3Name.get())
            
        if self.player4Name.get() == "" and self.player4Type.get() == "Player":
            valid = False
            msg += "Player 4 has no name!\n"            
        elif self.player4Type.get() == "Player" and self.player4Name.get() in chosenNames:
            valid = False
            msg += "Player 4 needs a unique name!\n"            

        index = 0
        while index < len(chosenNames) and valid:
            if chosenNames[index].startswith("Computer "):
                valid = False
                msg += "You cannot use the name 'Computer ' as it is reserved by the game, sorry."
            index += 1

        if not valid:
            tkMessageBox.showerror("Name error!", msg)
            
        return valid
        
    def apply(self):
        self.playerNames = []
        self.playerTypes = ["Player"]
        self.players = 2

        # p1 name only, type = player
        self.playerNames.append(self.player1Name.get())
        # p2 name and type
        self.playerNames.append(self.player2Name.get())
        self.playerTypes.append(self.player2Type.get())
        
        if self.player3Type.get() != "None":
            self.players += 1
            self.playerNames.append(self.player3Name.get())
            self.playerTypes.append(self.player3Type.get())

        if self.player4Type.get() != "None":
            self.players += 1
            self.playerNames.append(self.player4Name.get())
            self.playerTypes.append(self.player4Type.get())            
        
        
        
        
            
        
class DominoGameHandler:
    def __init__(self):
        self.availableValues = []                    
        self.availableSize = 0
        self.handFaceUp = False
        self.playerHands = {}
        self.initializeAvailableValues() 
        self.players = 0
        self.table = Table()
        self.dominoSize = self.availableValues[0].relSize * 2
        self.turn = -1
        self.currentInfo = ()
        self.overflowDomino = 1 #used for display
        self.tableYOffset = 0  
        self.showHelp = False
        self.helpText = '''Quick Controls Help
        Up or Page Up   - will scroll the screen up.
        Down or Page Down   - will scroll the screen down.
        Right   - will select the next domino in your hand.
        Left    - will select the previous domino in your hand.
        Escape  - will toggle full screen.
        H   - will open up this help screen.
        S   - will toggle the view of your hand.
        R   - will place the selected domino to the right
        L   - will place the selected domino to the left
        P   - will pass your move

How to Play
To win this game, you MUST play ALL of your dominoes. If you cannot see your dominoes, click 'Show' or press 's' on your keyboard to show the dominoes in your hand. To play a domino, you have to select it in your hand while it is your turn, and then, you must select where to place the domino: left or right depending on if it's valid or not. A valid move requires one of the domino values to be the same with the last value on the left or right. If the move was valid, it will be the next players turn, otherwise it will give you an error.

For more information, see the provided manual...
To close this screen, click the 'X' on the top-right

Made By: Abdul. D
        '''
        

    def initializeAvailableValues(self):
        if DEBUG:
            print "Avilable values intialized",        
        for index in range(0, 7): # first digit
            #0,1,2,3,4,5,6
            for index2 in range(index, 7): # second digit
                # 0 - 0,1,2,3,4,5,6    (min = 0)
                # 1 - 1,2,3,4,5,6     (min = 1)
                #....
                # 6 - 6               (min = 6, max = 6) therefore only 6
                dominoVal = str(index).strip() + str(index2).strip()
                if DEBUG:
                    print " ", dominoVal,
                self.availableValues.append( Domino(dominoVal) )
                self.availableSize += 1
        if DEBUG:
            print ""

    def beginGame(self, askPlayerInfo = True):
        startupVariables = showStartup()
        quitGame = False
        while startupVariables.players == None and not quitGame:
            if tkMessageBox.askyesno("Quit game?", "Would you like to quit the game?") == YES:
                quitGame = True
            if not quitGame:
                startupVariables = showStartup()                
        if quitGame:
            endGame()
        else:
            self.players = startupVariables.players
            computerPlayers = 1
            for index in range(0, self.players):
                name = startupVariables.playerNames[index]
                pType = startupVariables.playerTypes[index]
                hand = Hand([])
                if pType == "Computer":
                   name = "Computer " + str(computerPlayers)
                   computerPlayers += 1
                else:
                   name = name.capitalize()
                self.playerHands[name] = Hand([])                                
            self.deal()
            if self.isComputerPlayer():
                self.computerMakeMove()
 
    def updateGameDisplay(self, canvas, overflowX = 0, overflowY = 0):
        # delete all objects on the canvas so that the screen can get a good refresh
        # it is easier toe delete all items than to track each one and change it
        # since we have the processing power (thinking about linear vs binary search) -
        # might as well.
        canvas.delete(ALL)
        if self.showHelp:
            self.drawHelpInterface(canvas)
        else:
            # show game table
            self.table.displayTable(canvas, faceUp = True, yOffset = self.tableYOffset)
            
            self.drawUserInterface(canvas) # UI for playing game/seeing score, etc

    def drawUserInterface(self, canvas):
        ##################      USER INTERFACES BEGIN           #####################
            
        halfWidth = (WIDTH / 2)
        ##################      DOMINO INTERFACE SHOWING ALL DOMINOES ###############
        startY = HEIGHT - 125
        endY = HEIGHT - 3        
        canvas.create_rectangle(0, startY, halfWidth - 3, endY, fill ="beige", width = 5)

        num = 0 # current index of playerHands
        handsNameArray = list(self.playerHands)
        
        if self.players < 4: # show dogpile
            handsNameArray.append("Dog Pile:") ## the point of this and using list() is to ensure that dog pile is the last to be printed
            self.playerHands["Dog Pile:"] = Hand(self.availableValues, self.availableSize) # hand        
            
        for name in handsNameArray:
            # truncate the name if required'            
            if len(name) > 10:
                name = name[:11]
                
            startYExtra = startY + (24 * num) + 10

            canvas.create_text(5, startYExtra, text = name, anchor = NW, font = ("Verdana", 14))
            
            drawX = 153 
            numDrawn = 0 # number of mini dominoes drawn
            while drawX + 20 < halfWidth and numDrawn < self.playerHands[name].size:
                
                canvas.create_rectangle(drawX, startYExtra + 3, \
                                        drawX + 10, startYExtra + 18, fill = "white", width = 2)
                numDrawn += 1
                drawX += 20
                
                    
            num += 1

        if self.players < 4:
            del self.playerHands["Dog Pile:"]
        
        canvas.create_line(140, startY + 3, 140, endY)
        #################       CURRENT PLAYERS INTERFACE ################################
        canvas.create_rectangle(halfWidth + 3, startY, WIDTH, endY, fill = "brown3", width = 5)

        if len(self.currentInfo) > 0:
            currentName = self.currentInfo[0]
            currentHand = self.currentInfo[1]
        else:
            currentName = ""
            currentHand = Hand(list())

        canvas.create_text(3, startY - 15, anchor = W, text = currentName + "'s turn", fill = "white", font = ("Verdana", 14))

        dStartX = halfWidth + 25
        drawSpace = (WIDTH - dStartX) // ((self.dominoSize / 2) + 15) # this many dominoes can fit in the table area,

        if drawSpace + 1 > currentHand.size: # if enough can fit, make sure there is no overflow enabled
            self.overflowDomino = 1
            end = currentHand.size
        else:
            end = self.overflowDomino + drawSpace
            if end > currentHand.size: # can't draw more then there are
                end = currentHand.size
                
        dominoesDrawn = len(range(self.overflowDomino - 1, end))
        if dominoesDrawn > 0: # only proceed if there is anything to draw
            faceUp = self.handFaceUp
            if DEBUG and not faceUp:
                print "Displaying hands face down"
            currentHand.displayHand(canvas, x = dStartX, y = startY + 6, start = self.overflowDomino - 1, vertical = True, faceUp = faceUp)

            if self.overflowDomino > 1:
                ID = canvas.create_rectangle(halfWidth + 5, startY + 6, halfWidth + 23, HEIGHT - 5, fill ="brown4", outline ="brown4", activefill = "black") 
                canvas.tag_bind(ID, '<ButtonPress-1>', overflowDLeft)
                ID = canvas.create_text(halfWidth + 6, ((HEIGHT + startY) / 2), text = "<", anchor = NW, fill = "white", font = (14))
                canvas.tag_bind(ID, '<ButtonPress-1>', overflowDLeft)            

            if end < currentHand.size:
                ID = canvas.create_rectangle(WIDTH - 23, startY + 6, WIDTH - 3, HEIGHT - 5, fill ="brown4", outline ="brown4", activefill = "black")
                canvas.tag_bind(ID, '<ButtonPress-1>', overflowDRight)
                ID = canvas.create_text(WIDTH - 20, ((HEIGHT + startY) / 2), text = ">", anchor = NW, fill = "white", font = (14))
                canvas.tag_bind(ID, '<ButtonPress-1>', overflowDRight)

        # HAND MOVE PANEL
        startY -= 25
        endY = startY + 20
        textY = startY + 10

        startX = halfWidth
        
        ID = canvas.create_rectangle(startX, startY, startX + 50, endY, fill = "black", width = 1, outline = "white")
        canvas.tag_bind(ID, '<ButtonPress-1>', passMove)        
        ID = canvas.create_text(startX + 25, textY, text = "Pass", fill = "white")
        canvas.tag_bind(ID, '<ButtonPress-1>', passMove)        

        startX += 60
        ID = canvas.create_rectangle(startX, startY, startX + 50, endY, fill = "white", outline = "black")
        canvas.tag_bind(ID, '<ButtonPress-1>', leftMove)                                
        ID = canvas.create_text(startX + 25, textY, text = "Left", fill = "black")
        canvas.tag_bind(ID, '<ButtonPress-1>', leftMove)        

        startX += 60
        ID = canvas.create_rectangle(startX, startY, startX + 50, endY, fill = "white", outline = "black")
        canvas.tag_bind(ID, '<ButtonPress-1>', rightMove)                        
        ID = canvas.create_text(startX + 25, textY, text = "Right", fill = "black")
        canvas.tag_bind(ID, '<ButtonPress-1>', rightMove)                  

        startX += 60
        if self.handFaceUp:
            # hide button
            text = "Hide"
        else:
            # show button
            text = "Show"
        ID = canvas.create_rectangle(startX, startY, startX + 50, endY, fill = "black", outline = "white")
        canvas.tag_bind(ID, '<ButtonPress-1>', toggleHand)                        
        ID = canvas.create_text(startX + 25, textY, text = text, fill = "white")
        canvas.tag_bind(ID, '<ButtonPress-1>', toggleHand)            
            
        ####### HELP BUTTON ON TOP RIGHT OF SCREEN ######    
        ID = canvas.create_rectangle(WIDTH - 23, 0, WIDTH - 3, 20, fill = "black", width = 1, outline = "white")
        canvas.tag_bind(ID, '<ButtonPress-1>', toggleHelp)        
        ID = canvas.create_text(WIDTH - 12, 10, text = "?", fill = "white")
        canvas.tag_bind(ID, '<ButtonPress-1>', toggleHelp)        

    def drawHelpInterface(self, canvas, startX = 0, startY = 0):
        canvas.create_rectangle(startX, startY, WIDTH, HEIGHT, fill = "black") # draw a rect instead of canvas, easier to manage
        canvas.create_text(WIDTH / 2, 0, anchor = N, font = ("" ,26), text = "Domino - Quick Help", fill  = "green")
        startY += 50
        canvas.create_text(startX + 10, startY + 10, text = self.helpText, width = WIDTH - startX, font = ("", 14), anchor  = NW, fill = "white")
        ####### CLOSE BUTTON ON TOP RIGHT OF SCREEN ######    
        ID = canvas.create_rectangle(WIDTH - 20, 0, WIDTH, 20, fill = "white", width = 0)
        canvas.tag_bind(ID, '<ButtonPress-1>', toggleHelp)        
        ID = canvas.create_text(WIDTH - 12, 10, text = "X", fill = "black")
        canvas.tag_bind(ID, '<ButtonPress-1>', toggleHelp)
                                                

    def deal(self):
        # makes sure to deal the 66, first but randomly
        randomPlayer = random.randint(0, self.players - 1)
        self.turn = randomPlayer # set the turn to the random player
        self.currentInfo = self.getCurrentPlayerInfo() # get the currrent information for that player
        d66 = self.availableValues[self.availableSize - 1]
        self.currentInfo[1].addDomino(d66) # add the 66 to the hand (temp)
        self.table.insertRight(self.currentInfo[1].getDomino(0)) # insert 66 into the table        
        self.removeAvailable(-1) # remove 66 from available values
        for name in self.playerHands:
            hand = self.playerHands[name]
            dealt = hand.size # possible to have some dealt, i.e : 66
            # deal until you get to 7 (0...6 inclusive length: 7)            
            while dealt < 7:                
                # select random domino
                index = random.randint(0, self.availableSize - 1)
                domino = self.availableValues[index] # get it's reference                               
                # add domino to players hand                
                hand.addDomino(self.availableValues[index])                            
                # remove domino reference from available list and change counters
                self.removeAvailable(index) # one less domino available
                dealt += 1 # one more domino dealt                
            if DEBUG:
                print "Player Dealt: ", name, str(hand)
                print "Leftover: ", self.availableSize
                
        self.currentInfo[1].removeDomino(-1) # now remove the 66 from the players hand
        if DEBUG:
            print "First person to play: ", self.playerHands.keys()[self.turn]
            
    def removeAvailable(self, index):
        if index < self.availableSize:
            del self.availableValues[index]
            self.availableSize -= 1

    def canMove(self, hand = None):
        if hand == None:
            hand = self.currentInfo[1]
        canMove = False
        index = 0
        while not canMove and index < hand.size:
            domino = hand.getDomino(index)
            canMove = self.table.canInsert(domino)
            if DEBUG and not canMove:
                print "[canMove] domino with value: ", domino, " cannot be played left/right."
            index += 1            
        return canMove
            
    def playDomino(self, right = True):
        if self.currentInfo[1].isAnythingSelected():
            domino = self.currentInfo[1].selected
            hand = self.currentInfo[1]
            success = False
            if right:
                if self.table.canInsertRight(domino):
                    self.table.insertRight(domino)
                    success = True
            else:
                if self.table.canInsertLeft(domino):
                    self.table.insertLeft(domino)
                    success = True                
            if success:
                hand.removeSelected()
                if hand.size > 0:
                    self.nextTurn()
                else:
                    self.gameWon()
            else:
                self.showError("Bad Move!", "You cannot place this domino here.")

    def gameWon(self, winnerInfo = None, reason = ""):
        if winnerInfo == None:
            winnerInfo = self.currentInfo
        self.table.clearTable()
        if DEBUG:
            print "[GameWon] Game has been won by ", winnerInfo[0]
        message = "Player with the name: " + winnerInfo[0] + ", has won this game!\n"
        message += reason
        tkMessageBox.showinfo("Congratulation " + winnerInfo[0] + "!", message)
        if tkMessageBox.askyesno("Replay?", "Would you like to play again?") == YES:
            self.resetGame()
        else:
            # global function
            endGame()
            

    def resetGame(self):
        self.__init__()  # reset variables
        self.beginGame() # start up the game for play
        updateGame()     # update game screen, global function
        

    def showError(self, title = "", error = ""):
        if DEBUG:
            print "[",title,"] ",error        
        tkMessageBox.showerror(title, error)

    def passMove(self):
        if self.availableSize > 0:
            randomIndex = random.randint(0, self.availableSize - 1)
            randomDomino = self.availableValues[randomIndex]
            self.currentInfo[1].addDomino(randomDomino)
            self.removeAvailable(randomIndex)               # one less domino available
        self.nextTurn()

    def nextTurn(self):
        # check to make sure it is possible for any of the players to make a move
        canContinue = False
        if self.availableSize > 0:
            canContinue = True
        index = 0
        names = self.playerHands.keys() # store it for a bit, repetitive calls could increase time
        while not canContinue and index < self.players: # use a while loop to prevent unnecessary looping
            hand = self.playerHands[names[index]]
            indexDomino = 0
            canContinue = self.canMove(hand) # also uses a while loop
            if DEBUG and not canContinue:
                print "[nextTurn] Player: ", names[index], " cannot make a move."
            index += 1
            
        if canContinue:
            self.turn += 1
            if self.turn > (self.players - 1):
                self.turn = 0
            self.currentInfo = self.getCurrentPlayerInfo()      # set as variable to prevent unnecessary calls
            # reset any display variables        
            self.overflowDomino = 1
            self.tableYOffset = 0
            self.handFaceUp = False
            
            if self.isComputerPlayer():     
                self.computerMakeMove()
                updateGame()            
        else:
            winningPlayerInfo = self.getWinningPlayer()            
            self.gameWon(winningPlayerInfo, reason = "By default because the game detected no more possible moves.\n They had the smallest hand of: " + str(winningPlayerInfo[1]) + "\n\nHowever, it is possible that other players have the same score.")

    def isComputerPlayer(self):
        return self.currentInfo[0].startswith("Computer ")

    def getWinningPlayer(self):
        playerNames = self.playerHands.keys()
        winnerName = playerNames[0]
        winnerSize = self.playerHands[winnerName]
        for index in range(1, self.players):
            name = playerNames[index]
            hand = self.playerHands[name]
            if hand.size < winnerSize:
                winnerName = name
                winnerSize = hand.size
        return (winnerName, winnerSize)

    def computerMakeMove(self):
        possibleMoves = []
        if DEBUG:
            print "[Computer Make Move] Making a computed move - Hand: "
        for domino in self.currentInfo[1].hand:
            if DEBUG:
                print "Domino: ", domino, " ", 
            if self.table.canInsert(domino): # check if this domino can be played
                if DEBUG:
                    print "(+) ",
                possibleMoves.append(domino) # yes it can, add it to possible moves
        if DEBUG:
            print ". Possible Moves: ", len(possibleMoves), " - Randomly selecting..."
        if len(possibleMoves) > 0:
            domino = possibleMoves[random.randint(0, len(possibleMoves) - 1)]
            if self.table.canInsertRight(domino):
                self.table.insertRight(domino)
            else:
                self.table.insertLeft(domino)
            hand = self.currentInfo[1]
            index = hand.getDominoByValue(domino.value)
            if DEBUG:
                print "Removing domino with value: ", domino.value, " at index: ", index, " which contains: ", hand.getDomino(index).value            
            hand.removeDomino(index)
            if hand.size > 0:
                self.nextTurn()
            else:
                self.gameWon()
        else:            
            self.passMove()

    def getCurrentPlayerInfo(self):
        name = self.playerHands.keys()[self.turn]
        hand = self.playerHands[name]
        return (name, hand)
    

###############################################
##########      MAIN PROGRAM       ############

##globals
WIDTH = 700
HEIGHT = 500
# if debug is true, it will show extra information on the console
# Known issue: when you cause the game to refresh too many times while it is debugging,
#              the table will draw improperly. This is probably due to late calls.
DEBUG = False
VERSION = 6
AUTHORS = "Abdul. D"

main = DominoGameHandler()

# Initialize frame
frame = Tk()
frame.minsize(WIDTH, HEIGHT)

FULL_WIDTH = frame.winfo_screenwidth()
FULL_HEIGHT = frame.winfo_screenheight()
FULLSCREEN = False 

frame.title("Domino | By: Abdul W. D and Andrew L")

# Create the main canvas
canvas = Canvas(frame, width = WIDTH, height = HEIGHT, background = "darkgreen", borderwidth = 0)
canvas.pack(fill = "both", expand = 1)

################ GLOBAL FUNCTION FOR BASIC CONTROLS ################        
def overflowDRight(event):
    if DEBUG:
        print "overflow right clicked"
    main.overflowDomino +=  1
    updateGame()

def overflowDLeft(event):
    if DEBUG:
        print "overflow left clicked"
    main.overflowDomino -= 1
    updateGame()

def passMove(event):
    if DEBUG:
        print "Pass called"
    main.passMove()
    updateGame()

def rightMove(event):
    if DEBUG:
        print "Player wanted to move domino to right"
    main.playDomino(right = True)
    updateGame()

def leftMove(event):
    if DEBUG:
        print "Player wanted to move domino to left"
    main.playDomino(right = False)
    updateGame()

def handClicked(event, value = "00"):    
    index = main.playerHands[main.playerHands.keys()[main.turn]].getDominoByValue(value)
    if DEBUG:
        print "A domino in the hand has been clicked, value:" + value        
        print "The index of that is: ",  index
    main.currentInfo[1].updateSelected(index) # tell current players hand object to update the selected value
    updateGame()

def selectNext(event):
    main.currentInfo[1].selectNext()
    updateGame()

def selectPrevious(event):
    main.currentInfo[1].selectPrevious()
    updateGame()    

def canvasOffsetChange(event, up = True, reset = False):
    if DEBUG:
        print "Offset changed: Up?", up, " Reset? ", reset
    if not reset:
        if up:
            main.tableYOffset -= 10
        else:
            main.tableYOffset += 10
    else:
        main.tableYOffset = 0
    updateGame()

def toggleHand(event):
    if DEBUG:
        print "User requested to show or hide their hand!"
    main.handFaceUp = not main.handFaceUp # the opposite of faceUp
    updateGame()

def toggleHelp(event):
    if DEBUG:
        if main.showHelp:
            print "Showing help box..."
        else:
            print "Closing help box..."
    main.showHelp = not main.showHelp
    updateGame()

##### GLOBAL FUNCTIONS FOR FRAME AND CANVAS HANDLING #############

def showStartup():
    if DEBUG:
        print "[showStartup] Showing the startup frame."
    d = DominoGameStartupDialog(frame)
    return d
    
def updateGame():
    if DEBUG:
        print "[updateGame] Refreshing the game display."
    main.updateGameDisplay(canvas)
    
def endGame():
    if DEBUG:
        print "[endGame] The game will shut down. Any error after this is from a 'stray' function call."
    frame.destroy()
##################################################################
def toggleFullScreen(event):
    global FULLSCREEN
    if FULLSCREEN:        
        frame.overrideredirect(False)
        frame.geometry(str(WIDTH / 2) + "x" + str(HEIGHT / 2))
        FULLSCREEN = False
    else:
        frame.overrideredirect(True)       
        frame.geometry(str(FULL_WIDTH) + "x" + str(FULL_HEIGHT) + "+0+0")
        FULLSCREEN = True
    if DEBUG:
        print "[toggleFullScreen] Fullscreen? ", FULLSCREEN

def canvasResized(event):
    global WIDTH
    global HEIGHT
    
    if event.width != WIDTH or event.height != HEIGHT:
        WIDTH = event.width
        HEIGHT = event.height
        main.updateGameDisplay(canvas)
        if DEBUG:
            print "Resized to width: ", event.width, " height: ", event.height
    
canvas.bind('<Configure>', canvasResized)
frame.bind('<Key-Prior>', canvasOffsetChange)
frame.bind('<Key-Up>', canvasOffsetChange)
frame.bind('<Key-Next>', lambda x: canvasOffsetChange(x, False))
frame.bind('<Key-Down>', lambda x: canvasOffsetChange(x, False))
frame.bind('<Key-Right>', selectNext)
frame.bind('<Key-Left>', selectPrevious)
frame.bind('r', lambda x: canvasOffsetChange(x, reset = True))
frame.bind('0', lambda x: canvasOffsetChange(x, reset = True))
frame.bind('<Escape>', toggleFullScreen)
frame.bind('h', toggleHelp)
frame.bind('s', toggleHand)
frame.bind('r', rightMove)
frame.bind('l', leftMove)
frame.bind('p', passMove)
toggleFullScreen(None)
##################################################################
if DEBUG:
    print "[main] Debugging is enabled."
    print "[main] Game Version", VERSION , " Authors: ", AUTHORS

main.beginGame()
main.updateGameDisplay(canvas)
canvas.create_text(5, 5, fill = "white", font = (14), anchor = NW, text = "For help, click the '?' button on the top-right.")

frame.mainloop()

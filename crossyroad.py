#Crossy road game
#Best played in 1920x1080
#Images used from clipart-library.com
import tkinter as tk
from tkinter import messagebox
import json, os, random

users = {"name": [], "level": [], "score": []} #A dictionary of user data
currentUser = 0 #The index of the current user from the dictionary
registerUser = "" #The user name of a registering user

#Create a file to store the user data if it doesn't already exist
if(os.path.exists('userdata.json') == False):
    f = open("userdata.json", "w")
    with open("userdata.json", "w") as outfile:
        json.dump(users, outfile)

#Loads the user data
def loadUserdata():
    with open('userdata.json', 'r') as openFile:
        global users
        users = json.load(openFile) #Store in the users dictionary

#Saves the user data
def saveUserdata():
    with open("userdata.json", "w") as outfile:
        json.dump(users, outfile) #Store the users dictionary in the json file

#Check if the user exists
def userExists(user):
    return user in users["name"]

#Add a new user to the dictionary
def newUser(user):
     users["name"].append(user)
     users["level"].append(0)
     users["score"].append(0)
     
loadUserdata()

#Setting up the window
def setWindowDimensions(w, h):
    window = tk.Tk()
    window.title("Crossy Road") #Set window title
    resolution = str(w) + "x" + str(h)
    window.geometry(resolution) #Set window geometry
    window.attributes('-fullscreen', True) #Make window fullscreen
    return window

#The width and height that the window will be 1920x1080
width = 1920
height = 1080
root = setWindowDimensions(width, height) #Create a window

#hex codes for colours used
lightblue = "#ADD8E6"
red = "#FF0000"
brass = "#E1C16E"

#Creating a canvas to draw on
menuCanvas = tk.Canvas(root , bg = lightblue, height = height, width = width)
gameCanvas = tk.Canvas(root, bg = brass, height = height, width = width)

#Called when the quit button is pressed
def quitOption():
    #Quit confirmation
    quitmessage = messagebox.askyesno(title = "Quit", message = "Are you sure you want to quit?") 
    if quitmessage:
        exit() #If yes, quit

#Called when the back button on the play menu is pressed
def playBackOption():
    backButton.place_forget() 
    loginButton.place_forget()
    registerButton.place_forget()
    username.place_forget()
    mainMenu() #Goes back to the main menu

#Called when the login button is pressed
def loginOption():
    currentUsername = username.get() #Gets the username that the user entered
    #If the username is found
    if userExists(currentUsername):
        global currentUser
        currentUser = users["name"].index(currentUsername) #Get the index of the username in the users dictionary
        messagebox.showinfo(title = "Welcome", message = ("Welcome " + currentUsername)) #Welcome message
        username.delete(0, "end") #Clears the username entry field
        levelsScreen()
    #If the user has not entered anything
    elif len(currentUsername) == 0:
        messagebox.showinfo(title = "Error", message = "Please enter a user name") #Error message
        username.delete(0, "end")
    #Else, username does not exist
    else:
            messagebox.showinfo(title = "User Not Nound", message = (currentUsername + " was not found, please try again or register"))
            username.delete(0, "end")

#Called when the register button is pressed
def registerOption():
    newUsername = username.get() #Gets the username that the user entered
    #Check if the username already exists
    if userExists(newUsername):
        messagebox.showinfo(title = "User Already Exists", message = (newUsername + " already exists")) #Error message
        username.delete(0, "end")
    #The user name must be at least 4 characters
    elif len(newUsername) < 4:
        messagebox.showinfo(title = "Too Short", message = "Please enter a username that is at least 4 characters")
        username.delete(0, "end")
    #Else, add the new user to the users dictionary and save this
    else:
        newUser(newUsername) 
        saveUserdata()
        messagebox.showinfo(title = "Success", message = (newUsername + " is registered, you may now login"))
        username.delete(0, "end")

paused = False #The game is initially not paused

#Called when the pause button is pressed
def pauseOption():
    global paused, showPaused
    paused = not paused
    if(paused):
        showPaused = gameCanvas.create_image(width/2 - 112, height/2 - 112, image = bigPause)
    else:
        gameCanvas.delete(showPaused)
        
#Images used
play = tk.PhotoImage(file = "play.png")
leaderboard = tk.PhotoImage(file = "leaderboard.png")
settings = tk.PhotoImage(file = "settings.png")
quit = tk.PhotoImage(file = "quit.png")
back = tk.PhotoImage(file = "back.png")
lock = tk.PhotoImage(file = "lock.png")
playLevel = tk.PhotoImage(file = "playLevel.png")
car = tk.PhotoImage(file = "car.png")
avatar = tk.PhotoImage(file = "player.png")
pause = tk.PhotoImage(file = "pause.png")
bigPause = tk.PhotoImage(file = "bigPause.png")
bossScreen = tk.PhotoImage(file = "boss.png")

#Back button for sub menus
backButton = tk.Button(root, image = back, width = 300, height = 228, command = None)

#Login and register button in the play menu
loginButton = tk.Button(root, text = "Login", width = 10, height = 5, command = loginOption)
registerButton = tk.Button(root, text = "Register", width = 10, height = 5, command = registerOption)

#User input for the username in the play menu
username = tk.Entry(root, width = 75)

levels = [] #Array of level buttons
levelLabels = [] #Array of level labels

roads = [] #Array of roads
water = [] #Array of water
cars = [] #Array of cars
logs = [] #Array of logs

#Pause button
pauseButton = tk.Button(root, width = 90, height = 50, image = pause, command = pauseOption)

#When the user presses left
def leftKey(event):
    global playerDirection
    playerDirection = 'left'

#When the user presses right
def rightKey(event):
    global playerDirection 
    playerDirection = 'right'

#When the user presses up
def upKey(event):
    global playerDirection
    playerDirection = 'up'

#When the user presses down
def downKey(event):
    global playerDirection 
    playerDirection = 'down'

#When the user presses the cheat key
def cheatKey(event):
    global cheat
    cheat = not cheat

#When the user presses the boss key
def bossKey(event):
    global boss
    boss = True

playerDirection = None #Player is initially not moving
player = gameCanvas.create_image(750, 54, image = avatar, state = "hidden") #player
cheat = False #Player is initially not cheating
boss = False #Boss screen is initially disabled

#Score
score = 0
scoreText = gameCanvas.create_text(1400, 30, font = "Times 20", text = "Score : ", fill = "white", state = "hidden")

#Binding keys
left = 'a'
right = 'd'
up = 'w'
down = 's'

gameCanvas.bind(left, leftKey)
gameCanvas.bind(right, rightKey)
gameCanvas.bind(up, upKey)
gameCanvas.bind(down, downKey)
gameCanvas.bind('c', cheatKey)
gameCanvas.bind('b', bossKey)
menuCanvas.bind('b', bossKey)

#Called when the play button is pressed
def playOption():
    hideMainMenu()
    backButton.pack()
    loginButton.pack()
    registerButton.pack()

    backButton.configure(command = playBackOption)

    backButton.place(x = 100, y = 500)
    loginButton.place(x = width/2 - 300, y = 500, anchor = "center")
    registerButton.place(x = width/2, y = 500, anchor = "center")

    username.pack()
    username.place(x = width/2 - 150, y = 300, anchor = "center")

#Called when the user logs in
def levelsScreen():
    menuCanvas.focus_set()
    #Clear the levels and levelLabels arrays
    levels.clear()
    levelLabels.clear()

    backButton.configure(command = levelsBackOption)
    backButton.place_configure(y = 600)
    loginButton.place_forget()
    registerButton.place_forget()
    username.place_forget()
    x = 50
    y = 50      
    currentLevel = users["level"][currentUser] #Gets the level the user was previously on

    #Generate a grid of levels
    for i in range(25):
        levels.append(tk.Button(root, image = playLevel if i<=currentLevel else lock, width = 50, height = 50, state = "normal" if i<=currentLevel else "disabled", command = lambda c=i: crossyRoad(c)))
        levels[i].pack()
        levels[i].place(x=x, y=y)
        levelLabels.append(tk.Label(root, text = "Level " + str(i + 1)))
        levelLabels[i].pack()
        levelLabels[i].place(x=x, y=y+70)
        if (x >= 1000):
            x = 50
            y += 150
        else:
            x += 150

#Called when the back button on the levels screen is pressed
def levelsBackOption():
    backButton.configure(command = playBackOption)
    for i in range(len(levels)):
        levels[i].place_forget()
        levelLabels[i].place_forget()
    playOption()

#Moves cars repeatedly
def moveCars():
    #If the game is not paused
    if(paused == False):
        direction = -1 #Cars initially move from right to left
        for i in range(len(cars)):
            #If the car exists
            if cars[i] in gameCanvas.find_all():
                gameCanvas.move(cars[i], (50 * direction), 0) #Moves the car
                pos1 = gameCanvas.coords(cars[i])
                #If the next car is not in the same road, change the direction
                if (i != len(cars) - 1):
                    pos2 = gameCanvas.coords(cars[i + 1])
                    if pos1[1] != pos2[1]:
                        direction *= -1
                
                #If the car has gone off the screen, the car comes back onto the screen from the other end
                if pos1[0] < -100:
                    gameCanvas.coords(cars[i], width, pos1[1])
                elif pos1[0] > width + 100:
                    gameCanvas.coords(cars[i], 0, pos1[1])

                #Clear the pos1 and pos2 arrays
                pos1.clear()
                pos2.clear()

    #Moves cars every 250ms if the car exists
    if(len(cars) != 0):
        if cars[0] in gameCanvas.find_all():
            root.after(250, moveCars) 

#Moves logs repeatedly
def moveLogs():
    #If the game is not paused
    if(paused == False):
        direction = -1 #Logs initially move from right to left
        for i in range(len(logs)):
            #If the log exists
            if logs[i] in gameCanvas.find_all():
                pos1 = gameCanvas.coords(logs[i])
                gameCanvas.move(logs[i], (50 * direction), 0) #Moves the log

                #If the player is on a log, move the player with the log
                playerPos = gameCanvas.coords(player)
                if overlappingWithLogOrWater(playerPos, pos1):
                    gameCanvas.move(player, 50 * direction, 0)

                #If the next log is not in the same river, change the direction
                if(i != len(logs) - 1):
                    pos2 = gameCanvas.coords(logs[i + 1])
                    if pos1[1] != pos2[1]:
                        direction *= -1

                #If the log has gone off the screen, the log comes back onto the screen from the other end
                if pos1[0] < -100:
                    gameCanvas.coords(logs[i], width, pos1[1], width + (pos1[2] - pos1[0]), pos1[3])
                elif pos1[0] > width + 100:
                    gameCanvas.coords(logs[i], 0, pos1[1], 0 + (pos1[2] - pos1[0]), pos1[3])

                #Clear the pos1 and pos2 arrays
                pos1.clear()
                pos2.clear()

    #Moves logs every 250ms if the log exists
    if len(logs) != 0:
        if logs[0] in gameCanvas.find_all():
            root.after(250, moveLogs) 

#Generates the terrain for the main game
def terrainGen(levelNo):
    #Hide the levels screen
    menuCanvas.pack_forget()
    backButton.place_forget()
    quitButton.place_forget()
    for i in range(len(levels)):
        levels[i].place_forget()
        levelLabels[i].place_forget()

    gameCanvas.pack()

    #Clear the roads, water, cars, logs arrays
    roads.clear()
    water.clear()
    cars.clear()
    logs.clear()

    #Generate a number of rows depending on the level
    i = 1 #First row needs to be free for the player
    while i < 10 + (levelNo * 2):
        toPlace = random.randint(0, 1) #Place a river or road
        if(toPlace == 0): #road
            #Add 1 or 2 roads
            for j in range(random.randint(1, 2)): 
                roads.append(gameCanvas.create_rectangle(0, 108 * i, width, (108 * i) + 108, fill = "black"))
                #Create random space between each car
                for k in range(3):
                    space = random.randint(0, 2)
                    cars.append(gameCanvas.create_image(350 * k + (space * 350), (108 * i) + 50, image = car))
                i += 1
            i += random.randint(1, 3)
        elif(toPlace == 1): #river
            #Add between 1 and 3 rivers
            for j in range(random.randint(1, 3)):
                water.append(gameCanvas.create_rectangle(0, 108 * i, width, (108 * i) + 108, fill = "blue"))
                #Create random space between each log of varying length
                for k in range(5):
                    length = random.randint(3, 6)
                    space = random.randint(2, 4)
                    logs.append(gameCanvas.create_rectangle(250 * k + (space * 350), (108 * i) + 25, 250 * k + (space * 350) + (50 * length), (108 * i) + 75, fill = "brown"))
                i += 1
            i += random.randint(1, 3)

#Check if the player is colliding with a log or water
def overlappingWithLogOrWater(p, l):
    if(p[0] > l[0] and p[0] < l[2] and p[1] > l[1] and p[1] < l[3]):
        return True
    else:
        return False

#Check if the player is colliding with a car
def overlappingWithCar(p, c):
    if(p[0] > c[0] - 83 and p[0] < c[0] + 83 and p[1] > c[1] - 44 and p[1] < c[1] + 44):
        return True
    else:
        return False

#Called when the user selects a level
def crossyRoad(levelNo):
    gameCanvas.focus_set() #Focus on the game canvas
    terrainGen(levelNo) #Generate terrain

    #Display pause button
    pauseButton.pack()
    pauseButton.place(x = 10, y = 10)
    pauseButton.lift()

    gameCanvas.coords(player, 750, 54) #Reset the player coordinates

    moveCars()
    moveLogs()

    #Display player and score
    gameCanvas.itemconfigure(player, state = "normal")
    gameCanvas.itemconfigure(scoreText, state = "normal", text = "Score : " + str(score))

    #Bring the player and the score to the front of the screen
    gameCanvas.lift(player)
    gameCanvas.lift(scoreText)
    
    movePlayer()

    isGameWon(levelNo)
    isGameOver()
    
#Checks if the game has been won
def isGameWon(levelNo):
    #If the player is visible and the game is not paused
    if (gameCanvas.itemcget(player, 'state') == "normal" and paused == False):
        playerPos = gameCanvas.coords(player)

        #If there are roads and rivers
        if(len(roads) >= 1 and len(water) >= 1):
            lastRoadPos = gameCanvas.coords(roads[len(roads) - 1])
            lastWaterPos = gameCanvas.coords(water[len(water) - 1])

            #If the player is below the last river and the last road
            if (playerPos[1] > lastRoadPos[3] and playerPos[1] > lastWaterPos[3]):
                gameWon = True

        #If there are only roads
        elif(len(roads) >= 1):
            lastRoadPos = gameCanvas.coords(roads[len(roads) - 1])

            #If the player is below the last road
            if(playerPos[1] > lastRoadPos[3]):
                gameWon = True    

        #If there are only rivers
        elif(len(water) >= 1):
            lastWaterPos = gameCanvas.coords(water[len(water) - 1])
            
            #If the player is below the last river
            if(playerPos[1] > lastWaterPos[3]):
                gameWon = True
            
        #If the game is won
        if("gameWon" in locals()):
            if(gameWon):
                root.after_cancel(isGameWon) #Stop calling isGameWon

                #Delete all the items on gameCanvas apart from player and score
                for i in range(len(cars)):
                    gameCanvas.delete(cars[i])
                for i in range(len(logs)):
                    gameCanvas.delete(logs[i])
                for i in range(len(roads)):
                    gameCanvas.delete(roads[i])
                for i in range(len(water)):
                    gameCanvas.delete(water[i])
                
                #Hide the player
                gameCanvas.itemconfigure(player, state = "hidden")

                #Show game won message
                messagebox.showinfo(title = "Level Completed", message = "Congratulations, you won!")
            
                #Go back to the levels screen and update the user's level
                pauseButton.place_forget()
                gameCanvas.pack_forget()
                menuCanvas.pack()
                quitButton.place(x = width - 500, y = 150, anchor = "center")
                backButton.place(x = 100, y = 600)
                highestLevelReached = users["level"][currentUser]

                global score

                if highestLevelReached == levelNo:
                    users["level"][currentUser] += 1
                    users["score"][currentUser] += score #Add the user's score
                    saveUserdata()

                #Reset score
                score = 0

                levelsScreen()

    #If the game hasn't been won or lost, call isGameWon every 100ms
    if ("gameWon" not in locals() and "gameOver" not in locals()):
        root.after(100, isGameWon, levelNo)

#Check if the game is over
def isGameOver():
    #If the player is visible and the game is not paused
    if(gameCanvas.itemcget(player, 'state') == "normal" and paused == False):
        playerPos = gameCanvas.coords(player)

        #If the player has collided with a car
        for i in range(len(cars)):
            carPos = gameCanvas.coords(cars[i])
            if overlappingWithCar(playerPos, carPos):
                gameOver = True

        #If the player has collided with a log, set onLog to True
        onLog = False
        for i in range(len(logs)):
            logPos = gameCanvas.coords(logs[i])
            if overlappingWithLogOrWater(playerPos, logPos):
                onLog = True
                break

        #If the player has collided with a river but not collided with a log
        for j in range(len(water)):
            waterPos = gameCanvas.coords(water[j])
            if onLog == False and overlappingWithLogOrWater(playerPos, waterPos):
                gameOver = True

        #If the player has exited the screen
        if(playerPos[0] < 0 or playerPos[0] > 1600):
            gameOver = True
            
        #If the game is over
        if("gameOver" in locals()):
            if(gameOver):
                root.after_cancel(isGameOver) #Stop calling isGameOver

                #Delete all the items on gameCanvas apart from player and score
                for i in range(len(cars)):
                    gameCanvas.delete(cars[i])
                for i in range(len(logs)):
                    gameCanvas.delete(logs[i])
                for i in range(len(roads)):
                    gameCanvas.delete(roads[i])
                for i in range(len(water)):
                    gameCanvas.delete(water[i])
                
                #Hide the player
                gameCanvas.itemconfigure(player, state = "hidden")

                #Show game over message
                messagebox.showinfo(title = "Level failed", message = "Unlucky, Game Over!")

                #Reset score
                global score
                score = 0
                
                #Go back to the levels screen
                pauseButton.place_forget()
                gameCanvas.pack_forget()
                menuCanvas.pack()
                quitButton.place(x = width - 500, y = 150, anchor = "center")
                backButton.place(x = 100, y = 600)
                levelsScreen()

    #If the game hasn't been won or lost, call isGameOver every 100ms
    if("gameOver" not in locals() and "gameWon" not in locals()):
        root.after(100, isGameOver)

#Shift the terrain upwards
def shiftTerrain():
    #Moves roads, rivers, cars and logs upwards
    for i in range(len(roads)):
        gameCanvas.move(roads[i], 0, -108)
    for i in range(len(water)):
        gameCanvas.move(water[i], 0, -108)
    for i in range(len(cars)):
        gameCanvas.move(cars[i], 0, -108)
    for i in range(len(logs)):
        gameCanvas.move(logs[i], 0, -108)
    gameCanvas.move(player, 0, -108) #Move player upwards

#Moves the player
def movePlayer():
    #If the game is not paused
    if(paused == False):
        playerPos = gameCanvas.coords(player)

        global playerDirection
        global score

        #Move left
        if(playerDirection == 'left' and playerPos[0] > 108):
            gameCanvas.move(player, -108, 0)
            playerDirection = None #Stop moving

        #Move right
        if(playerDirection == 'right' and playerPos[0] < 1300):
            gameCanvas.move(player, 108, 0)
            playerDirection = None

        #Move up
        if(playerDirection == 'up' and playerPos[1] > 108):
            gameCanvas.move(player, 0, -108)
            playerDirection = None
            #If player is cheating, increase score by 100
            if(cheat):
                score += 100
            else:
                score -= 10 #Else, decrease score
            gameCanvas.itemconfigure(scoreText, state = "normal", text = "Score : " + str(score))
        
        #Move down
        if(playerDirection == 'down'):
            gameCanvas.move(player, 0, 108)
            playerDirection = None
            #If player is cheating, increase score by 100
            if(cheat):
                score += 100
            else:
                score += 10 #Else, increase score by 10
            gameCanvas.itemconfigure(scoreText, state = "normal", text = "Score : " + str(score))

        #If the player has moved more than halfway down the screen
        if playerPos[1] > height/2 + 108:
            shiftTerrain()

        playerPos.clear() #Clear the playerPos array
    
    #If the player is visible, call movePlayer every 100ms
    if(gameCanvas.itemcget(player, 'state') == "normal"):
        root.after(100, movePlayer) 

#Called when the leader board button is pressed
def leaderboardOption():
    hideMainMenu()

    backButton.pack()
    backButton.place(x = 100, y = 500)
    backButton.configure(command = leaderboardBack)

    #Copy the array of scores and names
    scores = users["score"].copy()
    names = users["name"].copy()

    #Sort the scores in descending orders
    for i in range(1, len(scores)):
        for j in range(len(scores) - 1):
            if scores[i] > scores[j]:
                temp1 = scores[j]
                scores[j] = scores[i]
                scores[i] = temp1

                temp2 = names[j]
                names[j] = names[i]
                names[i] = temp2
            
    #Display the leaderboard
    global position, name, userScore
    position = []
    name = []
    userScore = []
    for i in range(len(scores)):
        position.append(menuCanvas.create_text(30, 50 + (50 * i), text = str(i + 1), font = "Times 20"))
        name.append(menuCanvas.create_text(330, 50 + (50 * i), text = names[i], font = "Times 20"))
        userScore.append(menuCanvas.create_text(630, 50 + (50 * i), text = scores[i], font = "Times 20"))
    
    #Clear the scores and names array
    scores.clear()
    names.clear()

#Called when the back button on the leader board screen is pressed
def leaderboardBack():
    #Delete all text
    global position, name, userScore
    for i in range(len(position)):
        menuCanvas.delete(position[i])
        menuCanvas.delete(name[i])
        menuCanvas.delete(userScore[i])
    
    #Go back to the main menu
    backButton.place_forget()
    mainMenu()

#Called when the settings button is pressed
def settingsOption():
    #Hide the main menu
    hideMainMenu()

    backButton.pack()
    backButton.place(x = 100, y = 500)
    backButton.configure(command = settingsBack)

    global left, right, up, down, leftEntry, rightEntry, upEntry, downEntry, leftText, rightText, upText, downText

    #Create entry fields for each of the inputs
    leftEntry = tk.Entry(root)
    rightEntry = tk.Entry(root)
    upEntry = tk.Entry(root)
    downEntry = tk.Entry(root)

    leftEntry.pack()
    rightEntry.pack()
    upEntry.pack()
    downEntry.pack()

    leftEntry.place(x = 500, y = 100)
    rightEntry.place(x = 500, y = 200)
    upEntry.place(x = 500, y = 300)
    downEntry.place(x = 500, y = 400)

    #Create text displaying the key bind for the corresponding input
    leftText = menuCanvas.create_text(400, 100, text = "Left: " + left, font = "Times 20")
    rightText = menuCanvas.create_text(400, 200, text = "Right: " + right, font = "Times 20")
    upText = menuCanvas.create_text(400, 300, text = "Up: " + up, font = "Times 20")
    downText = menuCanvas.create_text(400, 400, text = "Down: " + down, font = "Times 20")

    checkEntry() #Checks the entry field

#Called when the back button on the settings screen is pressed
def settingsBack():
    #Remove the entry fields and text from the settings screen
    leftEntry.place_forget()
    rightEntry.place_forget()
    upEntry.place_forget()
    downEntry.place_forget()

    menuCanvas.delete(leftText)
    menuCanvas.delete(rightText)
    menuCanvas.delete(upText)
    menuCanvas.delete(downText)

    #Go back to the main menu
    backButton.place_forget()
    mainMenu()

#Checks the entry field to see when a character has been entered
def checkEntry():
    #Get the data in the entry fields
    a = leftEntry.get()
    b = rightEntry.get()
    c = upEntry.get()
    d = downEntry.get()   

    #If a character has been entered
    if(len(a) == 1):
        leftEntry.delete(0, "end") #Delete this from the entry field
        left = a
        gameCanvas.bind(left, leftKey) #Bind this to the key
        menuCanvas.itemconfigure(leftText, text = "Left: " + left) #Display the text showing this update
    elif(len(b) == 1):
        rightEntry.delete(0, "end")
        right = b
        gameCanvas.bind(right, rightKey)
        menuCanvas.itemconfigure(rightText, text = "Right: " + right)
    elif(len(c) == 1):
        upEntry.delete(0, "end")
        up = c
        gameCanvas.bind(up, upKey)
        menuCanvas.itemconfigure(upText, text = "Up: " + up)
    elif(len(d) == 1):
        downEntry.delete(0, "end")
        down = d
        gameCanvas.bind(down, downKey)
        menuCanvas.itemconfigure(downText, text = "Down: " + down)

    #If the settings screen is active, call checkEntry every 50ms
    if(leftEntry.winfo_exists()):
        root.after(50, checkEntry)

#Buttons for the main menu
playButton = tk.Button(root, image = play, width = 200, height = 200, command = playOption)
leaderboardButton = tk.Button(root, image = leaderboard, width = 200, height = 200, command = leaderboardOption)
settingsButton = tk.Button(root, image = settings, width = 200, height = 200, command = settingsOption)
quitButton = tk.Button(root, image = quit, width = 200, height = 200, command = quitOption)

#Text to be displayed in the menu screens
crossyText = menuCanvas.create_text(300, 300, font = 'Times 80', fill = red, text = "Crossy")
roadText = menuCanvas.create_text(300, 450, font = 'Times 80', fill = red, text = "Road")

#Main menu
def mainMenu():
    menuCanvas.focus_set()
    #Text is visible
    menuCanvas.itemconfigure(crossyText, state = 'normal')
    menuCanvas.itemconfigure(roadText, state = 'normal')

    #Packs buttons against the top
    playButton.pack(side = "top")
    leaderboardButton.pack(side = "top")
    settingsButton.pack(side = "top")
    
    #Packs button against the right
    quitButton.pack(side = "right")

    #Places buttons in specified position
    playButton.place(x = width/2 - 200, y = 150, anchor = "center")
    leaderboardButton.place(x = width/2 - 200, y = 400, anchor = "center")
    settingsButton.place(x = width/2 - 200, y = 650, anchor = "center")
    quitButton.place(x = width - 500, y = 150, anchor = "center")

#Hides widgets on the main menu
def hideMainMenu():
    playButton.place_forget()
    leaderboardButton.place_forget()
    settingsButton.place_forget()

    menuCanvas.itemconfigure(crossyText, state = 'hidden')
    menuCanvas.itemconfigure(roadText, state = 'hidden')

#Checks if the boss key has been pressed
def checkBoss():
    global boss
    global pause
    #If the boss key has been pressed
    if(boss == True):
        window = tk.Toplevel(root) #Create a new window
        window.title("Stocks")
        window.geometry("1920x1080")
        window.attributes("-topmost", True) #On top of the current window
        tk.Label(window, image = bossScreen).place(x = 0, y = 0)
        boss = False
    
    #Call checkBoss every 100ms
    root.after(100, checkBoss)
    
checkBoss()

menuCanvas.pack() #Canvas is visible

mainMenu() #Main menu is diplayed first

root.mainloop() 
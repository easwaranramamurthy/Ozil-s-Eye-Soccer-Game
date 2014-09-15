import pygame
import random
import math
import sys
import time

#ball and player are sprites in the game
class Ball(pygame.sprite.Sprite):
	def __init__(self, data):
		#calls sprite superclass
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.image.load("Soccer Ball.png").convert()		
		self.image.set_colorkey(data.white)
		self.image=pygame.transform.scale(self.image,(data.ballSize,
			data.ballSize))
		self.speed=0
		self.dir=[0,0]
		#stores coordinates
		self.rect=self.image.get_rect()
		
class Player(pygame.sprite.Sprite):
	def __init__(self, data, playerName, position, color):
		pygame.sprite.Sprite.__init__(self)
		if color==data.red:
			#loads red player image
			self.image=pygame.image.load("Player Image1.png").convert()
		else:
			#loads blue player image
			self.image=pygame.image.load("Player Image2.png").convert()
		#for transparency
		self.image.set_colorkey(data.white)
		self.image=pygame.transform.scale(self.image,(data.playerSize,
			data.playerSize))
		self.speed=0
		self.angle=0.5 * math.pi - math.atan2(0, 0)
		self.dir=[0,0]
		self.destination=[None, None]
		#stores the formation position of player (i.e.Goalie,Forward,Defender)
		self.position=position
		self.possession=False
		self.rect=self.image.get_rect()
		self.currentPlayer=False

def makeBall(data):
	#creates the ball
	data.ballSize=15
	#creates the ball
	data.ball=Ball(data)
	#puts it at the center of the field
	data.ball.rect.x=data.margin+data.fieldWidth/2-data.ballSize/2
	data.ball.rect.y=data.margin+data.fieldHeight/2-data.ballSize/2
	#makes it a sprite
	data.allSpritesList.add(data.ball)

def mousePressed(data):
	data.mousePos = pygame.mouse.get_pos()
	#mouse presses meant to work only in menu screen
	if data.displayMenu==True:
		menuMousePressed(data)

def menuMousePressed(data):
	#handles mouse presses in the main menu
	#for the play AI button
	if (data.play1Coord[0]<data.mousePos[0]<data.play1Coord[0]+
		data.menuButtonWidth and data.play1Coord[1]<data.mousePos[1]<
		data.play1Coord[1]+data.menuButtonHeight):
			data.playAI=True
			data.displayMenu=False
			initAIGame(data)
	#for the challenge mode button
	elif (data.play2Coord[0]<data.mousePos[0]<data.play2Coord[0]+
		data.menuButtonWidth and data.play2Coord[1]<data.mousePos[1]<
		data.play2Coord[1]+data.menuButtonHeight):		
			data.challengeMode=True
			data.displayMenu=False
			initChallengeMode(data)
	#for the instruction button
	elif (data.instructionCoord[0]<data.mousePos[0]<data.instructionCoord[0]+
		data.menuButtonWidth and data.instructionCoord[1]<data.mousePos[1]<
		data.instructionCoord[1]+data.menuButtonHeight):
			data.displayInstruction=True
			data.displayMenu=False

def keyPressed(data, event):
	#different key presses for different screens
	if data.challengeMode==True or data.playAI==True:
		#handles game key presses
		AIKeyPressed(data, event)
	elif data.displayInstruction==True:
		#handles key presses on instruction screen
		instructionKeyPressed(data, event)
	elif data.gameOver==True:
		#handles key presses on game over screens
		gameOverKeyPressed(data, event)
		
def gameOverKeyPressed(data, event):
	#goes back to main menu if 'r' is pressed
	if event.key==pygame.K_r:
		data.gameOver=False
		data.displayMenu=True
		
def instructionKeyPressed(data, event):
	#back to main menu if 'r' is pressed
	if event.key==pygame.K_r:
		data.displayInstruction=False
		data.displayMenu=True

def initScreen(data):
	#main function
	#sets margin
	data.margin=70
	data.width=700
	data.height=680
	data.fieldWidth=360
	data.fieldHeight=540
	data.clock=pygame.time.Clock()
	data.screen=pygame.display.set_mode((data.width,data.height))
	#sets the name of the game
	pygame.display.set_caption("Ozil's Eye")
	#puts field on the screen
	#
	data.field=pygame.image.load("Soccer Field.png").convert()
	data.gameOver=False
	
def initColors(data):
	data.red=(255,0,0)
	data.blue=(0,0,255)
	data.white=(255,255,255)
	data.yellow=(255,255,0)
	data.black=(0,0,0)
	
def initMenuVariables(data):
	data.menuButtonWidth=314
	data.menuButtonHeight=150	
	#states for which screens to display or run
	data.displayMenu=True
	data.challengeMode=False
	data.displayInstruction=False
	data.playAI=False
	#coordinates of menu buttons
	data.play1Coord=(data.width/2-data.menuButtonWidth/2,
		data.height/2-2*data.menuButtonHeight)
	data.play2Coord=(data.width/2-data.menuButtonWidth/2,
		data.height/2-0.5*data.menuButtonHeight)
	data.instructionCoord=(data.width/2-data.menuButtonWidth/2,
		data.height/2+data.menuButtonHeight)

def initTeams(data):
	#creates all players and puts them in their respective teams
	for team in data.teamList:
		positionIndex=0
		for playerName in data.teamList[team]:
			player=Player(data, playerName, data.positionList[positionIndex],
				data.teamColor[team])
			data.allSpritesList.add(player)
			data.playerList.add(player)
			if team=="Team A":
				data.homePlayerList.add(player)
			else:
				data.awayPlayerList.add(player)
			placePlayers(data, player, team, positionIndex)
			#next player created at new position
			positionIndex+=1

#functions to move current user player based on key presses
def turnLeft(data):
	data.currentHomePlayer.rect.x-=5
	data.currentHomePlayer.dir[0]=-1
	#out of bounds conditions
	if data.currentHomePlayer.rect.x<data.fieldLeft:
		data.currentHomePlayer.rect.x+=5
		data.currentHomePlayer.dir=[0,0]
		return
	#puts ball on left of player if in possession
	if data.currentHomePlayer.possession==True:
		data.ball.rect.x=data.currentHomePlayer.rect.x-data.ballSize
		data.ball.rect.y=data.currentHomePlayer.rect.y+data.playerSize/2\
			-data.ballSize/2
		
def turnRight(data):
	data.currentHomePlayer.rect.x +=5
	data.currentHomePlayer.dir[0]=1
	#out of bounds conditions
	if data.currentHomePlayer.rect.x+data.playerSize>data.fieldRight:
		data.currentHomePlayer.rect.x-=5
		data.currentHomePlayer.dir=[0,0]
		return
	#puts ball on right of player
	if data.currentHomePlayer.possession==True:
		data.ball.rect.x=data.currentHomePlayer.rect.x+data.playerSize
		data.ball.rect.y=data.currentHomePlayer.rect.y+data.playerSize/2\
			-data.ballSize/2
		
def turnUp(data):
	data.currentHomePlayer.rect.y -=5
	data.currentHomePlayer.dir[1]=-1
	#out of bounds conditions
	if data.currentHomePlayer.rect.y<data.fieldTop:
		data.currentHomePlayer.rect.y+=5
		data.currentHomePlayer.dir=[0,0]
		return
	#puts ball on top of player
	if data.currentHomePlayer.possession==True:
		data.ball.rect.x=data.currentHomePlayer.rect.x+data.playerSize/2\
			-data.ballSize/2
		data.ball.rect.y=data.currentHomePlayer.rect.y-data.ballSize

def turnDown(data):
	data.currentHomePlayer.rect.y +=5
	if data.currentHomePlayer.rect.y>data.upBoxEdgeY:
		data.shootMessage=None
	data.currentHomePlayer.dir[1]=1
	if data.currentHomePlayer.rect.y>data.fieldBottom-data.playerSize:
		data.currentHomePlayer.rect.y-=5
		data.currentHomePlayer.dir=[0,0]
		return	
	#puts ball on bottom of player
	if data.currentHomePlayer.possession==True:
		data.ball.rect.x=data.currentHomePlayer.rect.x+data.playerSize/2\
			-data.ballSize/2
		data.ball.rect.y=data.currentHomePlayer.rect.y+data.playerSize

def redrawAll(data):
	if data.gameOver==False:
		data.screen.fill(data.red)
	if data.displayMenu==True:
		#draws main menu
		drawStartMenu(data)
	if data.challengeMode==True or data.playAI==True:
		if data.gameOver==True:
			drawGameOver(data)
		else:
			drawGame(data)
	elif data.displayInstruction==True:
		drawInstructions(data)
	pygame.display.flip()

def drawGameOver(data):
	#challenge mode has different game over conditions
	if data.challengeMode==True:
		data.challengeMode=False
		if data.result=="win":
			screen = pygame.image.load("Win Screen.png").convert()
			data.screen.blit(screen, (0,0))		
		else:
			screen = pygame.image.load("Loss Screen.png").convert()
			data.screen.blit(screen, (0,0))	
	#different game over conditions for play vs AI mode
	elif data.playAI==True:
		data.playAI=False
		if data.result=="AI win":
			screen=pygame.image.load("AI Win Screen.png").convert()
			data.screen.blit(screen, (0,0))
		elif data.result=="AI loss":
			screen=pygame.image.load("AI Loss Screen.png").convert()
			data.screen.blit(screen, (0,0))
		elif data.result=="AI draw":
			screen=pygame.image.load("AI Draw Screen.png").convert()
			data.screen.blit(screen, (0,0))
	
def drawGame(data):
	pygame.draw.rect(data.screen, data.white, (0,0,data.width,data.height),0)
	#draws the field
	data.screen.blit(data.field,[data.margin,data.margin])		
	#draws all sprites
	data.allSpritesList.draw(data.screen)
	for player in data.playerList:
		if player.currentPlayer==True:
			#puts a circle around the current player
			pygame.draw.circle(data.screen, data.white,
				(player.rect.x+data.playerSize/2,
					player.rect.y+data.playerSize/2),data.playerSize/2+5, 1)
	#shoot error message displaying
	if data.shootMessage!=None:
		font = pygame.font.SysFont('times new roman', 20, bold=True,
			italic=False)
		text = font.render(data.shootMessage,True,data.black)
		data.screen.blit(text, (data.margin+data.fieldWidth+20,
			data.margin+460))
	#draws score and game time
	drawScoreAndTime(data)

def drawScoreAndTime(data):
	totalSeconds=data.gameTime/1000
	minutes=totalSeconds/60
	seconds=totalSeconds%60
	#time text
	text1="Time Remaining"
	text2="%d:%02d s"%(minutes, seconds)
	font = pygame.font.SysFont('times new roman', 30, bold=True,
		italic=False)
	timeText1 = font.render(text1,True,data.black)
	data.screen.blit(timeText1, (data.margin+data.fieldWidth+20,
		data.margin+100))	
	timeText2 = font.render(text2, True, data.black)
	data.screen.blit(timeText2, (data.margin+data.fieldWidth+80,
		data.margin+160))
	#score text different for different modes
	if data.challengeMode==True:
		drawChallengeScoreText(data)
	elif data.playAI==True:
		drawPlayAIScoreText(data)

def drawPlayAIScoreText(data):		
	font = pygame.font.SysFont('times new roman', 20, bold=True,
		italic=False)
	#team 1 named cretins and team 2 named hypocrites
	scoreText1=font.render("Cretins %d-%d Hypocrites"%(data.homeGoals,
		data.awayGoals), True, data.black)
	data.screen.blit(scoreText1, (data.margin+data.fieldWidth+25,
		data.margin+220))
		
def drawChallengeScoreText(data):		
	font = pygame.font.SysFont('times new roman', 20, bold=True,
		italic=False)	
	#draws score for challenge mode
	scoreText1=font.render("Goals Scored", True, data.black)
	data.screen.blit(scoreText1, (data.margin+data.fieldWidth+20,
		data.margin+220))
	scoreText2=font.render("%d" %data.goalsScored, True, data.black)
	data.screen.blit(scoreText2, (data.margin+data.fieldWidth+100,
		data.margin+280))
	scoreText3=font.render("Total Goals Needed", True, data.black)
	data.screen.blit(scoreText3, (data.margin+data.fieldWidth+20,
		data.margin+340))
	scoreText4=font.render("%d" %data.totalGoals, True, data.black)
	data.screen.blit(scoreText4, (data.margin+data.fieldWidth+100,
		data.margin+400))	

def drawInstructions(data):
	#loads instructons screen
	screen = pygame.image.load("Instruction Screen.png").convert()
	data.screen.blit(screen, (0,0))

def drawStartMenu(data):
	#draws the start menu
	background = pygame.image.load("Background.png").convert()
	data.screen.blit(background, (0,0))
	#creates three buttons
	menuButton=pygame.image.load("Menu Button.png").convert()
	data.screen.blit(menuButton, data.play1Coord)
	drawMenuText(data,"PLAY AI", data.play1Coord)
	data.screen.blit(menuButton, data.play2Coord)
	drawMenuText(data,"CHALLENGE MODE", data.play2Coord)
	data.screen.blit(menuButton, data.instructionCoord)
	drawMenuText(data, "INSTRUCTIONS", data.instructionCoord)
	
def drawMenuText(data, text, coord):
	#creates text on the menu buttons
	font = pygame.font.SysFont('lucida handwriting', 26, bold=True, 
		italic=False)
	option = font.render(text,True,data.white)
	data.screen.blit(option, (coord[0]+20,
		coord[1]+data.menuButtonHeight/2-30))

def startSoccer():
	#main functions that is first called
	pygame.init()
	#allows for hard key presses
	pygame.key.set_repeat(10,10)
	class Struct: pass
	data=Struct()
	initScreen(data)
	initColors(data)
	initMenuVariables(data)
	data.playerSize=20
	data.fieldLeft=data.margin+7
	data.fieldRight=data.margin+351
	#speed of the ball when a shot is taken on goal
	data.shotSpeed=30
	data.playerSpeed=5
	data.fieldTop=data.margin+27
	data.fieldBottom=data.margin+513
	data.goalLeft=data.margin+142
	data.goalRight=data.margin+218
	data.upBoxEdgeY=data.margin+123
	data.downBoxEdgeY=data.margin+417
	redrawAll(data)
	while True:
		timerFired(data)
	
def initChallengeMode(data):
	#starts the challenge mode
	#sets initial possessing team to the home team (user controlled)	
	data.gameTime=90000 #90 seconds, time taken in milliseconds
	#total goals needed
	data.totalGoals=10
	data.goalsScored=0
	data.gameOver=False
	data.result=None
	initNewPlay(data)

def initAIGame(data):
	#starts the play vs AI mode
	data.gameTime=300000 #300 seconds = 5 minutes
	#variables to store goals of both teams
	data.homeGoals=0
	data.awayGoals=0
	data.gameOver=False
	data.result=None
	initNewAIPlay(data)
	
def initNewAIPlay(data):
	#radius of the extra player in AI Mode
	data.extraMoveRadius=60
	#same game start as challenge mode
	initNewPlay(data)
	#certain differences overriden
	data.radiusList={"RCB": data.defendMoveRadius,
		"LCB": data.defendMoveRadius,"RF": data.attackMoveRadius,
		"LF": data.attackMoveRadius, "Extra": data.extraMoveRadius}
	data.centerList["Extra"]=(data.margin+data.fieldWidth/2,data.margin+360)
	data.anglesList["Extra"]=180
	data.angleUpdateList["Extra"]=1
	data.extraOmega=10
	data.awayShotTaken=False

#function to start a new play	
def initNewPlay(data):
	data.possessingTeam="Home"
	data.allSpritesList=pygame.sprite.Group()	
	#time elapsed before possession changes can occur again
	data.changeThreshold=1
	#cannot shoot from above the upper box edge
	data.shootThreshold=110
	data.shotTaken=False
	data.shootMessage=None
	#angular speed of rotating players
	data.omega=5
	data.defendMoveRadius=70
	data.attackMoveRadius=60
	#inits radii and angles of away players
	initMotionVariables(data)
	#last possession change time
	data.possessionChangeTime=time.time()
	makeBall(data)
	initPositions(data)
	initTeams(data)

#initializes variables required to move players in circles
def initMotionVariables(data):
	#inits radii of different players in different positions
	data.radiusList={"RCB": data.defendMoveRadius,
		"LCB": data.defendMoveRadius,"RF": data.attackMoveRadius,
		"LF": data.attackMoveRadius}
	#inits centers
	data.centerList={"RCB":(data.margin+100,data.margin+120),
		"LCB": (data.margin+data.fieldWidth-100,data.margin+120),
		"RF": (data.margin+100,data.margin+120+data.defendMoveRadius
			+data.attackMoveRadius),
		"LF": (data.margin+data.fieldWidth-100,data.margin+120+
			data.defendMoveRadius+data.attackMoveRadius)}
	#inits start angles of players
	data.anglesList={"RCB":0,"LCB":0,"RF":0,"LF":0}
	#inits direction of rotation (clockwise, counter-clockwise)
	data.angleUpdateList={"RCB":-1,"LCB":1,"RF":1,"LF":-1}

def initPositions(data):
	#creates sprite groups
	#will store all players
	data.playerList=pygame.sprite.Group()
	#will store user controlled players
	data.homePlayerList=pygame.sprite.Group()
	#will store ai players
	data.awayPlayerList=pygame.sprite.Group()
	data.teamList={"Team A":("Amelia", "Andre", "Andrew", "Angela", "Anqi"),
		"Team B":("Charlie", "Chris", "Connor", "Dena", "Edison")}		
	#team colors
	#user color is red
	#ai color is blue
	data.teamColor={"Team A": data.red, "Team B": data.blue}
	#5 positions for 5 players on each team
	data.positionList=["GK", "RCB", "LCB", "RF", "LF"]
	if data.playAI==True:
		#adds a new player "Kosbie" to the away team in play AI mode
		data.teamList={"Team A":
			("Amelia", "Andre", "Andrew", "Angela", "Anqi"),
			"Team B":("Charlie", "Chris", "Connor", "Dena",
			"Edison", "Kosbie")}
		#extra position added to position list
		data.positionList.append("Extra")
	fixPositions(data)

def fixPositions(data):
	#home player positions
	initHomePlayerPositions(data)
	initAwayPlayerPositions(data)

def initHomePlayerPositions(data):
	margin=data.margin
	fieldWidth=data.fieldWidth
	fieldHeight=data.fieldHeight
	fieldCenterX=margin+fieldWidth/2
	fieldCenterY=margin+fieldHeight/2
	playerSize=data.playerSize
	#home player positions
	data.homePlayerPositions=\
	{"GK":(margin+fieldWidth/2,margin+fieldHeight-50),
	"RCB":(margin+fieldWidth/2+100,margin+fieldHeight-120),
	"LCB": (margin+fieldWidth/2-100,margin+fieldHeight-120),
	"RF": (margin+fieldWidth/2+data.playerSize/2,
		margin+fieldHeight/2+playerSize/2),
	"LF": (margin+fieldWidth/2-data.playerSize/2,
		margin+fieldHeight/2+playerSize/2)}

def initAwayPlayerPositions(data):		
	margin=data.margin
	fieldWidth=data.fieldWidth
	fieldHeight=data.fieldHeight
	fieldCenterX=margin+fieldWidth/2
	fieldCenterY=margin+fieldHeight/2
	playerSize=data.playerSize	
	#away player positions
	data.awayPlayerPositions=\
	{"GK":(margin+fieldWidth/2,margin+35),
	"RCB":(margin+100+data.defendMoveRadius,margin+120),
	"LCB": (margin+fieldWidth-100+data.defendMoveRadius,margin+120),
	"RF": (margin+100+data.attackMoveRadius,margin+120+
		data.defendMoveRadius+data.attackMoveRadius),
	"LF": (margin+fieldWidth-100+data.attackMoveRadius,margin+120
		+data.defendMoveRadius+data.attackMoveRadius)
	}
	#extra player added if play ai mode is being played
	if data.playAI==True:
		data.awayPlayerPositions["Extra"]=(data.margin+data.fieldWidth/2
			+data.extraMoveRadius,data.margin+360)

def placePlayers(data, player, team, positionIndex):
	#places all players in their respective positions
	position=data.positionList[positionIndex]
	if team=="Team A":
		#places players according to the position dictionary created earlier
		player.rect.x=data.homePlayerPositions[position][0]-data.playerSize/2
		player.rect.y=data.homePlayerPositions[position][1]-data.playerSize/2
		if position=="LF":
			#initial current player for each team is the left forward
			data.currentHomePlayer=player
			player.currentPlayer=True
			player.possession=True
	else:
		player.rect.x=data.awayPlayerPositions[position][0]-data.playerSize/2
		player.rect.y=data.awayPlayerPositions[position][1]-data.playerSize/2
		if position=="LF":
			data.currentAwayPlayer=player
			player.currentPlayer=True			
	for nPlayer in data.playerList:
		#sets all player destinations to their current positions so they 
		#don't move
		nPlayer.destination=[nPlayer.rect.x, nPlayer.rect.y]

def timerFired(data):
	#manual event handling
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif event.type==pygame.MOUSEBUTTONDOWN:
			mousePressed(data)
		elif event.type==pygame.KEYDOWN:
			keyPressed(data, event)
	if data.challengeMode==True:
		playChallengeMode(data)
	elif data.playAI==True:
		playAIMode(data)
	data.clock.tick(20)
	redrawAll(data)

def playAIMode(data):
	#move away players
	moveAwayPlayers(data)
	if data.possessingTeam==None:
		#if ball is free i.e no one is possessing it,
		#it moves with it's own speed
		moveBall(data)	
	#if collision is detected, it switches possession to different players
	makePossessionChanges(data)
	if data.possessingTeam=="Away":
		awayShooting(data)
	if data.shotTaken==True:
		checkHomeGoalScored(data)
	elif data.awayShotTaken==True:
		checkAwayGoalScored(data)
	#moves all home players with a given destination
	#(used for goalie movement)
	moveGoalie(data)
	#ticking the game clock
	data.gameTime-=50
	checkAIGameOver(data)
	
def checkAIGameOver(data):
	if data.gameTime==0:
		data.gameOver=True
		#different game over scenarios
		if data.homeGoals>data.awayGoals:
			data.result="AI win"
		elif data.homeGoals<data.awayGoals:
			data.result="AI loss"
		else:
			data.result="AI draw"

def awayShooting(data):
	#function to make shots if extra player is near goal
	for player in data.awayPlayerList:
		#only the extra player shoots when he is nearest to goal
		if player.position=="Extra" and player.possession==True:
			#360 is the full circle
			#270 is the angle where player is at his bottom most point
			if data.anglesList["Extra"]%360==270:
				#makes the shot
				shootAtHomeGoal(data)
				data.awayShotTaken=True
				#now player is no longer in possession
				player.possession=False


def playChallengeMode(data):
	moveAwayPlayers(data)
	#if ball is free i.e no one is possessing it,
	#it moves with it's own speed	
	if data.possessingTeam==None:
		moveBall(data)	
	#if collision is detected, it switches possession to different players
	makePossessionChanges(data)
	if data.shotTaken==True:
		checkHomeGoalScored(data)
	#moves all players with a destination
	#useful for goalie movement
	moveGoalie(data)
	#clock ticking
	data.gameTime-=50
	#game over conditions
	if data.goalsScored==data.totalGoals:
		#player wins if he reaches max goal limit
		data.gameOver=True
		data.result="win"	
	elif data.gameTime==0:
		data.gameOver=True
		data.result="loss"
	
def moveAwayPlayers(data):
	#moves away players in circles
	for player in data.awayPlayerList:
		if player.position in data.radiusList:
			key=player.position	
			if key=="Extra":
				#extra player moves with a different angular speed
				data.anglesList[key]+=\
					data.angleUpdateList[key]*data.extraOmega
			else:
				#other players move with same angular speed
				data.anglesList[key]+=\
					data.angleUpdateList[key]*data.omega
			#conversion to radians
			theta=math.radians(data.anglesList[key])
			#updates player to next position on circle
			player.rect.x=data.centerList[key][0]\
				+data.radiusList[key]*math.cos(theta)-data.playerSize/2
			player.rect.y=data.centerList[key][1]\
				-data.radiusList[key]*math.sin(theta)-data.playerSize/2
			#moves ball along with player if he is in possession
			#ball is on outer side of circle always
			if player.possession==True:
				moveBallWithPlayer(data, key, theta)
			
def moveBallWithPlayer(data, key, theta):
	data.ball.rect.x=data.centerList[key][0]+\
		(data.radiusList[key]+data.playerSize/2+
		data.ballSize/2)*math.cos(theta)-data.ballSize/2
	data.ball.rect.y=data.centerList[key][1]-\
		(data.radiusList[key]+data.playerSize/2+
		data.ballSize/2)*math.sin(theta)-data.ballSize/2
			
def moveGoalie(data):
	#moves goalie to its destination
	for player in data.playerList:
		#won't move Gk if user controls him
		if player!=data.currentHomePlayer:
			#only for gk
			if player.position=="GK":
				#moves gk if he is not at his destination
				if [player.rect.x, player.rect.y]!=player.destination:
					player.rect.x+=player.dir[0]*player.speed
					player.rect.y+=player.dir[1]*player.speed
					#stopping conditions
					if ((abs(player.rect.x+data.playerSize/2-
						player.destination[0])<data.playerSize)
						and (abs(player.rect.y+data.playerSize/2
						-player.destination[1])<data.playerSize)):				
						player.speed=0
						player.dir=[0,0]
						#sets goalie destination to his current position
						#now he cannot move
						player.destination=[player.rect.x, player.rect.y]
	
def makePossessionChanges(data):
	#makes changes in possession
	#for home player winning the ball
	makeHomeChange(data)
	#for away player winning the ball
	makeAwayChange(data)
	
def makeHomeChange(data):
	if time.time()-data.possessionChangeTime>data.changeThreshold:
		collision=pygame.sprite.spritecollide(data.ball,
			data.homePlayerList, False)	
		#if collision occurred it will switch possession to him
		if collision!=[]:
			if collision[0].possession!=True:
				#shot is no longer valid as player has ball
				data.shotTaken=False
				data.awayShotTaken=False
				#sets all destinations to current position
				for player in data.playerList:
					if player.possession==True:
						player.dir=[0,0]
						player.destination=[player.rect.x, player.rect.y]			
				#possession status made false for all players
				for player in data.playerList:
					player.possession=False
				for player in data.homePlayerList:
					player.currentPlayer=False
				#possession status made true for new player
				collision[0].possession=True
				collision[0].currentPlayer=True
				data.currentHomePlayer=collision[0]
				data.possessingTeam="Home"
				data.possessionChangeTime=time.time()
		
def makeAwayChange(data):		
	#makes change only if threshold has passed
	if time.time()-data.possessionChangeTime>data.changeThreshold:
		#collision with away player
		collision=pygame.sprite.spritecollide(data.ball,
			data.awayPlayerList, False)
		if collision!=[]:
			if collision[0].possession!=True:
				data.shotTaken=False
				data.awayShotTaken=False
				for player in data.playerList:
					if player.possession==True:
						player.dir=[0,0]
						player.destination=[player.rect.x, player.rect.y]		
				for player in data.playerList:
					player.possession=False				
				for player in data.awayPlayerList:
					player.currentPlayer=False
				collision[0].possession=True
				collision[0].currentPlayer=True
				player=collision[0]
				data.ball.rect.x=player.rect.x+data.playerSize/2\
					-data.ballSize/2
				data.ball.rect.y=player.rect.y+data.playerSize
				data.possessingTeam="Away"
				data.possessionChangeTime=time.time()

def checkHomeGoalScored(data):
	#checks for home goal scored
	if data.ball.rect.y==data.fieldTop:
		#if ball withing goal limits
		if data.goalLeft<data.ball.rect.x<data.goalRight-data.ballSize:
			if data.playAI==True:
				data.homeGoals+=1
				#new play initiated if goal scored
				initNewAIPlay(data)
			elif data.challengeMode==True:
				#similarly for challenge mode
				data.goalsScored+=1
				initNewPlay(data)
		else:
			data.shotTaken=False
			
def checkAwayGoalScored(data):
	#checks away goals being scored
	if data.ball.rect.y+data.ballSize==data.fieldBottom:
		if data.goalLeft<data.ball.rect.x<data.goalRight-data.ballSize:
			data.awayGoals+=1
			initNewAIPlay(data)
		else:
			data.awayShotTaken=False
		
def shootRandomAtGoal(data):
	data.shotTaken=True
	data.ball.speed=data.shotSpeed
	#sets ball destinations randomly
	destinationX=random.randrange(data.goalLeft, data.goalRight)
	#y destination is still the top of the field
	if data.possessingTeam=="Home":
		destinationY=data.fieldTop	
	#AI tries to save the shot if shot made
	saveShot(data, destinationX)
	#calculates ball dirs
	angle=math.atan2(destinationX-(data.ball.rect.x+data.ballSize/2),
		data.fieldTop-(data.ball.rect.y+data.ballSize/2))
	data.ball.dir[0]=math.sin(angle)
	data.ball.dir[1]=math.cos(angle)	
	data.currentHomePlayer.possession=False
	data.currentAwayPlayer.possession=False
	data.possessingTeam=None

def shootAtHomeGoal(data):
	#makes shoots at the home goal
	data.possessionChangeTime=0
	data.awayShotTaken=True
	data.ball.speed=data.shotSpeed-5
	destinationX=random.randrange(data.goalLeft, data.goalRight)
	destinationY=data.fieldBottom
	angle=math.atan2(destinationX-(data.ball.rect.x+data.ballSize/2),
		destinationY-(data.ball.rect.y+data.ballSize/2))
	data.ball.dir[0]=math.sin(angle)
	data.ball.dir[1]=math.cos(angle)	
	data.currentHomePlayer.possession=False
	data.currentAwayPlayer.possession=False
	data.possessingTeam=None
	
def shootStraight(data):
	#makes a straight shoot
	data.shotTaken=True
	data.ball.speed=data.shotSpeed
	destinationX=data.ball.rect.x+data.ballSize/2
	if data.possessingTeam=="Home":
		destinationY=data.fieldTop
	elif data.possessingTeam=="Away":
		destinationY=data.fieldBottom	
	saveShot(data, destinationX)
	angle=math.atan2(destinationX-(data.ball.rect.x+data.ballSize/2),
		data.fieldTop-(data.ball.rect.y+data.ballSize/2))
	data.ball.dir[0]=math.sin(angle)
	data.ball.dir[1]=math.cos(angle)	
	data.currentHomePlayer.possession=False
	data.currentAwayPlayer.possession=False
	data.possessingTeam=None	
	
def saveShot(data, destinationX):
	#makes AI goalie save the shot
	if data.possessingTeam=="Home":
		for player in data.awayPlayerList:
			if player.position=="GK":
				player.speed=data.playerSpeed
				player.dir[0]=1 if (destinationX>
					player.rect.x+data.playerSize/2) else -1
				player.destination=[destinationX,player.rect.y]
	else:
		for player in data.homePlayerList:
			if player.position=="GK":
				player.speed=data.playerSpeed
				player.dir[0]=1 if destinationX>(player.rect.x
					+data.playerSize) else -1
				player.destination=[destinationX, player.rect.y]

def moveBall(data):
	#moves the ball if it is free
	if data.ball.speed>0:
		data.ball.rect.x+=data.ball.dir[0]*data.ball.speed
		if data.ball.rect.x<data.fieldLeft:
			data.ball.rect.x=data.fieldLeft
			data.ball.dir[0]*=(-1)
		elif data.ball.rect.x>data.fieldRight-data.ballSize:
			data.ball.rect.x=data.fieldRight-data.ballSize
			data.ball.dir[0]*=(-1)
		data.ball.rect.y+=data.ball.dir[1]*data.ball.speed
		if data.ball.rect.y<data.fieldTop:
			data.ball.rect.y=data.fieldTop
			data.ball.dir[1]*=(-1)
		elif data.ball.rect.y>data.fieldBottom-data.ballSize:
			data.ball.rect.y=data.fieldBottom-data.ballSize
			data.ball.dir[1]*=(-1)
		#ball speed decreases as it moves
		data.ball.speed-=data.ball.speed*0.2
		data.ball.speed=int(data.ball.speed)
	else:
		#ball stopping condition		
		stopBall(data)
	data.ball.rect.x=int(data.ball.rect.x)
	data.ball.rect.y=int(data.ball.rect.y)
		
def stopBall(data):		
	data.ball.speed=0
	data.ball.dir=[0,0]
	data.shotTaken=False

def AIKeyPressed(data, event):
	#handles key presses in play vs AI mode
	keys = pygame.key.get_pressed()
	if keys[pygame.K_LEFT]:
		turnLeft(data)
	if keys[pygame.K_RIGHT]:
		turnRight(data)
	if keys[pygame.K_UP]:
		turnUp(data)
	if keys[pygame.K_DOWN]:
		turnDown(data)
	if data.possessingTeam=="Home":
		if keys[pygame.K_d]:
			if data.currentHomePlayer.rect.y>data.margin+data.shootThreshold:
				shootRandomAtGoal(data)	
			else:
				data.shootMesssage="You can't shoot from there"
		if keys[pygame.K_f]:
			if data.currentHomePlayer.rect.y>data.margin+data.shootThreshold:
				shootStraight(data)
			else:
				data.shootMessage="You can't shoot from there"
	else:
		if keys[pygame.K_q]:
			switchPlayer(data)
		if keys[pygame.K_g]:
			switchToGoalie(data)
			
def switchToGoalie(data):
	#shortcut switching to goalie
	data.currentHomePlayer.currentPlayer=False
	data.currentHomePlayer.dir=[0,0]
	for player in data.homePlayerList:
		if player.position=="GK":
			player.currentPlayer=True
			data.currentHomePlayer=player
			data.currentHomePlayer.dir=[0,0]
			data.currentHomePlayer.destination=[data.currentHomePlayer.rect.x,
				data.currentHomePlayer.rect.y]
			return
			
def switchPlayer(data):
	#switches between players
	#cycles through them
	if data.currentHomePlayer.position=="GK":
		nextPlayer="RCB"
	elif data.currentHomePlayer.position=="RCB":
		nextPlayer="LCB"
	elif data.currentHomePlayer.position=="LCB":
		nextPlayer="RF"
	elif data.currentHomePlayer.position=="RF":
		nextPlayer="LF"
	elif data.currentHomePlayer.position=="LF":
		nextPlayer="GK"
	data.currentHomePlayer.currentPlayer=False
	data.currentHomePlayer.dir=[0,0]
	for player in data.homePlayerList:
		if player.position==nextPlayer:
			player.currentPlayer=True
			data.currentHomePlayer=player
			data.currentHomePlayer.dir=[0,0]
			data.currentHomePlayer.destination=[data.currentHomePlayer.rect.x,
				data.currentHomePlayer.rect.y]
			return

#starts the game
startSoccer()
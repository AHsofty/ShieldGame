enemyspeed = 0.5

# Made by @a_hsoft
# Follow me on twitter ^
# If you run into any problems or have questions, feel free to contact me.
import turtle
import random


# setup
cheats = False # False = disable cheats // True = enable cheats. Default is False. You can also press space to enable/disable

ongoing = True
direction = "right"
enemy_from = None
chosen=False
points = 0
count = 0
move = True
coords = []
position = None
closest = None
cl = False
distances = []
coords = []
num = 0



wn = turtle.Screen()
wn.bgcolor("Orange")
wn.title("Don't get hit")
wn.tracer(0)
wn.setup(height=500, width=500, startx=500, starty=100)
wn.addshape("down.gif")
wn.addshape("up.gif")
wn.addshape("left.gif")
wn.addshape("right.gif")

# Creates the player
player = turtle.Turtle()
player.color("blue")
player.shape('right.gif')
player.speed(0)
player.goto(0,0)

# Creates a scoreboard
scoreboard = turtle.Turtle()
scoreboard.hideturtle()
scoreboard.penup()
scoreboard.goto(180, 200)
scoreboard.write(points, font=("courier", 24, "normal"))


"""
Create the enemies
"""
class Create_Enemies(turtle.Turtle):
	def __init__(self):
		turtle.Turtle.__init__(self)
		self.penup()
		self.color("red")
		self.speed(0)
		self.replace_enemies()
		self.shape("circle")

	def replace_enemies(self):
		global points
		global cl
		global enemies
		"""
		This function will replace the enemy
		"""
		cl = False
		num = random.randint(1,4)
		self.color("red")
		if num==1: 
			self.goto(player.xcor(), random.randint(300, 400))
		if num==2:
			self.goto(player.xcor(), random.randint(-500, -400))
		if num==3:
			self.goto(random.randint(500, 600), player.ycor())
		if num==4:
			self.goto(random.randint(-700, -600), player.ycor())


		self.setheading(self.towards(player.xcor(), player.ycor())) # Make the enemy look at the player


		distance_array = []
		for enem in enemies:
			distance_array.append(enem.distance(player))
		for idx, i in enumerate(distance_array):
			for x in distance_array:
				if i-x < 45 and i-x > 0:
					enemies[idx].replace_enemies()


enemies = []
for i in range(4):
	enemies.append(Create_Enemies())


def left():
	global player
	global direction
	global move
	if move:
		direction = "left"
		player.setheading(0)
		player.shape("left.gif")



def right():
	global player
	global direction
	global move
	if move:
		direction = "right"
		player.setheading(90)
		player.shape("right.gif")
		

def down():
	global player
	global direction
	global move
	if move:
		direction = "down"
		player.setheading(180)
		player.shape("down.gif")

def up():
	global player
	global direction
	global move
	if move:
		direction = "up"
		player.setheading(270)
		player.shape("up.gif")

def game_over():
	global ongoing
	global move
	move=False
	ongoing=False

	

def reset():
	global enemies
	global ongoing
	global points
	global scoreboard
	global move
	global cl
	global coords
	global cheats
	coord = []
	cl = False
	move=True
	ongoing=True
	points=0
	scoreboard.clear()
	scoreboard.write(points, font=("courier", 24, "normal"))

	for enem in enemies:
		enem.replace_enemies()

def EnableDisable_cheats():
	global cheats
	if cheats == True:
		cheats = False
	elif cheats == False:
		cheats = True


# Binds the keys to actual funcionts
wn.listen()
wn.onkeypress(up, "w")
wn.onkeypress(left, "a")
wn.onkeypress(right, "d")
wn.onkeypress(down, "s")

wn.onkeypress(up, "Up")
wn.onkeypress(left, "Left")
wn.onkeypress(right, "Right")
wn.onkeypress(down, "Down")

wn.onkeypress(reset, "q")
wn.onkeypress(EnableDisable_cheats, "space")



while True:
	wn.update()
	if ongoing==True:

		"""
		Create cheats, if you want to enable this change the cheats variable to True in the setup, or just press the cheats keybind (space)
		"""
		if cheats == True:
			for enem in enemies:
				distances.append(enem.distance(player))
			closest = min((abs(x), x) for x in distances)[1]
			x = distances.index(closest)
			closest = enemies[x]

			if closest.xcor() <= -1 and chosen==False:
				enemy_from = "left"
				chosen=True
			if closest.xcor() >= 1 and chosen==False:
				enemy_from = "right" 
				chosen=True
			if closest.ycor() <= 0 and chosen==False:
				enemy_from = "down"
				chosen=True
			if closest.ycor() >= 0 and chosen==False:
				enemy_from = "up"
				chosen=True

			if enemy_from == "left":
				left()
			if enemy_from == "right":
				right()
			if enemy_from == "up":
				up()
			if enemy_from == "down":
				down()
				

		for enem in enemies:
			enem.forward(enemyspeed) # Makes the enemy go forward. depending on your system you might want to raise this number or lower it. Is essentially just changes the enemy speed

			"""
			This checks if the player is looking in the direction of the enemy
			"""
			if enem.xcor() <= -1 and chosen==False:
				enemy_from = "left"
				chosen=True
			if enem.xcor() >= 1 and chosen==False:
				enemy_from = "right" 
				chosen=True
			if enem.ycor() <= 0 and chosen==False:
				enemy_from = "down"
				chosen=True
			if enem.ycor() >= 0 and chosen==False:
				enemy_from = "up"
				chosen=True

			"""
			Checks for colissions, If the player is looking at the enemy and there is a colission it'll add a point and replace the enemy,
			otherwise it'll stop the game
			"""
			if enem.distance(player) < 20 and enemy_from == direction:
				enem.replace_enemies()

				# Edits the board
				points+=1
				scoreboard.clear()
				scoreboard.write(points, font=("courier", 24, "normal"))
			elif enem.distance(player) < 20 and enemy_from != direction:
				game_over()
			chosen=False


		"""
		Finds the enemy closest to the player and changes it's colour to make the game easier
		(Sorry to all the colourblind people, I'm sure you're a great person :D)
		"""
		if cl == False:
			cl = True
			for enem in enemies:
				l = enem.distance(player) # Gets all the distances to the player and puts them in an array
				coords.append(l) 
			closest = min((abs(x), x) for x in coords)[1] # https://stackoverflow.com/questions/11923657/python-find-integer-closest-to-0-in-list (Gets the position closest to 0)
			for i in coords:
				if closest == i:
					position = coords.index(i) # Finds the position of the closest coordinate in the list to mach it up with the right enemy
			special = enemies[position] # Gets the position of the character closest to the player
			special.color("blue")
			coords = [] # Resets the array
		
		distances=[]










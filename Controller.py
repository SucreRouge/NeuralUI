# Briar Doty
# Oct 2013
# Controller.py
# Wires units together into 2d demo/game

from tkinter import *
from Unit import Unit

# on keypress change unit velocity
def keyPressed(event):
	canvas = event.widget.canvas
	
	if (event.keysym == "Up"):
		canvas.data["player"].accY(-1)
	elif (event.keysym == "Down"):
		canvas.data["player"].accY(1)
	elif (event.keysym == "Left"):
		canvas.data["player"].accX(-1)
	elif (event.keysym == "Right"):
		canvas.data["player"].accX(1)

# advances game state
def timerFired(canvas):
	moveUnit(canvas)
	delay = 50 # milliseconds
	canvas.after(delay, timerFired, canvas)
	
# erase and redraw unit in new position
def moveUnit(canvas):
	#canvas.data["player"].displayState()
	canvas.data["player"].advance()
	
	left = canvas.data["player"].x - 5
	right = canvas.data["player"].x + 5
	top = canvas.data["player"].y - 5
	bottom = canvas.data["player"].y + 5
	
	canvas.delete(ALL)
	canvas.create_oval(left, top, right, bottom, fill="red")
		
# initializes app
def init(canvas):
	canvas.data["player"] = Unit(100, 100, 0, 0, 720, 540)
	return

# main function initializes and launches app
def run():
	# create root and canvas
	root = Tk()
	canvas = Canvas(root, width=720, height=540)
	canvas.pack()
	
	# store canvas in root and itself
	root.canvas = canvas.canvas = canvas
	
	# set up data and initialize
	canvas.data = { }
	init(canvas)
	
	# bind keypress
	root.bind("<Key>", keyPressed)
	
	# fire timer
	timerFired(canvas)
	
	# run app
	root.mainloop()

# call main
run()


















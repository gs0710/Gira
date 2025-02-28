import turtle
import random

# Set up screen
win = turtle.Screen()
win.title("Bike Racing Game")
win.bgcolor("black")
win.setup(width=800, height=600)

# Draw the finish line
finish_line = turtle.Turtle()
finish_line.shape("square")
finish_line.color("white")
finish_line.shapesize(stretch_wid=30, stretch_len=0.5)
finish_line.penup()
finish_line.goto(350, 0)

# Player 1 bike
player1 = turtle.Turtle()
player1.shape("turtle")
player1.color("blue")
player1.penup()
player1.goto(-350, 100)

# Player 2 bike
player2 = turtle.Turtle()
player2.shape("turtle")
player2.color("red")
player2.penup()
player2.goto(-350, -100)

# Player 1 controls
def player1_up():
    y = player1.ycor()
    if y < 250:
        player1.sety(y + 20)

def player1_down():
    y = player1.ycor()
    if y > -250:
        player1.sety(y - 20)

# Player 2 controls
def player2_up():
    y = player2.ycor()
    if y < 250:
        player2.sety(y + 20)

def player2_down():
    y = player2.ycor()
    if y > -250:
        player2.sety(y - 20)

# Keyboard bindings
win.listen()
win.onkey(player1_up, "w")
win.onkey(player1_down, "s")
win.onkey(player2_up, "Up")
win.onkey(player2_down, "Down")

# Game loop
game_on = True
while game_on:
    # Move players forward
    player1.forward(random.randint(1, 5))
    player2.forward(random.randint(1, 5))

    # Check if Player 1 wins
    if player1.xcor() >= 350:
        print("Player 1 Wins!")
        game_on = False

    # Check if Player 2 wins
    if player2.xcor() >= 350:
        print("Player 2 Wins!")
        game_on = False

win.mainloop()

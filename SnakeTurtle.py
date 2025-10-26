import time
import random
import turtle

screen = turtle.Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("My snake game")
screen.tracer(0)

starting_position = [(0, 0), (-20, 0), (-40, 0)]
apple_position = (random.randint(-280, 280), random.randint(-280, 280))

class Snake():

    def __init__(self):
        self.segments = []
        self.create_snake()
        self.head = self.segments[0]

    def create_snake(self):
        for position in starting_position:
            new_segment = turtle.Turtle("square")
            new_segment.color("red")
            new_segment.penup()
            new_segment.goto(position)
            self.segments.append(new_segment)

    def move(self):
        for seg_num in range(len(self.segments) - 1, 0, -1):
            new_x = self.segments[seg_num - 1].xcor()
            new_y = self.segments[seg_num - 1].ycor()
            self.segments[seg_num].goto(new_x, new_y)
        self.head.forward(20)

    def up(self):
        if self.head.heading() != 270:
            self.head.setheading(90)

    def down(self):
        if self.head.heading() != 90:
            self.head.setheading(270)

    def left(self):
        if self.head.heading() != 0:
            self.head.setheading(180)

    def right(self):
        if self.head.heading() != 180:
            self.head.setheading(0)

    def grow(self):
        new_segment = turtle.Turtle("square")
        new_segment.color("red")
        new_segment.penup()
        self.segments.append(new_segment)

snake = Snake()

def spawn_apple():
    global apple_position
    apple_position = (random.randint(-280, 280), random.randint(-280, 280))

apple = turtle.Turtle("square")
apple.color("green")
apple.penup()
apple.goto(apple_position)

screen.listen()
screen.onkey(snake.up, "Up")
screen.onkey(snake.down, "Down")
screen.onkey(snake.left, "Left")
screen.onkey(snake.right, "Right")

game_on = True
while game_on:
    screen.update()
    time.sleep(0.1)
    snake.move()

    if snake.head.distance(apple) < 20:
        snake.grow()
        spawn_apple()
        apple.goto(apple_position)

    # Check boundaries
    if (
        snake.head.xcor() < -290 or snake.head.xcor() > 290 or
        snake.head.ycor() < -290 or snake.head.ycor() > 290
    ):
        game_on = False

    # Check collision with itself
    for segment in snake.segments[1:]:
        if snake.head.distance(segment) < 10:
            game_on = False

screen.bye()

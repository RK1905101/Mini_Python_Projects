import turtle
wn = turtle.Screen()
wn.bgcolor("Black")
turtle = turtle.Turtle()
turtle.speed(10)
turtle.penup()
turtle.shape("turtle")

def drawFillRectangle(x, y, length, width, color):
    turtle.goto(x,y)
    turtle.pendown()
    turtle.color(color)
    turtle.begin_fill()
    turtle.forward(width)
    turtle.right(90)
    turtle.forward(length)
    turtle.right(90)
    turtle.forward(width)
    turtle.right(90)
    turtle.forward(length)
    turtle.right(90)
    turtle.end_fill()
    turtle.penup()

def drawStar(x,y,color,length) :
    turtle.goto(x,y)
    turtle.setheading(0)
    turtle.pendown()
    turtle.begin_fill()
    turtle.color(color)
    for turn in range(0,5) :
        turtle.forward(length)
        turtle.right(144)
    turtle.end_fill()
    turtle.penup()

def drawCircle(x,y,color,radius) :
    turtle.goto(x,y)
    turtle.color(color)
    turtle.begin_fill()
    turtle.circle(radius)
    turtle.end_fill()

def drawMoon (x,y,color,radius):
    turtle.up()
    turtle.goto(x,y)
    turtle.color(color)
    turtle.begin_fill()
    turtle.circle(radius)
    turtle.end_fill()  

def drawGreen() :
    x = -230
    y = 125
    color = 'dark green'
    drawFillRectangle(x, y, 280, 460, color)

def drawWhite() :
    x = -230
    y =  125
    color = 'white'
    drawFillRectangle(x, y, 280, 130, color)

def Star() :
        x = 70
        y = 30
        color = 'white'
        drawStar(x, y, color, 50)
  
def Circle() :
           x = 45
           y = -100
           color = 'white'
           drawCircle(x, y, color, 80)

def Moon():
            x = 65
            y = -72
            color = 'dark green'
            drawMoon(x, y, color, 70)
             
drawGreen()
drawWhite()
Circle()
Moon()
Star()
turtle.goto(120,-200)
turtle.color('green')
turtle.write('PAKISTAN ZINDABAD !!!', font=('Arial', 15, 'normal'))
turtle.back(20)

wn.listen()
wn.mainloop()

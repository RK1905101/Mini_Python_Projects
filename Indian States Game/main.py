import turtle
import pandas as pd

t = turtle.Turtle()
s = turtle.Screen()

df = pd.read_csv("states.csv")

s.setup(height=650,width=600)
s.addshape('indiamap.gif')
t.shape('indiamap.gif')



state_list = df["states"].to_list()

entered_states = []

while len(entered_states) < 28:
    answer = s.textinput(title=f"{len(entered_states)}/28",prompt="Guess the states").title()

    if (answer == "exit".title()):
        break
    if answer in state_list:
        entered_states.append(answer)
        ttl = turtle.Turtle()
        ttl.hideturtle()
        ttl.penup()
        ttl.goto(x=int(df[df["states"] == answer].x),y=int(df[df["states"] == answer].y))
        ttl.write(answer)

missed_states = []
for i in state_list:
    if i not in entered_states:
        missed_states.append(i)

mdf = pd.Series(missed_states)
mdf.to_csv('missed_states.csv')

s.exitonclick()
'''

 ____  __ _   __   __ _  ____  _  _ 
/ ___)(  ( \ / _\ (  / )(  __)( \/ )
\___ \/    //    \ )  (  ) _)  )  / 
(____/\_)__)\_/\_/(__\_)(____)(__/  
        ___   __   _  _  ____       
       / __) / _\ ( \/ )(  __)      
      ( (_ \/    \/ \/ \ ) _)       
       \___/\_/\_/\_)(_/(____)      
       
This game is made as practice for doubly linked lists. The objective of the game is to 
collect orbs and grow the snake to be as large as possible. The game is lost by going out of 
bounds or doubling over another section of the snake.
'''

import dudraw
from random import random, randint

#class node which stores value, prev, and next of each node in doublylinkedlist
class Node:
    def __init__(self, value, prev=None, next=None):
        """I'm a function called __init__ that stores value, next, and prev of all nodes
        Parameters: value - value of the node
        prev - prev arrow from node
        next - next arrow from node
        Return: none"""

        #set all variables
        self.value = value
        self.prev = prev
        self.next = next

#class doublylinkedlist that allows you to do all needed actions with the nodes
class DoublyLinkedList:
    def __init__(self):
        """I'm a function called __init__ that stores header, trailer, and size
        Parameters: none
        Return: none"""

        #set header to a node with none for all val, prev, and next
        self.header = Node(None)
        #set header to a node with none for val and next, then prev set to header
        self.trailer = Node(None, self.header)
        #set header next to trailer
        self.header.next = self.trailer
        #set size to 0
        self.size = 0

    def add_first(self, value):
        """I'm a function called add_first that adds a node to the start of the doublylinkedlist
        Parameters: value - the value of the new node
        Return: none"""

        #set new node variable to be a node with value between header and current first node
        new_node = Node(value, self.header, self.header.next)
        #finish drawing the arrows from header and node on the other side to the new node
        new_node.prev.next = new_node
        new_node.next.prev = new_node
        #increase size by 1
        self.size += 1

    def add_last(self, value):
        """I'm a function called add_last that adds a node to the end of the doublylinkedlist
        Parameters: value - the value of the new node
        Return: none"""

        #set new node variable to be a node with value between trailer and current last node
        new_node = Node(value, self.trailer.prev, self.trailer)
        #finish drawing the arrows from trailer and node on the other side to the new node
        new_node.prev.next = new_node
        new_node.next.prev = new_node
        #increase size by 1
        self.size += 1

    def last(self):
        """I'm a function called last that returns the last node in the doublylinkedlist
        Parameters: none
        Return: last node in doublylinkedlist"""

        #if size is 0
        if self.size == 0:
            #raise an error
            raise IndexError("List is empty")
        #return last node in the doublylinkedlist
        return self.trailer.prev

    def first(self):
        """I'm a function called first that returns the first node in the doublylinkedlist
        Parameters: none
        Return: first node in doublylinkedlist"""

        #if size is 0
        if self.size == 0:
            #raise an error
            raise IndexError("List is empty")
        #return first node in the doublylinkedlist
        return self.header.next

    def get_size(self):
        """I'm a function called get_size that returns the size of the doublylinkedlist
        Parameters: none
        Return: size of doublylinkedlist"""

        #return the size of list
        return self.size

    def __str__(self):
        """I'm a function called __str__ that prints nodes to the terminal
        Parameters: none
        Return: values"""

        #if size is 0
        if self.size == 0:
            #return an empty list
            return '[]'
        #start return val with [
        return_val = '['
        #set cur to first node
        cur = self.header.next
        #while cur is not the trailer
        while cur is not self.trailer:
            #add val and space to return val
            return_val += str(cur.value) + ' '
            #set cur to next node
            cur = cur.next
        #return val set to everything minus last val
        return_val = return_val[:-1]
        #add ] to end of return val 
        return_val += ']'
        #return the completed return val
        return return_val

    def remove_between(self, node1, node2):
        """I'm a function called remove_between that removes a node between two other nodes
        Parameters: node1 - first node
        node2 - second node
        Return: value"""

        #if node1 is none or node2 is none
        if node1 == None or node2 == None:
            #raise an error
            raise ValueError("Node cannot be None")
        #value = value of the node after node1
        value = node1.next.value
        #draw arrows
        node1.next = node2
        node2.prev = node1
        #return value
        return value

    def remove_first(self):
        """I'm a function called remove_first that removes the first node
        Parameters: none
        Return: value"""

        #value = remove between first node function which returns value
        value = self.remove_between(self.header, self.header.next.next)
        #decrease size by 1
        self.size-=1
        #return value
        return value

    def remove_last(self):
        """I'm a function called remove_last that removes the last node
        Parameters: none
        Return: value"""

        #value = remove between last node function which returns value
        value = self.remove_between(self.trailer.prev.prev, self.trailer)
        #decrease size by 1
        self.size-=1
        #return value
        return value

    def is_empty(self):
        """I'm a function called is_empty that checks if doublylinkedlist is nothing
        Parameters: none
        Return: bool val"""

        #return bool of if size is 0
        return self.size == 0

    def search(self, value):
        """I'm a function called search that returns the index of a node
        Parameters: value - value of the node we are looking for
        Return: index of value"""

        #set curr to be first node
        curr = self.header.next
        #set index to 0
        index = 0
        #while curr is not trailer
        while curr != self.trailer:
            #if curr value is equal to the value
            if curr.value == value:
                #return the index
                return index
            #set curr to next node
            curr = curr.next
            #increase index by 1
            index += 1
        #return -1 if value was not found
        return -1


def apple(val):
    """I'm a function called apple that draws the apple on the canvas
    Parameters: val - the x and y of the apple
    Return: none"""

    #set pen color to red
    dudraw.set_pen_color(dudraw.RED)
    #draw apple at val x and y values of half width 0.4
    dudraw.filled_square(val[0], val[1], 0.4)
    #set pen color to dark green
    dudraw.set_pen_color(dudraw.DARK_GREEN)
    #draw apple stem at val x and y values of half width 0.1 and half height 0.2
    dudraw.filled_rectangle(val[0], val[1] + 0.5, 0.1, 0.2)

def eat_apple(val, num):
    """I'm a function called eat_apple that tests if snake ate the apple
    Parameters: val - the x and y of the apple
    num - the x and y of the snake head
    Return: bool value"""

    #if apple x and y values are the same as the snake head x and y values
    if num[0] == val[0] and num[1] == val[1]:
        #return True meaning the snake ate the apple
        return True
    #return False meaning the snake did not eat the apple
    return False

def self_intersects(d) -> bool:
    """I'm a function called self_intersects that checks if snake head is running into another part(node) of the snake
    Parameters: d - the doublylinkedlist
    Return: bool value"""

    #set head to be snake head or first node in doublylinkedlist
    head = d.header.next
    #set temp to be the next node in the doublylinkedlist
    temp = head.next
    #while temp is not the trailer
    while temp != d.trailer:
        #if head x and y values are the same as the body x and y values
        if head.value[0] == temp.value[0] and head.value[1] == temp.value[1]:
            #return False meaning to end the game loop
            return False
        #set temp to be next node in doublylinkedlist
        temp = temp.next
    #return True meaning to continue the game loop
    return True

def wall(x, y) -> bool:
    """I'm a function called wall that checks if snake head is running into the wall
    Parameters: x - the x value of the snake head currently
    y - the y value of the snake head currently
    Return: bool value"""

    #if snake hits edge of canvas for x values
    if x+0.5 >= 21 or x-0.5 <= -1:
        #return false meaning end the game loop
        return False
    #if snake hits edge of canvas for y values
    if y+0.5 >= 21 or y-0.5 <= -1:
        #return false meaning end the game loop
        return False
    #return true meaning continue the game loop
    return True

def clear_canvas():
    """I'm a function called clear_canvas that draws the checkerboard pattern seen in game
    Parameters: none
    Return: none"""

    #for loop i in range 20
    for i in range(0,20):
        #nested for loop z in range 20
        for z in range(0,20):
            #if i + z is even
            if (i+z) % 2 == 0:
                #set pen color to very light green
                dudraw.set_pen_color_rgb(144, 238, 144)
            else:
                #set pen color to light green
                dudraw.set_pen_color_rgb(124, 218, 124)
            #draw a filled square at location from i and z with hald width 0.5
            dudraw.filled_square(i+0.5, z+0.5, 0.5)


def main():
    """I'm snake game, a game that takes user input through w, a, s, d to control a snake on the screen.
    To grow the snake eat the apples that appear on the screen, if you run into the wall or another part of
    your snake then you lose
    Parameters: none
    Return: none"""

    #set canvas size to be 500 by 500
    dudraw.set_canvas_size(500,500)
    #set scale to be 0, 20 for x and y to make it easy to change movement
    dudraw.set_x_scale(0,20)
    dudraw.set_y_scale(0,20)
    #call clear_canvas to draw the checkerboard background
    clear_canvas()
    #set val to random x and y for inital placement of first apple
    val = [randint(0,19)+0.5, randint(0,19)+0.5]

    #create the doublylinkedlist set to d
    d=DoublyLinkedList()
    #create x and y for snake head node
    x = 9.5
    y = 9.5
    #add snake head node to d(doublylinkedlist)
    d.add_first((x,y))
    #for loop 2 iterations
    for i in range(2):
        #decrease y by 1
        y -= 1
        #add snake body node to d(doublylinkedlist)
        d.add_last((x, y))
    #reset x and y values for snake head node
    x = 9.5
    y = 9.5

    #set initial x_vel to 1 and y_vel to 0
    x_vel = 1
    y_vel = 0
    #create game varaible and set it to True
    game = True
    #set inital direction to 'd' or right movement
    number = 4

    #number of frames to allow to pass before snake moves
    limit = 5
    #a timer to keep track of number of frames that passed
    timer = 4
    #game loop tp coninue unless snake hits wall or the head of snake hits other part of snake
    while(game):
        #increment timer by one
        timer += 1
        #process keyboard press here
        key = dudraw.next_key_typed()
        #if key pressed was w
        if key == 'w':
            #change y_vel to 1 so snake moves upward
            y_vel = 1
            x_vel = 0
            #set number to 1
            number = 1
        #if key pressed was s
        elif key == 's':
            #change y_vel to -1 so snake moves downward
            y_vel = -1
            x_vel = 0
            #set number to 2
            number = 2
        #if key pressed was a
        elif key == 'a':
            #change x_vel to -1 so snake moves to the left
            y_vel = 0
            x_vel = -1
            #set number to 3
            number = 3
        #if key pressed was d
        elif key == 'd':
            #change x_vel to 1 so snake moves to the right
            y_vel = 0
            x_vel = 1
            #set number to 4
            number = 4
        #if timer reachs the limit
        if timer == limit:
            #reset timer to 0
            timer = 0
            #call the clear_canvas to re-draw the checker board background
            clear_canvas()
            #set temp to be the first element of the doublylinkedlist
            temp = d.header.next
            #while temp is not equal to the trailer
            while temp != d.trailer:
                #set pen color to black
                dudraw.set_pen_color(dudraw.BLACK)
                #draw a filled square at the values within each node in the doublylinked list with half width 0.45
                dudraw.filled_square(temp.value[0], temp.value[1], 0.45)
                #if temp is the first node and the 'w' was pressed last
                if temp == d.header.next and number == 1:
                    #set pen color to white
                    dudraw.set_pen_color(dudraw.WHITE)
                    #draw both eye balls on side snake is moving using the first nodes values 
                    dudraw.filled_circle(temp.value[0] - 0.25, temp.value[1] + 0.25, 0.15)
                    dudraw.filled_circle(temp.value[0] + 0.25, temp.value[1] + 0.25, 0.15)
                    #set pen color to red
                    dudraw.set_pen_color(dudraw.RED)
                    #draw a filled rectangle on side snake is moving using the first nodes values
                    dudraw.filled_rectangle(temp.value[0], temp.value[1] + 0.65, 0.1, 0.2)
                #if temp is the first node and the 's' was pressed last
                if temp == d.header.next and number == 2:
                    #set pen color to white
                    dudraw.set_pen_color(dudraw.WHITE)
                    #draw both eye balls on side snake is moving using the first nodes values 
                    dudraw.filled_circle(temp.value[0] - 0.25, temp.value[1] - 0.25, 0.15)
                    dudraw.filled_circle(temp.value[0] + 0.25, temp.value[1] - 0.25, 0.15)
                    #set pen color to red
                    dudraw.set_pen_color(dudraw.RED)
                    #draw a filled rectangle on side snake is moving using the first nodes values
                    dudraw.filled_rectangle(temp.value[0], temp.value[1] - 0.65, 0.1, 0.2)
                #if temp is the first node and the 'a' was pressed last
                if temp == d.header.next and number == 3:
                    #set pen color to white
                    dudraw.set_pen_color(dudraw.WHITE)
                    #draw both eye balls on side snake is moving using the first nodes values 
                    dudraw.filled_circle(temp.value[0] - 0.25, temp.value[1] - 0.25, 0.15)
                    dudraw.filled_circle(temp.value[0] - 0.25, temp.value[1] + 0.25, 0.15)
                    #set pen color to red
                    dudraw.set_pen_color(dudraw.RED)
                    #draw a filled rectangle on side snake is moving using the first nodes values
                    dudraw.filled_rectangle(temp.value[0] - 0.65, temp.value[1], 0.2, 0.1)
                #if temp is the first node and the 'd' was pressed last
                if temp == d.header.next and number == 4:
                    #set pen color to white
                    dudraw.set_pen_color(dudraw.WHITE)
                    #draw both eye balls on side snake is moving using the first nodes values 
                    dudraw.filled_circle(temp.value[0] + 0.25, temp.value[1] - 0.25, 0.15)
                    dudraw.filled_circle(temp.value[0] + 0.25, temp.value[1] + 0.25, 0.15)
                    #set pen color to red
                    dudraw.set_pen_color(dudraw.RED)
                    #draw a filled rectangle on side snake is moving using the first nodes values
                    dudraw.filled_rectangle(temp.value[0] + 0.65, temp.value[1], 0.2, 0.1)
                #move temp to be the next node in the doublylinkedlist
                temp = temp.next

            #set temp to be the last node in the doublylinkedlist
            temp = d.trailer.prev
            #while loop until temp equals header
            while temp != d.header:
                #set value of current node to be the value of node in front of it in the doublylinkedlist
                temp.value = temp.prev.value
                #set temp to be prev node in list
                temp = temp.prev
            
            #increase x and y using the x_vel and y_vel
            x += x_vel
            y += y_vel
            #update header value to new x and y values
            d.header.next.value = (x,y)

            #if the snake ate the apple
            if eat_apple(val, d.header.next.value):
                #add new snake part at the end of the doublylinkedlist with the value of the node in front of it
                d.add_last(d.trailer.prev.value)
                #choose new random apple location
                val = [randint(0,19)+0.5, randint(0,19)+0.5]
            #call apple function to draw the apple
            apple(val)

            #if snake doesn't self intersect and snake doesn't hit a well
            if self_intersects(d) and wall(x, y):
                #continue game loop
                game = True
            #if snake self intersects or hits a wall
            else:
                #end game loop
                game = False

        #draw canvas
        dudraw.show(20)

#call main function to start main code block
if __name__ == "__main__":
        main()

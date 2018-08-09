import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN, A_BOLD, A_UNDERLINE
from random import randint

print(KEY_UP, KEY_RIGHT, KEY_DOWN, KEY_LEFT)

# Initialize the screen
curses.initscr()
# Screen size
win = curses.newwin(50, 100, 5, 10)

#Bold lettering
win.attron(A_BOLD)

phrase = 'WELCOME TO SNAKE'
win.addstr( 15, 25, phrase )
win.attroff(A_BOLD)


win.keypad(1)
curses.noecho()
# Curser Visibility from range 0 - 2
curses.curs_set(0)
win.nodelay(1)


# Game starts with the snake starts going right
key = KEY_RIGHT
# Score starts at 0
score = 0
# Spaces "slithered" starts at 0
count = 0
# Starting position of the snake
snake = [[15,15],[0,0]]
# Establish the range for food to randomly appear
food = [randint(1, 49), randint(1, 99)]
# Add the food to the screen
win.addch(food[0], food[1], '@')

# Hit the esc key to quit...quitter
while key != 27:
    win.attron(A_BOLD)                                                              
    win.border(0)                             
    #Spaces Traveled
    win.addstr(0, 60, ' SNAKE SLITHER COUNT: ' + str(count) + ' ')
    #Score                                      
    win.addstr(0, 20, ' SCORE : ' + str(score) + ' ')
    win.attroff(A_BOLD)                                                       
    
    #Speed of the snake based on size
    speed = int(90 - (len(snake)/5 + len(snake)/10) % 120)
    # Makes the snake speed up so relative speed stays the same
    win.timeout(speed)
    count += 1 
    
    #Keep track of the previous key
    lastKey = key
    # Push a button, something happens...amazing
    event = win.getch()
    key = key if event == -1 else event                                             

    if key == ord(' '):
        key = -1

        # Pause control
        while key != ord(' '):
            key = win.getch() 
            curses.beep()

        key = lastKey
        continue

    # Makes other keys useless so people don't try to break the game
    if key not in [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN, 27]:
        key = lastKey

    # Snake movement: constantly popping the last item annd replacing the head with part of the body and placing the head at the front
    snake.insert(0, [snake[0][0] + (key == KEY_DOWN and 1) + (key == KEY_UP and -1), snake[0][1] + (key == KEY_LEFT and -1) + (key == KEY_RIGHT and 1)])

    # Don't run into the walls and you won't lose.
    if snake[0][0] == 0 or snake[0][0] == 49 or snake[0][1] == 0 or snake[0][1] == 99:
        curses.beep() 
        break

    # If the snake runs into itself, game over
    if snake[0] in snake[1:]:
        break

    # Snake head position is the same as food
    if snake[0] == food:
        food = []   
        #Score goes up, snake body grows
        score += 1
        while food == []: 
            #Randomly place food somewhere in the borders
            food = [randint(1, 48), randint(1, 98)]
            #Ensure the food goes in no space that the snake is occupying
            if food in snake:
                food = []
        #This is the food                                          
        win.addch(food[0], food[1], '@')
    else:    
        # snake.pop() pops the last [x,y]
        last = snake.pop() 
        # This is the animation essentially, replaces previously snake occupied space with a blank
        win.addch(last[0], last[1], ' ')
        
    # The snake points and slithers in the direction it is going    
    if key == KEY_UP:
        win.addch(snake[0][0], snake[0][1], '^')
        win.addch(snake[1][0], snake[1][1], '|') 
    if key == KEY_DOWN:
        win.addch(snake[0][0], snake[0][1], 'v')
        win.addch(snake[1][0], snake[1][1], '|')
    if key == KEY_LEFT:
        win.addch(snake[0][0], snake[0][1], '<') 
        win.addch(snake[1][0], snake[1][1], '-')
    if key == KEY_RIGHT:
        win.addch(snake[0][0], snake[0][1], '>')
        win.addch(snake[1][0], snake[1][1], '-')

#Terminate the window when the while loop is broken (when the game is lost)
curses.endwin()                          

print('Final Score: ' + str(score))                       
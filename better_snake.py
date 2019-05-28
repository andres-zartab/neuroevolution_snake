import curses
import random

stdscr = curses.initscr()
curses.curs_set(False)
height, width = (15, 40)
win = curses.newwin(height, width, 0, 0)
win.keypad(True)
win.border(0)
win.timeout(1000)

y_cor = height//4
x_cor = width//10

snake = [
    [y_cor, x_cor],
    [y_cor, x_cor-1],
    [y_cor, x_cor-2]
]

food = [height//4, width//2]

win.addch(food[0], food[1], curses.ACS_PI)

key = curses.KEY_RIGHT

orientation = 'right'
score = 0
x_to_food = 0
y_to_food = 0

while True:
    x_to_food = snake[0][1] - food[1]
    y_to_food = snake[0][0] - food[0]
    win.addstr(0, 2, 'SC : ' + str(score) + ' ')                # Printing 'Score' and
    win.addstr(0, 15, 'y: ' + str(y_to_food) + ' ')
    win.addstr(0, 22, 'x: ' + str(x_to_food) + ' ')
    win.addstr(0, 30, orientation + ' ')


    next_key = win.getch()
    key = key if next_key == -1 else next_key

    if snake[0][0] in [0, height - 1] or snake[0][1] in [0, width - 1] or snake[0] in snake[1:]:
        curses.endwin()
        quit()
    
    updated_head = [snake[0][0], snake[0][1]]

    if key == curses.KEY_DOWN:
        updated_head[0] += 1
        orientation = 'down'
    elif key == curses.KEY_UP:
        updated_head[0] -= 1
        orientation = 'up'
    elif key == curses.KEY_LEFT:
        updated_head[1] -= 1
        orientation = 'left'
    elif key == curses.KEY_RIGHT:
        updated_head[1] += 1
        orientation = 'right'


    snake.insert(0, updated_head)

    if snake[0] == food:
        score += 1
        food = None
        while food is None:
            food = [random.randint(1, height - 2),
                    random.randint(1, width - 2)]
            food = food if food not in snake else None
            win.addch(food[0], food[1], curses.ACS_PI)
    else:
        tail = snake.pop()
        win.addch(tail[0], tail[1], ' ')

    
    win.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD)

#curses.endwin()
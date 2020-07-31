import curses
import random
import numpy as np


np.set_printoptions(threshold=np.inf)
stdscr = curses.initscr()
curses.curs_set(False)
height, width = 16, 81
win = curses.newwin(height, width, 0, 0)
win.keypad(True)
win.border(0)
win.timeout(1000)

x_or = np.ones((height - 1, width - 1))
x_or = x_or * -1
x_or[1:-1, 1:-1] = 0

# f = open("dumps.txt", "w")

y_cor = height // 4
x_cor = width // 10

snake = [[y_cor, x_cor], [y_cor, x_cor - 1], [y_cor, x_cor - 2]]

food = [height // 4, width // 2]

win.addch(food[0], food[1], curses.ACS_PI)

key = curses.KEY_RIGHT
score = 0

n_run = 1
train_x = []
train_y = []

while True:

    if snake[0][0] in [0, height - 1] or snake[0][1] in [0, width - 1] or snake[0] in snake[1:]:
        train_x = np.asarray(train_x)
        np.save(f"train_x_{n_run}.npy", train_x)
        train_y = np.asarray(train_y)
        np.save(f"train_y_{n_run}.npy", train_y)
        # f.close()
        curses.endwin()
        quit()

    x = np.copy(x_or)
    for block in snake:
        x_pos = block[0]
        y_pos = block[1]
        x[x_pos, y_pos] = -1

    x_head = snake[0][0]
    y_head = snake[0][1]
    x[x_head, y_head] = 1

    x_food = food[0]
    y_food = food[1]
    x[x_food, y_food] = 1

    if key == curses.KEY_DOWN:
        verbose_key = 0
    elif key == curses.KEY_UP:
        verbose_key = 1
    elif key == curses.KEY_LEFT:
        verbose_key = 2
    elif key == curses.KEY_RIGHT:
        verbose_key = 3

    # f.write("NEW STEP\n\n")
    # f.write(f"KEY: {verbose_key}\n\n")
    # np.savetxt(f, x, fmt="%5d", delimiter=",")
    # np.savetxt(f, x)
    train_y.append(verbose_key)
    train_x.append(x)

    win.addstr(0, 2, "SC : " + str(snake[0][0]) + " ")  # Printing 'Score' and

    next_key = win.getch()
    key = key if next_key == -1 else next_key

    updated_head = [snake[0][0], snake[0][1]]

    if key == curses.KEY_DOWN:
        updated_head[0] += 1
        orientation = "down"
    elif key == curses.KEY_UP:
        updated_head[0] -= 1
        orientation = "up"
    elif key == curses.KEY_LEFT:
        updated_head[1] -= 1
        orientation = "left"
    elif key == curses.KEY_RIGHT:
        updated_head[1] += 1
        orientation = "right"

    snake.insert(0, updated_head)

    if snake[0] == food:
        score += 1
        food = None
        while food is None:
            food = [random.randint(1, height - 2), random.randint(1, width - 2)]
            food = food if food not in snake else None
        win.addch(food[0], food[1], curses.ACS_PI)
    else:
        tail = snake.pop()
        win.addch(tail[0], tail[1], " ")

    win.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD)

# curses.endwin()

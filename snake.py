import pygame

#game board
width = 600
height = 600
startposition = (200, 200)

#the snake
snake = []
snakewidth = 10
initiallength = 80
moving = (0, -1)  # (1,0) - right, (-1,0) - left, (0,1) - down, (0, -1) up
white = (255, 255, 255)
isalive = True


def drawgame(game):
    global width, height, snake
    game.fill((0, 0, 0))
    for x in snake:
        pygame.draw.line(game, white, x[0], x[1])
    pygame.display.update()


def initsnake():
    global snake, snakewidth, initiallength, moving, startposition
    for a in range(initiallength):
        x = startposition[0] + a * moving[0]
        y = startposition[1] + a * moving[1]
        snake.append(((x, y), (x + 10 * moving[1], y + 10 * moving[0])))


def movesnake():
    global snake
    snake.pop(0)
    length = len(snake)-1
    head = snake[length]
    tail = snake[length-1]
    x1 = head[0][0] + head[0][0] - tail[0][0]
    y1 = head[0][1] + (head[0][1] - tail[0][1])
    x2 = head[1][0] + (head[1][0] - tail[1][0])
    y2 = head[1][1] + (head[1][1] - tail[1][1])
    snake.append(((x1, y1), (x2, y2)))


def rotatesnake(direction):
    global snake, moving
    index = len(snake) - 1
    head = snake[index]
    if direction == -1:
        if moving == (0, -1):
            a = head[0][0] - snakewidth
            b = head[0][1] + snakewidth
            c = head[1][0]
            d = head[1][1]
            moving = (-1, 0)
        elif moving == (1, 0):
            a = head[0][0]
            b = head[0][1]
            c = head[1][0] - snakewidth
            d = head[1][1] - snakewidth
            moving = (0, -1)
        elif moving == (0, 1):
            a = head[0][0] + snakewidth
            b = head[0][1] - snakewidth
            c = head[1][0]
            d = head[1][1]
            moving = (1, 0)
        elif moving == (-1, 0):
            a = head[0][0]
            b = head[0][1]
            c = head[1][0] + snakewidth
            d = head[1][1] + snakewidth
            moving = (0, 1)
    elif direction == 1:
        print(moving)
        if moving == (0, -1):
            a = head[0][0]
            b = head[0][1]
            c = head[1][0] + snakewidth
            d = head[1][1] + snakewidth
            moving = (1, 0)
        elif moving == (1, 0):
            a = head[0][0] - snakewidth
            b = head[0][1] + snakewidth
            c = head[1][0]
            d = head[1][1]
            moving = (0, 1)
        elif moving == (0, 1):
            a = head[0][0]
            b = head[0][1]
            c = head[1][0] - snakewidth
            d = head[1][1] - snakewidth
            moving = (-1, 0)
        elif moving == (-1, 0):
            a = head[0][0] + snakewidth
            b = head[0][1] - snakewidth
            c = head[1][0]
            d = head[1][1]
            moving = (0, -1)

    snake[index] = ((a, b), (c, d))

    for x in range(1, snakewidth + 1):
        snake[index - x] = ((a - moving[0] * x, b - moving[1] * x), (c - moving[0] * x, d - moving[1] * x))


def readkey():
    global snake, moving
    rotate = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_KP4]:
            if moving[1] != 0:
                rotate = moving[1]

        elif keys[pygame.K_RIGHT] or keys[pygame.K_KP6]:
            if moving[1] != 0:
                rotate = - moving[1]

        elif keys[pygame.K_UP] or keys[pygame.K_KP8]:
            if moving[0] != 0:
                rotate = 0 - moving[0]

        elif keys[pygame.K_DOWN] or keys[pygame.K_KP2]:
            if moving[0] != 0:
                rotate = moving[0]

    return rotate



game = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
initsnake()
counter = 1
key = False
while isalive:
    clock.tick(10)  # Frames per second
    for x in range(snakewidth):
        drawgame(game)
        movesnake()
        pygame.time.delay(30)  #bremsen
        if not key:
            key = readkey()
            print(key)
        counter += 1
        if counter % snakewidth == 0 and key:
            rotatesnake(key)
            counter = 1
            key = False
pass


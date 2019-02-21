import pygame
import snake_model

#game board
width_fields = 30   # Anzahl Felder in der Breite
height_fields = 30  # Anzahl Felder in der Hoehe
field_size = 10     # Feldgröße

width = width_fields * field_size             # Breite in Pixel
height = height_fields * field_size + 20      # Hoehe in Pixel

pygame.init()
pygame.display.set_caption("Snake 1.0")
game = pygame.display.set_mode((width, height))


effect_gameover = pygame.mixer.Sound('game-over.wav')
effect_bite = pygame.mixer.Sound('eat.wav')

white = (255, 255, 255)
green = (0,255,0)
red = (255, 0, 0)
grey = (189, 195, 199)

# the snake
snakewidth = 10


def draw(game, snake,i):  # Bei jedem draw rückt die Schlange um 1 Pixel weiter (nur das erste und letzte Feld)
    game.fill((0, 0, 0))
    font = pygame.font.SysFont("lucidaconsole", 18)
    text = "Score: " + str(snake.Score)
    if snake.Gameover:
        text += '    GAME OVER'
        restart_panel = font.render("Press space to restart", True, red, grey)
        game.blit(restart_panel,(0,0))

        effect_gameover.play()

    text += '                                 '
    score_panel = font.render(text, True, red, grey )

    pygame.draw.rect(game, green, (snake.Food[1] * snakewidth, snake.Food[0] * snakewidth, snakewidth, snakewidth), 0)

    if (i==0) and snake.Eating:
        effect_bite.play()

    for j in range(len(snake.Snake)):
        field = snake.Snake[j]
        if j == 0:  # erstes Feld muss sich schrittweise nach vorne bewegen
            pygame.draw.rect(game, white, (field[1] * snakewidth - (snakewidth - i) * direction[1], field[0] * snakewidth - (snakewidth-i) * direction[0], snakewidth, snakewidth), 0)


        elif (j == len(snake.Snake)-1) and not snake.Eating:
            # letztes Feld muss schrittweise kürzer werden
            # (außer bei Eating, da wird die Schlange um 1 länger und das letzte Feld bleibt stehen)

            # Richtung in die sich das letzte Feld der Schlange bewegt
            dir = [snake.Snake[j-1][0] - snake.Snake[j][0], snake.Snake[j-1][1] - snake.Snake[j][1]]

            if dir[1] > 1:  # wenn die Schlange beim linken/rechten Rand rausgeht
                dir[1] = -1
            elif dir[1] < -1:
                dir[1] = 1

            if dir[0] > 1: # wenn die Schlange beim oberen/unteren Rand rausgeht
                dir[0] = -1
            elif dir[0] < -1:
                dir[0] = 1

            pygame.draw.rect(game, white, (field[1] * snakewidth + (i+1) * dir[1], field[0] * snakewidth + (i+1) * dir[0], snakewidth, snakewidth), 0)
        else:
            # alle anderen Felder werden als Quadrate gezeichnet
            pygame.draw.rect(game, white, (field[1]*snakewidth, field[0]*snakewidth, snakewidth, snakewidth), 0)

    game.blit(score_panel, (0, height-19))

    if snake.Gameover:
       # Den Kollisionspunkt rot zeichnen
       pygame.draw.rect(game, red,
                        (snake.Collision[1] * snakewidth, snake.Collision[0] * snakewidth, snakewidth, snakewidth), 0)

    pygame.display.update()


def readkey():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        keys = pygame.key.get_pressed()

        direction = None

        if keys[pygame.K_LEFT] or keys[pygame.K_KP4]:
             direction = (0, -1)
        elif keys[pygame.K_RIGHT] or keys[pygame.K_KP6]:
            direction = (0, 1)
        elif keys[pygame.K_UP] or keys[pygame.K_KP8]:
            direction = (-1, 0)
        elif keys[pygame.K_DOWN] or keys[pygame.K_KP2]:
            direction = (1, 0)

        return direction


def init_game():
    global model, wait_for_restart, direction

    model = snake_model.Snake(width_fields,height_fields, 10)
    direction = (0, -1)  # nach links
    wait_for_restart = False


init_game()
isalive = True
while isalive:
    if wait_for_restart:
        # Spiel beendet, warten auf Neustart
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            if keys[pygame.K_SPACE]:
                init_game()

        pygame.time.delay(10)
    else:
        new_direction = None
        for i in range(snakewidth):
            draw(game, model, i)
            pygame.time.delay(10)  # bremsen

            if (new_direction == direction) or (new_direction == None):
                new_direction = readkey()

        if (new_direction is not None) and not((new_direction[0] == -direction[0]) and (new_direction[1] == -direction[1])):
            direction = new_direction

        if not model.Gameover:
            model.move(direction)
        else:
            wait_for_restart = True



pass


from random import randrange

class Snake:
    def __init__(self, width, height, initial_length):
        self.__height = height
        self.__width = width

        self.Gameover = False
        self.Score = 0
        self.Snake = []
        self.Collision = None
        self.Eating = False

        self.__gameboard = [[False for j in range(width)] for i in range(height)]

        i = height // 2
        j = width // 2
        for _ in range(initial_length):
            j += 1
            self.Snake.append((i, j))
            self.__gameboard[i][j] = True

        self.__new_food()

    def __new_food(self):
        while True:
            i = randrange(0, self.__height)
            j = randrange(0, self.__width)
            if not self.__gameboard[i][j]:
                break;

        self.Food = (i, j)


    def move(self, direction):
        if self.Eating:
            self.__new_food()
            self.Eating = False
        else:
            tail = self.Snake[-1]
            self.__gameboard[tail[0]][tail[1]] = False
            self.Snake.pop()

        new_head = [self.Snake[0][0] + direction[0], self.Snake[0][1] + direction[1]]
        # wenn die Schlange beim Bildschirmrand rausgeht..
        if new_head[1] == self.__width:
            new_head[1] = 0
        elif new_head[1] == -1:
            new_head[1] = self.__width - 1

        if new_head[0] == self.__height:
            new_head[0] = 0
        elif new_head[0] == -1:
            new_head[0] = self.__height - 1


        if self.__gameboard[new_head[0]][new_head[1]]:
            # Kollision
            self.Gameover = True
            self.Collision = new_head
            self.Snake.insert(0, new_head)
        else:
            # beim Kopf ein Feld hinzufuegen
            self.Snake.insert(0, new_head)
            self.__gameboard[new_head[0]][new_head[1]] = True
            if (new_head[0] != self.Food[0]) or (new_head[1] != self.Food[1]):
                # Food nicht gefressen -> am Ende ein Feld loeschen
               # tail = self.Snake[-1]
                #self.__gameboard[tail[0]][tail[1]] = False
                #self.Snake.pop()
                self.Eating = False
            else:
                # Food gefressen
                self.Score += 1
                self.Eating = True

import random
import pygame
import pathFinder
import startingWindow


class Cube:
    def __init__(self, starting_position, cube_color, direction_x=1, direction_y=0):
        self.cube_position = starting_position
        self.direction_x = direction_x
        self.direction_y = direction_y  # "L", "R", "U", "D"
        self.cube_color = cube_color
        self.num_of_rows = num_of_rows
        self.playground_size = playground_size

    def move_cube(self, direction_x, direction_y):
        """"""
        self.direction_x = direction_x
        self.direction_y = direction_y
        self.cube_position = (self.cube_position[0] + self.direction_x, self.cube_position[1] + self.direction_y)

    def draw_cube(self, playground, eyes=False):
        cube_size = self.playground_size // self.num_of_rows
        cube_position_x = self.cube_position[0]
        cube_position_y = self.cube_position[1]

        pygame.draw.rect(playground, self.cube_color,
                         (cube_position_x * cube_size + 1, cube_position_y * cube_size + 1,
                          cube_size - 1, cube_size - 1))
        if eyes:
            centre = cube_size // 2
            radius = 3
            left_eye = (cube_position_x * cube_size + centre - radius, cube_position_y * cube_size + 8)
            right_eye = (cube_position_x * cube_size + cube_size - radius * 2, cube_position_y * cube_size + 8)
            pygame.draw.circle(playground, (0, 0, 0), left_eye, radius)
            pygame.draw.circle(playground, (0, 0, 0), right_eye, radius)


class Snake:
    body = []
    turns = {}

    def __init__(self, body_color, starting_position):
        self.body_color = body_color
        self.head = Cube(starting_position, self.body_color)
        self.body.append(self.head)
        self.direction_x = 0
        self.direction_y = 1

    def reset_snake(self, starting_position, additional_length=False, starting_length=0):
        self.body = []
        self.turns = {}
        self.head = Cube(starting_position, self.body_color)
        self.body.append(self.head)
        self.direction_x = 0
        self.direction_y = 1
        if additional_length:
            for i in range(starting_length):
                self.add_cube()
        else:
            self.add_cube()

    def add_cube(self):
        tail = self.body[-1]
        dx, dy = tail.direction_x, tail.direction_y

        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.cube_position[0] - 1, tail.cube_position[1]), self.body_color))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.cube_position[0] + 1, tail.cube_position[1]), self.body_color))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.cube_position[0], tail.cube_position[1] - 1), self.body_color))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.cube_position[0], tail.cube_position[1] + 1), self.body_color))

        self.body[-1].direction_x = dx
        self.body[-1].direction_y = dy

    def draw_body(self, playground):
        for ith_cube, cube_object in enumerate(self.body):
            if ith_cube == 0:
                cube_object.draw_cube(playground, True)
            else:
                cube_object.draw_cube(playground)


class ManualSnake(Snake):
    def __init__(self, body_color, starting_position):
        super().__init__(body_color, starting_position)

    def move_body(self):
        self.turn_head()

        for ith_cube, cube_object in enumerate(self.body):
            position = cube_object.cube_position[:]
            if position in self.turns:
                turn = self.turns[position]
                cube_object.move_cube(turn[0], turn[1])
                if ith_cube == len(self.body) - 1:
                    self.turns.pop(position)
            else:
                cube_object.move_cube(cube_object.direction_x, cube_object.direction_y)

    def turn_head(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.direction_x = -1
                    self.direction_y = 0
                    self.turns[self.head.cube_position[:]] = [self.direction_x, self.direction_y]
                elif keys[pygame.K_RIGHT]:
                    self.direction_x = 1
                    self.direction_y = 0
                    self.turns[self.head.cube_position[:]] = [self.direction_x, self.direction_y]
                elif keys[pygame.K_UP]:
                    self.direction_y = -1
                    self.direction_x = 0
                    self.turns[self.head.cube_position[:]] = [self.direction_x, self.direction_y]
                elif keys[pygame.K_DOWN]:
                    self.direction_y = 1
                    self.direction_x = 0
                    self.turns[self.head.cube_position[:]] = [self.direction_x, self.direction_y]
                elif keys[pygame.K_p]:
                    pathFinder.path_finder_draw_maze(num_of_rows, red_snake, purple_snake, snack)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            quit()


class AutomatedSnake(Snake):
    def __init__(self, body_color, starting_position):
        super().__init__(body_color, starting_position)

    def move_body(self, allow):
        if allow:
            self.turn_head()

            for ith_cube, cube_object in enumerate(self.body):
                position = cube_object.cube_position[:]
                if position in self.turns:
                    turn = self.turns[position]
                    cube_object.move_cube(turn[0], turn[1])
                    if ith_cube == len(self.body) - 1:
                        self.turns.pop(position)
                else:
                    cube_object.move_cube(cube_object.direction_x, cube_object.direction_y)

    def turn_head(self, next_move=None):
        check_head = purple_snake.body[0].cube_position
        try:
            next_move = pathFinder.path_finder(num_of_rows, red_snake, purple_snake, snack)
        except:
            pass

        if len(next_move) > 0:
            self.direction_x = next_move[0] - check_head[0]
            self.direction_y = next_move[1] - check_head[1]
            self.turns[self.head.cube_position[:]] = [self.direction_x, self.direction_y]
        else:
            pass


def random_snack_position(rows, snake_one, snake_two):
    snake_one_body = snake_one.body
    snake_two_body = snake_two.body

    while True:
        snack_position_x = random.randrange(1, rows - 1)
        snack_position_y = random.randrange(1, rows - 1)
        if len(list(filter(lambda body: body.cube_position == (snack_position_x, snack_position_y),
                           snake_one_body))) > 0 or len(list(
                filter(lambda body: body.cube_position == (snack_position_x, snack_position_y), snake_two_body))) > 0:
            continue
        else:
            break

    return snack_position_x, snack_position_y


def redraw_window(window):
    window.fill((0, 0, 0))
    red_snake.draw_body(window)
    purple_snake.draw_body(window)
    snack.draw_cube(window)
    pygame.display.update()
    pass


def victory_annoucment():
    print("\nYour score:", len(red_snake.body), "\nPurple snake score:", len(purple_snake.body), "\nYou WIN!")
    pathFinder.path_finder_draw_maze(num_of_rows, red_snake, purple_snake, snack)


def defeat_annoucment(starting_length):
    if len(red_snake.body) < len(purple_snake.body):
        result = "\nYou Lose!"
    elif len(red_snake.body) == len(purple_snake.body):
        result = "\nDraw!"
    print("\nYour score:", len(red_snake.body), "\nPurple snake score:", len(purple_snake.body), result)
    red_snake.reset_snake((15, 10))
    purple_snake.reset_snake((15, 20), True, starting_length)


def run_game():
    global playground_size, num_of_rows, red_snake, purple_snake, snack
    playground_size = 600
    num_of_rows = 30
    lvl = startingWindow.runCode()
    if lvl == 1:
        starting_length = 4
        tick = 8
    else:
        starting_length = 14
        tick = 10
    window = pygame.display.set_mode((playground_size, playground_size))
    red_snake = ManualSnake((255, 0, 0), (15, 10))
    red_snake.reset_snake((15, 10))
    purple_snake = AutomatedSnake((128, 0, 128), (15, 20))
    purple_snake.reset_snake((15, 20), True, starting_length)
    snack_position = random_snack_position(num_of_rows, red_snake, purple_snake)
    snack = Cube(snack_position, cube_color=(0, 255, 0))
    flag = True
    allow = True
    clock = pygame.time.Clock()
    pygame.time.wait(1000)

    while flag:
        pygame.time.delay(50)
        clock.tick(tick)
        purple_snake.move_body(allow)
        red_snake.move_body()
        if allow:
            allow = False
        else:
            allow = True

        if red_snake.body[0].cube_position == snack.cube_position:
            red_snake.add_cube()
            snack_position = random_snack_position(num_of_rows, red_snake, purple_snake)
            snack = Cube(snack_position, cube_color=(0, 255, 0))
        elif purple_snake.body[0].cube_position == snack.cube_position:
            purple_snake.add_cube()
            snack_position = random_snack_position(num_of_rows, red_snake, purple_snake)
            snack = Cube(snack_position, cube_color=(0, 255, 0))

        if len(red_snake.body) > len(purple_snake.body):
            victory_annoucment()

        head_pos = red_snake.head.cube_position
        purple_head_pos = purple_snake.head.cube_position

        # When red_snake go beyond playground
        if head_pos[0] >= num_of_rows or head_pos[0] < 0 or head_pos[1] >= num_of_rows or head_pos[1] < 0:
            defeat_annoucment(starting_length)

        # When purple_snake go beyond playground
        if purple_head_pos[0] >= num_of_rows or purple_head_pos[0] < 0 \
                or purple_head_pos[1] >= num_of_rows or purple_head_pos[1] < 0:
            victory_annoucment()

        for x in range(len(purple_snake.body)):
            if head_pos in list(map(lambda z: z.cube_position, purple_snake.body[x:])):
                defeat_annoucment(starting_length)
                break

        for x in range(len(red_snake.body)):
            if head_pos in list(map(lambda z: z.cube_position, red_snake.body[x + 1:])):
                defeat_annoucment(starting_length)
                break

        for x in range(len(purple_snake.body)):
            if purple_head_pos in list(map(lambda z: z.cube_position, purple_snake.body[x + 1:])):
                victory_annoucment()
                break

        try:
            redraw_window(window)
        except:
            print("Good Game!")
            flag = False


try:
    run_game()
except:
    print("Thank you for game!")


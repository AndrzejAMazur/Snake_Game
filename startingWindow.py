import pygame

pygame.init()

window = pygame.display.set_mode((600, 600))
window.fill((0, 0, 0))


class button():
    def __init__(self, color, x_coordinate, y_coordinate, width, height, text=''):
        self.color = color
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.width = width
        self.height = height
        self.text = text

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x_coordinate, self.y_coordinate, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0, 0, 0))
            window.blit(text, (self.x_coordinate + (self.width / 2 - text.get_width() / 2),
                               self.y_coordinate + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, mouse_position):
        if mouse_position[0] > self.x_coordinate and mouse_position[0] < self.x_coordinate + self.width:
            if mouse_position[1] > self.y_coordinate and mouse_position[1] < self.y_coordinate + self.height:
                return True

        return False


def redrawWindow(first_text_line, second_text_line, third_text_line, forth_text_line, EasyButton, HardButton):
    window.fill((0, 0, 0))

    window.blit(first_text_line, (300 - first_text_line.get_width() // 2, 140 - first_text_line.get_height() // 2))
    window.blit(second_text_line, (300 - second_text_line.get_width() // 2, 190 - second_text_line.get_height() // 2))
    window.blit(third_text_line, (300 - third_text_line.get_width() // 2, 240 - third_text_line.get_height() // 2))
    window.blit(forth_text_line, (207 - third_text_line.get_width() // 2, 290 - third_text_line.get_height() // 2))

    EasyButton.draw(window)
    HardButton.draw(window)


def runCode():
    run = True
    EasyButton = button((0, 255, 0), 50, 350, 200, 100, 'Easy')
    HardButton = button((0, 255, 0), 350, 350, 200, 100, 'Hard')

    font_normal = pygame.font.SysFont('comicsans', 35)
    first_text_line = font_normal.render("Purple Snake", True, (128, 0, 128))
    second_text_line = font_normal.render("Pick the snacks to become the longest snake.", True, (255, 255, 255))
    third_text_line = font_normal.render("Control by means of arrows.", True, (255, 255, 255))

    font_small = pygame.font.SysFont('comicsans', 25)
    forth_text_line = font_small.render("(After winning game the graph of path finding will be displayed)", True, (255, 255, 255))

    while run:
        redrawWindow(first_text_line, second_text_line, third_text_line, forth_text_line, EasyButton, HardButton)
        pygame.display.update()

        for event in pygame.event.get():
            mouse_position = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if EasyButton.isOver(mouse_position):
                    return 1

            if event.type == pygame.MOUSEMOTION:
                if EasyButton.isOver(mouse_position):
                    EasyButton.color = (255, 0, 0)
                else:
                    EasyButton.color = (0, 255, 0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if HardButton.isOver(mouse_position):
                    return 2

            if event.type == pygame.MOUSEMOTION:
                if HardButton.isOver(mouse_position):
                    HardButton.color = (255, 0, 0)
                else:
                    HardButton.color = (0, 255, 0)

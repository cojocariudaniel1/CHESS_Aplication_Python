import pygame as pg
import sprites

# Initialize the pygame
pg.init()

W = 800
H = 800
# Create the screen
screen = pg.display.set_mode((W, H))

# pygame.draw.line(screen, white, (375, 35), (375, 225), 1)
# circle = pygame.draw.line(screen, (116, 198, 249), (10, 10), (50, 10))
# Game Loop


# Rectangle (screen, color, x,y, width, height)
pg.font.init()  # you have to call this at the start,
# if you want to use this module.

my_font = pg.font.SysFont('Comic Sans MS', 75)
text_surface = my_font.render('R', False, (50, 50, 152))

color1 = (100, 50, 230)

chess_board_color = (195, 195, 213)

black_pion7 = sprites.ChessPieces(-17, "black_pion", screen)
black_pion1 = sprites.ChessPieces(-11, "black_pion", screen)
black_pion2 = sprites.ChessPieces(-12, "black_pion", screen)
black_pion3 = sprites.ChessPieces(-13, "black_pion", screen)
black_pion4 = sprites.ChessPieces(-14, "black_pion", screen)
black_pion5 = sprites.ChessPieces(-15, "black_pion", screen)
black_pion6 = sprites.ChessPieces(-16, "black_pion", screen)
black_pion8 = sprites.ChessPieces(-18, "black_pion", screen)
black_left_rock = sprites.ChessPieces(-50, "black_rock", screen)
black_right_rock = sprites.ChessPieces(-51, "black_rock", screen)
black_left_kning = sprites.ChessPieces(-30, "black_knight", screen)
black_right_kning = sprites.ChessPieces(-31, "black_knight", screen)
black_left_bishop = sprites.ChessPieces(-40, "black_bishop", screen)
black_right_bishop = sprites.ChessPieces(-41, "black_bishop", screen)
black_quen = sprites.ChessPieces(-9, "black_quen", screen)
black_quen2 = sprites.ChessPieces(-90, "black_quen", screen)

black_king = sprites.ChessPieces(-10, "black_king", screen)

sprites_black = [black_pion7, black_pion1, black_pion3, black_pion4, black_pion6, black_quen, black_pion8,
                 black_king, black_right_bishop,
                 black_left_bishop, black_left_kning, black_right_kning, black_pion2, black_pion5, black_left_rock,
                 black_right_rock]

white_left_kning = sprites.ChessPieces(30, "white_knight", screen)
white_right_kning = sprites.ChessPieces(31, "white_knight", screen)
white_quen = sprites.ChessPieces(9, "white_quen", screen)
white_king = sprites.ChessPieces(10, "white_king", screen)
white_left_bishop = sprites.ChessPieces(40, "white_bishop", screen)
white_right_bishop = sprites.ChessPieces(41, "white_bishop", screen)
white_left_rock = sprites.ChessPieces(50, "white_rock", screen)
white_right_rock = sprites.ChessPieces(51, "white_rock", screen)
white_pion1 = sprites.ChessPieces(11, "white_pion", screen)
white_pion2 = sprites.ChessPieces(12, "white_pion", screen)
white_pion3 = sprites.ChessPieces(13, "white_pion", screen)
white_pion4 = sprites.ChessPieces(14, "white_pion", screen)
white_pion5 = sprites.ChessPieces(15, "white_pion", screen)
white_pion6 = sprites.ChessPieces(16, "white_pion", screen)
white_pion7 = sprites.ChessPieces(17, "white_pion", screen)
white_pion8 = sprites.ChessPieces(18, "white_pion", screen)



sprites_white = [white_pion1, white_pion2, white_pion3, white_pion4, white_pion5, white_pion6, white_pion7, white_pion8,
                 white_left_rock, white_right_rock, white_left_kning, white_right_kning, white_left_bishop,
                 white_right_bishop, white_quen, white_king
                 ]


def draw_chess_board():
    x_pos = []
    for i in range(8):
        x_pos.append(i)
    y_pos = []
    for i in range(8):
        y_pos.append(i)

    for k in y_pos:
        index_k = y_pos.index(k)
        for j in x_pos:
            index_j = x_pos.index(j)
            if (index_k % 2) == 0:
                if (index_j % 2) != 0:
                    pg.draw.rect(screen, (73, 73, 105), (index_j * 100, index_k * 100, 100, 100))
                else:
                    pg.draw.rect(screen, (255, 255, 255), (index_j * 100, index_k * 100, 100, 100))
            else:
                if (index_j % 2) == 0:
                    pg.draw.rect(screen, (73, 73, 105), (index_j * 100, index_k * 100, 100, 100))
                else:
                    pg.draw.rect(screen, (255, 255, 255), (index_j * 100, index_k * 100, 100, 100))


def check_x_y(pos_sprite, x, y):
    # pos_sprite = (232,121)
    # x = 200
    # y = 300
    # 310 110
    try:
        x = x * 100
        y = y * 100
        if pos_sprite[0] in range(x, x + 100) and pos_sprite[1] in range(y, y + 100):
            return True
    except Exception as e:
        pass


def update_pieces():
    draw_chess_board()
    for k in sprites_white:
        k.update_pieces()
        k.moves.clear()
    for k in sprites_black:
        k.update_pieces()
        k.moves.clear()


def reset_moves():
    for i in sprites_white:
        i.moves.clear()
        i.sah_moves.clear()
    for i in sprites_black:
        i.moves.clear()
        i.sah_moves.clear()


def check_for_changes_in_matrix():
    matrix = sprites.initiate_matrix
    matrix_convert = []
    for k in matrix:
        for j in k:
            matrix_convert.append(j)

    for i in sprites_white:
        if i.id not in matrix_convert:
            index_sprite = sprites_white.index(i)
            sprites_white.pop(index_sprite)

    for i in sprites_black:
        if i.id not in matrix_convert:
            index_sprite = sprites_black.index(i)
            sprites_black.pop(index_sprite)


#
# def check_for_changes_in_matrix_black():
#     sprite_id = 0
#     matrix = sprites.initiate_matrix
#     for i in sprites_black:
#         for k in matrix:
#             if i.id not in k:
#                 sprite_id = i.id
#     if sprite_id != 0:
#         for i in sprites_black:
#             if sprite_id == i.id:
#
#                 sprites_white[i].remove()

class Game:
    def __init__(self):
        self.states = ('white', 'black')
        self.state = self.states[0]

    def white(self, state):
        if state == self.states[0]:
            while 1:
                event = pg.event.get()
                for ev in event:
                    pos = pg.mouse.get_pos()
                    if ev.type == pg.QUIT:
                        running = -1
                        return running
                    elif ev.type == pg.MOUSEBUTTONUP:
                        for s in sprites_white:
                            if check_x_y(pos, s.x_pos, s.y_pos):
                                for i in sprites_white:
                                    if i.id == s.id:
                                        # print('1')
                                        s.make_move = True
                                        s.pion_draw_rect()
                                        pg.display.update()
                                        return 1

    def black(self, state):
        pg.display.update()
        if state == self.states[1]:
            while 1:
                event = pg.event.get()
                for ev in event:
                    pos = pg.mouse.get_pos()
                    if ev.type == pg.QUIT:
                        running = -1
                        return running
                    elif ev.type == pg.MOUSEBUTTONUP:
                        for s in sprites_black:
                            if check_x_y(pos, s.x_pos, s.y_pos):
                                for i in sprites_black:
                                    if i.id == s.id:
                                        s.make_move = True
                                        s.pion_draw_rect()
                                        pg.display.update()
                                        return 2

    def second_move_white(self):
        # print('try second kmove')
        while 1:
            event = pg.event.get()
            pos = pg.mouse.get_pos()
            for ev in event:
                if ev.type == pg.MOUSEBUTTONUP:
                    if self.move_pieces_check(pos):
                        # print('tesdadadadat')
                        return True
                    else:
                        reset_moves()
                        update_pieces()
                        pg.display.update()
                        return False

    def second_move_black(self):
        while 1:
            event = pg.event.get()
            pos = pg.mouse.get_pos()
            for ev in event:
                if ev.type == pg.MOUSEBUTTONUP:
                    if self.move_pieces_check(pos):
                        return True
                    else:
                        reset_moves()
                        update_pieces()
                        pg.display.update()
                        return False

    def test(self):
        for i in sprites_black:
            if i.id in [-11, -12, -13, -14, -15, -16, -17, -18]:
                if i.y_pos == 7:
                    for y in sprites.initiate_matrix:
                        index_y = sprites.initiate_matrix.index(y)
                        for x in y:
                            index_x = y.index(x)
                            if i.id == x:
                                sprites.initiate_matrix[index_y][index_x] = -90
                                sprites_black.append(black_quen2)
                                print('try to make pion quen')

    def game_loop(self):

        running = True
        while running:
            self.test()
            draw_chess_board()
            update_pieces()
            pg.display.update()
            if self.state == self.states[0]:
                if self.white(self.state) == 1:
                    if self.second_move_white():
                        self.state = self.states[1]

                        check_for_changes_in_matrix()
                        update_pieces()
                        pg.display.update()
                    else:
                        self.state = self.states[0]
                        reset_moves()
                        update_pieces()
                        pg.display.update()

            if self.state == self.states[1]:
                if self.black(self.state) == 2:
                    if self.second_move_black():
                        self.state = self.states[0]
                        check_for_changes_in_matrix()
                        update_pieces()
                        pg.display.update()

                    else:
                        self.state = self.states[1]
                        reset_moves()
                        update_pieces()
                        pg.display.update()
            check_for_changes_in_matrix()
            pg.display.update()
            #     if self.second_move_black():
            #         self.state = self.states[0]

    def move_pieces_check(self, poss):
        if self.state == self.states[0]:
            for i in sprites_white:
                if i.make_move and not i.sah_bool:
                    for k in i.moves:
                        print('try to moves piece that is not in check')
                        index = 0
                        y = k[0] * 100
                        x = k[1] * 100
                        if index <= len(i.moves):
                            if poss[0] in range(x + 10, x + 90) and poss[1] in range(y + 10, y + 90):
                                i.move_pieces(k[0], k[1])
                                pg.display.update()
                                return True
                            else:
                                index += 1
                        else:
                            reset_moves()
                elif i.make_move and i.sah_bool:
                    print('try to move piece in check')
                    for k in i.sah_moves:
                        index = 0
                        y = k[0] * 100
                        x = k[1] * 100
                        if index <= len(i.sah_moves):
                            if poss[0] in range(x + 10, x + 90) and poss[1] in range(y + 10, y + 90):
                                i.move_pieces(k[0], k[1])
                                pg.display.update()
                                i.sah_count = 0
                                i.sah_bool = False
                                return True
                            else:
                                index += 1
                        else:
                            reset_moves()



                            # pg.draw.rect(screen, (32, 32, 70), (randint(x, x + 100), (randint(y, y + 100)), 22, 22))
        if self.state == self.states[1]:
            for i in sprites_black:
                if i.make_move:
                    for k in i.moves:
                        index = 0
                        y = k[0] * 100
                        x = k[1] * 100
                        if index <= len(i.moves):
                            if poss[0] in range(x + 10, x + 90) and poss[1] in range(y + 10, y + 90):
                                i.move_pieces(k[0], k[1])
                                pg.display.update()
                                return True
                            else:
                                index += 1
                        else:
                            reset_moves()
                            return False
                            # pg.draw.rect(screen, (32, 32, 70), (randint(x, x + 100), (randint(y, y + 100)), 22, 22))
        pg.time.delay(20)


g = Game()
g.game_loop()

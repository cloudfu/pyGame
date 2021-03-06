import pygame
from enum import Enum, unique

# region 棋盘相关设定

# 棋盘边距值（像素）
BROAD_MARGE_SPACE = 60
# 每个格子大小（像素）
CHESS_SIZE = 40
# 棋盘格子数量
CHESS_COUNT = 15
# 需要绘制棋盘的大小（像素）
BOARD_SIZE = CHESS_SIZE * (CHESS_COUNT - 1) + BROAD_MARGE_SPACE * 2
# 棋盘标题
BOARD_CAPTION = "五子棋"
# 棋盘划线颜色
BOARD_LINE_COLOR = pygame.Color(54, 40, 24)
# 棋盘背景色
BOARD_BACKGROUND = pygame.Color(216, 193, 168)

# endregion

# region 棋子相关设定

# 黑色棋子颜色
BLACK_CHESS_COLOR = (30, 30, 30)
# 白色棋子颜色
WHITE_CHESS_COLOR = (225, 225, 225)
# 白色棋子
WHITE_CHESS_CHAR = "○"
# 黑色棋子
BLACK_CHESS_CHAR = "●"
# 空棋子
EMPTY_CHESS_CHAR = "x"


# endregion

@unique
class chess_player(Enum):
    """
    当前棋盘状态
    """
    black_player = 10
    white_player = 20


class chess:
    """
    棋子对象
    """

    def __init__(self, player, x=-1, y=-1):
        self.player = player
        self.x = x
        self.y = y
        if self.player == chess_player.white_player:
            self.color = WHITE_CHESS_COLOR
        else:
            self.color = BLACK_CHESS_COLOR

    def set_position(self, x, y):
        """
        设置棋子在棋盘网格中的位置
        :param x:
        :param y:
        """
        self.x = x
        self.y = y

    def print(self):
        """
        落子对象打印
        """
        print(str(self.player) + " x：" + str(self.x) + " y:" + str(self.y))


class ui_board:
    """
    绘制五子棋盘
    """

    def __init__(self):
        # 设置棋盘大小
        self.screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))

        # 当前棋盘状态
        self.current_player = None
        self.next_player()

        # 当前棋盘已落子状态
        self.board_play_data = [[None for i in range(CHESS_COUNT)] for i in range(CHESS_COUNT)]

        # 已经落子历史记录
        self.played_chess_history = []

        # 棋盘刷新
        self.draw_board()

    def next_player(self):
        """
        更换下一位棋手
        :return:
        """

        # 执黑先行 & 白手 -> 黑手
        if self.current_player is None or self.current_player.player == chess_player.white_player:
            self.current_player = chess(chess_player.black_player)
        # 黑手 -> 白手
        elif self.current_player.player == chess_player.black_player:
            self.current_player = chess(chess_player.white_player)

        return self.current_player

    def is_empty_cell(self, x, y):
        """
        获得当前格子的状态
        """
        is_empty = True
        for cell in self.played_chess_history:
            if cell.x == x and cell.y == y:
                is_empty = False
                break
        return is_empty

    def print_board_play_data(self):
        """
        当前棋局落子数据打印
        """
        print("当前棋局情况：")
        for i in range(len(self.board_play_data)):
            for j in range(len(self.board_play_data[i])):
                if self.board_play_data[i][j] is None:
                    print(EMPTY_CHESS_CHAR, end='\t')
                elif isinstance(self.board_play_data[i][j], chess) and self.board_play_data[i][j].player == chess_player.black_player:
                    print(BLACK_CHESS_CHAR, end='\t')
                elif isinstance(self.board_play_data[i][j], chess) and self.board_play_data[i][j].player == chess_player.white_player:
                    print(WHITE_CHESS_CHAR, end='\t')

            print()

    def check_winner(self):
        """
        判断当前棋局是否获胜
        :return:
        """
        # 四个方向计数 横 竖 左斜 右斜
        # directions = [[(-1, 0), (1, 0)],
        #               [(0, -1), (0, 1)],
        #               [(-1, 1), (1, -1)],
        #               [(-1, -1), (1, 1)]]
        #
        # for axis in directions:
        #     axis_count = 1
        #     for (xdirection, ydirection) in axis:
        #         axis_count += self.count_on_direction(i, j, xdirection, ydirection, color)
        #         if axis_count >= 5:
        #             return True

        return False


    def draw_board(self):
        """
        绘制棋盘
        """
        while True:
            # 事件监听器
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONUP:
                    # 绘制棋子
                    self.calc_chess_position()

                    # 检测是否已经获胜
                    self.check_winner()

            # 绘制棋盘背景色
            self.screen.fill(BOARD_BACKGROUND)

            width = 0
            # 绘制棋盘X轴
            for x in range(0, CHESS_SIZE * CHESS_COUNT, CHESS_SIZE):
                if x == 0 or x == CHESS_SIZE * CHESS_COUNT - CHESS_SIZE:
                    width = 3
                else:
                    width = 1
                pygame.draw.line(self.screen, BOARD_LINE_COLOR, (x + BROAD_MARGE_SPACE, 0 + BROAD_MARGE_SPACE),
                                 (x + BROAD_MARGE_SPACE, CHESS_SIZE * (CHESS_COUNT - 1) + BROAD_MARGE_SPACE), width)

            # 绘制棋盘Y轴
            for y in range(0, CHESS_SIZE * CHESS_COUNT, CHESS_SIZE):
                if y == 0 or y == CHESS_SIZE * CHESS_COUNT - CHESS_SIZE:
                    width = 3
                else:
                    width = 1
                pygame.draw.line(self.screen, BOARD_LINE_COLOR, (0 + BROAD_MARGE_SPACE, y + BROAD_MARGE_SPACE),
                                 (CHESS_SIZE * (CHESS_COUNT - 1) + BROAD_MARGE_SPACE, y + BROAD_MARGE_SPACE), width)

            # 绘制4*4点
            x = 4
            y = 4
            pygame.draw.rect(self.screen, BOARD_LINE_COLOR, ((x * CHESS_SIZE + BROAD_MARGE_SPACE - 3, y * CHESS_SIZE + BROAD_MARGE_SPACE - 3), (8, 8)), 0)
            x = 10
            y = 4
            pygame.draw.rect(self.screen, BOARD_LINE_COLOR, ((x * CHESS_SIZE + BROAD_MARGE_SPACE - 3, y * CHESS_SIZE + BROAD_MARGE_SPACE - 3), (8, 8)), 0)
            x = 4
            y = 10
            pygame.draw.rect(self.screen, BOARD_LINE_COLOR, ((x * CHESS_SIZE + BROAD_MARGE_SPACE - 3, y * CHESS_SIZE + BROAD_MARGE_SPACE - 3), (8, 8)), 0)
            x = 10
            y = 10
            pygame.draw.rect(self.screen, BOARD_LINE_COLOR, ((x * CHESS_SIZE + BROAD_MARGE_SPACE - 3, y * CHESS_SIZE + BROAD_MARGE_SPACE - 3), (8, 8)), 0)

            # 绘制已经落子的棋子
            for chess_done in self.played_chess_history:
                if chess_done.player == chess_player.white_player:
                    pygame.draw.circle(self.screen, chess_done.color, [chess_done.x * CHESS_SIZE + BROAD_MARGE_SPACE,
                                                                       chess_done.y * CHESS_SIZE + BROAD_MARGE_SPACE],
                                       16, 16)
                else:
                    pygame.draw.circle(self.screen, chess_done.color, [chess_done.x * CHESS_SIZE + BROAD_MARGE_SPACE,
                                                                       chess_done.y * CHESS_SIZE + BROAD_MARGE_SPACE],
                                       16, 16)

            # Surface 刷新
            if event.type != pygame.QUIT:
                pygame.display.update()

    def calc_chess_position(self):
        """
        检查落子动作和计算落子位置
        """
        # 获取鼠标位置
        x, y = pygame.mouse.get_pos()

        # 获取当前棋子落位索引
        # 左边和上边的出界问题
        x_cell = int(round((x - BROAD_MARGE_SPACE) * 1.0 / CHESS_SIZE))
        y_cell = int(round((y - BROAD_MARGE_SPACE) * 1.0 / CHESS_SIZE))

        # 避免边界越界问题
        if 0 <= x_cell < CHESS_COUNT and 0 <= y_cell < CHESS_COUNT:
            # 确认落子无误，更换下一位玩家
            if self.make_chess_position(x_cell, y_cell):
                self.next_player()

    def make_chess_position(self, x_cell, y_cell):
        """
        进行棋子落子处理
        :param x_cell:
        :param y_cell:
        """
        result = False
        # 判断当前位置是否是可落子位置
        if self.is_empty_cell(x_cell, y_cell):
            self.current_player.set_position(x_cell, y_cell)

            # 更新当前玩家落子数据
            if self.current_player is not None:
                # 加入历史数据
                self.played_chess_history.append(self.current_player)

                # 加入棋谱数据
                # 二维数据第一维度是Y轴，第二维度是X轴
                # 打印是按照使用二维数组作为X轴进行打印，所以需要进行X、Y轴倒置处理
                self.board_play_data[self.current_player.y][self.current_player.x] = self.current_player

                # 当前棋局数据打印
                self.print_board_play_data()
                result = True

        return result


if __name__ == "__main__":
    ui_board()

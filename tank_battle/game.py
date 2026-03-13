"""坦克大战游戏主类"""
import pygame
import sys
from tank_battle.logger import get_logger
from tank_battle.constants import *
from tank_battle.states.menu_state import MenuState
from tank_battle.states.playing_state import PlayingState
from tank_battle.states.game_over_state import GameOverState


class TankBattleGame:
    """坦克大战游戏主类"""

    def __init__(self):
        """初始化游戏"""
        self.logger = get_logger("game")
        self.logger.info("初始化游戏...")

        # 初始化Pygame
        pygame.init()
        pygame.display.set_caption("坦克大战")
        pygame.key.set_repeat(100, 50)

        # 设置屏幕
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.clock = pygame.time.Clock()

        # 游戏状态
        self.current_state = None
        self.running = True
        self.score = 0
        self.lives = INITIAL_LIVES
        self.level = 1
        self.game_over = False
        self.game_won = False

        # 初始化状态
        self.change_state(MenuState)

        self.logger.info("游戏初始化完成")

    def change_state(self, state_class):
        """切换游戏状态"""
        self.logger.info(f"切换状态: {state_class.__name__}")
        self.current_state = state_class(self)

    def run(self):
        """游戏主循环"""
        self.logger.info("开始游戏主循环")

        while self.running:
            # 处理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.current_state.handle_event(event)

            # 更新
            self.current_state.update()

            # 绘制
            self.current_state.draw(self.screen)

            # 刷新显示
            pygame.display.flip()

            # 控制帧率
            self.clock.tick(FPS)

        self.logger.info("游戏主循环结束")

    def quit(self):
        """退出游戏"""
        self.running = False

    def reset_game(self):
        """重置游戏"""
        self.logger.info("重置游戏")
        self.score = 0
        self.lives = INITIAL_LIVES
        self.level = 1
        self.game_over = False
        self.game_won = False

    def next_level(self):
        """下一关"""
        self.logger.info(f"进入第 {self.level + 1} 关")
        self.level += 1

    def add_score(self, points: int):
        """加分"""
        self.score += points
        self.logger.debug(f"得分: +{points}, 总分: {self.score}")

    def lose_life(self):
        """失去生命"""
        self.lives -= 1
        self.logger.info(f"失去生命，剩余: {self.lives}")
        if self.lives <= 0:
            self.game_over = True
            self.change_state(GameOverState)

    def add_life(self):
        """增加生命"""
        self.lives += 1
        self.logger.info(f"获得生命，当前: {self.lives}")
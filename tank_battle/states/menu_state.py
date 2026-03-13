"""菜单状态"""
import pygame
from tank_battle.states.game_state import GameState
from tank_battle.constants import *
from tank_battle.logger import get_logger


class MenuState(GameState):
    """菜单状态"""

    def __init__(self, game):
        super().__init__(game)
        self.logger = get_logger("menu")
        self.logger.info("进入菜单")

        # 菜单选项
        self.menu_items = [
            ("开始游戏", self.start_game),
            ("操作说明", self.show_help),
            ("关于", self.show_about),
            ("退出", self.quit_game),
        ]
        self.selected_index = 0

        # 动画效果
        self.anim_timer = 0

    def start_game(self):
        """开始游戏"""
        self.logger.info("开始新游戏")
        self.game.reset_game()
        from tank_battle.states.playing_state import PlayingState
        self.game.change_state(PlayingState)

    def show_help(self):
        """显示操作说明"""
        self.logger.debug("显示操作说明")

    def show_about(self):
        """显示关于"""
        self.logger.debug("显示关于")

    def quit_game(self):
        """退出游戏"""
        self.logger.info("退出游戏")
        self.game.quit()

    def handle_event(self, event):
        """处理事件"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.menu_items)
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.menu_items)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self.menu_items[self.selected_index][1]()

    def update(self):
        """更新状态"""
        self.anim_timer += 1

    def draw(self, screen):
        """绘制菜单"""
        # 背景
        screen.fill(COLOR_DARK_BG)

        # 标题
        self._draw_title(screen)

        # 菜单选项
        self._draw_menu(screen)

        # 底部提示
        self._draw_hint(screen)

    def _draw_title(self, screen):
        """绘制标题"""
        font = pygame.font.SysFont(CHINESE_FONTS, FONT_SIZE_TITLE, bold=True)
        title = "坦克大战"

        # 闪烁效果
        if (self.anim_timer // 30) % 2 == 0:
            color = COLOR_GOLD
        else:
            color = COLOR_YELLOW

        text = font.render(title, True, color)
        rect = text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(text, rect)

    def _draw_menu(self, screen):
        """绘制菜单选项"""
        font = pygame.font.SysFont(CHINESE_FONTS, FONT_SIZE_MEDIUM)

        start_y = 280
        spacing = 50

        for i, (text, _) in enumerate(self.menu_items):
            # 选中状态
            if i == self.selected_index:
                color = COLOR_GOLD
                prefix = "▶ "
            else:
                color = COLOR_WHITE
                prefix = "  "

            # 绘制选项
            item_text = font.render(prefix + text, True, color)
            rect = item_text.get_rect(center=(SCREEN_WIDTH // 2, start_y + i * spacing))
            screen.blit(item_text, rect)

    def _draw_hint(self, screen):
        """绘制底部提示"""
        font = pygame.font.SysFont(CHINESE_FONTS, FONT_SIZE_SMALL)
        hint = "使用 ↑↓ 选择，Enter 确认"

        text = font.render(hint, True, COLOR_GREEN)
        rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        screen.blit(text, rect)
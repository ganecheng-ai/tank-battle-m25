"""游戏结束状态"""
import pygame
from tank_battle.states.game_state import GameState
from tank_battle.constants import *
from tank_battle.logger import get_logger


class GameOverState(GameState):
    """游戏结束状态"""

    def __init__(self, game):
        super().__init__(game)
        self.logger = get_logger("game_over")
        self.logger.info("进入游戏结束")

        self.selected_index = 0
        self.menu_items = [
            ("重新开始", self.restart),
            ("返回菜单", self.to_menu),
            ("退出游戏", self.quit),
        ]

        # 动画
        self.anim_timer = 0

    def restart(self):
        """重新开始"""
        self.logger.info("重新开始游戏")
        self.game.reset_game()
        from tank_battle.states.playing_state import PlayingState
        self.game.change_state(PlayingState)

    def to_menu(self):
        """返回菜单"""
        self.logger.info("返回菜单")
        from tank_battle.states.menu_state import MenuState
        self.game.change_state(MenuState)

    def quit(self):
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
        """绘制游戏结束画面"""
        # 半透明遮罩
        s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        s.set_alpha(128)
        s.fill(COLOR_BLACK)
        screen.blit(s, (0, 0))

        # 标题
        font = pygame.font.SysFont(CHINESE_FONTS, FONT_SIZE_TITLE, bold=True)

        if self.game.game_won:
            title = "游戏胜利!"
            color = COLOR_GOLD
        else:
            title = "游戏结束"
            color = COLOR_RED

        if (self.anim_timer // 20) % 2 == 0:
            text = font.render(title, True, color)
        else:
            text = font.render(title, True, COLOR_WHITE)

        rect = text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        screen.blit(text, rect)

        # 显示分数
        score_font = pygame.font.SysFont(CHINESE_FONTS, FONT_SIZE_LARGE)
        score_text = score_font.render(f"最终得分: {self.game.score}", True, COLOR_WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 280))
        screen.blit(score_text, score_rect)

        # 菜单选项
        menu_font = pygame.font.SysFont(CHINESE_FONTS, FONT_SIZE_MEDIUM)
        start_y = 360
        spacing = 50

        for i, (text, _) in enumerate(self.menu_items):
            if i == self.selected_index:
                color = COLOR_GOLD
                prefix = "▶ "
            else:
                color = COLOR_WHITE
                prefix = "  "

            item_text = menu_font.render(prefix + text, True, color)
            rect = item_text.get_rect(center=(SCREEN_WIDTH // 2, start_y + i * spacing))
            screen.blit(item_text, rect)

        # 提示
        hint_font = pygame.font.SysFont(CHINESE_FONTS, FONT_SIZE_SMALL)
        hint = hint_font.render("使用 ↑↓ 选择，Enter 确认", True, COLOR_GREEN)
        hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        screen.blit(hint, hint_rect)
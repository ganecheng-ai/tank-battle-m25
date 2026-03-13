"""游戏状态基类"""
from abc import ABC, abstractmethod


class GameState(ABC):
    """游戏状态基类"""

    def __init__(self, game):
        """
        初始化状态

        Args:
            game: 游戏主实例
        """
        self.game = game

    @abstractmethod
    def handle_event(self, event):
        """处理事件"""
        pass

    @abstractmethod
    def update(self):
        """更新状态"""
        pass

    @abstractmethod
    def draw(self, screen):
        """绘制状态"""
        pass
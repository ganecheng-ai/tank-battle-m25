"""爆炸效果类"""
import pygame
from tank_battle.constants import *
from tank_battle.logger import get_logger


class Explosion(pygame.sprite.Sprite):
    """爆炸效果类"""

    def __init__(self, x: int, y: int, size: str = "normal"):
        super().__init__()
        self.logger = get_logger("explosion")

        # 位置和大小
        self.x = x
        self.y = y

        # 根据类型设置大小
        if size == "small":
            self.width = 20
            self.height = 20
            self.max_frames = 10
        elif size == "large":
            self.width = 60
            self.height = 60
            self.max_frames = 20
        else:  # normal
            self.width = 40
            self.height = 40
            self.max_frames = 15

        # 动画
        self.frame = 0
        self.alive_flag = True

        # 创建图像
        self.image = self._create_explosion_frame()
        self.rect = self.image.get_rect()
        self.rect.center = (x + self.width // 2, y + self.height // 2)

    def _create_explosion_frame(self) -> pygame.Surface:
        """创建爆炸帧"""
        image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # 爆炸颜色渐变 - 从中心向外
        center = (self.width // 2, self.height // 2)
        radius = self.width // 2

        # 外层 - 橙色
        pygame.draw.circle(image, (255, 140, 0, 200), center, radius)

        # 中层 - 黄色
        pygame.draw.circle(image, (255, 200, 0, 220), center, int(radius * 0.7))

        # 核心 - 白色
        pygame.draw.circle(image, (255, 255, 255, 255), center, int(radius * 0.3))

        # 添加一些火花效果
        import random
        for _ in range(5):
            angle = random.uniform(0, 3.14159 * 2)
            dist = random.uniform(radius * 0.3, radius * 0.9)
            sx = center[0] + int(dist * (1 if random.random() > 0.5 else -1) * abs(pygame.math.Vector2(1, 0).rotate_rad(angle).x))
            sy = center[1] + int(dist * abs(pygame.math.Vector2(1, 0).rotate_rad(angle).y))
            pygame.draw.circle(image, (255, 255, 200), (sx, sy), 2)

        return image

    def update(self):
        """更新动画"""
        self.frame += 1

        # 更新透明度实现淡出效果
        alpha = 255 - int(255 * (self.frame / self.max_frames))
        self.image.set_alpha(max(0, alpha))

        if self.frame >= self.max_frames:
            self.kill()

    def kill(self):
        """移除爆炸"""
        self.alive_flag = False

    def alive(self) -> bool:
        """是否存活"""
        return self.alive_flag

    def draw(self, screen):
        """绘制"""
        if self.alive_flag:
            screen.blit(self.image, self.rect)


class ExplosionManager:
    """爆炸效果管理器"""

    def __init__(self):
        self.logger = get_logger("explosion_manager")
        self.explosions = []

    def add_explosion(self, x: int, y: int, size: str = "normal"):
        """添加爆炸效果"""
        explosion = Explosion(x, y, size)
        self.explosions.append(explosion)
        self.logger.info(f"添加爆炸效果: ({x}, {y})")

    def update(self):
        """更新所有爆炸效果"""
        for explosion in self.explosions[:]:
            explosion.update()
            if not explosion.alive():
                self.explosions.remove(explosion)

    def get_explosions(self):
        """获取所有爆炸效果"""
        return self.explosions

    def clear(self):
        """清除所有爆炸效果"""
        self.explosions.clear()
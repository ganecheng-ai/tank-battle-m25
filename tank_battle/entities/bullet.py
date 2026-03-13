"""子弹类"""
import pygame
from tank_battle.constants import *


class Bullet(pygame.sprite.Sprite):
    """子弹类"""

    def __init__(self, x: int, y: int, direction: int, speed: int, owner: str):
        super().__init__()

        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed
        self.owner = owner  # "player" 或 "enemy"
        self.damage = BULLET_DAMAGE
        self.alive_flag = True

        # 尺寸
        self.width = BULLET_WIDTH
        self.height = BULLET_HEIGHT

        # 图像
        self.image = self._create_image()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def _create_image(self) -> pygame.Surface:
        """创建子弹图像"""
        image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        if self.owner == "player":
            # 玩家子弹 - 黄色
            color = COLOR_YELLOW
        else:
            # 敌方子弹 - 红色
            color = COLOR_RED

        # 绘制圆形子弹
        pygame.draw.circle(image, color, (self.width // 2, self.height // 2), self.width // 2)

        return image

    def update(self):
        """更新子弹"""
        if not self.alive_flag:
            return

        # 移动
        dx, dy = 0, 0
        if self.direction == DIRECTION_UP:
            dy = -self.speed
        elif self.direction == DIRECTION_RIGHT:
            dx = self.speed
        elif self.direction == DIRECTION_DOWN:
            dy = self.speed
        elif self.direction == DIRECTION_LEFT:
            dx = -self.speed

        self.x += dx
        self.y += dy
        self.rect.topleft = (self.x, self.y)

        # 检查是否出界
        if self._is_out_of_bounds():
            self.kill()

    def _is_out_of_bounds(self) -> bool:
        """检查是否出界"""
        return (self.x < GAME_AREA_OFFSET_X or
                self.x > GAME_AREA_OFFSET_X + GAME_AREA_WIDTH or
                self.y < GAME_AREA_OFFSET_Y or
                self.y > GAME_AREA_OFFSET_Y + GAME_AREA_HEIGHT)

    def kill(self):
        """销毁子弹"""
        self.alive_flag = False

    def alive(self) -> bool:
        """是否存活"""
        return self.alive_flag

    def draw(self, screen):
        """绘制"""
        if self.alive_flag:
            screen.blit(self.image, self.rect)
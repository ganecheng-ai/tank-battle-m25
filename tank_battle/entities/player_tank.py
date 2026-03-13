"""玩家坦克"""
import pygame
from tank_battle.entities.tank import Tank
from tank_battle.constants import *


class PlayerTank(Tank):
    """玩家坦克"""

    def __init__(self, x: int, y: int):
        # 玩家颜色必须在调用父类__init__之前设置，因为父类会调用_create_tank_image()
        self.color = (50, 150, 200)  # 蓝色
        super().__init__(x, y, DIRECTION_UP)
        self.owner = "player"
        self.speed = PLAYER_SPEED
        self.fire_speed = PLAYER_BULLET_SPEED

        # 火力等级
        self.power_level = 1

        # 按键状态
        self.keys = {
            pygame.K_UP: False,
            pygame.K_DOWN: False,
            pygame.K_LEFT: False,
            pygame.K_RIGHT: False,
        }

    def _create_tank_image(self) -> pygame.Surface:
        """创建玩家坦克图像"""
        image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # 履带
        pygame.draw.rect(image, (60, 80, 30), (2, 0, 6, self.height))
        pygame.draw.rect(image, (60, 80, 30), (self.width - 8, 0, 6, self.height))

        # 主体 - 蓝色
        pygame.draw.rect(image, self.color, (6, 4, self.width - 12, self.height - 8))

        # 炮塔
        turret_color = (40, 120, 160)
        pygame.draw.circle(image, turret_color, (self.width // 2, self.height // 2), 8)

        # 炮管
        self._draw_turret(image, self.direction)

        return image

    def handle_event(self, event):
        """处理输入事件"""
        if event.type == pygame.KEYDOWN:
            if event.key in self.keys:
                self.keys[event.key] = True
            elif event.key == pygame.K_SPACE:
                self.fire()
        elif event.type == pygame.KEYUP:
            if event.key in self.keys:
                self.keys[event.key] = False

    def update(self):
        """更新玩家坦克"""
        super().update()

        if not self.alive_flag:
            return

        # 处理移动
        dx = 0
        dy = 0

        if self.keys[pygame.K_UP]:
            dy = -self.speed
        elif self.keys[pygame.K_DOWN]:
            dy = self.speed
        elif self.keys[pygame.K_LEFT]:
            dx = -self.speed
        elif self.keys[pygame.K_RIGHT]:
            dx = self.speed

        self.move(dx, dy)

    def upgrade_power(self):
        """升级火力"""
        if self.power_level < 3:
            self.power_level += 1
            self.fire_rate = max(10, PLAYER_FIRE_COOLDOWN - self.power_level * 5)
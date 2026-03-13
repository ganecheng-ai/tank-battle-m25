"""敌方坦克"""
import pygame
import random
from tank_battle.entities.tank import Tank
from tank_battle.constants import *


class EnemyTank(Tank):
    """敌方坦克"""

    def __init__(self, x: int, y: int):
        # 随机方向
        direction = random.choice([DIRECTION_UP, DIRECTION_RIGHT, DIRECTION_DOWN, DIRECTION_LEFT])
        super().__init__(x, y, direction)

        self.owner = "enemy"

        # 随机速度
        self.speed = random.uniform(ENEMY_SPEED_MIN, ENEMY_SPEED_MAX)
        self.fire_speed = ENEMY_BULLET_SPEED

        # AI状态
        self.ai_state = "move"  # move, change_direction, fire
        self.ai_timer = 0
        self.ai_change_interval = random.randint(60, 180)

        # 坦克类型 (影响颜色)
        self.enemy_type = random.choice(["normal", "fast", "heavy"])

        if self.enemy_type == "fast":
            self.speed = 2.5
            self.color = (200, 200, 50)  # 黄色
        elif self.enemy_type == "heavy":
            self.speed = 1
            self.health = 2
            self.max_health = 2
            self.color = (150, 50, 50)  # 红色
        else:
            self.color = (150, 100, 50)  # 棕色

        self.update_image()

    def _create_tank_image(self) -> pygame.Surface:
        """创建敌方坦克图像"""
        image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # 履带
        pygame.draw.rect(image, (60, 80, 30), (2, 0, 6, self.height))
        pygame.draw.rect(image, (60, 80, 30), (self.width - 8, 0, 6, self.height))

        # 主体 - 根据类型着色
        pygame.draw.rect(image, self.color, (6, 4, self.width - 12, self.height - 8))

        # 炮塔
        turret_color = tuple(max(0, c - 30) for c in self.color)
        pygame.draw.circle(image, turret_color, (self.width // 2, self.height // 2), 8)

        # 炮管
        self._draw_turret(image, self.direction)

        return image

    def update(self):
        """更新敌方坦克"""
        super().update()

        if not self.alive_flag:
            return

        # AI逻辑
        self._ai_update()

    def _ai_update(self):
        """AI更新"""
        self.ai_timer += 1

        if self.ai_state == "move":
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

            self.move(dx, dy)

            # 随机改变方向
            if self.ai_timer >= self.ai_change_interval:
                self.ai_timer = 0
                self.ai_change_interval = random.randint(60, 180)

                # 30%概率改变方向
                if random.random() < 0.3:
                    self.direction = random.choice([DIRECTION_UP, DIRECTION_RIGHT, DIRECTION_DOWN, DIRECTION_LEFT])
                    self.update_image()

                # 20%概率射击
                if random.random() < 0.2:
                    self.fire()

        # 检测是否撞墙，如果是则改变方向
        # (通过移动检测)

    def fire(self):
        """敌方射击"""
        if self.fire_cooldown > 0:
            return

        if self.bullets is None:
            return

        # 简单AI：有一定概率不射击
        if random.random() > 0.7:
            return

        from tank_battle.entities.bullet import Bullet

        # 子弹起始位置
        if self.direction == DIRECTION_UP:
            bx = self.x + self.width // 2 - BULLET_WIDTH // 2
            by = self.y - BULLET_HEIGHT
        elif self.direction == DIRECTION_RIGHT:
            bx = self.x + self.width
            by = self.y + self.height // 2 - BULLET_HEIGHT // 2
        elif self.direction == DIRECTION_DOWN:
            bx = self.x + self.width // 2 - BULLET_WIDTH // 2
            by = self.y + self.height
        else:
            bx = self.x - BULLET_WIDTH
            by = self.y + self.height // 2 - BULLET_HEIGHT // 2

        bullet = Bullet(bx, by, self.direction, self.fire_speed, self.owner)
        self.bullets.append(bullet)
        self.fire_cooldown = self.fire_rate + random.randint(-10, 10)
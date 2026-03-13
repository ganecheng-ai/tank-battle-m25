"""坦克基类"""
import pygame
from tank_battle.constants import *
from tank_battle.logger import get_logger


class Tank(pygame.sprite.Sprite):
    """坦克基类"""

    def __init__(self, x: int, y: int, direction: int = DIRECTION_UP):
        super().__init__()
        self.logger = get_logger("tank")

        # 位置和方向
        self.x = x
        self.y = y
        self.direction = direction

        # 速度
        self.speed = PLAYER_SPEED

        # 状态
        self.alive_flag = True
        self.health = 1
        self.max_health = 1
        self.invincible = False
        self.invincible_timer = 0

        # 射击
        self.fire_cooldown = 0
        self.fire_rate = PLAYER_FIRE_COOLDOWN

        # 子弹列表 (引用)
        self.bullets = None
        self.enemies = None

        # 地图引用
        self.game_map = None

        # 尺寸
        self.width = TANK_WIDTH
        self.height = TANK_HEIGHT

        # 创建精灵图像
        self.original_image = self._create_tank_image()
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def _create_tank_image(self) -> pygame.Surface:
        """创建坦克图像"""
        image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # 坦克身体 (使用几何图形绘制)
        body_color = (100, 150, 50)  # 军绿色

        # 履带
        pygame.draw.rect(image, (60, 80, 30), (2, 0, 6, self.height))
        pygame.draw.rect(image, (60, 80, 30), (self.width - 8, 0, 6, self.height))

        # 主体
        pygame.draw.rect(image, body_color, (6, 4, self.width - 12, self.height - 8))

        # 炮塔
        turret_color = (80, 120, 40)
        pygame.draw.circle(image, turret_color, (self.width // 2, self.height // 2), 8)

        # 炮管
        self._draw_turret(image, self.direction)

        return image

    def _draw_turret(self, image: pygame.Surface, direction: int):
        """绘制炮管"""
        turret_color = (70, 100, 30)
        center = (self.width // 2, self.height // 2)

        if direction == DIRECTION_UP:
            pygame.draw.line(image, turret_color, center, (self.width // 2, 2), 4)
        elif direction == DIRECTION_RIGHT:
            pygame.draw.line(image, turret_color, center, (self.width - 2, self.height // 2), 4)
        elif direction == DIRECTION_DOWN:
            pygame.draw.line(image, turret_color, center, (self.width // 2, self.height - 2), 4)
        elif direction == DIRECTION_LEFT:
            pygame.draw.line(image, turret_color, center, (2, self.height // 2), 4)

    def set_map(self, game_map):
        """设置地图"""
        self.game_map = game_map

    def add_bullets(self, bullets):
        """设置子弹列表引用"""
        self.bullets = bullets

    def add_enemies(self, enemies):
        """设置敌人列表引用"""
        self.enemies = enemies

    def update_image(self):
        """更新坦克图像"""
        self.original_image = self._create_tank_image()
        self.image = self.original_image
        # 根据方向旋转
        if self.direction == DIRECTION_LEFT:
            self.image = pygame.transform.rotate(self.original_image, 90)
            self.rect = self.image.get_rect()
            self.rect.topleft = (self.x, self.y)
        elif self.direction == DIRECTION_RIGHT:
            self.image = pygame.transform.rotate(self.original_image, -90)
            self.rect = self.image.get_rect()
            self.rect.topleft = (self.x, self.y)
        elif self.direction == DIRECTION_DOWN:
            self.image = pygame.transform.rotate(self.original_image, 180)
            self.rect = self.image.get_rect()
            self.rect.topleft = (self.x, self.y)
        else:
            self.rect = self.image.get_rect()
            self.rect.topleft = (self.x, self.y)

    def move(self, dx: int, dy: int):
        """移动坦克"""
        if dx == 0 and dy == 0:
            return

        # 更新方向
        if dx > 0:
            self.direction = DIRECTION_RIGHT
        elif dx < 0:
            self.direction = DIRECTION_LEFT
        elif dy > 0:
            self.direction = DIRECTION_DOWN
        elif dy < 0:
            self.direction = DIRECTION_UP

        self.update_image()

        # 尝试移动
        new_x = self.x + dx
        new_y = self.y + dy

        # 边界检查
        if not self._check_bounds(new_x, new_y):
            return

        # 碰撞检查
        if self._check_collision(new_x, new_y):
            return

        # 更新位置
        self.x = new_x
        self.y = new_y
        self.rect.topleft = (self.x, self.y)

    def _check_bounds(self, x: int, y: int) -> bool:
        """检查边界"""
        return (GAME_AREA_OFFSET_X <= x <= GAME_AREA_OFFSET_X + GAME_AREA_WIDTH - self.width and
                GAME_AREA_OFFSET_Y <= y <= GAME_AREA_OFFSET_Y + GAME_AREA_HEIGHT - self.height)

    def _check_collision(self, x: int, y: int) -> bool:
        """检查碰撞"""
        if self.game_map is None:
            return False

        test_rect = pygame.Rect(x, y, self.width, self.height)

        # 检查与地图的碰撞
        return self.game_map.check_tank_collision(test_rect)

    def fire(self):
        """射击"""
        if self.fire_cooldown > 0:
            return

        if self.bullets is None:
            return

        # 创建子弹
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
        self.fire_cooldown = self.fire_rate

    def take_damage(self, damage: int):
        """受到伤害"""
        if self.invincible:
            return

        self.health -= damage
        if self.health <= 0:
            self.kill()

    def kill(self):
        """杀死坦克"""
        self.alive_flag = False

    def alive(self) -> bool:
        """是否存活"""
        return self.alive_flag

    def update(self):
        """更新"""
        # 冷却
        if self.fire_cooldown > 0:
            self.fire_cooldown -= 1

        # 无敌时间
        if self.invincible_timer > 0:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False

    def draw(self, screen):
        """绘制"""
        if self.alive_flag:
            screen.blit(self.image, self.rect)
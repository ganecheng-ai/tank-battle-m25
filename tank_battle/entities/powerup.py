"""道具类"""
import pygame
import random
from tank_battle.constants import *
from tank_battle.logger import get_logger


class PowerUp(pygame.sprite.Sprite):
    """道具类"""

    # 道具类型配置
    POWERUP_CONFIGS = {
        POWERUP_STAR: {
            "name": "强化火力",
            "color": COLOR_GOLD,
            "symbol": "★",
        },
        POWERUP_HELMET: {
            "name": "防护头盔",
            "color": COLOR_BLUE,
            "symbol": "⛑",
        },
        POWERUP_SHOVEL: {
            "name": "加固老家",
            "color": COLOR_ORANGE,
            "symbol": "⛏",
        },
        POWERUP_GRENADE: {
            "name": "手雷",
            "color": COLOR_RED,
            "symbol": "💣",
        },
        POWERUP_SPEED: {
            "name": "加速鞋",
            "color": COLOR_GREEN,
            "symbol": "👟",
        },
        POWERUP_TANK: {
            "name": "增加生命",
            "color": (255, 0, 255),
            "symbol": "🚩",
        },
    }

    def __init__(self, x: int, y: int, powerup_type: int = None):
        super().__init__()
        self.logger = get_logger("powerup")

        # 随机选择道具类型
        if powerup_type is None:
            self.powerup_type = random.choice(list(self.POWERUP_CONFIGS.keys()))
        else:
            self.powerup_type = powerup_type

        # 位置
        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        # 存活时间
        self.alive_flag = True
        self.lifetime = 600  # 10秒 (60fps * 10)
        self.blink_time = 120  # 最后2秒闪烁

        # 动画
        self.anim_timer = 0
        self.anim_speed = 10

        # 创建图像
        self.image = self._create_powerup_image()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def _create_powerup_image(self) -> pygame.Surface:
        """创建道具图像"""
        image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # 获取配置
        config = self.POWERUP_CONFIGS[self.powerup_type]
        color = config["color"]
        symbol = config["symbol"]

        # 绘制背景圆形
        pygame.draw.circle(image, (*color, 180), (self.width // 2, self.height // 2), 16)

        # 绘制边框
        pygame.draw.circle(image, color, (self.width // 2, self.height // 2), 16, 2)

        # 绘制符号
        try:
            font = pygame.font.SysFont("Segoe UI Symbol", 20)
            text = font.render(symbol, True, COLOR_WHITE)
            text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
            image.blit(text, text_rect)
        except Exception:
            # 如果字体不支持符号，使用备用绘制
            pygame.draw.circle(image, COLOR_WHITE, (self.width // 2, self.height // 2), 8)

        return image

    def update(self):
        """更新"""
        self.lifetime -= 1
        self.anim_timer += 1

        # 闪烁效果
        if self.lifetime <= self.blink_time:
            if (self.anim_timer // self.anim_speed) % 2 == 0:
                self.image.set_alpha(100)
            else:
                self.image.set_alpha(255)

        # 过期
        if self.lifetime <= 0:
            self.kill()

    def kill(self):
        """移除道具"""
        self.alive_flag = False

    def alive(self) -> bool:
        """是否存活"""
        return self.alive_flag

    def draw(self, screen):
        """绘制"""
        if self.alive_flag:
            screen.blit(self.image, self.rect)


class PowerUpManager:
    """道具管理器"""

    def __init__(self):
        self.logger = get_logger("powerup_manager")
        self.powerups = []
        self.spawn_timer = 0
        self.spawn_interval = 900  # 15秒 (60fps * 15)

    def update(self):
        """更新"""
        # 更新所有道具
        for powerup in self.powerups[:]:
            powerup.update()
            if not powerup.alive():
                self.powerups.remove(powerup)

        # 随机生成道具
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            # 30%概率生成道具
            if random.random() < 0.3:
                self._spawn_random_powerup()

    def _spawn_random_powerup(self):
        """随机生成一个道具"""
        # 在游戏区域内随机位置
        x = random.randint(1, MAP_WIDTH - 2) * TILE_SIZE + GAME_AREA_OFFSET_X
        y = random.randint(2, MAP_HEIGHT - 2) * TILE_SIZE + GAME_AREA_OFFSET_Y

        powerup = PowerUp(x, y)
        self.powerups.append(powerup)
        self.logger.info(f"生成道具: {powerup.POWERUP_CONFIGS[powerup.powerup_type]['name']}")

    def check_collision(self, rect: pygame.Rect):
        """检查玩家是否吃到道具"""
        for powerup in self.powerups[:]:
            if powerup.rect.colliderect(rect):
                powerup_type = powerup.powerup_type
                powerup.kill()
                self.powerups.remove(powerup)
                return powerup_type
        return None

    def get_powerups(self):
        """获取所有道具"""
        return self.powerups

    def clear(self):
        """清除所有道具"""
        self.powerups.clear()
        self.spawn_timer = 0
"""地图系统"""
import pygame
from tank_battle.map.tile import Tile
from tank_battle.constants import *


class TileMap:
    """地图系统"""

    def __init__(self):
        self.width = MAP_WIDTH
        self.height = MAP_HEIGHT
        self.tile_size = TILE_SIZE
        self.tiles = []
        self.base_rect = None
        self.base_alive = True

        # 初始化地图
        self._init_map()

    def _init_map(self):
        """初始化地图"""
        # 创建空地图
        self.tiles = [[TILE_EMPTY for _ in range(self.width)] for _ in range(self.height)]

        # 创建基地 (在底部中间)
        base_x = 6  # 中间
        base_y = 12  # 底部
        self.base_rect = pygame.Rect(
            GAME_AREA_OFFSET_X + base_x * TILE_SIZE,
            GAME_AREA_OFFSET_Y + base_y * TILE_SIZE,
            TILE_SIZE,
            TILE_SIZE
        )

        # 添加基地瓦片
        self.tiles[base_y][base_x] = Tile(TILE_BASE,
            GAME_AREA_OFFSET_X + base_x * TILE_SIZE,
            GAME_AREA_OFFSET_Y + base_y * TILE_SIZE)

        # 边界墙
        self._create_borders()

        # 随机障碍物
        self._create_obstacles()

    def _create_borders(self):
        """创建边界"""
        # 四周
        for i in range(self.width):
            # 顶部和底部
            self.tiles[0][i] = Tile(TILE_STEEL,
                GAME_AREA_OFFSET_X + i * TILE_SIZE,
                GAME_AREA_OFFSET_Y)
            self.tiles[self.height - 1][i] = Tile(TILE_STEEL,
                GAME_AREA_OFFSET_X + i * TILE_SIZE,
                GAME_AREA_OFFSET_Y + (self.height - 1) * TILE_SIZE)

        for i in range(1, self.height - 1):
            # 左侧和右侧
            self.tiles[i][0] = Tile(TILE_STEEL,
                GAME_AREA_OFFSET_X,
                GAME_AREA_OFFSET_Y + i * TILE_SIZE)
            self.tiles[i][self.width - 1] = Tile(TILE_STEEL,
                GAME_AREA_OFFSET_X + (self.width - 1) * TILE_SIZE,
                GAME_AREA_OFFSET_Y + i * TILE_SIZE)

    def _create_obstacles(self):
        """创建随机障碍物"""
        import random

        # 保留区域 (玩家出生点周围不能有障碍)
        safe_zone = [(5, 11), (6, 11), (7, 11), (5, 12), (6, 12), (7, 12)]

        # 敌人出生点 (顶部)
        enemy_spawn = [(1, 0), (5, 0), (9, 0)]

        # 基地周围保护
        base_protection = [(5, 11), (6, 11), (7, 11), (5, 12), (6, 12), (7, 12),
                          (5, 10), (7, 10), (6, 10)]

        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                pos = (x, y)

                # 跳过安全区域
                if pos in safe_zone or pos in enemy_spawn or pos in base_protection:
                    continue

                # 随机生成瓦片
                rand = random.random()
                if rand < 0.1:
                    # 10% 砖块
                    self.tiles[y][x] = Tile(TILE_BRICK,
                        GAME_AREA_OFFSET_X + x * TILE_SIZE,
                        GAME_AREA_OFFSET_Y + y * TILE_SIZE)
                elif rand < 0.15:
                    # 5% 钢铁
                    self.tiles[y][x] = Tile(TILE_STEEL,
                        GAME_AREA_OFFSET_X + x * TILE_SIZE,
                        GAME_AREA_OFFSET_Y + y * TILE_SIZE)
                elif rand < 0.2:
                    # 5% 草丛
                    self.tiles[y][x] = Tile(TILE_GRASS,
                        GAME_AREA_OFFSET_X + x * TILE_SIZE,
                        GAME_AREA_OFFSET_Y + y * TILE_SIZE)

    def get_tile(self, x: int, y: int):
        """获取瓦片"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x]
        return None

    def draw(self, screen):
        """绘制地图"""
        for row in self.tiles:
            for tile in row:
                if tile:
                    tile.draw(screen)

        # 绘制基地
        if self.base_alive:
            pygame.draw.rect(screen, (255, 0, 255), self.base_rect)
            # 绘制旗帜图案
            pygame.draw.rect(screen, (255, 255, 0),
                           (self.base_rect.centerx - 5, self.base_rect.y + 5, 10, 25))
            pygame.draw.polygon(screen, (255, 0, 0),
                              [(self.base_rect.centerx + 5, self.base_rect.y + 5),
                               (self.base_rect.centerx + 15, self.base_rect.y + 12),
                               (self.base_rect.centerx + 5, self.base_rect.y + 19)])

    def check_tank_collision(self, rect: pygame.Rect) -> bool:
        """检查坦克碰撞"""
        # 转换为瓦片坐标
        start_x = max(0, (rect.x - GAME_AREA_OFFSET_X) // TILE_SIZE)
        end_x = min(self.width - 1, (rect.right - GAME_AREA_OFFSET_X) // TILE_SIZE)
        start_y = max(0, (rect.y - GAME_AREA_OFFSET_Y) // TILE_SIZE)
        end_y = min(self.height - 1, (rect.bottom - GAME_AREA_OFFSET_Y) // TILE_SIZE)

        for y in range(start_y, end_y + 1):
            for x in range(start_x, end_x + 1):
                tile = self.tiles[y][x]
                if tile and tile.is_solid():
                    tile_rect = pygame.Rect(
                        GAME_AREA_OFFSET_X + x * TILE_SIZE,
                        GAME_AREA_OFFSET_Y + y * TILE_SIZE,
                        TILE_SIZE,
                        TILE_SIZE
                    )
                    if rect.colliderect(tile_rect):
                        return True

        return False

    def check_bullet_collision(self, bullet) -> bool:
        """检查子弹碰撞"""
        # 转换为瓦片坐标 (使用int()确保是整数类型)
        tx = int((bullet.x - GAME_AREA_OFFSET_X) // TILE_SIZE)
        ty = int((bullet.y - GAME_AREA_OFFSET_Y) // TILE_SIZE)

        if 0 <= tx < self.width and 0 <= ty < self.height:
            tile = self.tiles[ty][tx]
            if tile and tile.is_solid():
                # 钢铁不可破坏
                if tile.type == TILE_STEEL:
                    return True
                # 砖块可破坏
                elif tile.type == TILE_BRICK:
                    tile.destroy()
                    self.tiles[ty][tx] = Tile(TILE_EMPTY, 0, 0)
                    return True
                # 基地
                elif tile.type == TILE_BASE:
                    self.base_alive = False
                    return True

        return False
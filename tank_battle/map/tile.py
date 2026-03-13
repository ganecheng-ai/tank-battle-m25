"""地图瓦片类"""
import pygame
from tank_battle.constants import *


class Tile:
    """瓦片类"""

    def __init__(self, tile_type: int, x: int, y: int):
        self.type = tile_type
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)

        # 颜色映射
        self.colors = {
            TILE_BRICK: COLOR_BRICK_RED,
            TILE_STEEL: COLOR_STEEL_GRAY,
            TILE_GRASS: COLOR_GRASS_GREEN,
            TILE_WATER: COLOR_WATER_BLUE,
            TILE_BASE: (255, 0, 255),  # 紫色 - 基地
        }

    def is_solid(self) -> bool:
        """是否可穿透"""
        return self.type in (TILE_BRICK, TILE_STEEL, TILE_WATER, TILE_BASE)

    def is_destructible(self) -> bool:
        """是否可破坏"""
        return self.type == TILE_BRICK

    def draw(self, screen):
        """绘制瓦片"""
        if self.type == TILE_EMPTY or self.type == TILE_BASE:
            return

        color = self.colors.get(self.type, COLOR_WHITE)

        if self.type == TILE_BRICK:
            # 砖块 - 画成砖块形状
            pygame.draw.rect(screen, color, self.rect)
            # 砖缝
            for i in range(4):
                y = self.rect.y + i * 10
                pygame.draw.line(screen, (100, 20, 20), (self.rect.x, y), (self.rect.right, y), 1)
            for i in range(2):
                x = self.rect.x + i * 20 + 10
                pygame.draw.line(screen, (100, 20, 20), (x, self.rect.y), (x, self.rect.bottom), 1)

        elif self.type == TILE_STEEL:
            # 钢铁 - 带银色高光
            pygame.draw.rect(screen, color, self.rect)
            pygame.draw.rect(screen, (200, 200, 200), self.rect, 2)

        elif self.type == TILE_GRASS:
            # 草丛 - 半透明
            s = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            s.fill((50, 200, 50, 128))
            screen.blit(s, self.rect.topleft)
            # 画草
            for i in range(5):
                gx = self.rect.x + 5 + i * 8
                gy = self.rect.y + 20 + (i % 3) * 5
                pygame.draw.line(screen, (30, 120, 30), (gx, gy + 10), (gx, gy), 2)

        elif self.type == TILE_WATER:
            # 水面 - 蓝色带波纹
            pygame.draw.rect(screen, color, self.rect)
            pygame.draw.line(screen, (100, 200, 255), (self.rect.x + 5, self.rect.y + 15),
                           (self.rect.x + 25, self.rect.y + 15), 2)
            pygame.draw.line(screen, (100, 200, 255), (self.rect.x + 10, self.rect.y + 30),
                           (self.rect.x + 30, self.rect.y + 30), 2)

    def destroy(self):
        """破坏瓦片"""
        if self.is_destructible():
            return True
        return False
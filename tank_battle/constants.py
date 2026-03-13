"""游戏配置常量"""
import os

# ==================== 路径配置 ====================
# 基础路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# 资源目录
SPRITES_DIR = os.path.join(ASSETS_DIR, "sprites")
SOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds")
FONTS_DIR = os.path.join(ASSETS_DIR, "fonts")

# 子目录
TANKS_DIR = os.path.join(SPRITES_DIR, "tanks")
BULLETS_DIR = os.path.join(SPRITES_DIR, "bullets")
TILES_DIR = os.path.join(SPRITES_DIR, "tiles")
EFFECTS_DIR = os.path.join(SPRITES_DIR, "effects")

# ==================== 游戏配置 ====================
# 屏幕尺寸
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

# 游戏区域 (地图区域)
GAME_AREA_WIDTH = 520  # 13格 * 40像素
GAME_AREA_HEIGHT = 520  # 13格 * 40像素
GAME_AREA_OFFSET_X = 40
GAME_AREA_OFFSET_Y = 40

# 瓦片大小
TILE_SIZE = 40

# 地图尺寸 (格数)
MAP_WIDTH = 13
MAP_HEIGHT = 13

# ==================== 坦克配置 ====================
# 玩家坦克
PLAYER_SPEED = 2  # 像素/帧
PLAYER_BULLET_SPEED = 5
PLAYER_FIRE_COOLDOWN = 30  # 帧
PLAYER_MAX_HEALTH = 1

# 敌方坦克
ENEMY_SPEED_MIN = 1
ENEMY_SPEED_MAX = 2
ENEMY_FIRE_COOLDOWN = 60
ENEMY_BULLET_SPEED = 4

# 坦克尺寸
TANK_WIDTH = 32
TANK_HEIGHT = 32

# ==================== 子弹配置 ====================
BULLET_WIDTH = 6
BULLET_HEIGHT = 6
BULLET_DAMAGE = 1

# ==================== 颜色配置 ====================
# 颜色 (R, G, B)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_YELLOW = (255, 255, 0)
COLOR_ORANGE = (255, 165, 0)

# 游戏色调
COLOR_DARK_BG = (26, 26, 46)      # 深色背景
COLOR_MILITARY_GREEN = (46, 125, 50)  # 军绿色
COLOR_GOLD = (255, 215, 0)        # 金色强调
COLOR_BRICK_RED = (178, 34, 34)   # 砖块色
COLOR_STEEL_GRAY = (119, 136, 153) # 钢铁色
COLOR_GRASS_GREEN = (34, 139, 34) # 草地色
COLOR_WATER_BLUE = (30, 144, 255) # 水蓝色

# ==================== 游戏设置 ====================
FPS = 60
MAX_ENEMIES = 4
INITIAL_LIVES = 3

# ==================== 方向 ====================
DIRECTION_UP = 0
DIRECTION_RIGHT = 1
DIRECTION_DOWN = 2
DIRECTION_LEFT = 3

# 方向向量
DIRECTION_VECTORS = {
    DIRECTION_UP: (0, -1),
    DIRECTION_RIGHT: (1, 0),
    DIRECTION_DOWN: (0, 1),
    DIRECTION_LEFT: (-1, 0),
}

# ==================== 瓦片类型 ====================
TILE_EMPTY = 0
TILE_BRICK = 1      # 砖块(可破坏)
TILE_STEEL = 2      # 钢铁(不可破坏)
TILE_GRASS = 3      # 草丛(可隐藏)
TILE_WATER = 4      # 水面(阻挡)
TILE_BASE = 5       # 基地(老家)

# ==================== 道具类型 ====================
POWERUP_STAR = 0     # 星星 - 强化火力
POWERUP_HELMET = 1   # 头盔 - 临时无敌
POWERUP_SHOVEL = 2   # 铁锹 - 加固老家
POWERUP_GRENADE = 3  # 手雷 - 全屏敌人
POWERUP_SPEED = 4    # 鞋子 - 加速
POWERUP_TANK = 5     # 坦克 - 1UP

# ==================== 字体配置 ====================
FONT_SIZE_SMALL = 16
FONT_SIZE_MEDIUM = 24
FONT_SIZE_LARGE = 32
FONT_SIZE_TITLE = 48

# 中文字体优先使用系统字体
CHINESE_FONTS = [
    "Microsoft YaHei",
    "SimHei",
    "SimSun",
    "WenQuanYi Micro Hei",
    "Noto Sans CJK SC",
    "Source Han Sans SC",
]
"""游戏中状态"""
import pygame
import random
from tank_battle.states.game_state import GameState
from tank_battle.constants import *
from tank_battle.logger import get_logger
from tank_battle.entities.player_tank import PlayerTank
from tank_battle.entities.enemy_tank import EnemyTank
from tank_battle.entities.bullet import Bullet
from tank_battle.entities.powerup import PowerUpManager
from tank_battle.entities.explosion import ExplosionManager
from tank_battle.map.tile_map import TileMap


class PlayingState(GameState):
    """游戏中状态"""

    def __init__(self, game):
        super().__init__(game)
        self.logger = get_logger("playing")
        self.logger.info("进入游戏中")

        # 初始化游戏对象
        self.player = None
        self.enemies = []
        self.bullets = []
        self.map = None
        self.enemy_spawn_timer = 0
        self.max_enemies = MAX_ENEMIES

        # 道具和爆炸系统
        self.powerup_manager = PowerUpManager()
        self.explosion_manager = ExplosionManager()

        # 道具效果计时器
        self.shovel_timer = 0
        self.grenade_timer = 0

        # 游戏数据
        self.enemies_killed = 0

        # 初始化
        self._init_game()

    def _init_game(self):
        """初始化游戏"""
        self.logger.info("初始化游戏对象")

        # 创建地图 - 传入关卡参数
        self.map = TileMap(self.game.level)

        # 先初始化列表（确保bullets列表在玩家创建前就存在）
        self.enemies = []
        self.bullets = []
        self.enemy_spawn_timer = 0
        self.enemies_killed = 0

        # 创建玩家坦克
        self.player = PlayerTank(SCREEN_WIDTH // 2 - TILE_SIZE, SCREEN_HEIGHT - TILE_SIZE * 2)
        self.player.add_enemies(self.enemies)
        self.player.add_bullets(self.bullets)
        self.player.set_map(self.map)

        # 初始化道具和爆炸管理器
        self.powerup_manager = PowerUpManager()
        self.explosion_manager = ExplosionManager()

        # 道具效果计时器
        self.shovel_timer = 0
        self.grenade_timer = 0

        # 生成初始敌人
        self._spawn_enemy()
        self._spawn_enemy()
        self._spawn_enemy()
        self._spawn_enemy()

    def _spawn_enemy(self):
        """生成敌方坦克"""
        if len(self.enemies) >= self.max_enemies:
            return

        # 随机生成位置 (上方三行)
        x = random.choice([1, 5, 9]) * TILE_SIZE + GAME_AREA_OFFSET_X
        y = GAME_AREA_OFFSET_Y + TILE_SIZE

        enemy = EnemyTank(x, y)
        enemy.add_bullets(self.bullets)
        enemy.set_map(self.map)
        self.enemies.append(enemy)

    def handle_event(self, event):
        """处理事件"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                # 暂停功能可后续添加
                pass
            elif event.key == pygame.K_r:
                # 重新开始
                self._init_game()

        # 玩家控制
        if self.player:
            self.player.handle_event(event)

    def update(self):
        """更新游戏"""
        # 更新玩家
        if self.player and self.player.alive():
            self.player.update()

        # 更新敌人
        for enemy in self.enemies:
            enemy.update()
            if not enemy.alive():
                self.enemies.remove(enemy)

        # 更新子弹
        for bullet in self.bullets:
            bullet.update()
            if not bullet.alive():
                self.bullets.remove(bullet)

        # 更新道具系统
        self.powerup_manager.update()
        self.explosion_manager.update()

        # 检查玩家是否吃到道具
        if self.player and self.player.alive():
            powerup_type = self.powerup_manager.check_collision(self.player.rect)
            if powerup_type is not None:
                self._apply_powerup(powerup_type)

        # 处理道具效果计时器
        if self.shovel_timer > 0:
            self.shovel_timer -= 1
            if self.shovel_timer == 0:
                # 恢复钢铁为普通砖块
                self.map.revert_base_protection()

        # 子弹与坦克碰撞检测
        self._check_bullet_collisions()

        # 生成新敌人
        if len(self.enemies) < self.max_enemies:
            self.enemy_spawn_timer += 1
            if self.enemy_spawn_timer >= 120:  # 2秒后生成
                self._spawn_enemy()
                self.enemy_spawn_timer = 0

        # 检查胜利条件
        if self.map.base_alive and self.enemies_killed >= 20:
            self.game.game_won = True

    def _apply_powerup(self, powerup_type: int):
        """应用道具效果"""
        powerup_names = {
            POWERUP_STAR: "强化火力",
            POWERUP_HELMET: "防护头盔",
            POWERUP_SHOVEL: "加固老家",
            POWERUP_GRENADE: "手雷",
            POWERUP_SPEED: "加速鞋",
            POWERUP_TANK: "增加生命",
        }

        self.logger.info(f"获得道具: {powerup_names.get(powerup_type, '未知')}")

        if powerup_type == POWERUP_STAR:
            # 强化火力
            if self.player:
                self.player.upgrade_power()
                self.game.add_score(50)

        elif powerup_type == POWERUP_HELMET:
            # 临时无敌
            if self.player:
                self.player.invincible = True
                self.player.invincible_timer = 600  # 10秒

        elif powerup_type == POWERUP_SHOVEL:
            # 加固老家
            if self.map:
                self.map.protect_base()
                self.shovel_timer = 600  # 10秒
            self.game.add_score(50)

        elif powerup_type == POWERUP_GRENADE:
            # 全屏敌人
            for enemy in self.enemies[:]:
                enemy.take_damage(10)  # 秒杀
                self.explosion_manager.add_explosion(enemy.x, enemy.y, "normal")
            self.game.add_score(100)

        elif powerup_type == POWERUP_SPEED:
            # 加速
            if self.player:
                self.player.speed = PLAYER_SPEED * 2
                # 5秒后恢复正常速度
                self.player.speed_timer = 300

        elif powerup_type == POWERUP_TANK:
            # 增加生命
            self.game.add_life()
            self.game.add_score(50)

    def _check_bullet_collisions(self):
        """子弹碰撞检测"""
        for bullet in self.bullets[:]:
            if not bullet.alive():
                continue

            # 子弹与地图碰撞
            if self.map.check_bullet_collision(bullet):
                bullet.kill()
                continue

            # 玩家子弹击中敌人
            if bullet.owner == "player":
                for enemy in self.enemies[:]:
                    if enemy.rect.colliderect(bullet.rect):
                        enemy.take_damage(bullet.damage)
                        bullet.kill()
                        if not enemy.alive():
                            self.enemies_killed += 1
                            self.game.add_score(100)
                            # 添加爆炸效果
                            self.explosion_manager.add_explosion(enemy.x, enemy.y, "normal")
                        break

            # 敌方子弹击中玩家
            elif bullet.owner == "enemy":
                if self.player and self.player.alive():
                    if self.player.rect.colliderect(bullet.rect):
                        self.player.take_damage(bullet.damage)
                        bullet.kill()
                        if not self.player.alive():
                            self.explosion_manager.add_explosion(self.player.x, self.player.y, "large")
                            self._player_died()

    def _player_died(self):
        """玩家死亡"""
        self.logger.info("玩家死亡")
        if self.game.lives > 1:
            self.game.lose_life()
            # 复活玩家
            self.player = PlayerTank(SCREEN_WIDTH // 2 - TILE_SIZE, SCREEN_HEIGHT - TILE_SIZE * 2)
            self.player.add_enemies(self.enemies)
            self.player.add_bullets(self.bullets)
            self.player.set_map(self.map)
        else:
            self.game.lose_life()
            from tank_battle.states.game_over_state import GameOverState
            self.game.change_state(GameOverState)

    def draw(self, screen):
        """绘制游戏"""
        # 背景
        screen.fill(COLOR_BLACK)

        # 绘制地图
        if self.map:
            self.map.draw(screen)

        # 绘制敌人
        for enemy in self.enemies:
            enemy.draw(screen)

        # 绘制玩家
        if self.player and self.player.alive():
            self.player.draw(screen)

        # 绘制子弹
        for bullet in self.bullets:
            bullet.draw(screen)

        # 绘制道具
        for powerup in self.powerup_manager.get_powerups():
            powerup.draw(screen)

        # 绘制爆炸效果
        for explosion in self.explosion_manager.get_explosions():
            explosion.draw(screen)

        # 绘制UI
        self._draw_ui(screen)

    def _draw_ui(self, screen):
        """绘制UI"""
        font = pygame.font.SysFont(CHINESE_FONTS, FONT_SIZE_SMALL)

        # 分数
        score_text = font.render(f"分数: {self.game.score}", True, COLOR_WHITE)
        screen.blit(score_text, (GAME_AREA_OFFSET_X, 10))

        # 关卡
        level_text = font.render(f"关卡: {self.game.level}", True, COLOR_WHITE)
        screen.blit(level_text, (GAME_AREA_OFFSET_X + 200, 10))

        # 生命
        lives_text = font.render(f"生命: {self.game.lives}", True, COLOR_RED)
        screen.blit(lives_text, (GAME_AREA_OFFSET_X + 400, 10))

        # 敌人数量
        enemy_text = font.render(f"敌人: {self.enemies_killed}/20", True, COLOR_WHITE)
        screen.blit(enemy_text, (GAME_AREA_OFFSET_X + 450, 10))

        # 操作提示
        hint_font = pygame.font.SysFont(CHINESE_FONTS, FONT_SIZE_SMALL - 2)
        hint = hint_font.render("方向键移动 空格射击 R重开", True, COLOR_GREEN)
        screen.blit(hint, (SCREEN_WIDTH - 190, 10))
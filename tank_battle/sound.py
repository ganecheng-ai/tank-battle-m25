"""音效系统"""
import os
import pygame
from tank_battle.constants import SOUNDS_DIR
from tank_battle.logger import get_logger


class SoundManager:
    """音效管理器"""

    def __init__(self):
        self.logger = get_logger("sound")
        self.enabled = True
        self.sounds = {}
        self.music_volume = 0.5
        self.sfx_volume = 0.7

        # 初始化pygame.mixer
        try:
            pygame.mixer.init()
            self.logger.info("音效系统初始化成功")
        except Exception as e:
            self.logger.warning(f"音效系统初始化失败: {e}")
            self.enabled = False
            return

        # 加载音效
        self._load_sounds()

    def _load_sounds(self):
        """加载音效文件"""
        if not self.enabled:
            return

        # 音效文件映射
        sound_files = {
            "shoot": "shoot.wav",
            "explosion": "explosion.wav",
            "powerup": "powerup.wav",
            "player_die": "player_die.wav",
            "enemy_die": "enemy_die.wav",
            "game_over": "game_over.wav",
            "win": "win.wav",
            "bullet_hit": "bullet_hit.wav",
        }

        for name, filename in sound_files.items():
            try:
                filepath = os.path.join(SOUNDS_DIR, filename)
                if os.path.exists(filepath):
                    self.sounds[name] = pygame.mixer.Sound(filepath)
                    self.sounds[name].set_volume(self.sfx_volume)
                else:
                    # 记录缺失的音效文件（调试用）
                    self.logger.debug(f"音效文件不存在: {filepath}")
            except Exception as e:
                self.logger.warning(f"加载音效失败 {filename}: {e}")

    def play_sound(self, name: str, volume: float = None):
        """播放音效"""
        if not self.enabled:
            return

        if name in self.sounds:
            sound = self.sounds[name]
            if volume is not None:
                sound.set_volume(volume)
            else:
                sound.set_volume(self.sfx_volume)
            sound.play()
        else:
            # 音效不存在时静默处理（不记录日志避免干扰）
            pass

    def play_shoot(self):
        """播放射击音效"""
        self.play_sound("shoot")

    def play_explosion(self):
        """播放爆炸音效"""
        self.play_sound("explosion")

    def play_powerup(self):
        """播放获得道具音效"""
        self.play_sound("powerup")

    def play_player_die(self):
        """播放玩家死亡音效"""
        self.play_sound("player_die")

    def play_enemy_die(self):
        """播放敌人死亡音效"""
        self.play_sound("enemy_die")

    def play_game_over(self):
        """播放游戏结束音效"""
        self.play_sound("game_over")

    def play_win(self):
        """播放胜利音效"""
        self.play_sound("win")

    def play_bullet_hit(self):
        """播放子弹命中音效"""
        self.play_sound("bullet_hit")

    def set_music_volume(self, volume: float):
        """设置音乐音量 (0.0 - 1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))

    def set_sfx_volume(self, volume: float):
        """设置音效音量 (0.0 - 1.0)"""
        self.sfx_volume = max(0.0, min(1.0, volume))
        # 更新已加载音效的音量
        for sound in self.sounds.values():
            sound.set_volume(self.sfx_volume)

    def toggle_sound(self):
        """切换音效开关"""
        self.enabled = not self.enabled
        if self.enabled:
            self.logger.info("音效已开启")
        else:
            self.logger.info("音效已关闭")
        return self.enabled


# 全局音效管理器实例
_sound_manager = None


def get_sound_manager() -> SoundManager:
    """获取音效管理器单例"""
    global _sound_manager
    if _sound_manager is None:
        _sound_manager = SoundManager()
    return _sound_manager
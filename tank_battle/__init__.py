"""tank_battle 包"""
from tank_battle.game import TankBattleGame
from tank_battle.logger import setup_logger, get_logger

__version__ = "0.1.0"
__author__ = "Tank Battle Team"

__all__ = ["TankBattleGame", "setup_logger", "get_logger"]
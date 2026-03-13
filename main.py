"""坦克大战游戏 - 入口文件"""
import sys
import os

# 确保项目根目录在Python路径中
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tank_battle.logger import setup_logger
from tank_battle.game import TankBattleGame


def main():
    """主函数"""
    # 设置日志
    logger = setup_logger()
    logger.info("=" * 50)
    logger.info("坦克大战游戏启动")
    logger.info("=" * 50)

    try:
        # 创建并运行游戏
        game = TankBattleGame()
        game.run()
    except Exception as e:
        logger.exception(f"游戏异常退出: {e}")
        raise
    finally:
        logger.info("游戏退出")


if __name__ == "__main__":
    main()
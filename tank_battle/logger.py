"""日志系统模块"""
import logging
import os
import sys
from datetime import datetime


def setup_logger(name: str = "tank_battle", log_file: str = None) -> logging.Logger:
    """
    设置日志系统

    Args:
        name: 日志记录器名称
        log_file: 日志文件路径，默认为运行目录下的 tank_battle.log

    Returns:
        配置好的日志记录器
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # 清除已有的处理器
    logger.handlers.clear()

    # 如果没有指定日志文件，使用运行目录
    if log_file is None:
        log_file = os.path.join(os.getcwd(), "tank_battle.log")

    # 文件处理器 - 记录所有级别
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)

    # 控制台处理器 - 记录INFO及以上
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)

    # 格式化器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def get_logger(name: str = None) -> logging.Logger:
    """获取日志记录器"""
    if name:
        return logging.getLogger(f"tank_battle.{name}")
    return logging.getLogger("tank_battle")
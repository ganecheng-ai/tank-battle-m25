# 坦克大战 (Tank Battle M25)

一个使用 Python 和 Pygame 开发的经典坦克大战游戏。

## 游戏介绍

这是一个向经典街机游戏《坦克大战》(Battle City) 致敬的作品。玩家控制坦克，保护基地，消灭敌人，体验原汁原味的战斗乐趣。

## 功能特性

- 🎮 经典操作体验 - 方向键移动，空格键射击
- 🀄 简体中文界面
- 🎯 多种敌人类型 - 普通、快速、重型
- 🗺️ 随机生成地图 - 难度随关卡递增
- 💥 丰富的视觉效果 - 爆炸动画、特效
- 📊 分数系统
- 🔄 关卡系统
- ⭐ 道具系统 - 星星、头盔、铁锹、手雷、鞋子、坦克
- 🔊 音效系统支持 (需要资源文件)

## 环境要求

- Python 3.10+
- Pygame 2.5+

## 安装

```bash
# 克隆仓库
git clone https://github.com/ganecheng-ai/tank-battle-m25.git
cd tank-battle-m25

# 安装依赖
pip install -r requirements.txt
```

## 运行游戏

```bash
python main.py
```

## 操作说明

| 按键 | 功能 |
|------|------|
| ↑↓←→ | 移动坦克 |
| 空格 | 射击 |
| R | 重新开始 |

## 游戏规则

- 保护底部中间的基地不被摧毁
- 消灭20辆敌方坦克即可过关
- 每辆坦克只有一次生命
- 初始生命：3条

## 道具系统

游戏中有多种道具可以帮助玩家：

| 道具 | 效果 |
|------|------|
| ⭐ 星星 | 升级火力 (最多3级) |
| ⛑ 头盔 | 临时无敌 (10秒) |
| ⛏ 铁锹 | 加固基地 (10秒) |
| 💣 手雷 | 消灭全屏敌人 |
| 👟 鞋子 | 加速移动 (5秒) |
| 🚩 坦克 | 增加1条生命 |

## 项目结构

```
tank-battle-m25/
├── main.py                 # 游戏入口
├── requirements.txt        # 依赖列表
├── tank_battle/           # 游戏主包
│   ├── game.py            # 游戏主类
│   ├── constants.py       # 配置常量
│   ├── logger.py          # 日志系统
│   ├── sound.py           # 音效系统
│   ├── entities/          # 游戏实体
│   │   ├── tank.py        # 坦克基类
│   │   ├── player_tank.py # 玩家坦克
│   │   ├── enemy_tank.py  # 敌方坦克
│   │   ├── bullet.py      # 子弹
│   │   ├── powerup.py     # 道具
│   │   └── explosion.py   # 爆炸效果
│   ├── map/               # 地图系统
│   │   ├── tile.py        # 瓦片
│   │   └── tile_map.py    # 地图
│   └── states/            # 游戏状态
│       ├── menu_state.py      # 菜单
│       ├── playing_state.py   # 游戏中
│       └── game_over_state.py # 游戏结束
├── assets/                # 资源文件
│   ├── sprites/           # 图片资源
│   ├── sounds/            # 音效资源
│   └── fonts/             # 字体资源
└── .github/               # GitHub Actions
```

## 日志

游戏运行时会自动在当前目录生成 `tank_battle.log` 文件，记录游戏运行信息。

## 构建发布

当创建 git tag 时会自动触发构建并发布：

```bash
git tag v1.0.0
git push origin v1.0.0
```

构建产物：
- Windows: `.exe` + `.zip`
- Linux: `.tar.gz`
- macOS: `.tar.gz`

## 技术栈

- Python 3.10+
- Pygame 2.5+
- PyInstaller (打包)

## 许可证

MIT License

## 作者

Tank Battle Team
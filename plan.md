# 坦克大战游戏开发计划

## 项目概述
使用Python + Pygame开发一个经典的坦克大战游戏（类似Battle City/坦克大战），支持简体中文界面，画面精美，操作与经典游戏一致。

## 技术栈
- **Python**: 3.10+
- **游戏框架**: Pygame 2.x (SDL2)
- **打包工具**: PyInstaller (跨平台构建)
- **版本控制**: Git + GitHub Actions

## 项目结构
```
tank-battle/
├── main.py                    # 游戏入口
├── requirements.txt           # 依赖
├── tank_battle/
│   ├── __init__.py
│   ├── game.py               # 游戏主循环
│   ├── constants.py          # 配置常量
│   ├── logger.py             # 日志系统
│   ├── entities/
│   │   ├── tank.py           # 坦克基类
│   │   ├── player_tank.py    # 玩家坦克
│   │   ├── enemy_tank.py     # 敌方坦克
│   │   └── bullet.py         # 子弹
│   ├── map/
│   │   ├── tile_map.py       # 地图系统
│   │   └── tile.py           # 瓦片类
│   ├── states/
│   │   ├── game_state.py     # 游戏状态基类
│   │   ├── menu_state.py     # 菜单状态
│   │   ├── playing_state.py  # 游戏中状态
│   │   └── game_over_state.py# 游戏结束状态
│   └── utils/
│       └── vector.py         # 向量运算
├── assets/
│   ├── sprites/              # 精灵图片
│   └── fonts/                # 字体(支持中文)
└── .github/
    └── workflows/
        └── build.yml         # GitHub Actions构建
```

## 核心功能

### 已实现
1. ✅ 项目结构创建
2. ✅ 日志系统
3. ✅ 游戏状态管理 (菜单、游戏、结束)
4. ✅ 地图系统 (边界、随机障碍物、基地)
5. ✅ 玩家坦克 (移动、射击、碰撞检测)
6. ✅ 敌方坦克 (AI、随机移动和射击)
7. ✅ 子弹系统 (碰撞检测、伤害)
8. ✅ UI界面 (分数、关卡、生命显示)
9. ✅ 中文界面显示
10. ✅ 道具系统 (星星、头盔、铁锹、手雷、鞋子、坦克)
11. ✅ 爆炸效果
12. ✅ 音效系统 (框架已创建)
13. ✅ 关卡难度递增

### 待实现 (后续迭代)
- 音效资源文件 (wav格式)
- 更多关卡设计

## 开发阶段

### Phase 1: 基础框架 ✅
- 项目结构创建
- 日志系统
- 资源加载器
- 游戏状态管理

### Phase 2: 地图系统 ✅
- 瓦片定义
- 地图渲染
- 基地保护

### Phase 3: 玩家坦克 ✅
- 移动控制
- 射击
- 碰撞检测

### Phase 4: 敌方坦克 ✅
- AI系统
- 行为模式

### Phase 5: UI和游戏流程 ✅
- 菜单界面
- 分数显示
- 游戏结束画面

### Phase 6: 构建和发布 ✅
- PyInstaller配置
- GitHub Actions
- Release自动化

## 验证结果

- ✅ 游戏可以正常启动
- ✅ 日志系统正常工作 (tank_battle.log)
- ✅ 中文菜单界面显示正常
- ✅ 游戏主循环运行正常

## GitHub Actions 构建

### 矩阵策略
- Windows (windows-latest)
- Linux (ubuntu-latest)
- macOS (macos-latest)

### 构建产物
- Windows: `.exe` + `.zip` + `checksums.txt`
- Linux: `.tar.gz` + `checksums.txt`
- macOS: `.tar.gz` + `checksums.txt`

### 触发条件
- 创建tag时自动构建发布 (v*)

## 更新日志

### v0.2.1 (2026-03-13)
- 新增道具系统 (星星、头盔、铁锹、手雷、鞋子、坦克)
- 新增爆炸效果系统
- 新增音效管理器 (sound.py)
- 关卡难度随关卡数增加
- 新增 add_life() 方法

### v0.1.1 (2026-03-13)
- 修复按R报错的问题（浮点数索引bug）
- 优化代码结构

### v0.1.0 (2026-03-13)
- 初始版本
- 基础游戏功能
- 中文界面
- 日志系统
- GitHub Actions 自动构建
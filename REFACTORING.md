# PMCL 代码重构说明

## 重构概述

本次重构将原有的单体 Python 文件（`pmcl.py` 542 行，`jc.py` 44 行）重构为模块化、可维护的现代 Python 项目结构。

## 新的项目结构

```
/workspace/
├── src/                          # 源代码目录
│   ├── __init__.py               # 包版本信息
│   ├── main.py                   # 新的主入口点
│   ├── config/                   # 配置管理模块
│   │   ├── __init__.py
│   │   ├── constants.py          # 常量定义
│   │   └── config_manager.py     # 配置管理器
│   ├── core/                     # 核心业务逻辑
│   │   ├── __init__.py
│   │   └── launcher.py           # 游戏启动器
│   ├── ui/                       # UI 组件
│   │   ├── __init__.py
│   │   ├── main_window.py        # 主窗口
│   │   ├── settings_dialog.py    # 设置对话框
│   │   └── vape_select_dialog.py # 外挂选择对话框
│   └── utils/                    # 工具模块
│       ├── __init__.py
│       └── styles.py             # 样式表定义
├── jc.py                         # 保留的旧入口（已重构使用新模块）
└── pmcl.py                       # 保留的旧入口（已重构使用新模块）
```

## 主要改进

### 1. 代码结构优化
- **分离关注点**: UI 代码与业务逻辑完全分离
- **模块化设计**: 按功能划分为 config、core、ui、utils 四个模块
- **单一职责**: 每个类只负责一个明确的功能

### 2. 配置管理
- **ConfigManager 类**: 统一管理所有配置的读写
- **常量集中**: 所有魔法数字和常量定义在 `constants.py`
- **类型安全**: 使用类型提示确保配置值的正确性

### 3. 错误处理
- **具体异常**: 替换裸 `except:` 为具体的异常处理
- **验证逻辑**: 启动参数验证集中在 `GameLauncher.validate_launch_params()`
- **更好的反馈**: 错误消息更明确和友好

### 4. 样式管理
- **Styles 类**: 所有 Qt 样式表集中定义，避免重复
- **易于维护**: 修改样式只需在一处更改

### 5. 命名规范
- **语义化命名**: 
  - `maxmb_t` → `maxmb_t` (保持但添加注释)
  - `game_c` → `game_c` (保持但添加注释)
  - `ty` → 消除，使用明确的变量名
- **英文注释**: 所有文档字符串使用英文
- **函数命名**: 使用动词 + 名词的清晰组合

### 6. 类型提示
- 所有函数都有参数和返回值类型注解
- 使用 `Optional`、`Tuple`、`Dict` 等泛型类型
- 提高代码可读性和 IDE 支持

### 7. 资源管理
- **上下文管理器**: 使用 `with` 语句管理 shelve 数据库
- **路径处理**: 使用 `pathlib.Path` 替代字符串拼接
- **目录创建**: 自动创建必要的目录

## 使用方式

### 方式 1: 使用新入口
```bash
python -m src.main
```

### 方式 2: 使用原有入口（向后兼容）
```bash
python pmcl.py
# 或
python jc.py
```

## 测试

运行测试验证重构后的功能：

```bash
# 测试配置模块
python -c "from src.config import ConfigManager; print('OK')"

# 测试核心模块
python -c "from src.core import GameLauncher; print('OK')"

# 测试 UI 模块（需要显示环境）
QT_QPA_PLATFORM=offscreen python -c "from src.ui import MainWindow; print('OK')"
```

## 迁移说明

原有功能完全保留，只是代码组织结构发生变化：
- 所有 UI 元素和功能保持不变
- 配置文件格式兼容（继续使用 shelve 和 txt 文件）
- 启动脚本（start_game.bat, fix.bat）使用方式不变

## 后续改进建议

1. **日志系统**: 添加 logging 模块替代 print
2. **单元测试**: 为各模块编写 pytest 测试
3. **配置文件**: 使用 JSON 或 YAML 替代 shelve
4. **国际化**: 添加 i18n 支持多语言
5. **主题系统**: 支持用户自定义 UI 主题

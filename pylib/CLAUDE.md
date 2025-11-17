# Python 库模块文档

[根目录](../../CLAUDE.md) > **pylib**

## ✨ 导航面包屑
`[根目录](../../CLAUDE.md) > **pylib**`

## 模块职责

Python 库模块作为 Rust 核心层的包装器，提供：

- Rust 核心功能的 Python 接口
- 跨语言通信桥梁（通过 Protobuf）
- Python 端的业务逻辑封装
- 数据库操作和集合管理
- 调度算法和学习统计
- 导入导出功能

## 入口和启动

- **后端接口**: `anki/_backend.py` - Rust 后端的主要 Python 接口
- **Rust 桥接**: `anki/_rsbridge.pyi` - Rust 桥接的类型定义
- **集合管理**: `anki/collection.py` - 集合操作的核心接口

### 核心架构
```
Python 应用 → anki/_backend.py → rsbridge → Rust 核心层
```

## 外部接口

### 核心模块
- **后端接口**: `_backend.py` - Rust 后端的 Python 包装
- **集合管理**: `collection.py` - 数据库集合操作
- **卡片管理**: `cards.py` - 卡片相关操作
- **牌组管理**: `decks.py` - 牌组管理功能
- **笔记管理**: `notes.py` - 笔记操作
- **模板管理**: `template.py` - 卡片模板处理

### 工具模块
- **数据库**: `db.py`, `dbproxy.py` - 数据库操作
- **配置**: `config.py` - 配置管理
- **搜索**: `find.py` - 搜索功能
- **导入导出**: `importing.py`, `exporting.py` - 数据交换
- **同步**: `sync.py`, `syncserver.py` - 同步功能

### 支持模块
- **媒体**: `media.py` - 媒体文件管理
- **声音**: `sound.py` - 音频处理
- **LaTeX**: `latex.py` - LaTeX 渲染
- **统计**: `stats.py` - 学习统计
- **工具**: `utils.py` - 通用工具函数

## 关键依赖和配置

### Python 依赖
```python
dependencies = [
    "decorator",
    "markdown",
    "orjson",
    "protobuf>=6.0,<8.0",
    "requests[socks]",
    "typing_extensions",
    "distro; sys_platform != 'darwin' and sys_platform != 'win32'"
]
```

### 构建配置
- **项目配置**: `pyproject.toml`
- **构建钩子**: `hatch_build.py`
- **包结构**: 打包为 `anki` 包
- **版本管理**: 从 `../python/version.py` 获取

## 数据模型

### 核心数据结构
- **Collection**: 数据库集合，包含所有学习数据
- **Card**: 学习卡片，包含正面、反面、调度信息
- **Note**: 笔记，包含多个字段和标签
- **Deck**: 牌组，组织卡片的方式
- **Model**: 卡片模板，定义卡片格式

### 配置和常量
- `consts.py` - 系统常量定义
- `config.py` - 配置项管理
- `types.py` - 类型定义

### 错误处理
- `errors.py` - 自定义异常类
- 统一的错误处理机制

## 测试和质量

### 测试覆盖
- `tests/test_collection.py` - 集合操作测试
- `tests/test_cards.py` - 卡片功能测试
- `tests/test_decks.py` - 牌组管理测试
- `tests/test_importing.py` - 导入功能测试
- `tests/test_exporting.py` - 导出功能测试
- `tests/test_media.py` - 媒体文件测试
- `tests/test_find.py` - 搜索功能测试
- `tests/test_template.py` - 模板处理测试
- `tests/test_schedv3.py` - 调度算法测试
- `tests/test_utils.py` - 工具函数测试

### 测试数据
- `tests/support/` - 测试数据和支持文件
- 包含各种格式的示例数据文件

### 代码质量
- Python 类型检查: `./tools/dmypy`
- 使用 `py.typed` 启用类型检查
- 遵循 PEP 8 代码风格

## 常见问题 (FAQ)

**Q: Python 如何与 Rust 后端通信？**
A: 通过 `_backend.py` 模块，使用 Protobuf 定义的接口进行跨语言通信。

**Q: 如何扩展新的业务功能？**
A: 在 Rust 层实现核心逻辑，然后在 Python 层添加包装接口。

**Q: 数据库操作如何处理？**
A: 通过 `db.py` 和 `dbproxy.py` 模块，大部分操作委托给 Rust 层。

**Q: 如何处理不同平台的数据路径？**
A: 使用 `utils.py` 中的跨平台路径处理函数。

**Q: 添加新的导入/导出格式？**
A: 在 `importing.py` 或 `exporting.py` 中添加新的处理器。

## 相关文件列表

### 核心接口
- `anki/_backend.py`
- `anki/collection.py`
- `anki/cards.py`
- `anki/decks.py`
- `anki/notes.py`

### 数据和配置
- `anki/db.py`
- `anki/config.py`
- `anki/consts.py`
- `anki/types.py`

### 业务功能
- `anki/find.py`
- `anki/importing.py`
- `anki/exporting.py`
- `anki/sync.py`
- `anki/media.py`

### 工具和支持
- `anki/utils.py`
- `anki/template.py`
- `anki/stats.py`
- `anki/errors.py`

### 测试文件
- `tests/test_*.py`
- `tests/support/` 目录

### 配置文件
- `pyproject.toml`
- `hatch_build.py`
- `README.md`

## 更新日志

- 2025-06-17: 初始化模块文档，添加导航面包屑
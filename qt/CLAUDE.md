# PyQt GUI 界面模块文档

[根目录](../../CLAUDE.md) > **qt**

## ✨ 导航面包屑
`[根目录](../../CLAUDE.md) > **qt**`

## 模块职责

PyQt GUI 模块负责 Anki 的桌面应用程序界面，包括：

- 桌面应用程序的主界面和窗口管理
- 嵌入式 Web 组件的集成
- 用户交互事件处理
- 系统集成（文件对话框、系统托盘等）
- 音视频播放和多媒体支持
- 插件系统和扩展支持
- 跨平台应用程序启动和部署

## 入口和启动

- **主入口**: `aqt/__init__.py` - 应用程序启动和环境检查
- **主窗口**: `aqt/main.py` - 主界面窗口实现
- **启动脚本**: `runanki.py` - 可执行入口点
- **应用启动器**: `launcher/` - 跨平台启动器和安装管理

### 启动流程
1. **启动器阶段**: 通过 launcher 检查环境、管理依赖
2. **环境检查**: Python 版本、编码支持等
3. **同步服务器模式检查**: `--syncserver` 参数处理
4. **平台特定初始化**: Windows AppUserModelID 设置等
5. **主窗口创建**: PyQt 应用程序启动和显示

## 外部接口

### 主要模块结构
- `aqt/`: 主要 GUI 组件
- `launcher/`: 应用程序启动器和部署管理

### 核心组件
- **主窗口**: `aqt/main.py` - 应用程序主窗口
- **复习器**: `aqt/reviewer.py` - 卡片复习界面
- **编辑器**: `aqt/editor.py` - 卡片编辑界面
- **浏览器**: `aqt/browser.py` - 卡片浏览和管理
- **设置**: `aqt/preferences.py` - 用户偏好设置
- **同步**: `aqt/sync.py` - 同步功能界面

### 集成组件
- **Web 视图**: `aqt/webview.py` - 嵌入式 Web 组件封装
- **媒体服务**: `aqt/mediasrv.py` - 媒体文件服务
- **音视频**: `aqt/mpv.py`, `aqt/sound.py`, `aqt/tts.py` - 多媒体播放
- **进度**: `aqt/progress.py` - 进度对话框

### 启动器详细功能
- **跨平台启动**: `launcher/src/main.rs` - Rust 启动器核心
- **平台适配**: `launcher/src/platform/` - Windows/macOS/Linux 支持
- **Python 环境**: UV 包管理和依赖解析
- **安装管理**: `launcher/{win,mac,lin}/` - 平台特定安装包
- **版本控制**: 自动更新和回滚机制
- **错误报告**: 启动错误诊断和收集

## 关键依赖和配置

### Python 依赖
```python
dependencies = [
    "beautifulsoup4",
    "flask",
    "flask_cors",
    "jsonschema",
    "requests",
    "send2trash",
    "waitress>=2.0.0",
    "pyqt6>=6.2",
    "pyqt6-webengine>=6.2"
]
```

### 平台特定依赖
- Windows: `pywin32`
- macOS: `anki-mac-helper>=0.1.1`
- 音频: `anki-audio==0.1.0` (Windows/macOS)

### 启动器依赖 (Rust)
```toml
[dependencies]
anki_i18n = { workspace = true }
anki_io = { workspace = true }
anki_process = { workspace = true }
anyhow = "1.0.98"
```

### 构建配置
- **构建配置**: `pyproject.toml`
- **构建钩子**: `hatch_build.py`
- **包配置**: 排除 `aqt/data` 和 `*.ui` 文件
- **启动器配置**: `launcher/pyproject.toml`, `launcher/Cargo.toml`

## 数据模型

### 配置和设置
- 用户配置通过 `anki.collection.Config` 管理
- 界面偏好设置存储在用户配置文件中
- 主题和样式通过 `theme.py` 和 `stylesheets.py` 管理

### 插件系统
- 插件管理: `aqt/addons.py`
- 插件钩子: `aqt/gui_hooks.py`
- 插件 API 通过钩子系统提供

### 启动器状态管理
- **版本信息**: `launcher/versions.py` - 版本控制和兼容性
- **环境状态**: Python 环境、依赖缓存、同步状态
- **平台配置**: 文件关联、菜单项、图标资源

## 测试和质量

### 测试文件
- `tests/test_addons.py` - 插件系统测试
- `tests/test_i18n.py` - 国际化测试
- 启动器测试通过 Rust 测试框架

### 代码质量
- Python 类型检查: `./tools/dmypy`
- 遵循 PEP 8 代码风格
- 使用 `py.typed` 启用类型检查
- Rust 代码: `cargo fmt`, `cargo clippy`

## 常见问题 (FAQ)

**Q: 如何启动 Anki 应用程序？**
A: 可以通过启动器自动管理（推荐），或直接运行 `python qt/runanki.py`。

**Q: 启动器如何处理不同平台？**
A: 使用 Rust 编写的跨平台启动器，为每个操作系统提供特定的安装和运行支持。

**Q: 如何处理 PyQt 版本兼容性？**
A: 项目支持多个 PyQt 版本，通过可选依赖项管理特定版本。

**Q: Web 组件如何与 Python 交互？**
A: 通过 `aqt/webview.py` 封装，使用 Flask 服务器和 POST 请求通信。

**Q: 如何添加新的界面组件？**
A: 在 `aqt/` 目录下创建新的 Python 模块，遵循现有的组件结构。

**Q: 插件如何与主应用交互？**
A: 通过 `aqt/gui_hooks.py` 定义的钩子系统，插件可以注册回调函数。

**Q: 启动器如何管理 Python 依赖？**
A: 使用 UV 包管理器，支持用户级别和分发版级别的环境管理。

**Q: 如何构建安装包？**
A: 使用启动器中的平台特定构建脚本：Windows (build.bat), macOS (build.sh), Linux (install.sh)。

## 相关文件列表

### 核心文件
- `aqt/__init__.py` - 应用程序入口
- `aqt/main.py` - 主窗口
- `aqt/reviewer.py` - 复习器
- `aqt/editor.py` - 编辑器
- `aqt/browser.py` - 浏览器
- `runanki.py` - 可执行脚本

### 启动器核心
- `launcher/src/main.rs` - 启动器主逻辑
- `launcher/src/platform/mod.rs` - 平台抽象
- `launcher/versions.py` - 版本管理
- `launcher/Cargo.toml` - Rust 项目配置

### 配置文件
- `pyproject.toml` - Python 包配置
- `hatch_build.py` - 构建钩子
- `launcher/pyproject.toml` - 启动器 Python 配置

### 界面组件
- `aqt/webview.py` - Web 视图封装
- `aqt/progress.py` - 进度对话框
- `aqt/preferences.py` - 偏好设置
- `aqt/theme.py` - 主题管理
- `aqt/stylesheets.py` - 样式表

### 多媒体支持
- `aqt/mpv.py` - MPV 播放器
- `aqt/sound.py` - 音频播放
- `aqt/tts.py` - 文本转语音
- `aqt/mediasrv.py` - 媒体服务

### 插件系统
- `aqt/addons.py` - 插件管理
- `aqt/gui_hooks.py` - 插件钩子

### 平台集成
- `launcher/src/platform/windows.rs` - Windows 平台
- `launcher/src/platform/mac.rs` - macOS 平台
- `launcher/src/platform/unix.rs` - Linux 平台
- `launcher/win/` - Windows 安装资源
- `launcher/mac/` - macOS 打包资源
- `launcher/lin/` - Linux 桌面集成

### 测试文件
- `tests/test_addons.py`
- `tests/test_i18n.py`

## 更新日志

- 2025-11-17: 增量更新，添加启动器详细信息、跨平台支持和部署管理
- 2025-06-17: 初始化模块文档，添加导航面包屑
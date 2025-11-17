# 应用程序启动器模块文档

[根目录](../../CLAUDE.md) > [qt](../) > **launcher**

## ✨ 导航面包屑
`[根目录](../../CLAUDE.md) > [qt](../) > **launcher**`

## 模块职责

应用程序启动器负责 Anki 的跨平台安装、部署和运行时管理：

- 跨平台应用程序启动和生命周期管理
- Python 环境管理和依赖解析
- 自动更新和版本检查
- 平台特定的系统集成（文件关联、菜单项等）
- 错误报告和诊断信息收集
- 安装包构建和分发包管理

## 入口和启动

- **主入口**: `src/main.rs` - 启动器主要逻辑
- **平台抽象**: `src/platform/` - 跨平台适配层
- **构建脚本**: `build.rs` - 构建时配置

### 启动流程
1. 环境检查和平台特定初始化
2. Python 环境检测和依赖管理
3. 版本检查和自动更新
4. 主应用程序进程启动
5. 错误监控和报告

## 外部接口

### 平台特定模块
- **Windows**: `src/platform/windows.rs` - Windows 特定功能
- **macOS**: `src/platform/mac.rs` - macOS 特定功能
- **Linux**: `src/platform/unix.rs` - Linux/Unix 特定功能

### 构建和打包
- **Windows**: `win/` - NSIS 安装程序和资源文件
- **macOS**: `mac/` - DMG 打包和代码签名
- **Linux**: `lin/` - AppImage/包管理器集成

### 工具和脚本
- **构建工具**: `src/bin/build_win.rs` - Windows 构建
- **控制台工具**: `src/bin/anki_console.rs` - 命令行接口

## 关键依赖和配置

### Rust 依赖
```toml
[dependencies]
anki_i18n = { workspace = true }
anki_io = { workspace = true }
anki_process = { workspace = true }
anyhow = "1.0.98"
```

### 构建依赖
- **Python**: `pyproject.toml` - Python 包配置
- **插件支持**: `addon/` - 插件包清单

## 数据模型

### 配置文件
- **包信息**: `addon/manifest.json` - 插件包信息
- **版本信息**: `versions.py` - 版本管理
- **Python 配置**: 用户和分发版 pyproject 文件

### 运行时状态
- **启动状态**: 包含版本、路径、环境信息
- **缓存管理**: UV 缓存和依赖缓存路径
- **同步状态**: 同步完成标记和触发器

## 平台集成

### Windows 集成
- **文件关联**: `win/fileassoc.nsh` - .apkg 文件关联
- **安装程序**: `win/anki.template.nsi` - NSIS 脚本
- **资源文件**: `win/anki-manifest.rc` - 应用程序资源
- **图标**: `win/anki-icon.ico` - 应用程序图标

### macOS 集成
- **DMG 打包**: `mac/dmg/` - 磁盘映像构建
- **代码签名**: `mac/notarize.sh` - 公证脚本
- **图标**: `mac/icon/` - 应用程序图标
- **权限**: `mac/entitlements.python.xml` - 应用程序权限

### Linux 集成
- **桌面集成**: `lin/anki.desktop` - 桌面文件
- **图标**: `lin/anki.png`, `lin/anki.xpm` - 图标文件
- **安装脚本**: `lin/install.sh` - 安装脚本
- **菜单项**: `lin/anki.xml` - 应用程序菜单

## 常见问题 (FAQ)

**Q: 启动器如何管理 Python 环境？**
A: 使用 UV 包管理器处理依赖，支持用户级别和分发版级别的 Python 环境。

**Q: 如何添加新平台支持？**
A: 在 `src/platform/` 目录下创建新的平台特定模块，实现必要的平台接口。

**Q: 更新机制如何工作？**
A: 启动器检查版本信息，支持增量更新和回滚机制。

**Q: 如何构建平台特定的安装包？**
A: 使用平台特定的构建脚本（Windows: build.bat, macOS: build.sh, Linux: build.sh）。

**Q: 错误报告如何处理？**
A: 启动器收集诊断信息，通过内置的错误报告系统发送到服务器。

## 相关文件列表

### 核心文件
- `src/main.rs` - 主启动逻辑
- `src/platform/mod.rs` - 平台抽象层
- `build.rs` - 构建脚本
- `pyproject.toml` - Python 包配置

### 平台特定代码
- `src/platform/windows.rs` - Windows 平台
- `src/platform/mac.rs` - macOS 平台
- `src/platform/unix.rs` - Linux/Unix 平台

### 构建和打包
- `win/anki.template.nsi` - Windows 安装程序
- `mac/build.sh` - macOS 构建
- `lin/install.sh` - Linux 安装脚本

### 资源文件
- `win/anki-icon.ico` - Windows 图标
- `mac/icon/` - macOS 图标
- `lin/anki.desktop` - Linux 桌面文件

### 配置和元数据
- `addon/manifest.json` - 插件包信息
- `versions.py` - 版本管理
- `Cargo.toml` - Rust 项目配置

## 更新日志

- 2025-11-17: 创建模块文档，添加导航面包屑和平台集成说明
# Anki 项目开发指南

## 项目概述

Anki 是一个跨平台的开源间隔重复记忆软件，该项目包含 Anki 桌面版的完整源代码。项目采用多语言混合架构：

- **Rust**: 核心库 (rslib)，提供数据模型、调度算法、同步等功能
- **Python**: Qt GUI 层 (qt)，负责用户界面和应用程序逻辑
- **TypeScript/Svelte**: 前端组件和编辑器界面 (ts)
- **C++**: 构建系统使用 Ninja/N2

项目使用工作区 (workspace) 结构管理多个 Rust crate，包括构建工具、国际化、协议缓冲区等组件。整体采用 AGPL-3.0 开源许可证。

## 架构组件

- `rslib`: Rust 核心库，包含卡片、笔记、牌组、调度器、同步、数据库等核心功能
- `qt`: Python Qt 界面层，提供桌面应用程序的图形界面
- `ts`: TypeScript/Svelte 前端，处理编辑器、审阅界面等 Web 组件
- `pylib`: Python 库，包含与 Rust 后端的桥接代码
- `build/`: 构建系统，使用 Rust 编写的 Ninja 生成器
- `ftl`: 国际化文件，支持多语言
- `proto`: 协议缓冲区定义，用于前后端通信

## 构建和运行

### 环境要求
- Rust (通过 rustup 安装，版本由 rust-toolchain.toml 指定)
- N2 或 Ninja 构建系统
- Python 3.9+
- Node.js 和 Yarn (用于前端)

### 构建命令
- `./run` (Linux/Mac) 或 `.\run` (Windows): 构建并运行开发版 Anki
- `./ninja check`: 运行所有测试
- `./ninja format`: 格式化代码
- `./ninja fix`: 修复 ruff/eslint 问题
- `./tools/build` (Linux/Mac) 或 `\tools\build.bat` (Windows): 构建可发布的 Python wheels

### 开发模式
- 使用 `./run` 启动非优化的开发构建（编译快但运行较慢）
- 使用 `./tools/runopt` 启动优化构建
- 设置 `ANKIDEV=1` 环境变量可启用开发模式（显示额外日志，禁用自动备份）

## 开发规范

- 代码格式化由 `./ninja format` 和 `./ninja fix` 处理
- 使用 Rust 的 Clippy 进行静态分析 (`cargo clippy --fix`)
- 测试通过 `./ninja check` 或 `cargo test` 运行
- 支持多语言，使用 FTL (Fluent) 进行国际化
- 遵循 Rust、Python、TypeScript 各自的社区规范和最佳实践

## 重要文件和目录

- `Cargo.toml`: Rust 工作区配置
- `package.json`: 前端依赖配置
- `pyproject.toml`: Python 项目配置
- `docs/`: 详细的开发文档
- `rslib/src/lib.rs`: Rust 核心库入口
- `qt/aqt/__init__.py`: Python Qt 应用入口
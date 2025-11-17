# 构建系统模块文档

[根目录](../../CLAUDE.md) > **build**

## ✨ 导航面包屑
`[根目录](../../CLAUDE.md) > **build**`

## 模块职责

构建系统模块负责 Anki 项目的自动化构建，包括：

- 跨平台构建配置和脚本
- 依赖管理和下载
- 代码生成和编译
- 测试执行和质量检查
- 打包和分发准备
- Ninja 构建文件生成

## 入口和启动

- **主运行器**: `runner/src/main.rs` - 构建系统的主要入口点
- **配置器**: `configure/src/main.rs` - 项目配置和环境检测
- **构建生成**: `ninja_gen/src/lib.rs` - Ninja 构建文件生成

### 构建流程
```
./ninja → runner → configure → ninja_gen → 构建文件 → 编译执行
```

## 外部接口

### 核心构建组件
- **Runner**: `runner/` - 主要构建执行器
- **Configure**: `configure/` - 项目配置和环境检测
- **Ninja Gen**: `ninja_gen/` - Ninja 构建文件生成器

### 构建命令
- **根目录命令**: `./ninja` - 调用构建系统
- **检查命令**: `./check` - 格式化和完整检查
- **快速检查**: `./check` 支持的子命令

## 关键依赖和配置

### Rust 工作空间成员
```toml
[workspace]
members = [
  "build/configure",
  "build/ninja_gen",
  "build/runner",
  "ftl",
  "pylib/rsbridge",
  "qt/launcher",
  "rslib",
  # ... 其他成员
]
```

### 构建工具
- **Ninja**: 快速构建系统
- **Cargo**: Rust 构建工具
- **Python**: 脚本执行和工具链
- **Node.js/Yarn**: 前端构建
- **Protobuf**: 跨语言代码生成

### 平台支持
- Windows (MSVC)
- macOS
- Linux
- 跨平台 CI/CD

## 构建特性

### 代码生成
- **Protobuf**: 自动生成 Rust/TypeScript/Python 绑定
- **国际化**: 从 FTL 文件生成类型安全的翻译 API
- **资源打包**: 嵌入资源文件
- **版本管理**: 自动版本号生成

### 优化配置
- **开发模式**: 快速增量编译
- **发布模式**: LTO 和优化编译
- **依赖缓存**: 减少重复构建时间
- **并行构建**: 多核 CPU 利用

### 质量检查
- **代码格式化**: Rust (`cargo fmt`), Python, TypeScript
- **静态分析**: Rust (`cargo clippy`), Python (`dmypy`)
- **测试执行**: 单元测试、集成测试
- **依赖检查**: 安全漏洞扫描

## 常见问题 (FAQ)

**Q: 如何触发完整构建？**
A: 运行根目录的 `./check` 命令，这会格式化代码并执行完整构建。

**Q: 构建失败如何调试？**
A: 查看构建日志，运行 `./check` 而不是手动 grep 搜索错误。

**Q: 如何添加新的构建目标？**
A: 在 `ninja_gen/src/` 中添加新的构建规则。

**Q: 依赖下载失败怎么办？**
A: 检查网络连接，构建系统会自动处理依赖下载和缓存。

**Q: 如何加速构建？**
A: 使用增量构建，避免修改 `.proto` 文件，利用缓存。

## 相关文件列表

### 核心模块
- `runner/src/main.rs` - 构建执行器
- `configure/src/main.rs` - 配置检测
- `ninja_gen/src/lib.rs` - 构建生成器

### 构建脚本
- `runner/src/` - 构建执行逻辑
- `configure/src/` - 环境检测和配置
- `ninja_gen/src/` - 构建规则定义

### 工具和脚本
- `runner/src/build.rs` - 构建命令处理
- `ninja_gen/src/build.rs` - 构建规则
- `ninja_gen/src/cargo.rs` - Cargo 集成
- `ninja_gen/src/python.rs` - Python 集成
- `ninja_gen/src/node.rs` - Node.js 集成

### 配置文件
- 各子模块的 `Cargo.toml`
- 构建配置文件
- 平台特定配置

## 构建命令参考

### 主要命令
```bash
# 完整构建和检查
./check

# 调用构建系统
./ninja <target>

# 快速检查特定组件
cargo check                    # Rust
./tools/dmypy                 # Python
./ninja check:svelte          # TypeScript/Svelte
```

### 开发工作流
1. 修改代码
2. 运行快速检查命令
3. 完成后运行 `./check` 验证
4. 提交代码

## 更新日志

- 2025-06-17: 初始化模块文档，添加导航面包屑
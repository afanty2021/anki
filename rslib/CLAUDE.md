# Rust 核心库模块文档

[根目录](../../CLAUDE.md) > **rslib**

## ✨ 导航面包屑
`[根目录](../../CLAUDE.md) > **rslib**`

## 模块职责

Rust 核心库是 Anki 的性能关键组件，负责：

- 核心业务逻辑和数据处理
- 数据库操作和集合管理
- 调度算法（FSRS）实现
- 跨语言服务的 Protobuf 接口
- 高性能的计算密集型操作
- 音视频处理和图像遮挡功能
- 网络同步和通信

## 入口和启动

- **库入口**: `src/lib.rs` - 模块导出和公共接口
- **服务层**: `src/services.rs` - Protobuf 服务实现
- **后端接口**: `src/backend/mod.rs` - 主要后端服务

### 核心架构
```
前端应用 → Protobuf → Backend Services → Core Logic → Database
```

## 外部接口

### 核心服务模块
- **后端服务**: `src/backend/mod.rs` - 主要后端 API 实现
- **集合服务**: `src/collection/mod.rs` - 数据库集合操作
- **卡片服务**: `src/card/mod.rs` - 卡片管理
- **调度服务**: `src/scheduler/` - 学习算法实现

### 后端服务详细模块
- **添加服务**: `src/backend/adding.rs` - 卡片添加操作
- **同步服务**: `src/backend/sync.rs` - 数据同步功能
- **导入导出**: `src/backend/import_export.rs` - 数据格式转换
- **卡片渲染**: `src/backend/card_rendering.rs` - 卡片显示处理
- **配置管理**: `src/backend/config.rs` - 系统配置
- **国际化**: `src/backend/i18n.rs` - 多语言支持
- **错误处理**: `src/backend/error.rs` - 统一错误管理
- **数据库代理**: `src/backend/dbproxy.rs` - 数据库操作封装

### 调度系统架构
- **调度器核心**: `src/scheduler/mod.rs` - 调度器主模块
- **FSRS 算法**: `src/scheduler/fsrs/` - Free Spaced Repetition Scheduler
  - `fsrs/mod.rs` - FSRS 算法核心
  - `fsrs/memory_state.rs` - 记忆状态管理
  - `fsrs/params.rs` - 参数优化
  - `fsrs/rescheduler.rs` - 重新调度逻辑
  - `fsrs/retention.rs` - 保持率计算
  - `fsrs/simulator.rs` - 调度模拟器
- **答题状态**: `src/scheduler/answering/` - 答题逻辑处理
  - `answering/current.rs` - 当前卡片答题
  - `answering/learning.rs` - 学习阶段处理
  - `answering/review.rs` - 复习阶段处理
  - `answering/relearning.rs` - 重新学习处理
  - `answering/preview.rs` - 预览模式
- **队列管理**: `src/scheduler/queue/` - 卡片队列系统
  - `queue/main.rs` - 主队列
  - `queue/learning.rs` - 学习队列
  - `queue/builder/` - 队列构建器
- **状态管理**: `src/scheduler/states/` - 调度状态处理
- **服务层**: `src/scheduler/service/` - 调度服务接口

### 数据处理模块
- **导入导出**: `src/import_export/` - 数据格式转换
- **搜索功能**: `src/search.rs` - 数据库搜索
- **查找替换**: `src/findreplace.rs` - 批量编辑

### 功能模块
- **牌组管理**: `src/decks/mod.rs` - 牌组操作
- **笔记管理**: `src/notes.rs` - 笔记处理
- **模板处理**: `src/template.rs` - 卡片模板渲染
- **配置管理**: `src/config/` - 系统配置
- **错误处理**: `src/error/mod.rs` - 统一错误类型

### 扩展功能
- **图像遮挡**: `src/image_occlusion/` - 图像遮罩功能
- **LaTeX 渲染**: `src/latex.rs` - 数学公式处理
- **媒体管理**: `src/media.rs` - 媒体文件处理
- **TTS 支持**: `src/card_rendering/tts/` - 文本转语音

## 关键依赖和配置

### 主要依赖
```toml
[dependencies]
# 数据库和存储
rusqlite = { version = "0.36.0", features = ["trace", "functions", "collation", "bundled"] }

# 序列化
serde = { version = "1.0.219", features = ["derive"] }
serde_json = "1.0.140"

# 异步运行时
tokio = { version = "1.45", features = ["fs", "rt-multi-thread", "macros", "signal"] }

# Web 服务
axum = { version = "0.8.4", features = ["multipart", "macros"] }
reqwest = { version = "0.12.20", default-features = false, features = ["json", "socks", "stream", "multipart"] }

# Protobuf
prost = "0.13"

# 调度算法
fsrs = "5.1.0"

# 错误处理
snafu = "0.8.6"
anyhow = "1.0.98"

# 性能优化
rayon = "1.10.0"
blake3 = "1.8.2"
```

### 构建配置
- **Cargo 配置**: `Cargo.toml`
- **构建脚本**: `build.rs`
- **工作空间**: 根目录工作空间成员
- **特性标志**: `bench`, `rustls`, `native-tls`

## 数据模型

### 核心数据结构
- **Collection**: 数据库集合，包含所有学习数据
- **Card**: 学习卡片，包含调度信息和内容
- **Note**: 笔记，包含字段和元数据
- **Deck**: 牌组，包含配置和统计
- **DeckConfig**: 牌组配置，包含学习参数

### Protobuf 服务
- **BackendService**: 主要后端服务
- **CollectionService**: 集合操作服务
- **其他服务**: 通过 `proto_gen` 自动生成

### 配置系统
- **系统配置**: `src/config/`
- **版本兼容**: `src/version.rs`
- **时间戳**: `src/timestamp.rs`

### FSRS 调度数据
- **MemoryState**: 记忆状态和稳定性
- **FSRSParams**: 调度算法参数
- **RetentionData**: 保持率历史数据
- **SchedulingState**: 卡片调度状态

## 测试和质量

### 测试结构
- **单元测试**: 各模块中的 `#[cfg(test)]` 测试
- **集成测试**: `src/tests.rs`
- **性能测试**: `bench.sh` 脚本
- **测试数据**: `tests/support/` 目录

### 测试覆盖领域
- 集合操作和数据库交互
- 调度算法正确性（特别是 FSRS）
- 导入导出功能
- 同步机制
- 错误处理路径
- 后端服务接口
- 跨平台兼容性

### 代码质量
- 严格的编译时检查 (`#![deny(unused_must_use)]`)
- 统一错误处理 (`error/mod.rs`)
- 代码格式化: `cargo fmt`
- 静态分析: `cargo clippy`

## 常见问题 (FAQ)

**Q: Rust 层如何暴露给其他语言使用？**
A: 通过 Protobuf 定义服务接口，使用 `prost-build` 生成跨语言绑定。

**Q: FSRS 算法如何集成到调度系统中？**
A: FSRS 作为默认调度算法，集成在 `src/scheduler/fsrs/` 模块中，提供科学的间隔重复计算。

**Q: 后端服务架构如何设计？**
A: 采用模块化设计，每个服务模块（adding, sync, import_export 等）负责特定功能领域。

**Q: 如何添加新的业务功能？**
A: 在相应模块中实现 Rust 逻辑，然后在 `src/backend/` 中添加 Protobuf 服务方法。

**Q: 数据库操作如何优化？**
A: 使用 SQLite 的 `bundled` 特性，配合 `rusqlite` 的编译时优化和连接池。

**Q: 调度系统如何处理不同的学习状态？**
A: 通过状态机模式，管理卡片在学习、复习、重新学习等不同阶段的状态转换。

**Q: 如何处理并发和异步操作？**
A: 使用 Tokio 异步运行时，配合 `rayon` 进行并行计算。

## 相关文件列表

### 核心文件
- `src/lib.rs` - 库入口
- `src/services.rs` - 服务层
- `src/backend/mod.rs` - 后端服务
- `rust_interface.rs` - Rust 接口生成

### 后端服务模块
- `src/backend/adding.rs` - 添加服务
- `src/backend/sync.rs` - 同步服务
- `src/backend/import_export.rs` - 导入导出
- `src/backend/card_rendering.rs` - 卡片渲染
- `src/backend/config.rs` - 配置管理
- `src/backend/i18n.rs` - 国际化
- `src/backend/error.rs` - 错误处理
- `src/backend/dbproxy.rs` - 数据库代理

### 调度系统
- `src/scheduler/mod.rs` - 调度器核心
- `src/scheduler/fsrs/` - FSRS 算法模块
- `src/scheduler/answering/` - 答题逻辑
- `src/scheduler/queue/` - 队列管理
- `src/scheduler/states/` - 状态管理
- `src/scheduler/service/` - 调度服务

### 数据管理
- `src/collection/mod.rs` - 集合操作
- `src/card/mod.rs` - 卡片管理
- `src/decks/mod.rs` - 牌组管理
- `src/notes.rs` - 笔记处理

### 功能模块
- `src/import_export/` - 导入导出
- `src/search.rs` - 搜索功能
- `src/template.rs` - 模板处理
- `src/config/` - 配置管理

### 扩展功能
- `src/image_occlusion/` - 图像遮挡
- `src/latex.rs` - LaTeX 渲染
- `src/media.rs` - 媒体管理
- `src/card_rendering/tts/` - 文本转语音

### 工具和支持
- `src/error/mod.rs` - 错误处理
- `src/utils.rs` - 工具函数 (通过 prelude)
- `src/version.rs` - 版本管理
- `src/timestamp.rs` - 时间处理

### 构建和配置
- `Cargo.toml`
- `build.rs`
- `bench.sh`

### 测试文件
- `src/tests.rs`
- `tests/support/`

## 更新日志

- 2025-11-17: 增量更新，添加详细的后端服务和调度系统架构说明
- 2025-06-17: 初始化模块文档，添加导航面包屑
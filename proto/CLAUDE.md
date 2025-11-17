# Protobuf 接口定义模块文档

[根目录](../CLAUDE.md) > **proto**

## ✨ 导航面包屑
`[根目录](../CLAUDE.md) > **proto**`

## 模块职责

Protobuf 模块定义了 Anki 各层之间的通信接口，负责：

- 跨语言服务接口定义（Rust ↔ Python ↔ TypeScript）
- 数据库存储结构规范
- 前端与后端通信协议
- API 版本管理和兼容性
- 服务方法签名和消息格式

## 入口和启动

- **核心定义**: `anki/` 目录包含所有 .proto 文件
- **接口入口**: `backend.proto` - 主要后端服务接口
- **服务构建**: 通过 build 系统自动生成跨语言绑定

## 外部接口

### 核心服务协议
- **backend.proto**: 主要后端服务接口和错误定义
- **collection.proto**: 集合操作相关服务
- **scheduler.proto**: 调度算法相关接口
- **sync.proto**: 同步功能通信协议

### 数据模型定义
- **cards.proto**: 卡片数据结构
- **notes.proto**: 笔记数据结构
- **decks.proto**: 牌组数据结构
- **config.proto**: 配置相关结构
- **search.proto**: 搜索功能接口

### 功能模块协议
- **card_rendering.proto**: 卡片渲染接口
- **import_export.proto**: 导入导出功能
- **media.proto**: 媒体文件处理
- **i18n.proto**: 国际化支持
- **stats.proto**: 统计数据接口

### 平台特定接口
- **ankidroid.proto**: AnkiDroid 特定功能
- **ankihub.proto**: AnkiHub 服务集成
- **ankiweb.proto**: AnkiWeb 服务通信
- **image_occlusion.proto**: 图像遮挡功能

### 通用工具
- **generic.proto**: 通用数据类型
- **links.proto**: 链接和引用定义
- **deck_config.proto**: 牌组配置
- **notetypes.proto**: 笔记类型定义
- **tags.proto**: 标签管理

## 关键依赖和配置

### 工具链依赖
- **Protocol Buffers**: protobuf 编译器
- **Prost**: Rust 代码生成
- **Build 系统**: 自动生成跨语言绑定

### 生成目标
- **Rust 绑定**: `out/` 目录下的 Rust 代码
- **Python 绑定**: pylib 中的生成代码
- **TypeScript 绑定**: ts 中的生成代码

## 数据模型

### 主要消息类型
- **BackendError**: 统一错误处理
- **Progress**: 进度报告机制
- **Collection**: 数据库集合结构
- **Card**: 学习卡片定义
- **Note**: 笔记数据结构
- **Deck**: 牌组定义

### 服务接口模式
- 每个服务定义 RPC 方法
- 请求/响应消息结构
- 流式处理支持（部分接口）
- 错误处理和状态返回

## 常见问题 (FAQ)

**Q: 如何修改现有的 Protobuf 接口？**
A: 编辑相应的 .proto 文件，然后运行 `./check` 重新生成绑定代码。

**Q: 如何添加新的服务方法？**
A: 在相应服务的 .proto 文件中添加 rpc 定义，确保消息结构完整。

**Q: 版本兼容性如何管理？**
A: 通过 protobuf 的向后兼容特性，谨慎修改现有字段。

**Q: 生成的代码位于哪里？**
A: 自动生成的代码位于 `out/` 目录，按语言分类组织。

**Q: 如何验证 Protobuf 定义？**
A: 使用 `./check` 构建命令会验证 protobuf 定义的完整性。

## 相关文件列表

### 核心协议文件
- `anki/backend.proto` - 主要后端服务
- `anki/collection.proto` - 集合操作
- `anki/scheduler.proto` - 调度接口

### 数据模型文件
- `anki/cards.proto` - 卡片定义
- `anki/notes.proto` - 笔记定义
- `anki/decks.proto` - 牌组定义
- `anki/config.proto` - 配置结构

### 功能模块文件
- `anki/card_rendering.proto` - 渲染接口
- `anki/import_export.proto` - 导入导出
- `anki/media.proto` - 媒体处理
- `anki/sync.proto` - 同步功能

### 通用工具文件
- `anki/generic.proto` - 通用类型
- `anki/links.proto` - 链接定义
- `anki/frontend.proto` - 前端接口

### 平台特定文件
- `anki/ankidroid.proto` - AnkiDroid
- `anki/ankihub.proto` - AnkiHub
- `anki/ankiweb.proto` - AnkiWeb

### 文档
- `README.md` - 说明文档

## 更新日志

- 2025-11-17: 创建模块文档，添加导航面包屑和接口定义说明
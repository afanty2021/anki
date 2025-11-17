# 国际化 (FTL) 模块文档

[根目录](../../CLAUDE.md) > **ftl**

## ✨ 导航面包屑
`[根目录](../../CLAUDE.md) > **ftl**`

## 模块职责

FTL (Fluent Translation List) 模块负责 Anki 项目的国际化，包括：

- 多语言翻译文件管理
- 类型安全的翻译 API 生成
- 翻译字符串的提取和处理
- 跨语言翻译一致性维护
- 翻译工具和脚本

## 入口和启动

- **翻译目录**: `core/` - 核心功能翻译
- **Qt 翻译**: `qt/` - Qt 界面特定翻译
- **工具脚本**: 各种翻译处理脚本

### 核心架构
```
FTL 文件 → rslib/i18n → Rust API
FTL 文件 → 生成器 → TypeScript/Python API
```

## 外部接口

### 翻译文件结构
- **核心翻译**: `core/` - 跨平台通用功能
- **Qt 翻译**: `qt/` - Qt 界面特定功能
- **翻译分类**: 按功能模块组织翻译文件

### 主要翻译类别
- `adding.ftl` - 添加卡片相关
- `browsing.ftl` - 浏览器功能
- `studying.ftl` - 学习和复习
- `preferences.ftl` - 设置和配置
- `sync.ftl` - 同步功能
- `media.ftl` - 媒体相关

## 关键依赖和配置

### 构建配置
- **Cargo 配置**: `Cargo.toml`
- **Rust 集成**: `rslib/i18n` 模块
- **代码生成**: 自动生成类型安全 API

### 翻译工具
- `ftl` - Fluent 编译器
- `copy-core-string.sh` - 字符串复制工具
- `remove-unused.sh` - 清理未使用翻译
- `update-anki*-usage.sh` - 使用情况更新

## 翻译系统特性

### 类型安全
- 编译时翻译键检查
- 参数类型验证
- 缺失翻译检测

### 多语言支持
- 支持复数形式
- 变量插值
- 条件翻译
- 富文本支持

### 工具链
- 自动翻译提取
- 翻译一致性检查
- 使用情况分析

## 翻译文件规范

### 命名约定
- 使用 kebab-case 命名
- 功能模块分组
- 层次化组织

### 翻译原则
- 优先使用 `core/` 翻译
- Qt 特定功能使用 `qt/`
- 保持翻译风格一致性
- 遵循现有翻译模式

### 参数规范
```fluent
welcome-back = { $username }，欢迎回来！
cards-count = { $count ->
    [one] { $count } 张卡片
    *[other] { $count } 张卡片
}
```

## 常见问题 (FAQ)

**Q: 如何添加新的翻译字符串？**
A: 确定合适的功能模块，在对应的 `.ftl` 文件中添加翻译。

**Q: 核心翻译和 Qt 翻译如何选择？**
A: 除非是 Qt 界面特定功能，否则优先使用 `core/` 翻译。

**Q: 如何处理复数形式？**
A: 使用 Fluent 的复数选择器语法，参考现有翻译文件。

**Q: 翻译 API 如何使用？**
A: 构建系统会自动生成类型安全的 API，在各语言模块中导入使用。

**Q: 如何检查未使用的翻译？**
A: 运行 `remove-unused.sh` 脚本清理未使用的翻译。

## 相关文件列表

### 核心翻译文件
- `core/adding.ftl`
- `core/browsing.ftl`
- `core/studying.ftl`
- `core/preferences.ftl`
- `core/sync.ftl`
- `core/media.ftl`

### 功能特定翻译
- `core/card-stats.ftl` - 卡片统计
- `core/decks.ftl` - 牌组管理
- `core/actions.ftl` - 操作按钮
- `core/errors.ftl` - 错误信息
- `core/help.ftl` - 帮助文档

### Qt 特定翻译
- `qt/` 目录下的 Qt 界面特定翻译

### 工具脚本
- `copy-core-string.sh`
- `remove-unused.sh`
- `update-ankidroid-usage.sh`
- `update-ankimobile-usage.sh`

### 配置文件
- `Cargo.toml`
- `README.md`

## 翻译工作流程

### 添加新翻译
1. 确定功能模块和翻译文件
2. 添加英文翻译键和内容
3. 运行构建验证
4. 更新各语言翻译（如需要）

### 维护翻译
1. 定期运行清理脚本
2. 检查翻译使用情况
3. 更新过时的翻译
4. 保持翻译一致性

### 翻译 API 使用
```rust
// Rust
use anki_i18n::I18n;
let tr = i18n.tr("welcome-back", &[]);
```

```typescript
// TypeScript
import { tr } from "@generated/i18n";
const message = tr("welcome-back", {});
```

## 更新日志

- 2025-06-17: 初始化模块文档，添加导航面包屑
# TypeScript/Svelte 前端模块文档

[根目录](../../CLAUDE.md) > **ts**

## ✨ 导航面包屑
`[根目录](../../CLAUDE.md) > **ts**`

## 模块职责

TypeScript/Svelte 模块负责 Anki 的 Web 前端开发，包括：

- Web 组件库开发和维护
- 用户界面的交互逻辑
- 与 Rust 后端的通信
- 样式和主题管理
- 前端路由和页面管理
- 跨语言通信的 TypeScript 绑定

## 入口和启动

- **主配置**: `tsconfig.json`, `vite.config.ts`
- **构建脚本**: `bundle_ts.mjs`, `bundle_svelte.mjs`
- **Svelte 配置**: `svelte.config.js`
- **依赖管理**: `yarn.sh`

## 外部接口

### 主要目录结构
- `src/`: 源代码目录
- `lib/`: 共享库和工具函数
- `routes/`: 页面路由组件
- `reviewer/`: 复习器相关组件
- `lib/generated/`: 生成的跨语言通信代码

### 生成的代码模块
- **通信层**: `lib/generated/post.ts` - Protobuf 通信封装
- **国际化**: `lib/generated/ftl-helpers.ts` - Fluent 翻译助手
- **后端绑定**: `@generated/backend` - Rust 后端类型绑定

### 关键文件
- `ts/src/app.html`: 主应用模板
- `ts/src/app.d.ts`: 类型定义
- `ts/src/hooks.client.js`: 客户端钩子

## 关键依赖和配置

- **构建工具**: Vite, TypeScript
- **UI 框架**: Svelte
- **包管理**: Yarn
- **依赖更新**: `./update.sh`
- **添加依赖**: `./add.sh -D <package>`

### 构建配置详解
- **TypeScript**: 严格模式，路径映射，ES2022 目标
- **Vite**: 开发服务器，热重载，生产优化
- **Svelte**: 预处理器配置，编译选项
- **ESLint**: 代码质量检查，TypeScript 集成

## 数据模型

### 跨语言通信架构
前端通过三层通信机制与后端交互：
1. **Protobuf 接口**: 定义在 `proto/` 目录，自动生成类型绑定
2. **HTTP 通信**: `post.ts` 提供类型安全的二进制通信
3. **翻译系统**: `ftl-helpers.ts` 提供多语言支持

### 生成的类型绑定
- Rust 后端服务通过 `@generated/backend` 模块暴露
- Protobuf 消息自动转换为 TypeScript 类型
- 保持与 Rust 层的类型一致性

### 国际化支持
- Fluent 翻译系统集成
- 动态语言包加载
- 类型安全的翻译键值访问

## 测试和质量

### 测试文件覆盖
- `html-filter/index.test.ts` - HTML 过滤功能测试
- `lib/domlib/surround/*.test.ts` - DOM 操作测试
- `lib/tslib/time.test.ts` - 时间处理工具测试
- `reviewer/lib.test.ts` - 复习器核心逻辑测试
- `routes/*/lib.test.ts` - 路由组件测试

### 质量检查工具
- **TypeScript**: 严格类型检查，`./ninja check:svelte`
- **ESLint**: `.eslintrc.cjs` 配置的代码风格检查
- **Svelte**: 组件编译检查和警告
- **代码格式化**: 通过根目录的 `./check` 统一格式化

### 性能优化
- **代码分割**: Vite 自动分割和懒加载
- **树摇优化**: 未使用代码自动移除
- **压缩优化**: 生产环境自动压缩
- **缓存策略**: 长期缓存友好的文件名

## 开发工作流程

### 前端开发流程
1. **环境准备**: `yarn install` 安装依赖
2. **开发模式**: `./ninja dev` 启动开发服务器
3. **组件开发**: 在相应目录创建 Svelte 组件
4. **样式开发**: 使用 Svelte 样式系统
5. **类型定义**: 利用 TypeScript 类型系统
6. **测试编写**: 为新功能编写测试用例
7. **代码检查**: 运行 `./check` 进行质量检查

### 跨语言集成开发
1. **接口定义**: 在 `proto/` 定义新的 Protobuf 服务
2. **类型生成**: 运行构建生成 TypeScript 绑定
3. **前端集成**: 使用生成的类型和服务接口
4. **测试验证**: 确保跨语言通信正确性

### 国际化开发
1. **翻译键**: 在 `ftl/` 目录添加新的翻译键
2. **类型生成**: 自动生成类型安全的翻译 API
3. **前端使用**: 通过 `ftl-helpers.ts` 访问翻译
4. **多语言测试**: 验证不同语言的显示效果

## 常见问题 (FAQ)

**Q: 如何添加新的前端依赖？**
A: 使用 `./add.sh -D <package-name>` 命令添加开发依赖，确保依赖兼容性。

**Q: 如何更新所有依赖？**
A: 运行 `./update.sh` 脚本，然后测试兼容性。

**Q: 前端如何与后端通信？**
A: 通过 `@generated/backend` 模块和 `lib/generated/post.ts`，使用类型安全的 Protobuf 通信。

**Q: 如何添加新的翻译支持？**
A: 在 `ftl/` 目录添加翻译文件，构建系统会自动生成类型绑定。

**Q: 构建失败怎么办？**
A: 首先运行根目录的 `./check` 命令进行完整检查，查看具体错误信息。

**Q: 如何优化前端性能？**
A: 使用 Vite 的代码分割，懒加载组件，优化资源打包。

**Q: 如何调试跨语言通信问题？**
A: 检查 Protobuf 定义一致性，查看生成的类型文件，使用浏览器开发者工具。

**Q: 如何编写前端测试？**
A: 使用现有测试模式，为组件和工具函数编写单元测试。

## 相关文件列表

### 配置文件
- `tsconfig.json` - TypeScript 配置
- `tsconfig_legacy.json` - 兼容性配置
- `vite.config.ts` - Vite 构建配置
- `svelte.config.js` - Svelte 编译配置
- `.eslintrc.cjs` - ESLint 代码检查配置
- `yarn.sh` - 包管理脚本
- `licenses.json` - 许可证信息

### 源代码目录
- `src/` - 主要源代码
- `lib/` - 共享库和工具
- `routes/` - 页面路由组件
- `reviewer/` - 复习器组件

### 生成代码
- `lib/generated/post.ts` - Protobuf 通信封装
- `lib/generated/ftl-helpers.ts` - 国际化助手
- `lib/generated/README.md` - 生成代码说明

### 构建相关
- `bundle_ts.mjs` - TypeScript 打包脚本
- `bundle_svelte.mjs` - Svelte 打包脚本
- `transform_ts.mjs` - TypeScript 转换
- `page.html` - 应用页面模板

### 测试文件
- `html-filter/index.test.ts`
- `lib/domlib/surround/*.test.ts`
- `lib/tslib/time.test.ts`
- `reviewer/lib.test.ts`
- `routes/*/lib.test.ts`

## 更新日志

- 2025-11-17: 深度补充更新，添加生成代码分析、跨语言通信架构、开发工作流程、质量工具配置
- 2025-06-17: 初始化模块文档，添加导航面包屑
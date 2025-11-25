# Implementation Plan: 能力刻度尺核心功能

**Branch**: `001-skill-tracker-core` | **Date**: 2025-11-25 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-skill-tracker-core/spec.md`

## Summary

构建一个纯前端的技能追踪与成长可视化系统，支持多职业角色、5级技能进阶、实时进度追踪、练习日志记录和本地数据持久化。采用 React 18 + Vite + Tailwind CSS 技术栈，所有数据存储在浏览器 localStorage 中，实现完全离线可用的个人能力管理工具。

## Technical Context

**Language/Version**: JavaScript (ES2022+) / TypeScript (可选，建议后期引入)
**Primary Dependencies**: 
- React 18.2+
- React DOM 18.2+
- Vite 5.0+
- Tailwind CSS 3.4+

**Storage**: localStorage (初期) / IndexedDB (未来扩展)
**Testing**: Vitest + React Testing Library
**Target Platform**: Modern Browsers (Chrome 100+, Safari 15+, Edge 100+)
**Project Type**: Single Page Application (SPA)
**Performance Goals**: 
- 首屏加载 < 2s (3G)
- 交互响应 < 100ms
- 打包体积 < 500KB (gzipped)

**Constraints**: 
- 完全前端运行，无后端依赖
- localStorage 限制 5-10MB
- 必须支持数据导入/导出
- 必须支持离线使用

**Scale/Scope**: 
- 2个职业角色
- 3个技能
- 每个技能5个等级
- 预计支持 100+ 条日志记录

## Constitution Check

✅ **简洁至上 (Simplicity First)**
- 使用 React 18 + Vite，无额外状态管理库
- 组件数量控制在 15 个以内
- 依赖库仅限必需项（React、ReactDOM、Tailwind）

✅ **组件化设计 (Component-Driven)**
- 所有 UI 元素拆分为可复用组件
- 使用 Props 明确定义组件接口
- 状态管理遵循就近原则

✅ **数据持久化优先 (Data Persistence First)**
- 所有用户操作实时同步到 localStorage
- 实现数据版本控制机制
- 提供数据导入/导出功能

✅ **技术栈约束**
- ✅ React 18 (函数组件 + Hooks)
- ✅ Vite 构建工具
- ✅ Tailwind CSS
- ✅ localStorage 存储
- ❌ 无状态管理库（全局状态 < 10 个）
- ❌ 无 UI 组件库
- ❌ 无后端服务

## Project Structure

### Documentation (this feature)

```text
specs/001-skill-tracker-core/
├── plan.md              # 本文件
├── spec.md              # 功能规格说明
├── data-model.md        # 数据模型设计
├── quickstart.md        # 快速开始指南
├── contracts/           # API 契约（localStorage schema）
│   └── storage-schema.json
└── tasks.md             # 任务分解（后续创建）
```

### Source Code (repository root)

```text
skill-tracker/
├── public/              # 静态资源
│   └── favicon.ico
│
├── src/
│   ├── main.jsx         # 应用入口
│   ├── App.jsx          # 根组件
│   │
│   ├── components/      # UI 组件
│   │   ├── Dashboard.jsx          # 主仪表盘
│   │   ├── RoleNavigator.jsx      # 职业角色导航
│   │   ├── SkillCard.jsx          # 技能卡片
│   │   ├── LevelCard.jsx          # 等级卡片
│   │   ├── ChecklistItem.jsx      # 验收标准项
│   │   ├── ProgressBar.jsx        # 进度条
│   │   ├── DetailView.jsx         # 等级详情页
│   │   ├── TrainingLog.jsx        # 练习日志
│   │   └── MetadataPanel.jsx      # 元数据面板
│   │
│   ├── hooks/           # 自定义 Hooks
│   │   ├── useLocalStorage.js     # localStorage 封装
│   │   ├── useSkillProgress.js    # 技能进度计算
│   │   └── useDataMigration.js    # 数据版本迁移
│   │
│   ├── data/            # 静态数据
│   │   ├── careerRoles.js         # 职业角色定义
│   │   └── initialSkills.js       # 初始技能数据
│   │
│   ├── utils/           # 工具函数
│   │   ├── storage.js             # localStorage 工具
│   │   ├── dataValidation.js      # 数据验证
│   │   └── exportImport.js        # 导入导出工具
│   │
│   └── styles/          # 样式文件
│       └── index.css              # Tailwind 入口
│
├── tests/               # 测试文件
│   ├── components/      # 组件测试
│   ├── hooks/           # Hooks 测试
│   └── utils/           # 工具函数测试
│
├── index.html           # HTML 入口
├── package.json         # 依赖配置
├── vite.config.js       # Vite 配置
├── tailwind.config.js   # Tailwind 配置
└── postcss.config.js    # PostCSS 配置
```

**Structure Decision**: 采用单项目结构（Option 1），因为这是纯前端 SPA 应用，无需前后端分离。所有组件、Hooks、工具函数都在 `src/` 目录下按职责清晰分类。

## Complexity Tracking

无违反项 - 所有设计均符合宪章约束。

## Implementation Phases

### Phase 0: Research & Setup (研究与环境准备)

**目标**: 验证技术栈可行性，搭建开发环境

**关键调研点**:
1. Vite 5.0 最佳实践和配置方案
2. React 18 Concurrent Features 使用建议
3. localStorage 容量限制和性能特征
4. Tailwind CSS 在 Vite 中的集成方式
5. React Testing Library + Vitest 测试配置

**输出文档**: `research.md`

**验收标准**:
- ✅ 创建 Vite + React 项目模板
- ✅ 配置 Tailwind CSS
- ✅ 验证 localStorage 读写性能
- ✅ 搭建基础测试环境

### Phase 1: Data Model & Architecture (数据模型与架构设计)

**目标**: 设计清晰的数据结构和组件架构

**关键设计点**:
1. **数据模型设计** (`data-model.md`)
   - CareerRole 结构
   - Skill 结构（5 级嵌套）
   - Criteria 和 Log 结构
   - localStorage Schema 版本控制

2. **组件架构设计**
   - 组件树层级关系
   - Props 接口定义
   - 状态提升策略
   - 数据流向图

3. **localStorage 契约** (`contracts/storage-schema.json`)
   - 数据存储键名规范
   - 数据格式定义
   - 版本迁移策略

**输出文档**: 
- `data-model.md`
- `contracts/storage-schema.json`
- `quickstart.md`

**验收标准**:
- ✅ 数据模型完整定义并有示例数据
- ✅ 组件树设计清晰，职责明确
- ✅ localStorage Schema 包含版本号
- ✅ Quickstart 指南可供开发参考

### Phase 2: Core UI Components (核心 UI 组件实现)

**目标**: 实现核心 UI 组件，建立组件库

**实现任务**:
1. 基础组件
   - ProgressBar - 进度条组件
   - ChecklistItem - 可勾选的验收标准项
   - SkillCard - 技能卡片（展示单个技能信息）

2. 布局组件
   - RoleNavigator - 左侧职业角色导航
   - Dashboard - 主仪表盘布局
   - MetadataPanel - 元数据展示面板

3. 复杂组件
   - LevelCard - 等级卡片（包含多个 ChecklistItem）
   - DetailView - 等级详情页
   - TrainingLog - 练习日志组件

**技术要点**:
- 所有组件使用函数式 + Hooks
- Props 严格类型检查（建议加 PropTypes）
- 响应式设计（mobile-first）
- 无障碍支持（ARIA 标签）

**验收标准**:
- ✅ 所有组件独立可测试
- ✅ Props 接口文档完整
- ✅ 响应式布局在移动端正常显示
- ✅ 单元测试覆盖率 > 60%

### Phase 3: State Management & Data Flow (状态管理与数据流)

**目标**: 实现应用状态管理和数据持久化

**实现任务**:
1. 自定义 Hooks
   - `useLocalStorage` - localStorage 封装，自动序列化/反序列化
   - `useSkillProgress` - 技能进度计算逻辑
   - `useDataMigration` - 数据版本迁移逻辑

2. 状态管理
   - App 级别状态：当前角色、当前技能
   - 技能数据状态：所有技能的完成情况
   - UI 状态：视图模式（dashboard/detail）

3. 数据持久化
   - 实时同步到 localStorage
   - 防抖优化（避免频繁写入）
   - 异常处理（配额超限、权限问题）

**技术要点**:
- 使用 React Context（仅限必要的全局状态）
- localStorage 写入采用 debounce 策略
- 实现数据校验和容错机制

**验收标准**:
- ✅ 所有用户操作实时保存
- ✅ 关闭浏览器后数据完整恢复
- ✅ localStorage 异常时有友好提示
- ✅ 单元测试覆盖核心 Hooks

### Phase 4: User Interactions & Features (用户交互与功能实现)

**目标**: 实现所有用户故事的交互功能

**实现任务**:
1. **US-1: 技能进度查看与管理**
   - 角色选择 → 技能列表展示
   - 验收标准勾选/取消勾选
   - 进度实时计算和显示
   - 等级自动解锁逻辑

2. **US-2: 练习日志记录与查看**
   - 日志输入框（支持 Ctrl+Enter）
   - 日志列表展示（时间倒序）
   - 日志计数徽章

3. **US-3: 职业角色切换**
   - 左侧导航点击切换
   - 右侧内容区平滑过渡
   - 进度数据独立计算

4. **US-4: 数据持久化**
   - 自动保存机制
   - 数据版本迁移
   - 导入/导出功能

5. **US-5: 元数据查看**
   - 技能元信息展示
   - 支撑技能、工具生态显示

**技术要点**:
- 交互动画使用 CSS Transition
- 表单验证（日志长度限制 5000 字符）
- 防止 XSS（使用 textContent 或 React 自动转义）

**验收标准**:
- ✅ 所有 User Story 的 Acceptance Scenarios 通过
- ✅ E2E 测试覆盖关键路径
- ✅ 无控制台错误或警告

### Phase 5: Data Security & Error Handling (数据安全与错误处理)

**目标**: 实现安全措施和完善的错误处理

**实现任务**:
1. 数据安全
   - localStorage 数据 Base64 编码
   - 输入内容 XSS 防护
   - 数据校验和（checksum）验证

2. 错误处理
   - localStorage 配额超限处理
   - 数据损坏恢复机制
   - 友好的错误提示 UI

3. 数据完整性
   - 数据写入前验证
   - 版本号检查
   - 数据备份提醒（7 天一次）

**技术要点**:
- 使用 Error Boundary 捕获组件错误
- localStorage 操作包裹在 try-catch
- 提供"安全模式"启动选项

**验收标准**:
- ✅ 通过基础 XSS 注入测试
- ✅ localStorage 满时有清晰提示
- ✅ 数据损坏时能降级处理

### Phase 6: Performance Optimization & Polish (性能优化与打磨)

**目标**: 达到性能指标，提升用户体验

**优化任务**:
1. 性能优化
   - 使用 React.memo 优化重渲染
   - 使用 useMemo/useCallback 优化计算
   - 代码分割（React.lazy）
   - 图片优化（使用 SVG 或 WebP）

2. 体验优化
   - 加载态、骨架屏
   - 过渡动画优化
   - 键盘快捷键支持
   - 无障碍改进（ARIA、语义化 HTML）

3. 打包优化
   - Tree-shaking 配置
   - 压缩优化
   - Chunk 分割策略

**技术要点**:
- Lighthouse 性能测试
- Bundle Analyzer 分析体积
- 浏览器 DevTools 性能分析

**验收标准**:
- ✅ Lighthouse 性能分数 > 90
- ✅ 打包体积 < 500KB (gzipped)
- ✅ 首屏加载 < 2s (3G)
- ✅ 交互响应 < 100ms

## Testing Strategy

### 测试层次

1. **单元测试** (60% 覆盖率目标)
   - 所有工具函数（utils/）
   - 所有自定义 Hooks（hooks/）
   - 关键业务逻辑（进度计算、数据验证）

2. **组件测试** (核心组件)
   - ChecklistItem - 勾选/取消勾选行为
   - TrainingLog - 日志添加/显示逻辑
   - Dashboard - 角色切换、技能展示

3. **E2E 测试** (关键路径)
   - 首次使用流程
   - 完成一个验收标准的完整流程
   - 数据持久化验证（刷新页面后恢复）

### 测试工具

- **Vitest**: 单元测试和组件测试
- **React Testing Library**: 组件交互测试
- **Playwright** (可选): E2E 测试

## Risk Mitigation

### 技术风险

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| localStorage 容量不足 | 高 | 实现日志数量限制（最多 500 条），提供导出功能 |
| 数据迁移失败 | 中 | 保留旧版本数据备份，提供手动恢复选项 |
| 浏览器兼容性 | 中 | 使用 Vite 的 browserslist 配置，添加必要的 polyfill |
| 性能问题（大量数据渲染） | 低 | 使用虚拟滚动（如果日志超过 100 条） |

### 产品风险

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| 用户数据丢失 | 高 | 定期提醒导出数据，实现数据校验机制 |
| 学习曲线过高 | 中 | 首次使用引导，清晰的 UI 提示 |
| 移动端体验差 | 中 | Mobile-first 设计，充分测试移动端 |

## Dependencies

### 生产依赖

```json
{
  "react": "^18.2.0",
  "react-dom": "^18.2.0"
}
```

### 开发依赖

```json
{
  "vite": "^5.0.0",
  "tailwindcss": "^3.4.0",
  "postcss": "^8.4.0",
  "autoprefixer": "^10.4.0",
  "vitest": "^1.0.0",
  "@testing-library/react": "^14.0.0",
  "@testing-library/jest-dom": "^6.0.0",
  "eslint": "^8.0.0",
  "eslint-plugin-react": "^7.33.0"
}
```

### 依赖说明

- **为什么不用 Redux/MobX**: 全局状态不超过 5 个（当前角色、当前技能、视图模式、技能数据、日志数据），使用 React Context + Hooks 足够
- **为什么不用 React Router**: 单页面应用，视图切换通过状态控制即可
- **为什么不用 UI 库**: 保持完全自主可控，符合宪章要求

## Deployment

### 构建流程

```bash
# 开发环境
npm run dev

# 生产构建
npm run build

# 预览生产构建
npm run preview
```

### 部署方案

1. **静态网站托管**
   - GitHub Pages
   - Netlify
   - Vercel

2. **本地运行**
   - 直接打开 `dist/index.html`
   - 使用 Live Server 等本地服务器

### 版本管理

- 使用语义化版本 (SemVer)
- 数据 Schema 版本独立管理
- 在 localStorage 中存储当前 Schema 版本号

## Success Metrics

### 开发阶段指标

- ✅ 所有 20 个 FR (Functional Requirements) 实现
- ✅ 所有 5 个 User Story 的 Acceptance Scenarios 通过
- ✅ 单元测试覆盖率 > 60%
- ✅ 无 ESLint 错误
- ✅ Lighthouse 性能分数 > 90

### 用户体验指标

- ✅ 首屏加载 < 2s (3G)
- ✅ 交互响应 < 100ms
- ✅ 打包体积 < 500KB (gzipped)
- ✅ 支持 Chrome/Edge/Safari 最新 2 个版本

## Next Steps

1. **立即执行**: Phase 0 - 搭建开发环境，生成 `research.md`
2. **后续执行**: Phase 1 - 设计数据模型，生成 `data-model.md` 和 `contracts/`
3. **最后生成**: 使用 `/speckit.tasks` 命令生成详细任务分解 (`tasks.md`)

---

**版本**: 1.0.0 | **最后更新**: 2025-11-25

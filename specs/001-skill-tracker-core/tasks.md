# Tasks: 能力刻度尺核心功能

**Input**: Design documents from `/specs/001-skill-tracker-core/`
**Prerequisites**: plan.md ✅, spec.md ✅

**Organization**: 任务按用户故事分组，支持独立实现和测试

## Format: `[ID] [P?] [Story] Description`

- **[P]**: 可并行执行（不同文件，无依赖关系）
- **[Story]**: 所属用户故事（US1, US2, US3, US4, US5）
- 包含具体文件路径

---

## Phase 0: Setup (项目初始化)

**目的**: 搭建项目基础结构和开发环境

- [ ] T001 使用 Vite 创建 React 项目 (`npm create vite@latest skill-tracker -- --template react`)
- [ ] T002 [P] 安装生产依赖：react@18.2+, react-dom@18.2+
- [ ] T003 [P] 安装开发依赖：tailwindcss, postcss, autoprefixer
- [ ] T004 [P] 安装测试依赖：vitest, @testing-library/react, @testing-library/jest-dom
- [ ] T005 配置 Tailwind CSS (`tailwind.config.js`, `postcss.config.js`)
- [ ] T006 配置 Vitest (`vite.config.js` 添加 test 配置)
- [ ] T007 [P] 配置 ESLint (`eslint-plugin-react`, `.eslintrc.js`)
- [ ] T008 创建基础目录结构 (`src/components/`, `src/hooks/`, `src/utils/`, `src/data/`, `tests/`)
- [ ] T009 清理 Vite 模板文件，创建干净的 `src/main.jsx` 和 `src/App.jsx`

**Checkpoint**: 项目初始化完成，可以运行 `npm run dev` 看到空白页面

---

## Phase 1: Foundational (基础设施)

**目的**: 实现核心基础设施，所有用户故事都依赖这些

**⚠️ CRITICAL**: 必须完成此阶段，才能开始任何用户故事

### 数据定义

- [ ] T010 [P] 创建 `src/data/careerRoles.js` - 定义职业角色静态数据
- [ ] T011 [P] 创建 `src/data/initialSkills.js` - 定义技能树静态数据（包含5级、验收标准、tips等）

### 工具函数

- [ ] T012 [P] 创建 `src/utils/storage.js` - localStorage 读写封装（含序列化/反序列化）
- [ ] T013 [P] 创建 `src/utils/dataValidation.js` - 数据验证函数（验证 schema 版本、数据完整性）
- [ ] T014 [P] 实现 `src/utils/storage.js` 中的错误处理（配额超限、权限问题）

### 自定义 Hooks

- [ ] T015 创建 `src/hooks/useLocalStorage.js` - localStorage Hook（自动同步、防抖写入）
- [ ] T016 创建 `src/hooks/useSkillProgress.js` - 技能进度计算 Hook
- [ ] T017 创建 `src/hooks/useDataMigration.js` - 数据版本迁移 Hook

### 基础组件

- [ ] T018 [P] 创建 `src/components/ProgressBar.jsx` - 进度条组件
- [ ] T019 [P] 创建 `src/components/ChecklistItem.jsx` - 可勾选验收标准组件

### 测试

- [ ] T020 [P] 为 `src/utils/storage.js` 编写单元测试
- [ ] T021 [P] 为 `src/hooks/useLocalStorage.js` 编写单元测试
- [ ] T022 [P] 为 `src/hooks/useSkillProgress.js` 编写单元测试

**Checkpoint**: 基础设施就绪，用户故事可以开始并行实现

---

## Phase 2: User Story 4 - 数据持久化与恢复 (Priority: P1) 🎯 MVP

**Goal**: 实现数据自动保存和恢复机制，这是所有其他功能的基础

**Independent Test**: 修改数据 → 关闭浏览器 → 重新打开 → 验证数据恢复

### 实现任务

- [ ] T023 [US4] 在 `src/App.jsx` 中集成 `useLocalStorage` Hook
- [ ] T024 [US4] 在 `src/App.jsx` 中集成 `useDataMigration` Hook，处理版本迁移
- [ ] T025 [US4] 实现数据 schema 版本控制逻辑（检查版本号，执行迁移）
- [ ] T026 [US4] 实现数据校验逻辑（启动时验证 localStorage 数据完整性）
- [ ] T027 [US4] 实现数据损坏时的降级处理（显示错误提示，提供重置选项）
- [ ] T028 [US4] 创建 `src/utils/exportImport.js` - 数据导入/导出工具函数
- [ ] T029 [US4] 添加数据导出功能（生成 JSON 文件下载）
- [ ] T030 [US4] 添加数据导入功能（文件上传 + 验证 + 合并）

### 测试

- [ ] T031 [P] [US4] E2E 测试：数据持久化流程（修改 → 刷新 → 验证）
- [ ] T032 [P] [US4] 单元测试：数据迁移逻辑（从 v1.0 迁移到 v1.1）
- [ ] T033 [P] [US4] 单元测试：数据损坏处理（无效 JSON、缺失字段）

**Checkpoint**: 数据持久化机制完整可用

---

## Phase 3: User Story 1 - 技能进度查看与管理 (Priority: P1) 🎯 MVP

**Goal**: 用户可以查看技能树、勾选验收标准、查看实时进度

**Independent Test**: 选择角色 → 查看技能 → 勾选标准 → 看到进度更新

### UI 组件

- [ ] T034 [P] [US1] 创建 `src/components/SkillCard.jsx` - 技能卡片组件
- [ ] T035 [P] [US1] 创建 `src/components/LevelCard.jsx` - 等级卡片组件
- [ ] T036 [US1] 创建 `src/components/Dashboard.jsx` - 主仪表盘组件

### 核心逻辑

- [ ] T037 [US1] 在 `src/App.jsx` 中实现当前技能等级计算逻辑
- [ ] T038 [US1] 在 `src/App.jsx` 中实现进度百分比计算逻辑
- [ ] T039 [US1] 实现验收标准勾选/取消勾选功能（`toggleCriteria` 函数）
- [ ] T040 [US1] 实现等级自动解锁逻辑（所有标准完成 → 解锁下一级）

### 视觉反馈

- [ ] T041 [US1] 为 `ChecklistItem` 添加勾选动画（CSS transition）
- [ ] T042 [US1] 为 `ProgressBar` 添加进度变化动画
- [ ] T043 [US1] 为当前目标等级添加高亮样式
- [ ] T044 [US1] 为已完成等级添加灰化样式

### 测试

- [ ] T045 [P] [US1] 组件测试：`ChecklistItem` 勾选行为
- [ ] T046 [P] [US1] 组件测试：`LevelCard` 渲染和交互
- [ ] T047 [P] [US1] 单元测试：进度计算逻辑
- [ ] T048 [US1] E2E 测试：完整的勾选 → 进度更新 → 等级解锁流程

**Checkpoint**: 用户可以完整地查看和管理技能进度

---

## Phase 4: User Story 3 - 职业角色切换与多技能管理 (Priority: P1) 🎯 MVP

**Goal**: 用户可以在多个职业角色间切换，查看不同技能树

**Independent Test**: 点击不同角色 → 验证技能列表更新 → 验证进度独立计算

### UI 组件

- [ ] T049 [US3] 创建 `src/components/RoleNavigator.jsx` - 左侧职业角色导航组件
- [ ] T050 [US3] 在 `Dashboard` 中集成 `RoleNavigator`

### 核心逻辑

- [ ] T051 [US3] 实现角色切换逻辑（更新当前角色状态）
- [ ] T052 [US3] 实现基于角色过滤技能列表的逻辑
- [ ] T053 [US3] 实现每个角色独立的进度计算
- [ ] T054 [US3] 实现技能快速定位功能（点击左侧技能名 → 右侧滚动到对应位置）

### 视觉优化

- [ ] T055 [US3] 添加角色切换过渡动画
- [ ] T056 [US3] 在左侧导航显示每个角色的整体完成度
- [ ] T057 [US3] 高亮当前选中的角色

### 测试

- [ ] T058 [P] [US3] 组件测试：`RoleNavigator` 渲染和点击
- [ ] T059 [US3] E2E 测试：角色切换流程

**Checkpoint**: 多角色切换功能完整可用

---

## Phase 5: User Story 2 - 练习日志记录与查看 (Priority: P2)

**Goal**: 用户可以在练习室记录学习日志并查看历史

**Independent Test**: 进入练习室 → 输入日志 → 提交 → 验证显示 → 刷新页面 → 验证保留

### UI 组件

- [ ] T060 [US2] 创建 `src/components/DetailView.jsx` - 等级详情页/练习室组件
- [ ] T061 [US2] 创建 `src/components/TrainingLog.jsx` - 练习日志组件

### 核心逻辑

- [ ] T062 [US2] 实现视图模式切换（dashboard ↔ detail）
- [ ] T063 [US2] 实现日志添加功能（带时间戳）
- [ ] T064 [US2] 实现日志列表展示（按时间倒序）
- [ ] T065 [US2] 实现 Ctrl+Enter 快捷键提交
- [ ] T066 [US2] 实现日志输入长度限制（5000 字符）

### 视觉优化

- [ ] T067 [US2] 添加日志列表滚动条优化（自定义样式）
- [ ] T068 [US2] 在"进入练习室"按钮旁显示日志数量徽章
- [ ] T069 [US2] 添加空状态提示（无日志时）

### 测试

- [ ] T070 [P] [US2] 组件测试：`TrainingLog` 日志添加
- [ ] T071 [P] [US2] 组件测试：`DetailView` 视图切换
- [ ] T072 [US2] E2E 测试：日志记录完整流程

**Checkpoint**: 练习日志功能完整可用

---

## Phase 6: User Story 5 - 能力元数据查看 (Priority: P3)

**Goal**: 用户可以查看技能的元信息（工具生态、核心技能等）

**Independent Test**: 滚动到页面底部 → 验证元数据卡片显示

### UI 组件

- [ ] T073 [US5] 创建 `src/components/MetadataPanel.jsx` - 元数据展示面板

### 核心逻辑

- [ ] T074 [US5] 在 `Dashboard` 中集成 `MetadataPanel`
- [ ] T075 [US5] 实现元数据渲染逻辑（4个卡片：类型、核心技能、工具、指标）

### 视觉优化

- [ ] T076 [US5] 为元数据卡片添加网格布局（响应式）
- [ ] T077 [US5] 为工具标签添加样式

### 测试

- [ ] T078 [P] [US5] 组件测试：`MetadataPanel` 渲染

**Checkpoint**: 元数据查看功能可用

---

## Phase 7: Security & Error Handling (安全与错误处理)

**目的**: 实现安全措施和错误处理

- [ ] T079 [P] 实现 XSS 防护（用户输入转义）
- [ ] T080 [P] 实现 localStorage 配额超限处理（提示并清理旧日志）
- [ ] T081 [P] 添加 Error Boundary 组件（捕获 React 错误）
- [ ] T082 实现"安全模式"启动选项（跳过损坏数据加载）
- [ ] T083 添加数据备份提醒（7天提示一次导出）
- [ ] T084 [P] 为所有 localStorage 操作添加 try-catch

### 测试

- [ ] T085 [P] 安全测试：XSS 注入防护验证
- [ ] T086 [P] 边界测试：localStorage 满载处理

**Checkpoint**: 安全措施和错误处理完善

---

## Phase 8: Performance & Polish (性能优化与打磨)

**目的**: 达到性能指标，提升用户体验

### 性能优化

- [ ] T087 [P] 使用 React.memo 优化组件重渲染（`SkillCard`, `LevelCard`）
- [ ] T088 [P] 使用 useMemo 优化进度计算
- [ ] T089 [P] 使用 useCallback 优化事件处理函数
- [ ] T090 添加代码分割（React.lazy）- `DetailView` 懒加载
- [ ] T091 优化 Tailwind CSS 打包（PurgeCSS 配置）

### 体验优化

- [ ] T092 [P] 添加加载态组件（Skeleton Screen）
- [ ] T093 [P] 优化动画性能（使用 transform 代替 position）
- [ ] T094 [P] 添加键盘快捷键支持（Esc 返回、Tab 导航）
- [ ] T095 添加无障碍改进（ARIA 标签、语义化 HTML）
- [ ] T096 实现响应式设计优化（移动端导航折叠）

### 性能测试

- [ ] T097 运行 Lighthouse 测试（目标 > 90 分）
- [ ] T098 使用 Bundle Analyzer 分析打包体积（目标 < 500KB）
- [ ] T099 使用 Chrome DevTools 性能分析（目标交互 < 100ms）

**Checkpoint**: 性能和体验达标

---

## Phase 9: Final Validation (最终验证)

**目的**: 确保所有功能完整可用

- [ ] T100 逐一验证所有 20 个功能需求（FR-001 ~ FR-020）
- [ ] T101 逐一验证所有 5 个用户故事的验收场景
- [ ] T102 验证所有 9 个成功标准（SC-001 ~ SC-009）
- [ ] T103 跨浏览器测试（Chrome、Safari、Edge）
- [ ] T104 移动端测试（iOS Safari、Android Chrome）
- [ ] T105 运行完整的测试套件（单元 + 组件 + E2E）
- [ ] T106 修复所有 ESLint 警告和错误
- [ ] T107 清理调试代码和 console.log

**Checkpoint**: 应用可以发布

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 0)**: 无依赖，立即开始
- **Foundational (Phase 1)**: 依赖 Setup 完成 - **阻塞所有用户故事**
- **US4 数据持久化 (Phase 2)**: 依赖 Foundational - **最高优先级 P1**
- **US1 技能进度 (Phase 3)**: 依赖 Foundational + US4 - **核心 MVP**
- **US3 角色切换 (Phase 4)**: 依赖 Foundational + US4 + US1 - **核心 MVP**
- **US2 练习日志 (Phase 5)**: 依赖 Foundational + US4 + US1 - **增值功能**
- **US5 元数据 (Phase 6)**: 依赖 Foundational - **低优先级**
- **Security (Phase 7)**: 依赖所有核心功能完成
- **Performance (Phase 8)**: 依赖所有功能完成
- **Validation (Phase 9)**: 依赖所有阶段完成

### MVP 定义

**Minimum Viable Product 包含**:
- ✅ Phase 0: Setup
- ✅ Phase 1: Foundational
- ✅ Phase 2: US4 (数据持久化)
- ✅ Phase 3: US1 (技能进度)
- ✅ Phase 4: US3 (角色切换)

**可选增强**:
- Phase 5: US2 (练习日志)
- Phase 6: US5 (元数据)
- Phase 7-9: 安全、性能、验证

### Parallel Opportunities

**Phase 0 并行任务**:
- T002, T003, T004, T007 可同时进行

**Phase 1 并行任务**:
- T010, T011 (数据定义)
- T012, T013, T014 (工具函数)
- T018, T019 (基础组件)
- T020, T021, T022 (测试)

**Phase 3 并行任务**:
- T034, T035 (UI 组件)
- T045, T046, T047 (测试)

**Phase 7 并行任务**:
- T079, T080, T081, T084, T085, T086

**Phase 8 并行任务**:
- T087, T088, T089, T092, T093, T094

---

## Task Summary

- **总任务数**: 107
- **MVP 任务**: ~70 (Phase 0-4)
- **并行机会**: ~30 任务可并行
- **预估工期**: 
  - MVP: 5-7 天（单人全职）
  - 完整版: 10-14 天（单人全职）

---

**版本**: 1.0.0 | **创建时间**: 2025-11-25

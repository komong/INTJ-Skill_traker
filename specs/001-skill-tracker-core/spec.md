# Feature Specification: 能力刻度尺核心功能

**Feature Branch**: `001-skill-tracker-core`  
**Created**: 2025-11-25  
**Status**: Draft  
**Input**: User description: "能力刻度尺核心功能：多维度技能追踪与成长可视化系统"

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - 技能进度查看与管理 (Priority: P1)

作为一名成长中的专业人士，我希望能够查看我在不同职业角色下的技能树，并通过勾选验收标准来追踪我的进度，以便清楚地了解自己当前的能力水平和下一步需要提升的方向。

**Why this priority**: 这是应用的核心功能，没有它就没有整个产品的价值。用户必须能够查看和更新自己的技能进度。

**Independent Test**: 可以通过打开应用、选择一个职业角色、查看技能列表、勾选/取消验收标准、看到实时进度更新来完整测试。

**Acceptance Scenarios**:

1. **Given** 用户打开应用, **When** 用户选择“AI产品经理”职业角色, **Then** 显示该角色关联的所有技能（如“AI代理使用”、“代理工具”）
2. **Given** 用户选择了一个技能，**When** 用户点击进入该技能详情页, **Then** 显示5个等级的完整列表，每个等级包含标题、描述、验收标准和Boss挑战
3. **Given** 用户在某个等级的验收标准列表中, **When** 用户勾选一个未完成的标准, **Then** 该标准显示为已完成状态，并且当前等级的完成度进度条实时更新
4. **Given** 用户完成了某个等级的所有验收标准, **When** 系统检测到完成度达到100%, **Then** 自动解锁下一等级，并更新主仪表盘的当前等级显示

---

### User Story 2 - 练习日志记录与查看 (Priority: P2)

作为一名持续学习者，我希望能够在每个技能等级的“练习室”中记录我的学习过程、遇到的问题和感悟，并随时回顾这些日志，以便总结经验和调整学习策略。

**Why this priority**: 这是区别于普通打卡工具的关键功能，让用户能够记录成长过程中的思考和经验，但不是核心MVP的必需功能。

**Independent Test**: 可以通过进入任意等级的练习室、输入日志内容、点击记录按钮、查看日志列表来完整测试。

**Acceptance Scenarios**:

1. **Given** 用户在某个技能等级的详情页, **When** 用户点击“进入练习室”按钮, **Then** 进入该等级的练习日志页面，显示Boss挑战、专家锦囊和历史日志列表
2. **Given** 用户在练习室的日志输入框中, **When** 用户输入内容后点击“记录”按钮, **Then** 日志以最新一条的形式显示在列表顶部，并包含时间戳
3. **Given** 用户已经记录了10条日志, **When** 用户再次进入该等级的练习室, **Then** 所有历史日志按时间倒序显示，并在“进入练习室”按钮旁显示日志数量徽章(10)
4. **Given** 用户在日志输入框中, **When** 用户按Ctrl+Enter快捷键, **Then** 日志自动提交并清空输入框

---

### User Story 3 - 职业角色切换与多技能管理 (Priority: P1)

作为一名多重职业角色的学习者，我希望能够在不同职业角色（如AI产品经理、销售）之间切换，并查看每个角色下的技能树和整体进度，以便系统地管理我的多维度能力发展。

**Why this priority**: 这是产品的差异化特色，支持多职业角色是核心价值之一，但可以先以单个角色作为MVP。

**Independent Test**: 可以通过在左侧导航栏点击不同职业角色、观察右侧内容区更新、查看进度条和数据统计来完整测试。

**Acceptance Scenarios**:

1. **Given** 用户在主页面, **When** 用户点击左侧导航栏的“销售”角色, **Then** 右侧内容区切换为销售相关的技能列表，顶部面包屑显示当前角色名称
2. **Given** 用户选择了“AI产品经理”角色, **When** 用户查看该角色下的技能列表, **Then** 显示“AI代理使用”和“代理工具”两个技能
3. **Given** 用户在某个角色页面, **When** 系统计算该角色的整体完成度, **Then** 左侧导航栏显示该角色的整体进度条和百分比
4. **Given** 用户在某个角色的技能列表中, **When** 用户点击左侧导航栏的具体技能名称, **Then** 右侧内容区滚动到该技能的详情区域

---

### User Story 4 - 数据持久化与恢复 (Priority: P1)

作为一名长期用户，我希望我的所有技能进度和练习日志能够自动保存到本地，并在下次打开应用时自动恢复，以便我不会丢失任何数据。

**Why this priority**: 数据持久化是应用的基础能力，没有它就无法实现长期追踪的价值。

**Independent Test**: 可以通过勾选几个验收标准、添加日志、关闭浏览器、重新打开应用、验证数据是否保留来完整测试。

**Acceptance Scenarios**:

1. **Given** 用户对技能进度做了任何更改, **When** 更改发生的瞬间, **Then** 数据立即同步保存到localStorage
2. **Given** 用户关闭了浏览器, **When** 用户再次打开应用, **Then** 所有之前的数据（勾选状态、日志记录）完整恢复
3. **Given** localStorage中存在老版本数据, **When** 用户打开新版本应用, **Then** 系统自动迁移数据结构到新版本格式
4. **Given** localStorage数据损坏, **When** 用户打开应用, **Then** 显示友好的错误提示，并提供“重置数据”或“尝试恢复”选项

---

### User Story 5 - 能力元数据查看 (Priority: P3)

作为一名深度用户，我希望能够查看每个技能的结构分析，包括支撑技能、工具生态、关键指标等元信息，以便更全面地理解该技能的完整图谱。

**Why this priority**: 这是增强用户体验的附加功能，不影响MVP的核心价值。

**Independent Test**: 可以通过滚动到页面底部、查看能力结构分析卡片、验证数据完整性来完整测试。

**Acceptance Scenarios**:

1. **Given** 用户在技能详情页, **When** 用户滚动到页面底部, **Then** 显示“能力结构分析”区域，包含4个卡片：能力类型、核心技能、工具生态、关键指标
2. **Given** 用户查看核心技能卡片, **When** 系统显示数据, **Then** 列出该技能的所有supportingSkills（如SPIN提问、价值呈现）
3. **Given** 用户查看工具生态卡片, **When** 系统显示数据, **Then** 以标签形式列出所有tools（如ChatGPT、Claude、Dify）

### Edge Cases

- **localStorage配额超限**: 当用户的日志记录超过localStorage容量时，系统应提示用户导出数据并清理老旧记录
- **空数据状态**: 首次使用的用户应该看到所有技能的默认未完成状态，且有明确的引导
- **长文本输入**: 用户在日志中输入超过5000字符时，应显示字数限制提示
- **快速切换角色**: 用户快速点击多个职业角色时，应确保界面不出现闪烁或数据错乱
- **浏览器兼容性**: 在不支持localStorage的环境中，应降级为内存模式并明确告知用户
- **同时打开多个Tab**: 用户在多个浏览器Tab中同时打开应用并修改数据时，应通过storage事件同步数据
- **特殊字符输入**: 用户输入Emoji、HTML标签或脚本代码时，应进行适当转义防止XSS

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

**核心显示能力:**
- **FR-001**: 系统必须显示所有预定义的职业角色（AI产品经理、销售）列表
- **FR-002**: 系统必须显示每个职业角色关联的技能列表
- **FR-003**: 系统必须显示每个技能的5个等级，每个等级包含：等级号、标题、描述、Boss挑战、验收标准列表
- **FR-004**: 系统必须实时计算并显示用户当前的技能等级（基于已完成的验收标准）
- **FR-005**: 系统必须实时计算并显示每个技能的整体完成度百分比

**交互能力:**
- **FR-006**: 用户必须能够勾选/取消勾选任意验收标准
- **FR-007**: 用户必须能够点击“进入练习室”按钮进入该等级的详情页
- **FR-008**: 用户必须能够在练习室中输入并保存日志记录
- **FR-009**: 用户必须能够在左侧导航栏切换不同职业角色
- **FR-010**: 用户必须能够通过点击左侧导航栏的技能名称快速定位到该技能

**数据持久化:**
- **FR-011**: 系统必须实时将所有用户操作（勾选、日志）保存到localStorage
- **FR-012**: 系统必须在启动时从localStorage恢复所有用户数据
- **FR-013**: 系统必须支持数据版本迁移（从老版本格式升级到新版本）

**视觉反馈:**
- **FR-014**: 系统必须在用户勾选验收标准时显示视觉反馈（勾选动画、进度条更新）
- **FR-015**: 系统必须高亮显示当前正在攻克的等级（与已完成/未解锁的等级区分）
- **FR-016**: 系统必须在用户完成一个等级的所有标准时显示明显的视觉反馈

**响应式设计:**
- **FR-017**: 系统必须在移动端和桌面端都能正常显示和操作
- **FR-018**: 系统必须在小屏幕设备上隐藏左侧导航栏，提供汉堡包菜单

**其他功能:**
- **FR-019**: 系统必须显示每个技能的元数据（能力类型、核心技能、工具生态、关键指标）
- **FR-020**: 系统必须在练习室中显示Boss挑战和专家锦囊

### Key Entities

- **CareerRole (职业角色)**: 代表一个职业路径，包含id、name、icon、color、description、skillIds（关联的技能ID列表）

- **Skill (技能)**: 代表一个可量化的能力领域，包含id、name、enName、icon、color、type（professional/technical）、category、description、supportingSkills、requiredKnowledge、tools、metrics、levels（等级列表）

- **Level (等级)**: 代表技能的一个阶段，包含lvl（1-5）、title、desc、bossChallenge、tips（提示列表）、logs（日志列表）、criteria（验收标准列表）

- **Criteria (验收标准)**: 代表一个可验证的成就，包含id、text（描述）、done（完成状态）

- **Log (练习日志)**: 代表用户的一条学习记录，包含id、date（时间戳）、text（内容）

**关系:**
- CareerRole 包含多个 Skill（通过skillIds关联）
- Skill 包含5个 Level
- Level 包含多个 Criteria 和多个 Log

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

**性能指标:**
- **SC-001**: 首屏加载时间小于2秒（3G网络环境）
- **SC-002**: 任何用户交互（勾选、切换）响应时间小于100ms
- **SC-003**: 应用打包后总体积小于500KB (gzipped)

**可用性指标:**
- **SC-004**: 90%的新用户在首次使用时3分钟内成功勾选至少一个验收标准
- **SC-005**: 95%的用户能够在不查看帮助文档的情况下找到练习室入口
- **SC-006**: 用户在关闭并重新打开应用后，100%的数据得到恢复

**业务指标:**
- **SC-007**: 用户平均每周至少记录3条练习日志
- **SC-008**: 用户在使用应用后，对自己能力水平的认知清晰度提升至少一个等级
- **SC-009**: 80%的用户会持续使用超过1个月

# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2026-04-01

### Added
- 初始化项目结构
- 实现核心数据模型（World, Character, Event, Simulation）
- 实现StateStore状态存储（SQLite后端）
- 实现EventBus事件总线（发布/订阅模式）
- 实现MasterOrchestrator协调器（模拟生命周期管理）
- 完整的单元测试和集成测试
- 测试覆盖率达到80%

### Technical Details
- 使用Pydantic v2进行数据验证
- 使用asyncio实现异步操作
- 使用SQLite作为数据持久化方案
- 采用TDD开发方法

### Documentation
- 核心框架设计文档
- 国内大模型接入文档
- 第一阶段开发计划
- API接口设计文档（待完成）

# Push Him To You | 把他推向你

[English](#english) | [中文](#中文)

---

<a name="english"></a>

## English

### Overview

**"Push Him To You"** is an innovative AI-driven fate simulation and novel generation system. It is not merely a writing tool, but a "life simulator" — after users set the initial conditions of characters and the world background, the system acts like a god's eye view, allowing characters to naturally grow and change based on their own characteristics and environmental factors, ultimately being pushed by fate toward their destined ending.

### ✨ Key Features

| Feature | Description |
|---------|-------------|
| **Multi-LLM Collaboration** | Different large models each perform their own duties, simulating different dimensions of the world |
| **Dynamic Character Growth** | Based on psychological models (Big Five), characters truly change due to environment and events |
| **Fate Engine** | Driven by causality rather than preset plots |
| **God's Eye View** | Observe character life trajectories, capture key moments |
| **Perspective Switching** | Switch to any character's perspective at any time to regenerate narrative |
| **Spark Capture** | Automatically identify and save touching, meaningful moments |

### 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    User Interface Layer                          │
│  [Settings] [World Building] [Character Creation] [Simulation]  │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Orchestration Layer                           │
│  Task Scheduling │ State Management │ Conflict Resolution        │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Agent Layer                                   │
│  WorldBuilder │ CharacterGen │ FateEngine │ Narrator            │
│  EmotionalRenderer │ EventGen │ RelationNet │ SparkCapture       │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Model Layer (LLM Gateway)                     │
│  Claude │ GPT-4 │ Gemini │ Wenxin │ Tongyi │ ...                │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Data Layer                                    │
│  Vector DB │ Graph DB (Neo4j) │ Time-series DB │ Spark Memory    │
└─────────────────────────────────────────────────────────────────┘
```

### 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | React + TypeScript, Ant Design / shadcn/ui, Zustand, D3.js, ECharts |
| **Backend** | Python + FastAPI, Celery + Redis |
| **AI/ML** | LiteLLM, OpenAI text-embedding-3-small / BGE, Milvus / Chroma |
| **Database** | PostgreSQL, Neo4j, TimescaleDB |
| **Infrastructure** | Docker, Kubernetes (optional), Prometheus + Grafana |

### 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/your-username/push-him-to-you.git
cd push-him-to-you

# Start with Docker Compose
docker-compose up -d

# Or install manually
pip install -r backend/requirements.txt
cd frontend && npm install
```

### 📁 Project Structure

```
push-him-to-you/
├── frontend/                # React frontend application
│   ├── src/
│   │   ├── components/     # UI components
│   │   ├── stores/         # State management
│   │   └── services/       # API services
│   └── package.json
│
├── backend/                 # Python backend application
│   ├── app/
│   │   ├── agents/         # 8 specialized agents
│   │   ├── core/           # Orchestrator & config
│   │   ├── models/         # Data models
│   │   └── services/       # LLM gateway, vector store
│   └── requirements.txt
│
├── docs/                    # Documentation
│   ├── 把他推向你-系统设计文档.md
│   └── Push-Him-To-You-System-Design-Document.md
│
├── docker-compose.yml
└── README.md
```

### 🤖 Agent System

The system includes 8 specialized agents:

| Agent | Role | Primary Model |
|-------|------|---------------|
| **WorldBuilder** | Creates and maintains story world settings | Claude-3-Opus |
| **CharacterGenerator** | Manages character attributes and growth | GPT-4 |
| **FateEngine** | Advances causal chains and generates events | Claude-3-Opus |
| **Narrator** | Generates narrative text | Claude-3-Opus |
| **EmotionalRenderer** | Analyzes and adjusts emotional tone | Claude-3-Sonnet |
| **EventGenerator** | Creates life events | GPT-4 |
| **RelationNetwork** | Manages character relationships | GPT-4 |
| **SparkCapture** | Identifies meaningful moments | Claude-3-Opus |

### 📊 Character Model

Characters are built on the **Big Five Personality Model (OCEAN)**:

- **O**penness - Imagination, aesthetics, curiosity
- **C**onscientiousness - Organization, discipline, reliability
- **E**xtraversion - Sociability, assertiveness, energy
- **A**greeableness - Trust, cooperation, compassion
- **N**euroticism - Emotional stability, anxiety, vulnerability

### 📖 Documentation

- [System Design Document (Chinese)](./把他推向你-系统设计文档.md)
- [System Design Document (English)](./Push-Him-To-You-System-Design-Document.md)

### 🗺️ Roadmap

#### v1.1 (Short-term)
- [ ] Support more LLM providers
- [ ] Character relationship visualization
- [ ] Multi-language narrative support
- [ ] Life retrospective functionality

#### v2.0 (Mid-term)
- [ ] Multi-character parallel simulation
- [ ] Complex relationship network evolution
- [ ] Social group simulation
- [ ] User intervention mechanism

#### v3.0 (Long-term)
- [ ] Multi-world cross-narrative
- [ ] AI-assisted creative suggestions
- [ ] Community sharing platform
- [ ] VR/AR immersive experience

### 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<a name="中文"></a>

## 中文

### 项目概述

**"把他推向你"** 是一个创新性的AI驱动命运模拟与小说生成系统。它不仅仅是一个写作工具，更是一个"人生模拟器"——用户设定好人物的初始条件和世界背景后，系统会像上帝视角一样，让人物根据自身特点和环境因素自然成长、变化，最终被命运推向注定的结局。

### ✨ 核心特性

| 特性 | 描述 |
|------|------|
| **多LLM协作** | 不同大模型各司其职，模拟世界的不同维度 |
| **动态人物成长** | 基于心理学模型（大五人格），人物会因环境、事件而真实改变 |
| **命运引擎** | 因果关系驱动，而非预设剧情 |
| **上帝视角** | 观察人物人生轨迹，捕捉关键时刻 |
| **视角切片** | 随时切换任一人物视角重新生成叙事 |
| **闪光记录** | 自动识别并保存感人、有意义的瞬间 |

### 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────────────┐
│                    用户界面层 (UI Layer)                         │
│  [参数设置] [世界构建] [人物创建] [人生模拟] [小说生成]          │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    协调引擎层 (Orchestration Layer)              │
│  任务调度 │ 状态管理 │ 冲突解决 │ 结果整合                       │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    智能体层 (Agent Layer)                        │
│  世界构建Agent │ 人物塑造Agent │ 命运引擎Agent │ 叙事生成Agent   │
│  情感渲染Agent │ 事件生成Agent │ 关系网络Agent │ 闪光捕捉Agent   │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    模型连接层 (Model Layer)                      │
│  Claude │ GPT-4 │ Gemini │ 文心 │ 通义 │ ...                    │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    数据存储层 (Data Layer)                       │
│  向量数据库 │ 关系图谱(Neo4j) │ 时序事件DB │ 闪光记忆库          │
└─────────────────────────────────────────────────────────────────┘
```

### 🛠️ 技术栈

| 层级 | 技术 |
|------|------|
| **前端** | React + TypeScript, Ant Design / shadcn/ui, Zustand, D3.js, ECharts |
| **后端** | Python + FastAPI, Celery + Redis |
| **AI/ML** | LiteLLM, OpenAI text-embedding-3-small / BGE, Milvus / Chroma |
| **数据库** | PostgreSQL, Neo4j, TimescaleDB |
| **基础设施** | Docker, Kubernetes (可选), Prometheus + Grafana |

### 🚀 快速开始

```bash
# 克隆仓库
git clone https://github.com/your-username/push-him-to-you.git
cd push-him-to-you

# 使用 Docker Compose 启动
docker-compose up -d

# 或手动安装
pip install -r backend/requirements.txt
cd frontend && npm install
```

### 📁 项目结构

```
push-him-to-you/
├── frontend/                # React 前端应用
│   ├── src/
│   │   ├── components/     # UI 组件
│   │   ├── stores/         # 状态管理
│   │   └── services/       # API 服务
│   └── package.json
│
├── backend/                 # Python 后端应用
│   ├── app/
│   │   ├── agents/         # 8个专业化智能体
│   │   ├── core/           # 协调器与配置
│   │   ├── models/         # 数据模型
│   │   └── services/       # LLM网关、向量存储
│   └── requirements.txt
│
├── docs/                    # 文档
│   ├── 把他推向你-系统设计文档.md
│   └── Push-Him-To-You-System-Design-Document.md
│
├── docker-compose.yml
└── README.md
```

### 🤖 智能体系统

系统包含8个专业化智能体：

| 智能体 | 角色 | 主要模型 |
|--------|------|----------|
| **WorldBuilder** | 创建和维护故事世界设定 | Claude-3-Opus |
| **CharacterGenerator** | 管理人物属性和成长 | GPT-4 |
| **FateEngine** | 推进因果链条，生成事件 | Claude-3-Opus |
| **Narrator** | 生成叙事文本 | Claude-3-Opus |
| **EmotionalRenderer** | 分析和调整情感基调 | Claude-3-Sonnet |
| **EventGenerator** | 创造人生事件 | GPT-4 |
| **RelationNetwork** | 管理人物关系网络 | GPT-4 |
| **SparkCapture** | 识别有意义时刻 | Claude-3-Opus |

### 📊 人物模型

人物基于**大五人格模型 (OCEAN)** 构建：

- **O**penness (开放性) - 想象力、审美、好奇心
- **C**onscientiousness (尽责性) - 条理性、自律、可靠性
- **E**xtraversion (外向性) - 社交性、自信、活力
- **A**greeableness (宜人性) - 信任、合作、同情心
- **N**euroticism (神经质) - 情绪稳定性、焦虑、脆弱性

### 📖 文档

- [系统设计文档 (中文)](./把他推向你-系统设计文档.md)
- [系统设计文档 (英文)](./Push-Him-To-You-System-Design-Document.md)

### 🗺️ 路线图

#### v1.1 (短期)
- [ ] 支持更多LLM提供商
- [ ] 人物关系可视化
- [ ] 多语言叙事支持
- [ ] 人生回溯功能

#### v2.0 (中期)
- [ ] 多人物并行模拟
- [ ] 复杂关系网络演化
- [ ] 社会群体模拟
- [ ] 用户干预机制

#### v3.0 (长期)
- [ ] 多世界交叉叙事
- [ ] AI辅助创作建议
- [ ] 社区分享平台
- [ ] VR/AR沉浸体验

### 🤝 参与贡献

欢迎参与贡献！请随时提交 Pull Request。

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

### 📄 许可证

本项目采用 MIT 许可证 - 详情请查看 [LICENSE](LICENSE) 文件。

---

## Core Innovation | 核心创新

1. **Dynamic Character Growth** | **动态人物成长**: Based on psychological models, characters truly change due to environment and events | 基于心理学模型，人物会因环境、事件而真实改变

2. **Fate Engine** | **命运引擎**: Driven by causality rather than preset plots | 因果关系驱动而非预设剧情

3. **Multi-LLM Collaboration** | **多LLM协作**: Different models each perform their own duties, simulating different dimensions of the world | 不同模型各司其职，模拟世界的不同维度

4. **Spark Capture** | **闪光捕捉**: Automatically identifies meaningful moments in life | 自动识别人生中有意义的瞬间

5. **Perspective Switching** | **视角切片**: Switch to any character's perspective at any time to regenerate narrative | 随时切换任一人物视角重新生成叙事

---

*"Fate is not a preset script, but a trajectory woven from countless choices. We are merely observers, recording the most shining moments in the journey toward the endpoint."*

*"命运不是预设的剧本，而是无数选择交织的轨迹。我们只是观察者，记录那些被推向终点的旅程中，最闪光的瞬间。"*

---

**Document Version | 文档版本**: v1.0  
**Creation Date | 创建日期**: 2026-04-01  
**Author | 作者**: 仲夏梦之夜和TREA
